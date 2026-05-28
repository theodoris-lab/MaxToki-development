# Train / Val / Test Split Rationale — MaxToki Heart Development Finetuning

**Last updated:** 2025-05  
**Author:** E. Niyonkuru  
**Context:** Fine-tuning the MaxToki developmental model on human cardiac single-cell RNA-seq data  
aggregated from four datasets (CXG cohort, Lázár et al. 2025, Xu et al. 2023, Tyser et al. 2021).

---

## 1. Summary of the Finalized Split

| Role | PCW / timepoints | Datasets present | Rationale |
|------|-----------------|-----------------|-----------|
| **Train** | 3, 4, 4.5, 5, 5.5, 6, 8, 9, 10.5, 11, 12, 13, 15, 16, 17, 19 | CXG, Lázár (w6–w12), Xu (CS12–CS15-16), Tyser | Largest portion; broad temporal coverage from gastrulation to mid-fetal |
| **Val** | **PCW 10, PCW 20** | PCW 10: CXG + Lázár; PCW 20: CXG only | Monitors training; selected for data richness and temporal spacing |
| **Test** | **PCW 7** | Lázár only | Held out entirely; interpolated (between PCW 6 and PCW 8 train points) |
| **Lineage holdout** | All PCW | Epicardial / EPDC, Vascular EC | Withheld entirely to assess cell-identity generalisation |

---

## 2. Why Two Complementary Holdout Strategies?

A temporal-only split (holding out specific timepoints) tests whether the model learns  
**developmental trajectory** — i.e., can it interpolate or extrapolate along the time axis?

A lineage-only split (holding out specific cell types at all timepoints) tests whether  
the model has learned **cell-type identity** — i.e., does the latent representation capture  
biology beyond the cell types it was trained on?

Using both simultaneously is more stringent:

> *Temporal holdout alone* — the model sees all cell types at adjacent time points; it may  
> pass without truly encoding cell identity.  
> *Lineage holdout alone* — the model sees the same cell types at all other ages; it may  
> pass without truly encoding developmental dynamics.  
> *Both together* — the model must generalise across time **and** cell identity, a more  
> faithful test of whether it has learned cardiac developmental biology.

---

## 3. Temporal Split — Detailed Rationale

### 3.1 Validation: PCW 10 and PCW 20

**PCW 10** is the richest dual-dataset time point in the collection. CXG contributes broad  
cell-type coverage while Lázár contributes 18 annotated cluster labels (e.g. LV_C, RV_C,  
SCV, A_EP, V_EP, EN, VE, LCV, FB, SM, PE, Mac, BC, PC, NC, Peri, Mast, NK). This overlap  
makes PCW 10 the best-powered point for monitoring training stability and catching overfitting  
to a single dataset's label scheme.

**PCW 20** represents mid-fetal development, a stage where CXG provides broad cardiomyocyte  
and stromal coverage but no Lázár data exist. Including it in validation ensures the model is  
evaluated at an underrepresented late-stage timepoint, complementing the early-stage richness  
of PCW 10.

Together, PCW 10 (peak multi-dataset) and PCW 20 (CXG-only mid-fetal) provide complementary  
views of model performance without being redundant.

### 3.2 Test: PCW 7

**PCW 7** is held as the primary test point for the following reasons:

1. **True interpolation** — PCW 7 lies between PCW 6 (train) and PCW 8 (train), so the model  
   must interpolate rather than merely extrapolate. A held-out early (PCW ≤ 5) or late  
   (PCW ≥ 25) point would test extrapolation and would be harder to interpret.

2. **Lázár-only** — unlike PCW 10, PCW 7 exists only in Lázár et al., so the test set draws  
   from a different sample preparation and annotation framework than the dominant CXG training  
   data. This tests cross-dataset generalisation as well as temporal generalisation.

3. **Anatomically meaningful boundary** — PCW 7 corresponds to the cardiac jelly / trabeculation  
   stage, just after the CXG PCW 6 timepoint that captures the very earliest committed CMs.  
   Testing here asks whether the model distinguishes nascent vs. maturing ventricular CMs.

### 3.3 Future Test / Val Candidates (not yet in dataset)

When data are acquired for PCW 25, 30, and 33:
- **PCW 25** → additional test (early post-birth transition)
- **PCW 30** → additional val (expanded mid-fetal monitoring)
- **PCW 33** → additional test (late fetal / near-term)

These are marked in both HTML visualisations as "future-test" / "future-val" with lighter  
column highlights.

---

## 4. Lineage Holdout — Detailed Rationale

### 4.1 Epicardial / EPDC

**What it covers (50 canonical types, ~9 rows):**  
Proepicardium, epicardium (atrial/ventricular), epicardial-derived cells undergoing  
epithelial-to-mesenchymal transition (EMT), EPDC-derived pericytes, EPDC-derived  
cardiac fibroblasts.

**Why this lineage?**

- **Distinct developmental origin** — the epicardial lineage arises from the proepicardial  
  organ, a mesothelial structure separate from the primary/secondary heart field. Its  
  transcriptomic signature (e.g. *WT1*, *TBX18*, *ALDH1A2*, *TCF21*) is biologically  
  distinct from cardiomyocytes and endocardial cells.
- **EMT complexity** — epicardial EMT produces multiple downstream fates (pericytes, SMC,  
  fibroblasts), making this lineage an internal test of whether the model correctly tracks  
  fate diversification, not just broad cell-class identity.
- **Multi-dataset coverage** — Epicardial/EPDC cells are present across all four datasets  
  (CXG PCW 5.5–20, Lázár A_EP/V_EP PCW 6–12, Xu epicardium/EPDC/pericyte CS12–CS15-16),  
  so withheld cells span the full temporal range and multiple independent annotations.
- **Cardiac relevance** — unlike purely non-cardiac holdouts, epicardial cells are heart-intrinsic  
  and clinically important (epicardial reactivation after MI). A model that fails here is  
  uninformative in a specific, medically interpretable way.

### 4.2 Vascular Endothelial Cells (Vascular EC)

**What it covers:**  
Arterial EC, capillary EC, venous EC, lymphatic EC, angioblasts.

**Why this lineage?**

- **Distinct angiogenic program** — vascular ECs arise via splanchnic lateral plate mesoderm  
  → angioblast → vasculogenesis. Their signature (*PECAM1*, *CDH5*, *KDR*, *PROX1* for  
  lymphatics) is clearly distinct from cardiomyocytes and epicardial cells.
- **Sub-type diversity** — arterial vs. venous vs. lymphatic EC identity is driven by  
  Notch/VEGF gradients, not simply by stage. Testing whether the model recovers these  
  EC subtypes without ever seeing them during training is a strong generalisation probe.
- **Multi-dataset annotation** — Lázár annotates EN (endocardial), VE (vascular EC), and  
  LCV (lymphatic/capillary vasculature) distinctly. CXG and Xu also annotate vascular ECs.  
  Together they provide multi-source, multi-stage representation of this lineage at test time.
- **Not trivially easy** — unlike immune or neural cells (which would be easy holdouts because  
  they are transcriptomically far from cardiac cells), vascular ECs co-occupy the heart and  
  share some mesodermal signals with ECs in other datasets. Passing this test is non-trivial.

### 4.3 Why NOT Neural or Immune as holdouts?

**Immune cells** (*PTPRC*+, *CD3D*+, macrophages, mast cells) are transcriptomically very  
distant from cardiomyocytes. The model would almost certainly fail to represent them (or  
trivially succeed because they are so distinct), making this holdout uninformative for the  
cardiac biology question.

**Neural cells** (cardiac neurons, neural crest, Schwann cells) are similarly distant from  
the dominant cardiac cell types. Holding out something completely off-target provides no  
signal about whether the model is learning cardiac development specifically.

**Epicardial / EPDC and Vascular EC** are the right choices because:
1. They are cardiac-resident.
2. They are transcriptomically intermediate (not easy, not impossible to reconstruct from context).
3. They have clear biological interpretations for pass / fail outcomes.

---

## 5. Visualisation Files

| File | Contents |
|------|---------|
| `cell_type_harmonization/train_val_test_coverage.html` | SVG dot-plot, all 4 datasets × PCW × 50 cell types; split annotations and lineage holdout stripe overlay |
| `cell_type_harmonization/lineage_tree_author_labels.html` | Lineage tree × PCW; author labels by dataset; holdout sections marked with ⊗ badge and diagonal stripe |
| `cell_type_harmonization/train_val_test_coverage_lineage_explorer.html` | Split-pane: collapsible lineage tree sidebar + full dot-plot; click to highlight rows |

---

## 6. Implementation

The split annotation and holdout set are encoded in two scripts:

- `scripts/plot_train_val_test_coverage.py` — `SPLIT_ANNOTATION` dict (PCW key → role) and  
  `LINEAGE_HOLDOUTS` set.
- `scripts/plot_lineage_tree_author_labels.py` — `PCW_COLS` list (PCW key, label, dataset, role)  
  and `LINEAGE_HOLDOUTS` set.

Both scripts re-generate their HTML from source data on each run. No manual edits to the  
output HTML are needed.
