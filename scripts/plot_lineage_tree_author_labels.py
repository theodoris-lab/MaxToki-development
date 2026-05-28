"""
Generate a lineage-tree × PCW-timeline HTML that shows:
  - The developmental lineage hierarchy as the row organizer
  - Author-specific labels (by dataset) for each canonical cell type
  - Per-PCW availability dots (colored by dataset)
  - Val / Test PCW split proposal highlighted

Output: cell_type_harmonization/lineage_tree_author_labels.html

Usage:
    python scripts/plot_lineage_tree_author_labels.py
"""

import csv
import json
import math
import html as html_mod
from collections import defaultdict
from pathlib import Path

import pandas as pd

# Dot-radius normalisation: log2 scale, calibrated to global max observed count
GLOBAL_MAX_N = 42_762   # CXG cardiac muscle cell @ PCW 12 — sets the upper bound
DOT_R_MIN    = 2.0      # radius in SVG units for 1 cell
DOT_R_MAX    = 8.0      # radius for GLOBAL_MAX_N cells

ROOT = Path(__file__).parent.parent

# ── Input files ───────────────────────────────────────────────────────────────
HARM_MAP_JSON    = ROOT / "cell_type_harmonization" / "cell_type_harmonization_map.json"
HARM_TABLE_CSV   = ROOT / "cell_type_harmonization" / "cell_type_harmonization_table.csv"
CXG_CSV          = ROOT / "dump" / "cellxgene_heart_development_subset_celltype_by_stage_combined.csv"
LAZAR_CSV        = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/lazar_et_al_2025/lazar_metadata.csv")
XU_ANNOTATION    = Path("/gladstone/theodoris/lab/dwen/data/organogenesis_data/organogenesis/cell_annotation.txt")
OUT_HTML         = ROOT / "cell_type_harmonization" / "lineage_tree_author_labels.html"

# ── PCW columns (unique timepoints, shown as merged columns) ─────────────────
#  Each entry: (sort_key, display_label, split_role)
#  split_role: "val", "test", "train", or "future-val"/"future-test" (not in data)
PCW_COLS = [
    (3.0,   "PCW 3",   "Tyser\nCS7",   "train"),
    (4.0,   "PCW ~4",  "Xu\nCS12",     "train"),
    (4.5,   "PCW ~4.5","Xu\nCS13-14",  "train"),
    (5.0,   "PCW ~5",  "Xu\nCS15-16",  "train"),
    (5.5,   "PCW ~5.5","CXG\nEmbryonic","train"),
    (6.0,   "PCW 6",   "CXG+Lázár",   "train"),
    (7.0,   "PCW 7",   "Lázár",        "test"),
    (8.0,   "PCW 8",   "Lázár",        "train"),
    (9.0,   "PCW 9",   "Lázár",        "train"),
    (10.0,  "PCW 10",  "CXG+Lázár",   "val"),
    (10.5,  "PCW 10.5","Lázár",        "train"),
    (11.0,  "PCW 11",  "CXG",          "train"),
    (12.0,  "PCW 12",  "CXG+Lázár",   "train"),
    (13.0,  "PCW 13",  "CXG",          "train"),
    (15.0,  "PCW 15",  "CXG",          "train"),
    (16.0,  "PCW 16",  "CXG",          "train"),
    (17.0,  "PCW 17",  "CXG",          "train"),
    (19.0,  "PCW 19",  "CXG",          "train"),
    (20.0,  "PCW 20",  "CXG",          "val"),
    (25.0,  "PCW 25",  "—",            "future-test"),
    (30.0,  "PCW 30",  "—",            "future-val"),
    (33.0,  "PCW 33",  "—",            "future-test"),
]
PCW_KEYS = [p[0] for p in PCW_COLS]

# ── Lázár age string → PCW sort_key ──────────────────────────────────────────
LAZAR_AGE_TO_PCW = {"w6": 6.0, "w7": 7.0, "w8": 8.0, "w9": 9.0,
                     "w10": 10.0, "w10.5": 10.5, "w12": 12.0}

# ── Xu stage → PCW sort_key ───────────────────────────────────────────────────
XU_STAGE_TO_PCW  = {"CS12": 4.0, "CS13-14": 4.5, "CS15-16": 5.0}

# ── CXG stage column → PCW sort_key ──────────────────────────────────────────
CXG_STAGE_TO_PCW = {
    "embryonic stage":                       5.5,
    "6th week post-fertilization stage":     6.0,
    "10th week post-fertilization stage":   10.0,
    "11th week post-fertilization stage":   11.0,
    "12th week post-fertilization stage":   12.0,
    "13th week post-fertilization stage":   13.0,
    "15th week post-fertilization stage":   15.0,
    "16th week post-fertilization stage":   16.0,
    "17th week post-fertilization stage":   17.0,
    "19th week post-fertilization stage":   19.0,
    "20th week post-fertilization stage":   20.0,
}

# ── Tyser data (hardcoded) ────────────────────────────────────────────────────
TYSER_PCW = 3.0
TYSER_PROGENITORS = {
    "epiblast cell":     133,
    "primitive streak":  202,
    "advanced mesoderm": 164,
    "emergent mesoderm": 185,
    "nascent mesoderm":   98,
    "axial mesoderm":     23,
    "yolk sac mesoderm":  83,
    "ectodermal cell":    29,
    "hematopoietic cell": 111,
    "erythrocyte":         32,
}

# Tyser Xu cell types
XU_CELL_LINEAGE = {
    "ventricle cardiomyocyte":  "Cardiomyocyte",
    "atria cardiomyocyte":      "Cardiomyocyte",
    "cardiomyocyte":            "Cardiomyocyte",
    "cardiomyocyte like":       "Cardiomyocyte",
    "Second heart field (SHF)": "Cardiomyocyte",
    "atrioventricular canal":   "Cardiomyocyte",
    "sinoatrial node (SAN)":    "Cardiomyocyte",
    "epicardium":               "Epicardial / EPDC",
    "epicardial derived cell":  "Epicardial / EPDC",
    "pericyte":                 "Epicardial / EPDC",
    "pericyte (myocardium)":    "Epicardial / EPDC",
    "endocardium":              "Endocardial / Valve",
    "endocardial derived cell": "Endocardial / Valve",
}

# ── Lineage section order ──────────────────────────────────────────────────────
SECTION_ORDER = [
    "Tyser progenitors",
    "Cardiomyocyte",
    "Endocardial / Valve",
    "Epicardial / EPDC",
    "Mesenchymal / Stromal",
    "Vascular EC",
    "Immune / Haematopoietic",
    "Neural",
]

SECTION_COLORS = {
    "Tyser progenitors":     ("#fff8e1", "#fbc02d"),
    "Cardiomyocyte":         ("#fde8e8", "#e57373"),
    "Endocardial / Valve":   ("#fef3e2", "#f59e0b"),
    "Epicardial / EPDC":     ("#e6f4ea", "#34a853"),
    "Mesenchymal / Stromal": ("#e8f0fe", "#4285f4"),
    "Vascular EC":           ("#f3e8ff", "#8b5cf6"),
    "Immune / Haematopoietic":("#fce7f3", "#ec4899"),
    "Neural":                ("#e0f7fa", "#00acc1"),
}

# Lineage sections withheld from all splits to test cell-identity generalisation
LINEAGE_HOLDOUTS: set[str] = {"Epicardial / EPDC", "Vascular EC"}

DATASET_COLORS = {
    "CXG":   "#4285f4",
    "Lázár": "#0f9d58",
    "Xu":    "#9c27b0",
    "Tyser": "#e65100",
}

SPLIT_COLORS = {
    "val":         ("rgba(52,168,83,0.15)",  "#34a853", "Val"),
    "test":        ("rgba(234,67,53,0.15)",  "#ea4335", "Test"),
    "train":       ("transparent",           "#ccc",    "Train"),
    "future-val":  ("rgba(52,168,83,0.06)",  "#34a853", "Val*"),
    "future-test": ("rgba(234,67,53,0.06)",  "#ea4335", "Test*"),
}

# ── Load data ─────────────────────────────────────────────────────────────────

def load_all():
    with HARM_MAP_JSON.open() as f:
        hmap = json.load(f)
    harm_entries = hmap["harmonization_map"]

    ht = pd.read_csv(HARM_TABLE_CSV)

    # canonical → {source: [observed_label, ...]}
    canon_to_labels: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    # canonical → lineage section (from harmonization_map, inferred from path)
    canon_to_section: dict[str, str] = {}
    canon_to_path: dict[str, list[str]] = {}

    for _, row in ht.iterrows():
        canon = row["canonical_tree_label"]
        src   = row["source"]
        obs   = row["observed_label"]
        canon_to_labels[canon][src].append(obs)

    # Explicit canonical → section mapping (from lineage_path inspection)
    CANON_SECTION: dict[str, str] = {
        # ── Tyser early progenitors ──────────────────────────────────────────
        "Epiblast":                              "Tyser progenitors",
        "Primitive Streak":                      "Tyser progenitors",
        "Mesoderm":                              "Tyser progenitors",
        "Cardiogenic Mesoderm":                  "Tyser progenitors",
        "Ectoderm":                              "Tyser progenitors",
        # ── Cardiomyocyte ────────────────────────────────────────────────────
        "Cardiac Muscle Cell":                   "Cardiomyocyte",
        "Ventricular Cardiomyocytes":            "Cardiomyocyte",
        "Regular Atrial Cardiac Myocyte":        "Cardiomyocyte",
        "SA Node Pacemaker Cell":                "Cardiomyocyte",
        "Outflow Tract Smooth Muscle Cell":      "Cardiomyocyte",
        # ── Endocardial / Valve ───────────────────────────────────────────────
        "Endocardial Cell":                      "Endocardial / Valve",
        "AV Canal Endocardial Cells":            "Endocardial / Valve",
        "Endocardial Cushion":                   "Endocardial / Valve",
        "Valve Mesenchymal Cells":               "Endocardial / Valve",
        "Valve Interstitial Cell":               "Endocardial / Valve",
        # ── Epicardial / EPDC ────────────────────────────────────────────────
        "Mesothelial Cell of Epicardium":        "Epicardial / EPDC",
        "Epicardium Derived Cell":               "Epicardial / EPDC",
        "Cardiac Fibroblast":                    "Epicardial / EPDC",
        "Vascular Smooth Muscle Cell":           "Epicardial / EPDC",
        "Pericyte":                              "Epicardial / EPDC",
        "Adipocyte":                             "Epicardial / EPDC",
        "Epicardial Adipocyte":                  "Epicardial / EPDC",
        # ── Mesenchymal / Stromal ────────────────────────────────────────────
        "Cardiac Mesenchymal Cell":              "Mesenchymal / Stromal",
        "Stromal Cell":                          "Mesenchymal / Stromal",
        "Mesenchymal Stem Cell":                 "Mesenchymal / Stromal",
        "Fibroblast":                            "Mesenchymal / Stromal",
        # ── Vascular EC ──────────────────────────────────────────────────────
        "Vascular Endothelial Cell":             "Vascular EC",
        "Capillary Endothelial Cell":            "Vascular EC",
        "Arterial Endothelial Cell":             "Vascular EC",
        "Venous Endothelial Cell":               "Vascular EC",
        "Lymphatic Endothelial Cell":            "Vascular EC",
        "Dermis Microvascular Lymphatic Endothelial Cell": "Vascular EC",
        # ── Immune / Haematopoietic ───────────────────────────────────────────
        "Hematopoietic Cell":                    "Immune / Haematopoietic",
        "Myeloid Cell":                          "Immune / Haematopoietic",
        "Monocyte":                              "Immune / Haematopoietic",
        "Macrophage":                            "Immune / Haematopoietic",
        "Neutrophil":                            "Immune / Haematopoietic",
        "Dendritic Cell":                        "Immune / Haematopoietic",
        "Professional Antigen Presenting Cell":  "Immune / Haematopoietic",
        "Leukocyte":                             "Immune / Haematopoietic",
        "Innate Lymphoid Cell":                  "Immune / Haematopoietic",
        "T Cell":                                "Immune / Haematopoietic",
        "Erythroid Progenitor Cell":             "Immune / Haematopoietic",
        "Erythroblast":                          "Immune / Haematopoietic",
        "Erythroid Lineage Cell":                "Immune / Haematopoietic",
        "Erythrocyte":                           "Immune / Haematopoietic",
        # ── Neural ───────────────────────────────────────────────────────────
        "Neural Cell":                           "Neural",
        "Neuron":                                "Neural",
        "Visceromotor Neuron":                   "Neural",
        "Schwann Cell":                          "Neural",
    }

    for name, entry in harm_entries.items():
        path = entry.get("lineage_path", [name])
        canon_to_path[name] = path
        canon_to_section[name] = CANON_SECTION.get(name, "Neural")

    # ── CXG PCW coverage ────────────────────────────────────────────────────
    # normalized CXG label → canonical
    cxg_norm_to_canon: dict[str, str] = {}
    for _, row in ht[ht["source"] == "CXG"].iterrows():
        norm = row["normalized_observed_label"].strip().lower()
        cxg_norm_to_canon[norm] = row["canonical_tree_label"]

    # canonical → {pcw: cell_count}  (CXG only)
    cxg_cov: dict[str, dict[float, int]] = defaultdict(lambda: defaultdict(int))
    cxg_df = pd.read_csv(CXG_CSV)
    stage_cols = [c for c in cxg_df.columns if c in CXG_STAGE_TO_PCW]
    for _, row in cxg_df.iterrows():
        raw = str(row["cell type"]).strip().rstrip("*").lower()
        canon = cxg_norm_to_canon.get(raw)
        if not canon:
            continue
        for sc in stage_cols:
            n = int(row.get(sc, 0) or 0)
            if n > 0:
                cxg_cov[canon][CXG_STAGE_TO_PCW[sc]] += n

    # ── Lázár PCW coverage ───────────────────────────────────────────────────
    # DL cluster abbrev → canonical
    lazar_abbrev_to_canon: dict[str, str] = {}
    for _, row in ht[ht["source"] == "Lázár"].iterrows():
        obs = row["observed_label"].strip()
        # Extract abbreviation from "Full Name (ABBREV)" or just keep as-is
        import re
        m = re.search(r'\((\w+)\)$', obs)
        abbrev = m.group(1) if m else obs
        lazar_abbrev_to_canon[abbrev] = row["canonical_tree_label"]

    lazar_df = pd.read_csv(LAZAR_CSV)
    lazar_cov: dict[str, dict[float, int]] = defaultdict(lambda: defaultdict(int))
    for _, row in lazar_df.iterrows():
        cluster = str(row["seurat_clusters_annot"]).strip()
        age     = str(row["age"]).strip()
        canon   = lazar_abbrev_to_canon.get(cluster)
        if not canon:
            continue
        pcw = LAZAR_AGE_TO_PCW.get(age)
        if pcw is None:
            continue
        lazar_cov[canon][pcw] += 1

    # ── Xu PCW coverage ──────────────────────────────────────────────────────
    xu_obs_to_canon: dict[str, str] = {}
    for _, row in ht[ht["source"] == "Xu"].iterrows():
        obs = row["observed_label"].strip()
        xu_obs_to_canon[obs] = row["canonical_tree_label"]

    xu_df = pd.read_csv(XU_ANNOTATION, sep="\t", usecols=["annotation", "stage"])
    xu_cov: dict[str, dict[float, int]] = defaultdict(lambda: defaultdict(int))
    for _, row in xu_df.iterrows():
        annot = str(row["annotation"]).strip()
        stage = str(row["stage"]).strip()
        canon = xu_obs_to_canon.get(annot)
        if not canon:
            continue
        pcw = XU_STAGE_TO_PCW.get(stage)
        if pcw is None:
            continue
        xu_cov[canon][pcw] += 1

    # ── Tyser coverage ───────────────────────────────────────────────────────
    tyser_obs_to_canon: dict[str, str] = {}
    for _, row in ht[ht["source"] == "Tyser"].iterrows():
        obs = row["observed_label"].strip()
        tyser_obs_to_canon[obs] = row["canonical_tree_label"]

    tyser_cov: dict[str, dict[float, int]] = defaultdict(lambda: defaultdict(int))
    for obs, n in TYSER_PROGENITORS.items():
        canon = tyser_obs_to_canon.get(obs)
        if canon:
            tyser_cov[canon][TYSER_PCW] += n

    # ── Lázár DL cluster rows (sub-rows under canonical CMs) ─────────────────
    lazar_cluster_data: dict[str, dict[float, int]] = defaultdict(lambda: defaultdict(int))
    for _, row in lazar_df.iterrows():
        cluster = str(row["seurat_clusters_annot"]).strip()
        age     = str(row["age"]).strip()
        pcw     = LAZAR_AGE_TO_PCW.get(age)
        if pcw is not None:
            lazar_cluster_data[cluster][pcw] += 1

    return (harm_entries, canon_to_labels, canon_to_section, canon_to_path,
            cxg_cov, lazar_cov, xu_cov, tyser_cov, lazar_cluster_data, lazar_abbrev_to_canon)


# ── Lázár DL cluster expanded names ──────────────────────────────────────────
LAZAR_CLUSTER_NAMES = {
    "LV_C":  "LV Compact (LV_C)",
    "LV_T":  "LV Trabecular (LV_T)",
    "RV_C":  "RV Compact (RV_C)",
    "RV_T":  "RV Trabecular (RV_T)",
    "LA":    "Left Atrial (LA)",
    "RA":    "Right Atrial (RA)",
    "OFT":   "Outflow Tract (OFT)",
    "PM":    "Papillary Muscle (PM)",
    "MY":    "Myocardial Progenitor (MY)",
    "VM":    "Ventricular Myocardium (VM)",
    "TA":    "Trabecular Atrial (TA)",
    "TM":    "Trabecular Myocardium (TM)",
    "SCV":   "Sinus Venosus/Caval (SCV)",
    "B_A":   "Bipotent Atrial (B_A)",
    "B_V":   "Bipotent Ventricular (B_V)",
    "AVP_A": "AV Progenitor, Atrial (AVP_A)",
    "AVP_V": "AV Progenitor, Ventricular (AVP_V)",
    "VCS":   "Ventricular Conduction Sys. (VCS)",
    "EN":    "Endothelium (EN)",
    "VE":    "Venous Endothelium (VE)",
    "LCV":   "Lympho-Capillary Vessel (LCV)",
    "A_EP":  "Atrial Epicardium (A_EP)",
    "V_EP":  "Ventricular Epicardium (V_EP)",
}

LAZAR_CLUSTER_SECTION = {
    **{k: "Cardiomyocyte" for k in
       ["LV_C","LV_T","RV_C","RV_T","LA","RA","OFT","PM","MY","VM",
        "TA","TM","SCV","B_A","B_V","AVP_A","AVP_V","VCS"]},
    "EN":  "Vascular EC",
    "VE":  "Vascular EC",
    "LCV": "Vascular EC",
    "A_EP":"Epicardial / EPDC",
    "V_EP":"Epicardial / EPDC",
}


# ── HTML generation ───────────────────────────────────────────────────────────

def dot_html(pcw_key: float, ds_cov: dict[float, int], color: str, label: str) -> str:
    """Return a colored circle SVG sized proportional to log(cell count)."""
    n = ds_cov.get(pcw_key, 0)
    if n == 0:
        return ""
    tip = html_mod.escape(f"{label}: {n:,} cells @ PCW {pcw_key}")
    r = DOT_R_MIN + (DOT_R_MAX - DOT_R_MIN) * math.log2(n + 1) / math.log2(GLOBAL_MAX_N + 1)
    size = int(r * 2 + 4)  # SVG canvas slightly bigger than dot
    return (f'<svg width="{size}" height="{size}" style="display:inline-block;vertical-align:middle" '
            f'title="{tip}">'
            f'<circle cx="{size/2:.0f}" cy="{size/2:.0f}" r="{r:.1f}" fill="{color}" opacity="0.82"/>'
            f'</svg>')


def chips_html(labels_by_source: dict[str, list[str]]) -> str:
    parts = []
    for src, col in DATASET_COLORS.items():
        labs = labels_by_source.get(src, [])
        if not labs:
            continue
        chips = "".join(
            f'<span class="chip" style="background:{col}20;color:{col};border-color:{col}80">'
            f'{html_mod.escape(l.rstrip("*"))}</span>'
            for l in labs
        )
        parts.append(f'<span class="src-group"><span class="src-badge" style="background:{col};color:#fff">'
                     f'{html_mod.escape(src)}</span>{chips}</span>')
    return "".join(parts)


def row_html(name: str, labels_by_src: dict[str, list[str]],
             cxg: dict, lazar: dict, xu: dict, tyser: dict,
             indent: int = 0, is_cluster: bool = False,
             section_border: str = "#ccc") -> str:
    indent_px = indent * 16
    bg = "#f9f9f9" if is_cluster else "#fff"
    border_left = f"3px solid {section_border}" if indent == 0 else "none"

    cells = []
    for pk, _lbl, _ds, _role in PCW_COLS:
        cell_parts = []
        cell_parts.append(dot_html(pk, tyser,  DATASET_COLORS["Tyser"], "Tyser"))
        cell_parts.append(dot_html(pk, xu,     DATASET_COLORS["Xu"],    "Xu"))
        cell_parts.append(dot_html(pk, cxg,    DATASET_COLORS["CXG"],   "CXG"))
        cell_parts.append(dot_html(pk, lazar,  DATASET_COLORS["Lázár"], "Lázár"))
        inner = "".join(cell_parts)
        cells.append(f'<td class="pcw-cell">{inner}</td>')

    chips = chips_html(labels_by_src) if not is_cluster else ""

    name_esc = html_mod.escape(name)
    name_style = "font-size:0.78rem;color:#666;" if is_cluster else "font-size:0.84rem;font-weight:600;"
    # Dim holdout rows slightly
    holdout_borders = {SECTION_COLORS.get(s, ("", ""))[1] for s in LINEAGE_HOLDOUTS}
    is_holdout_row = not is_cluster and section_border in holdout_borders
    row_opacity = "opacity:0.72;" if is_holdout_row else ""
    stripe_bg = ("repeating-linear-gradient(45deg,rgba(0,0,0,0.04),rgba(0,0,0,0.04) 1px,"
                 "transparent 1px,transparent 5px)") if is_holdout_row else "none"

    return (f'<tr style="background:{bg};{row_opacity}">'
            f'<td class="label-cell" style="padding-left:{indent_px + 8}px;border-left:{border_left};'
            f'background-image:{stripe_bg}">'
            f'<span style="{name_style}">{name_esc}</span>'
            f'<div class="chips-wrap">{chips}</div>'
            f'</td>'
            + "".join(cells) +
            f'</tr>\n')


def section_header_html(section: str, bg: str, border: str) -> str:
    n_pcw = len(PCW_COLS)
    is_holdout = section in LINEAGE_HOLDOUTS
    badge = ('&nbsp;&nbsp;<span style="font-size:0.72rem;font-weight:700;'
             'color:#555;background:#e0e0e0;padding:1px 7px;border-radius:3px;'
             'letter-spacing:0">&#8855; LINEAGE HOLDOUT</span>') if is_holdout else ""
    extra_style = "opacity:0.75;" if is_holdout else ""
    return (f'<tr class="section-header">'
            f'<td style="background:{bg};border-left:4px solid {border};'
            f'padding:6px 10px;font-size:0.82rem;font-weight:700;color:#333;'
            f'letter-spacing:0.05em;{extra_style}">'
            f'{html_mod.escape(section.upper())}{badge}</td>'
            f'<td colspan="{n_pcw}" style="background:{bg};{extra_style}"></td>'
            f'</tr>\n')


def generate_html(out_path: Path):
    (harm_entries, canon_to_labels, canon_to_section, canon_to_path,
     cxg_cov, lazar_cov, xu_cov, tyser_cov, lazar_cluster_data,
     lazar_abbrev_to_canon) = load_all()

    # Group canonicals by section
    by_section: dict[str, list[str]] = defaultdict(list)
    for name in harm_entries:
        sec = canon_to_section.get(name, "Neural")
        by_section[sec].append(name)

    # Build table rows
    body_rows = []

    # ── PCW header ─────────────────────────────────────────────────────────
    header_cells = ['<th class="label-hdr">Cell Type / Author Labels<br>'
                    '<span style="font-weight:400;font-size:0.7rem;color:#888">'
                    'Click dataset badge rows to show labels</span></th>']
    for pk, plbl, ds_lbl, role in PCW_COLS:
        sc, bc, rl = SPLIT_COLORS[role]
        future = "opacity:0.5;" if "future" in role else ""
        header_cells.append(
            f'<th class="pcw-hdr" style="background:{sc};border-bottom:2px solid {bc};{future}">'
            f'<div class="pcw-top">{html_mod.escape(plbl)}</div>'
            f'<div class="pcw-ds" style="color:#777">{html_mod.escape(ds_lbl.replace(chr(10)," "))}</div>'
            f'<div class="split-lbl" style="color:{bc}">{rl}</div>'
            f'</th>'
        )
    header_row = "<tr>" + "".join(header_cells) + "</tr>\n"

    for section in SECTION_ORDER:
        canonicals = by_section.get(section, [])
        if not canonicals:
            continue
        bg, border = SECTION_COLORS.get(section, ("#f5f5f5", "#999"))
        body_rows.append(section_header_html(section, bg, border))

        # Sort by lineage path length then name
        canonicals.sort(key=lambda n: (len(canon_to_path.get(n, [])), n))

        for name in canonicals:
            labels_by_src = canon_to_labels.get(name, {})
            cxg   = cxg_cov.get(name, {})
            lazar = lazar_cov.get(name, {})
            xu    = xu_cov.get(name, {})
            tyser = tyser_cov.get(name, {})
            body_rows.append(row_html(name, labels_by_src, cxg, lazar, xu, tyser,
                                      indent=1, section_border=border))

            # For canonical CMs / VEC / Epicardial that have Lázár sub-clusters,
            # add those as indented sub-rows
            clusters_in_section = [
                (abbrev, full)
                for abbrev, full in LAZAR_CLUSTER_NAMES.items()
                if LAZAR_CLUSTER_SECTION.get(abbrev) == section
                and lazar_abbrev_to_canon.get(abbrev) == name
            ]
            for abbrev, full in sorted(clusters_in_section, key=lambda x: x[1]):
                cl_cov = lazar_cluster_data.get(abbrev, {})
                body_rows.append(row_html(
                    f"└ {full}", {}, {}, cl_cov, {}, {},
                    indent=2, is_cluster=True, section_border=border
                ))

    # ── Size legend ─────────────────────────────────────────────────────────
    legend_ns = [10, 100, 1000, 10_000]
    legend_parts = []
    for ln in legend_ns:
        r = DOT_R_MIN + (DOT_R_MAX - DOT_R_MIN) * math.log2(ln + 1) / math.log2(GLOBAL_MAX_N + 1)
        sz = int(r * 2 + 4)
        lbl = f"{ln:,}"
        legend_parts.append(
            f'<svg width="{sz}" height="{sz}" style="display:inline-block;vertical-align:middle;margin-right:2px">'
            f'<circle cx="{sz/2:.0f}" cy="{sz/2:.0f}" r="{r:.1f}" fill="#aaa" opacity="0.7"/></svg>'
            f'<span style="font-size:0.65rem;color:#aaa;margin-right:6px">{lbl}</span>'
        )
    size_legend_html = "".join(legend_parts)

    # ── Assemble HTML ───────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Heart Development — Lineage Tree × Author Labels × PCW Coverage</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          font-size: 13px; background: #f0f0f0; }}

  /* ── Top info bar ── */
  .info-bar {{
    padding: 12px 16px; background: #1a1a2e; color: #eee;
    font-size: 0.8rem; line-height: 1.6;
  }}
  .info-bar h1 {{ font-size: 1.05rem; color: #fff; margin-bottom: 4px; }}
  .info-bar .badges {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }}
  .ds-badge {{ padding: 2px 9px; border-radius: 10px; font-size: 0.7rem;
               font-weight: 600; color: #fff; }}
  .split-pill {{ display: inline-flex; align-items: center; gap: 5px;
                 padding: 2px 10px; border-radius: 10px; font-size: 0.7rem;
                 font-weight: 600; border: 2px solid; }}

  /* ── Table wrapper ── */
  .tbl-wrap {{ overflow: auto; max-height: calc(100vh - 90px); }}
  table {{ border-collapse: collapse; width: max-content; min-width: 100%; }}

  /* ── Header ── */
  thead {{ position: sticky; top: 0; z-index: 10; }}
  .label-hdr {{
    min-width: 340px; width: 340px; padding: 8px 10px;
    background: #1a1a2e; color: #ddd; font-size: 0.75rem; text-align: left;
    vertical-align: bottom; position: sticky; left: 0; z-index: 20;
  }}
  .pcw-hdr {{
    min-width: 58px; width: 58px; padding: 4px 2px; text-align: center;
    vertical-align: bottom; font-size: 0.65rem; border-right: 1px solid #e0e0e0;
  }}
  .pcw-top {{ font-weight: 700; font-size: 0.72rem; color: #1a1a2e; }}
  .pcw-ds  {{ font-size: 0.6rem; color: #888; }}
  .split-lbl {{ font-size: 0.68rem; font-weight: 700; margin-top: 2px; }}

  /* ── Body rows ── */
  .label-cell {{
    position: sticky; left: 0; background: inherit; z-index: 5;
    padding: 5px 8px; vertical-align: top;
    border-bottom: 1px solid #f0f0f0; border-right: 2px solid #e0e0e0;
    min-width: 340px; max-width: 340px;
  }}
  .pcw-cell {{
    text-align: center; vertical-align: middle;
    padding: 2px 1px; border-bottom: 1px solid #f0f0f0;
    border-right: 1px solid #eee;
  }}
  tr:hover td {{ background: #fffde7 !important; }}
  .section-header td {{ border-bottom: 2px solid #ddd; }}

  /* ── Author label chips ── */
  .chips-wrap {{ margin-top: 3px; display: flex; flex-wrap: wrap; gap: 3px; }}
  .src-group {{ display: flex; flex-wrap: wrap; align-items: center; gap: 2px; margin-bottom: 2px; }}
  .src-badge {{ font-size: 0.6rem; font-weight: 700; padding: 1px 5px;
                border-radius: 3px; white-space: nowrap; }}
  .chip {{ font-size: 0.62rem; padding: 1px 5px; border-radius: 3px;
           border: 1px solid; white-space: nowrap; }}

  /* ── PCW future-split columns ── */
  td.pcw-cell:nth-last-child(-n+3) {{ opacity: 0.55; }}
  th.pcw-hdr:nth-last-child(-n+3) {{ opacity: 0.7; }}
</style>
</head>
<body>

<div class="info-bar">
  <h1>Heart Development — Lineage × Author Labels × PCW Coverage</h1>
  <div>Rows = canonical cell types (grouped by lineage). Indented rows (└) = Lázár DL sub-clusters.
       Hover a dot to see cell count. Columns marked * = proposed split timepoints not yet in dataset.</div>
  <div class="badges">
    <span class="ds-badge" style="background:#e65100">Tyser (PCW&nbsp;3, CS7)</span>
    <span class="ds-badge" style="background:#9c27b0">Xu 2023 (PCW ~4–5, CS12–CS15-16)</span>
    <span class="ds-badge" style="background:#4285f4">CXG (PCW ~5.5–20)</span>
    <span class="ds-badge" style="background:#0f9d58">Lázár 2025 DL clusters (PCW 6–12)</span>
    &nbsp;&nbsp;
    <span class="split-pill" style="border-color:#34a853;color:#34a853;background:rgba(52,168,83,0.1)">
      Val: PCW 10, 20</span>
    <span class="split-pill" style="border-color:#ea4335;color:#ea4335;background:rgba(234,67,53,0.1)">
      Test: PCW 7</span>
    <span class="split-pill" style="border-color:#888;color:#666;background:rgba(0,0,0,0.05)">
      Train: all remaining PCW</span>
    <span class="split-pill" style="border-color:#555;color:#444;background:repeating-linear-gradient(45deg,rgba(0,0,0,0.07),rgba(0,0,0,0.07) 1px,transparent 1px,transparent 5px)">
      &#8855; Lineage holdout: Epicardial/EPDC &amp; Vascular EC</span>
    &nbsp;&nbsp;
    <span style="font-size:0.68rem;color:#aaa">● dot size ∝ log(cell count)&nbsp;&nbsp;</span>
    {size_legend_html}
  </div>
</div>

<div class="tbl-wrap">
<table>
<thead>
{header_row}
</thead>
<tbody>
{"".join(body_rows)}
</tbody>
</table>
</div>

</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"Written → {out_path}  ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    generate_html(OUT_HTML)
