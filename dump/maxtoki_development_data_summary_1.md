# Maxtoki Development Data: Shape and Head Summary

## Overview

| # | source | dataset | size | dimension | unique cells | kind |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CellxGene | Construction of a human cell landscape at single-cell level | 1.3GiB | 599,926 observations x 26,069 variables | 599,926 | AnnData H5AD |
| 2 | CellxGene | Survey of human embryonic development | 18.7GiB | 4,062,980 observations x 45,676 variables | 4,062,980 | AnnData H5AD |
| 3 | CellxGene | Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor | 816.5MiB | 51,176 observations x 35,477 variables | 51,176 | AnnData H5AD |
| 4 | CellxGene | Integrated adult and foetal hearts | 409.1MiB | 60,668 observations x 26,886 variables | 60,668 | AnnData H5AD |
| 5 | CellxGene | Rotem_12W_heart_C1 | 34.0MiB | 4,992 observations x 35,476 variables | 4,992 | AnnData H5AD |
| 6 | CellxGene | Rotem_12W_heart_B1 | 36.7MiB | 4,992 observations x 35,476 variables | 4,992 | AnnData H5AD |
| 7 | CellxGene | Rotem_12W_heart_D1 | 24.2MiB | 4,992 observations x 35,476 variables | 4,992 | AnnData H5AD |
| 8 | CellxGene | Rotem_12W_heart_A1 | 42.8MiB | 4,992 observations x 35,476 variables | 4,992 | AnnData H5AD |
| 9 | CellxGene | Single-nuclei RNA-seq of human outflow tract and aortic valve tissue | 437.1MiB | 30,125 observations x 31,008 variables | 30,125 | AnnData H5AD |
| 10 | Human Early Embryogenesis Atlas | GSE157329 raw counts | 1.3GiB | 32,351 rows x 185,140 columns | 185,140 | Matrix Market sparse coordinate matrix |
| 11 | UCSC Cells | Human cardiogenesis in vitro expression matrix | 1.7GiB | 24,919 rows x 78,609 columns | 78,608 | Gzipped tab-separated expression matrix |
| 12 | UCSC Cells | Human cardiogenesis in vivo expression matrix | 340.3MiB | 24,919 rows x 30,427 columns | 30,426 | Gzipped tab-separated expression matrix |
| 13 | UCSC Cells | Multiomic human heart snRNA-seq matrix | 20.5GiB | 16,115 rows x 2,275,105 columns | 2,275,105 | Matrix Market sparse coordinate matrix |
| 14 | UCSC Cells | Multiomic human heart snATAC-seq matrix | 24.7GiB | 654,221 rows x 690,044 columns | 690,044 | Matrix Market sparse coordinate matrix |
| 15 | UCSC Cells | Heart of Cells overall heart scRNA-seq expression matrix | 360.6MiB | 33,538 rows x 142,947 columns | 142,946 | Gzipped tab-separated expression matrix |
| 16 | Lab Directory | Human fetal cis-regulatory elements | 1.2GiB | 19,329 genes/features x 185,061 cells | 185,061 | Loom HDF5 matrix |
| 17 | Lab Directory | Human fetal striatum atlas | 1.4GiB | 38,263 genes/features x 150,129 cells | 150,129 | Loom HDF5 matrix |
| 18 | Lab Directory | Human megakaryocyte development: yolk-sac stage | 90.9MiB | 17,614 genes/features x 11,021 cells | 11,021 | Loom HDF5 matrix |
| 19 | Lab Directory | Human megakaryocyte development: hESC Day 0 | 76.2MiB | 17,091 genes/features x 9,485 cells | 9,485 | Loom HDF5 matrix |
| 20 | Lazar et al. 2025 | Spatial dynamics of the developing human heart | 16.8GiB | 76,991 cells x 59,480 features | 76,991 | CellRanger H5 + Visium/ISS (zip archives) |

## 1. Construction of a human cell landscape at single-cell level

- Source group: `CellxGene`
- File: `source_1_cellxgene/01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad`
- Size: 1.3GiB
- Data kind: AnnData H5AD
- Dimension: 599,926 observations x 26,069 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 599,926 observations x 26,069 variables |
| file size | 1.3GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 599,926 (observation/cell axis count)
- Unique cell types: 44 values from `cell_type`
  - `erythroid progenitor cell`, `fibroblast`, `epithelial cell`, `mesothelial cell`, `stratified epithelial cell`, `T cell`, `mast cell`, `endothelial cell`
  - `astrocyte`, `oligodendrocyte`, `mesenchymal stem cell`, `chondrocyte`, `professional antigen presenting cell`, `peptic cell`, `goblet cell`, `endocrine cell`
  - `cell of skeletal muscle`, `smooth muscle cell`, `Sertoli cell`, `macrophage`, `B cell`, `dendritic cell`, `stromal cell`, `neuron`
  - `monocyte`, `enterocyte`, `acinar cell`, `basal cell`, `primordial germ cell`, `myeloid cell`, `erythroid lineage cell`, `neutrophil`
  - `plasma cell`, `alternatively activated macrophage`, `pulmonary alveolar type 2 cell`, `thyroid follicular cell`, `epithelial cell of proximal tubule`, `embryonic stem cell`, `renal intercalated cell`, `inflammatory cell`
  - `kidney loop of Henle epithelial cell`, `epithelial cell of exocrine pancreas`, `ventricular cardiac muscle cell`, `cord blood hematopoietic stem cell`
- Unique tissues: 49 values from `tissue`
  - `embryonic stem cell`, `uterine cervix`, `ureter`, `intestine`, `blood`, `testis`, `stomach`, `heart`
  - `brain`, `eye`, `pleura`, `ovary`, `uterus`, `adipose tissue`, `esophagus`, `rectum`
  - `vermiform appendix`, `ascending colon`, `transverse colon`, `sigmoid colon`, `pancreas`, `muscle organ`, `artery`, `temporal lobe`
  - `placenta`, `cerebellum`, `thyroid gland`, `lung`, `skin of body`, `spleen`, `liver`, `gallbladder`
  - `kidney`, `duodenum`, `jejunum`, `ileum`, `rib`, `spinal cord`, `prostate gland`, `adrenal gland`
  - `thymus`, `bone marrow`, `trachea`, `omentum`, `fallopian tube`, `vault of skull`, `chorionic villus`, `umbilical cord blood`
  - `bladder organ`
- Unique development stages: 36 values from `development_stage`
  - `embryonic stage`, `10th week post-fertilization stage`, `11th week post-fertilization stage`, `12th week post-fertilization stage`, `13th week post-fertilization stage`, `14th week post-fertilization stage`, `26th week post-fertilization stage`, `21-year-old stage`
  - `23-year-old stage`, `25-year-old stage`, `27-year-old stage`, `30-year-old stage`, `32-year-old stage`, `34-year-old stage`, `36-year-old stage`, `41-year-old stage`
  - `43-year-old stage`, `45-year-old stage`, `46-year-old stage`, `47-year-old stage`, `49-year-old stage`, `51-year-old stage`, `52-year-old stage`, `55-year-old stage`
  - `56-year-old stage`, `57-year-old stage`, `58-year-old stage`, `59-year-old stage`, `60-year-old stage`, `61-year-old stage`, `62-year-old stage`, `63-year-old stage`
  - `64-year-old stage`, `66-year-old stage`, `83-year-old stage`, `newborn stage (0-28 days)`
- Unique diseases: 1 values from `disease`
  - `normal`

## 2. Survey of human embryonic development

- Source group: `CellxGene`
- File: `source_1_cellxgene/03_survey_of_human_embryonic_development.h5ad`
- Size: 18.7GiB
- Data kind: AnnData H5AD
- Dimension: 4,062,980 observations x 45,676 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 4,062,980 observations x 45,676 variables |
| file size | 18.7GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 4,062,980 (observation/cell axis count)
- Unique cell types: 72 values from `cell_type`
  - `hematopoietic stem cell`, `ciliated epithelial cell`, `blood vessel endothelial cell`, `squamous epithelial cell`, `mesothelial cell`, `bipolar neuron`, `granule cell`, `Purkinje cell`
  - `stellate neuron`, `neuron associated cell (sensu Vertebrata)`, `glial cell`, `macroglial cell`, `astrocyte`, `oligodendrocyte`, `microglial cell`, `professional antigen presenting cell`
  - `goblet cell`, `endocrine cell`, `neuroendocrine cell`, `chromaffin cell`, `cell of skeletal muscle`, `smooth muscle cell`, `taste receptor cell`, `photoreceptor cell`
  - `ganglion interneuron`, `inhibitory interneuron`, `stromal cell`, `syncytiotrophoblast cell`, `neuron`, `megakaryocyte`, `amacrine cell`, `corneal epithelial cell`
  - `skeletal muscle satellite cell`, `GABAergic neuron`, `acinar cell`, `hepatic stellate cell`, `Mueller cell`, `mesangial cell`, `glutamatergic neuron`, `retinal ganglion cell`
  - `retina horizontal cell`, `cardiac muscle cell`, `myeloid cell`, `erythroblast`, `thymocyte`, `hematopoietic cell`, `innate lymphoid cell`, `pancreatic ductal cell`
  - `cortical cell of adrenal gland`, `regular atrial cardiac myocyte`, `endothelial cell of lymphatic vessel`, `endothelial cell of vascular tree`, `tuft cell`, `epithelial cell of thymus`, `endocardial cell`, `trophoblast giant cell`
  - `intestinal epithelial cell`, `Schwann cell`, `retinal pigment epithelial cell`, `epithelial cell of lower respiratory tract`, `visceromotor neuron`, `hepatoblast`, `enteric neuron`, `extravillous trophoblast`
  - `lens fiber cell`, `chorionic trophoblast cell`, `sympathetic neuron`, `epicardial adipocyte`, `dermis microvascular lymphatic vessel endothelial cell`, `ventricular cardiac muscle cell`, `unipolar brush cell`, `unknown`
- Unique tissues: 15 values from `tissue`
  - `intestine`, `stomach`, `heart`, `eye`, `pancreas`, `muscle organ`, `telencephalon`, `placenta`
  - `cerebellum`, `lung`, `spleen`, `liver`, `kidney`, `adrenal gland`, `thymus`
- Unique development stages: 8 values from `development_stage`
  - `10th week post-fertilization stage`, `12th week post-fertilization stage`, `13th week post-fertilization stage`, `14th week post-fertilization stage`, `15th week post-fertilization stage`, `16th week post-fertilization stage`, `17th week post-fertilization stage`, `18th week post-fertilization stage`
- Unique diseases: 2 values from `disease`
  - `trisomy 18`, `normal`

## 3. Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor

- Source group: `CellxGene`
- File: `source_1_cellxgene/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad`
- Size: 816.5MiB
- Data kind: AnnData H5AD
- Dimension: 51,176 observations x 35,477 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 51,176 observations x 35,477 variables |
| file size | 816.5MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 51,176 (observation/cell axis count)
- Unique cell types: 8 values from `cell_type`
  - `fibroblast`, `endothelial cell`, `smooth muscle cell`, `erythrocyte`, `neuron`, `leukocyte`, `cardiac muscle cell`, `mesothelial cell of epicardium`
- Unique tissues: 1 values from `tissue`
  - `apical region of left ventricle`
- Unique development stages: 8 values from `development_stage`
  - `19th week post-fertilization stage`, `20th week post-fertilization stage`, `4-year-old stage`, `10-year-old stage`, `14-year-old stage`, `35-year-old stage`, `41-year-old stage`, `42-year-old stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 4. Integrated adult and foetal hearts

- Source group: `CellxGene`
- File: `source_1_cellxgene/05_integrated_adult_and_foetal_hearts.h5ad`
- Size: 409.1MiB
- Data kind: AnnData H5AD
- Dimension: 60,668 observations x 26,886 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 60,668 observations x 26,886 variables |
| file size | 409.1MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 60,668 (observation/cell axis count)
- Unique cell types: 17 values from `cell_type`
  - `fibroblast`, `endothelial cell`, `adipocyte`, `smooth muscle cell`, `neuron`, `cardiac mesenchymal cell`, `pericyte`, `cardiac muscle cell`
  - `myeloid cell`, `innate lymphoid cell`, `capillary endothelial cell`, `endocardial cell`, `fetal cardiomyocyte`, `vein endothelial cell`, `mesothelial cell of epicardium`, `endothelial cell of artery`
  - `unknown`
- Unique tissues: 7 values from `tissue`
  - `right cardiac atrium`, `left cardiac atrium`, `heart right ventricle`, `heart left ventricle`, `interventricular septum`, `apex of heart`, `basal zone of heart`
- Unique development stages: 5 values from `development_stage`
  - `embryonic stage`, `10th week post-fertilization stage`, `sixth decade stage`, `seventh decade stage`, `eighth decade stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 5. Rotem_12W_heart_C1

- Source group: `CellxGene`
- File: `source_1_cellxgene/06_rotem_12w_heart_c1.h5ad`
- Size: 34.0MiB
- Data kind: AnnData H5AD
- Dimension: 4,992 observations x 35,476 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 4,992 observations x 35,476 variables |
| file size | 34.0MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 4,992 (observation/cell axis count)
- Unique cell types: 5 values from `cell_type`
  - `endothelial cell`, `cardiac mesenchymal cell`, `cardiac muscle cell`, `neural cell`, `unknown`
- Unique tissues: 1 values from `tissue`
  - `outflow tract myocardium`
- Unique development stages: 1 values from `development_stage`
  - `13th week post-fertilization stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 6. Rotem_12W_heart_B1

- Source group: `CellxGene`
- File: `source_1_cellxgene/07_rotem_12w_heart_b1.h5ad`
- Size: 36.7MiB
- Data kind: AnnData H5AD
- Dimension: 4,992 observations x 35,476 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 4,992 observations x 35,476 variables |
| file size | 36.7MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 4,992 (observation/cell axis count)
- Unique cell types: 6 values from `cell_type`
  - `endothelial cell`, `cardiac mesenchymal cell`, `cardiac muscle cell`, `hematopoietic cell`, `neural cell`, `unknown`
- Unique tissues: 1 values from `tissue`
  - `outflow tract myocardium`
- Unique development stages: 1 values from `development_stage`
  - `13th week post-fertilization stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 7. Rotem_12W_heart_D1

- Source group: `CellxGene`
- File: `source_1_cellxgene/08_rotem_12w_heart_d1.h5ad`
- Size: 24.2MiB
- Data kind: AnnData H5AD
- Dimension: 4,992 observations x 35,476 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 4,992 observations x 35,476 variables |
| file size | 24.2MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 4,992 (observation/cell axis count)
- Unique cell types: 6 values from `cell_type`
  - `endothelial cell`, `cardiac mesenchymal cell`, `cardiac muscle cell`, `hematopoietic cell`, `neural cell`, `unknown`
- Unique tissues: 1 values from `tissue`
  - `outflow tract myocardium`
- Unique development stages: 1 values from `development_stage`
  - `13th week post-fertilization stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 8. Rotem_12W_heart_A1

- Source group: `CellxGene`
- File: `source_1_cellxgene/09_rotem_12w_heart_a1.h5ad`
- Size: 42.8MiB
- Data kind: AnnData H5AD
- Dimension: 4,992 observations x 35,476 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 4,992 observations x 35,476 variables |
| file size | 42.8MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 4,992 (observation/cell axis count)
- Unique cell types: 5 values from `cell_type`
  - `endothelial cell`, `cardiac mesenchymal cell`, `cardiac muscle cell`, `neural cell`, `unknown`
- Unique tissues: 1 values from `tissue`
  - `outflow tract myocardium`
- Unique development stages: 1 values from `development_stage`
  - `13th week post-fertilization stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 9. Single-nuclei RNA-seq of human outflow tract and aortic valve tissue

- Source group: `CellxGene`
- File: `source_1_cellxgene/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad`
- Size: 437.1MiB
- Data kind: AnnData H5AD
- Dimension: 30,125 observations x 31,008 variables

### Summary

| field | value |
| --- | --- |
| storage type | AnnData H5AD |
| matrix/data shape | 30,125 observations x 31,008 variables |
| file size | 437.1MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 30,125 (observation/cell axis count)
- Unique cell types: 6 values from `cell_type`
  - `endothelial cell`, `cardiac mesenchymal cell`, `cardiac muscle cell`, `hematopoietic cell`, `neural cell`, `valve interstitial cell`
- Unique tissues: 2 values from `tissue`
  - `outflow tract`, `outflow tract myocardium`
- Unique development stages: 3 values from `development_stage`
  - `Carnegie stage 17`, `13th week post-fertilization stage`, `adult stage`
- Unique diseases: 1 values from `disease`
  - `normal`

## 10. GSE157329 raw counts

- Source group: `Human Early Embryogenesis Atlas`
- File: `source_2_human_early_embryogenesis_atlas/93a9e248-b704-419f-b5ab-a0b96eefeaa0/GSE157329_raw_counts.mtx.gz`
- Size: 1.3GiB
- Data kind: Matrix Market sparse coordinate matrix
- Dimension: 32,351 rows x 185,140 columns

### Summary

| field | value |
| --- | --- |
| storage type | Matrix Market sparse coordinate matrix |
| matrix/data shape | 32,351 rows x 185,140 columns |
| file size | 1.3GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 185,140 (matrix column count; metadata fields are not embedded in this Matrix Market file)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 11. Human cardiogenesis in vitro expression matrix

- Source group: `UCSC Cells`
- File: `source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz`
- Size: 1.7GiB
- Data kind: Gzipped tab-separated expression matrix
- Dimension: 24,919 rows x 78,609 columns

### Summary

| field | value |
| --- | --- |
| storage type | Gzipped tab-separated expression matrix |
| matrix/data shape | 24,919 rows x 78,609 columns |
| file size | 1.7GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 78,608 (cell/barcode columns in the expression matrix header)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 12. Human cardiogenesis in vivo expression matrix

- Source group: `UCSC Cells`
- File: `source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz`
- Size: 340.3MiB
- Data kind: Gzipped tab-separated expression matrix
- Dimension: 24,919 rows x 30,427 columns

### Summary

| field | value |
| --- | --- |
| storage type | Gzipped tab-separated expression matrix |
| matrix/data shape | 24,919 rows x 30,427 columns |
| file size | 340.3MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 30,426 (cell/barcode columns in the expression matrix header)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 13. Multiomic human heart snRNA-seq matrix

- Source group: `UCSC Cells`
- File: `source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.mtx.gz`
- Size: 20.5GiB
- Data kind: Matrix Market sparse coordinate matrix
- Dimension: 16,115 rows x 2,275,105 columns

### Summary

| field | value |
| --- | --- |
| storage type | Matrix Market sparse coordinate matrix |
| matrix/data shape | 16,115 rows x 2,275,105 columns |
| file size | 20.5GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 2,275,105 (matrix column count; metadata fields are not embedded in this Matrix Market file)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 14. Multiomic human heart snATAC-seq matrix

- Source group: `UCSC Cells`
- File: `source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.mtx.gz`
- Size: 24.7GiB
- Data kind: Matrix Market sparse coordinate matrix
- Dimension: 654,221 rows x 690,044 columns

### Summary

| field | value |
| --- | --- |
| storage type | Matrix Market sparse coordinate matrix |
| matrix/data shape | 654,221 rows x 690,044 columns |
| file size | 24.7GiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 690,044 (matrix column count; metadata fields are not embedded in this Matrix Market file)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 15. Heart of Cells overall heart scRNA-seq expression matrix

- Source group: `UCSC Cells`
- File: `source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.tsv.gz`
- Size: 360.6MiB
- Data kind: Gzipped tab-separated expression matrix
- Dimension: 33,538 rows x 142,947 columns

### Summary

| field | value |
| --- | --- |
| storage type | Gzipped tab-separated expression matrix |
| matrix/data shape | 33,538 rows x 142,947 columns |
| file size | 360.6MiB |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 142,946 (cell/barcode columns in the expression matrix header)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 16. Human fetal cis-regulatory elements

- Source group: `Lab Directory`
- File: `source_4_lab_directory/01_human_fetal_cis_regulatory_elements.loom`
- Size: 1.2GiB
- Data kind: Loom HDF5 matrix
- Dimension: 19,329 genes/features x 185,061 cells

### Summary

| field | value |
| --- | --- |
| storage type | Loom HDF5 matrix |
| matrix/data shape | 19,329 genes/features x 185,061 cells |
| file size | 1.2GiB |
| row attributes | 6 |
| column attributes | 11 |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 185,061 (cell axis count)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 17. Human fetal striatum atlas

- Source group: `Lab Directory`
- File: `source_4_lab_directory/02_human_fetal_striatum_atlas.loom`
- Size: 1.4GiB
- Data kind: Loom HDF5 matrix
- Dimension: 38,263 genes/features x 150,129 cells

### Summary

| field | value |
| --- | --- |
| storage type | Loom HDF5 matrix |
| matrix/data shape | 38,263 genes/features x 150,129 cells |
| file size | 1.4GiB |
| row attributes | 5 |
| column attributes | 11 |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 150,129 (cell axis count)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 18. Human megakaryocyte development: yolk-sac stage

- Source group: `Lab Directory`
- File: `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.loom`
- Size: 90.9MiB
- Data kind: Loom HDF5 matrix
- Dimension: 17,614 genes/features x 11,021 cells

### Summary

| field | value |
| --- | --- |
| storage type | Loom HDF5 matrix |
| matrix/data shape | 17,614 genes/features x 11,021 cells |
| file size | 90.9MiB |
| row attributes | 6 |
| column attributes | 11 |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 11,021 (cell axis count)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 19. Human megakaryocyte development: hESC Day 0

- Source group: `Lab Directory`
- File: `source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.loom`
- Size: 76.2MiB
- Data kind: Loom HDF5 matrix
- Dimension: 17,091 genes/features x 9,485 cells

### Summary

| field | value |
| --- | --- |
| storage type | Loom HDF5 matrix |
| matrix/data shape | 17,091 genes/features x 9,485 cells |
| file size | 76.2MiB |
| row attributes | 6 |
| column attributes | 11 |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 9,485 (cell axis count)
- Unique cell types: not embedded in this file
- Unique tissues: not embedded in this file
- Unique development stages: not embedded in this file
- Unique diseases: not embedded in this file

## 20. Spatial dynamics of the developing human heart

- Source group: `Lazar et al. 2025`
- File: `lazar_et_al_2025/` (22 CellRanger h5 files, Visium RDS, ISS spatial data; distributed as two zip archives)
- Size: 16.8GiB total (two zip archives: ~6.1GiB + ~10.7GiB)
- Data kind: CellRanger H5 (scRNA-seq) + Visium spatial transcriptomics (Seurat/Semla RDS) + ISS spatial transcriptomics
- Dimension: 76,991 cells x 59,480 features (high-level clustering; raw per-sample h5 files)

### Summary

| field | value |
| --- | --- |
| storage type | CellRanger H5 (scRNA-seq) + Seurat/Semla RDS (Visium spatial) + ISS read coordinates (CSV) |
| matrix/data shape | 76,991 cells x 59,480 features (high-level clustering); 68,378 cells (detailed-level clustering) |
| file size | 16.8GiB (two zip archives) |
| samples | 22 CellRanger h5 files from 15 donors; 28 library preparations |
| clustering levels | High-level (HL): 34 cell types; Detailed-level (DL): 74 subtypes |
| reference genome | GRCh38 |

### Cell/tissue/stage/disease metadata

- Unique cells recorded: 76,991 (high-level clustering); 68,378 (detailed-level, excluding low-quality clusters)
- Unique cell types (HL, 34 types):
  - Cardiomyocytes: `Mat_vCM`, `Mat_aCM`, `MetAct_vCM_1`, `MetAct_vCM_2`, `MetAct_aCM`, `Immat_CM`, `Prol_CM`, `TMSB10high_C_1`, `TMSB10high_C_2`
  - Fibroblasts/mesenchymal: `Int_FB`, `OFT_FB`, `AnnFibr_FB`, `PDE4Chigh_FB`, `Prol_FB`, `Valve_MC`, `Peric_MC`, `EPDC`, `OFT_SMC`, `CA_SMC`
  - Endothelial: `Endoc_EC`, `MicroVasc_EC`, `MacroVasc_EC`, `EndocCush_EC`, `PDE4Chigh_EC`, `LEC`
  - Other: `PC` (pericytes), `MyC` (myeloid), `EpC` (epicardial), `LyC` (lymphoid), `NB-N`, `SCP-GC`
  - Excluded (low quality): `HL_excl_1`, `HL_excl_2`, `HL_excl_3`, `HL_excl_4`
- Unique cell types (DL, 74 subtypes) including conduction system: `SAN_CM`, `AVN_CM`, `AVB-BB_CM`, `PF_CM`, `TsPF_CM`
- Unique tissues: `Heart`
- Unique development stages: 12 stages (5.5–14.0 pcw)
  - `5.5 pcw`, `6.0 pcw`, `7.0 pcw`, `8.0 pcw`, `8.5 pcw`, `8.75 pcw`, `9.0 pcw`, `10.0 pcw`, `11.5 pcw`, `12.0 pcw`, `13.25 pcw`, `14.0 pcw`
- Unique donors: 15
- Unique diseases: normal (all donors)
- Assay: 10x Chromium v2/v3 scRNA-seq + Visium spatial transcriptomics + ISS (149-gene panel)

### Top 5 rows / preview (from TenX303_2.h5, donor XDD:400, 5.5 pcw)

| field | value |
| --- | --- |
| cells in sample | 2,554 |
| median genes/cell | 4,537 |
| median UMIs/cell | 17,472 |
| median mito fraction | 3.3% |
| total features measured | 59,480 (GRCh38; includes marker controls) |

