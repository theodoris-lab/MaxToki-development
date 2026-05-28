# Cell Type Harmonization Decisions

Reference tree: `documents/human_heart_development_lineage_tree_with_dataset_synonyms_v2.txt`  
Map file: `cell_type_harmonization/cell_type_harmonization_map.json`  
Apply script: `developmental_finetuning/heart_dev_finetune/src/prepare_heart_dev_finetune_data.py`

---

## Case Sensitivity

**Decision**: Alias lookup is performed case-insensitively (both keys and query strings are lowercased before comparison).

**Rationale**: CXG CL ontology labels use all-lowercase (e.g., `cardiac muscle cell`, `stromal cell`), while most canonical names in the map are Title Case. Making the lookup case-insensitive recovers ~180,000+ CXG cells that would otherwise be dropped due to a simple capitalisation mismatch.

---

## Time Parsing

### `"embryonic stage"` (and variants)

**Decision**: Assign **PCW 5.5** to cells annotated with `"embryonic stage"`, `"embryonic human stage"`, or `"human embryonic stage"`.

**Rationale**: This vague UBERON/HsapDv ontology term appears on ~22,557 CXG cells and provides no specific week. The human embryonic period spans PCW 3–8; PCW 5.5 is the midpoint and falls within the period of active cardiac morphogenesis (Carnegie stages 13–15, approximately PCW 5–6). Cells at this stage are likely early progenitors. Assigning PCW 5.5 allows them to contribute to early-stage trajectories rather than being discarded.

**Impact**: ~22,557 additional CXG cells (subject to passing cell-type and other filters).

---

## Cell Type Aliases

### CXG CL Ontology → Canonical Mappings

All CXG cell types use lowercase CL ontology labels. The following mappings were added to `lineage_tree_aliases` (case-insensitive matching handles most of these automatically; explicit aliases are listed for non-obvious cases):

| CXG Label | Count | Canonical Name | Notes |
|---|---|---|---|
| `cardiac muscle cell` | 121,959 | Cardiac Muscle Cell | Case-insensitive match |
| `stromal cell` | 19,106 | Stromal Cell | Case-insensitive match |
| `cardiac mesenchymal cell` | 12,228 | Cardiac Mesenchymal Cell | Case-insensitive match |
| `endocardial cell` | 10,932 | Endocardial Cell | Case-insensitive match |
| `endothelial cell` | 9,030 | Vascular Endothelial Cell | Explicit alias; generic EC → parent vascular EC node |
| `fibroblast` | 7,183 | Cardiac Fibroblast | Explicit lowercase alias (already in original map) |
| `endothelial cell of vascular tree` | 6,100 | Vascular Endothelial Cell | Already mapped (lowercase) |
| `smooth muscle cell` | 5,859 | Vascular Smooth Muscle Cell | Already mapped (lowercase) |
| `myeloid cell` | 4,621 | Myeloid Cell | Case-insensitive match |
| `innate lymphoid cell` | 3,333 | Innate Lymphoid Cell | Case-insensitive match |
| `ventricular cardiac muscle cell` | 3,203 | Ventricular Cardiomyocytes | Case-insensitive match |
| `neuron` | 2,394 | Neuron | Case-insensitive match |
| `epicardial adipocyte` | 2,358 | Epicardial Adipocyte | Case-insensitive match |
| `mesothelial cell of epicardium` | 2,276 | Mesothelial Cell of Epicardium | Case-insensitive match |
| `capillary endothelial cell` | 1,567 | Capillary Endothelial Cell | Case-insensitive match |
| `fetal cardiomyocyte` | 1,310 | Cardiac Muscle Cell | Case-insensitive match (alias in original map) |
| `pericyte` | 1,134 | Pericyte | Case-insensitive match |
| `endothelial cell of lymphatic vessel` | 820 | Lymphatic Endothelial Cell | Case-insensitive match |
| `dermis microvascular lymphatic vessel endothelial cell` | 742 | Dermis Microvascular Lymphatic Endothelial Cell | Already mapped (lowercase) |
| `leukocyte` | 709 | Leukocyte | Case-insensitive match |
| `schwann cell` | 669 | Schwann Cell | Case-insensitive match |
| `visceromotor neuron` | 439 | Visceromotor Neuron | Case-insensitive match |
| `hematopoietic cell` | 328 | Hematopoietic Cell | Case-insensitive match |
| `endothelial cell of artery` | 903 | Arterial Endothelial Cell | Case-insensitive match |
| `vein endothelial cell` | 248 | Venous Endothelial Cell | Case-insensitive match |
| `mesenchymal stem cell` | 261 | Mesenchymal Stem Cell | Case-insensitive match |
| `macrophage` | 112 | Macrophage | Case-insensitive match |
| `regular atrial cardiac myocyte` | 121 | Regular Atrial Cardiac Myocyte | Case-insensitive match |
| `erythrocyte` | 99 | Erythrocyte | Case-insensitive match |
| `erythroid lineage cell` | 80 | Erythroid Lineage Cell | Case-insensitive match |
| `cord blood hematopoietic stem cell` | 6 | Hematopoietic Cell | Explicit alias; HSC → parent hematopoietic node |
| `valve interstitial cell` | 3 | Valve Interstitial Cell | Case-insensitive match |

**Dropped CXG labels** (not mappable to any heart lineage node):

| CXG Label | Count | Reason |
|---|---|---|
| `unknown` | ~15,125 | No cell identity information |
| `epithelial cell` | ~few | Out of scope (non-cardiac epithelium) |
| `cell of skeletal muscle` | ~few | Out of scope (non-cardiac) |
| `primordial germ cell` | ~few | Out of scope |

---

### Xu Dataset → Canonical Mappings

The Xu 2023 dataset is a whole-embryo atlas. Only cardiac-relevant labels are retained.

| Xu Label | Count | Canonical Name | Notes |
|---|---|---|---|
| `fibroblast` | 4,641 | Cardiac Fibroblast | Already mapped (lowercase alias) |
| `endocardium` | 1,020 | Endocardial Cell | Explicit alias; anatomical → CL equivalent |
| `ventricle cardiomyocyte` | 972 | Ventricular Cardiomyocytes | Explicit alias |
| `atria cardiomyocyte` | 595 | Regular Atrial Cardiac Myocyte | Explicit alias |
| `epicardial derived cell` | 785 | Epicardium Derived Cell | Explicit alias; "epicardial" ≠ "epicardium" → added |
| `endocardial derived cell` | 503 | Endocardial Cushion | Explicit alias; EMT-derived cushion cells |
| `epicardium` | 252 | Mesothelial Cell of Epicardium | Explicit alias; anatomical → cell type |
| `atrioventricular canal` | 258 | AV Canal Endocardial Cells | Explicit alias; anatomical region → endocardial cell subtype |
| `cardiomyocyte` | 363 | Cardiac Muscle Cell | Explicit alias; generic → parent CM node |
| `Second heart field (SHF)` | 373 | Cardiogenic Mesoderm | Explicit alias; SHF is a progenitor pool within cardiogenic mesoderm |
| `sinoatrial node (SAN)` | 105 | SA Node Pacemaker Cell | Explicit alias; anatomical region → cell type |
| `pericyte (myocardium)` | 17 | Pericyte | Explicit alias; parenthetical qualifier stripped |

**Dropped Xu labels** (majority of Xu dataset — non-cardiac):

All non-cardiac Xu labels are dropped (sclerotome, hepatocyte, pharyngeal arch, hindlimb, etc.). The Xu dataset is a whole-embryo reference; only the cardiac-specific labels above are retained.

---

### Lázár Dataset

Lázár labels use a mix of Lázár-specific cell type codes (e.g., `Immature Cardiomyocyte (Immat_CM)`, `Microvascular Endothelial Cell (MicroVasc_EC)`). These were mapped in the original harmonization map and are unaffected by the current changes. All Lázár cells that pass time filtering are expected to pass cell type filtering.

### Tyser Dataset

Tyser 2021 is a gastrulation-stage atlas (CS7, ~PCW 2.5). Most Tyser cell types are gastrulation-specific (epiblast, primitive streak, nascent mesoderm, etc.) and not heart-specific. The following are retained:

| Tyser Label | Count | Canonical Name |
|---|---|---|
| `hemogenic endothelial progenitor` | 111 | Hematopoietic Cell |
| `erythrocyte (CS7)` | 32 | Erythrocyte |
| `epiblast cell` | 133 | Epiblast |
| `primitive streak` | ~many | Primitive Streak |
| `advanced/emergent/nascent mesoderm` | ~many | Mesoderm |
| `ectodermal cell` | ~many | Ectoderm |

Note: Tyser PCW values (from `"Day 16"` annotation → PCW 2.29) are parsed and included where cell types match. Most Tyser cells will still be dropped because the lineage holdout excludes Epicardial / EPDC and Vascular EC lineages, and gastrulation types have no associated cardiac trajectory timepoints.

---

## Lineage Holdouts

The following canonical types are **excluded from all train/val/test splits** regardless of availability:

- `Epicardial / EPDC` lineage branch (includes Mesothelial Cell of Epicardium, Epicardium Derived Cell, Epicardial Adipocyte, Cardiac Fibroblast, Vascular Smooth Muscle Cell, Pericyte, Adipocyte)
- `Vascular EC` lineage branch (includes all endothelial cell subtypes)

**Rationale**: These lineages are held out to test the model's ability to predict unseen lineage trajectories at evaluation time, following the brain-aging pipeline design.

---

## Summary of Expected Cell Recovery

After applying all changes above, expected cell counts (approximate, subject to PCW filter and lineage holdouts):

| Source | Before | After | Notes |
|---|---|---|---|
| CXG | 13,944 | ~200,000+ | Case-insensitive + embryonic stage fix |
| Xu | 4,641 | ~10,000+ | Explicit Xu heart-specific aliases |
| Lázár | 71,250 | ~71,250 | Unchanged |
| Tyser | 0 | ~few | CS7 cells with mappable types |
| **Total** | **89,835** | **~280,000+** | Before lineage holdout filtering |

Actual numbers depend on `--val-pcw`, `--test-pcw`, lineage holdout, and `--max-cells-per-source` settings.
