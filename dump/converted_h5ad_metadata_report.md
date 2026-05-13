# Converted H5AD Metadata Report

Generated: 2026-04-15T23:33:18

This report covers the 11 unique converted `.h5ad` outputs from source 2, source 3, and source 4. For each file it lists cell/feature counts, metadata column names, and any explicit cell type or development stage annotations found in `obs`.

## Overview

| dataset id | dataset | cells | features | obs cols | var cols | cell type cols | development stage cols |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source4_megakaryocyte_hesc_day0 | GSE144024 hESC Day0 gene | 9,485 | 17,091 | 10 | 5 | none | none |
| source2_hca_raw_counts | GSE157329 raw counts | 185,140 | 32,351 | 0 | 0 | none | none |
| source3_ucsc_in_vitro_expr | human cardiogenesis in vitro exprMatrix | 78,608 | 24,919 | 0 | 0 | none | none |
| source3_ucsc_in_vivo_expr | human cardiogenesis in vivo exprMatrix | 30,426 | 24,919 | 0 | 0 | none | none |
| source3_ucsc_multiomic_snrna | multiomic human heart snrna seq matrix | 2,275,105 | 16,115 | 0 | 0 | none | none |
| source3_ucsc_multiomic_snatac | multiomic human heart snatac seq matrix | 690,044 | 654,221 | 0 | 0 | none | none |
| source3_ucsc_heart_of_cells_expr | heart of cells overall heart scrna seq exprMatrix | 142,946 | 33,538 | 0 | 0 | none | none |
| source4_fetal_cre | human fetal cis regulatory elements | 185,061 | 19,329 | 10 | 5 | none | none |
| source4_fetal_striatum | human fetal striatum atlas | 150,129 | 38,263 | 10 | 4 | none | none |
| source4_megakaryocyte_ys | GSE144024 YS Stage gene | 11,021 | 17,614 | 10 | 5 | none | none |
| source4_epicardium | fetal vs adult human epicardium | 30,889 | 60,664 | 18 | 4 | cell_subclass, cell_type | development_stage |

## 1. GSE144024 hESC Day0 gene

- Dataset ID: `source4_megakaryocyte_hesc_day0`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.h5ad`
- Conversion status: `skipped_existing`
- Cells: 9,485
- Genes / features: 17,091
- Output size: 67,174,499 bytes
- Conversion time: 0.0 seconds

### Columns

- `obs` column count: 10
- `obs` column names: `dataset`, `filter_pass`, `n_counts`, `n_func_genes`, `organ_specific`, `pct_mito`, `platform`, `sample`, `study`, `unique_cell_id`
- `var` column count: 5
- `var` column names: `ensembl_id`, `ensembl_id_version`, `ensembl_original`, `gene_original`, `gene_type`

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 2. GSE157329 raw counts

- Dataset ID: `source2_hca_raw_counts`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_2_human_early_embryogenesis_atlas/GSE157329_raw_counts.h5ad`
- Conversion status: `written`
- Cells: 185,140
- Genes / features: 32,351
- Output size: 1,000,202,143 bytes
- Conversion time: 459.9 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 3. human cardiogenesis in vitro exprMatrix

- Dataset ID: `source3_ucsc_in_vitro_expr`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.h5ad`
- Conversion status: `written`
- Cells: 78,608
- Genes / features: 24,919
- Output size: 2,487,904,467 bytes
- Conversion time: 544.6 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 4. human cardiogenesis in vivo exprMatrix

- Dataset ID: `source3_ucsc_in_vivo_expr`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.h5ad`
- Conversion status: `written`
- Cells: 30,426
- Genes / features: 24,919
- Output size: 434,605,538 bytes
- Conversion time: 129.1 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 5. multiomic human heart snrna seq matrix

- Dataset ID: `source3_ucsc_multiomic_snrna`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.h5ad`
- Conversion status: `written`
- Cells: 2,275,105
- Genes / features: 16,115
- Output size: 13,873,871,589 bytes
- Conversion time: 3821.1 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 6. multiomic human heart snatac seq matrix

- Dataset ID: `source3_ucsc_multiomic_snatac`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.h5ad`
- Conversion status: `written`
- Cells: 690,044
- Genes / features: 654,221
- Output size: 19,783,370,883 bytes
- Conversion time: 4066.8 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 7. heart of cells overall heart scrna seq exprMatrix

- Dataset ID: `source3_ucsc_heart_of_cells_expr`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.h5ad`
- Conversion status: `written`
- Cells: 142,946
- Genes / features: 33,538
- Output size: 768,328,696 bytes
- Conversion time: 539.1 seconds

### Columns

- `obs` column count: 0
- `obs` column names: none
- `var` column count: 0
- `var` column names: none

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 8. human fetal cis regulatory elements

- Dataset ID: `source4_fetal_cre`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_4_lab_directory/01_human_fetal_cis_regulatory_elements.h5ad`
- Conversion status: `written`
- Cells: 185,061
- Genes / features: 19,329
- Output size: 922,987,040 bytes
- Conversion time: 237.4 seconds

### Columns

- `obs` column count: 10
- `obs` column names: `dataset`, `filter_pass`, `n_counts`, `n_func_genes`, `organ_specific`, `pct_mito`, `platform`, `sample`, `study`, `unique_cell_id`
- `var` column count: 5
- `var` column names: `ensembl_id`, `ensembl_id_version`, `ensembl_original`, `gene_original`, `gene_type`

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 9. human fetal striatum atlas

- Dataset ID: `source4_fetal_striatum`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_4_lab_directory/02_human_fetal_striatum_atlas.h5ad`
- Conversion status: `written`
- Cells: 150,129
- Genes / features: 38,263
- Output size: 628,170,326 bytes
- Conversion time: 247.6 seconds

### Columns

- `obs` column count: 10
- `obs` column names: `dataset`, `filter_pass`, `n_counts`, `n_func_genes`, `organ_specific`, `pct_mito`, `platform`, `sample`, `study`, `unique_cell_id`
- `var` column count: 4
- `var` column names: `ensembl_id`, `ensembl_id_version`, `ensembl_original`, `gene_type`

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 10. GSE144024 YS Stage gene

- Dataset ID: `source4_megakaryocyte_ys`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.h5ad`
- Conversion status: `written`
- Cells: 11,021
- Genes / features: 17,614
- Output size: 80,153,601 bytes
- Conversion time: 12.1 seconds

### Columns

- `obs` column count: 10
- `obs` column names: `dataset`, `filter_pass`, `n_counts`, `n_func_genes`, `organ_specific`, `pct_mito`, `platform`, `sample`, `study`, `unique_cell_id`
- `var` column count: 5
- `var` column names: `ensembl_id`, `ensembl_id_version`, `ensembl_original`, `gene_original`, `gene_type`

### Cell Type Metadata

No explicit cell type metadata column found in `obs`.

### Development Stage Metadata

No explicit development stage metadata column found in `obs`.

## 11. fetal vs adult human epicardium

- Dataset ID: `source4_epicardium`
- Output file: `/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted/source_4_lab_directory/04_fetal_vs_adult_human_epicardium.h5ad`
- Conversion status: `written`
- Cells: 30,889
- Genes / features: 60,664
- Output size: 144,516,959 bytes
- Conversion time: 42.2 seconds

### Columns

- `obs` column count: 18
- `obs` column names: `cell_subclass`, `cell_type`, `dataset`, `development_stage`, `disease`, `donor_id`, `filter_pass`, `n_counts`, `n_func_genes`, `organ_specific`, `pct_mito`, `platform`, `sample`, `self_reported_ethnicity`, `sex`, `study`, `tissue`, `tissue_general`
- `var` column count: 4
- `var` column names: `ensembl_id`, `ensembl_id_version`, `ensembl_original`, `gene_type`

### Cell Type Metadata

#### `cell_subclass`

| cell_subclass | cells |
| --- | --- |
| cardiocyte | 6,433 |
| native cell | 4,964 |
| fibroblast | 4,207 |
| endothelial cell | 3,822 |
| myeloid cell | 3,323 |
| muscle cell | 3,020 |
| neuron | 2,014 |
| lymphocyte | 1,656 |
| pericyte | 1,134 |
| progenitor cell | 315 |
| fat cell | 1 |

#### `cell_type`

| cell_type | cells |
| --- | --- |
| native cell | 4,964 |
| fibroblast | 4,207 |
| myeloid cell | 3,323 |
| smooth muscle cell | 3,020 |
| cardiac muscle cell | 2,566 |
| neuron | 2,014 |
| endocardial cell | 1,667 |
| innate lymphoid cell | 1,656 |
| capillary endothelial cell | 1,567 |
| fetal cardiomyocyte | 1,310 |
| pericyte | 1,134 |
| endothelial cell | 1,104 |
| endothelial cell of artery | 903 |
| mesothelial cell of epicardium | 890 |
| cardiac mesenchymal cell | 315 |
| vein endothelial cell | 248 |
| fat cell | 1 |

### Development Stage Metadata

#### `development_stage`

| development_stage | cells |
| --- | --- |
| 10th week post-fertilization human stage | 15,235 |
| 12th week post-fertilization human stage | 8,332 |
| 9th week post-fertilization human stage | 7,322 |

