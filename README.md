# MaxToki — Fine-Tuning on Human Developmental Data

Fine-tuning the [MaxToki](https://github.com/theodoris-lab) single-cell foundation model on human developmental transcriptomics to improve its representation of developmental cell states and lineage transitions.

We start with **cardiac development** as a proof of concept, then expand to other organs.

## Roadmap

| Step | Status |
|---|---|
| 1. Data curation | ✅ in progress |
| 2. Fine-tuning | 🔲 next |
| 3. Validation | 🔲 planned |

## Data (Step 1 — Heart Development)

~319,000 cells across 10 datasets spanning 5.5–20 post-conceptual weeks, curated from five sources:

| Source | Description | Cells |
|---|---|---:|
| [CellxGene](https://cellxgene.cziscience.com/) | 9 scRNA-seq/Visium datasets subsetted to fetal heart | 211,692 |
| [Lázár et al. 2025](https://www.nature.com/articles/s41588-025-02352-6) | Spatiotemporal atlas of the developing human heart (Mendeley Data) | 107,673 |
| [HCA Early Embryogenesis Atlas](https://data.humancellatlas.org/) | Sparse count matrix from early human embryogenesis | — |
| [UCSC Cell Browser](https://cells.ucsc.edu/) | In vitro/in vivo cardiogenesis + multiomic heart matrices | — |
| Lab internal (GeneCorpus) | Fetal epicardium, fetal cis-regulatory elements, megakaryocyte development | — |

Large files (~90 GB) are stored externally on the Gladstone HPC at `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` and are not tracked by git.

See the full [data curation report](documents/maxtoki_heart_development_data_survey_report.md) for dataset-level details.

## Usage

```bash
# 1. Download all datasets
scripts/download_datasets.sh          # or: sbatch scripts/download_datasets.sbatch

# 2. Subset CellxGene files to fetal heart cells
python scripts/subset_cellxgene_heart_development.py

# 3. Convert HCA / UCSC / loom files to H5AD
python scripts/convert_non_cellxgene_to_h5ad.py   # or: sbatch scripts/convert_non_cellxgene_to_h5ad.sbatch

# 4. Generate reports
python scripts/generate_data_summary.py
```

## Environment

Python ≥ 3.10 with `anndata`, `h5py`, `numpy`, `pandas`, `scipy`.
Conda env on Gladstone HPC: `/gladstone/theodoris/home/eniyonkuru/miniconda3/envs/env_maxtoki`
