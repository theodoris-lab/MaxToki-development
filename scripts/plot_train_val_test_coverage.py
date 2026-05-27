#!/usr/bin/env python3
"""
Generate a standalone interactive HTML dot-plot showing cell type coverage
across developmental time (PCW) to support train / val / test split decisions.

Data sources:
  - CellxGene heart-dev subset: exact per-PCW counts
    (dump/cellxgene_heart_development_subset_celltype_by_stage_combined.csv)
  - Tyser et al. 2021: aggregate counts at CS7 (≈ PCW 3), hardcoded
  - Lázár DL / Xu: aggregated across the full fetal window; shown as a
    marginal bar chart rather than per-PCW dots (no staged breakdown available)

Usage:
    python scripts/plot_train_val_test_coverage.py

Output:
    cell_type_harmonization/train_val_test_coverage.html
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
CXG_CSV = ROOT / "dump" / "cellxgene_heart_development_subset_celltype_by_stage_combined.csv"
OUT_HTML = ROOT / "cell_type_harmonization" / "train_val_test_coverage.html"

# ── Lineage grouping ───────────────────────────────────────────────────────
# Maps CXG cell type label → canonical lineage group (display order matters)
LINEAGE_ORDER = [
    "Cardiomyocyte",
    "Endocardial / Valve",
    "Epicardial / EPDC",
    "Mesenchymal / Stromal",
    "Vascular EC",
    "Immune / Haematopoietic",
    "Neural",
]

LINEAGE_MAP: dict[str, str] = {
    # ── Cardiomyocyte ──────────────────────────────────────────────────────
    "cardiac muscle cell":              "Cardiomyocyte",
    "fetal cardiomyocyte":              "Cardiomyocyte",
    "ventricular cardiac muscle cell":  "Cardiomyocyte",
    "regular atrial cardiac myocyte":   "Cardiomyocyte",
    # ── Endocardial / Valve ────────────────────────────────────────────────
    "endocardial cell":                 "Endocardial / Valve",
    "valve interstitial cell":          "Endocardial / Valve",
    # ── Epicardial / EPDC ─────────────────────────────────────────────────
    "mesothelial cell of epicardium":   "Epicardial / EPDC",
    "fibroblast":                       "Epicardial / EPDC",
    "smooth muscle cell":               "Epicardial / EPDC",
    "pericyte":                         "Epicardial / EPDC",
    "adipocyte":                        "Epicardial / EPDC",
    "epicardial adipocyte":             "Epicardial / EPDC",
    # ── Mesenchymal / Stromal ─────────────────────────────────────────────
    "cardiac mesenchymal cell":         "Mesenchymal / Stromal",
    "stromal cell":                     "Mesenchymal / Stromal",
    "mesenchymal stem cell":            "Mesenchymal / Stromal",
    # ── Vascular EC ───────────────────────────────────────────────────────
    "endothelial cell":                                        "Vascular EC",
    "endothelial cell of vascular tree":                       "Vascular EC",
    "capillary endothelial cell":                              "Vascular EC",
    "endothelial cell of artery":                              "Vascular EC",
    "vein endothelial cell":                                   "Vascular EC",
    "endothelial cell of lymphatic vessel":                    "Vascular EC",
    "dermis microvascular lymphatic vessel endothelial cell":  "Vascular EC",
    # ── Immune / Haematopoietic ───────────────────────────────────────────
    "hematopoietic cell":               "Immune / Haematopoietic",
    "cord blood hematopoietic stem cell": "Immune / Haematopoietic",
    "megakaryocyte":                    "Immune / Haematopoietic",
    "myeloid cell":                     "Immune / Haematopoietic",
    "monocyte":                         "Immune / Haematopoietic",
    "macrophage":                       "Immune / Haematopoietic",
    "neutrophil":                       "Immune / Haematopoietic",
    "dendritic cell":                   "Immune / Haematopoietic",
    "professional antigen presenting cell": "Immune / Haematopoietic",
    "leukocyte":                        "Immune / Haematopoietic",
    "innate lymphoid cell":             "Immune / Haematopoietic",
    "T cell":                           "Immune / Haematopoietic",
    "erythroid progenitor cell":        "Immune / Haematopoietic",
    "erythroblast":                     "Immune / Haematopoietic",
    "erythroid lineage cell":           "Immune / Haematopoietic",
    "erythrocyte":                      "Immune / Haematopoietic",
    # ── Neural ────────────────────────────────────────────────────────────
    "neural cell":                      "Neural",
    "neuron":                           "Neural",
    "visceromotor neuron":              "Neural",
    "Schwann cell":                     "Neural",
}

# Cell types to exclude entirely
EXCLUDE = {"unknown", "Total", "cell of skeletal muscle", "epithelial cell", "primordial germ cell"}

# ── PCW column mapping ─────────────────────────────────────────────────────
# Maps CSV column header → (sort_key, display_label)
CXG_STAGE_MAP: dict[str, tuple[float, str]] = {
    "embryonic stage":                       (5.5,  "Embryonic\n(~PCW 5–7)"),
    "6th week post-fertilization stage":     (6,    "PCW 6"),
    "10th week post-fertilization stage":    (10,   "PCW 10"),
    "11th week post-fertilization stage":    (11,   "PCW 11"),
    "12th week post-fertilization stage":    (12,   "PCW 12"),
    "13th week post-fertilization stage":    (13,   "PCW 13"),
    "15th week post-fertilization stage":    (15,   "PCW 15"),
    "16th week post-fertilization stage":    (16,   "PCW 16"),
    "17th week post-fertilization stage":    (17,   "PCW 17"),
    "19th week post-fertilization stage":    (19,   "PCW 19"),
    "20th week post-fertilization stage":    (20,   "PCW 20"),
}

# ── Tyser data (CS7–CS8 ≈ PCW 3) hardcoded ────────────────────────────────
# Maps CXG-compatible cell type → count  (types not in CXG shown separately)
TYSER_PCW = 3.0
TYSER_LABEL = "PCW ~3\n(Tyser CS7)"
TYSER_PROGENITORS: dict[str, int] = {
    # Early types with no CXG equivalent — shown as extra rows at top
    "epiblast cell":        133,
    "primitive streak":     202,
    "advanced mesoderm":    164,
    "emergent mesoderm":    185,
    "nascent mesoderm":      98,
    "axial mesoderm":        23,
    "yolk sac mesoderm":     83,
    "ectodermal cell":       29,
}
TYSER_CXG_OVERLAP: dict[str, int] = {
    # Tyser types that map to CXG cell type labels
    "hematopoietic cell":   111,   # hemogenic endothelial progenitor
    "erythrocyte":           32,
}

# Lázár DL + Xu totals (no per-PCW breakdown available)
LAZAR_DL_TOTAL  = 107_673
XU_TOTAL        =   5_243

# ── Proposed split annotation ──────────────────────────────────────────────
# Highlight certain PCW columns with a background colour
SPLIT_ANNOTATION: dict[float, dict] = {
    10: {"label": "Val", "color": "rgba(52,168,83,0.12)", "border": "#34a853"},
    20: {"label": "Val", "color": "rgba(52,168,83,0.12)", "border": "#34a853"},
    6:  {"label": "Test (option)", "color": "rgba(234,67,53,0.10)", "border": "#ea4335"},
}

# ── Lineage group colours ──────────────────────────────────────────────────
LINEAGE_COLORS: dict[str, str] = {
    "Cardiomyocyte":              "#fde8e8",
    "Endocardial / Valve":        "#fef3e2",
    "Epicardial / EPDC":          "#e6f4ea",
    "Mesenchymal / Stromal":      "#e8f0fe",
    "Vascular EC":                "#f3e8ff",
    "Immune / Haematopoietic":    "#fce7f3",
    "Neural":                     "#e0f7fa",
    "Tyser progenitors":          "#fff8e1",
}
LINEAGE_BORDER: dict[str, str] = {
    "Cardiomyocyte":              "#e57373",
    "Endocardial / Valve":        "#f59e0b",
    "Epicardial / EPDC":          "#34a853",
    "Mesenchymal / Stromal":      "#4285f4",
    "Vascular EC":                "#8b5cf6",
    "Immune / Haematopoietic":    "#ec4899",
    "Neural":                     "#00acc1",
    "Tyser progenitors":          "#fbc02d",
}

# ── Read CXG CSV ───────────────────────────────────────────────────────────

def load_cxg_data() -> tuple[list[str], dict[str, dict[str, int]]]:
    """Return (ordered_stage_cols, {cell_type: {stage_col: count}})."""
    with CXG_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    stage_cols = [c for c in rows[0].keys() if c in CXG_STAGE_MAP]

    data: dict[str, dict[str, int]] = {}
    for row in rows:
        ct = row["cell type"].strip()
        if ct in EXCLUDE or ct not in LINEAGE_MAP:
            continue
        data[ct] = {col: int(row[col] or 0) for col in stage_cols}
    return stage_cols, data


# ── Build flat row list ────────────────────────────────────────────────────

def build_rows(
    stage_cols: list[str],
    cxg_data: dict[str, dict[str, int]],
) -> list[dict]:
    """
    Return a list of row dicts ordered by lineage group then by total count desc.
    Each row: {label, lineage, cells: {col_key: count}, total, is_group_header,
               is_tyser_only, dataset}
    col_key = sort_key float (PCW value)
    """
    rows = []

    # ── Tyser-only progenitors first ──────────────────────────────────────
    rows.append({"is_group_header": True, "lineage": "Tyser progenitors",
                 "label": "Tyser early progenitors (CS7)"})
    for ct, n in sorted(TYSER_PROGENITORS.items(), key=lambda x: -x[1]):
        rows.append({
            "is_group_header": False,
            "label": ct,
            "lineage": "Tyser progenitors",
            "dataset": "Tyser",
            "cells": {TYSER_PCW: n},
            "total": n,
        })

    # ── CXG cell types by lineage group ───────────────────────────────────
    for lineage in LINEAGE_ORDER:
        members = sorted(
            [(ct, d) for ct, d in cxg_data.items() if LINEAGE_MAP[ct] == lineage],
            key=lambda x: -sum(x[1].values()),
        )
        if not members:
            continue
        rows.append({"is_group_header": True, "lineage": lineage, "label": lineage})
        for ct, stage_dict in members:
            cells: dict[float, int] = {}
            total = 0
            # CXG
            for col, count in stage_dict.items():
                pcw_key = CXG_STAGE_MAP[col][0]
                cells[pcw_key] = cells.get(pcw_key, 0) + count
                total += count
            # Tyser overlap if applicable
            if ct in TYSER_CXG_OVERLAP:
                n = TYSER_CXG_OVERLAP[ct]
                cells[TYSER_PCW] = cells.get(TYSER_PCW, 0) + n
                total += n
            rows.append({
                "is_group_header": False,
                "label": ct,
                "lineage": lineage,
                "dataset": "CXG",
                "cells": cells,
                "total": total,
            })
    return rows


# ── Dot sizing ─────────────────────────────────────────────────────────────

def dot_r(count: int, max_count: int, max_r: float = 20.0, min_r: float = 3.0) -> float:
    if count <= 0:
        return 0.0
    # log scale relative to max
    r = max_r * math.log1p(count) / math.log1p(max_count)
    return max(min_r, r)


# ── HTML generation ────────────────────────────────────────────────────────

def build_html(rows: list[dict], stage_cols: list[str]) -> str:
    # Ordered PCW columns: Tyser first, then CXG stages sorted by PCW
    pcw_cols: list[tuple[float, str]] = [(TYSER_PCW, TYSER_LABEL)]
    for col in stage_cols:
        pcw_key, label = CXG_STAGE_MAP[col]
        pcw_cols.append((pcw_key, label))

    # Find global max for dot sizing
    max_count = 1
    for row in rows:
        if row.get("is_group_header"):
            continue
        for v in row["cells"].values():
            if v > max_count:
                max_count = v

    # Geometry
    ROW_H      = 24
    COL_W      = 64
    LABEL_W    = 230
    RIGHT_W    = 80   # total count column
    TOP_H      = 90   # header area
    PAD        = 12

    n_data_rows = sum(1 for r in rows if not r.get("is_group_header"))
    n_headers   = sum(1 for r in rows if r.get("is_group_header"))
    SVG_H = TOP_H + len(rows) * ROW_H + PAD
    SVG_W = LABEL_W + len(pcw_cols) * COL_W + RIGHT_W + PAD

    svg_parts: list[str] = []

    # Background rect
    svg_parts.append(f'<rect width="{SVG_W}" height="{SVG_H}" fill="#ffffff"/>')

    # Column backgrounds (for split annotations and alternating)
    for ci, (pcw_key, _) in enumerate(pcw_cols):
        cx = LABEL_W + ci * COL_W
        ann = SPLIT_ANNOTATION.get(pcw_key)
        if ann:
            svg_parts.append(
                f'<rect x="{cx}" y="{TOP_H}" width="{COL_W}" height="{SVG_H - TOP_H}" '
                f'fill="{ann["color"]}"/>'
            )
        elif ci % 2 == 0:
            svg_parts.append(
                f'<rect x="{cx}" y="{TOP_H}" width="{COL_W}" height="{SVG_H - TOP_H}" '
                f'fill="rgba(0,0,0,0.02)"/>'
            )

    # Row backgrounds + row labels
    y = TOP_H
    for row in rows:
        lin = row["lineage"]
        bg = LINEAGE_COLORS.get(lin, "#f8f8f8")
        bdr = LINEAGE_BORDER.get(lin, "#ccc")
        if row.get("is_group_header"):
            # Group header row
            svg_parts.append(
                f'<rect x="0" y="{y}" width="{SVG_W}" height="{ROW_H}" '
                f'fill="{bdr}" opacity="0.18"/>'
            )
            svg_parts.append(
                f'<rect x="0" y="{y}" width="4" height="{ROW_H}" fill="{bdr}"/>'
            )
            svg_parts.append(
                f'<text x="8" y="{y + ROW_H - 7}" font-size="10" font-weight="700" '
                f'fill="#333" font-family="sans-serif">{row["label"].upper()}</text>'
            )
        else:
            svg_parts.append(
                f'<rect x="0" y="{y}" width="{LABEL_W}" height="{ROW_H}" '
                f'fill="{bg}"/>'
            )
            svg_parts.append(
                f'<rect x="0" y="{y}" width="4" height="{ROW_H}" fill="{bdr}"/>'
            )
            label_text = row["label"]
            svg_parts.append(
                f'<text x="10" y="{y + ROW_H - 7}" font-size="10" fill="#333" '
                f'font-family="sans-serif">{label_text}</text>'
            )
            # Total count on right
            total = row.get("total", 0)
            svg_parts.append(
                f'<text x="{LABEL_W + len(pcw_cols)*COL_W + 6}" y="{y + ROW_H - 7}" '
                f'font-size="9" fill="#666" font-family="sans-serif">'
                f'n={total:,}</text>'
            )
        y += ROW_H

    # Column headers
    for ci, (pcw_key, label) in enumerate(pcw_cols):
        cx = LABEL_W + ci * COL_W + COL_W // 2
        ann = SPLIT_ANNOTATION.get(pcw_key)
        # Dataset label (Tyser vs CXG)
        ds_label = "Tyser" if pcw_key == TYSER_PCW else "CXG"
        ds_color = "#f59e0b" if pcw_key == TYSER_PCW else "#4285f4"
        svg_parts.append(
            f'<rect x="{LABEL_W + ci*COL_W + 4}" y="4" width="{COL_W - 8}" height="14" '
            f'rx="3" fill="{ds_color}" opacity="0.85"/>'
        )
        svg_parts.append(
            f'<text x="{cx}" y="15" text-anchor="middle" font-size="9" fill="white" '
            f'font-weight="600" font-family="sans-serif">{ds_label}</text>'
        )
        # PCW label (multi-line via tspan)
        lines = label.split("\n")
        y0 = 30
        for li, ltext in enumerate(lines):
            svg_parts.append(
                f'<text x="{cx}" y="{y0 + li*13}" text-anchor="middle" font-size="10" '
                f'fill="#222" font-family="sans-serif" font-weight="600">{ltext}</text>'
            )
        # Split annotation label
        if ann:
            svg_parts.append(
                f'<text x="{cx}" y="{TOP_H - 5}" text-anchor="middle" font-size="9" '
                f'fill="{ann["border"]}" font-weight="700" font-family="sans-serif">'
                f'{ann["label"]}</text>'
            )
            svg_parts.append(
                f'<line x1="{LABEL_W + ci*COL_W}" y1="{TOP_H - 12}" '
                f'x2="{LABEL_W + ci*COL_W + COL_W}" y2="{TOP_H - 12}" '
                f'stroke="{ann["border"]}" stroke-width="1.5" stroke-dasharray="3,2"/>'
            )

    # Dots (interactive via title tooltip)
    y = TOP_H
    for row in rows:
        if row.get("is_group_header"):
            y += ROW_H
            continue
        cy = y + ROW_H // 2
        dataset = row.get("dataset", "CXG")
        dot_color = "#f59e0b" if dataset == "Tyser" else "#4285f4"
        for ci, (pcw_key, _) in enumerate(pcw_cols):
            count = row["cells"].get(pcw_key, 0)
            if count <= 0:
                y_dot = y + ROW_H
                continue
            r = dot_r(count, max_count)
            cx = LABEL_W + ci * COL_W + COL_W // 2
            svg_parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" '
                f'fill="{dot_color}" fill-opacity="0.75" stroke="{dot_color}" '
                f'stroke-width="0.5">'
                f'<title>{row["label"]} @ PCW {pcw_key}: n={count:,}</title>'
                f'</circle>'
            )
        y += ROW_H

    # Gridlines between rows
    y = TOP_H
    for row in rows:
        svg_parts.append(
            f'<line x1="0" y1="{y}" x2="{SVG_W}" y2="{y}" '
            f'stroke="#e0e0e0" stroke-width="0.5"/>'
        )
        y += ROW_H

    # Vertical grid lines between columns
    for ci in range(len(pcw_cols) + 1):
        cx = LABEL_W + ci * COL_W
        svg_parts.append(
            f'<line x1="{cx}" y1="{TOP_H}" x2="{cx}" y2="{SVG_H}" '
            f'stroke="#e0e0e0" stroke-width="0.5"/>'
        )

    # Right total header
    svg_parts.append(
        f'<text x="{LABEL_W + len(pcw_cols)*COL_W + 6}" y="{TOP_H - 5}" '
        f'font-size="10" fill="#555" font-family="sans-serif" font-weight="600">'
        f'Total</text>'
    )

    # Lázár DL + Xu note box
    note_x = LABEL_W + len(pcw_cols) * COL_W + RIGHT_W - 10
    # (rendered below SVG in HTML)

    svg_body = "\n".join(svg_parts)

    # ── Scale legend ──────────────────────────────────────────────────────
    legend_svg_parts = []
    for example_n, ex_label in [(100, "100"), (1_000, "1K"), (10_000, "10K"), (100_000, "100K")]:
        r = dot_r(example_n, max_count)
        legend_svg_parts.append((r, ex_label))

    legend_items_html = ""
    for r, lbl in legend_svg_parts:
        legend_items_html += (
            f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:14px">'
            f'<svg width="{int(r*2+2)}" height="{int(r*2+2)}">'
            f'<circle cx="{r+1}" cy="{r+1}" r="{r:.1f}" fill="#4285f4" fill-opacity="0.75"/>'
            f'</svg>'
            f'<span style="font-size:11px">{lbl}</span>'
            f'</span>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cell Coverage by PCW — Train/Val/Test Planning</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 13px; background: #f5f5f5; padding: 20px; }}
    h1 {{ font-size: 1.3rem; margin-bottom: 4px; color: #1a1a2e; }}
    .subtitle {{ color: #666; font-size: 0.82rem; margin-bottom: 14px; }}
    .legend-row {{ display:flex; flex-wrap:wrap; align-items:center; gap:10px;
                   margin-bottom:10px; }}
    .legend-badge {{ display:inline-flex; align-items:center; gap:5px;
                     padding:3px 9px; border-radius:4px; font-size:11px;
                     font-weight:600; color:#fff; }}
    .note-box {{ background:#fff8e1; border:1px solid #f59e0b; border-radius:6px;
                 padding:10px 14px; margin-top:14px; max-width:680px;
                 font-size:11px; line-height:1.6; color:#555; }}
    .note-box strong {{ color:#333; }}
    .scroll-wrap {{ overflow-x:auto; background:#fff; border:1px solid #ddd;
                    border-radius:6px; padding:10px; margin-top:8px; }}
    .split-legend {{ display:flex; gap:16px; flex-wrap:wrap; margin-bottom:8px; }}
    .split-item {{ display:inline-flex; align-items:center; gap:6px; font-size:11px; }}
    .split-swatch {{ width:14px; height:14px; border-radius:2px; }}
  </style>
</head>
<body>
  <h1>Cell Type Coverage by Developmental Stage</h1>
  <p class="subtitle">
    Dot size ∝ log(cell count). Hover over a dot for exact count.
    CellxGene data has per-PCW breakdown; Tyser (CS7) placed at PCW&nbsp;~3.
  </p>

  <div class="legend-row">
    <span style="font-size:11px;font-weight:600;color:#555">Dataset:</span>
    <span class="legend-badge" style="background:#4285f4">CXG — CellxGene heart-dev subset</span>
    <span class="legend-badge" style="background:#f59e0b">Tyser et al. 2021 (CS7)</span>
  </div>

  <div class="legend-row">
    <span style="font-size:11px;font-weight:600;color:#555">Dot size (n cells):</span>
    {legend_items_html}
  </div>

  <div class="split-legend">
    <div class="split-item">
      <div class="split-swatch" style="background:rgba(52,168,83,0.25);border:1px dashed #34a853"></div>
      <span>Proposed <strong>Val</strong> (PCW 10, 20)</span>
    </div>
    <div class="split-item">
      <div class="split-swatch" style="background:rgba(234,67,53,0.18);border:1px dashed #ea4335"></div>
      <span>Proposed <strong>Test</strong> option (PCW 6)</span>
    </div>
  </div>

  <div class="scroll-wrap">
    <svg width="{SVG_W}" height="{SVG_H}" xmlns="http://www.w3.org/2000/svg">
      {svg_body}
    </svg>
  </div>

  <div class="note-box">
    <strong>Datasets without per-PCW breakdown (not shown above):</strong><br>
    &bull; <strong>Lázár et al. (DL clusters)</strong> — {LAZAR_DL_TOTAL:,} cells total,
      spanning ~PCW 6–20+ (fetal heart atlas). Same PCW window as CXG; adds depth,
      not new timepoints.<br>
    &bull; <strong>Xu et al. 2023</strong> — {XU_TOTAL:,} cells total, fetal cardiac
      development (~PCW 4–20); includes early SHF progenitors and conduction system cells
      underrepresented in CXG.<br>
    Per-PCW breakdown for these datasets requires extracting metadata from the H5AD files.
  </div>
</body>
</html>"""
    return html


def main() -> None:
    stage_cols, cxg_data = load_cxg_data()
    rows = build_rows(stage_cols, cxg_data)
    html = build_html(rows, stage_cols)
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Written: {OUT_HTML}")


if __name__ == "__main__":
    main()
