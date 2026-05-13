# CellxGene Heart Development Subset Report

## Overall Summary

- Original input observations across the 9 reported CellxGene files: 4,824,843 cells
- Kept observations across the subset files: 211,692 cells (4.4% of original)
- Removed observations: 4,613,151 cells
- Genes/features were preserved per dataset; the subset changes cells/observations, not the gene axis.

| dataset | original cells | original genes | kept cells | kept % | kept genes |
| --- | --- | --- | --- | --- | --- |
| 01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad | 599,926 | 26,069 | 7,997 | 1.3% | 26,069 |
| 03_survey_of_human_embryonic_development.h5ad | 4,062,980 | 45,676 | 101,749 | 2.5% | 45,676 |
| 04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad | 51,176 | 35,477 | 26,394 | 51.6% | 35,477 |
| 05_integrated_adult_and_foetal_hearts.h5ad | 60,668 | 26,886 | 30,889 | 50.9% | 26,886 |
| 06_rotem_12w_heart_c1.h5ad | 4,992 | 35,476 | 4,992 | 100.0% | 35,476 |
| 07_rotem_12w_heart_b1.h5ad | 4,992 | 35,476 | 4,992 | 100.0% | 35,476 |
| 08_rotem_12w_heart_d1.h5ad | 4,992 | 35,476 | 4,992 | 100.0% | 35,476 |
| 09_rotem_12w_heart_a1.h5ad | 4,992 | 35,476 | 4,992 | 100.0% | 35,476 |
| 10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad | 30,125 | 31,008 | 24,695 | 82.0% | 31,008 |

## Overall Subset Composition

### Cell Type Counts Across Reported Subsets

| cell type | cells across reported subsets | reported subset % |
| --- | --- | --- |
| cardiac muscle cell | 105,295 | 49.7% |
| stromal cell | 15,955 | 7.5% |
| unknown | 15,125 | 7.1% |
| cardiac mesenchymal cell | 12,228 | 5.8% |
| endocardial cell | 9,065 | 4.3% |
| endothelial cell | 9,030 | 4.3% |
| fibroblast | 7,183 | 3.4% |
| smooth muscle cell | 5,369 | 2.5% |
| endothelial cell of vascular tree | 4,911 | 2.3% |
| myeloid cell | 4,363 | 2.1% |
| ventricular cardiac muscle cell | 3,160 | 1.5% |
| innate lymphoid cell | 3,004 | 1.4% |
| neuron | 2,394 | 1.1% |
| mesothelial cell of epicardium | 2,276 | 1.1% |
| epicardial adipocyte | 1,891 | 0.9% |
| capillary endothelial cell | 1,567 | 0.7% |
| fetal cardiomyocyte | 1,310 | 0.6% |
| pericyte | 1,134 | 0.5% |
| neural cell | 1,000 | 0.5% |
| endothelial cell of artery | 903 | 0.4% |
| leukocyte | 709 | 0.3% |
| endothelial cell of lymphatic vessel | 648 | 0.3% |
| dermis microvascular lymphatic vessel endothelial cell | 603 | 0.3% |
| Schwann cell | 535 | 0.3% |
| megakaryocyte | 361 | 0.2% |
| visceromotor neuron | 348 | 0.2% |
| hematopoietic cell | 328 | 0.2% |
| mesenchymal stem cell | 261 | 0.1% |
| vein endothelial cell | 248 | 0.1% |
| macrophage | 112 | 0.1% |
| regular atrial cardiac myocyte | 102 | 0.0% |
| erythrocyte | 99 | 0.0% |
| erythroid lineage cell | 80 | 0.0% |
| epithelial cell | 16 | 0.0% |
| cell of skeletal muscle | 15 | 0.0% |
| T cell | 11 | 0.0% |
| professional antigen presenting cell | 10 | 0.0% |
| dendritic cell | 9 | 0.0% |
| erythroid progenitor cell | 9 | 0.0% |
| cord blood hematopoietic stem cell | 6 | 0.0% |
| erythroblast | 6 | 0.0% |
| neutrophil | 5 | 0.0% |
| primordial germ cell | 3 | 0.0% |
| valve interstitial cell | 3 | 0.0% |
| adipocyte | 1 | 0.0% |
| monocyte | 1 | 0.0% |

### Development Stage Counts Across Reported Subsets

| development stage | cells across reported subsets | reported subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 42,762 | 20.2% |
| 15th week post-fertilization stage | 42,276 | 20.0% |
| 17th week post-fertilization stage | 28,644 | 13.5% |
| embryonic stage | 22,557 | 10.7% |
| 19th week post-fertilization stage | 18,747 | 8.9% |
| 12th week post-fertilization stage | 17,557 | 8.3% |
| 16th week post-fertilization stage | 13,213 | 6.2% |
| 10th week post-fertilization stage | 8,332 | 3.9% |
| 20th week post-fertilization stage | 7,647 | 3.6% |
| Carnegie stage 17 | 7,279 | 3.4% |
| 11th week post-fertilization stage | 2,678 | 1.3% |

## Dataset Details

## 1. 01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad

- Original file: `source_1_cellxgene/01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/01_construction_of_a_human_cell_landscape_at_single_cell_level_heart_development_subset.h5ad`
- Original size: 599,926 cells x 26,069 genes
- Kept subset: 7,997 cells x 26,069 genes (1.3% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| stromal cell | 3,207 | 40.1% |
| ventricular cardiac muscle cell | 2,996 | 37.5% |
| endothelial cell | 1,115 | 13.9% |
| mesenchymal stem cell | 261 | 3.3% |
| macrophage | 112 | 1.4% |
| smooth muscle cell | 105 | 1.3% |
| erythroid lineage cell | 80 | 1.0% |
| neuron | 32 | 0.4% |
| epithelial cell | 16 | 0.2% |
| cell of skeletal muscle | 15 | 0.2% |
| T cell | 11 | 0.1% |
| professional antigen presenting cell | 10 | 0.1% |
| dendritic cell | 9 | 0.1% |
| erythroid progenitor cell | 9 | 0.1% |
| cord blood hematopoietic stem cell | 6 | 0.1% |
| neutrophil | 5 | 0.1% |
| fibroblast | 4 | 0.1% |
| primordial germ cell | 3 | 0.0% |
| monocyte | 1 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 12th week post-fertilization stage | 5,319 | 66.5% |
| 11th week post-fertilization stage | 2,678 | 33.5% |

## 2. 03_survey_of_human_embryonic_development.h5ad

- Original file: `source_1_cellxgene/03_survey_of_human_embryonic_development.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/03_survey_of_human_embryonic_development_heart_development_subset.h5ad`
- Original size: 4,062,980 cells x 45,676 genes
- Kept subset: 101,749 cells x 45,676 genes (2.5% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| cardiac muscle cell | 67,610 | 66.4% |
| stromal cell | 12,748 | 12.5% |
| endocardial cell | 7,398 | 7.3% |
| endothelial cell of vascular tree | 4,911 | 4.8% |
| smooth muscle cell | 2,036 | 2.0% |
| epicardial adipocyte | 1,891 | 1.9% |
| innate lymphoid cell | 1,348 | 1.3% |
| myeloid cell | 1,040 | 1.0% |
| endothelial cell of lymphatic vessel | 648 | 0.6% |
| dermis microvascular lymphatic vessel endothelial cell | 603 | 0.6% |
| Schwann cell | 535 | 0.5% |
| megakaryocyte | 361 | 0.4% |
| visceromotor neuron | 348 | 0.3% |
| ventricular cardiac muscle cell | 164 | 0.2% |
| regular atrial cardiac myocyte | 102 | 0.1% |
| erythroblast | 6 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 15th week post-fertilization stage | 42,276 | 41.5% |
| 17th week post-fertilization stage | 28,644 | 28.2% |
| 16th week post-fertilization stage | 13,213 | 13.0% |
| 12th week post-fertilization stage | 12,238 | 12.0% |
| 13th week post-fertilization stage | 5,378 | 5.3% |

## 3. 04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad

- Original file: `source_1_cellxgene/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor_heart_development_subset.h5ad`
- Original size: 51,176 cells x 35,477 genes
- Kept subset: 26,394 cells x 35,477 genes (51.6% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| cardiac muscle cell | 19,118 | 72.4% |
| fibroblast | 2,972 | 11.3% |
| endothelial cell | 1,554 | 5.9% |
| mesothelial cell of epicardium | 1,386 | 5.3% |
| leukocyte | 709 | 2.7% |
| neuron | 348 | 1.3% |
| smooth muscle cell | 208 | 0.8% |
| erythrocyte | 99 | 0.4% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 19th week post-fertilization stage | 18,747 | 71.0% |
| 20th week post-fertilization stage | 7,647 | 29.0% |

## 4. 05_integrated_adult_and_foetal_hearts.h5ad

- Original file: `source_1_cellxgene/05_integrated_adult_and_foetal_hearts.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/05_integrated_adult_and_foetal_hearts_heart_development_subset.h5ad`
- Original size: 60,668 cells x 26,886 genes
- Kept subset: 30,889 cells x 26,886 genes (50.9% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| unknown | 4,964 | 16.1% |
| fibroblast | 4,207 | 13.6% |
| myeloid cell | 3,323 | 10.8% |
| smooth muscle cell | 3,020 | 9.8% |
| cardiac muscle cell | 2,566 | 8.3% |
| neuron | 2,014 | 6.5% |
| endocardial cell | 1,667 | 5.4% |
| innate lymphoid cell | 1,656 | 5.4% |
| capillary endothelial cell | 1,567 | 5.1% |
| fetal cardiomyocyte | 1,310 | 4.2% |
| pericyte | 1,134 | 3.7% |
| endothelial cell | 1,104 | 3.6% |
| endothelial cell of artery | 903 | 2.9% |
| mesothelial cell of epicardium | 890 | 2.9% |
| cardiac mesenchymal cell | 315 | 1.0% |
| vein endothelial cell | 248 | 0.8% |
| adipocyte | 1 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| embryonic stage | 22,557 | 73.0% |
| 10th week post-fertilization stage | 8,332 | 27.0% |

## 5. 06_rotem_12w_heart_c1.h5ad

- Original file: `source_1_cellxgene/06_rotem_12w_heart_c1.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/06_rotem_12w_heart_c1_heart_development_subset.h5ad`
- Original size: 4,992 cells x 35,476 genes
- Kept subset: 4,992 cells x 35,476 genes (100.0% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| unknown | 2,677 | 53.6% |
| cardiac muscle cell | 1,579 | 31.6% |
| cardiac mesenchymal cell | 648 | 13.0% |
| neural cell | 54 | 1.1% |
| endothelial cell | 34 | 0.7% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 4,992 | 100.0% |

## 6. 07_rotem_12w_heart_b1.h5ad

- Original file: `source_1_cellxgene/07_rotem_12w_heart_b1.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/07_rotem_12w_heart_b1_heart_development_subset.h5ad`
- Original size: 4,992 cells x 35,476 genes
- Kept subset: 4,992 cells x 35,476 genes (100.0% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| unknown | 2,310 | 46.3% |
| cardiac muscle cell | 1,848 | 37.0% |
| cardiac mesenchymal cell | 633 | 12.7% |
| endothelial cell | 135 | 2.7% |
| neural cell | 65 | 1.3% |
| hematopoietic cell | 1 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 4,992 | 100.0% |

## 7. 08_rotem_12w_heart_d1.h5ad

- Original file: `source_1_cellxgene/08_rotem_12w_heart_d1.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/08_rotem_12w_heart_d1_heart_development_subset.h5ad`
- Original size: 4,992 cells x 35,476 genes
- Kept subset: 4,992 cells x 35,476 genes (100.0% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| unknown | 3,017 | 60.4% |
| cardiac muscle cell | 1,098 | 22.0% |
| cardiac mesenchymal cell | 679 | 13.6% |
| endothelial cell | 139 | 2.8% |
| neural cell | 58 | 1.2% |
| hematopoietic cell | 1 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 4,992 | 100.0% |

## 8. 09_rotem_12w_heart_a1.h5ad

- Original file: `source_1_cellxgene/09_rotem_12w_heart_a1.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/09_rotem_12w_heart_a1_heart_development_subset.h5ad`
- Original size: 4,992 cells x 35,476 genes
- Kept subset: 4,992 cells x 35,476 genes (100.0% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| cardiac muscle cell | 2,371 | 47.5% |
| unknown | 2,157 | 43.2% |
| cardiac mesenchymal cell | 382 | 7.7% |
| endothelial cell | 62 | 1.2% |
| neural cell | 20 | 0.4% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 4,992 | 100.0% |

## 9. 10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad

- Original file: `source_1_cellxgene/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad`
- Subset file: `source_1_cellxgene_heart_development_subset/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve_heart_development_subset.h5ad`
- Original size: 30,125 cells x 31,008 genes
- Kept subset: 24,695 cells x 31,008 genes (82.0% of original cells)

### Subset Cell Type Counts

| cell type | cells in subset | subset % |
| --- | --- | --- |
| cardiac mesenchymal cell | 9,571 | 38.8% |
| cardiac muscle cell | 9,105 | 36.9% |
| endothelial cell | 4,887 | 19.8% |
| neural cell | 803 | 3.3% |
| hematopoietic cell | 326 | 1.3% |
| valve interstitial cell | 3 | 0.0% |

### Subset Development Stage Counts

| development stage | cells in subset | subset % |
| --- | --- | --- |
| 13th week post-fertilization stage | 17,416 | 70.5% |
| Carnegie stage 17 | 7,279 | 29.5% |

## Additional External Dataset: Lazar et al. 2025

This dataset is not from CellxGene and was not processed through the CellxGene subsetting pipeline. It is included here as an additional heart development reference dataset.

- Publication: Lazar et al. (2025) — "Spatial dynamics of the developing human heart"
- Data repository: Mendeley Data
- Local path: `lazar_et_al_2025/` (two zip archives totaling ~16.8GiB)
- Technology: 10x Chromium scRNA-seq + Visium spatial transcriptomics + ISS (in-situ sequencing; 149-gene panel)
- Reference genome: GRCh38

### Dataset Summary

| field | value |
| --- | --- |
| total cells (SC libraries, extracted) | 107,673 |
| total features | 59,480 |
| scRNA-seq samples | 21 SC libraries (10x Chromium v2/v3) |
| unique donors | 15 |
| developmental stages | 11 (5.5–14.0 pcw) |
| cell types (HL annotation) | 23 assigned + unassigned |
| ISS gene panel | 149 genes |

### Cell Type Counts by Developmental Stage

Counts derived from `ClustersSecondary` (integrated HL cluster IDs) across all 21 10x Chromium SC libraries. Cell type labels from `HDCA_heart_SC_annotations_HL_240115.csv`. Cluster 18 combines two sub-annotations (Immat_CM / TMSB10high_C_1). Cluster 0 cells are unassigned in the integrated clustering.

23 of the 34 HL cell types are detected across these libraries. The 11 absent types — Macrovascular Endothelial Cell (MacroVasc_EC), PDE4C-high Endothelial Cell (PDE4Chigh_EC), Lymphatic Endothelial Cell (LEC), PDE4C-high Fibroblast (PDE4Chigh_FB), Proliferating Fibroblast (Prol_FB), Lymphoid Cell (LyC), Neuroblast-Neuron (NB-N), Schwann Cell / Glial Cell (SCP-GC), TMSB10-high Cell 2 (TMSB10high_C_2), Heart-Lung Atlas Excluded 3 (HL_excl_3), Heart-Lung Atlas Excluded 4 (HL_excl_4) — are rare populations not captured in these 21 libraries or absorbed into cluster 0.

#### Complete HL Cell Type Reference (all 34 types)

| HL Cluster | Cell Type (abbreviated) | Full Name | Detected |
| ---: | --- | --- | --- |
| 1 | OFT_FB | Outflow Tract Fibroblast | Yes |
| 2 | Int_FB | Interstitial Fibroblast | Yes |
| 3 | Endoc_EC | Endocardial Endothelial Cell | Yes |
| 4 | Mat_vCM | Mature Ventricular Cardiomyocyte | Yes |
| 5 | MetAct_vCM_2 | Metabolically Active Ventricular Cardiomyocyte 2 | Yes |
| 6 | HL_excl_1 | Heart-Lung Atlas Excluded 1 | Yes |
| 7 | Prol_CM | Proliferating Cardiomyocyte | Yes |
| 8 | OFT_SMC | Outflow Tract Smooth Muscle Cell | Yes |
| 9 | MetAct_vCM_1 | Metabolically Active Ventricular Cardiomyocyte 1 | Yes |
| 10 | CA_SMC | Coronary Artery Smooth Muscle Cell | Yes |
| 11 | MetAct_aCM | Metabolically Active Atrial Cardiomyocyte | Yes |
| 12 | MicroVasc_EC | Microvascular Endothelial Cell | Yes |
| 13 | Valve_MC | Valve Mesenchymal Cell | Yes |
| 14 | EPDC | Epicardium-Derived Cell | Yes |
| 15 | MyC | Myeloid Cell | Yes |
| 16 | AnnFibr_FB | Annulus Fibrosus Fibroblast | Yes |
| 17 | Mat_aCM | Mature Atrial Cardiomyocyte | Yes |
| 18 | Immat_CM / TMSB10high_C_1 | Immature Cardiomyocyte / TMSB10-high Cell 1 | Yes |
| 19 | HL_excl_2 | Heart-Lung Atlas Excluded 2 | Yes |
| 20 | EpC | Epicardial Cell | Yes |
| 21 | EndocCush_EC | Endocardial Cushion Endothelial Cell | Yes |
| 22 | PC | Pericyte | Yes |
| 23 | Peric_MC | Pericardial Mesenchymal Cell | Yes |
| 24 | PDE4Chigh_EC | PDE4C-high Endothelial Cell | No |
| 25 | NB-N | Neuroblast-Neuron | No |
| 26 | SCP-GC | Schwann Cell / Glial Cell | No |
| 27 | HL_excl_3 | Heart-Lung Atlas Excluded 3 | No |
| 28 | MacroVasc_EC | Macrovascular Endothelial Cell | No |
| 29 | LyC | Lymphoid Cell | No |
| 30 | PDE4Chigh_FB | PDE4C-high Fibroblast | No |
| 31 | Prol_FB | Proliferating Fibroblast | No |
| 32 | LEC | Lymphatic Endothelial Cell | No |
| 33 | TMSB10high_C_2 | TMSB10-high Cell 2 | No |
| 34 | HL_excl_4 | Heart-Lung Atlas Excluded 4 | No |

#### Detailed-Level (DL) Cell Type Reference (lineage sub-clusterings)

The DL level re-clusters each major lineage independently, resolving 23 HL types into finer sub-types. Per-stage counts at DL level have not been extracted. The four lineage sub-clusterings are listed below.

**Cardiomyocytes (CM) — 22 clusters**

| DL Cluster | Cell Type | Description |
| --- | --- | --- |
| CM_1 | vCM_5 | Ventricular cardiomyocyte subtype 5 |
| CM_2 | Immat_CM_3 | Immature cardiomyocyte subtype 3 |
| CM_3 | Immat_CM_1 | Immature cardiomyocyte subtype 1 |
| CM_4-1 | TsPF_CM | Transitional sinoatrial pacemaker / Purkinje fibre cardiomyocyte |
| CM_4-2 | PF_CM | Purkinje fibre cardiomyocyte |
| CM_5 | Prol_CM_2 | Proliferating cardiomyocyte subtype 2 |
| CM_6 | vCM_4 | Ventricular cardiomyocyte subtype 4 |
| CM_7 | Immat_CM_2 | Immature cardiomyocyte subtype 2 |
| CM_8-1 | vCM_2 | Ventricular cardiomyocyte subtype 2 |
| CM_8-2 | vCM_1 | Ventricular cardiomyocyte subtype 1 |
| CM_8-3 | vCM_3 | Ventricular cardiomyocyte subtype 3 |
| CM_9 | Left_aCM | Left atrial cardiomyocyte |
| CM_10 | vCM_6 | Ventricular cardiomyocyte subtype 6 |
| CM_11 | CM_excl_1 | Cardiomyocyte excluded cluster 1 |
| CM_12 | Cond_aCM | Conducting atrial cardiomyocyte (AVN/AVB) |
| CM_13 | CM_excl_2 | Cardiomyocyte excluded cluster 2 |
| CM_14 | Right_aCM | Right atrial cardiomyocyte |
| CM_15 | CM_excl_3 | Cardiomyocyte excluded cluster 3 |
| CM_16 | CM_excl_4 | Cardiomyocyte excluded cluster 4 |
| CM_17 | Prol_CM_1 | Proliferating cardiomyocyte subtype 1 |
| CM_18 | AVB-BB_CM | Atrioventricular bundle / bundle branch cardiomyocyte |
| CM_19-1 | AVN_CM | Atrioventricular node cardiomyocyte |
| CM_19-2 | SAN_CM | Sinoatrial node cardiomyocyte |
| CM_20 | CM_excl_5 | Cardiomyocyte excluded cluster 5 |
| CM_21 | CM_excl_6 | Cardiomyocyte excluded cluster 6 |
| CM_22 | CM_excl_7 | Cardiomyocyte excluded cluster 7 |

**Fibroblasts / Mesenchymal (FB) — 22 clusters**

| DL Cluster | Cell Type | Description |
| --- | --- | --- |
| FB_1 | Adv_FB_1 | Adventitial fibroblast subtype 1 |
| FB_2 | Prol_FB_2 | Proliferating fibroblast subtype 2 |
| FB_3 | EPDC_2 | Epicardium-derived cell subtype 2 |
| FB_4 | VIC | Valve interstitial cell |
| FB_5 | Int_FB_1 | Interstitial fibroblast subtype 1 |
| FB_6 | Adv_FB_2 | Adventitial fibroblast subtype 2 |
| FB_7 | EPDC_1 | Epicardium-derived cell subtype 1 |
| FB_8 | AnnFibr_FB | Annulus fibrosus fibroblast |
| FB_9 | Int_FB_2 | Interstitial fibroblast subtype 2 |
| FB_10 | FB_excl_1 | Fibroblast excluded cluster 1 |
| FB_11 | Valve_MC_2 | Valve mesenchymal cell subtype 2 |
| FB_12 | Prol_FB_1 | Proliferating fibroblast subtype 1 |
| FB_13 | Valve_MC_1 | Valve mesenchymal cell subtype 1 |
| FB_14 | FAP | Fibroadipogenic progenitor |
| FB_15 | Peric_MC | Pericardial mesenchymal cell |
| FB_16 | FB_excl_2 | Fibroblast excluded cluster 2 |
| FB_17 | CALN1high_FB | CALN1-high fibroblast |
| FB_18 | Infl_FB | Inflammatory fibroblast |
| FB_19 | Int_FB_3 | Interstitial fibroblast subtype 3 |
| FB_20 | PDE4Chigh_FB | PDE4C-high fibroblast |
| FB_21 | FB_excl_3 | Fibroblast excluded cluster 3 |
| FB_22 | FB_excl_4 | Fibroblast excluded cluster 4 |

**Endothelial (EN) — 22 clusters**

| DL Cluster | Cell Type | Description |
| --- | --- | --- |
| EN_1 | Endoc_EC_1 | Endocardial endothelial cell subtype 1 |
| EN_2 | Cap_EC_2 | Capillary endothelial cell subtype 2 |
| EN_3 | Endoc_EC_3 | Endocardial endothelial cell subtype 3 |
| EN_4 | EC_excl_1 | Endothelial excluded cluster 1 |
| EN_5 | Prol_EC | Proliferating endothelial cell |
| EN_6 | Endoc_EC_4 | Endocardial endothelial cell subtype 4 |
| EN_7 | OF_VEC | Outflow tract venous endothelial cell |
| EN_8 | EC_excl_2 | Endothelial excluded cluster 2 |
| EN_9 | EC_excl_3 | Endothelial excluded cluster 3 |
| EN_10 | Cap_EC_1 | Capillary endothelial cell subtype 1 |
| EN_11 | TMSB10high_C_2 | TMSB10-high cell 2 |
| EN_12 | Endoc_EC_2 | Endocardial endothelial cell subtype 2 |
| EN_13 | Arteriol_EC | Arteriolar endothelial cell |
| EN_14 | PDE4Chigh_EC | PDE4C-high endothelial cell |
| EN_15 | Art_EC_2 | Arterial endothelial cell subtype 2 |
| EN_16 | Ven_EC | Venous endothelial cell |
| EN_17 | IF_VEC | Inflow tract venous endothelial cell |
| EN_18 | AtrSept_EC | Atrial septal endothelial cell |
| EN_19 | Art_EC_1 | Arterial endothelial cell subtype 1 |
| EN_20 | LEC | Lymphatic endothelial cell |
| EN_21 | Venul_EC | Venular endothelial cell |
| EN_22 | EC_excl_4 | Endothelial excluded cluster 4 |

**Innate / Neural (IN) — 19 clusters**

| DL Cluster | Cell Type | Description |
| --- | --- | --- |
| IN_1 | Chrom_C | Chromaffin cell |
| IN_2 | IN_excl_1 | Innate/neural excluded cluster 1 |
| IN_3 | Aut_Neu_1 | Autonomic neuron subtype 1 |
| IN_4 | SCP_1 | Schwann cell precursor subtype 1 |
| IN_5 | IN_excl_2 | Innate/neural excluded cluster 2 |
| IN_6 | IN_excl_3 | Innate/neural excluded cluster 3 |
| IN_7 | SCP_2 | Schwann cell precursor subtype 2 |
| IN_8 | SCP_5 | Schwann cell precursor subtype 5 |
| IN_9 | IN_excl_4 | Innate/neural excluded cluster 4 |
| IN_10 | IN_excl_5 | Innate/neural excluded cluster 5 |
| IN_11 | SCP_4 | Schwann cell precursor subtype 4 |
| IN_12 | SCP_3 | Schwann cell precursor subtype 3 |
| IN_13 | Aut_Neu_2 | Autonomic neuron subtype 2 |
| IN_14 | IN_excl_6 | Innate/neural excluded cluster 6 |
| IN_15 | IN_excl_7 | Innate/neural excluded cluster 7 |
| IN_16 | IN_excl_8 | Innate/neural excluded cluster 8 |
| IN_17 | Bridge_state | Bridge / transitional state cell |
| IN_18 | IN_excl_9 | Innate/neural excluded cluster 9 |
| IN_19 | My_SC | Myelinating Schwann cell |

| Cell Type | 5.5 pcw | 6.0 pcw | 7.0 pcw | 8.0 pcw | 8.5 pcw | 9.0 pcw | 10.0 pcw | 11.5 pcw | 12.0 pcw | 13.2 pcw | 14.0 pcw | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Interstitial Fibroblast (Int_FB) | 731 | 3,150 | 1,194 | 3,448 | 1,413 | 979 | 1,278 | 108 | 882 | 218 | 753 | 14,154 |
| Outflow Tract Fibroblast (OFT_FB) | 829 | 1,211 | 124 | 3,473 | 3,098 | 452 | 333 | 21 | 1,442 | 734 | 864 | 12,581 |
| unassigned (cluster 0) | 94 | 2,268 | 1,180 | 2,355 | 1,341 | 135 | 77 | 1,187 | 512 | 1,130 | 1,755 | 12,034 |
| Metabolically Active Ventricular Cardiomyocyte 2 (MetAct_vCM_2) | 1,247 | 1,672 | 2,302 | 790 | 175 | 87 | 57 | 246 | 369 | 348 | 1,022 | 8,315 |
| Mature Ventricular Cardiomyocyte (Mat_vCM) | 758 | 1,761 | 169 | 2,215 | 298 | 247 | 113 | 32 | 614 | 348 | 978 | 7,533 |
| Proliferating Cardiomyocyte (Prol_CM) | 217 | 1,164 | 1,104 | 1,779 | 725 | 157 | 753 | 88 | 356 | 122 | 1,010 | 7,475 |
| Endocardial Endothelial Cell (Endoc_EC) | 73 | 1,187 | 765 | 157 | 567 | 1,700 | 117 | 339 | 158 | 798 | 1,133 | 6,994 |
| Heart-Lung Atlas Excluded 1 (HL_excl_1) | 138 | 1,563 | 865 | 601 | 84 | 143 | 19 | 86 | 528 | 673 | 1,511 | 6,211 |
| Microvascular Endothelial Cell (MicroVasc_EC) | 169 | 644 | 422 | 1,326 | 27 | 183 | 194 | 96 | 157 | 446 | 889 | 4,553 |
| Metabolically Active Ventricular Cardiomyocyte 1 (MetAct_vCM_1) | 117 | 532 | 590 | 403 | 218 | 218 | 246 | 39 | 465 | 207 | 822 | 3,857 |
| Coronary Artery Smooth Muscle Cell (CA_SMC) | 132 | 768 | 142 | 1,513 | 121 | 163 | 67 | 26 | 95 | 251 | 293 | 3,571 |
| Outflow Tract Smooth Muscle Cell (OFT_SMC) | 279 | 298 | 151 | 356 | 127 | 84 | 173 | 132 | 553 | 499 | 855 | 3,507 |
| Metabolically Active Atrial Cardiomyocyte (MetAct_aCM) | 56 | 203 | 1,203 | 614 | 408 | 297 | 26 | 111 | 153 | 15 | 235 | 3,321 |
| Valve Mesenchymal Cell (Valve_MC) | 65 | 817 | 454 | 344 | 148 | 229 | 384 | 0 | 54 | 360 | 351 | 3,206 |
| Myeloid Cell (MyC) | 0 | 412 | 157 | 786 | 147 | 113 | 5 | 0 | 49 | 13 | 334 | 2,016 |
| Epicardium-Derived Cell (EPDC) | 1 | 357 | 199 | 281 | 302 | 118 | 68 | 104 | 92 | 29 | 405 | 1,956 |
| Annulus Fibrosus Fibroblast (AnnFibr_FB) | 0 | 310 | 101 | 331 | 97 | 193 | 111 | 0 | 136 | 33 | 33 | 1,345 |
| Immature Cardiomyocyte / TMSB10-high Cell 1 (Immat_CM/TMSB10high_C_1) | 0 | 319 | 61 | 182 | 339 | 83 | 37 | 33 | 5 | 28 | 198 | 1,285 |
| Mature Atrial Cardiomyocyte (Mat_aCM) | 0 | 224 | 81 | 289 | 342 | 57 | 67 | 19 | 96 | 19 | 7 | 1,201 |
| Epicardial Cell (EpC) | 0 | 0 | 61 | 629 | 0 | 0 | 0 | 0 | 61 | 30 | 143 | 924 |
| Heart-Lung Atlas Excluded 2 (HL_excl_2) | 0 | 104 | 52 | 45 | 3 | 0 | 5 | 0 | 65 | 1 | 305 | 580 |
| Pericyte (PC) | 0 | 0 | 25 | 368 | 0 | 0 | 0 | 0 | 102 | 0 | 6 | 501 |
| Endocardial Cushion Endothelial Cell (EndocCush_EC) | 0 | 0 | 98 | 172 | 15 | 0 | 0 | 0 | 16 | 0 | 3 | 304 |
| Pericardial Mesenchymal Cell (Peric_MC) | 0 | 0 | 0 | 249 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 249 |
| **Total** | **4,906** | **18,964** | **11,500** | **22,706** | **9,995** | **5,638** | **4,130** | **2,667** | **6,960** | **6,302** | **13,905** | **107,673** |

### Developmental Stage Coverage

| stage (pcw) | samples | donors |
| --- | --- | --- |
| 5.5 | 2 | XDD:400 |
| 6.0 | 3 | XDD:5743:326, XDD:395 |
| 7.0 | 2 | XDD:399 |
| 8.0 | 2 | XDD:1003:334 |
| 8.5 | 2 | XDD:0600:318, XDD:2924:342 |
| 9.0 | 1 | XHU:3565:310 |
| 10.0 | 1 | XDD:394 |
| 11.5 | 1 | XDD:390 |
| 12.0 | 2 | (donor not recorded) |
| 13.2 | 2 | XDD:380 |
| 14.0 | 3 | XDD:385 |

