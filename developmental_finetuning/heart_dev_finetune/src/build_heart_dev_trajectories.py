#!/usr/bin/env python3
"""Build masked MaxToki trajectory datasets grouped by canonical_cell_type.

This stage converts stage-split source cell datasets into paragraph-style
MaxToki training examples for the heart-development fine-tune.

Grouping strategy
-----------------
Cells are grouped by ``canonical_cell_type`` alone (no sex covariate — sex
metadata is sparse in developmental datasets). Within each canonical type, the
assembler samples context cells at one PCW and a target cell of the same type
at a later PCW, producing a trajectory that spans developmental time.

Time encoding
-------------
``dev_time_num`` = PCW × 10 (integer). A one-PCW gap → timelapse token 10.
This produces timelapse values in the range 1–370 (≈ 0.1–37 PCW), which
overlaps with the numeric token range of the existing MaxToki token dictionary.
Run ``scripts/check_token_dict_coverage.py`` to verify before training.

Val/test trajectory construction
---------------------------------
Correct MaxToki evaluation requires that context cells come from training-stage
cells while query cells come from held-out val/test-stage cells. This mirrors
the brain-aging pipeline: ``build_split`` is used for train (context + query
both from train stage); ``build_eval_split`` is used for val and test (context
from train stage, query from val/test stage).
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
import shutil
import sys

from utils import load_token_dictionary
from datetime import datetime
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba-maxtoki-heart-dev")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-maxtoki-heart-dev")

from datasets import disable_caching, load_from_disk

disable_caching()

MAXTOKI_REPO = Path("/gladstone/theodoris/lab/models/MaxToki")
if str(MAXTOKI_REPO) not in sys.path:
    sys.path.insert(0, str(MAXTOKI_REPO))

from maxtoki.paragraph_assembler.cell_paragraph_assembler import CellParagraphAssembler
from maxtoki.paragraph_assembler.query_assembler import QueryAssembler

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
_SHARED = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data")

DEFAULT_PREPARED_ROOT = _DATA / "finetuning_heart_dev"
DEFAULT_TOKEN_DICT = _SHARED / "token_dictionary_aging_gc95M.pkl"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_csv_list(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def remove_if_needed(path: Path, overwrite: bool) -> None:
    if not path.exists():
        return
    if not overwrite:
        raise FileExistsError(f"{path} already exists. Pass --overwrite to replace it.")
    shutil.rmtree(path)


def map_num_proc(nproc: int | None) -> int | None:
    return nproc if nproc and nproc > 1 else None


# ---------------------------------------------------------------------------
# Mask & metadata helpers
# ---------------------------------------------------------------------------

def add_attention_and_loss_masks(dataset, token_dictionary: dict, nproc: int):
    """Add full attention masks and response-only loss masks.

    Loss is computed only over response tokens after ``<eoq>``.
    """
    eoq_id = token_dictionary["<eoq>"]

    def add_masks(batch):
        attention_masks = []
        loss_masks = []
        for input_ids in batch["input_ids"]:
            ids = list(input_ids)
            try:
                eoq_idx = ids.index(eoq_id)
            except ValueError as exc:
                raise ValueError("Training example is missing <eoq>; cannot build loss_mask.") from exc
            response_start = eoq_idx + 1
            attention_masks.append([1] * len(ids))
            loss_masks.append([0] * response_start + [1] * (len(ids) - response_start))
        return {"attention_mask": attention_masks, "loss_mask": loss_masks}

    return dataset.map(add_masks, batched=True, num_proc=map_num_proc(nproc))


def add_evaluation_metadata(dataset, blueprint: dict):
    """Attach trajectory metadata needed for post-training validation reports."""
    tasks = list(blueprint["predict_time_or_cell_list"])
    time_choices = [list(map(int, values)) for values in blueprint["time_choices"]]
    timegroup_order = [str(value) for value in blueprint["timegroup_order"]]
    dataset_order = [int(value) for value in blueprint["dataset_order"]]

    # dev_time_num values (PCW × 10)
    context_dev_time_num = [values[-2] for values in time_choices]
    target_dev_time_num = [values[-1] for values in time_choices]
    true_timelapse_num = [target - context
                          for context, target in zip(context_dev_time_num, target_dev_time_num)]

    dataset = dataset.add_column("task", tasks)
    dataset = dataset.add_column("timegroup_order", timegroup_order)
    dataset = dataset.add_column("dataset_order", dataset_order)
    dataset = dataset.add_column("time_choices", time_choices)
    dataset = dataset.add_column("context_dev_time_num", context_dev_time_num)
    dataset = dataset.add_column("target_dev_time_num", target_dev_time_num)
    dataset = dataset.add_column("true_timelapse_num", true_timelapse_num)
    # Human-readable PCW columns (divide dev_time_num by 10)
    dataset = dataset.add_column("context_dev_time_pcw",
                                 [n / 10.0 for n in context_dev_time_num])
    dataset = dataset.add_column("target_dev_time_pcw",
                                 [n / 10.0 for n in target_dev_time_num])
    dataset = dataset.add_column("true_timelapse_pcw",
                                 [n / 10.0 for n in true_timelapse_num])
    return dataset


# ---------------------------------------------------------------------------
# Train split builder
# ---------------------------------------------------------------------------

def build_split(
    split_name: str,
    source_dataset: Path,
    output_dir: Path,
    token_dictionary_path: Path,
    token_dictionary: dict,
    num_examples: int,
    time_group_columns: list[str],
    nproc: int,
    seed: int,
    min_timepoints: int,
    max_timepoints: int,
    max_repeat_timepoints: int,
    balance_timegroups: float,
    task_ratio: float,
    model_input_size: int,
    overwrite: bool,
    time_bin_length: int | None = None,
) -> dict:
    """Assemble, mask, and save the train trajectory split."""
    split_dir = output_dir / split_name
    split_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = f"{split_name}_heart_dev"
    masked_path = split_dir / f"{output_prefix}_masked.dataset"
    remove_if_needed(masked_path, overwrite)

    cpa_nproc = map_num_proc(nproc)
    cpa_kwargs = dict(
        time_group_columns=time_group_columns,
        time_column="dev_time_num",
        min_timepoints=min_timepoints,
        max_timepoints=max_timepoints,
        max_repeat_timepoints=max_repeat_timepoints,
        group_by_dataset=False,
        balance_datasets=0,
        balance_timegroups=balance_timegroups,
        num_examples=num_examples,
        task_ratio=task_ratio,
        nproc=cpa_nproc,
        model_input_size=model_input_size,
        seed=seed,
    )
    if time_bin_length is not None:
        import inspect
        if "time_bin_length" in inspect.signature(CellParagraphAssembler.__init__).parameters:
            cpa_kwargs["time_bin_length"] = time_bin_length

    cpa = CellParagraphAssembler(**cpa_kwargs)

    try:
        dataset_list, blueprint = cpa.generate_cell_paragraph_blueprint(
            str(source_dataset),
            str(split_dir),
            output_prefix,
        )
    except IndexError as exc:
        raise RuntimeError(
            f"No valid time groups remained for the {split_name} split at {source_dataset}. "
            "Check that each canonical_cell_type group has ≥ "
            f"{min_timepoints - max_repeat_timepoints} distinct dev_time_num values."
        ) from exc

    time_dictionary_path = split_dir / f"{output_prefix}_time_dictionary.pkl"
    with time_dictionary_path.open("wb") as handle:
        pickle.dump(token_dictionary, handle)

    unmasked = cpa.assemble_cell_paragraphs(
        dataset_list, blueprint, token_dictionary,
        str(split_dir), clip_timesteps=False, clip_first_cell=True,
        is_train=True, nproc=cpa_nproc,
    )
    masked = add_attention_and_loss_masks(unmasked, token_dictionary, nproc=nproc)
    masked = add_evaluation_metadata(masked, blueprint)
    masked.save_to_disk(str(masked_path))

    return {
        "split": split_name,
        "source_dataset": str(source_dataset),
        "num_examples_requested": num_examples,
        "num_examples_written": len(masked),
        "masked_dataset": str(masked_path),
        "unmasked_dataset": str(split_dir / f"{blueprint['output_prefix_complete']}.dataset"),
        "blueprint": str(split_dir / f"{blueprint['output_prefix_complete']}_cell_paragraph_blueprint.pkl"),
        "time_dictionary": str(time_dictionary_path),
        "max_timepoint": blueprint["max_timepoint"],
        "time_group_columns": time_group_columns,
    }


# ---------------------------------------------------------------------------
# Eval split builder (context from train, query from val/test)
# ---------------------------------------------------------------------------

def build_eval_split(
    split_name: str,
    train_source: Path,
    eval_source: Path,
    output_dir: Path,
    token_dictionary_path: Path,
    token_dictionary: dict,
    num_examples: int,
    time_group_columns: list[str],
    nproc: int,
    seed: int,
    min_timepoints: int,
    max_timepoints: int,
    max_repeat_timepoints: int,
    balance_timegroups: float,
    task_ratio: float,
    model_input_size: int,
    overwrite: bool,
    time_bin_length: int | None = None,
) -> dict:
    """Build val/test trajectories: context from train stage, query from eval stage.

    This follows the same pattern as the brain-aging pipeline so that the
    model is evaluated on its ability to generalise from training PCW windows
    (PCW 3–9, 17+) to held-out developmental windows (PCW 10–12 for val, 13–16
    for test).
    """
    split_dir = output_dir / split_name
    split_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = f"{split_name}_heart_dev"
    final_path = split_dir / f"{output_prefix}_masked.dataset"
    remove_if_needed(final_path, overwrite)

    cpa_nproc = map_num_proc(nproc)
    cpa_kwargs = dict(
        time_group_columns=time_group_columns,
        time_column="dev_time_num",
        min_timepoints=min_timepoints,
        max_timepoints=max_timepoints,
        max_repeat_timepoints=max_repeat_timepoints,
        group_by_dataset=False,
        balance_datasets=0,
        balance_timegroups=balance_timegroups,
        num_examples=num_examples,
        task_ratio=task_ratio,
        nproc=cpa_nproc,
        model_input_size=model_input_size,
        seed=seed,
    )
    if time_bin_length is not None:
        import inspect
        if "time_bin_length" in inspect.signature(CellParagraphAssembler.__init__).parameters:
            cpa_kwargs["time_bin_length"] = time_bin_length

    cpa = CellParagraphAssembler(**cpa_kwargs)

    try:
        dataset_list, blueprint = cpa.generate_cell_paragraph_blueprint(
            str(train_source),
            str(split_dir),
            output_prefix,
        )
    except IndexError as exc:
        raise RuntimeError(
            f"No valid time groups remained for the {split_name} eval split at {train_source}. "
            "Check that --train-source has enough canonical cell types with ≥2 distinct "
            "dev_time_num values."
        ) from exc

    blueprint_path = split_dir / f"{blueprint['output_prefix_complete']}_cell_paragraph_blueprint.pkl"
    time_dictionary_path = split_dir / f"{output_prefix}_time_dictionary.pkl"
    with time_dictionary_path.open("wb") as handle:
        pickle.dump(token_dictionary, handle)

    # Assemble in eval format so QueryAssembler can replace the query cell
    cpa.assemble_cell_paragraphs(
        dataset_list, blueprint, token_dictionary,
        str(split_dir), clip_timesteps=False, clip_first_cell=True,
        is_train=False, nproc=cpa_nproc,
    )
    unmasked_path = split_dir / f"{blueprint['output_prefix_complete']}.dataset"

    qa = QueryAssembler(
        query_subset_dict=None,
        time_column="dev_time_num",
        time_group_columns=time_group_columns,
        allow_zero_timelapses="question",
        allow_negative_timelapses=True,
        exclude_times=None,
        nproc=1,
        model_input_size=model_input_size,
        seed=seed,
    )
    qa_prefix = f"{output_prefix}_query"
    query_dataset = qa.build_eval_cell_query_dataset(
        blueprint_dictionary_file=str(blueprint_path),
        time_token_dictionary_file=str(time_dictionary_path),
        cell_paragraph_dataset_file=str(unmasked_path),
        query_data_files=[str(eval_source)],
        output_directory=str(split_dir),
        output_prefix=qa_prefix,
    )

    def reconstruct_and_mask(batch):
        full_input_ids = []
        attention_masks = []
        loss_masks = []
        for prompt_ids, response_ids in zip(batch["input_ids"], batch["response"]):
            prompt_ids = list(prompt_ids)
            response_ids = list(response_ids)
            full_ids = prompt_ids + response_ids
            full_input_ids.append(full_ids)
            attention_masks.append([1] * len(full_ids))
            loss_masks.append([0] * len(prompt_ids) + [1] * len(response_ids))
        return {
            "input_ids": full_input_ids,
            "attention_mask": attention_masks,
            "loss_mask": loss_masks,
        }

    masked = query_dataset.map(reconstruct_and_mask, batched=True, num_proc=cpa_nproc)

    # Add evaluation metadata from QueryAssembler output
    masked = masked.rename_column("predict_time_or_cell", "task")
    time_choices_list = [list(map(int, tc)) for tc in masked["time_choices"]]
    context_dev_time_num = [tc[-2] for tc in time_choices_list]
    target_dev_time_num = [tc[-1] for tc in time_choices_list]
    true_timelapse_num = [t - c for c, t in zip(context_dev_time_num, target_dev_time_num)]

    masked = masked.add_column("context_dev_time_num", context_dev_time_num)
    masked = masked.add_column("target_dev_time_num", target_dev_time_num)
    masked = masked.add_column("true_timelapse_num", true_timelapse_num)
    masked = masked.add_column("context_dev_time_pcw", [n / 10.0 for n in context_dev_time_num])
    masked = masked.add_column("target_dev_time_pcw", [n / 10.0 for n in target_dev_time_num])
    masked = masked.add_column("true_timelapse_pcw", [n / 10.0 for n in true_timelapse_num])
    masked.save_to_disk(str(final_path))

    return {
        "split": split_name,
        "train_source": str(train_source),
        "eval_source": str(eval_source),
        "num_examples_requested": num_examples,
        "num_examples_written": len(masked),
        "masked_dataset": str(final_path),
        "unmasked_dataset": str(unmasked_path),
        "query_dataset": str(split_dir / f"{qa_prefix}.dataset"),
        "blueprint": str(blueprint_path),
        "time_dictionary": str(time_dictionary_path),
        "max_timepoint": blueprint["max_timepoint"],
        "time_group_columns": time_group_columns,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build canonical_cell_type MaxToki train/val trajectories for heart development."
    )
    parser.add_argument("--prepared-root", type=Path, default=DEFAULT_PREPARED_ROOT)
    parser.add_argument("--train-source", type=Path, default=None)
    parser.add_argument("--val-source", type=Path, default=None)
    parser.add_argument("--test-source", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--token-dictionary", type=Path, default=DEFAULT_TOKEN_DICT)
    parser.add_argument("--time-group-columns", default="canonical_cell_type",
                        help="Comma-separated grouping columns. Default: canonical_cell_type.")
    parser.add_argument("--train-examples", type=int, default=500_000)
    parser.add_argument("--val-examples", type=int, default=25_000)
    parser.add_argument("--test-examples", type=int, default=10_000)
    parser.add_argument("--test-only", action="store_true",
                        help="Skip train/val and only rebuild the test split.")
    parser.add_argument("--min-timepoints", type=int, default=3)
    parser.add_argument("--max-timepoints", type=int, default=4)
    parser.add_argument("--max-repeat-timepoints", type=int, default=1)
    parser.add_argument("--balance-timegroups", type=float, default=1.0)
    parser.add_argument("--task-ratio", type=float, default=0.5,
                        help="Fraction of examples that are timelapse tasks (vs cell-token tasks).")
    parser.add_argument("--model-input-size", type=int, default=16_384)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--nproc", type=int, default=8)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--time-bin-length", type=int, default=None,
        help=(
            "Length of each time bin for bin-balanced trajectory sampling, in dev_time_num "
            "units (PCW × 10). E.g. 20 = 2-PCW bins. Default: no time-bin balancing."
        ),
    )
    args = parser.parse_args()

    prepared_root = args.prepared_root.resolve()
    output_dir = (args.output_dir or (prepared_root / "trajectories")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    train_source = args.train_source or (prepared_root / "source_train_heart_dev.dataset")
    val_source = args.val_source or (prepared_root / "source_val_heart_dev.dataset")
    test_source = args.test_source or (prepared_root / "source_test_heart_dev.dataset")
    time_group_columns = parse_csv_list(args.time_group_columns)

    token_dictionary = load_token_dictionary(args.token_dictionary)
    required_tokens = ["<pad>", "<bos>", "<eos>", "<boq>", "<eoq>"]
    missing_tokens = [t for t in required_tokens if t not in token_dictionary]
    if missing_tokens:
        raise ValueError(f"Token dictionary missing required tokens: {', '.join(missing_tokens)}")

    # Check that PCW timelapse values fall within the numeric token range
    numeric_keys = set()
    for key in token_dictionary:
        try:
            numeric_keys.add(float(key))
        except (TypeError, ValueError):
            pass
    max_dev_time_num = 400  # PCW 40 × 10
    missing_timelapse = [v for v in range(1, 38) if float(v) not in numeric_keys]
    if missing_timelapse:
        print(
            f"WARNING: dev_time_num timelapse values {missing_timelapse[:10]}... "
            "are not present as numeric tokens in the token dictionary. "
            "Training will fail if these appear as timelapse targets. "
            "Consider building a heart-dev-specific token dictionary."
        )

    manifest: dict = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "prepared_root": str(prepared_root),
        "output_dir": str(output_dir),
        "token_dictionary": str(args.token_dictionary),
        "time_group_columns": time_group_columns,
        "time_column": "dev_time_num",
        "time_unit": "PCW × 10 (integer tenths of post-conception week)",
        "parameters": {
            "train_examples": args.train_examples,
            "val_examples": args.val_examples,
            "test_examples": args.test_examples,
            "min_timepoints": args.min_timepoints,
            "max_timepoints": args.max_timepoints,
            "max_repeat_timepoints": args.max_repeat_timepoints,
            "balance_timegroups": args.balance_timegroups,
            "task_ratio": args.task_ratio,
            "model_input_size": args.model_input_size,
            "seed": args.seed,
            "nproc": args.nproc,
            "time_bin_length": args.time_bin_length,
        },
    }

    common_kwargs = dict(
        token_dictionary_path=args.token_dictionary,
        token_dictionary=token_dictionary,
        time_group_columns=time_group_columns,
        nproc=args.nproc,
        min_timepoints=args.min_timepoints,
        max_timepoints=args.max_timepoints,
        max_repeat_timepoints=args.max_repeat_timepoints,
        balance_timegroups=args.balance_timegroups,
        task_ratio=args.task_ratio,
        model_input_size=args.model_input_size,
        overwrite=args.overwrite,
        time_bin_length=args.time_bin_length,
    )

    if not args.test_only:
        train_result = build_split(
            "train", train_source, output_dir,
            num_examples=args.train_examples, seed=args.seed,
            **common_kwargs,
        )
        val_result = build_eval_split(
            "val", train_source, val_source, output_dir,
            num_examples=args.val_examples, seed=args.seed + 1,
            **common_kwargs,
        )
        manifest["train"] = train_result
        manifest["val"] = val_result
        print(f"Train: {train_result['num_examples_written']:,} examples")
        print(f"Val:   {val_result['num_examples_written']:,} examples")

    if test_source.exists():
        test_result = build_eval_split(
            "test", train_source, test_source, output_dir,
            num_examples=args.test_examples, seed=args.seed + 2,
            **common_kwargs,
        )
        manifest["test"] = test_result
        print(f"Test:  {test_result['num_examples_written']:,} examples")

    manifest_path = output_dir / "trajectory_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
