# Maxtoki Development Data Inventory

Generated: 2026-04-15

Data directory:

```text
/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data
```

This document summarizes the datasets currently present in `maxtoki_development_data`, where each file came from, its size, and the biological scope of the dataset.

## Summary

| Source group | Directory | Current size | Status |
|---|---:|---:|---|
| Source 1: CellxGene | `source_1_cellxgene` | 31G | Complete |
| Source 2: Human Early Embryogenesis Atlas | `source_2_human_early_embryogenesis_atlas` | 1.5G | Complete |
| Source 3: UCSC / local copied matrices | `source_3_ucsc_cells` | 56G | Complete for current 5-file scope |
| Source 4: Lab directory copies | `source_4_lab_directory` | 2.8G | Complete |
| Total data directory | `maxtoki_development_data` | 90G | Complete for current scope |

Notes:

- The original Source 3 `.h5ad` and subset-matrix downloads were removed from the current scope.
- Source 3 files were ultimately supplied/copied locally because direct access to `cells.ucsc.edu` timed out from the Gladstone cluster.
- Runtime logs live under `maxtoki_development_data/logs` and are not included in the dataset-file tables below.
- The HCA `.download_complete` marker and `download_manifest.tsv` are operational metadata, not biological data files.

## Source 1: CellxGene

These files were downloaded from CellxGene/CZI as `.h5ad` AnnData objects. They provide broad human single-cell and spatial datasets relevant to developmental, fetal, adult, and heart-focused analyses.

| # | File | Size | Origin | Dataset notes |
|---:|---|---:|---|---|
| 1 | `source_1_cellxgene/01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad` | 1.4GiB | `https://datasets.cellxgene.cziscience.com/74c3403a-451c-4a62-84e0-d8a8e45c7ea7.h5ad` | Human cell landscape across 49 tissues, normal human samples, microwell-seq; useful as a broad reference atlas. |
| 2 | `source_1_cellxgene/02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad` | 4.7GiB | `https://datasets.cellxgene.cziscience.com/c3bf819d-423d-435f-b8d0-e36ad6088138.h5ad` | One-million-cell subset of a human fetal gene expression atlas across 15 tissues, generated with sci-RNA-seq3. |
| 3 | `source_1_cellxgene/03_survey_of_human_embryonic_development.h5ad` | 19GiB | `https://datasets.cellxgene.cziscience.com/dd2564a6-27a0-433a-893c-72475e4a39fe.h5ad` | Full human embryonic/fetal development atlas across 15 tissues; largest CellxGene dataset currently stored here. |
| 4 | `source_1_cellxgene/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad` | 817MiB | `https://datasets.cellxgene.cziscience.com/d61a74ab-e1ef-4ced-9131-698bf7d94be2.h5ad` | Heart maturation dataset focused on sex-specific effects and progesterone receptor biology in the left ventricle. |
| 5 | `source_1_cellxgene/05_integrated_adult_and_foetal_hearts.h5ad` | 410MiB | `https://datasets.cellxgene.cziscience.com/51073d23-97b7-4c05-84eb-5a18024e966c.h5ad` | Integrated adult and fetal heart single-cell RNA-seq dataset across multiple heart tissues. |
| 6 | `source_1_cellxgene/06_rotem_12w_heart_c1.h5ad` | 34MiB | `https://datasets.cellxgene.cziscience.com/380b448b-85de-4953-8e82-2fda20276a12.h5ad` | 12-week human heart spatial transcriptomics sample C1 from the developing outflow tract study. |
| 7 | `source_1_cellxgene/07_rotem_12w_heart_b1.h5ad` | 37MiB | `https://datasets.cellxgene.cziscience.com/57c7e31e-6bf5-4498-a2d3-2a3728c64ded.h5ad` | 12-week human heart spatial transcriptomics sample B1 from the developing outflow tract study. |
| 8 | `source_1_cellxgene/08_rotem_12w_heart_d1.h5ad` | 25MiB | `https://datasets.cellxgene.cziscience.com/72e35ce5-fb20-46d0-adf9-a8c7f44af287.h5ad` | 12-week human heart spatial transcriptomics sample D1 from the developing outflow tract study. |
| 9 | `source_1_cellxgene/09_rotem_12w_heart_a1.h5ad` | 43MiB | `https://datasets.cellxgene.cziscience.com/731fb49f-4a81-48d5-9f28-ee1b08f1018d.h5ad` | 12-week human heart spatial transcriptomics sample A1 from the developing outflow tract study. |
| 10 | `source_1_cellxgene/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad` | 438MiB | `https://datasets.cellxgene.cziscience.com/e6c07fbd-c90b-48c0-b6e3-b03b2d7218c5.h5ad` | Single-nuclei RNA-seq of human outflow tract and aortic valve tissue spanning CS16-17, 12 pcw, and adult samples. |

## Source 2: Human Early Embryogenesis Atlas

This source came from an HCA/Azul manifest download. The downloaded data currently consists of a raw count matrix from GEO accession-style file naming.

| # | File | Size | Origin | Dataset notes |
|---:|---|---:|---|---|
| 1 | `source_2_human_early_embryogenesis_atlas/93a9e248-b704-419f-b5ab-a0b96eefeaa0/GSE157329_raw_counts.mtx.gz` | 1.3GiB | HCA/Azul manifest URL in `documents/data_sources.txt` | Sparse raw count matrix associated with the Human Early Embryogenesis Atlas source; useful for early human developmental expression analyses. |

## Source 3: UCSC Cell Browser Matrices

These are the current Source 3 files after the scope change that removed `.h5ad` files and the subset matrix. The UCSC host was not reachable from the cluster, so these files were supplied locally and copied into `source_3_ucsc_cells`.

| # | File | Size | Origin | Dataset notes |
|---:|---|---:|---|---|
| 1 | `source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz` | 1.7GiB | Local copy corresponding to `https://cells.ucsc.edu/cardiogenesis-atac/in-vitro/exprMatrix.tsv.gz` | Matrix for in vitro human cardiogenesis data from the UCSC Cell Browser cardiogenesis-atac source. |
| 2 | `source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz` | 341MiB | Local copy corresponding to `https://cells.ucsc.edu/cardiogenesis-atac/in-vivo/exprMatrix.tsv.gz` | Matrix for in vivo human cardiogenesis data from the UCSC Cell Browser cardiogenesis-atac source. |
| 3 | `source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.mtx.gz` | 21GiB | Local copy corresponding to `https://cells.ucsc.edu/multiomic-human-heart/rna/matrix.mtx.gz` | Sparse matrix for the multiomic human heart snRNA-seq component. |
| 4 | `source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.mtx.gz` | 25GiB | Local copy corresponding to `https://cells.ucsc.edu/multiomic-human-heart/atac/matrix.mtx.gz` | Sparse matrix for the multiomic human heart snATAC-seq component. |
| 5 | `source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.tsv.gz` | 361MiB | Local copy corresponding to UCSC Heart of Cells overall heart scRNA-seq `exprMatrix.tsv.gz` | Overall heart scRNA-seq matrix from the UCSC Heart of Cells browser view. |

## Source 4: Lab Directory

These files were copied from existing lab storage under `/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom`. Most files are `.loom` expression matrices, with supporting QC/log files for the megakaryocyte development directory.

| # | File | Size | Origin | Dataset notes |
|---:|---|---:|---|---|
| 1 | `source_4_lab_directory/01_human_fetal_cis_regulatory_elements.loom` | 1.3GiB | `/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/9010519993/File_S3_Matrix.Gene_Raw_Counts_of_Cells.loom` | Human fetal cis-regulatory elements-related expression/count matrix, copied from the lab GeneCorpus loom collection. |
| 2 | `source_4_lab_directory/02_human_fetal_striatum_atlas.loom` | 1.4GiB | `/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/E-MTAB-8894/E-MTAB-8894.loom` | Human fetal striatum atlas dataset in loom format, copied from the lab GeneCorpus loom collection. |
| 3a | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.loom` | 91MiB | `/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/4110056855/` | Human megakaryocyte development loom matrix for yolk-sac stage cells. |
| 3b | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene_log.txt` | 234KiB | Same local directory as above | Processing log accompanying the yolk-sac stage loom matrix. |
| 3c | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene_per_cell_summary.pickle` | 3.2MiB | Same local directory as above | Per-cell summary metadata generated during processing of the yolk-sac stage matrix. |
| 3d | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene_postcheck.txt` | 3.2KiB | Same local directory as above | Post-check report for the yolk-sac stage matrix. |
| 3e | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.loom` | 77MiB | Same local directory as above | Human embryonic stem cell day 0 loom matrix related to megakaryocyte-development comparisons. |
| 3f | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene_log.txt` | 233KiB | Same local directory as above | Processing log accompanying the hESC day 0 loom matrix. |
| 3g | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene_per_cell_summary.pickle` | 2.8MiB | Same local directory as above | Per-cell summary metadata generated during processing of the hESC day 0 matrix. |
| 3h | `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene_postcheck.txt` | 3.2KiB | Same local directory as above | Post-check report for the hESC day 0 matrix. |
| 4 | `source_4_lab_directory/04_fetal_vs_adult_human_epicardium.loom` | 302MiB | `/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/cxg/5500c673-1610-40a0-86d9-64d987ae50e6.loom` | Fetal versus adult human epicardium loom matrix from the local lab GeneCorpus collection. |

## Operational Notes

- Source 1 and Source 2 were downloaded by `scripts/download_datasets.sh`.
- Source 3 was assembled from local copies because the cluster could not establish TCP connections to UCSC hosts such as `cells.ucsc.edu`, `genome.soe.ucsc.edu`, or `hgdownload.soe.ucsc.edu`.
- Source 4 was copied from the lab directory using `rsync`.
- The downloader is resumable for direct downloads: complete final files are skipped, and interrupted direct downloads resume from `.part` files.
- Current visible data files exclude logs, Slurm output files, `download_manifest.tsv`, and the Source 2 `.download_complete` marker.

