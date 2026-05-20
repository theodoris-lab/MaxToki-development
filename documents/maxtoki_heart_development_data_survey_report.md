# Maxtoki Heart Development — Data Curation Report


---

## Overview

This report summarizes the single-cell transcriptomics datasets curated for the **maxtoki heart development** project. Four data sources are covered: (1) five single-cell datasets downloaded from [CellxGene](https://cellxgene.cziscience.com/) and subsetted to embryonic/fetal human heart cells, (2) one external dataset from [Mendeley Data](https://data.mendeley.com/) (Lázár et al. 2025, *Nature Genetics*), (3) one gastrulation atlas from EMBL-EBI (Tyser et al. 2021, *Nature*), and (4) a cardiac-subset of the whole-embryo organogenesis atlas from the lab directory (Xu et al. 2023, *Nat. Cell Biol.*). All datasets are single-cell resolution (10x Chromium, microwell-seq, sci-RNA-seq3, snRNA-seq, or Smart-seq2); Visium and all other spatial transcriptomics modalities are excluded. Together these eight datasets span from gastrulation (Carnegie Stage 7, ~Day 17) through the 20th post-fertilization week.

**Combined totals:**

| Source | Datasets | Cells | Genes | Developmental window |
| --- | ---: | ---: | ---: | --- |
| CellxGene (5 sc datasets) | 5 | 191,724 | — | Embryonic – 20th week pcf |
| Lázár et al. 2025 | 1 | 107,673 | 59,480 | 5.5 – 14.0 pcw |
| Tyser et al. 2021 | 1 | 1,195 | 40,614 | CS7 (~Day 17) |
| Xu et al. 2023 (curated cardiac subset) | 1 | 5,243 | 32,351 | CS12–CS15-16 (~Day 26–40) |
| **Grand total** | **8** | **305,835** | — | **CS7 (~Day 17) – 20th week pcf** |

*pcf = post-fertilization (CellxGene ontology terminology); pcw = post-conceptual week (Lázár et al. terminology). These are equivalent naming systems (pcw ≈ pcf); the difference in terminology reflects each study's annotation conventions.*

---

## Section 1: Data Curation Summary Table

Datasets are numbered 1–8. Datasets 1–5 were downloaded from CellxGene and subsetted using a custom pipeline (`subset_cellxgene_heart_development.py`) that filters to embryonic/fetal human heart observations. Dataset 6 was downloaded from Mendeley Data and is already heart-specific; no further subsetting was applied. Dataset 7 was downloaded from EMBL-EBI. Dataset 8 is a cardiac subset of the whole-embryo Xu et al. 2023 organogenesis atlas from the lab directory. Visium and all spatial transcriptomics modalities are excluded throughout.

| # | Dataset | Source | First Author & Year | Journal | Assay | Orig. Cells | Orig. Genes | Curated Cells | Curated Genes | % Kept | Unique Cell Types (curated) | Donors | Unique Dev. Stages | Link |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Construction of a human cell landscape at single-cell level | CellxGene | Han et al. (2020) | *Nature* | microwell-seq | 599,926 | 26,069 | 7,997 | 26,069 | 1.3% | 19 | 2 | 2 | https://www.nature.com/articles/s41586-020-2157-4 |
| 2 | Survey of human embryonic development | CellxGene | Cao et al. (2020) | *Science* | sci-RNA-seq3 | 4,062,980 | 45,676 | 101,749 | 45,676 | 2.5% | 16 | 9 | 5 | https://www.science.org/doi/10.1126/science.aba7721 |
| 3 | Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor | CellxGene | Sim et al. (2021) | *Circulation* | 10x 3′ v3 | 51,176 | 35,477 | 26,394 | 35,477 | 51.6% | 8 | 3 | 2 | https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.120.051921 |
| 4 | Integrated adult and foetal hearts | CellxGene | Knight-Schrijver et al. (2022) | *Nat. Cardiovasc. Res.* | 10x 3′ v2/v3 | 60,668 | 26,886 | 30,889 | 26,886 | 50.9% | 17 | 7 | 2 | https://www.nature.com/articles/s44161-022-00183-w |
| 5 | snRNA-seq of human outflow tract and aortic valve tissue (CS16-17, 12 pcw) | CellxGene | Leshem et al. (2025) | *eLife* | 10x 3′ v2/v3 (snRNA-seq) | 30,125 | 31,008 | 24,695 | 31,008 | 82.0% | 6 | 4 | 2 | https://doi.org/10.7554/eLife.107748 |
| 6 | Spatiotemporal gene expression and cellular dynamics of the developing human heart | Mendeley Data | Lázár et al. (2025) | *Nat. Genetics* | 10x Chromium v2/v3 scRNA-seq | 107,673 | 59,480 | 107,673 | 59,480 | N/A | 23 | 15 | 11 | https://www.nature.com/articles/s41588-025-02352-6 |
| 7 | Single-cell transcriptomic characterization of a gastrulating human embryo | EMBL-EBI | Tyser et al. (2021) | *Nature* | Smart-seq2 (plate-based) | 1,195 | 40,614 | 1,195 | 40,614 | 100% | 11 | 1 | 1 | https://www.nature.com/articles/s41586-021-04158-y |
| 8 | A single-cell transcriptome atlas profiles early organogenesis in human embryos | Lab directory | Xu et al. (2023) | *Nat. Cell Biol.* | 10x Chromium scRNA-seq | 185,140 | 32,351 | 5,243 | 32,351 | 2.8% | 11 | 7 | 3 | https://www.nature.com/articles/s41556-023-01108-w |

**Notes:**
- **Dataset 5 (Leshem et al. 2025)** — snRNA-seq from embryonic (Carnegie Stage 16-17) and fetal (12 pcw) outflow tract tissue. The same publication also includes four Visium spatial transcriptomics slides and adult aortic valve nuclei; neither are included here.
- **Dataset 6 (Lázár et al. 2025)** was not subjected to the CellxGene subsetting pipeline; the 107,673 cells represent all cells extracted from the 21 10x Chromium SC libraries. These libraries are already heart-specific (curated from embryonic/fetal donors). The paper also includes Visium spatial and ISS modalities; only the sc RNA-seq libraries are used here.
- **Dataset 7 (Tyser et al. 2021)** is a plate-based (Smart-seq2) single-cell gastrulation atlas from one IVF embryo at Carnegie Stage 7 (~Day 17); it covers the earliest pluripotent and nascent mesoderm stages, predating cardiac specification. Downloaded from EMBL-EBI (E-MTAB-9388) via the lab directory (`/gladstone/theodoris/lab/ctheodoris/validation/gastrulation`).
- **Dataset 8 (Xu et al. 2023)** is a whole-embryo organogenesis atlas (185,140 cells, 7 embryos, Carnegie stages CS12–CS15-16, ~4–6 weeks post-fertilization). Only cardiac-relevant cells are retained: cells from the `splanchnic_LPM` developmental system with cardiac annotations (ventricle cardiomyocyte, atria cardiomyocyte, cardiomyocyte, Second heart field, atrioventricular canal, sinoatrial node, epicardium, epicardial derived cell, pericyte) and cells from the `endothelium` developmental system labeled as endocardium or endocardial derived cell. Data from lab directory (David Wen; `/gladstone/theodoris/lab/dwen/data/organogenesis_data/organogenesis/`). Note: the user-cited companion URL https://www.nature.com/articles/s41556-023-01113-z points to the same issue; the canonical PubMed DOI is 10.1038/s41556-023-01108-w.
- The CellxGene subsetting pipeline filtered to: `tissue = heart` (or equivalent ontology terms), `disease = normal`, `organism = Homo sapiens`, and `developmental_stage` restricted to embryonic / fetal stages.

---

## Section 2: Cell Type × Development Stage Counts — All Datasets (1–8)

Rows are cell types grouped into broad biological categories; columns are developmental time points in post-conceptual weeks (pcw). Post-fertilization week (CellxGene) and pcw (Lázár) are treated as equivalent; 1 pcw = 1 week post-fertilization. CellxGene uses Human Cell Ontology labels; Lázár uses HDCA Heart-Lung Atlas (HL) cluster labels — the two nomenclature systems do not share names, but the **Category** column groups cell types from both sources by shared biology. "—" = time point not covered by that source.

**Carnegie Stage 17 conversion:** Dataset 5 (Leshem et al. 2025, snRNA-seq OFT) annotates its embryonic cells as "Carnegie stage 17". Carnegie Stage 17 ≈ days 41–44 of development (≈ 6.0–6.5 pcw, per O'Rahilly & Müller's Carnegie staging criteria). Those 7,279 cells are counted under 6.0 pcw. Datasets 7–8 (Tyser et al., Xu et al.) also use Carnegie stages; CS7, CS12, CS13-14, and CS15-16 are mapped to approximate pcw values (2.5, 4.0, 4.5, and 5.0 pcw respectively) in the table.

- **Total cells (all 8 datasets):** 305,835 (191,724 CellxGene sc + 107,673 Lázár + 5,243 Xu et al. cardiac subset + 1,195 Tyser et al.).
- **Columns 2.5–5.0 pcw (marked ‡, Datasets 7–8 only):** approximate Carnegie stage conversions — CS7 ≈ 2.5 pcw (Day 16–19); CS12 ≈ 4.0 pcw (Day 26–28); CS13-14 ≈ 4.5 pcw (Day 28–33); CS15-16 ≈ 5.0 pcw (Day 33–40).
- **Columns emb\* and 5.5–20.0 pcw:** Datasets 1–6 only. "emb" = CellxGene "embryonic stage" (unresolved pcw, Datasets 1, 3, 4 only).

| Category | Cell Type | Src | 2.5‡ | 4.0‡ | 4.5‡ | 5.0‡ | emb\* | 5.5 | 6.0† | 7.0 | 8.0 | 8.5 | 9.0 | 10.0 | 11.0 | 11.5 | 12.0 | 13.0 | 14.0 | 15.0 | 16.0 | 17.0 | 19.0 | 20.0 | **Total** |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cardiomyocyte | cardiac muscle cell* | CXG | — | — | — | — | 2,375 | — | 3,149 | — | — | — | — | 191 | 0 | — | 8,485 | 10,258 | — | 25,913 | 9,943 | 18,967 | 14,021 | 5,097 | **98,399** |
| Cardiomyocyte | ventricular cardiac muscle cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 925 | — | 2,080 | 23 | — | 40 | 31 | 61 | 0 | 0 | **3,160** |
| Cardiomyocyte | fetal cardiomyocyte* | CXG | — | — | — | — | 1,137 | — | 0 | — | — | — | — | 173 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **1,310** |
| Cardiomyocyte | regular atrial cardiac myocyte* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 4 | 11 | — | 34 | 15 | 38 | 0 | 0 | **102** |
| Cardiomyocyte | Metabolically Active Ventricular Cardiomyocyte 2 (MetAct_vCM_2) | Lázár | — | — | — | — | — | 1,247 | 1,672 | 2,302 | 790 | 175 | 87 | 57 | — | 246 | 369 | 348 | 1,022 | — | — | — | — | — | **8,315** |
| Cardiomyocyte | Mature Ventricular Cardiomyocyte (Mat_vCM) | Lázár | — | — | — | — | — | 758 | 1,761 | 169 | 2,215 | 298 | 247 | 113 | — | 32 | 614 | 348 | 978 | — | — | — | — | — | **7,533** |
| Cardiomyocyte | Proliferating Cardiomyocyte (Prol_CM) | Lázár | — | — | — | — | — | 217 | 1,164 | 1,104 | 1,779 | 725 | 157 | 753 | — | 88 | 356 | 122 | 1,010 | — | — | — | — | — | **7,475** |
| Cardiomyocyte | Metabolically Active Ventricular Cardiomyocyte 1 (MetAct_vCM_1) | Lázár | — | — | — | — | — | 117 | 532 | 590 | 403 | 218 | 218 | 246 | — | 39 | 465 | 207 | 822 | — | — | — | — | — | **3,857** |
| Cardiomyocyte | Metabolically Active Atrial Cardiomyocyte (MetAct_aCM) | Lázár | — | — | — | — | — | 56 | 203 | 1,203 | 614 | 408 | 297 | 26 | — | 111 | 153 | 15 | 235 | — | — | — | — | — | **3,321** |
| Cardiomyocyte | Immature Cardiomyocyte (Immat_CM) | Lázár | — | — | — | — | — | 0 | 319 | 61 | 182 | 339 | 83 | 37 | — | 33 | 5 | 28 | 198 | — | — | — | — | — | **1,285** |
| Cardiomyocyte | Mature Atrial Cardiomyocyte (Mat_aCM) | Lázár | — | — | — | — | — | 0 | 224 | 81 | 289 | 342 | 57 | 67 | — | 19 | 96 | 19 | 7 | — | — | — | — | — | **1,201** |
| Cardiomyocyte | ventricle cardiomyocyte | Xu | — | 260 | 281 | 431 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **972** |
| Cardiomyocyte | atria cardiomyocyte | Xu | — | 137 | 163 | 295 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **595** |
| Cardiomyocyte | cardiomyocyte | Xu | — | 99 | 88 | 176 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **363** |
| Cardiac Progenitor | Second heart field (SHF) | Xu | — | 75 | 169 | 129 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **373** |
| Cardiac Progenitor | atrioventricular canal | Xu | — | 22 | 68 | 168 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **258** |
| Cardiac Progenitor | sinoatrial node (SAN) | Xu | — | 14 | 26 | 65 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **105** |
| Stromal / Mesenchymal | stromal cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 1,002 | — | 3,658 | 293 | — | 5,926 | 1,378 | 3,698 | 0 | 0 | **15,955** |
| Stromal / Mesenchymal | cardiac mesenchymal cell* | CXG | — | — | — | — | 117 | — | 2,556 | — | — | — | — | 198 | 0 | — | 0 | 7,015 | — | 0 | 0 | 0 | 0 | 0 | **9,886** |
| Stromal / Mesenchymal | fibroblast* | CXG | — | — | — | — | 3,584 | — | 0 | — | — | — | — | 623 | 3 | — | 1 | 0 | — | 0 | 0 | 0 | 1,781 | 1,191 | **7,183** |
| Stromal / Mesenchymal | mesenchymal stem cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 198 | — | 63 | 0 | — | 0 | 0 | 0 | 0 | 0 | **261** |
| Stromal / Mesenchymal | Interstitial Fibroblast (Int_FB) | Lázár | — | — | — | — | — | 731 | 3,150 | 1,194 | 3,448 | 1,413 | 979 | 1,278 | — | 108 | 882 | 218 | 753 | — | — | — | — | — | **14,154** |
| Stromal / Mesenchymal | Outflow Tract Fibroblast (OFT_FB) | Lázár | — | — | — | — | — | 829 | 1,211 | 124 | 3,473 | 3,098 | 452 | 333 | — | 21 | 1,442 | 734 | 864 | — | — | — | — | — | **12,581** |
| Stromal / Mesenchymal | Valve Mesenchymal Cell (Valve_MC) | Lázár | — | — | — | — | — | 65 | 817 | 454 | 344 | 148 | 229 | 384 | — | 0 | 54 | 360 | 351 | — | — | — | — | — | **3,206** |
| Stromal / Mesenchymal | Annulus Fibrosus Fibroblast (AnnFibr_FB) | Lázár | — | — | — | — | — | 0 | 310 | 101 | 331 | 97 | 193 | 111 | — | 0 | 136 | 33 | 33 | — | — | — | — | — | **1,345** |
| Pericyte | pericyte* | CXG | — | — | — | — | 893 | — | 0 | — | — | — | — | 241 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **1,134** |
| Pericyte | Pericyte* (PC) | Lázár | — | — | — | — | — | 0 | 0 | 25 | 368 | 0 | 0 | 0 | — | 0 | 102 | 0 | 6 | — | — | — | — | — | **501** |
| Pericyte | Pericyte-like Mesenchymal Cell / Pericyte* (Peric_MC) | Lázár | — | — | — | — | — | 0 | 0 | 0 | 249 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 | — | — | — | — | — | **249** |
| Pericyte | pericyte (myocardium) | Xu | — | 0 | 0 | 17 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **17** |
| Endothelial | endocardial cell* | CXG | — | — | — | — | 1,451 | — | 0 | — | — | — | — | 216 | 0 | — | 621 | 308 | — | 3,938 | 735 | 1,796 | 0 | 0 | **9,065** |
| Endothelial | endothelial cell | CXG | — | — | — | — | 858 | — | 1,572 | — | — | — | — | 246 | 309 | — | 806 | 3,315 | — | 0 | 0 | 0 | 1,035 | 519 | **8,660** |
| Endothelial | endothelial cell of vascular tree | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 880 | 168 | — | 1,962 | 458 | 1,443 | 0 | 0 | **4,911** |
| Endothelial | capillary endothelial cell* | CXG | — | — | — | — | 935 | — | 0 | — | — | — | — | 632 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **1,567** |
| Endothelial | endothelial cell of artery* | CXG | — | — | — | — | 651 | — | 0 | — | — | — | — | 252 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **903** |
| Endothelial | endothelial cell of lymphatic vessel* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 68 | 44 | — | 361 | 36 | 139 | 0 | 0 | **648** |
| Endothelial | dermis microvascular lymphatic vessel endothelial cell | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 76 | 36 | — | 318 | 32 | 141 | 0 | 0 | **603** |
| Endothelial | vein endothelial cell* | CXG | — | — | — | — | 168 | — | 0 | — | — | — | — | 80 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **248** |
| Endothelial | Endocardial Endothelial Cell* (Endoc_EC) | Lázár | — | — | — | — | — | 73 | 1,187 | 765 | 157 | 567 | 1,700 | 117 | — | 339 | 158 | 798 | 1,133 | — | — | — | — | — | **6,994** |
| Endothelial | Microvascular Endothelial Cell (MicroVasc_EC) | Lázár | — | — | — | — | — | 169 | 644 | 422 | 1,326 | 27 | 183 | 194 | — | 96 | 157 | 446 | 889 | — | — | — | — | — | **4,553** |
| Endothelial | Endocardial Cushion Endothelial Cell (EndocCush_EC) | Lázár | — | — | — | — | — | 0 | 0 | 98 | 172 | 15 | 0 | 0 | — | 0 | 16 | 0 | 3 | — | — | — | — | — | **304** |
| Endothelial | endocardium | Xu | — | 20 | 417 | 583 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **1,020** |
| Endothelial | endocardial derived cell | Xu | — | 23 | 254 | 226 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **503** |
| Smooth Muscle | smooth muscle cell | CXG | — | — | — | — | 2,356 | — | 0 | — | — | — | — | 664 | 42 | — | 393 | 77 | — | 766 | 222 | 641 | 74 | 134 | **5,369** |
| Smooth Muscle | Coronary Artery Smooth Muscle Cell (CA_SMC) | Lázár | — | — | — | — | — | 132 | 768 | 142 | 1,513 | 121 | 163 | 67 | — | 26 | 95 | 251 | 293 | — | — | — | — | — | **3,571** |
| Smooth Muscle | Outflow Tract Smooth Muscle Cell* (OFT_SMC) | Lázár | — | — | — | — | — | 279 | 298 | 151 | 356 | 127 | 84 | 173 | — | 132 | 553 | 499 | 855 | — | — | — | — | — | **3,507** |
| Epicardial | mesothelial cell of epicardium* | CXG | — | — | — | — | 375 | — | 0 | — | — | — | — | 515 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 987 | 399 | **2,276** |
| Epicardial | epicardial adipocyte* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 111 | 49 | — | 1,124 | 147 | 460 | 0 | 0 | **1,891** |
| Epicardial | Epicardium-Derived Cell (EPDC) | Lázár | — | — | — | — | — | 1 | 357 | 199 | 281 | 302 | 118 | 68 | — | 104 | 92 | 29 | 405 | — | — | — | — | — | **1,956** |
| Epicardial | Epicardial Cell (EpC) | Lázár | — | — | — | — | — | 0 | 0 | 61 | 629 | 0 | 0 | 0 | — | 0 | 61 | 30 | 143 | — | — | — | — | — | **924** |
| Epicardial | epicardium | Xu | — | 15 | 142 | 95 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **252** |
| Epicardial | epicardial derived cell | Xu | — | 6 | 131 | 648 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **785** |
| Myeloid / Immune | myeloid cell* | CXG | — | — | — | — | 2,203 | — | 0 | — | — | — | — | 1,120 | 0 | — | 57 | 21 | — | 519 | 67 | 376 | 0 | 0 | **4,363** |
| Myeloid / Immune | innate lymphoid cell* | CXG | — | — | — | — | 450 | — | 0 | — | — | — | — | 1,206 | 0 | — | 16 | 4 | — | 726 | 51 | 551 | 0 | 0 | **3,004** |
| Myeloid / Immune | leukocyte* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 535 | 174 | **709** |
| Myeloid / Immune | hematopoietic cell* | CXG | — | — | — | — | 0 | — | 2 | — | — | — | — | 0 | 0 | — | 0 | 324 | — | 0 | 0 | 0 | 0 | 0 | **326** |
| Myeloid / Immune | macrophage* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 90 | — | 22 | 0 | — | 0 | 0 | 0 | 0 | 0 | **112** |
| Myeloid / Immune | T cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 8 | — | 3 | 0 | — | 0 | 0 | 0 | 0 | 0 | **11** |
| Myeloid / Immune | professional antigen presenting cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 9 | — | 1 | 0 | — | 0 | 0 | 0 | 0 | 0 | **10** |
| Myeloid / Immune | dendritic cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 6 | — | 3 | 0 | — | 0 | 0 | 0 | 0 | 0 | **9** |
| Myeloid / Immune | monocyte* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 1 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **1** |
| Myeloid / Immune | Myeloid Cell* (MyC) | Lázár | — | — | — | — | — | 0 | 412 | 157 | 786 | 147 | 113 | 5 | — | 0 | 49 | 13 | 334 | — | — | — | — | — | **2,016** |
| Neural | neuron* | CXG | — | — | — | — | 1,763 | — | 0 | — | — | — | — | 251 | 19 | — | 13 | 0 | — | 0 | 0 | 0 | 239 | 109 | **2,394** |
| Neural | neural cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 803 | — | 0 | 0 | 0 | 0 | 0 | **803** |
| Neural | Schwann cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 70 | 18 | — | 250 | 35 | 162 | 0 | 0 | **535** |
| Neural | visceromotor neuron* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 20 | 14 | — | 230 | 27 | 57 | 0 | 0 | **348** |
| Blood / Hematopoietic | megakaryocyte | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 38 | 10 | — | 167 | 36 | 110 | 0 | 0 | **361** |
| Blood / Hematopoietic | erythrocyte* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 75 | 24 | **99** |
| Blood / Hematopoietic | erythroid lineage cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 45 | — | 35 | 0 | — | 0 | 0 | 0 | 0 | 0 | **80** |
| Blood / Hematopoietic | erythroid progenitor cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 5 | — | 4 | 0 | — | 0 | 0 | 0 | 0 | 0 | **9** |
| Blood / Hematopoietic | cord blood hematopoietic stem cell | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 4 | — | 2 | 0 | — | 0 | 0 | 0 | 0 | 0 | **6** |
| Blood / Hematopoietic | erythroblast* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 0 | — | 2 | 0 | 4 | 0 | 0 | **6** |
| Blood / Hematopoietic | neutrophil* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 3 | — | 2 | 0 | — | 0 | 0 | 0 | 0 | 0 | **5** |
| Valve | valve interstitial cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 3 | — | 0 | 0 | 0 | 0 | 0 | **3** |
| Unclassified | unknown | CXG | — | — | — | — | 3,240 | — | 0 | — | — | — | — | 1,724 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **4,964** |
| Unclassified | epithelial cell* | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 8 | — | 8 | 0 | — | 0 | 0 | 0 | 0 | 0 | **16** |
| Unclassified | cell of skeletal muscle | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 0 | — | 15 | 0 | — | 0 | 0 | 0 | 0 | 0 | **15** |
| Unclassified | primordial germ cell | CXG | — | — | — | — | 0 | — | 0 | — | — | — | — | 0 | 1 | — | 2 | 0 | — | 0 | 0 | 0 | 0 | 0 | **3** |
| Unclassified | adipocyte* | CXG | — | — | — | — | 1 | — | 0 | — | — | — | — | 0 | 0 | — | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | **1** |
| Unclassified | Heart-Lung Atlas Excluded 1 (HL_excl_1) | Lázár | — | — | — | — | — | 138 | 1,563 | 865 | 601 | 84 | 143 | 19 | — | 86 | 528 | 673 | 1,511 | — | — | — | — | — | **6,211** |
| Unclassified | unassigned (cluster 0) | Lázár | — | — | — | — | — | 94 | 2,268 | 1,180 | 2,355 | 1,341 | 135 | 77 | — | 1,187 | 512 | 1,130 | 1,755 | — | — | — | — | — | **12,034** |
| Unclassified | Heart-Lung Atlas Excluded 2 (HL_excl_2) | Lázár | — | — | — | — | — | 0 | 104 | 52 | 45 | 3 | 0 | 5 | — | 0 | 65 | 1 | 305 | — | — | — | — | — | **580** |
| Gastrulation / Early Mesoderm | primitive streak | Tyser | 202 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **202** |
| Gastrulation / Early Mesoderm | emergent mesoderm | Tyser | 185 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **185** |
| Gastrulation / Early Mesoderm | advanced mesoderm | Tyser | 164 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **164** |
| Gastrulation / Early Mesoderm | endodermal cell | Tyser | 135 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **135** |
| Gastrulation / Early Mesoderm | epiblast cell | Tyser | 133 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **133** |
| Gastrulation / Early Mesoderm | hemogenic endothelial progenitor | Tyser | 111 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **111** |
| Gastrulation / Early Mesoderm | nascent mesoderm | Tyser | 98 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **98** |
| Gastrulation / Early Mesoderm | yolk sac mesoderm | Tyser | 83 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **83** |
| Gastrulation / Early Mesoderm | erythrocyte (CS7) | Tyser | 32 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **32** |
| Gastrulation / Early Mesoderm | ectodermal cell | Tyser | 29 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **29** |
| Gastrulation / Early Mesoderm | axial mesoderm | Tyser | 23 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **23** |
| **CXG Subtotal** | | | **—** | **—** | **—** | **—** | **22,557** | **—** | **7,279** | **—** | **—** | **—** | **—** | **8,332** | **2,678** | **—** | **17,557** | **22,794** | **—** | **42,276** | **13,213** | **28,644** | **18,747** | **7,647** | **191,724** |
| **Lázár Subtotal** | | | **—** | **—** | **—** | **—** | **—** | **4,906** | **18,964** | **11,500** | **22,706** | **9,995** | **5,638** | **4,130** | **—** | **2,667** | **6,960** | **6,302** | **13,905** | **—** | **—** | **—** | **—** | **—** | **107,673** |
| **Xu et al. Subtotal** | | | **—** | **671** | **1,739** | **2,833** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **5,243** |
| **Tyser Subtotal** | | | **1,195** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **1,195** |
| **Grand Total** | | | **1,195** | **671** | **1,739** | **2,833** | **22,557** | **4,906** | **26,243** | **11,500** | **22,706** | **9,995** | **5,638** | **12,462** | **2,678** | **2,667** | **24,517** | **29,096** | **13,905** | **42,276** | **13,213** | **28,644** | **18,747** | **7,647** | **305,835** |

\*"embryonic stage" is the CellxGene Human Cell Ontology label for early embryonic cells with no resolved week annotation (Datasets 1, 3, and 4).
†6.0 pcw column includes the 7,279 Carnegie Stage 17 cells from Dataset 5, remapped as described above.
‡2.5, 4.0, 4.5, and 5.0 pcw columns are approximate conversions from Carnegie staging for Datasets 7–8: CS7 (~Day 16–19) ≈ 2.5 pcw; CS12 (~Day 26–28) ≈ 4.0 pcw; CS13-14 (~Day 28–33) ≈ 4.5 pcw; CS15-16 (~Day 33–40) ≈ 5.0 pcw.
Src: CXG = CellxGene Datasets 1–5 (Human Cell Ontology labels); Lázár = Lázár et al. 2025 Dataset 6 (HDCA HL cluster labels); Xu = Xu et al. 2023 Dataset 8 (original annotation labels, cardiac subset only); Tyser = Tyser et al. 2021 Dataset 7 (original cell type labels).
Lineage tree cross-reference: cell type names marked with \* have an exact name match in documents/human_heart_development_lineage_tree.txt.

**Category mapping rationale:** Cardiomyocyte — CXG generic/ventricular/atrial/fetal CM types mapped to Lázár mature/metabolically-active/proliferating/immature CM types; Xu et al. ventricle cardiomyocyte, atria cardiomyocyte, and cardiomyocyte added. Cardiac Progenitor (new) — Xu et al. Second heart field, atrioventricular canal, and sinoatrial node; no equivalent in CXG or Lázár HL schema. Stromal/Mesenchymal — CXG fibroblast, cardiac mesenchymal, and stromal cell types mapped to Lázár interstitial, OFT, annulus fibrosus, valve mesenchymal, and pericyte-like mesenchymal fibroblast types. Endothelial — CXG endocardial/vascular/capillary/arterial/lymphatic types mapped to Lázár endocardial, microvascular, and endocardial cushion EC types; Xu et al. endocardium and endocardial derived cell added. Smooth Muscle — CXG smooth muscle cell mapped to Lázár coronary artery and OFT SMC types. Epicardial — CXG mesothelial/epicardial adipocyte types mapped to Lázár epicardial and epicardium-derived cell types; Xu et al. epicardium and epicardial derived cell added. Pericyte — CXG/Lázár pericyte types; Xu et al. pericyte (myocardium) added. Myeloid/Immune — CXG myeloid, macrophage, monocyte, DC, lymphoid types mapped to Lázár myeloid cell type. Neural (CXG only) and Blood/Hematopoietic (CXG only) have no corresponding Lázár HL types. Valve interstitial cell (CXG only) has no direct Lázár equivalent at HL level. Unclassified includes CXG "unknown" and Lázár HL-excluded and unassigned cluster 0 cells. Gastrulation / Early Mesoderm (new) — Tyser et al. 2021 CS7 cell types; all predating cardiac specification.

---

## Section 3: Per-Dataset Details

---

### Dataset 1 — Construction of a human cell landscape at single-cell level

| Field | Value |
| --- | --- |
| **First author & year** | Han et al. (2020) |
| **Journal** | *Nature* |
| **Link** | https://www.nature.com/articles/s41586-020-2157-4 |
| **Assay** | microwell-seq |
| **Source** | CellxGene |
| **Original cells × genes** | 599,926 × 26,069 |
| **Curated cells × genes** | 7,997 × 26,069 (1.3% retained) |
| **Developmental stages** | 11th week post-fertilization stage, 12th week post-fertilization stage |

**Abstract:**
Single-cell analysis is a valuable tool for dissecting cellular heterogeneity in complex systems. However, a comprehensive single-cell atlas has not been achieved for humans. Here we use single-cell mRNA sequencing to determine the cell-type composition of all major human organs and construct a scheme for the human cell landscape (HCL). We have uncovered a single-cell hierarchy for many tissues that have not been well characterized. We established a 'single-cell HCL analysis' pipeline that helps to define human cell identity. Finally, we performed a single-cell comparative analysis of landscapes from human and mouse to identify conserved genetic networks. We found that stem and progenitor cells exhibit strong transcriptomic stochasticity, whereas differentiated cells are more distinct. Our results provide a useful resource for the study of human biology.

**Cell Type × Development Stage Counts:**

| Cell Type | 11th wk pcf | 12th wk pcf | **Total** |
| --- | ---: | ---: | ---: |
| stromal cell | 1,002 | 2,205 | **3,207** |
| ventricular cardiac muscle cell | 925 | 2,071 | **2,996** |
| endothelial cell | 309 | 806 | **1,115** |
| mesenchymal stem cell | 198 | 63 | **261** |
| macrophage | 90 | 22 | **112** |
| smooth muscle cell | 42 | 63 | **105** |
| erythroid lineage cell | 45 | 35 | **80** |
| neuron | 19 | 13 | **32** |
| epithelial cell | 8 | 8 | **16** |
| cell of skeletal muscle | 0 | 15 | **15** |
| T cell | 8 | 3 | **11** |
| professional antigen presenting cell | 9 | 1 | **10** |
| dendritic cell | 6 | 3 | **9** |
| erythroid progenitor cell | 5 | 4 | **9** |
| cord blood hematopoietic stem cell | 4 | 2 | **6** |
| neutrophil | 3 | 2 | **5** |
| fibroblast | 3 | 1 | **4** |
| primordial germ cell | 1 | 2 | **3** |
| monocyte | 1 | 0 | **1** |
| **Total** | **2,678** | **5,319** | **7,997** |

---

### Dataset 2 — Survey of human embryonic development

| Field | Value |
| --- | --- |
| **First author & year** | Cao et al. (2020) |
| **Journal** | *Science* |
| **Link** | https://www.science.org/doi/10.1126/science.aba7721 |
| **Assay** | sci-RNA-seq3 |
| **Source** | CellxGene |
| **Original cells × genes** | 4,062,980 × 45,676 |
| **Curated cells × genes** | 101,749 × 45,676 (2.5% retained) |
| **Developmental stages** | 12th – 17th week post-fertilization stage (5 stages) |

**Abstract:**
Understanding the trajectory of a developing human requires an understanding of how genes are regulated and expressed. Two papers now present a pooled approach using three levels of combinatorial indexing to examine the single-cell gene expression and chromatin landscapes from 15 organs in fetal samples. Cao et al. focus on measurements of RNA in broadly distributed cell types and provide insights into organ specificity. Domcke et al. examined the chromatin accessibility of cells from these organs and identify the regulatory elements that regulate gene expression. Together, these analyses generate comprehensive atlases of early human development. *(from Science editorial introduction)*

**Cell Type × Development Stage Counts:**

| Cell Type | 12th wk pcf | 13th wk pcf | 15th wk pcf | 16th wk pcf | 17th wk pcf | **Total** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cardiac muscle cell | 8,485 | 4,302 | 25,913 | 9,943 | 18,967 | **67,610** |
| stromal cell | 1,453 | 293 | 5,926 | 1,378 | 3,698 | **12,748** |
| endocardial cell | 621 | 308 | 3,938 | 735 | 1,796 | **7,398** |
| endothelial cell of vascular tree | 880 | 168 | 1,962 | 458 | 1,443 | **4,911** |
| smooth muscle cell | 330 | 77 | 766 | 222 | 641 | **2,036** |
| epicardial adipocyte | 111 | 49 | 1,124 | 147 | 460 | **1,891** |
| innate lymphoid cell | 16 | 4 | 726 | 51 | 551 | **1,348** |
| myeloid cell | 57 | 21 | 519 | 67 | 376 | **1,040** |
| endothelial cell of lymphatic vessel | 68 | 44 | 361 | 36 | 139 | **648** |
| dermis microvascular lymphatic vessel endothelial cell | 76 | 36 | 318 | 32 | 141 | **603** |
| Schwann cell | 70 | 18 | 250 | 35 | 162 | **535** |
| megakaryocyte | 38 | 10 | 167 | 36 | 110 | **361** |
| visceromotor neuron | 20 | 14 | 230 | 27 | 57 | **348** |
| ventricular cardiac muscle cell | 9 | 23 | 40 | 31 | 61 | **164** |
| regular atrial cardiac myocyte | 4 | 11 | 34 | 15 | 38 | **102** |
| erythroblast | 0 | 0 | 2 | 0 | 4 | **6** |
| **Total** | **12,238** | **5,378** | **42,276** | **13,213** | **28,644** | **101,749** |

---

### Dataset 3 — Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor

| Field | Value |
| --- | --- |
| **First author & year** | Sim et al. (2021) |
| **Journal** | *Circulation* |
| **Link** | https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.120.051921 |
| **Assay** | 10x 3′ v3 |
| **Source** | CellxGene |
| **Original cells × genes** | 51,176 × 35,477 |
| **Curated cells × genes** | 26,394 × 35,477 (51.6% retained) |
| **Developmental stages** | 19th week post-fertilization stage, 20th week post-fertilization stage |

**Abstract:**
*Background:* Despite in-depth knowledge of the molecular mechanisms controlling embryonic heart development, little is known about the signals governing postnatal maturation of the human heart. *Methods:* Single-nucleus RNA sequencing of 54,140 nuclei from 9 human donors was used to profile transcriptional changes in diverse cardiac cell types during maturation from fetal stages to adulthood. Bulk RNA sequencing and the Assay for Transposase-Accessible Chromatin using sequencing were used to further validate transcriptional changes and to profile alterations in the chromatin accessibility landscape in purified cardiomyocyte nuclei from 21 human donors. Functional validation studies of sex steroids implicated in cardiac maturation were performed in human pluripotent stem cell–derived cardiac organoids and mice. *Results:* Our data identify the progesterone receptor as a key mediator of sex-dependent transcriptional programs during cardiomyocyte maturation. Functional validation studies in human cardiac organoids and mice demonstrate that the progesterone receptor drives sex-specific metabolic programs and maturation of cardiac contractile properties. *Conclusions:* These data provide a blueprint for understanding human heart maturation in both sexes and reveal an important role for the progesterone receptor in human heart development.

**Cell Type × Development Stage Counts:**

| Cell Type | 19th wk pcf | 20th wk pcf | **Total** |
| --- | ---: | ---: | ---: |
| cardiac muscle cell | 14,021 | 5,097 | **19,118** |
| fibroblast | 1,781 | 1,191 | **2,972** |
| endothelial cell | 1,035 | 519 | **1,554** |
| mesothelial cell of epicardium | 987 | 399 | **1,386** |
| leukocyte | 535 | 174 | **709** |
| neuron | 239 | 109 | **348** |
| smooth muscle cell | 74 | 134 | **208** |
| erythrocyte | 75 | 24 | **99** |
| **Total** | **18,747** | **7,647** | **26,394** |

---

### Dataset 4 — Integrated adult and foetal hearts

| Field | Value |
| --- | --- |
| **First author & year** | Knight-Schrijver et al. (2022) |
| **Journal** | *Nature Cardiovascular Research* |
| **Link** | https://www.nature.com/articles/s44161-022-00183-w |
| **Assay** | 10x 3′ v2/v3 |
| **Source** | CellxGene |
| **Original cells × genes** | 60,668 × 26,886 |
| **Curated cells × genes** | 30,889 × 26,886 (50.9% retained) |
| **Developmental stages** | embryonic stage, 10th week post-fertilization stage |

**Abstract:**
Re-activating quiescent adult epicardium represents a potential therapeutic approach for human cardiac regeneration. However, the exact molecular differences between inactive adult and active fetal epicardium are not known. In this study, we combined fetal and adult human hearts using single-cell and single-nuclei RNA sequencing and compared epicardial cells from both stages. We found that a migratory fibroblast-like epicardial population only in the fetal heart and fetal epicardium expressed angiogenic gene programs, whereas the adult epicardium was solely mesothelial and immune responsive. Furthermore, we predicted that adult hearts may still receive fetal epicardial paracrine communication, including WNT signaling with endocardium, reinforcing the validity of regenerative strategies that administer or reactivate epicardial cells in situ. Finally, we explained graft efficacy of our human embryonic stem-cell-derived epicardium model by noting its similarity to human fetal epicardium. Overall, our study defines epicardial programs of regenerative angiogenesis absent in adult hearts, contextualizes animal studies and defines epicardial states required for effective human heart regeneration.

**Cell Type × Development Stage Counts:**

| Cell Type | embryonic stage | 10th wk pcf | **Total** |
| --- | ---: | ---: | ---: |
| unknown | 3,240 | 1,724 | **4,964** |
| fibroblast | 3,584 | 623 | **4,207** |
| myeloid cell | 2,203 | 1,120 | **3,323** |
| smooth muscle cell | 2,356 | 664 | **3,020** |
| cardiac muscle cell | 2,375 | 191 | **2,566** |
| neuron | 1,763 | 251 | **2,014** |
| endocardial cell | 1,451 | 216 | **1,667** |
| innate lymphoid cell | 450 | 1,206 | **1,656** |
| capillary endothelial cell | 935 | 632 | **1,567** |
| fetal cardiomyocyte | 1,137 | 173 | **1,310** |
| pericyte | 893 | 241 | **1,134** |
| endothelial cell | 858 | 246 | **1,104** |
| endothelial cell of artery | 651 | 252 | **903** |
| mesothelial cell of epicardium | 375 | 515 | **890** |
| cardiac mesenchymal cell | 117 | 198 | **315** |
| vein endothelial cell | 168 | 80 | **248** |
| adipocyte | 1 | 0 | **1** |
| **Total** | **22,557** | **8,332** | **30,889** |

---

### Dataset 5 — A cell atlas of the developing human outflow tract of the heart *(Leshem et al. 2025)*

| Field | Value |
| --- | --- |
| **First author & year** | Leshem et al. (2025) |
| **Journal** | *eLife* (Reviewed Preprint) |
| **Link** | https://doi.org/10.7554/eLife.107748 |
| **Assay** | 10x 3′ v2/v3 (snRNA-seq) |
| **Source** | CellxGene |
| **Original cells × genes** | 30,125 × 31,008 |
| **Curated cells × genes** | 24,695 × 31,008 (82.0% retained) |
| **Developmental stages** | 6th week post-fertilization stage (CS16-17 embryonic), 13th week post-fertilization stage (12 pcw fetal) |

*Note: The same publication also includes four Visium spatial transcriptomics slides (not single-cell resolution) and adult aortic valve nuclei; neither are included here.*

**Abstract:**
The outflow tract (OFT) of the heart carries blood away from the heart into the great arteries. During embryogenesis, the OFT divides to form the aorta and pulmonary trunk, creating the double circulation present in mammals. Defects in this area account for one-third of all congenital heart disease cases. Here, we present comprehensive transcriptomic data on the developing OFT at two distinct timepoints (embryonic and fetal) and its adult derivatives, the aortic valves, and use spatial transcriptomics to define the distribution of cell populations. We uncover that distinctive embryonic signatures persist in adult cells and can be used as labels to retrospectively attribute relationships between cells separated by a large time scale. Single-cell regulatory network inference identifies GATA6, a transcription factor linked to common arterial trunk and bicuspid aortic valve, as a key regulator of valve precursor cells. Its downstream network reveals candidate drivers of human cardiac defects and illuminates the molecular mechanisms of both normal and pathological valve development. Our findings define the cellular and molecular signatures of the human OFT and its distinct cell lineages, which is critical for understanding congenital heart defects and developing cardiac tissue for regenerative medicine.

**Cell Type × Development Stage Counts:**

| Cell Type | 6th wk pcf | 13th wk pcf | **Total** |
| --- | ---: | ---: | ---: |
| cardiac mesenchymal cell | 2,556 | 7,015 | **9,571** |
| cardiac muscle cell | 3,149 | 5,956 | **9,105** |
| endothelial cell | 1,572 | 3,315 | **4,887** |
| neural cell | 0 | 803 | **803** |
| hematopoietic cell | 2 | 324 | **326** |
| valve interstitial cell | 0 | 3 | **3** |
| **Total** | **7,279** | **17,416** | **24,695** |

---

### Dataset 6 — Spatiotemporal gene expression and cellular dynamics of the developing human heart *(Lázár et al. 2025)*

| Field | Value |
| --- | --- |
| **First author & year** | Lázár et al. (2025) |
| **Journal** | *Nature Genetics* |
| **Link** | https://www.nature.com/articles/s41588-025-02352-6 |
| **Assay** | 10x Chromium v2/v3 scRNA-seq *(SC libraries only; paper also includes Visium spatial transcriptomics and ISS — not used here)* |
| **Source** | Mendeley Data |
| **Cells × genes** | 107,673 × 59,480 *(from 21 10x Chromium libraries; no subsetting applied)* |
| **Developmental stages** | 11 time points: 5.5, 6.0, 7.0, 8.0, 8.5, 9.0, 10.0, 11.5, 12.0, 13.2, 14.0 pcw |
| **Reference genome** | GRCh38 |

**Abstract** *(from Nature Genetics 2025)*:
Heart development relies on topologically orchestrated cellular transitions and interactions, many of which remain poorly characterized in humans. Here, we combined unbiased spatial and single-cell transcriptomics with imaging-based validation across postconceptional weeks 5.5 to 14 to uncover the molecular landscape of human early cardiogenesis. We present a high-resolution transcriptomic map of the developing human heart, revealing the spatial arrangements of 31 coarse-grained and 72 fine-grained cell states organized into distinct spatial and temporal domains.

**Cell Type × Development Stage Counts:** *(see Section 2)*

The complete HL cell type × stage table for this dataset is provided in **Section 2** above. The Lázár et al. atlas additionally defines a detailed-level (DL) sub-clustering of 72 fine-grained states across four lineages:

| Lineage | DL clusters | Key cell states |
| --- | ---: | --- |
| Cardiomyocyte (CM) | 26 subtypes | Mature vCM/aCM, Proliferating CM, Immature CM, SAN, AVN, AVB-Bundle Branch, Purkinje |
| Fibroblast / Mesenchymal (FB) | 22 subtypes | Interstitial FB, OFT FB, Valve MC, EPDC, Pericardial MC, Annulus Fibrosus FB, VIC, FAP |
| Endothelial (EN) | 22 subtypes | Endocardial EC, Capillary EC, Arterial EC, Venous EC, Arteriolar EC, Lymphatic EC |
| Innate / Neural (IN) | 19 subtypes | Schwann cell precursors (SCP 1–5), Autonomic neurons, Chromaffin cells, Myelinating SC |

---

### Dataset 7 — Single-cell transcriptomic characterization of a gastrulating human embryo *(Tyser et al. 2021)*

| Field | Value |
| --- | --- |
| **First author & year** | Tyser et al. (2021) |
| **Journal** | *Nature* |
| **Link** | https://www.nature.com/articles/s41586-021-04158-y |
| **Assay** | Smart-seq2 (plate-based scRNA-seq) |
| **Source** | EMBL-EBI (E-MTAB-9388); lab copy at `/gladstone/theodoris/lab/ctheodoris/validation/gastrulation` |
| **Original cells × genes** | 1,195 × 40,614 |
| **Curated cells × genes** | 1,195 × 40,614 (100% retained; dataset is pre-curated, all cells pass filter) |
| **Developmental stage** | Carnegie Stage 7 (~Day 16–19; gastrulation, pre-cardiac specification) |
| **Donors** | 1 IVF embryo |

**Abstract:**
Single-cell RNA sequencing of a gastrulating human embryo at Carnegie Stage 7 (approximately 16–19 days post-fertilization) reveals the transcriptional landscape of epiblast, primitive streak, and nascent germ layer cells. Eleven cell populations are identified — including emergent, nascent, and advanced mesoderm; endoderm; ectoderm; axial mesoderm; yolk-sac mesoderm; hemogenic endothelial progenitors; and erythrocytes — providing a reference for the earliest stages of human cardiac and hematopoietic progenitor specification.

**Cell Type × Development Stage Counts:**

| Cell Type | CS7 (~Day 17) | **Total** |
| --- | ---: | ---: |
| primitive streak | 202 | **202** |
| emergent mesoderm | 185 | **185** |
| advanced mesoderm | 164 | **164** |
| endodermal cell | 135 | **135** |
| epiblast cell | 133 | **133** |
| hemogenic endothelial progenitor | 111 | **111** |
| nascent mesoderm | 98 | **98** |
| yolk sac mesoderm | 83 | **83** |
| erythrocyte | 32 | **32** |
| ectodermal cell | 29 | **29** |
| axial mesoderm | 23 | **23** |
| **Total** | **1,195** | **1,195** |


---

### Dataset 8 — A single-cell transcriptome atlas profiles early organogenesis in human embryos *(Xu et al. 2023)*

| Field | Value |
| --- | --- |
| **First author & year** | Xu et al. (2023) |
| **Journal** | *Nature Cell Biology* |
| **Link** | https://www.nature.com/articles/s41556-023-01108-w |
| **Assay** | 10x Chromium scRNA-seq (multi-region dissection; 7 embryos, 23 samples) |
| **Source** | Lab directory (David Wen; `/gladstone/theodoris/lab/dwen/data/organogenesis_data/organogenesis/`) |
| **Original cells × genes** | 185,140 × 32,351 (full whole-embryo atlas) |
| **Curated cells × genes** | 5,243 × 32,351 (2.8% retained; cardiac subset only) |
| **Developmental stages** | CS12 (~Day 26–28), CS13-14 (~Day 28–33), CS15-16 (~Day 33–40) |
| **Donors** | 7 embryos (emb1–emb7) |
| **Reference genome** | — (not stated in available metadata) |

*Note: The full atlas covers 185,140 cells across 18–19 developmental systems (313 clusters). Only cardiac-relevant cells are included here — filtered to `splanchnic_LPM` system cardiac annotations and `endothelium` system endocardial annotations (see Section 1 notes for filter criteria). The dataset also includes spatial transcriptomics on embryonic sections; spatial data are excluded.*

**Abstract:**
The early window of human embryogenesis is largely a black box for developmental biologists. Here we probed the cellular diversity of 4-6 week human embryos when essentially all organs are just laid out. On the basis of over 180,000 single-cell transcriptomes, we generated a comprehensive atlas of 313 clusters in 18 developmental systems, which were annotated with a collection of ontology and markers from 157 publications. Together with spatial transcriptome on embryonic sections, we characterized the molecule and spatial architecture of previously unappreciated cell types. Combined with data from other vertebrates, the rich information shed light on spatial patterning of axes, systemic temporal regulation of developmental progression and potential human-specific regulation. Our study provides a compendium of early progenitor cells of human organs, which can serve as the root of lineage analysis in organogenesis.

**Cell Type × Development Stage Counts (curated cardiac subset):**

| Cell Type | CS12 | CS13-14 | CS15-16 | **Total** |
| --- | ---: | ---: | ---: | ---: |
| endocardium | 20 | 417 | 583 | **1,020** |
| ventricle cardiomyocyte | 260 | 281 | 431 | **972** |
| epicardial derived cell | 6 | 131 | 648 | **785** |
| atria cardiomyocyte | 137 | 163 | 295 | **595** |
| endocardial derived cell | 23 | 254 | 226 | **503** |
| Second heart field (SHF) | 75 | 169 | 129 | **373** |
| cardiomyocyte | 99 | 88 | 176 | **363** |
| atrioventricular canal | 22 | 68 | 168 | **258** |
| epicardium | 15 | 142 | 95 | **252** |
| sinoatrial node (SAN) | 14 | 26 | 65 | **105** |
| pericyte (myocardium) | 0 | 0 | 17 | **17** |
| **Total** | **671** | **1,739** | **2,833** | **5,243** |
