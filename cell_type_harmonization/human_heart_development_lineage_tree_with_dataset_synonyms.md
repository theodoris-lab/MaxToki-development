# Human Heart Development — Cell Type Harmonization Reference

This document maps canonical human cardiac developmental cell types to the exact labels used in each constituent dataset. It serves as the harmonization reference for the MaxToki training data build and covers cell types observed across four sources spanning **embryonic day 7 through post-natal week 40**.

## Datasets

| Dataset | Coverage | Technology | Cells |
|---|---|---|---|
| **CXG** — CellxGene Heart Development Subset | PCW 5–40 | 10x Chromium (multiple studies) | ~350,000 |
| **Tyser** — Tyser et al. 2021 | Day 7–CS7 (~PCW 3) | scRNA-seq (Smart-seq2) | ~1,300 |
| **Xu** — Xu et al. 2024 | PCW 5–25 | 10x Chromium | ~65,000 |
| **Lázár** — Lázár et al. 2025 | PCW 5.5–14 | 10x Chromium | ~77,000 |

## Table Structure

Each row represents a **canonical cell type** placed on the human heart developmental lineage. Columns show the exact label(s) used in each dataset, followed by cell counts in parentheses.

- **Canonical Name** — the harmonized cell type identity used in MaxToki
- **PCW** — developmental window across all datasets combined
- **Total Cells** — sum of cells across CXG + Tyser + Xu + Lázár (HL only; see below)
- **CXG / Tyser / Xu** — exact `cell_type` / `cluster` / `annotation` labels from each dataset
- **Lázár (HL)** — Heart-Lung Atlas tier labels (35 coarse clusters); these drive the Lázár cell count in Total Cells
- **Lázár (DL)** — Deep Learning sub-atlas tier labels (74 fine-grained clusters); shown for reference and cross-mapping — these annotate the **same cells** at higher resolution and are **not added to Total Cells** to avoid double-counting, except for rows where no HL entry exists

Cell types that could not be placed on the lineage tree are listed in the unmapped section at the bottom.

---

## Dataset Synonyms

Cell types observed in our datasets, with the exact label used in each source paper.

---

### Cardiomyocyte Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Epiblast** | Day 7–14 | 133 | — | epiblast cell (133) | — | — | — |
| **Primitive Streak** | Day 14–16 | 202 | — | primitive streak (202) | — | — | — |
| **Mesoderm** | PCW 2–3 | 553 | — | advanced mesoderm (164), axial mesoderm (23), emergent mesoderm (185), nascent mesoderm (98), yolk sac mesoderm (83) | — | — | — |
| **Cardiogenic Mesoderm** | PCW 2–3 | 373 | — | — | Second heart field (SHF) (373) | — | — |
| **Cardiac Muscle Cell** | PCW 2–20 | 134,390 | cardiac muscle cell (121,959), fetal cardiomyocyte (1,310) | — | cardiomyocyte (363) | Immature Cardiomyocyte (Immat\_CM) (1,285), Proliferating Cardiomyocyte (Prol\_CM) (7,475), High TMSB10 Cluster 1 (TMSB10high\_C\_1) (1,998) | Immature Cardiomyocyte 1 (Immat\_CM\_1) (2,894), Immature Cardiomyocyte 2 (Immat\_CM\_2) (2,179), Immature Cardiomyocyte 3 (Immat\_CM\_3) (1,993), Proliferating Cardiomyocyte 1 (Prol\_CM\_1) (619), Proliferating Cardiomyocyte 2 (Prol\_CM\_2) (808) |
| **Ventricular Cardiomyocytes** | PCW 3–40 | 23,880 | ventricular cardiac muscle cell (3,203) | — | ventricle cardiomyocyte (972) | Mature Ventricular Cardiomyocyte (Mat\_vCM) (7,533), Metabolically Active Ventricular Cardiomyocyte 1 (MetAct\_vCM\_1) (3,857), Metabolically Active Ventricular Cardiomyocyte 2 (MetAct\_vCM\_2) (8,315) | Ventricular Cardiomyocyte 1 (vCM\_1) (349), Ventricular Cardiomyocyte 2 (vCM\_2) (535), Ventricular Cardiomyocyte 3 (vCM\_3) (277), Ventricular Cardiomyocyte 4 (vCM\_4) (1,552), Ventricular Cardiomyocyte 5 (vCM\_5) (1,955), Ventricular Cardiomyocyte 6 (vCM\_6) (2,085) |
| **Regular Atrial Cardiac Myocyte** | PCW 3–40 | 5,238 | regular atrial cardiac myocyte (121) | — | atria cardiomyocyte (595) | Mature Atrial Cardiomyocyte (Mat\_aCM) (1,201), Metabolically Active Atrial Cardiomyocyte (MetAct\_aCM) (3,321) | Left Atrial Cardiomyocyte (Left\_aCM) (823), Right Atrial Cardiomyocyte (Right\_aCM) (1,635), Conducting Atrial Cardiomyocyte (Cond\_aCM) (1,319) |
| **SA Node Pacemaker Cell** | PCW 10–40 | 1,448 | — | — | sinoatrial node (SAN) (105) | — | SA Node Cardiomyocyte (SAN\_CM) (299), AV Node Cardiomyocyte (AVN\_CM) (147), AV Bundle / Bundle Branch Cardiomyocyte (AVB-BB\_CM) (164), Transitional / Stellate Purkinje Fiber Cardiomyocyte (TsPF\_CM) (454), Purkinje Fiber Cardiomyocyte (PF\_CM) (279) |

---

### Endocardial / Valve Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Endocardial Cell** | PCW 5–40 | 18,946 | endocardial cell (10,932) | — | endocardium (1,020) | Endocardial Endothelial Cell (Endoc\_EC) (6,994) | Endocardial Endothelial Cell 1 (Endoc\_EC\_1) (2,310), Endocardial Endothelial Cell 2 (Endoc\_EC\_2) (778), Endocardial Endothelial Cell 3 (Endoc\_EC\_3) (1,363), Endocardial Endothelial Cell 4 (Endoc\_EC\_4) (621), Proliferating Endothelial Cell (Prol\_EC) (301) |
| **Atrial Septum Endothelial Cell** | PCW 8–40 | 195 | — | — | — | — | Atrial Septum Endothelial Cell (AtrSept\_EC) (195) |
| **AV Canal Endocardial Cells** | PCW 4–5 | 258 | — | — | atrioventricular canal (258) | — | — |
| **Inflow Valve Endothelial Cells** | PCW 5–40 | 357 | — | — | — | — | Inflow Valve Endothelial Cell (IF\_VEC) (357) |
| **Endocardial Cushion** | PCW 5–6 | 807 | — | — | endocardial derived cell (503) | Endocardial Cushion Endothelial Cell (EndocCush\_EC) (304) | — |
| **Valve Mesenchymal Cells** | PCW 6–8 | 3,206 | — | — | — | Valve Mesenchymal Cell (Valve\_MC) (3,206) | Valve Mesenchymal Cell 1 (Valve\_MC\_1) (961), Valve Mesenchymal Cell 2 (Valve\_MC\_2) (1,540) |
| **Valve Interstitial Cell** | PCW 7–40 | 1,363 | valve interstitial cell (3) | — | — | — | Valve Interstitial Cell (VIC) (1,360) |
| **Outflow Valve Endothelial Cells** | PCW 5–40 | 213 | — | — | — | — | Outflow Valve Endothelial Cell (OF\_VEC) (213) |

---

### Mesenchymal and Stromal Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Cardiac Mesenchymal Cell** | PCW 5–10 | 12,228 | cardiac mesenchymal cell (12,228) | — | — | — | — |
| **Stromal Cell** | PCW 10–40 | 19,106 | stromal cell (19,106) | — | — | — | — |
| **Mesenchymal Stem Cell** | PCW 5–10 | 261 | mesenchymal stem cell (261) | — | — | — | — |
| **Fibroblast** | PCW 10–40 | 28,967 | — | — | — | Annulus Fibrosus Fibroblast (AnnFibr\_FB) (1,345), Interstitial Fibroblast (Int\_FB) (14,154), Outflow Tract Fibroblast (OFT\_FB) (12,581), PDE4Chigh Fibroblast (PDE4Chigh\_FB) (563), Proliferating Fibroblast (Prol\_FB) (324) | Adventitial Fibroblast 1 (Adv\_FB\_1) (2,129), Adventitial Fibroblast 2 (Adv\_FB\_2) (918), Interstitial Fibroblast 1 (Int\_FB\_1) (2,463), Interstitial Fibroblast 2 (Int\_FB\_2) (1,612), Interstitial Fibroblast 3 (Int\_FB\_3) (257), Proliferating Fibroblast 1 (Prol\_FB\_1) (479), Proliferating Fibroblast 2 (Prol\_FB\_2) (740), Annulus Fibrosus Fibroblast (AnnFibr\_FB^fg) (638), PDE4Chigh Fibroblast (PDE4Chigh\_FB^fg) (696), CALN1-High Fibroblast (CALN1high\_FB) (586), Inflammatory Fibroblast (Infl\_FB) (1,150), Fibroblast Activation Protein+ Cell (FAP) (634) |

---

### Hematopoietic Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Hematopoietic Cell** | PCW 3–40 | 884 | hematopoietic cell (328), cord blood hematopoietic stem cell (6), megakaryocyte (439) | hemogenic endothelial progenitor (111) | — | — | — |
| **Myeloid Cell** | PCW 4–40 | 6,637 | myeloid cell (4,621) | — | — | Myeloid Cell (MyC) (2,016) | — |
| **Monocyte** | PCW 6–40 | 1 | monocyte (1) | — | — | — | — |
| **Macrophage** | PCW 8–40 | 112 | macrophage (112) | — | — | — | — |
| **Neutrophil** | PCW 10–40 | 5 | neutrophil (5) | — | — | — | — |
| **Dendritic Cell** | PCW 8–40 | 9 | dendritic cell (9) | — | — | — | — |
| **Professional Antigen Presenting Cell** | PCW 8–40 | 10 | professional antigen presenting cell (10) | — | — | — | — |
| **Leukocyte** | PCW 6–40 | 709 | leukocyte (709) | — | — | — | — |
| **Innate Lymphoid Cell** | PCW 8–40 | 4,000 | innate lymphoid cell (3,333) | — | — | Lymphoid Cell (LyC) (667) | — |
| **T Cell** | PCW 10–40 | 11 | T cell (11) | — | — | — | — |
| **Erythroid Progenitor Cell** | PCW 4–10 | 9 | erythroid progenitor cell (9) | — | — | — | — |
| **Erythroblast** | PCW 6–20 | 7 | erythroblast (7) | — | — | — | — |
| **Erythroid Lineage Cell** | — | 80 | erythroid lineage cell (80) | — | — | — | — |
| **Erythrocyte** | PCW 8–40 | 131 | erythrocyte (99) | erythrocyte (CS7) (32) | — | — | — |

---

### Epicardial / Vascular Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Mesothelial Cell of Epicardium** | PCW 8–40 | 3,452 | mesothelial cell of epicardium (2,276) | — | epicardium (252) | Epicardial Cell (EpC) (924) | — |
| **Epicardium Derived Cell** | PCW 6–10 | 2,741 | — | — | epicardial derived cell (785) | Epicardium-Derived Cell (EPDC) (1,956) | Epicardium-Derived Cell 1 (EPDC\_1) (552), Epicardium-Derived Cell 2 (EPDC\_2) (1,697) |
| **Cardiac Fibroblast** | PCW 10–40 | 7,183 | fibroblast (7,183) | — | — | — | — |
| **Vascular Smooth Muscle Cell** | PCW 10–40 | 9,430 | smooth muscle cell (5,859) | — | — | Coronary Artery Smooth Muscle Cell (CA\_SMC) (3,571) | — |
| **Pericyte** | PCW 10–40 | 1,901 | pericyte (1,134) | — | pericyte (myocardium) (17) | Pericyte (PC) (501), Pericyte-like Mesenchymal Cell / Pericyte (Peric\_MC) (249) | Pericyte-like Mesenchymal Cell (Peric\_MC^fg) (1,431) |
| **Adipocyte** | PCW 20–40 | 1 | adipocyte (1) | — | — | — | — |
| **Epicardial Adipocyte** | PCW 20–40 | 2,358 | epicardial adipocyte (2,358) | — | — | — | — |
| **Vascular Endothelial Cell** | PCW 8–40 | 17,486 | endothelial cell (9,030), endothelial cell of vascular tree (6,100) | — | — | PDE4Chigh Endothelial Cell (PDE4Chigh\_EC) (1,658), High TMSB10 Cluster 2 (TMSB10high\_C\_2) (698) | PDE4Chigh Endothelial Cell (PDE4Chigh\_EC^fg) (769), High TMSB10 Endothelial Cell (TMSB10high\_C\_2^fg) (747) |
| **Capillary Endothelial Cell** | PCW 8–40 | 6,120 | capillary endothelial cell (1,567) | — | — | Microvascular Endothelial Cell (MicroVasc\_EC) (4,553) | Capillary Endothelial Cell 1 (Cap\_EC\_1) (1,458), Capillary Endothelial Cell 2 (Cap\_EC\_2) (2,859) |
| **Arterial Endothelial Cell** | PCW 10–40 | 3,023 | endothelial cell of artery (903) | — | — | Macrovascular Endothelial Cell (MacroVasc\_EC) (2,120) | Arteriolar Endothelial Cell (Arteriol\_EC) (1,006), Arterial Endothelial Cell 1 (Art\_EC\_1) (269), Arterial Endothelial Cell 2 (Art\_EC\_2) (525) |
| **Venous Endothelial Cell** | PCW 10–40 | 547 | vein endothelial cell (248) | — | — | — | Venous Endothelial Cell (Ven\_EC) (166), Venular Endothelial Cell (Venul\_EC) (133) |
| **Lymphatic Endothelial Cell** | PCW 10–40 | 1,264 | endothelial cell of lymphatic vessel (820) | — | — | Lymphatic Endothelial Cell (LEC) (444) | Lymphatic Endothelial Cell (LEC^fg) (403) |
| **Dermis Microvascular Lymphatic Endothelial Cell** | PCW 10–40 | 742 | dermis microvascular lymphatic vessel endothelial cell (742) | — | — | — | — |

---

### Neural / Ectoderm Lineage

| Canonical Name | PCW | Total Cells | CXG | Tyser | Xu | Lázár (HL) | Lázár (DL) |
|---|---|---|---|---|---|---|---|
| **Ectoderm** | PCW 2–3 | 29 | — | ectodermal cell (29) | — | — | — |
| **Neural Cell** | PCW 3–40 | 1,000 | neural cell (1,000) | — | — | — | — |
| **Neuron** | PCW 6–40 | 2,756 | neuron (2,394) | — | — | Neuroblast-Neuron (NB-N) (362) | Autonomic Neuron 1 (Aut\_Neu\_1) (145), Autonomic Neuron 2 (Aut\_Neu\_2) (69), Chromaffin Cell (Chrom\_C) (41) |
| **Visceromotor Neuron** | PCW 8–40 | 439 | visceromotor neuron (439) | — | — | — | — |
| **Schwann Cell** | PCW 8–40 | 1,413 | Schwann cell (669) | — | — | Schwann Cell Precursor / Glia Cell (SCP-GC) (744) | Schwann Cell Precursor 1 (SCP\_1) (168), Schwann Cell Precursor 2 (SCP\_2) (80), Schwann Cell Precursor 3 (SCP\_3) (38), Schwann Cell Precursor 4 (SCP\_4) (72), Schwann Cell Precursor 5 (SCP\_5) (195), Myelinating Schwann Cell (My\_SC) (28), Bridge State (Bridge\_state) (34) |
| **Outflow Tract Smooth Muscle Cell** | PCW 8–40 | 3,507 | — | — | — | Outflow Tract Smooth Muscle Cell (OFT\_SMC) (3,507) | — |

---

## Cell Types That Could Not Be Placed on the Lineage Tree

### Non-cardiac / out-of-scope lineages
Biologically real but outside the cardiac developmental tree:

| Label | Source |
|---|---|
| cell of skeletal muscle | CXG |
| primordial germ cell | CXG |
| endodermal cell (135) | Tyser |

### Too generic to place at a specific node

| Label | Source |
|---|---|
| epithelial cell | CXG |

### Unannotated / computationally excluded clusters
No biological identity — cannot be mapped:

| Label | Source |
|---|---|
| Heart-Lung Atlas Excluded 1 (HL\_excl\_1) | Lázár |
| Heart-Lung Atlas Excluded 2 (HL\_excl\_2) | Lázár |
| Heart-Lung Atlas Excluded 3 (HL\_excl\_3) (392) | Lázár |
| Heart-Lung Atlas Excluded 4 (HL\_excl\_4) (276) | Lázár |
| unassigned (cluster 0) | Lázár |
| unknown | CXG |
