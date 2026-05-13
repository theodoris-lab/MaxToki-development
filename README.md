# Maxtoki Heart Development — Data Curation

Code and documentation for curating multi-source single-cell transcriptomics datasets covering human heart development from approximately 5.5 to 20 post-conceptual weeks (pcw).

## Overview

This repository contains scripts, notebooks, and reports for downloading, subsetting, and converting ~319,000 cells from 10 published datasets into a unified collection of AnnData H5AD files.

| Source | Datasets | Cells (curated) | Developmental window |
|---|---:|---:|---|
| CellxGene (9 datasets) | 9 | 211,692 | embryonic – 20th week pcf |
| Lázár et al. 2025 (*Nat. Genetics*) | 1 | 107,673 | 5.5 – 14.0 pcw |
| **Total** | **10** | **319,365** | **5.5 pcw – 20th week** |

Large H5AD/Loom/MTX data files are stored externally (see [Data](#data) below) and are not tracked by git.

## Repository Structure

```
scripts/                       # Pipeline scripts
│  download_datasets.sh        # Download all datasets (CellxGene, HCA, UCSC, lab)
│  download_datasets.sbatch    # Slurm wrapper for download_datasets.sh
│  subset_cellxgene_heart_development.py  # Filter CellxGene H5ADs to heart/fetal cells
│  convert_non_cellxgene_to_h5ad.py       # Convert HCA/UCSC/loom files to H5AD
│  convert_non_cellxgene_to_h5ad.sbatch   # Slurm wrapper for conversion
│  generate_data_summary.py    # Lightweight dataset summary report (no heavy deps)
│  report_cellxgene_heart_development_subset.py
│  report_cellxgene_subset_celltype_by_stage.py
│  report_converted_h5ad_metadata.py
│  submit_download_datasets_job.sh

notebooks/                     # Exploratory notebooks
│  preview_cellxgene_heart_subsets.ipynb

data_extraction/               # Notebooks used during data wrangling
│  data_preparation.ipynb
│  downloading_vent_cardiomyocytes.ipynb

data/                          # Small metadata files tracked in git
│  cellxgene_heart_development_subset_manifest_*.tsv

documents/                     # Reference documents
│  atlas.txt                   # Cardiac cell-type lineage tree
│  maxtoki_heart_development_data_survey_report.md  # Full curation report

dump/                          # Generated report outputs
```

## Data

Large data files are stored at (Gladstone HPC):

```
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/
  source_1_cellxgene/                   # Raw H5ADs from CellxGene
  source_1_cellxgene_heart_development_subset/  # Subsetted H5ADs
  source_2_human_early_embryogenesis_atlas/
  source_3_ucsc_cells/
  source_4_lab/
  source_2_3_4_h5ad_converted/          # Converted H5ADs
```

### Dataset Sources

| # | Dataset | First Author | Year | Journal | Assay |
|---:|---|---|---|---|---|
| 1 | Construction of a human cell landscape | Han et al. | 2020 | *Nature* | microwell-seq |
| 2 | Survey of human embryonic development | Cao et al. | 2020 | *Science* | sci-RNA-seq3 |
| 3 | Sex-Specific Control of Human Heart Maturation | Sim et al. | 2021 | *Circulation* | 10x 3′ v3 |
| 4 | Integrated adult and foetal hearts | Knight-Schrijver et al. | 2022 | *Nat. Cardiovasc. Res.* | 10x 3′ v2/v3 |
| 5–8 | Rotem 12W heart (A1/B1/C1/D1 Visium slides) | Leshem et al. | 2025 | *eLife* | Visium |
| 9 | snRNA-seq of human outflow tract and aortic valve | Leshem et al. | 2025 | *eLife* | 10x snRNA-seq |
| 10 | Spatiotemporal dynamics of the developing human heart | Lázár et al. | 2025 | *Nat. Genetics* | 10x scRNA-seq + Visium + ISS |

## Usage

### 1. Download datasets

```bash
# Interactive (fills MAXTOKI_DATA_DIR from the default or env var)
scripts/download_datasets.sh

# Slurm
sbatch scripts/download_datasets.sbatch

# Only specific sources
scripts/download_datasets.sh --only cellxgene,ucsc

# Dry-run to preview what would be downloaded
scripts/download_datasets.sh --dry-run
```

### 2. Subset CellxGene files to heart / fetal cells

```bash
python scripts/subset_cellxgene_heart_development.py
```

Filters to: `tissue ∈ {heart, ventricle, …}`, `disease = normal`, `organism = Homo sapiens`, embryonic/fetal developmental stages.

### 3. Convert non-CellxGene datasets to H5AD

```bash
# Interactive
python scripts/convert_non_cellxgene_to_h5ad.py

# Slurm (128 GB, 4 CPUs, 72 h)
sbatch scripts/convert_non_cellxgene_to_h5ad.sbatch
```

### 4. Generate reports

```bash
python scripts/generate_data_summary.py           # lightweight, no heavy deps
python scripts/report_cellxgene_heart_development_subset.py
python scripts/report_cellxgene_subset_celltype_by_stage.py
python scripts/report_converted_h5ad_metadata.py
```

## Environment

Scripts require:

- Python ≥ 3.10
- `anndata`, `h5py`, `numpy`, `pandas`, `scipy`

The Gladstone HPC conda environment used for development:

```
/gladstone/theodoris/home/eniyonkuru/miniconda3/envs/env_maxtoki
```

Slurm wrappers call this environment directly.

## Documentation

- [Data curation report](documents/maxtoki_heart_development_data_survey_report.md) — full dataset-by-dataset summary including cell counts, cell types, and developmental stage coverage.
- [Cardiac lineage tree](documents/atlas.txt) — reference tree of cardiac cell types and key transcription factors across developmental stages.
