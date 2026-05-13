# MaxToki — Fine-Tuning on Human Developmental Data

**MaxToki** is a single-cell foundation model developed in the Theodoris Lab. This repository contains the code and documentation for adapting MaxToki to human developmental biology through domain-specific fine-tuning and validation.

The core goal is to endow MaxToki with a deep understanding of gene programs that govern cell-type specification and maturation across human development — enabling the model to reason about developmental trajectories, predict the effect of perturbations during organogenesis, and generalize across developmental contexts.

---

## Vision

Foundation models for single-cell transcriptomics are typically pretrained on broad collections of adult and mixed-age tissue data. While powerful, they may not fully capture the dynamic, stage-specific gene regulatory programs that define early development. By fine-tuning MaxToki on high-quality developmental datasets, we aim to:

- Improve the model's representation of developmental cell states and lineage transitions
- Enable accurate prediction of transcriptional responses to perturbations during organogenesis
- Build a developmental-context-aware model that can be applied across multiple organ systems

**We start with cardiac development** — one of the best-characterized organ development systems with rich multi-modal single-cell data spanning the embryonic through fetal period. Cardiac development serves as a proof-of-concept and benchmark before expanding to other organs.

---

## Project Roadmap

```
Step 1 — Data Curation       ← current stage
  Collect, harmonize, and QC multi-source scRNA-seq/spatial datasets
  covering human heart development from 5.5 to 20 post-conceptual weeks

Step 2 — Fine-Tuning
  Fine-tune MaxToki on the curated developmental heart dataset
  using the Theodoris Lab training infrastructure

Step 3 — Validation
  Evaluate the fine-tuned model on held-out developmental datasets,
  perturbation prediction benchmarks, and cross-organ transfer tasks
```

---

## Step 1: Data Curation (Heart Development)

~319,000 cells were curated from 10 published datasets spanning embryonic through late-fetal human cardiac development (5.5–20 pcw). Data originates from four sources:

| Source | Datasets | Cells (curated) | Developmental window |
|---|---:|---:|---|
| CellxGene (9 datasets) | 9 | 211,692 | embryonic – 20th week pcf |
| Lázár et al. 2025 (*Nat. Genetics*) | 1 | 107,673 | 5.5 – 14.0 pcw |
| **Total** | **10** | **319,365** | **5.5 pcw – 20th week** |

Large H5AD/Loom/MTX data files (~90 GB total) are stored externally on the Gladstone HPC and are not tracked by git (see [Data Storage](#data-storage)).

---

## Repository Structure

```
scripts/                       # Pipeline scripts
│  download_datasets.sh        # Download all datasets (CellxGene, HCA, UCSC, lab)
│  download_datasets.sbatch    # Slurm wrapper for download_datasets.sh
│  subset_cellxgene_heart_development.py  # Filter CellxGene H5ADs to heart/fetal cells
│  convert_non_cellxgene_to_h5ad.py       # Convert HCA/UCSC/loom files to H5AD
│  convert_non_cellxgene_to_h5ad.sbatch   # Slurm wrapper for conversion
│  generate_data_summary.py    # Lightweight dataset summary (no heavy deps)
│  report_cellxgene_heart_development_subset.py
│  report_cellxgene_subset_celltype_by_stage.py
│  report_converted_h5ad_metadata.py
│  submit_download_datasets_job.sh

notebooks/                     # Exploratory notebooks
│  preview_cellxgene_heart_subsets.ipynb

data_extraction/               # Notebooks used during initial data wrangling
│  data_preparation.ipynb
│  downloading_vent_cardiomyocytes.ipynb

data/                          # Small metadata files tracked in git
│  cellxgene_heart_development_subset_manifest_*.tsv

documents/                     # Reference documents
│  atlas.txt                   # Cardiac cell-type lineage tree with key TFs
│  maxtoki_heart_development_data_survey_report.md  # Full curation report
```

---

## Data Storage

All large binary files are stored at (Gladstone HPC):

```
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/   (~90 GB total)
  source_1_cellxgene/                         # Raw H5ADs from CellxGene (~31 GB)
  source_1_cellxgene_heart_development_subset/# Subsetted heart/fetal H5ADs
  source_2_human_early_embryogenesis_atlas/   # HCA sparse matrix (~1.5 GB)
  source_3_ucsc_cells/                        # UCSC Cell Browser matrices (~56 GB)
  source_4_lab_directory/                     # Lab loom files (~2.8 GB)
  source_2_3_4_h5ad_converted/               # All non-CellxGene files converted to H5AD
```

---

## Dataset Sources

### Source 1 — CellxGene (9 datasets, ~31 GB)

Downloaded from the [CZI CellxGene portal](https://cellxgene.cziscience.com/) and subsetted to human embryonic/fetal heart cells using `subset_cellxgene_heart_development.py`.

| # | Dataset | First Author | Year | Journal | Assay | Curated cells |
|---:|---|---|---|---|---|---:|
| 1 | Construction of a human cell landscape | Han et al. | 2020 | *Nature* | microwell-seq | 7,997 |
| 2 | Survey of human embryonic development | Cao et al. | 2020 | *Science* | sci-RNA-seq3 | 101,749 |
| 3 | Sex-Specific Control of Human Heart Maturation | Sim et al. | 2021 | *Circulation* | 10x 3′ v3 | 26,394 |
| 4 | Integrated adult and foetal hearts | Knight-Schrijver et al. | 2022 | *Nat. Cardiovasc. Res.* | 10x 3′ v2/v3 | 30,889 |
| 5–8 | Rotem 12W heart — Visium slides A1/B1/C1/D1 | Leshem et al. | 2025 | *eLife* | Visium spatial | 4 × 4,992 |
| 9 | snRNA-seq of human outflow tract and aortic valve | Leshem et al. | 2025 | *eLife* | 10x snRNA-seq | 24,695 |

### Source 2 — Human Cell Atlas / Human Early Embryogenesis Atlas (~1.5 GB)

Downloaded via the [HCA Azul manifest API](https://data.humancellatlas.org/). Contains a sparse raw count matrix (`GSE157329_raw_counts.mtx.gz`) covering early human embryogenesis. Provides cellular context from the earliest stages of development, complementing the cardiac-focused CellxGene datasets.

### Source 3 — UCSC Cell Browser (~56 GB)

Five expression matrices from the [UCSC Cell Browser](https://cells.ucsc.edu/) (local copies, as the cluster cannot reach UCSC hosts directly):

| # | Dataset | Assay | Notes |
|---:|---|---|---|
| 1 | Human cardiogenesis — in vitro | scRNA-seq + ATAC | Directed differentiation of cardiomyocytes from hPSCs |
| 2 | Human cardiogenesis — in vivo | scRNA-seq + ATAC | In vivo cardiac progenitor reference |
| 3 | Multiomic human heart — snRNA-seq | snRNA-seq | Paired RNA component of adult multiomic heart atlas |
| 4 | Multiomic human heart — snATAC-seq | snATAC-seq | Paired ATAC component; chromatin accessibility reference |
| 5 | Heart of Cells — overall heart | scRNA-seq | Broad heart cell-type reference atlas |

These datasets provide both developmental and adult cardiac references, including chromatin accessibility data useful for understanding regulatory programs the model may need to learn.

### Source 4 — Theodoris Lab Internal Data (~2.8 GB)

Four datasets from the lab's GeneCorpus loom collection (`/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/`):

| # | Dataset | Notes |
|---:|---|---|
| 1 | Human fetal cis-regulatory elements | Gene expression linked to fetal regulatory element activity |
| 2 | Human fetal striatum atlas | Cross-organ fetal reference; useful for distinguishing cardiac-specific programs |
| 3 | Human megakaryocyte development | Hematopoietic developmental reference from yolk-sac and hESC stages |
| 4 | Fetal vs. adult human epicardium | Direct comparison of fetal and adult epicardial transcriptomes — directly relevant to cardiac maturation |

### Source 5 — Lázár et al. 2025 / Mendeley Data (107,673 cells)

Downloaded from [Mendeley Data](https://data.mendeley.com/). Spatiotemporal gene expression and cellular dynamics of the developing human heart (*Nat. Genetics*, 2025). The largest single dataset in this collection — 107,673 cells from 21 10x Chromium SC libraries spanning 5.5–14.0 pcw, with paired Visium spatial and in-situ sequencing (ISS) modalities. Already heart-specific; no further subsetting applied.

---

## Usage

### 1. Download datasets

```bash
# Download all sources to the default HPC directory
scripts/download_datasets.sh

# Slurm (24 h, 8 GB RAM)
sbatch scripts/download_datasets.sbatch

# Only specific sources
scripts/download_datasets.sh --only cellxgene,ucsc

# Preview without downloading
scripts/download_datasets.sh --dry-run
```

### 2. Subset CellxGene files to heart / fetal cells

```bash
python scripts/subset_cellxgene_heart_development.py
```

Filters to: `tissue ∈ {heart, ventricle, atrium, outflow tract, …}`, `disease = normal`, `organism = Homo sapiens`, embryonic/fetal developmental stages only.

### 3. Convert non-CellxGene datasets to H5AD

```bash
# Interactive
python scripts/convert_non_cellxgene_to_h5ad.py

# Slurm (128 GB RAM, 4 CPUs, 72 h)
sbatch scripts/convert_non_cellxgene_to_h5ad.sbatch
```

Converts HCA sparse matrices, UCSC TSV/MTX files, and lab loom files into unified AnnData H5AD format.

### 4. Generate reports

```bash
python scripts/generate_data_summary.py                    # lightweight, no heavy deps
python scripts/report_cellxgene_heart_development_subset.py
python scripts/report_cellxgene_subset_celltype_by_stage.py
python scripts/report_converted_h5ad_metadata.py
```

---

## Environment

Scripts require Python ≥ 3.10 with `anndata`, `h5py`, `numpy`, `pandas`, `scipy`.

Conda environment on the Gladstone HPC:

```
/gladstone/theodoris/home/eniyonkuru/miniconda3/envs/env_maxtoki
```

Slurm wrappers invoke this environment directly.

---

## Documentation

- [Data curation report](documents/maxtoki_heart_development_data_survey_report.md) — full dataset-by-dataset summary with cell counts, cell types, and developmental stage coverage across all 10 datasets.
- [Cardiac lineage tree](documents/atlas.txt) — reference hierarchy of cardiac cell types, key transcription factors, and developmental timing from zygote through the fetal period.
