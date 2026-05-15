# MaxToki Fine-Tuning on Human Developmental Data

Fine-tuning the MaxToki single-cell foundation model on human developmental transcriptomics to improve its representation of developmental cell states and lineage transitions.

We start with **cardiac development** as a proof of concept, then expand to other organs.

## Human Heart Development Atlas

To guide data curation and model training, we built a [hierarchical cardiac cell-type atlas](documents/human_heart_development_atlas.txt) from publicly available literature on human heart development. The goal was to map how cells differentiate — from the zygote all the way to mature cardiac cell types present at birth — capturing the full developmental trajectory of the human heart.

The atlas is organized as a lineage tree and includes:
- **Differentiation hierarchy** — from zygote → mesoderm → cardiac progenitors → specialized cardiac cell types
- **PCW** (post-conceptual weeks) — the developmental time window when each cell type emerges or is active
- **Transcription factors** — key regulators driving each differentiation step, where known from literature
- **`*`** — marks cell types present in our downloaded dataset, allowing direct mapping between the atlas and available data

## Data Curation for Heart Development

Starting with ~319,000 cells spanning 5.5–20 post-conceptual weeks from two sources:

| Source | Description | Cells |
|---|---|---:|
| [CellxGene](https://cellxgene.cziscience.com/) | 9 scRNA-seq datasets subsetted to fetal heart (Visium slides excluded) | 191,724 |
| [Lázár et al. 2025](https://www.nature.com/articles/s41588-025-02352-6) | Spatiotemporal atlas of the developing human heart (Mendeley Data) | 107,673 |

> **Note — Visium excluded:** The 4 Visium spatial transcriptomics slides (Leshem et al. 2025, datasets 5–8; 19,968 spots) are excluded from training data because Visium is not single-cell resolution.

**Datasets to add:**
- [Tyser et al. *Nature* 2021](https://pubmed.ncbi.nlm.nih.gov/34789876/) — human gastrulation atlas; available at `/gladstone/theodoris/lab/ctheodoris/validation/gastrulation/` (added to download script)
- [Xu et al. *Nat. Cell Biol.* 2023](https://www.nature.com/articles/s41556-023-01113-z) — human organogenesis atlas; **path needed from David**

Large files (~90 GB) are stored externally on the Gladstone HPC at `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/` and are not tracked by git.

See the full [data curation report](documents/maxtoki_heart_development_data_survey_report.md) for dataset-level details.

