# MaxToki Fine-Tuning on Human Developmental Data

Fine-tuning the MaxToki single-cell foundation model on human developmental transcriptomics to improve its representation of developmental cell states and lineage transitions.

We start with **cardiac development** as a proof of concept, then expand to other organs.

## Human Heart Development Lineage Tree

To guide data curation and model training, we built a [hierarchical cardiac cell-type lineage tree](documents/human_heart_development_lineage_tree_with_dataset_synonyms_v2.txt) from publicly available literature on human heart development. The goal was to map how cells differentiate — from the zygote all the way to mature cardiac cell types present at birth — capturing the full developmental trajectory of the human heart.

The lineage tree is organized hierarchically and includes:
- **Differentiation hierarchy** — from zygote → mesoderm → cardiac progenitors → specialized cardiac cell types
- **PCW** (post-conceptual weeks) — the developmental time window when each cell type emerges or is active
- **Transcription factors** — key regulators driving each differentiation step, where known from literature
- **Dataset synonyms** — observed cell-type labels from each source dataset, used to build the harmonization map
- **`*`** — marks cell types present in our downloaded dataset, allowing direct mapping between the lineage tree and available data

## Data Curation for Heart Development

305,835 cells spanning gastrulation (Carnegie Stage 7, ~Day 17) through 20 post-conceptual weeks (PCW), curated from four sources:

| Source | Description | Datasets | Cells |
|---|---|---:|---:|
| [CellxGene](https://cellxgene.cziscience.com/) | scRNA-seq studies subsetted to embryonic/fetal heart (Visium excluded) | 5 | 191,724 |
| [Lázár et al. 2025](https://www.nature.com/articles/s41588-025-02352-6) | Spatiotemporal atlas of the developing human heart (Mendeley Data) | 1 | 107,673 |
| [Tyser et al. 2021](https://www.nature.com/articles/s41586-021-04158-y) | Single-cell gastrulation atlas (EMBL-EBI, Smart-seq2) | 1 | 1,195 |
| [Xu et al. 2023](https://www.nature.com/articles/s41556-023-01108-w) | Curated cardiac subset of whole-embryo organogenesis atlas (lab directory) | 1 | 5,243 |
| **Total** | | **8** | **305,835** |

> **Note — Visium excluded:** The 4 Visium spatial transcriptomics slides (Leshem et al. 2025; 19,968 spots) are excluded from training data because Visium is not single-cell resolution.

Large files (~90 GB) are stored externally on the Gladstone HPC at `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` and are not tracked by git.

See the full [data curation report](documents/maxtoki_heart_development_data_survey_report.md) for dataset-level details.

## Cell Type Harmonization

To enable consistent training across datasets, observed cell-type labels are mapped to a set of canonical types anchored to the lineage tree. The harmonization pipeline lives in `cell_type_harmonization/` and produces three outputs:

| File | Description |
|---|---|
| `cell_type_harmonization_map.json` | Maps each observed label to a canonical lineage-tree cell type with confidence tier (`high` / `medium` / `low`) and full lineage path |
| `cell_type_harmonization_table.csv` | Flat table of all observed → canonical mappings |
| `cell_type_harmonization_review_queue.csv` | Labels flagged for manual review (low confidence or unmapped) |

Harmonization is applied by `scripts/apply_harmonization.py`, which adds three columns to each dataset's `.obs`:

| Column | Description |
|---|---|
| `cell_type_harmonized` | Canonical label from the lineage tree |
| `harmonization_confidence` | `high` / `medium` / `low` / `none` |
| `lineage_path_str` | Full ancestor path from root, joined with ` → ` |

## Fine-Tuning Pipeline

The heart-development fine-tune lives in `developmental_finetuning/heart_dev_finetune/`. It adapts the MaxToki 94 M-parameter foundational model to predict developmental trajectories, learning two joint objectives:

- **Cell-token prediction** — cross-entropy over response gene tokens
- **Timelapse prediction** — MSE regression on the developmental time gap between two cells (in PCW)

The pipeline runs in five Slurm stages:

| Stage | Script | Description |
|---|---|---|
| 0 | `src/tokenize_heart_dev_sources.py` | Tokenize source h5ads into HuggingFace `.dataset` files |
| 1 | `src/prepare_heart_dev_finetune_data.py` | Harmonize and split datasets into train / val / test |
| 2 | `src/build_heart_dev_trajectories.py` | Build MaxToki paragraph trajectories |
| 3 | `src/finetune_heart_dev.py` | Training loop (GPU, DeepSpeed ZeRO-3) |
| 4 | `src/evaluate_heart_dev.py` | Evaluation and metrics |

See `developmental_finetuning/heart_dev_finetune/README.md` for full pipeline details.

## Data Curation Scripts

Utility scripts for dataset download and preprocessing live in `scripts/`:

| Script | Purpose |
|---|---|
| `download_datasets.sh` / `download_datasets.sbatch` | Download CellxGene h5ads and non-CXG datasets to HPC storage |
| `subset_cellxgene_heart_development.py` | Filter CellxGene h5ads to cardiac / embryonic / normal observations |
| `convert_non_cellxgene_to_h5ad.py` | Convert non-CXG source datasets (Tyser, Xu) to h5ad format |
| `convert_lazar_to_h5ad.py` | Convert Lázár RDS metadata + HDF5 counts to h5ad format |
| `build_cell_type_harmonization.py` | Build the initial harmonization map from lineage tree and dataset labels |
| `apply_harmonization.py` | Apply the harmonization map to h5ad `.obs`, adding `cell_type_harmonized` columns |
| `visualize_lineage_tree.py` | Generate interactive HTML lineage tree visualization |
| `plot_lineage_tree_author_labels.py` | Plot author-provided cell-type labels overlaid on the lineage tree |
| `plot_train_val_test_coverage.py` | Generate train/val/test coverage dot-plot across PCW timepoints |
| `utils.py` | Shared utilities (h5ad I/O, metadata helpers) |

## Data Extraction Notebooks

`data_extraction/` contains exploratory notebooks used during dataset curation:

| Notebook | Purpose |
|---|---|
| `data_preparation.ipynb` | Initial exploration and QC of downloaded datasets |
| `downloading_vent_cardiomyocytes.ipynb` | Exploratory download of ventricular cardiomyocyte subsets from CellxGene |

## Contact

For questions about this repository, please reach out:

- **Enock Niyonkuru** — enock.niyonkuru@ucsf.edu · enock.niyonkuru@gladstone.ucsf.edu
- **Javier Gomez** — javier.gomezortega@gladstone.ucsf.edu
