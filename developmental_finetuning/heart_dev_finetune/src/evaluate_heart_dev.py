#!/usr/bin/env python3
"""Evaluate a heart-development MaxToki fine-tune.

Reads the val (or test) trajectory dataset produced by
``build_heart_dev_trajectories.py`` and the fine-tuned model, then writes:

- ``evaluation_metrics.json`` — combined_loss, mse_loss, ce_loss, timelapse
  MAE/RMSE/Pearson r in PCW units.
- ``timelapse_pcw_predictions.csv`` — per-example true vs predicted timelapse
  (PCW) and absolute developmental timepoints (PCW).
- ``cell_ce_losses.csv`` — per-example CE loss for cell-token prediction
  examples.

All timelapse values are reported in PCW (post-conception weeks) by dividing
the internal dev_time_num representation (PCW × 10) by 10.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
from contextlib import nullcontext
from pathlib import Path

import numpy as np
import torch
from datasets import disable_caching, load_from_disk
from tqdm import tqdm

from finetune_heart_dev import (
    DEFAULT_DATA_ROOT,
    DEFAULT_FOUNDATIONAL_MODEL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TOKEN_DICT,
    MaxTokiDataCollator,
    limit_dataset,
    setup_model,
)
from utils import load_token_dictionary

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba-maxtoki-heart-dev")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-maxtoki-heart-dev")
disable_caching()

DEFAULT_VAL_DATASET = (
    DEFAULT_DATA_ROOT / "trajectories/val/val_heart_dev_masked.dataset"
)
DEFAULT_EVAL_OUTPUT = DEFAULT_DATA_ROOT / "evaluation"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reverse_numeric_dictionary(token_dictionary: dict) -> dict[int, float]:
    reverse: dict[int, float] = {}
    for key, value in token_dictionary.items():
        try:
            reverse[int(value)] = float(key)
        except (TypeError, ValueError):
            continue
    if not reverse:
        raise ValueError("Token dictionary does not contain numeric timelapse tokens.")
    return reverse


def latest_final_model_safetensors(output_dir: Path) -> Path:
    latest_file = output_dir / "latest_final_model_dir.txt"
    if latest_file.exists():
        model_dir = Path(latest_file.read_text().strip())
        model_file = model_dir / "model.safetensors"
        if model_file.exists():
            return model_file
    candidates = sorted(
        output_dir.glob("*/final_model/model.safetensors"),
        key=lambda p: p.stat().st_mtime,
    )
    if not candidates:
        raise FileNotFoundError(
            f"No final model safetensors found under {output_dir}. "
            "Pass --model-safetensors explicitly."
        )
    return candidates[-1]


def batched_indices(n_items: int, batch_size: int):
    for start in range(0, n_items, batch_size):
        yield list(range(start, min(start + batch_size, n_items)))


def scalar_metrics(
    values_true: list[float], values_pred: list[float], prefix: str
) -> dict[str, float]:
    if not values_true:
        return {}
    true = np.asarray(values_true, dtype=float)
    pred = np.asarray(values_pred, dtype=float)
    errors = pred - true
    metrics = {
        f"{prefix}_n": int(true.size),
        f"{prefix}_mae": float(np.mean(np.abs(errors))),
        f"{prefix}_rmse": float(np.sqrt(np.mean(errors ** 2))),
        f"{prefix}_bias": float(np.mean(errors)),
    }
    if true.size > 1 and np.std(true) > 0 and np.std(pred) > 0:
        metrics[f"{prefix}_pearson_r"] = float(np.corrcoef(true, pred)[0, 1])
    return metrics


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(args) -> dict:
    token_dictionary = load_token_dictionary(args.token_dictionary)
    reverse_numeric = reverse_numeric_dictionary(token_dictionary)
    # max_timelapse is used for normalisation; same as training
    max_timelapse = max(reverse_numeric.values())
    eoq_token_id = token_dictionary["<eoq>"]
    bos_token_id = token_dictionary["<bos>"]

    model_safetensors = args.model_safetensors or latest_final_model_safetensors(
        args.model_output_root
    )
    model, _ = setup_model(
        args.foundational_model,
        token_dictionary,
        model_safetensors,
        args.rope_factor,
    )

    device = torch.device(
        args.device if args.device else ("cuda" if torch.cuda.is_available() else "cpu")
    )
    model.to(device)
    model.eval()

    dataset = load_from_disk(str(args.dataset))
    dataset = limit_dataset(dataset, args.max_examples, args.seed, args.shuffle_before_select)
    required = ["input_ids", "attention_mask", "loss_mask"]
    missing = [c for c in required if c not in dataset.column_names]
    if missing:
        raise ValueError(f"Evaluation dataset is missing required columns: {', '.join(missing)}")

    has_dev_time_metadata = {"context_dev_time_num", "target_dev_time_num"}.issubset(
        set(dataset.column_names)
    )
    if args.require_dev_time_metadata and not has_dev_time_metadata:
        raise ValueError(
            "Dev-time evaluation requires context_dev_time_num and target_dev_time_num "
            "columns. Rebuild trajectories with build_heart_dev_trajectories.py."
        )

    collator = MaxTokiDataCollator(pad_token_id=token_dictionary.get("<pad>", 0))
    use_autocast = args.bf16 and device.type == "cuda"
    autocast_ctx = (
        torch.autocast(device_type="cuda", dtype=torch.bfloat16)
        if use_autocast
        else nullcontext()
    )

    ce_loss_sum = 0.0
    ce_token_count = 0
    mse_loss_sum = 0.0
    mse_token_count = 0
    combined_loss_sum = 0.0
    combined_loss_count = 0

    time_rows: list[dict] = []
    cell_rows: list[dict] = []
    # In PCW units (dev_time_num / 10)
    true_timelapses_pcw: list[float] = []
    pred_timelapses_pcw: list[float] = []

    for batch_indices in tqdm(
        list(batched_indices(len(dataset), args.batch_size)), desc="Evaluating"
    ):
        features = [dataset[int(i)] for i in batch_indices]
        batch = collator(features)
        batch = {k: v.to(device) for k, v in batch.items()}

        with torch.no_grad(), autocast_ctx:
            preds_mse, output_ce = model(
                input_ids=batch["input_ids"], attention_mask=batch["attention_mask"]
            )

        logits = output_ce["logits"]
        input_ids = batch["input_ids"]
        loss_mask = batch["loss_mask"]
        attention_mask = batch["attention_mask"]

        for row_idx, example_index in enumerate(batch_indices):
            valid_len = int(attention_mask[row_idx].sum().item())
            ids = input_ids[row_idx, :valid_len]
            try:
                eoq_idx = (ids == eoq_token_id).nonzero(as_tuple=True)[0][0].item()
            except IndexError as exc:
                raise ValueError(f"Example {example_index} is missing <eoq>.") from exc
            response_start = eoq_idx + 1
            if response_start >= valid_len:
                raise ValueError(
                    f"Example {example_index} has no response token after <eoq>."
                )

            feature_task = (
                features[row_idx].get("task")
                if isinstance(features[row_idx], dict) else None
            )
            task = feature_task or (
                "cell" if int(ids[response_start].item()) == bos_token_id else "time"
            )

            shift_logits = logits[row_idx, : valid_len - 1, :]
            shift_preds = preds_mse[row_idx, : valid_len - 1, 0]
            shift_labels = input_ids[row_idx, 1:valid_len]
            shift_loss_mask = loss_mask[row_idx, 1:valid_len].bool()

            if task == "time":
                label_tokens = shift_labels[shift_loss_mask].detach().cpu().tolist()
                pred_values = shift_preds[shift_loss_mask]
                numeric_labels = [reverse_numeric[int(t)] for t in label_tokens]
                label_tensor = torch.tensor(
                    numeric_labels, dtype=torch.float32, device=device
                )
                mse_losses = (
                    (pred_values.float() / max_timelapse * 10.0)
                    - (label_tensor / max_timelapse * 10.0)
                ) ** 2
                raw_errors = pred_values.float() - label_tensor

                mse_loss_sum += float(mse_losses.sum().detach().cpu())
                mse_token_count += int(mse_losses.numel())
                if mse_losses.numel() > 0:
                    combined_loss_sum += float(mse_losses.mean().detach().cpu())
                    combined_loss_count += 1

                # Internal units are dev_time_num (PCW × 10); convert to PCW
                true_timelapse_num = float(numeric_labels[-1])
                pred_timelapse_num = float(pred_values[-1].detach().float().cpu())
                true_timelapse_pcw = true_timelapse_num / 10.0
                pred_timelapse_pcw = pred_timelapse_num / 10.0
                true_timelapses_pcw.append(true_timelapse_pcw)
                pred_timelapses_pcw.append(pred_timelapse_pcw)

                row: dict = {
                    "example_index": int(example_index),
                    "task": task,
                    "timegroup_order": features[row_idx].get("timegroup_order"),
                    "dataset_order": features[row_idx].get("dataset_order"),
                    # Timelapse in PCW
                    "true_timelapse_pcw": true_timelapse_pcw,
                    "predicted_timelapse_pcw": pred_timelapse_pcw,
                    "timelapse_error_pcw": pred_timelapse_pcw - true_timelapse_pcw,
                    "timelapse_abs_error_pcw": abs(pred_timelapse_pcw - true_timelapse_pcw),
                    "timelapse_sq_error_pcw": (pred_timelapse_pcw - true_timelapse_pcw) ** 2,
                    "mse_loss": (
                        float(mse_losses.mean().detach().cpu())
                        if mse_losses.numel() else None
                    ),
                }

                if has_dev_time_metadata:
                    ctx_num = float(features[row_idx]["context_dev_time_num"])
                    tgt_num = float(features[row_idx]["target_dev_time_num"])
                    pred_tgt_num = ctx_num + pred_timelapse_num
                    row.update({
                        "context_dev_time_pcw": ctx_num / 10.0,
                        "target_dev_time_pcw": tgt_num / 10.0,
                        "predicted_dev_time_pcw": pred_tgt_num / 10.0,
                        "dev_time_error_pcw": (pred_tgt_num - tgt_num) / 10.0,
                        "dev_time_abs_error_pcw": abs(pred_tgt_num - tgt_num) / 10.0,
                    })
                time_rows.append(row)

            elif task == "cell":
                labels_masked = shift_labels[shift_loss_mask]
                logits_masked = shift_logits[shift_loss_mask]
                ce_losses = torch.nn.functional.cross_entropy(
                    logits_masked.float(), labels_masked, reduction="none"
                )
                ce_loss_sum += float(ce_losses.sum().detach().cpu())
                ce_token_count += int(ce_losses.numel())
                if ce_losses.numel() > 0:
                    ce_mean = float(ce_losses.mean().detach().cpu())
                    combined_loss_sum += ce_mean
                    combined_loss_count += 1
                    cell_rows.append({
                        "example_index": int(example_index),
                        "task": task,
                        "timegroup_order": features[row_idx].get("timegroup_order"),
                        "dataset_order": features[row_idx].get("dataset_order"),
                        "ce_loss": ce_mean,
                        "n_cell_tokens": int(ce_losses.numel()),
                    })
            else:
                raise ValueError(f"Example {example_index} has unknown task: {task!r}")

    metrics: dict = {
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "dataset": str(args.dataset),
        "model_safetensors": str(model_safetensors),
        "n_examples": len(dataset),
        "n_time_examples": len(time_rows),
        "n_cell_examples": len(cell_rows),
        "max_timelapse_token": max_timelapse,
        "timelapse_unit": "PCW (post-conception weeks)",
        "combined_loss": (
            combined_loss_sum / combined_loss_count if combined_loss_count else None
        ),
        "mse_loss": mse_loss_sum / mse_token_count if mse_token_count else None,
        "ce_loss": ce_loss_sum / ce_token_count if ce_token_count else None,
    }
    metrics.update(scalar_metrics(true_timelapses_pcw, pred_timelapses_pcw, "timelapse_pcw"))

    if has_dev_time_metadata and time_rows:
        true_tgt = [r["target_dev_time_pcw"] for r in time_rows if "target_dev_time_pcw" in r]
        pred_tgt = [r["predicted_dev_time_pcw"] for r in time_rows if "predicted_dev_time_pcw" in r]
        metrics.update(scalar_metrics(true_tgt, pred_tgt, "dev_time_pcw"))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.output_dir / "evaluation_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    write_rows(args.output_dir / "timelapse_pcw_predictions.csv", time_rows)
    write_rows(args.output_dir / "cell_ce_losses.csv", cell_rows)

    print(f"Wrote metrics:              {metrics_path}")
    print(f"Wrote timelapse predictions: {args.output_dir / 'timelapse_pcw_predictions.csv'}")
    print(f"Wrote cell CE losses:        {args.output_dir / 'cell_ce_losses.csv'}")
    return metrics


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate a heart-development fine-tuned MaxToki model."
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_VAL_DATASET)
    parser.add_argument("--model-safetensors", type=Path, default=None)
    parser.add_argument("--model-output-root", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--foundational-model", type=Path, default=DEFAULT_FOUNDATIONAL_MODEL)
    parser.add_argument("--token-dictionary", type=Path, default=DEFAULT_TOKEN_DICT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_EVAL_OUTPUT)
    parser.add_argument("--max-examples", type=int, default=10_000)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--shuffle-before-select", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--rope-factor", type=float, default=4.0)
    parser.add_argument("--device", default=None)
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--require-dev-time-metadata", action="store_true")
    args = parser.parse_args()
    evaluate(args)


if __name__ == "__main__":
    main()
