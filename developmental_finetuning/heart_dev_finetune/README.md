# MaxToki Heart-Development Fine-Tune

Fine-tuning pipeline for adapting the MaxToki foundational 94 M-parameter LLaMA-based model to predict **human heart developmental trajectories** from single-cell transcriptomics.

The model learns two joint objectives from the same paragraph format:
- **Cell-token prediction** — cross-entropy over response gene tokens
- **Timelapse prediction** — MSE regression on the developmental time gap between two cells (in PCW, post-conception weeks)

---

## Repository layout

```
heart_dev_finetune/
├── config/
│   └── ds_config_zero3_bf16.json     DeepSpeed ZeRO-3 + BF16 config
├── lib/
│   └── slack_notify.sh               Slack notification helpers for Slurm jobs
├── logs/
│   └── slurm/                        Slurm stdout/stderr logs (auto-created)
├── slurm/
│   ├── submit_finetune_pipeline.sh   One-shot pipeline submitter
│   ├── run_prepare_data.sh           Stage 1 Slurm job (CPU)
│   ├── run_build_trajectories.sh     Stage 2 Slurm job (CPU)
│   ├── run_train.sh                  Stage 3 Slurm job (GPU, DeepSpeed)
│   └── run_evaluate.sh               Stage 4 Slurm job (GPU)
└── src/
    ├── prepare_heart_dev_finetune_data.py   Stage 1 — harmonise & split datasets
    ├── build_heart_dev_trajectories.py      Stage 2 — build MaxToki paragraphs
    ├── finetune_heart_dev.py                Stage 3 — training loop
    ├── evaluate_heart_dev.py                Stage 4 — evaluation & metrics
    └── plot_training_progress.py            Live training-curve plotter
```

---

## Data sources

| Source | ~Cells | Notes |
|---|---|---|
| CellxGene heart-dev subset | ~350 K | `development_stage` column parsed to PCW |
| Tyser et al. | ~1.3 K | Early gastrulation (CS7, ~PCW 3) |
| Xu et al. | ~65 K | Fetal heart (PCW 5–25) |
| Lázár et al. | ~77 K | `pcw` column already numeric |

Tokenised per-source datasets are expected under:
```
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/tokenized/
```

Cell types are harmonised to 50 canonical types using:
```
cell_type_harmonization/cell_type_harmonization_map.json
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

Splits are **stage-based** (not donor-based) to test generalisation across developmental windows:

| Split | PCW range | Rationale |
|---|---|---|
| Train | < 10 or > 16 | Majority of data, covers early and late stages |
| Val | 10 – 12 | Cardiomyocyte maturation onset |
| Test | 13 – 16 | Mid-fetal heart |

---

## Pipeline stages

### Stage 1 — Prepare data (`prepare_heart_dev_finetune_data.py`)

- Loads tokenised per-source datasets
- Applies canonical cell-type harmonisation
- Parses heterogeneous developmental-stage strings → `dev_time_pcw` / `dev_time_num`
- Filters to cell types with ≥ 2 distinct PCW timepoints
- Saves `source_{train,val,test}_heart_dev.dataset` under `finetuning_heart_dev/`

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
- DeepSpeed ZeRO-3 + BF16, 4 × H200 GPUs
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

### Full pipeline (all 4 stages in sequence)

```bash
cd developmental_finetuning/heart_dev_finetune
bash slurm/submit_finetune_pipeline.sh
```

### Skip stages already completed

```bash
# Trajectories already built — submit training + evaluation only
bash slurm/submit_finetune_pipeline.sh --skip-prepare --skip-traj

# Evaluate on the test split instead of val
bash slurm/submit_finetune_pipeline.sh --skip-prepare --skip-traj --eval-test
```

### Override data sizes or hyperparameters

```bash
MAX_TRAIN=200000 EPOCHS=2 LR=0.0001 bash slurm/submit_finetune_pipeline.sh --skip-prepare --skip-traj
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
| Slurm partitions | `pod` (GPU), `ctbatch` (CPU) |

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
