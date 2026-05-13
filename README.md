# MaxToki Fine-Tuning on Human Developmental Data

Fine-tuning the MaxToki single-cell foundation model on human developmental transcriptomics to improve its representation of developmental cell states and lineage transitions.

We start with **cardiac development** as a proof of concept, then expand to other organs.

## Human Heart Development Atlas

We constructed a [human heart development atlas](documents/maxtoki_heart_development_data_survey_report.md) by aggregating and harmonizing multi-source single-cell and spatial transcriptomics data spanning 5.5–20 post-conceptual weeks. Datasets were filtered to normal human fetal heart tissue, unified into AnnData H5AD format, and annotated with consistent developmental stage and cell-type labels across 10 published studies totaling ~319,000 cells.

## Data Curation for Heart Development

Starting with ~319,000 cells spanning 5.5–20 post-conceptual weeks from two sources:

| Source | Description | Cells |
|---|---|---:|
| [CellxGene](https://cellxgene.cziscience.com/) | 9 scRNA-seq/Visium datasets subsetted to fetal heart | 211,692 |
| [Lázár et al. 2025](https://www.nature.com/articles/s41588-025-02352-6) | Spatiotemporal atlas of the developing human heart (Mendeley Data) | 107,673 |

Large files (~90 GB) are stored externally on the Gladstone HPC at `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` and are not tracked by git.

See the full [data curation report](documents/maxtoki_heart_development_data_survey_report.md) for dataset-level details.

