#!/usr/bin/env python3
"""Fine-tune the MaxToki foundational model on heart-development trajectories.

This is the first heart-development fine-tune (no prior heart-specific weights
exist). Training starts from the foundational 94M LLaMA model directly.
After a successful run the saved model becomes the "prior heart weights" for
future fine-tuning rounds.

The model learns two target types from the same paragraph format:

- cell-token prediction  — cross entropy over response gene tokens
- timelapse prediction   — MSE against numeric developmental timelapse tokens
                           (units: PCW × 10, i.e. tenths of post-conception week)

The custom trainer keeps those components separate for logging while optimising
their mixed batch loss, identical in structure to the brain-aging trainer.

Timelapse normalisation
-----------------------
MSE is computed on timelapse values normalised to [0, 10] relative to the
maximum timelapse in the token dictionary (same as the aging trainer). Since
PCW × 10 timelapse values are small integers (1–37 for up to 3.7 PCW gaps),
the normalisation keeps gradients comparable to the aging runs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import random
import re
from pathlib import Path

import numpy as np
import torch
import transformers
from datasets import disable_caching, load_from_disk
from safetensors.torch import load_file

from utils import load_token_dictionary
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from transformers import Trainer, TrainingArguments

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba-maxtoki-heart-dev")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-maxtoki-heart-dev")
disable_caching()

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
_SHARED = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data")

DEFAULT_DATA_ROOT = _DATA / "finetuning_heart_dev"
DEFAULT_TOKEN_DICT = _SHARED / "token_dictionary_aging_gc95M.pkl"
DEFAULT_FOUNDATIONAL_MODEL = _SHARED / "foundational_94M_model"
DEFAULT_OUTPUT_DIR = DEFAULT_DATA_ROOT / "model"


# ---------------------------------------------------------------------------
# Data collator
# ---------------------------------------------------------------------------

class MaxTokiDataCollator:
    """Pad training examples containing input_ids, attention_mask, and loss_mask."""

    def __init__(self, pad_token_id: int = 0):
        self.pad_token_id = pad_token_id

    def __call__(self, features):
        input_ids = [torch.as_tensor(f["input_ids"], dtype=torch.long) for f in features]
        attention_mask = [torch.as_tensor(f["attention_mask"], dtype=torch.long) for f in features]
        loss_mask = [torch.as_tensor(f["loss_mask"], dtype=torch.long) for f in features]
        return {
            "input_ids": pad_sequence(input_ids, batch_first=True,
                                      padding_value=self.pad_token_id),
            "attention_mask": pad_sequence(attention_mask, batch_first=True, padding_value=0),
            "loss_mask": pad_sequence(loss_mask, batch_first=True, padding_value=0),
        }


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class PredModel(nn.Module):
    """LLaMA backbone plus scalar timelapse head (same architecture as aging model)."""

    def __init__(self, cf_model, config, output_size: int = 1):
        super().__init__()
        self.config = config
        self.linear1 = nn.Linear(config.hidden_size, output_size)
        self.cf = cf_model

    def forward(self, input_ids, attention_mask=None):
        outputs = self.cf(input_ids=input_ids, attention_mask=attention_mask,
                          output_hidden_states=True)
        mse_out = self.linear1(outputs["hidden_states"][-1][:, :])
        return mse_out, outputs


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------

class MaxTokiHeartDevTrainer(Trainer):
    """Trainer implementing the MaxToki mixed CE + timelapse-MSE loss for heart dev."""

    def __init__(self, *args, token_dictionary: dict, **kwargs):
        self.token_dictionary = token_dictionary
        self.reverse_numeric_token_dictionary: dict[int, float] = {}
        numeric_timelapses = []
        for key, value in token_dictionary.items():
            try:
                numeric_value = float(key)
            except (TypeError, ValueError):
                continue
            self.reverse_numeric_token_dictionary[int(value)] = numeric_value
            numeric_timelapses.append(numeric_value)
        if not numeric_timelapses:
            raise ValueError("Token dictionary does not contain numeric timelapse tokens.")
        self.max_timelapse = max(numeric_timelapses)
        self.eoq_token_id = token_dictionary["<eoq>"]
        self.bos_token_id = token_dictionary["<bos>"]
        self.train_component_sums = self.empty_component_sums()
        self.eval_component_sums = self.empty_component_sums()
        super().__init__(*args, **kwargs)

    @staticmethod
    def empty_component_sums() -> dict[str, float]:
        return {
            "ce_loss_sum": 0.0,
            "ce_token_count": 0.0,
            "mse_loss_sum": 0.0,
            "mse_token_count": 0.0,
            "timelapse_abs_error_sum": 0.0,
            "timelapse_sq_error_sum": 0.0,
            "timelapse_count": 0.0,
        }

    @staticmethod
    def update_component_sums(target: dict[str, float], source: dict[str, float]) -> None:
        for key, value in source.items():
            target[key] = target.get(key, 0.0) + float(value)

    def finalize_component_sums(self, sums: dict[str, float], prefix: str) -> dict[str, float]:
        metrics = {}
        if sums["ce_token_count"] > 0:
            metrics[f"{prefix}_ce_loss"] = sums["ce_loss_sum"] / sums["ce_token_count"]
        if sums["mse_token_count"] > 0:
            metrics[f"{prefix}_mse_loss"] = sums["mse_loss_sum"] / sums["mse_token_count"]
        if sums["timelapse_count"] > 0:
            # Timelapse in PCW (divide dev_time_num unit by 10)
            metrics[f"{prefix}_timelapse_mae_pcw"] = (
                sums["timelapse_abs_error_sum"] / sums["timelapse_count"] / 10.0
            )
            metrics[f"{prefix}_timelapse_rmse_pcw"] = math.sqrt(
                sums["timelapse_sq_error_sum"] / sums["timelapse_count"]
            ) / 10.0
        return metrics

    def compute_loss_components(self, model, inputs):
        """Compute mixed CE / MSE loss for one batch."""
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        loss_mask = inputs.get("loss_mask", attention_mask)
        labels = input_ids

        batch_size, seq_len = input_ids.size()
        eoq_positions = (input_ids == self.eoq_token_id).float()
        first_eoq_pos = eoq_positions.argmax(dim=1)
        after_eoq_idx = first_eoq_pos + 1
        valid_pos = after_eoq_idx < seq_len

        after_eoq_token = torch.zeros(batch_size, dtype=torch.long, device=input_ids.device)
        after_eoq_token[valid_pos] = input_ids[
            torch.arange(batch_size, device=input_ids.device),
            after_eoq_idx[valid_pos],
        ]
        is_cell_mask = after_eoq_token == self.bos_token_id

        preds_mse, output_ce = model(input_ids=input_ids, attention_mask=attention_mask)
        logits_ce = output_ce["logits"][:, :-1, :]
        preds_mse = preds_mse[:, :-1]
        labels = labels[:, 1:]
        loss_mask = loss_mask[:, 1:]

        loss_sum = torch.tensor(0.0, dtype=preds_mse.dtype, device=input_ids.device)
        count = 0.0
        component_sums = self.empty_component_sums()

        # Cell-token CE branch
        idx_cell = is_cell_mask.nonzero(as_tuple=True)[0]
        if idx_cell.numel() > 0:
            logits_cell = logits_ce[idx_cell]
            labels_cell = labels[idx_cell]
            mask_cell = loss_mask[idx_cell].bool()
            logits_masked = logits_cell.reshape(-1, logits_cell.size(-1))[mask_cell.reshape(-1)]
            labels_masked = labels_cell.reshape(-1)[mask_cell.reshape(-1)]
            if labels_masked.numel() > 0:
                ce_losses = torch.nn.functional.cross_entropy(
                    logits_masked, labels_masked, reduction="none"
                )
                ce_loss = ce_losses.mean()
                n_cell = float(idx_cell.numel())
                loss_sum = loss_sum + ce_loss * n_cell
                count += n_cell
                component_sums["ce_loss_sum"] += float(ce_losses.detach().sum().float().cpu())
                component_sums["ce_token_count"] += float(ce_losses.numel())

        # Timelapse MSE branch (timelapse in dev_time_num units = PCW × 10)
        idx_non_cell = (~is_cell_mask).nonzero(as_tuple=True)[0]
        if idx_non_cell.numel() > 0:
            preds_nc = preds_mse[idx_non_cell]
            labels_nc = labels[idx_non_cell]
            mask_nc = loss_mask[idx_non_cell].bool()
            preds_masked = preds_nc.reshape(-1)[mask_nc.reshape(-1)]
            label_tokens = labels_nc.reshape(-1)[mask_nc.reshape(-1)]
            if label_tokens.numel() > 0:
                numeric_labels = [
                    self.reverse_numeric_token_dictionary[int(token_id)]
                    for token_id in label_tokens.detach().cpu().tolist()
                ]
                labels_float = torch.tensor(
                    numeric_labels, dtype=preds_masked.dtype, device=input_ids.device
                )
                preds_norm = preds_masked / self.max_timelapse * 10.0
                labels_norm = labels_float / self.max_timelapse * 10.0
                mse_losses = torch.nn.functional.mse_loss(
                    preds_norm, labels_norm, reduction="none"
                )
                mse_loss = mse_losses.mean()
                n_non_cell = float(idx_non_cell.numel())
                loss_sum = loss_sum + mse_loss * n_non_cell
                count += n_non_cell
                raw_errors = preds_masked.detach() - labels_float.detach()
                component_sums["mse_loss_sum"] += float(
                    mse_losses.detach().sum().float().cpu()
                )
                component_sums["mse_token_count"] += float(mse_losses.numel())
                component_sums["timelapse_abs_error_sum"] += float(
                    raw_errors.abs().sum().float().cpu()
                )
                component_sums["timelapse_sq_error_sum"] += float(
                    (raw_errors ** 2).sum().float().cpu()
                )
                component_sums["timelapse_count"] += float(raw_errors.numel())

        if count == 0:
            raise ValueError("No CE or MSE loss terms were available for this batch.")

        loss = loss_sum / count
        return loss, output_ce, component_sums

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        loss, output_ce, component_sums = self.compute_loss_components(model, inputs)
        if model.training:
            self.update_component_sums(self.train_component_sums, component_sums)
        if return_outputs:
            return loss, output_ce
        return loss

    def prediction_step(self, model, inputs, prediction_loss_only, ignore_keys=None):
        inputs = self._prepare_inputs(inputs)
        with torch.no_grad():
            loss, _, component_sums = self.compute_loss_components(model, inputs)
        self.update_component_sums(self.eval_component_sums, component_sums)
        return loss.detach(), None, None

    def evaluate(self, eval_dataset=None, ignore_keys=None, metric_key_prefix: str = "eval"):
        self.eval_component_sums = self.empty_component_sums()
        metrics = super().evaluate(
            eval_dataset=eval_dataset, ignore_keys=ignore_keys,
            metric_key_prefix=metric_key_prefix,
        )
        component_metrics = self.finalize_component_sums(
            self.eval_component_sums, metric_key_prefix
        )
        if component_metrics:
            metrics.update(component_metrics)
            self.log(metrics)
        self.eval_component_sums = self.empty_component_sums()
        return metrics

    def log(self, logs: dict[str, float], start_time: float | None = None) -> None:
        if not any(key.startswith("eval_") for key in logs):
            train_metrics = self.finalize_component_sums(
                self.train_component_sums, "train"
            )
            if train_metrics:
                logs.update(train_metrics)
                self.train_component_sums = self.empty_component_sums()
        super().log(logs, start_time)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def setup_model(
    foundational_model_path: Path,
    token_dictionary: dict,
    prior_model_safetensors: Path | None,
    rope_factor: float,
):
    """Load the foundational LLaMA model, optionally applying prior heart weights.

    For the first heart-development fine-tune ``prior_model_safetensors`` is
    None and training starts directly from the foundational model. After the
    first run, the resulting ``model.safetensors`` becomes the prior weights
    for subsequent rounds.
    """
    config = transformers.LlamaConfig.from_pretrained(str(foundational_model_path))
    original_max_pos = int(getattr(config, "max_position_embeddings", 4096))
    rope_theta = 10000.0
    if isinstance(getattr(config, "rope_scaling", None), dict):
        rope_theta = config.rope_scaling.get("rope_theta", rope_theta)
    config.rope_scaling = {
        "rope_type": "dynamic",
        "factor": rope_factor,
        "original_max_position_embeddings": original_max_pos,
        "rope_theta": rope_theta,
    }
    config.max_position_embeddings = int(original_max_pos * rope_factor)

    cf_model = transformers.LlamaForCausalLM.from_pretrained(
        str(foundational_model_path), config=config
    )
    cf_model.resize_token_embeddings(len(token_dictionary))
    model = PredModel(cf_model, config)

    if prior_model_safetensors is not None:
        state_dict = load_file(str(prior_model_safetensors), device="cpu")
        missing, unexpected = model.load_state_dict(state_dict, strict=False)
        print(f"Loaded prior weights from {prior_model_safetensors}")
        print(f"  Missing keys: {len(missing)}; unexpected keys: {len(unexpected)}")
    else:
        print("No prior heart-dev weights provided — starting from foundational model.")

    return model, config


def freeze_transformer_layers(model: nn.Module, freeze_layers: int) -> None:
    if freeze_layers <= 0:
        return
    for name, param in model.named_parameters():
        parts = name.split(".")
        if "layers" not in parts:
            continue
        layer_pos = parts.index("layers") + 1
        if (layer_pos < len(parts)
                and parts[layer_pos].isdigit()
                and int(parts[layer_pos]) < freeze_layers):
            param.requires_grad = False


def latest_checkpoint(output_dir: Path) -> str | None:
    if not output_dir.exists():
        return None
    checkpoints = []
    for path in output_dir.glob("checkpoint-*"):
        match = re.search(r"checkpoint-(\d+)$", path.name)
        if match:
            checkpoints.append((int(match.group(1)), path))
    return str(sorted(checkpoints)[-1][1]) if checkpoints else None


def limit_dataset(dataset, max_samples: int | None, seed: int, shuffle: bool):
    if max_samples is None or len(dataset) <= max_samples:
        return dataset
    if shuffle:
        dataset = dataset.shuffle(seed=seed)
    return dataset.select(range(max_samples))


def step_count(
    train_size: int, per_device_batch_size: int,
    gradient_accumulation_steps: int, world_size: int,
) -> int:
    global_batch_size = max(1, per_device_batch_size * gradient_accumulation_steps * world_size)
    return max(1, math.ceil(train_size / global_batch_size))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fine-tune MaxToki on heart-development trajectories."
    )
    parser.add_argument(
        "--train-dataset", type=Path,
        default=DEFAULT_DATA_ROOT / "trajectories/train/train_heart_dev_masked.dataset",
    )
    parser.add_argument(
        "--val-dataset", type=Path,
        default=DEFAULT_DATA_ROOT / "trajectories/val/val_heart_dev_masked.dataset",
    )
    parser.add_argument("--token-dictionary", type=Path, default=DEFAULT_TOKEN_DICT)
    parser.add_argument("--foundational-model", type=Path, default=DEFAULT_FOUNDATIONAL_MODEL)
    parser.add_argument(
        "--prior-model-safetensors", type=Path, default=None,
        help=(
            "Optional prior heart-dev model weights (.safetensors). "
            "Leave unset for the first fine-tuning round (starts from foundational model)."
        ),
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--run-prefix", default="heart_dev_finetune_2026_05_22",
    )
    parser.add_argument("--max-train-samples", type=int, default=500_000)
    parser.add_argument("--max-val-samples", type=int, default=10_000)
    parser.add_argument("--shuffle-before-select", action="store_true")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--per-device-train-batch-size", type=int, default=1)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=0.00016)
    parser.add_argument("--warmup-ratio", type=float, default=0.007)
    parser.add_argument("--weight-decay", type=float, default=0.044)
    parser.add_argument("--freeze-layers", type=int, default=0)
    parser.add_argument("--rope-factor", type=float, default=4.0)
    parser.add_argument("--save-fraction", type=float, default=0.01)
    parser.add_argument("--logging-fraction", type=float, default=0.001)
    parser.add_argument("--eval-fraction", type=float, default=0.02)
    parser.add_argument("--do-eval", action="store_true")
    parser.add_argument("--save-total-limit", type=int, default=3)
    parser.add_argument("--report-to", default="none", choices=["none", "wandb"])
    parser.add_argument("--wandb-project", default="heart_dev_finetune")
    parser.add_argument("--deepspeed", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--local_rank", type=int, default=-1)
    args = parser.parse_args()

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    if args.report_to == "wandb":
        os.environ.setdefault("WANDB_MODE", "offline")
        os.environ.setdefault("WANDB_PROJECT", args.wandb_project)

    seed_everything(args.seed)
    world_size = int(os.getenv("WORLD_SIZE", "1"))
    rank = int(os.getenv("RANK", "0"))

    token_dictionary = load_token_dictionary(args.token_dictionary)
    train_dataset = load_from_disk(str(args.train_dataset))
    val_dataset = load_from_disk(str(args.val_dataset))
    train_dataset = limit_dataset(
        train_dataset, args.max_train_samples, args.seed, args.shuffle_before_select
    )
    val_dataset = limit_dataset(
        val_dataset, args.max_val_samples, args.seed + 1, args.shuffle_before_select
    )

    columns_to_keep = ["input_ids", "attention_mask", "loss_mask"]
    for name, dataset in [("train", train_dataset), ("val", val_dataset)]:
        missing = [c for c in columns_to_keep if c not in dataset.column_names]
        if missing:
            raise ValueError(
                f"{name} dataset is missing required columns: {', '.join(missing)}"
            )
    train_dataset = train_dataset.remove_columns(
        [c for c in train_dataset.column_names if c not in columns_to_keep]
    )
    val_dataset = val_dataset.remove_columns(
        [c for c in val_dataset.column_names if c not in columns_to_keep]
    )
    train_dataset.set_format(type="torch", columns=columns_to_keep)
    val_dataset.set_format(type="torch", columns=columns_to_keep)

    date_stamp = dt.datetime.now().strftime("%y%m%d")
    run_name = (
        f"{args.run_prefix}_{date_stamp}_L11_E{args.epochs}"
        f"_B{args.per_device_train_batch_size}"
        f"_LR{args.learning_rate}_WU{args.warmup_ratio}_WD{args.weight_decay}"
        f"_GAS{args.gradient_accumulation_steps}_FZ{args.freeze_layers}"
        f"_GPUs{world_size}"
    )
    training_output_dir = args.output_dir.resolve() / run_name
    logging_dir = training_output_dir / "logs"
    training_output_dir.mkdir(parents=True, exist_ok=True)
    logging_dir.mkdir(parents=True, exist_ok=True)

    if rank == 0:
        print(f"Run name: {run_name}")
        print(f"Train examples: {len(train_dataset):,}")
        print(f"Val examples: {len(val_dataset):,}")
        print(f"World size: {world_size}")

    model, config = setup_model(
        args.foundational_model,
        token_dictionary,
        args.prior_model_safetensors,
        args.rope_factor,
    )
    freeze_transformer_layers(model, args.freeze_layers)

    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_total = sum(p.numel() for p in model.parameters())
    if rank == 0:
        print(f"Trainable parameters: {n_trainable:,} / {n_total:,}")
        print(f"RoPE scaling: {config.rope_scaling}")

    steps_per_epoch = step_count(
        len(train_dataset), args.per_device_train_batch_size,
        args.gradient_accumulation_steps, world_size,
    )
    save_steps = max(1, int(round(steps_per_epoch * args.save_fraction)))
    logging_steps = max(1, int(round(steps_per_epoch * args.logging_fraction)))
    eval_steps = max(1, int(round(steps_per_epoch * args.eval_fraction)))

    training_args = TrainingArguments(
        output_dir=str(training_output_dir),
        logging_dir=str(logging_dir),
        run_name=run_name,
        do_train=True,
        do_eval=args.do_eval,
        eval_strategy="steps" if args.do_eval else "no",
        eval_steps=eval_steps if args.do_eval else None,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=args.warmup_ratio,
        weight_decay=args.weight_decay,
        num_train_epochs=args.epochs,
        save_strategy="steps",
        save_steps=save_steps,
        save_total_limit=args.save_total_limit,
        logging_steps=logging_steps,
        logging_first_step=False,
        remove_unused_columns=False,
        disable_tqdm=False,
        fp16=False,
        bf16=True,
        report_to=[] if args.report_to == "none" else [args.report_to],
        deepspeed=str(args.deepspeed) if args.deepspeed else None,
    )

    trainer = MaxTokiHeartDevTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset if args.do_eval else None,
        token_dictionary=token_dictionary,
        data_collator=MaxTokiDataCollator(
            pad_token_id=token_dictionary.get("<pad>", 0)
        ),
    )

    manifest = {
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "run_name": run_name,
        "train_dataset": str(args.train_dataset),
        "val_dataset": str(args.val_dataset),
        "foundational_model": str(args.foundational_model),
        "prior_model_safetensors": str(args.prior_model_safetensors)
        if args.prior_model_safetensors else None,
        "token_dictionary": str(args.token_dictionary),
        "train_examples": len(train_dataset),
        "val_examples": len(val_dataset),
        "world_size": world_size,
        "steps_per_epoch": steps_per_epoch,
        "training_args": training_args.to_dict(),
    }
    if rank == 0:
        (training_output_dir / "finetune_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True, default=str) + "\n"
        )
        (args.output_dir.resolve() / "latest_run_dir.txt").write_text(
            str(training_output_dir) + "\n"
        )

    checkpoint = latest_checkpoint(training_output_dir)
    if checkpoint:
        print(f"Resuming from checkpoint: {checkpoint}")
        trainer.train(resume_from_checkpoint=checkpoint)
    else:
        prior_str = str(args.prior_model_safetensors) if args.prior_model_safetensors else "foundational model"
        print(f"Starting training from {prior_str}.")
        trainer.train()

    final_dir = training_output_dir / "final_model"
    trainer.save_model(str(final_dir))
    if rank == 0:
        (args.output_dir.resolve() / "latest_final_model_dir.txt").write_text(
            str(final_dir) + "\n"
        )
        print(f"Saved final model to {final_dir}")


if __name__ == "__main__":
    main()
