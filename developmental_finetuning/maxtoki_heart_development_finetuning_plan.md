# MaxToki Heart Development Fine-Tuning Plan

Fine-tune the Theodoris-lab MaxToki foundational model to learn the temporal
dynamics of human heart development, using a merged single-cell dataset spanning
Day 7 (gastrulation) through PCW 40 (term) across four complementary sources.

The approach mirrors the brain aging fine-tuning pipeline
(`brain_aging_finetune_2026_04_29`) but adapts the time axis, grouping
strategy, and split design for developmental biology.

---

## Context: What the Brain Aging Pipeline Taught Us

| Component | Brain Aging | Heart Development (proposed) |
|---|---|---|
| Time axis | Age in months (`Age * 12`) | Developmental time in PCW (float) |
| Time grouping | `annot_res3,sex` (cell type × sex) | `canonical_cell_type` (cell type alone, or + dataset) |
| Held-out split | By donor (rank-based: youngest/oldest normal donors) | By developmental stage or by dataset |
| Starting weights | Previous brain-aging model `.safetensors` | Foundational 94M model (no heart-prior weights yet) |
| Loss | Mixed CE (cell token) + MSE (timelapse months) | Mixed CE + MSE (timelapse in PCW) |
| Data scale | ~1 M cells, 107 donors | ~493 K cells across 4 datasets |
| Training examples | 1 M trajectories | TBD — scale to available cells |
| Infrastructure | DeepSpeed ZeRO-3, 8× H200, Slurm | Same cluster infrastructure |

---

## Dataset Inventory

| Dataset key | Paper / source | Developmental window | Technology | Cells |
|---|---|---|---|---|
| **CXG** | CellxGene Heart Development Subset (10 h5ad files) | PCW 5–40 | 10x Chromium | ~350,000 |
| **Tyser** | Tyser et al. 2021 (`GSE157329_raw_counts.h5ad`) | Day 7–CS7 (~PCW 3) | Smart-seq2 | ~1,300 |
| **Xu** | Xu et al. 2024 (UCSC Cells, 2 h5ad files: in vitro + in vivo) | PCW 5–25 | 10x Chromium | ~65,000 |
| **Lázár** | Lázár et al. 2025 (Heart-Lung Atlas HL tier; 35 clusters) | PCW 5.5–14 | 10x Chromium | ~77,000 |

**Total: ~493,000 cells**

All h5ad files already live under:
```
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/
```

The CXG data has already been tokenized (by the `subset_cellxgene_heart_development.py`
pipeline). The non-CXG sources have been converted to h5ad but not yet merged
or tokenized as a MaxToki `.dataset`.

The cell-type harmonization map is at:
```
cell_type_harmonization/cell_type_harmonization_map.json   (50 canonical types)
cell_type_harmonization/cell_type_harmonization_table.csv
```

---

## The Four-Stage Pipeline

```
heart_dev_finetune/
├── slurm/
│   ├── submit_finetune_pipeline.sh      ← one-shot full-pipeline submit
│   ├── run_prepare_data.sh
│   ├── run_build_trajectories.sh
│   ├── run_train.sh
│   └── run_evaluate.sh
├── src/
│   ├── prepare_heart_dev_finetune_data.py
│   ├── build_heart_dev_trajectories.py
│   ├── finetune_heart_dev.py
│   └── evaluate_heart_dev.py
├── config/
│   └── ds_config_zero3_bf16.json
├── lib/
│   └── slack_notify.sh
└── logs/slurm/
```

---

## Stage 1 — Data Preparation

**Script:** `src/prepare_heart_dev_finetune_data.py`
**Slurm:** `slurm/run_prepare_data.sh` (12 CPU, 250 GB, ~1 h)

### What it does

1. **Load and merge all four source datasets** from disk (h5ad → HuggingFace
   `.dataset` via the same tokenization path used for CXG). The CXG files
   are already in h5ad form; Tyser and Xu have been converted. Lázár needs
   to be checked — if only h5ad (not yet tokenized), tokenize first.

2. **Add the unified developmental time column `dev_time_pcw`** (float,
   post-conception weeks):
   - CXG: parse `development_stage` UBERON string → PCW float
     (e.g. "12th week post-fertilization stage" → 12.0)
   - Tyser: Day 7–CS7 → convert to PCW (Day 7 = PCW ~1; CS7 ≈ PCW 3.0)
   - Xu: `developmental_stage` or equivalent metadata → PCW float
   - Lázár: `pcw` / `timepoint` column → PCW float
   
   All values end up as a single float column (e.g. 3.0, 5.5, 12.0, 20.0).

3. **Add `canonical_cell_type`** by applying `cell_type_harmonization_map.json`
   to each dataset's native cell type label column. This is analogous to
   `annot_res3` in the brain aging pipeline — the harmonized label used for
   trajectory grouping.

4. **Add `source_dataset`** column (`CXG`, `Tyser`, `Xu`, `Lazar`) to allow
   dataset-aware grouping or filtering later.

5. **Filter to cell types that have temporal coverage** — i.e., canonical types
   present at ≥ 2 distinct PCW timepoints across the merged dataset (needed for
   meaningful timelapse trajectories). Cell types with `✗` in the lineage tree
   and no dataset annotations are excluded.

6. **Define train / val / test splits** (developmental-stage–based, not
   donor-based):
   - Because this is developmental data, donors are not interchangeable across
     time the way brain aging donors are. Instead, hold out entire developmental
     windows:
     - **Val set:** PCW 10–12 (well-covered transition window spanning
       cardiomyocyte maturation onset and endocardial cushion remodeling)
     - **Test set:** PCW 13–16 (mid-fetal window with all major lineages
       present, used for final generalization assessment)
     - **Train set:** all remaining PCW (3–9, 17–40) — early embryonic and
       late fetal/neonatal data
   - Alternatively (to be decided with Christina): hold out by **dataset
     source** — e.g., hold out Xu as val, Lázár as test, train on CXG + Tyser.
     This tests cross-dataset generalization. Both options should be benchmarked.

7. **Write three donor-disjoint (or stage-disjoint) `.dataset` splits:**
   - `source_train_heart_dev.dataset`
   - `source_val_heart_dev.dataset`
   - `source_test_heart_dev.dataset`
   - plus a JSON manifest of split sizes, PCW ranges, cell counts per type.

### Key design decisions to confirm

- [ ] **Time unit:** use PCW as float weeks (e.g. 5.5, 12.0). Do not convert
  to months (as in brain aging) — keep PCW as the natural developmental unit.
  The token dictionary needs to have numeric tokens for PCW values, or we
  discretize to integer PCW steps.
- [ ] **Token dictionary:** check whether the existing
  `token_dictionary_aging_gc95M.pkl` contains PCW-range numeric tokens (it
  likely does not — it was built for month-range ages). A new token dictionary
  may need to be built for developmental PCW values (range ~3–40) or the
  existing one can be reused if PCW values fall within the month range (they
  do: PCW 3–40 overlaps with age 3–40 months).
- [ ] **Split strategy:** confirm stage-based vs. dataset-based split with
  Christina before implementing.

---

## Stage 2 — Trajectory Building

**Script:** `src/build_heart_dev_trajectories.py`
**Slurm:** `slurm/run_build_trajectories.sh` (24 CPU, 500 GB, ~2–4 h)

Mirrors `build_annot_res3_trajectories.py` from the brain aging pipeline.

### What it does

1. **Load the prepared train/val splits** from Stage 1.

2. **Assemble MaxToki cell-paragraph trajectories** using
   `CellParagraphAssembler`:
   - `time_group_columns = canonical_cell_type`
     (analogous to `annot_res3,sex` in brain aging — cell type is the primary
     grouping axis; sex is less meaningful here since developmental data has
     limited sex metadata)
   - `time_column = dev_time_pcw`
   - `min_timepoints = 2` (need at least two PCW points to form a trajectory)
   - Trajectories sample a context cell at one PCW and a target cell of the
     same canonical type at a later PCW, learning to predict forward in
     developmental time.

3. **Add `attention_mask` and `loss_mask`** (response-only loss masking after
   `<eoq>`), identical to brain aging.

4. **Add evaluation metadata** to the val dataset:
   - `context_dev_time_pcw`, `target_dev_time_pcw`
   - `true_timelapse_pcw` (= target − context PCW)
   - `canonical_cell_type`, `source_dataset`

5. **Write masked trajectory datasets:**
   - `trajectories/train/train_heart_dev_masked.dataset`
   - `trajectories/val/val_heart_dev_masked.dataset`

### Scale targets (starting estimates, to tune)

| Split | Target examples |
|---|---|
| Train | 500,000 |
| Val | 25,000 |

Scale is lower than brain aging (~1 M) because total cells are ~493 K vs.
~1 M. Adjust if training is too fast (increase) or if OOM (decrease).

---

## Stage 3 — Fine-Tuning

**Script:** `src/finetune_heart_dev.py`
**Slurm:** `slurm/run_train.sh` (4–8× GPU H200, 500 GB, up to 7 days)

Mirrors `finetune_brain_aging_annot_res3.py`.

### What it does

1. **Load foundational model architecture** from:
   ```
   /gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/foundational_94M_model/
   ```
   (same foundational weights used in brain aging)

2. **No pre-trained heart weights yet** — this is the first heart fine-tune,
   so we start directly from the foundational model (not from brain aging
   weights, which encode age in a non-developmental way).
   - After an initial training run, the resulting weights become the "previous
     heart weights" for future fine-tuning rounds.

3. **`PredModel` wrapper** — same architecture as brain aging: LLaMA backbone
   + scalar linear head for timelapse (PCW delta) regression.

4. **`MaxTokiHeartDevTrainer`** — mixed CE + MSE loss:
   - CE: cross-entropy on cell token prediction (which gene tokens appear in
     target cell)
   - MSE: regression on timelapse prediction (how many PCW forward)
   - Same loss formulation as brain aging; only the timelapse unit changes
     (months → PCW).

5. **Training configuration:**
   ```
   --per-device-train-batch-size 1
   --gradient-accumulation-steps 256
   --epochs 1               # start with 1, increase if loss still falling
   --max-train-samples 500000
   --max-val-samples 10000
   --do-eval
   ```

6. **DeepSpeed ZeRO-3 + BF16** (same `ds_config_zero3_bf16.json`).

7. **Output:** saves final model to:
   ```
   /gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/
   finetuning_heart_dev/model/
   ```

---

## Stage 4 — Evaluation

**Script:** `src/evaluate_heart_dev.py`
**Slurm:** `slurm/run_evaluate.sh` (1× GPU, 200 GB, ~1–2 h)

Mirrors `evaluate_brain_aging_annot_res3.py`.

### What it does

Evaluates the fine-tuned model on held-out val trajectories and writes:

| Output file | Content |
|---|---|
| `evaluation_metrics.json` | `combined_loss`, `mse_loss`, `ce_loss`, timelapse MAE/RMSE/Pearson r |
| `timelapse_pcw_predictions.csv` | per-example true vs. predicted PCW timelapse and PCW timepoints |
| `cell_ce_losses.csv` | per-example CE loss for cell-token prediction examples |

### Key metrics

- **Timelapse MAE** (in PCW) — can the model predict how far forward a cell
  has progressed in development?
- **Timelapse Pearson r** — correlation of predicted vs. true PCW delta
- **CE loss by cell type** — which lineages does the model learn best?
- **Cross-dataset generalization** — if using dataset-based split, does the
  model generalize from CXG to Xu or Lázár?

---

## Data Paths (Proposed)

| What | Path |
|---|---|
| Source h5ad files | `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` |
| Token dictionary | `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl` (reuse if PCW range fits; else build new) |
| Foundational model | `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/foundational_94M_model/` |
| MaxToki source code | `/gladstone/theodoris/lab/models/MaxToki` |
| Pipeline output root | `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/finetuning_heart_dev/` |
| Scripts repo | `maxtoki_development/developmental_finetuning/heart_dev_finetune/` |

---

## Open Questions / Decisions Needed

1. **Token dictionary:** Does `token_dictionary_aging_gc95M.pkl` already cover
   PCW 3–40 as numeric tokens? If it does (likely, since months 3–40 overlap),
   we can reuse it. If not, we need to build a new one for PCW.

2. **Split strategy (critical):** Stage-based split (hold out PCW 10–16) or
   dataset-based split (hold out Xu/Lázár)?
   - Stage-based tests *temporal generalization* (can it predict later PCW
     from earlier context?)
   - Dataset-based tests *cross-study generalization* (is it robust to
     batch/technology differences?)
   - **Recommendation:** start with stage-based split since we have fewer cells
     and PCW 10–16 is the richest window.

3. **Time grouping columns:** `canonical_cell_type` alone, or
   `canonical_cell_type,source_dataset`? Adding `source_dataset` would let the
   model learn dataset-conditioned trajectories, but might limit trajectory
   pool size for sparse types.

4. **Tyser dataset:** only ~1,300 cells from Day 7–PCW 3 (earliest window).
   Should they be included or will they create problematic short trajectories
   given the large PCW gap to the next data (PCW 5)?

5. **What to do with `✗` cell types:** cell types marked as not found in any
   dataset (e.g., Cardiomyocyte Lineage progenitor, AV Canal Endocardial) are
   excluded from trajectory building. Confirm this is correct.

6. **Multi-round strategy:** after this first heart fine-tune, future rounds
   could incorporate additional data (e.g., spatial transcriptomics from
   Lázár 2025 zip files, or additional fetal cardiac datasets) and fine-tune
   from the first heart checkpoint rather than the foundational model.

---

## Immediate Next Steps

1. **Confirm token dictionary coverage** — run a quick check to see if PCW
   values 3.0–40.0 appear as keys in `token_dictionary_aging_gc95M.pkl`.
2. **Decide split strategy** with Christina.
3. **Audit Lázár h5ad** — the zip files haven't been extracted yet; confirm
   the HL-tier 35-cluster h5ad is available and has a PCW column.
4. **Write `prepare_heart_dev_finetune_data.py`** — adapting the brain aging
   prepare script for multi-dataset merge, PCW time axis, and harmonized cell
   types.
5. **Write `build_heart_dev_trajectories.py`** — adapting the brain aging
   trajectory builder for `dev_time_pcw` and `canonical_cell_type` grouping.
6. **Copy and adapt Slurm scripts** from the brain aging pipeline.
7. **First training run** on a small subset
   (`MAX_TRAIN_SAMPLES=10000 EPOCHS=1`) to verify the pipeline end-to-end
   before committing to a full multi-day training job.
