# CellxGene Subset: Cell Type by Development Stage Counts

## Overview

| dataset title | source file | subset cells | subset genes | unique cell types | unique development stages |
| --- | --- | --- | --- | --- | --- |
| Construction of a human cell landscape at single-cell level | 01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad | 7,997 | 26,069 | 19 | 2 |
| Survey of human embryonic development | 03_survey_of_human_embryonic_development.h5ad | 101,749 | 45,676 | 16 | 5 |
| Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor | 04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad | 26,394 | 35,477 | 8 | 2 |
| Integrated adult and foetal hearts | 05_integrated_adult_and_foetal_hearts.h5ad | 30,889 | 26,886 | 17 | 2 |
| Rotem 12W heart C1 | 06_rotem_12w_heart_c1.h5ad | 4,992 | 35,476 | 5 | 1 |
| Rotem 12W heart B1 | 07_rotem_12w_heart_b1.h5ad | 4,992 | 35,476 | 6 | 1 |
| Rotem 12W heart D1 | 08_rotem_12w_heart_d1.h5ad | 4,992 | 35,476 | 6 | 1 |
| Rotem 12W heart A1 | 09_rotem_12w_heart_a1.h5ad | 4,992 | 35,476 | 5 | 1 |
| Single-nuclei (sn) RNA-seq of the human outflow tract and aortic valve tissue (CS16-17, 12 pcw, Adult) | 10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad | 24,695 | 31,008 | 6 | 2 |
| Spatial dynamics of the developing human heart | lazar_et_al_2025/ (22 CellRanger h5 files) | 76,991 | 59,480 | 34 (HL) / 74 (DL) | 12 |

## 1. Construction of a human cell landscape at single-cell level

- Source file: `01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad`
- Cells in subset: 7,997
- Genes in subset: 26,069
- Unique cell types in subset: 19
- Unique development stages in subset: 2

### Dataset Metadata

| field | value |
| --- | --- |
| assay | microwell-seq |
| source / publication | Han et al. (2020) Nature |
| paper | https://www.nature.com/articles/s41586-020-2157-4 |

### Abstract

Single-cell analysis is a valuable tool for dissecting cellular heterogeneity in complex systems1. However, a comprehensive single-cell atlas has not been achieved for humans. Here we use single-cell mRNA sequencing to determine the cell-type composition of all major human organs and construct a scheme for the human cell landscape (HCL). We have uncovered a single-cell hierarchy for many tissues that have not been well characterized. We established a ‘single-cell HCL analysis’ pipeline that helps to define human cell identity. Finally, we performed a single-cell comparative analysis of landscapes from human and mouse to identify conserved genetic networks. We found that stem and progenitor cells exhibit strong transcriptomic stochasticity, whereas differentiated cells are more distinct. Our results provide a useful resource for the study of human biology.

| cell type | 11th week post-fertilization stage | 12th week post-fertilization stage | Total |
| --- | --- | --- | --- |
| stromal cell | 1,002 | 2,205 | 3,207 |
| ventricular cardiac muscle cell | 925 | 2,071 | 2,996 |
| endothelial cell | 309 | 806 | 1,115 |
| mesenchymal stem cell | 198 | 63 | 261 |
| macrophage | 90 | 22 | 112 |
| smooth muscle cell | 42 | 63 | 105 |
| erythroid lineage cell | 45 | 35 | 80 |
| neuron | 19 | 13 | 32 |
| epithelial cell | 8 | 8 | 16 |
| cell of skeletal muscle | 0 | 15 | 15 |
| T cell | 8 | 3 | 11 |
| professional antigen presenting cell | 9 | 1 | 10 |
| dendritic cell | 6 | 3 | 9 |
| erythroid progenitor cell | 5 | 4 | 9 |
| cord blood hematopoietic stem cell | 4 | 2 | 6 |
| neutrophil | 3 | 2 | 5 |
| fibroblast | 3 | 1 | 4 |
| primordial germ cell | 1 | 2 | 3 |
| monocyte | 1 | 0 | 1 |
| Total | 2,678 | 5,319 | 7,997 |

## 2. Survey of human embryonic development

- Source file: `03_survey_of_human_embryonic_development.h5ad`
- Cells in subset: 101,749
- Genes in subset: 45,676
- Unique cell types in subset: 16
- Unique development stages in subset: 5

### Dataset Metadata

| field | value |
| --- | --- |
| assay | sci-RNA-seq3 |
| source / publication | Cao et al. (2020) Science |
| paper | https://www.science.org/doi/10.1126/science.aba7721 |

### Abstract

Understanding the trajectory of a developing human requires an understanding of how genes are regulated and expressed. Two papers now present a pooled approach using three levels of combinatorial indexing to examine the single-cell gene expression and chromatin landscapes from 15 organs in fetal samples. Cao et al. focus on measurements of RNA in broadly distributed cell types and provide insights into organ specificity. Domcke et al. examined the chromatin accessibility of cells from these organs and identify the regulatory elements that regulate gene expression. Together, these analyses generate comprehensive atlases of early human development.

| cell type | 12th week post-fertilization stage | 13th week post-fertilization stage | 15th week post-fertilization stage | 16th week post-fertilization stage | 17th week post-fertilization stage | Total |
| --- | --- | --- | --- | --- | --- | --- |
| cardiac muscle cell | 8,485 | 4,302 | 25,913 | 9,943 | 18,967 | 67,610 |
| stromal cell | 1,453 | 293 | 5,926 | 1,378 | 3,698 | 12,748 |
| endocardial cell | 621 | 308 | 3,938 | 735 | 1,796 | 7,398 |
| endothelial cell of vascular tree | 880 | 168 | 1,962 | 458 | 1,443 | 4,911 |
| smooth muscle cell | 330 | 77 | 766 | 222 | 641 | 2,036 |
| epicardial adipocyte | 111 | 49 | 1,124 | 147 | 460 | 1,891 |
| innate lymphoid cell | 16 | 4 | 726 | 51 | 551 | 1,348 |
| myeloid cell | 57 | 21 | 519 | 67 | 376 | 1,040 |
| endothelial cell of lymphatic vessel | 68 | 44 | 361 | 36 | 139 | 648 |
| dermis microvascular lymphatic vessel endothelial cell | 76 | 36 | 318 | 32 | 141 | 603 |
| Schwann cell | 70 | 18 | 250 | 35 | 162 | 535 |
| megakaryocyte | 38 | 10 | 167 | 36 | 110 | 361 |
| visceromotor neuron | 20 | 14 | 230 | 27 | 57 | 348 |
| ventricular cardiac muscle cell | 9 | 23 | 40 | 31 | 61 | 164 |
| regular atrial cardiac myocyte | 4 | 11 | 34 | 15 | 38 | 102 |
| erythroblast | 0 | 0 | 2 | 0 | 4 | 6 |
| Total | 12,238 | 5,378 | 42,276 | 13,213 | 28,644 | 101,749 |

## 3. Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor

- Source file: `04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad`
- Cells in subset: 26,394
- Genes in subset: 35,477
- Unique cell types in subset: 8
- Unique development stages in subset: 2

### Dataset Metadata

| field | value |
| --- | --- |
| assay | 10x 3' v3 |
| source / publication | Sim et al. (2021) Circulation |
| paper | https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.120.051921 |

### Abstract

Background:
Despite in-depth knowledge of the molecular mechanisms controlling embryonic heart development, little is known about the signals governing postnatal maturation of the human heart.
Methods:
Single-nucleus RNA sequencing of 54 140 nuclei from 9 human donors was used to profile transcriptional changes in diverse cardiac cell types during maturation from fetal stages to adulthood. Bulk RNA sequencing and the Assay for Transposase-Accessible Chromatin using sequencing were used to further validate transcriptional changes and to profile alterations in the chromatin accessibility landscape in purified cardiomyocyte nuclei from 21 human donors. Functional validation studies of sex steroids implicated in cardiac maturation were performed in human pluripotent stem cell–derived cardiac organoids and mice.
Results:
Our data identify the progesterone receptor as a key mediator of sex-dependent transcriptional programs during cardiomyocyte maturation. Functional validation studies in human cardiac organoids and mice demonstrate that the progesterone receptor drives sex-specific metabolic programs and maturation of cardiac contractile properties.
Conclusions:
These data provide a blueprint for understanding human heart maturation in both sexes and reveal an important role for the progesterone receptor in human heart development.

| cell type | 19th week post-fertilization stage | 20th week post-fertilization stage | Total |
| --- | --- | --- | --- |
| cardiac muscle cell | 14,021 | 5,097 | 19,118 |
| fibroblast | 1,781 | 1,191 | 2,972 |
| endothelial cell | 1,035 | 519 | 1,554 |
| mesothelial cell of epicardium | 987 | 399 | 1,386 |
| leukocyte | 535 | 174 | 709 |
| neuron | 239 | 109 | 348 |
| smooth muscle cell | 74 | 134 | 208 |
| erythrocyte | 75 | 24 | 99 |
| Total | 18,747 | 7,647 | 26,394 |

## 4. Integrated adult and foetal hearts

- Source file: `05_integrated_adult_and_foetal_hearts.h5ad`
- Cells in subset: 30,889
- Genes in subset: 26,886
- Unique cell types in subset: 17
- Unique development stages in subset: 2

### Dataset Metadata

| field | value |
| --- | --- |
| assay | 10x 3' v2, 10x 3' v3 |
| source / publication | Knight-Schrijver et al. (2022) Nat Cardiovasc Res |
| paper | https://www.nature.com/articles/s44161-022-00183-w |

### Abstract

Re-activating quiescent adult epicardium represents a potential therapeutic approach for human cardiac regeneration. However, the exact molecular differences between inactive adult and active fetal epicardium are not known. In this study, we combined fetal and adult human hearts using single-cell and single-nuclei RNA sequencing and compared epicardial cells from both stages. We found that a migratory fibroblast-like epicardial population only in the fetal heart and fetal epicardium expressed angiogenic gene programs, whereas the adult epicardium was solely mesothelial and immune responsive. Furthermore, we predicted that adult hearts may still receive fetal epicardial paracrine communication, including WNT signaling with endocardium, reinforcing the validity of regenerative strategies that administer or reactivate epicardial cells in situ. Finally, we explained graft efficacy of our human embryonic stem-cell-derived epicardium model by noting its similarity to human fetal epicardium. Overall, our study defines epicardial programs of regenerative angiogenesis absent in adult hearts, contextualizes animal studies and defines epicardial states required for effective human heart regeneration.

| cell type | embryonic stage | 10th week post-fertilization stage | Total |
| --- | --- | --- | --- |
| unknown | 3,240 | 1,724 | 4,964 |
| fibroblast | 3,584 | 623 | 4,207 |
| myeloid cell | 2,203 | 1,120 | 3,323 |
| smooth muscle cell | 2,356 | 664 | 3,020 |
| cardiac muscle cell | 2,375 | 191 | 2,566 |
| neuron | 1,763 | 251 | 2,014 |
| endocardial cell | 1,451 | 216 | 1,667 |
| innate lymphoid cell | 450 | 1,206 | 1,656 |
| capillary endothelial cell | 935 | 632 | 1,567 |
| fetal cardiomyocyte | 1,137 | 173 | 1,310 |
| pericyte | 893 | 241 | 1,134 |
| endothelial cell | 858 | 246 | 1,104 |
| endothelial cell of artery | 651 | 252 | 903 |
| mesothelial cell of epicardium | 375 | 515 | 890 |
| cardiac mesenchymal cell | 117 | 198 | 315 |
| vein endothelial cell | 168 | 80 | 248 |
| adipocyte | 1 | 0 | 1 |
| Total | 22,557 | 8,332 | 30,889 |

## 5. Rotem 12W heart C1

- Source file: `06_rotem_12w_heart_c1.h5ad`
- Cells in subset: 4,992
- Genes in subset: 35,476
- Unique cell types in subset: 5
- Unique development stages in subset: 1

### Dataset Metadata

| field | value |
| --- | --- |
| assay | Visium Spatial Gene Expression V1 |
| source / publication | https://elifesciences.org/reviewed-preprints/107748v1 |
| paper | not listed in output.txt |

### Abstract

The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single- cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

| cell type | 13th week post-fertilization stage | Total |
| --- | --- | --- |
| unknown | 2,677 | 2,677 |
| cardiac muscle cell | 1,579 | 1,579 |
| cardiac mesenchymal cell | 648 | 648 |
| neural cell | 54 | 54 |
| endothelial cell | 34 | 34 |
| Total | 4,992 | 4,992 |

## 6. Rotem 12W heart B1

- Source file: `07_rotem_12w_heart_b1.h5ad`
- Cells in subset: 4,992
- Genes in subset: 35,476
- Unique cell types in subset: 6
- Unique development stages in subset: 1

### Dataset Metadata

| field | value |
| --- | --- |
| assay | Visium Spatial Gene Expression V1 |
| source / publication | https://elifesciences.org/reviewed-preprints/107748v1 |
| paper | not listed in output.txt |

### Abstract

The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single- cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

| cell type | 13th week post-fertilization stage | Total |
| --- | --- | --- |
| unknown | 2,310 | 2,310 |
| cardiac muscle cell | 1,848 | 1,848 |
| cardiac mesenchymal cell | 633 | 633 |
| endothelial cell | 135 | 135 |
| neural cell | 65 | 65 |
| hematopoietic cell | 1 | 1 |
| Total | 4,992 | 4,992 |

## 7. Rotem 12W heart D1

- Source file: `08_rotem_12w_heart_d1.h5ad`
- Cells in subset: 4,992
- Genes in subset: 35,476
- Unique cell types in subset: 6
- Unique development stages in subset: 1

### Dataset Metadata

| field | value |
| --- | --- |
| assay | Visium Spatial Gene Expression V1 |
| source / publication | https://elifesciences.org/reviewed-preprints/107748v1 |
| paper | not listed in output.txt |

### Abstract

The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single- cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

| cell type | 13th week post-fertilization stage | Total |
| --- | --- | --- |
| unknown | 3,017 | 3,017 |
| cardiac muscle cell | 1,098 | 1,098 |
| cardiac mesenchymal cell | 679 | 679 |
| endothelial cell | 139 | 139 |
| neural cell | 58 | 58 |
| hematopoietic cell | 1 | 1 |
| Total | 4,992 | 4,992 |

## 8. Rotem 12W heart A1

- Source file: `09_rotem_12w_heart_a1.h5ad`
- Cells in subset: 4,992
- Genes in subset: 35,476
- Unique cell types in subset: 5
- Unique development stages in subset: 1

### Dataset Metadata

| field | value |
| --- | --- |
| assay | Visium Spatial Gene Expression V1 |
| source / publication | https://elifesciences.org/reviewed-preprints/107748v1 |
| paper | not listed in output.txt |

### Abstract

The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single- cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

| cell type | 13th week post-fertilization stage | Total |
| --- | --- | --- |
| cardiac muscle cell | 2,371 | 2,371 |
| unknown | 2,157 | 2,157 |
| cardiac mesenchymal cell | 382 | 382 |
| endothelial cell | 62 | 62 |
| neural cell | 20 | 20 |
| Total | 4,992 | 4,992 |

## 9. Single-nuclei (sn) RNA-seq of the human outflow tract and aortic valve tissue (CS16-17, 12 pcw, Adult)

- Source file: `10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad`
- Cells in subset: 24,695
- Genes in subset: 31,008
- Unique cell types in subset: 6
- Unique development stages in subset: 2

### Dataset Metadata

| field | value |
| --- | --- |
| assay | 10x 3' v2, 10x 3' v3 |
| source / publication | https://elifesciences.org/reviewed-preprints/107748v1 |
| paper | not listed in output.txt |

### Abstract

The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single- cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

| cell type | 6th week post-fertilization stage | 13th week post-fertilization stage | Total |
| --- | --- | --- | --- |
| cardiac mesenchymal cell | 2,556 | 7,015 | 9,571 |
| cardiac muscle cell | 3,149 | 5,956 | 9,105 |
| endothelial cell | 1,572 | 3,315 | 4,887 |
| neural cell | 0 | 803 | 803 |
| hematopoietic cell | 2 | 324 | 326 |
| valve interstitial cell | 0 | 3 | 3 |
| Total | 7,279 | 17,416 | 24,695 |

## 10. Spatial dynamics of the developing human heart (Lazar et al. 2025)

- Source: External dataset (not from CellxGene); Mendeley Data
- Files: `lazar_et_al_2025/` — 22 CellRanger h5 files + Visium/ISS spatial data (two zip archives)
- Cells: 76,991 (high-level clustering); 68,378 (detailed-level)
- Features: 59,480
- Unique cell types: 34 (high-level) / 74 (detailed-level)
- Unique development stages: 12 (5.5–14.0 pcw)

### Dataset Metadata

| field | value |
| --- | --- |
| assay | 10x Chromium v2/v3 scRNA-seq + Visium spatial + ISS |
| source / publication | Lazar et al. (2025) — Mendeley Data |
| paper | Spatial dynamics of the developing human heart |
| reference genome | GRCh38 |

### Abstract

A multi-modal single-cell and spatial atlas of the developing human heart spanning 5.5–14.0 post-conceptual weeks. Integrates 10x Chromium scRNA-seq (76,991 cells from 15 donors across 12 time points), Visium spatial transcriptomics, and in-situ sequencing (ISS; 149-gene panel) to characterize the spatial and temporal dynamics of cardiac cell types including cardiomyocytes, endothelial cells, fibroblasts/mesenchymal cells, and the cardiac conduction system (SAN, AVN, AVB-Bundle Branch, Purkinje fibers) at unprecedented resolution.

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
| Outflow Tract Fibroblast (OFT_FB) | 829 | 1,211 | 124 | 3,473 | 3,098 | 452 | 333 | 21 | 1,442 | 734 | 864 | 12,581 |
| Interstitial Fibroblast (Int_FB) | 731 | 3,150 | 1,194 | 3,448 | 1,413 | 979 | 1,278 | 108 | 882 | 218 | 753 | 14,154 |
| Endocardial Endothelial Cell (Endoc_EC) | 73 | 1,187 | 765 | 157 | 567 | 1,700 | 117 | 339 | 158 | 798 | 1,133 | 6,994 |
| Mature Ventricular Cardiomyocyte (Mat_vCM) | 758 | 1,761 | 169 | 2,215 | 298 | 247 | 113 | 32 | 614 | 348 | 978 | 7,533 |
| Metabolically Active Ventricular Cardiomyocyte 2 (MetAct_vCM_2) | 1,247 | 1,672 | 2,302 | 790 | 175 | 87 | 57 | 246 | 369 | 348 | 1,022 | 8,315 |
| Heart-Lung Atlas Excluded 1 (HL_excl_1) | 138 | 1,563 | 865 | 601 | 84 | 143 | 19 | 86 | 528 | 673 | 1,511 | 6,211 |
| Proliferating Cardiomyocyte (Prol_CM) | 217 | 1,164 | 1,104 | 1,779 | 725 | 157 | 753 | 88 | 356 | 122 | 1,010 | 7,475 |
| Outflow Tract Smooth Muscle Cell (OFT_SMC) | 279 | 298 | 151 | 356 | 127 | 84 | 173 | 132 | 553 | 499 | 855 | 3,507 |
| Metabolically Active Ventricular Cardiomyocyte 1 (MetAct_vCM_1) | 117 | 532 | 590 | 403 | 218 | 218 | 246 | 39 | 465 | 207 | 822 | 3,857 |
| Coronary Artery Smooth Muscle Cell (CA_SMC) | 132 | 768 | 142 | 1,513 | 121 | 163 | 67 | 26 | 95 | 251 | 293 | 3,571 |
| Metabolically Active Atrial Cardiomyocyte (MetAct_aCM) | 56 | 203 | 1,203 | 614 | 408 | 297 | 26 | 111 | 153 | 15 | 235 | 3,321 |
| Microvascular Endothelial Cell (MicroVasc_EC) | 169 | 644 | 422 | 1,326 | 27 | 183 | 194 | 96 | 157 | 446 | 889 | 4,553 |
| Valve Mesenchymal Cell (Valve_MC) | 65 | 817 | 454 | 344 | 148 | 229 | 384 | 0 | 54 | 360 | 351 | 3,206 |
| Epicardium-Derived Cell (EPDC) | 1 | 357 | 199 | 281 | 302 | 118 | 68 | 104 | 92 | 29 | 405 | 1,956 |
| Myeloid Cell (MyC) | 0 | 412 | 157 | 786 | 147 | 113 | 5 | 0 | 49 | 13 | 334 | 2,016 |
| Annulus Fibrosus Fibroblast (AnnFibr_FB) | 0 | 310 | 101 | 331 | 97 | 193 | 111 | 0 | 136 | 33 | 33 | 1,345 |
| Mature Atrial Cardiomyocyte (Mat_aCM) | 0 | 224 | 81 | 289 | 342 | 57 | 67 | 19 | 96 | 19 | 7 | 1,201 |
| Immature Cardiomyocyte / TMSB10-high Cell 1 (Immat_CM/TMSB10high_C_1) | 0 | 319 | 61 | 182 | 339 | 83 | 37 | 33 | 5 | 28 | 198 | 1,285 |
| Heart-Lung Atlas Excluded 2 (HL_excl_2) | 0 | 104 | 52 | 45 | 3 | 0 | 5 | 0 | 65 | 1 | 305 | 580 |
| Epicardial Cell (EpC) | 0 | 0 | 61 | 629 | 0 | 0 | 0 | 0 | 61 | 30 | 143 | 924 |
| Endocardial Cushion Endothelial Cell (EndocCush_EC) | 0 | 0 | 98 | 172 | 15 | 0 | 0 | 0 | 16 | 0 | 3 | 304 |
| Pericyte (PC) | 0 | 0 | 25 | 368 | 0 | 0 | 0 | 0 | 102 | 0 | 6 | 501 |
| Pericardial Mesenchymal Cell (Peric_MC) | 0 | 0 | 0 | 249 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 249 |
| unassigned (cluster 0) | 94 | 2,268 | 1,180 | 2,355 | 1,341 | 135 | 77 | 1,187 | 512 | 1,130 | 1,755 | 12,034 |
| **Total** | **4,906** | **18,964** | **11,500** | **22,706** | **9,995** | **5,638** | **4,130** | **2,667** | **6,960** | **6,302** | **13,905** | **107,673** |

## Consolidated View

This section treats the 9 retained CellxGene subset datasets as one combined collection. Counts are based on concatenating the subset observations after excluding the redundant `02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad` dataset. The Lazar et al. 2025 dataset (section 10) is **not** included in this combined view because it uses a different cell type nomenclature system (HL cluster labels rather than CellxGene ontology terms); its per-stage counts are shown separately in section 10.

- Combined cells across retained subsets: 211,692
- Combined unique cell types: 46
- Combined development stages: 11

### Combined Development Stage Order

| order | development stage | cells in combined data |
| --- | --- | --- |
| 1 | embryonic stage | 22,557 |
| 2 | 6th week post-fertilization stage | 7,279 |
| 3 | 10th week post-fertilization stage | 8,332 |
| 4 | 11th week post-fertilization stage | 2,678 |
| 5 | 12th week post-fertilization stage | 17,557 |
| 6 | 13th week post-fertilization stage | 42,762 |
| 7 | 15th week post-fertilization stage | 42,276 |
| 8 | 16th week post-fertilization stage | 13,213 |
| 9 | 17th week post-fertilization stage | 28,644 |
| 10 | 19th week post-fertilization stage | 18,747 |
| 11 | 20th week post-fertilization stage | 7,647 |

### Combined Cell Type by Development Stage Counts

Rows are all cell types observed anywhere in the retained subsets. Columns are the full ordered set of development stages present after combining the datasets.

| cell type | embryonic stage | 6th week post-fertilization stage | 10th week post-fertilization stage | 11th week post-fertilization stage | 12th week post-fertilization stage | 13th week post-fertilization stage | 15th week post-fertilization stage | 16th week post-fertilization stage | 17th week post-fertilization stage | 19th week post-fertilization stage | 20th week post-fertilization stage | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cardiac muscle cell | 2,375 | 3,149 | 191 | 0 | 8,485 | 17,154 | 25,913 | 9,943 | 18,967 | 14,021 | 5,097 | 105,295 |
| stromal cell | 0 | 0 | 0 | 1,002 | 3,658 | 293 | 5,926 | 1,378 | 3,698 | 0 | 0 | 15,955 |
| unknown | 3,240 | 0 | 1,724 | 0 | 0 | 10,161 | 0 | 0 | 0 | 0 | 0 | 15,125 |
| cardiac mesenchymal cell | 117 | 2,556 | 198 | 0 | 0 | 9,357 | 0 | 0 | 0 | 0 | 0 | 12,228 |
| endocardial cell | 1,451 | 0 | 216 | 0 | 621 | 308 | 3,938 | 735 | 1,796 | 0 | 0 | 9,065 |
| endothelial cell | 858 | 1,572 | 246 | 309 | 806 | 3,685 | 0 | 0 | 0 | 1,035 | 519 | 9,030 |
| fibroblast | 3,584 | 0 | 623 | 3 | 1 | 0 | 0 | 0 | 0 | 1,781 | 1,191 | 7,183 |
| smooth muscle cell | 2,356 | 0 | 664 | 42 | 393 | 77 | 766 | 222 | 641 | 74 | 134 | 5,369 |
| endothelial cell of vascular tree | 0 | 0 | 0 | 0 | 880 | 168 | 1,962 | 458 | 1,443 | 0 | 0 | 4,911 |
| myeloid cell | 2,203 | 0 | 1,120 | 0 | 57 | 21 | 519 | 67 | 376 | 0 | 0 | 4,363 |
| ventricular cardiac muscle cell | 0 | 0 | 0 | 925 | 2,080 | 23 | 40 | 31 | 61 | 0 | 0 | 3,160 |
| innate lymphoid cell | 450 | 0 | 1,206 | 0 | 16 | 4 | 726 | 51 | 551 | 0 | 0 | 3,004 |
| neuron | 1,763 | 0 | 251 | 19 | 13 | 0 | 0 | 0 | 0 | 239 | 109 | 2,394 |
| mesothelial cell of epicardium | 375 | 0 | 515 | 0 | 0 | 0 | 0 | 0 | 0 | 987 | 399 | 2,276 |
| epicardial adipocyte | 0 | 0 | 0 | 0 | 111 | 49 | 1,124 | 147 | 460 | 0 | 0 | 1,891 |
| capillary endothelial cell | 935 | 0 | 632 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,567 |
| fetal cardiomyocyte | 1,137 | 0 | 173 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,310 |
| pericyte | 893 | 0 | 241 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,134 |
| neural cell | 0 | 0 | 0 | 0 | 0 | 1,000 | 0 | 0 | 0 | 0 | 0 | 1,000 |
| endothelial cell of artery | 651 | 0 | 252 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 903 |
| leukocyte | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 535 | 174 | 709 |
| endothelial cell of lymphatic vessel | 0 | 0 | 0 | 0 | 68 | 44 | 361 | 36 | 139 | 0 | 0 | 648 |
| dermis microvascular lymphatic vessel endothelial cell | 0 | 0 | 0 | 0 | 76 | 36 | 318 | 32 | 141 | 0 | 0 | 603 |
| Schwann cell | 0 | 0 | 0 | 0 | 70 | 18 | 250 | 35 | 162 | 0 | 0 | 535 |
| megakaryocyte | 0 | 0 | 0 | 0 | 38 | 10 | 167 | 36 | 110 | 0 | 0 | 361 |
| visceromotor neuron | 0 | 0 | 0 | 0 | 20 | 14 | 230 | 27 | 57 | 0 | 0 | 348 |
| hematopoietic cell | 0 | 2 | 0 | 0 | 0 | 326 | 0 | 0 | 0 | 0 | 0 | 328 |
| mesenchymal stem cell | 0 | 0 | 0 | 198 | 63 | 0 | 0 | 0 | 0 | 0 | 0 | 261 |
| vein endothelial cell | 168 | 0 | 80 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 248 |
| macrophage | 0 | 0 | 0 | 90 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 112 |
| regular atrial cardiac myocyte | 0 | 0 | 0 | 0 | 4 | 11 | 34 | 15 | 38 | 0 | 0 | 102 |
| erythrocyte | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 75 | 24 | 99 |
| erythroid lineage cell | 0 | 0 | 0 | 45 | 35 | 0 | 0 | 0 | 0 | 0 | 0 | 80 |
| epithelial cell | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |
| cell of skeletal muscle | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 15 |
| T cell | 0 | 0 | 0 | 8 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| professional antigen presenting cell | 0 | 0 | 0 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| dendritic cell | 0 | 0 | 0 | 6 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| erythroid progenitor cell | 0 | 0 | 0 | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| cord blood hematopoietic stem cell | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| erythroblast | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 0 | 0 | 6 |
| neutrophil | 0 | 0 | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| valve interstitial cell | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| primordial germ cell | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| adipocyte | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| monocyte | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| Total | 22,557 | 7,279 | 8,332 | 2,678 | 17,557 | 42,762 | 42,276 | 13,213 | 28,644 | 18,747 | 7,647 | 211,692 |



