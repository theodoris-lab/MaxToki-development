#!/usr/bin/env python3
"""Plot live training-loss curves from a heart-dev fine-tune Trainer run.

Reads ``trainer_state.json`` (updated at every checkpoint) and saves a PNG
with training and (optionally) evaluation metrics. Safe to run while training
is in progress.

Usage
-----
# Auto-discover the latest run:
python plot_training_progress.py

# Explicit run directory:
python plot_training_progress.py --run-dir /path/to/run_dir

# Watch mode (re-plot every 60 s):
python plot_training_progress.py --watch --interval 60
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-maxtoki-heart-dev")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
DEFAULT_MODEL_ROOT = _DATA / "finetuning_heart_dev" / "model"
DEFAULT_OUTPUT_PNG = Path("training_progress.png")


def find_run_dir(model_root: Path) -> Path:
    latest_file = model_root / "latest_run_dir.txt"
    if latest_file.exists():
        run_dir = Path(latest_file.read_text().strip())
        if run_dir.exists():
            return run_dir
    subdirs = [p for p in model_root.iterdir() if p.is_dir()]
    if not subdirs:
        raise FileNotFoundError(f"No run directories found under {model_root}.")
    return max(subdirs, key=lambda p: p.stat().st_mtime)


def load_log_history(run_dir: Path) -> list[dict]:
    state_path = run_dir / "trainer_state.json"
    if not state_path.exists():
        checkpoints = sorted(
            run_dir.glob("checkpoint-*"),
            key=lambda p: int(p.name.split("-")[-1])
            if p.name.split("-")[-1].isdigit() else 0,
        )
        if checkpoints:
            state_path = checkpoints[-1] / "trainer_state.json"
    if not state_path.exists():
        return []
    with state_path.open() as f:
        state = json.load(f)
    return state.get("log_history", [])


def split_logs(log_history: list[dict]) -> tuple[list[dict], list[dict]]:
    train_logs = [e for e in log_history if "loss" in e or "train_ce_loss" in e]
    eval_logs = [e for e in log_history if any(k.startswith("eval_") for k in e)]
    return train_logs, eval_logs


def extract(logs: list[dict], key: str) -> tuple[list[float], list[float]]:
    steps, values = [], []
    for entry in logs:
        if key in entry:
            steps.append(entry["step"])
            values.append(entry[key])
    return steps, values


# Timelapse metrics are in PCW (converted from dev_time_num / 10 in the trainer)
TRAIN_METRICS = [
    ("loss",                       "Total Loss",                 "#1f77b4"),
    ("train_ce_loss",              "CE Loss (cell tokens)",      "#ff7f0e"),
    ("train_mse_loss",             "MSE Loss (timelapse)",       "#2ca02c"),
    ("train_timelapse_mae_pcw",    "Timelapse MAE (PCW)",        "#d62728"),
    ("train_timelapse_rmse_pcw",   "Timelapse RMSE (PCW)",       "#9467bd"),
    ("learning_rate",              "Learning Rate",              "#8c564b"),
]

EVAL_METRICS = [
    ("eval_loss",                  "Eval Total Loss",            "#1f77b4"),
    ("eval_ce_loss",               "Eval CE Loss",               "#ff7f0e"),
    ("eval_mse_loss",              "Eval MSE Loss",              "#2ca02c"),
    ("eval_timelapse_mae_pcw",     "Eval Timelapse MAE (PCW)",   "#d62728"),
    ("eval_timelapse_rmse_pcw",    "Eval Timelapse RMSE (PCW)",  "#9467bd"),
]


def make_figure(
    train_logs: list[dict], eval_logs: list[dict],
    run_name: str, total_steps: int | None,
) -> plt.Figure:
    has_eval = bool(eval_logs)
    n_train = len(TRAIN_METRICS)
    n_eval = len(EVAL_METRICS) if has_eval else 0
    n_cols = 2

    fig_width = 14 if has_eval else 10
    n_rows = max(
        (n_train + n_cols - 1) // n_cols,
        (n_eval + n_cols - 1) // n_cols if has_eval else 0,
    )
    fig_height = max(3 * n_rows + 2, 6)
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=140)
    fig.suptitle(f"Heart-Dev Training Progress\n{run_name}", fontsize=9, y=0.98)

    if has_eval:
        outer = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)
        train_gs = gridspec.GridSpecFromSubplotSpec(
            n_rows, 1, subplot_spec=outer[0], hspace=0.55
        )
        eval_gs = gridspec.GridSpecFromSubplotSpec(
            n_rows, 1, subplot_spec=outer[1], hspace=0.55
        )
    else:
        outer = gridspec.GridSpec(n_rows, n_cols, figure=fig, hspace=0.55, wspace=0.35)

    def _add_panel(ax, steps, values, label, color, marker=None):
        if steps:
            kw = {"color": color, "linewidth": 0.9, "alpha": 0.85}
            if marker:
                kw.update({"marker": marker, "markersize": 3})
            ax.plot(steps, values, **kw)
            if total_steps:
                ax.set_xlim(0, total_steps)
            ax.set_title(label, fontsize=8, pad=3)
            ax.set_xlabel("Step", fontsize=7)
            ax.tick_params(labelsize=7)
            ax.grid(True, linewidth=0.3, alpha=0.5)
            ax.annotate(
                f"{values[-1]:.4f}",
                xy=(steps[-1], values[-1]),
                fontsize=7, color=color,
                xytext=(4, 0), textcoords="offset points",
            )
        else:
            ax.set_title(f"{label}\n(no data yet)", fontsize=8, color="grey")

    for i, (key, label, color) in enumerate(TRAIN_METRICS):
        steps, values = extract(train_logs, key)
        ax = (fig.add_subplot(train_gs[i]) if has_eval
              else fig.add_subplot(outer[i // n_cols, i % n_cols]))
        _add_panel(ax, steps, values, label, color)

    if has_eval:
        for i, (key, label, color) in enumerate(EVAL_METRICS):
            steps, values = extract(eval_logs, key)
            ax = fig.add_subplot(eval_gs[i])
            _add_panel(ax, steps, values, label, color, marker="o")
        fig.text(0.27, 0.99, "Training", ha="center", va="top", fontsize=9, fontweight="bold")
        fig.text(0.73, 0.99, "Evaluation", ha="center", va="top", fontsize=9, fontweight="bold")

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    return fig


def plot_once(run_dir: Path, output_png: Path) -> None:
    log_history = load_log_history(run_dir)
    if not log_history:
        print(f"No log history yet in {run_dir}.")
        return
    train_logs, eval_logs = split_logs(log_history)
    run_name = run_dir.name

    total_steps = None
    state_path = run_dir / "trainer_state.json"
    if state_path.exists():
        with state_path.open() as f:
            state = json.load(f)
        total_steps = state.get("max_steps")

    fig = make_figure(train_logs, eval_logs, run_name, total_steps)
    fig.savefig(str(output_png), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_png} ({len(train_logs)} train entries, {len(eval_logs)} eval entries)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot heart-dev training progress.")
    parser.add_argument("--run-dir", type=Path, default=None)
    parser.add_argument("--model-root", type=Path, default=DEFAULT_MODEL_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PNG)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()

    run_dir = args.run_dir or find_run_dir(args.model_root)
    print(f"Monitoring run: {run_dir}")

    if args.watch:
        while True:
            plot_once(run_dir, args.output)
            time.sleep(args.interval)
    else:
        plot_once(run_dir, args.output)


if __name__ == "__main__":
    main()
