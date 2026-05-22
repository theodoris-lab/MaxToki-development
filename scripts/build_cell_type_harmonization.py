#!/usr/bin/env python3
"""Build a cell-type harmonization dictionary linked to the lineage tree.

Outputs:
- dump/cell_type_harmonization_table.csv
- dump/cell_type_harmonization_map.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Lineage paths: canonical label → ordered list of ancestors from root
# ---------------------------------------------------------------------------
LINEAGE_PATHS: Dict[str, List[str]] = {
    # Early lineage nodes
    "Epiblast": ["Epiblast"],
    "Ectoderm": ["Epiblast", "Ectoderm"],
    "Primitive Streak": ["Epiblast", "Primitive Streak"],
    "Mesoderm": ["Epiblast", "Primitive Streak", "Mesoderm"],
    "Cardiogenic Mesoderm": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
    ],
    # Cardiomyocyte lineage
    "Cardiac Muscle Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Cardiomyocyte Lineage", "Cardiac Muscle Cell",
    ],
    "Ventricular Cardiomyocytes": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Cardiomyocyte Lineage", "Cardiac Muscle Cell", "Ventricular Cardiomyocytes",
    ],
    "Regular Atrial Cardiac Myocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Cardiomyocyte Lineage", "Cardiac Muscle Cell", "Regular Atrial Cardiac Myocyte",
    ],
    "SA Node Pacemaker Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Cardiomyocyte Lineage", "Cardiac Muscle Cell",
        "Regular Atrial Cardiac Myocyte", "SA Node Pacemaker Cell",
    ],
    # Endocardial / endothelial lineage
    "Endocardial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Endothelial / Endocardial Lineage", "Endocardial Cell",
    ],
    "AV Canal Endocardial Cells": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Endothelial / Endocardial Lineage", "Endocardial Cell",
        "AV Canal Endocardial Cells",
    ],
    "Endocardial Cushion": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Endothelial / Endocardial Lineage", "Endocardial Cell",
        "AV Canal Endocardial Cells", "Endocardial Cushion",
    ],
    "Valve Mesenchymal Cells": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Endothelial / Endocardial Lineage", "Endocardial Cell",
        "AV Canal Endocardial Cells", "Endocardial Cushion", "Valve Mesenchymal Cells",
    ],
    "Valve Interstitial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Endothelial / Endocardial Lineage", "Endocardial Cell",
        "AV Canal Endocardial Cells", "Endocardial Cushion",
        "Valve Mesenchymal Cells", "Valve Interstitial Cell",
    ],
    # Mesenchymal / Stromal lineage
    "Cardiac Mesenchymal Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Mesenchymal and Stromal Lineage", "Cardiac Mesenchymal Cell",
    ],
    "Stromal Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Mesenchymal and Stromal Lineage", "Stromal Cell",
    ],
    "Mesenchymal Stem Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Mesenchymal and Stromal Lineage", "Mesenchymal Stem Cell",
    ],
    "Fibroblast": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Cardiogenic Mesoderm",
        "Mesenchymal and Stromal Lineage", "Fibroblast",
    ],
    # Hematopoietic lineage
    "Hematopoietic Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell",
    ],
    "Myeloid Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Myeloid Cell",
    ],
    "Monocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Monocyte",
    ],
    "Macrophage": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Monocyte", "Macrophage",
    ],
    "Neutrophil": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Neutrophil",
    ],
    "Dendritic Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Dendritic Cell",
    ],
    "Professional Antigen Presenting Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Professional Antigen Presenting Cell",
    ],
    "Leukocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Hematopoietic Cell", "Leukocyte",
    ],
    "Innate Lymphoid Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Innate Lymphoid Cell",
    ],
    "T Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Lymphoid Lineage", "T Cell",
    ],
    "Erythroid Progenitor Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Erythroid Lineage", "Erythroid Progenitor Cell",
    ],
    "Erythroblast": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Erythroid Lineage", "Erythroblast",
    ],
    "Erythroid Lineage Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Erythroid Lineage", "Erythroid Lineage Cell",
    ],
    "Erythrocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm",
        "Hematopoietic Mesoderm", "Erythroid Lineage", "Erythrocyte",
    ],
    # Epicardial lineage (from Splanchnic Mesoderm)
    "Mesothelial Cell of Epicardium": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Mesothelial Cell of Epicardium",
    ],
    "Epicardium Derived Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell",
    ],
    "Cardiac Fibroblast": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell", "Cardiac Fibroblast",
    ],
    "Vascular Smooth Muscle Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell",
        "Vascular Smooth Muscle Cell",
    ],
    "Pericyte": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell", "Pericyte",
    ],
    "Adipocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell", "Adipocyte",
    ],
    "Epicardial Adipocyte": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Proepicardial Organ", "Epicardium", "Epicardium Derived Cell",
        "Adipocyte", "Epicardial Adipocyte",
    ],
    # Vascular Endothelial lineage (from Splanchnic Mesoderm)
    "Vascular Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell",
    ],
    "Capillary Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell", "Capillary Endothelial Cell",
    ],
    "Arterial Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell", "Arterial Endothelial Cell",
    ],
    "Venous Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell", "Venous Endothelial Cell",
    ],
    "Lymphatic Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell", "Lymphatic Endothelial Cell",
    ],
    "Dermis Microvascular Lymphatic Endothelial Cell": [
        "Epiblast", "Primitive Streak", "Mesoderm", "Splanchnic Mesoderm",
        "Vascular Endothelial Cell", "Lymphatic Endothelial Cell",
        "Dermis Microvascular Lymphatic Endothelial Cell",
    ],
    # Neural lineage (from Ectoderm / Neural Crest)
    "Neural Cell": ["Epiblast", "Ectoderm", "Neural Lineage", "Neural Cell"],
    "Neuron": ["Epiblast", "Ectoderm", "Neural Lineage", "Neuron"],
    "Visceromotor Neuron": [
        "Epiblast", "Ectoderm", "Neural Lineage", "Neuron", "Visceromotor Neuron",
    ],
    "Schwann Cell": ["Epiblast", "Ectoderm", "Neural Lineage", "Schwann Cell"],
    "Outflow Tract Smooth Muscle Cell": [
        "Epiblast", "Ectoderm", "Neural Crest", "Cardiac Neural Crest Cell",
        "Outflow Tract Smooth Muscle Cell",
    ],
}

STRATEGY_TO_CONFIDENCE: Dict[str, str] = {
    "exact_tree_alias": "high",
    "manual_override": "medium",
    "heuristic_ventricular_cm": "low",
    "heuristic_atrial_cm": "low",
    "heuristic_endocardial": "low",
    "heuristic_fibroblast": "low",
    "heuristic_smc": "low",
    "heuristic_lymphatic_ec": "low",
    "unmapped": "none",
}


@dataclass
class TreeEntry:
    canonical: str
    aliases: Set[str]
    raw_line: str


def strip_accents(text: str) -> str:
    """Convert accented characters to ASCII equivalents (e.g. á → a)."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )


def normalize_label(text: str) -> str:
    text = text.strip()
    text = text.replace("*", "")
    text = re.sub(r"[’`\"]", "'", text)
    text = re.sub(r"\(.*?\)", " ", text)
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def clean_tree_cell_type_segment(line: str) -> str:
    line = line.split("[")[0].strip()
    line = re.sub(r"\([^)]*\)", " ", line)
    line = line.replace("*", "")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def parse_tree_entries(tree_path: Path) -> List[TreeEntry]:
    entries: List[TreeEntry] = []
    seen_canonicals: Set[str] = set()

    for raw in tree_path.read_text(encoding="utf-8").splitlines():
        if "*" not in raw:
            continue
        if "-->" in raw and "*" not in raw.split("-->")[-1]:
            continue

        segment = re.sub(r"^[^A-Za-z0-9*]+", "", raw)
        segment = clean_tree_cell_type_segment(segment)
        if not segment:
            continue

        aliases = [a.strip() for a in segment.split("/") if a.strip()]
        if not aliases:
            continue

        canonical = aliases[0]
        if canonical in seen_canonicals:
            continue

        seen_canonicals.add(canonical)
        entries.append(TreeEntry(canonical=canonical, aliases=set(aliases), raw_line=raw.rstrip()))

    return entries


def extract_survey_cell_types(survey_report: Path) -> List[Tuple[str, str]]:
    text = survey_report.read_text(encoding="utf-8")
    pairs: List[Tuple[str, str]] = []

    section_start = text.find("## Section 2:")
    section_end = text.find("## Section 3:")
    if section_start != -1 and section_end != -1 and section_end > section_start:
        text = text[section_start:section_end]

    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue

        parts = [p.strip() for p in line.strip().split("|")]
        if len(parts) < 5:
            continue

        category = parts[1]
        cell_type = parts[2]
        src = parts[3]

        if category in {"", "Category", "---"}:
            continue
        if cell_type in {"", "Cell Type", "---"}:
            continue
        if category.startswith("**"):
            continue

        # Use accent-stripped lowercase for source matching (handles Lázár → lazar)
        src_plain = strip_accents(src).lower().strip()
        if not any(s in src_plain for s in ["cxg", "xu", "tyser", "laz"]):
            continue

        pairs.append((cell_type, src))

    return sorted(set(pairs), key=lambda x: (x[0].lower(), x[1].lower()))


def build_tree_alias_index(tree_entries: List[TreeEntry]) -> Dict[str, str]:
    idx: Dict[str, str] = {}
    for e in tree_entries:
        idx[normalize_label(e.canonical)] = e.canonical
        for alias in e.aliases:
            idx[normalize_label(alias)] = e.canonical
    return idx


def get_manual_overrides() -> Dict[str, Optional[str]]:
    return {
        "native cell": None,
        "unknown": None,
        "unassigned cluster 0": None,
        "heart lung atlas excluded 1": None,
        "heart lung atlas excluded 2": None,
        "metabolically active ventricular cardiomyocyte 1": "Ventricular Cardiomyocytes",
        "metabolically active ventricular cardiomyocyte 2": "Ventricular Cardiomyocytes",
        "mature ventricular cardiomyocyte": "Ventricular Cardiomyocytes",
        "proliferating cardiomyocyte": "Cardiac Muscle Cell",
        "immature cardiomyocyte": "Cardiac Muscle Cell",
        "mature atrial cardiomyocyte": "Regular Atrial Cardiac Myocyte",
        "metabolically active atrial cardiomyocyte": "Regular Atrial Cardiac Myocyte",
        "outflow tract smooth muscle cell": "Outflow Tract Smooth Muscle Cell",
        "coronary artery smooth muscle cell": "Vascular Smooth Muscle Cell",
        "microvascular endothelial cell": "Capillary Endothelial Cell",
        "endocardial endothelial cell": "Endocardial Cell",
        "endocardial cushion endothelial cell": "Endocardial Cushion",
        "outflow tract fibroblast": "Fibroblast",
        "interstitial fibroblast": "Fibroblast",
        "annulus fibrosus fibroblast": "Fibroblast",
        "valve mesenchymal cell": "Valve Mesenchymal Cells",
        "epicardium derived cell": "Epicardium Derived Cell",
        "epicardial cell": "Mesothelial Cell of Epicardium",
        "myeloid cell": "Myeloid Cell",
        "pericardial mesenchymal cell": "Pericyte",
        # Lázár combined label "Pericyte-like Mesenchymal Cell / Pericyte* (Peric_MC)"
        # normalizes with trailing " pericyte" due to the slash
        "pericyte like mesenchymal cell pericyte": "Pericyte",
        "endothelial cell": "Vascular Endothelial Cell",
        "epicardial derived cell": "Epicardium Derived Cell",
        "epicardium": "Mesothelial Cell of Epicardium",
        "megakaryocyte": "Hematopoietic Cell",
        "cord blood hematopoietic stem cell": "Hematopoietic Cell",
        "second heart field": "Cardiogenic Mesoderm",
        "atrioventricular canal": "AV Canal Endocardial Cells",
        "sinoatrial node": "SA Node Pacemaker Cell",
        "endocardial derived cell": "Endocardial Cushion",
        "endocardium": "Endocardial Cell",
        "ventricle cardiomyocyte": "Ventricular Cardiomyocytes",
        "atria cardiomyocyte": "Regular Atrial Cardiac Myocyte",
        "cardiomyocyte": "Cardiac Muscle Cell",
        "primitive streak": "Primitive Streak",
        "emergent mesoderm": "Mesoderm",
        "advanced mesoderm": "Mesoderm",
        "nascent mesoderm": "Mesoderm",
        "axial mesoderm": "Mesoderm",
        "epiblast cell": "Epiblast",
        "endodermal cell": None,
        "hemogenic endothelial progenitor": "Hematopoietic Cell",
        "yolk sac mesoderm": "Mesoderm",
        "ectodermal cell": "Ectoderm",
        "erythrocyte cs7": "Erythrocyte",
        "unassigned": None,
    }


def best_effort_match(
    norm: str,
    tree_alias_index: Dict[str, str],
    overrides: Dict[str, Optional[str]],
) -> Tuple[Optional[str], str]:
    if norm in tree_alias_index:
        return tree_alias_index[norm], "exact_tree_alias"

    if norm in overrides:
        return overrides[norm], "manual_override"

    if "ventricular" in norm and "cardio" in norm:
        return tree_alias_index.get(normalize_label("Ventricular Cardiomyocytes")), "heuristic_ventricular_cm"
    if "atrial" in norm and "cardio" in norm:
        return tree_alias_index.get(normalize_label("Regular Atrial Cardiac Myocyte")), "heuristic_atrial_cm"
    if "endocard" in norm and "endothelial" in norm:
        return tree_alias_index.get(normalize_label("Endocardial Cell")), "heuristic_endocardial"
    if "fibroblast" in norm:
        return tree_alias_index.get(normalize_label("Fibroblast")), "heuristic_fibroblast"
    if "smooth muscle" in norm:
        return tree_alias_index.get(normalize_label("Vascular Smooth Muscle Cell")), "heuristic_smc"
    if "lymphatic" in norm and "endothelial" in norm:
        return tree_alias_index.get(normalize_label("Lymphatic Endothelial Cell")), "heuristic_lymphatic_ec"

    return None, "unmapped"


def build_outputs(tree_entries: List[TreeEntry], observed: List[Tuple[str, str]]) -> Tuple[List[Dict[str, str]], Dict[str, dict]]:
    tree_alias_index = build_tree_alias_index(tree_entries)
    overrides = get_manual_overrides()

    rows: List[Dict[str, str]] = []
    by_canonical: Dict[str, dict] = defaultdict(lambda: {"synonyms": set(), "sources": set()})

    for observed_label, source in observed:
        norm = normalize_label(observed_label)
        canonical, strategy = best_effort_match(norm, tree_alias_index, overrides)

        mapped = canonical is not None
        canonical_out = canonical if canonical else "UNMAPPED"
        confidence = STRATEGY_TO_CONFIDENCE.get(strategy, "none")
        path = LINEAGE_PATHS.get(canonical_out, []) if mapped else []
        path_str = " → ".join(path)

        rows.append(
            {
                "observed_label": observed_label,
                "source": source,
                "normalized_observed_label": norm,
                "canonical_tree_label": canonical_out,
                "mapping_status": "mapped" if mapped else "unmapped",
                "mapping_strategy": strategy,
                "confidence_tier": confidence,
                "lineage_path": path_str,
            }
        )

        if mapped:
            by_canonical[canonical]["synonyms"].add(observed_label)
            by_canonical[canonical]["sources"].add(source)

    harmonization_map: Dict[str, dict] = {}
    for canonical, payload in sorted(by_canonical.items(), key=lambda kv: kv[0].lower()):
        harmonization_map[canonical] = {
            "synonyms": sorted(payload["synonyms"], key=lambda s: s.lower()),
            "sources": sorted(payload["sources"]),
            "lineage_path": LINEAGE_PATHS.get(canonical, []),
            "lineage_path_str": " → ".join(LINEAGE_PATHS.get(canonical, [])),
            "linked_to_lineage_tree": True,
        }

    return rows, harmonization_map


_CSV_FIELDS = [
    "observed_label",
    "source",
    "normalized_observed_label",
    "canonical_tree_label",
    "mapping_status",
    "mapping_strategy",
    "confidence_tier",
    "lineage_path",
]


def write_csv(rows: List[Dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_review_queue(rows: List[Dict[str, str]], out_path: Path) -> None:
    """Write only medium/low/none-confidence rows for human curation."""
    review_rows = [r for r in rows if r["confidence_tier"] != "high"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(review_rows)


def write_json(harmonization_map: Dict[str, dict], tree_entries: List[TreeEntry], out_path: Path) -> None:
    tree_lookup = {e.canonical: sorted(e.aliases) for e in tree_entries}
    payload = {
        "metadata": {
            "description": "Canonical cell-type harmonization map anchored to human heart development lineage tree",
            "canonical_count": len(harmonization_map),
            "tree_anchor_count": len(tree_entries),
        },
        "lineage_tree_aliases": tree_lookup,
        "harmonization_map": harmonization_map,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")




def main() -> None:
    parser = argparse.ArgumentParser(description="Build lineage-linked cell-type harmonization outputs")
    parser.add_argument(
        "--tree",
        type=Path,
        default=Path("documents/human_heart_development_lineage_tree.txt"),
        help="Path to lineage tree text file",
    )
    parser.add_argument(
        "--survey-report",
        type=Path,
        default=Path("documents/maxtoki_heart_development_data_survey_report.md"),
        help="Path to survey report markdown with cross-dataset cell-type table",
    )
    parser.add_argument(
        "--out-csv",
        type=Path,
        default=Path("cell_type_harmonization/cell_type_harmonization_table.csv"),
        help="Output CSV path for observed->canonical mapping",
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("cell_type_harmonization/cell_type_harmonization_map.json"),
        help="Output JSON path for canonical map and synonyms",
    )
    parser.add_argument(
        "--out-review",
        type=Path,
        default=Path("cell_type_harmonization/cell_type_harmonization_review_queue.csv"),
        help="Output CSV for non-high-confidence rows requiring human review",
    )
    args = parser.parse_args()

    tree_entries = parse_tree_entries(args.tree)
    observed = extract_survey_cell_types(args.survey_report)
    rows, harmonization_map = build_outputs(tree_entries, observed)

    write_csv(rows, args.out_csv)
    write_review_queue(rows, args.out_review)
    write_json(harmonization_map, tree_entries, args.out_json)

    mapped = sum(1 for r in rows if r["mapping_status"] == "mapped")
    high   = sum(1 for r in rows if r["confidence_tier"] == "high")
    medium = sum(1 for r in rows if r["confidence_tier"] == "medium")
    low    = sum(1 for r in rows if r["confidence_tier"] == "low")
    total  = len(rows)
    pct = (mapped / total * 100) if total else 0.0

    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_json}")
    print(f"Wrote {args.out_review}")
    print(f"\nMapping summary: {mapped}/{total} labels mapped ({pct:.1f}%)")
    print(f"  High confidence  (exact tree alias) : {high}")
    print(f"  Medium confidence (manual override)  : {medium}")
    print(f"  Low confidence   (heuristic)         : {low}")
    print(f"  Unmapped                             : {total - mapped}")
    print(f"\nReview queue: {total - high} labels → {args.out_review}")


if __name__ == "__main__":
    main()
