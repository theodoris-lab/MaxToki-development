# MaxToki Heart-Development Fine-Tune

Fine-tuning pipeline for adapting the MaxToki foundational 94 M-parameter LLaMA-based model to predict **human heart developmental trajectories** from single-cell transcriptomics.

The model learns two joint objectives from the same paragraph format:
- **Cell-token prediction** — cross-entropy over response gene tokens
- **Timelapse prediction** — MSE regression on the developmental time gap between two cells (in PCW, post-conception weeks)

---

## Repository layout

```
heart_dev_finetune/
├── bash_scripts/
│   └── setup_env.sh                  One-shot environment setup (run before first job)
├── config/
│   └── ds_config_zero3_bf16.json     DeepSpeed ZeRO-3 + BF16 config
├── lib/
│   └── slack_notify.sh               Slack notification helpers for Slurm jobs
├── logs/
│   └── slurm/                        Slurm stdout/stderr logs (auto-created)
├── slurm/
│   ├── submit_finetune_pipeline.sh   One-shot pipeline submitter (Stages 0–4)
│   ├── run_tokenize.sh               Stage 0 Slurm job (CPU — tokenize h5ads)
│   ├── run_prepare_data.sh           Stage 1 Slurm job (CPU — harmonise & split)
│   ├── run_build_trajectories.sh     Stage 2 Slurm job (CPU — trajectories)
│   ├── run_smoke_test.sh             Quick smoke test (~10 min, ctdev) before production
│   ├── run_train.sh                  Stage 3 Slurm job (GPU, DeepSpeed, ctbatch)
│   └── run_evaluate.sh               Stage 4 Slurm job (GPU, ctbatch)
└── src/
    ├── tokenize_heart_dev_sources.py        Stage 0 — tokenize source h5ads
    ├── prepare_heart_dev_finetune_data.py   Stage 1 — harmonise & split datasets
    ├── build_heart_dev_trajectories.py      Stage 2 — build MaxToki paragraphs
    ├── finetune_heart_dev.py                Stage 3 — training loop
    ├── evaluate_heart_dev.py                Stage 4 — evaluation & metrics
    └── plot_training_progress.py            Live training-curve plotter
```

---

## Data sources

| Source | Cells (train) | Notes |
|---|---|---|
| CellxGene heart-dev subset | 221,625 | `development_stage` strings parsed to PCW; case-insensitive harmonisation |
| Lázár et al. 2025 (HDCA SC) | 71,250 | `pcw` column already numeric; RDS → h5ad via `scripts/convert_lazar_to_h5ad.py` |
| Xu et al. 2024 (Organogenesis) | 14,167 | Fetal heart (PCW 5–25) |
| Tyser et al. 2021 (Gastrulation) | 143 | CS7 (~PCW 3); "embryonic stage" → PCW 5.5 |
| **Total train** | **284,873** | After harmonisation, filtering to ≥2 PCW timepoints per cell type |

Tokenised per-source datasets are expected under:
```
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/tokenized/
```

Cell types are harmonised to **53 canonical types** using:
```
cell_type_harmonization/cell_type_harmonization_map.json
```

The map contains 85+ lowercase aliases for case-insensitive lookup across all four datasets.
Harmonisation decisions (alias rationale, dropped labels, lineage holdouts) are documented in:
```
cell_type_harmonization/harmonization_decisions.md
```

---

## Developmental time representation

| Concept | Variable | Formula | Range |
|---|---|---|---|
| Absolute timepoint | `dev_time_pcw` | PCW as float | 3 – 40 |
| Internal integer | `dev_time_num` | `round(pcw × 10)` | 30 – 400 |
| Timelapse token | timelapse token key | `dev_time_num` delta | 1 – 370 |

The integer encoding is compatible with MaxToki's existing numeric token system (token dictionary from the brain-aging run).

---

## Train / val / test split

Splits are **stage-based** (not donor-based), using **specific PCW timepoints** (not contiguous
ranges), so the model must interpolate between timepoints it has seen:

| Split | PCW points | Datasets present | Rationale |
|---|---|---|---|
| **Train** | 3, 4, 4.5, 5, 5.5, 6, 8, 9, 10.5, 11, 12, 13, 15, 16, 17, 19 | CXG, Lázár, Xu, Tyser | Broadest temporal coverage |
| **Val** | **10, 20** | PCW 10: CXG + Lázár; PCW 20: CXG | Two disjoint points: peak dual-dataset (10) and mid-fetal (20) |
| **Test** | **7** | Lázár only | Interpolated between PCW 6 and 8 train; cross-dataset generalisation |
| **Lineage holdout** | all | Epicardial/EPDC, Vascular EC | Withheld from every split to test cell-identity generalisation |

The lineage holdouts are removed in Stage 1 (`prepare_heart_dev_finetune_data.py`) before any
split assignment. Val/test use `--val-pcw-points` / `--test-pcw-points` with a ±0.15 PCW
matching tolerance.

---

## Pipeline stages

### Stage 0 — Tokenize (`tokenize_heart_dev_sources.py`)

- Tokenizes raw h5ad files (CXG subset, Xu) into HuggingFace `.dataset` files
- Tyser is pre-tokenized; Lázár is prepared via `scripts/convert_lazar_to_h5ad.py` first
- Submit via `slurm/run_tokenize.sh` (CPU, ctbatch, 8 h)

### Stage 1 — Prepare data (`prepare_heart_dev_finetune_data.py`)

- Loads tokenised per-source datasets
- Applies canonical cell-type harmonisation with case-insensitive alias lookup
- Parses heterogeneous developmental-stage strings → `dev_time_pcw` / `dev_time_num`
  - Handles "embryonic stage" (no numeric age) → PCW 5.5 (midpoint of PCW 3–8 embryonic window)
- Filters to cell types with ≥ 2 distinct PCW timepoints
- Saves `source_{train,val,test}_heart_dev.dataset` under `finetuning_heart_dev/`
- Use `--overwrite` to bypass HuggingFace `.map()` cache when the harmonisation map changes

### Stage 2 — Build trajectories (`build_heart_dev_trajectories.py`)

- Uses `CellParagraphAssembler` with `time_group_columns=["canonical_cell_type"]`
- Train split: context + query both from train PCW cells
- Val / test splits: context from train PCW, query from val / test PCW (`QueryAssembler`)
- Adds `attention_mask`, `loss_mask` (response-only masking after `<eoq>`)
- Adds trajectory metadata columns: `context_dev_time_pcw`, `target_dev_time_pcw`, etc.
- Default sizes: 500 K train / 25 K val / 10 K test examples

### Stage 3 — Fine-tune (`finetune_heart_dev.py`)

- `PredModel`: LLaMA backbone + scalar linear head
- Mixed CE (cell-token) + normalised MSE (timelapse) loss, same architecture as brain-aging trainer
- Logs `timelapse_mae_pcw` and `timelapse_rmse_pcw` at every checkpoint
- DeepSpeed ZeRO-3 + BF16, 4 × A100 GPUs
- **First round**: starts from foundational 94 M model (no prior heart weights)
- Saves `latest_final_model_dir.txt` for downstream stage auto-resolution

### Stage 4 — Evaluate (`evaluate_heart_dev.py`)

Outputs to `finetuning_heart_dev/evaluation/`:

| File | Contents |
|---|---|
| `evaluation_metrics.json` | combined_loss, mse_loss, ce_loss, timelapse MAE/RMSE/Pearson r (PCW) |
| `timelapse_pcw_predictions.csv` | Per-example true vs predicted timelapse (PCW) |
| `cell_ce_losses.csv` | Per-example CE loss for cell-token examples |

---

## Running the pipeline

### Environment setup (first time only)

```bash
cd developmental_finetuning/heart_dev_finetune
bash bash_scripts/setup_env.sh
```

### Smoke test (recommended before every production run)

Verifies the full training loop (model load → forward/backward → checkpoint save) in ~10 min:

```bash
sbatch slurm/run_smoke_test.sh
tail -f logs/slurm/smoke_<JOB_ID>.out
```

Check the log for `"Smoke test PASSED"` and a finite training loss before proceeding.

### Full pipeline (Stages 0–4 in sequence, ctbatch)

```bash
cd developmental_finetuning/heart_dev_finetune
bash slurm/submit_finetune_pipeline.sh
```

### Skip stages already completed

```bash
# Tokenization done — run Stages 1–4
bash slurm/submit_finetune_pipeline.sh --skip-tokenize

# Trajectories already built — submit training + evaluation only
bash slurm/submit_finetune_pipeline.sh --skip-tokenize --skip-prepare --skip-traj

# Evaluate on the test split instead of val
bash slurm/submit_finetune_pipeline.sh --skip-tokenize --skip-prepare --skip-traj --eval-test
```

### Override data sizes or hyperparameters

```bash
MAX_TRAIN=200000 EPOCHS=2 LR=0.0001 bash slurm/submit_finetune_pipeline.sh --skip-tokenize --skip-prepare --skip-traj
```

### Monitor jobs

```bash
squeue -u $USER | grep hd26
tail -f logs/slurm/train_<JOB_ID>.out
```

### Plot training curves (while training is running)

```bash
conda activate env_maxtoki
python src/plot_training_progress.py --watch --interval 60
```

---

## Key paths

| Resource | Path |
|---|---|
| Data root | `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` |
| Tokenised source datasets | `…/maxtoki_development_data/tokenized/` |
| Fine-tune outputs | `…/maxtoki_development_data/finetuning_heart_dev/` |
| Token dictionary | `…/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl` |
| Foundational model | `…/maxtoki_brain_aging_data/data/foundational_94M_model/` |
| Conda env | `env_maxtoki` |
| Slurm partition (testing) | `ctdev` — 8 h limit, 4× A100; use for smoke tests |
| Slurm partition (production) | `ctbatch` — 7-day limit, 4× A100; use for full runs |

---

## Conda environment

```bash
conda activate env_maxtoki
```

All `src/` scripts are runnable locally (CPU) for testing with reduced `--max-*` arguments:

```bash
python src/prepare_heart_dev_finetune_data.py --help
python src/build_heart_dev_trajectories.py --help
python src/finetune_heart_dev.py --help
python src/evaluate_heart_dev.py --help
```
