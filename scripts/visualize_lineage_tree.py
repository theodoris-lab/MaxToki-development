#!/usr/bin/env python3
"""
Generate a standalone interactive HTML visualization of the human heart
development lineage tree, showing which cell types are present in each dataset
and how the original authors labeled them.

Usage:
    python scripts/visualize_lineage_tree.py

Output:
    cell_type_harmonization/lineage_tree_visualization.html
"""
from __future__ import annotations

from pathlib import Path

# ── Tree data ──────────────────────────────────────────────────────────────
# Each node:
#   name     : canonical cell type name shown in the tree
#   pcw      : developmental window string (e.g. "PCW 5–40"), optional
#   missing  : True → not found in any dataset (greyed out, ✗)
#   datasets : {source: [(author_label, cell_count), ...]}
#              Valid sources: "CXG" | "Tyser" | "Xu" | "Lazar_HL" | "Lazar_DL"
#   children : [child_node, ...]

TREE: dict = {
    "name": "Human Heart Development",
    "pcw": "",
    "missing": False,
    "datasets": {},
    "children": [
        # ── Epiblast → Mesoderm branch ─────────────────────────────────────
        {
            "name": "Epiblast",
            "pcw": "Day 7–14",
            "missing": False,
            "datasets": {"Tyser": [("epiblast cell", 133)]},
            "children": [
                {
                    "name": "Primitive Streak",
                    "pcw": "Day 14–16",
                    "missing": False,
                    "datasets": {"Tyser": [("primitive streak", 202)]},
                    "children": [
                        {
                            "name": "Mesoderm",
                            "pcw": "PCW 2–3",
                            "missing": False,
                            "datasets": {
                                "Tyser": [
                                    ("advanced mesoderm", 164),
                                    ("axial mesoderm", 23),
                                    ("emergent mesoderm", 185),
                                    ("nascent mesoderm", 98),
                                    ("yolk sac mesoderm", 83),
                                ]
                            },
                            "children": [
                                # ── Cardiogenic Mesoderm ──────────────────
                                {
                                    "name": "Cardiogenic Mesoderm",
                                    "pcw": "PCW 2–3",
                                    "missing": False,
                                    "datasets": {
                                        "Xu": [("Second heart field (SHF)", 373)]
                                    },
                                    "children": [
                                        # Cardiomyocyte lineage
                                        {
                                            "name": "Cardiomyocyte Lineage",
                                            "pcw": "PCW 2–8",
                                            "missing": True,
                                            "datasets": {},
                                            "children": [
                                                {
                                                    "name": "Cardiac Muscle Cell",
                                                    "pcw": "PCW 2–20",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [
                                                            ("cardiac muscle cell", 121_959),
                                                            ("fetal cardiomyocyte", 1_310),
                                                        ],
                                                        "Xu": [("cardiomyocyte", 363)],
                                                        "Lazar_HL": [
                                                            ("Immature Cardiomyocyte (Immat_CM)", 1_285),
                                                            ("Proliferating Cardiomyocyte (Prol_CM)", 7_475),
                                                            ("High TMSB10 Cluster 1 (TMSB10high_C_1)", 1_998),
                                                        ],
                                                    },
                                                    "children": [
                                                        {
                                                            "name": "Ventricular Cardiomyocyte",
                                                            "pcw": "PCW 3–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("ventricular cardiac muscle cell", 3_203)],
                                                                "Xu": [("ventricle cardiomyocyte", 972)],
                                                                "Lazar_HL": [
                                                                    ("Mature Ventricular CM (Mat_vCM)", 7_533),
                                                                    ("MetAct_vCM_1", 3_857),
                                                                    ("MetAct_vCM_2", 8_315),
                                                                ],
                                                            },
                                                            "children": [
                                                                {
                                                                    "name": "AV Bundle / Bundle Branch CM",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [
                                                                            ("AV Bundle / Bundle Branch CM (AVB-BB_CM)", 164),
                                                                        ]
                                                                    },
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Transitional / Stellate Purkinje Fiber CM",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [
                                                                            ("Transitional / Stellate Purkinje Fiber CM (TsPF_CM)", 454),
                                                                        ]
                                                                    },
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Purkinje Fiber Cell",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [
                                                                            ("Purkinje Fiber CM (PF_CM)", 279),
                                                                        ]
                                                                    },
                                                                    "children": [],
                                                                },
                                                                {"name": "Left Ventricular CM", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                {"name": "Right Ventricular CM", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                            ],
                                                        },
                                                        {
                                                            "name": "Atrial Cardiomyocyte",
                                                            "pcw": "PCW 3–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("regular atrial cardiac myocyte", 121)],
                                                                "Xu": [("atria cardiomyocyte", 595)],
                                                                "Lazar_HL": [
                                                                    ("Mature Atrial CM (Mat_aCM)", 1_201),
                                                                    ("Metabolically Active Atrial CM (MetAct_aCM)", 3_321),
                                                                ],
                                                            },
                                                            "children": [
                                                                {"name": "Left Atrial CM", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                {
                                                                    "name": "Right Atrial CM",
                                                                    "pcw": "",
                                                                    "missing": True,
                                                                    "datasets": {},
                                                                    "children": [
                                                                        {
                                                                            "name": "SA Node Pacemaker Cell",
                                                                            "pcw": "PCW 10–40",
                                                                            "missing": False,
                                                                            "datasets": {
                                                                                "Xu": [("sinoatrial node (SAN)", 105)],
                                                                                "Lazar_DL": [
                                                                                    ("SA Node CM (SAN_CM)", 299),
                                                                                ],
                                                                            },
                                                                            "children": [],
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "name": "AV Node Cell",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [
                                                                            ("AV Node CM (AVN_CM)", 147),
                                                                        ],
                                                                    },
                                                                    "children": [],
                                                                },
                                                            ],
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                        # Endocardial lineage
                                        {
                                            "name": "Endothelial / Endocardial Lineage",
                                            "pcw": "PCW 3–10",
                                            "missing": True,
                                            "datasets": {},
                                            "children": [
                                                {
                                                    "name": "Endocardial Cell",
                                                    "pcw": "PCW 5–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("endocardial cell", 10_932)],
                                                        "Xu": [("endocardium", 1_020)],
                                                        "Lazar_HL": [("Endocardial Endothelial Cell (Endoc_EC)", 6_994)],
                                                    },
                                                    "children": [
                                                        {
                                                            "name": "Atrial Septum EC",
                                                            "pcw": "PCW 8–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "Lazar_DL": [("Atrial Septum EC (AtrSept_EC)", 195)]
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "AV Canal Endocardial",
                                                            "pcw": "PCW 4–5",
                                                            "missing": False,
                                                            "datasets": {
                                                                "Xu": [("atrioventricular canal", 258)]
                                                            },
                                                            "children": [
                                                                {
                                                                    "name": "Inflow Valve EC",
                                                                    "pcw": "PCW 5–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [("Inflow Valve EC (IF_VEC)", 357)]
                                                                    },
                                                                    "children": [
                                                                        {"name": "Mitral Valve EC", "pcw": "PCW 7–40", "missing": True, "datasets": {}, "children": []},
                                                                        {"name": "Tricuspid Valve EC", "pcw": "PCW 7–40", "missing": True, "datasets": {}, "children": []},
                                                                    ],
                                                                },
                                                                {
                                                                    "name": "EndMT (AV Canal)",
                                                                    "pcw": "PCW 4–5",
                                                                    "missing": True,
                                                                    "datasets": {},
                                                                    "children": [
                                                                        {
                                                                            "name": "Endocardial Cushion",
                                                                            "pcw": "PCW 5–6",
                                                                            "missing": False,
                                                                            "datasets": {
                                                                                "Xu": [("endocardial derived cell", 503)],
                                                                                "Lazar_HL": [("Endocardial Cushion EC (EndocCush_EC)", 304)],
                                                                            },
                                                                            "children": [
                                                                                {
                                                                                    "name": "Valve Mesenchymal Cell",
                                                                                    "pcw": "PCW 6–8",
                                                                                    "missing": False,
                                                                                    "datasets": {
                                                                                        "Lazar_HL": [("Valve Mesenchymal Cell (Valve_MC)", 3_206)],
                                                                                        "Lazar_DL": [
                                                                                            ("Valve_MC_1", 961),
                                                                                            ("Valve_MC_2", 1_540),
                                                                                        ],
                                                                                    },
                                                                                    "children": [
                                                                                        {
                                                                                            "name": "Valve Interstitial Cell",
                                                                                            "pcw": "PCW 7–40",
                                                                                            "missing": False,
                                                                                            "datasets": {
                                                                                                "CXG": [("valve interstitial cell", 3)],
                                                                                                "Lazar_DL": [("Valve Interstitial Cell (VIC)", 1_360)],
                                                                                            },
                                                                                            "children": [
                                                                                                {"name": "Mitral Valve IC", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                                                {"name": "Tricuspid Valve IC", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                                            ],
                                                                                        }
                                                                                    ],
                                                                                }
                                                                            ],
                                                                        }
                                                                    ],
                                                                },
                                                            ],
                                                        },
                                                        {
                                                            "name": "Outflow Tract Endocardial",
                                                            "pcw": "PCW 4–5",
                                                            "missing": True,
                                                            "datasets": {},
                                                            "children": [
                                                                {
                                                                    "name": "Outflow Valve EC",
                                                                    "pcw": "PCW 5–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "Lazar_DL": [("Outflow Valve EC (OF_VEC)", 213)]
                                                                    },
                                                                    "children": [
                                                                        {"name": "Aortic Valve EC", "pcw": "PCW 7–40", "missing": True, "datasets": {}, "children": []},
                                                                        {"name": "Pulmonary Valve EC", "pcw": "PCW 7–40", "missing": True, "datasets": {}, "children": []},
                                                                    ],
                                                                },
                                                                {
                                                                    "name": "EndMT (OFT)",
                                                                    "pcw": "PCW 4–5",
                                                                    "missing": True,
                                                                    "datasets": {},
                                                                    "children": [
                                                                        {
                                                                            "name": "Outflow Cushion Mesenchyme",
                                                                            "pcw": "PCW 5–6",
                                                                            "missing": True,
                                                                            "datasets": {},
                                                                            "children": [
                                                                                {
                                                                                    "name": "Semilunar Valve Mesenchyme",
                                                                                    "pcw": "PCW 6–7",
                                                                                    "missing": True,
                                                                                    "datasets": {},
                                                                                    "children": [
                                                                                        {
                                                                                            "name": "Valve Interstitial Cell (OFT origin)",
                                                                                            "pcw": "PCW 7–40",
                                                                                            "missing": False,
                                                                                            "datasets": {
                                                                                                "CXG": [("valve interstitial cell", 3)],
                                                                                                "Lazar_DL": [("Valve Interstitial Cell (VIC)", 1_360)],
                                                                                            },
                                                                                            "children": [
                                                                                                {"name": "Aortic Valve IC", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                                                {"name": "Pulmonary Valve IC", "pcw": "", "missing": True, "datasets": {}, "children": []},
                                                                                            ],
                                                                                        }
                                                                                    ],
                                                                                }
                                                                            ],
                                                                        }
                                                                    ],
                                                                },
                                                            ],
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                        # Mesenchymal / Stromal lineage
                                        {
                                            "name": "Mesenchymal & Stromal Lineage",
                                            "pcw": "PCW 5–40",
                                            "missing": True,
                                            "datasets": {},
                                            "children": [
                                                {
                                                    "name": "Cardiac Mesenchymal Cell",
                                                    "pcw": "PCW 5–10",
                                                    "missing": False,
                                                    "datasets": {"CXG": [("cardiac mesenchymal cell", 12_228)]},
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Stromal Cell",
                                                    "pcw": "PCW 10–40",
                                                    "missing": False,
                                                    "datasets": {"CXG": [("stromal cell", 19_106)]},
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Mesenchymal Stem Cell",
                                                    "pcw": "PCW 5–10",
                                                    "missing": False,
                                                    "datasets": {"CXG": [("mesenchymal stem cell", 261)]},
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Fibroblast",
                                                    "pcw": "PCW 10–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "Lazar_HL": [
                                                            ("Annulus Fibrosus Fibroblast (AnnFibr_FB)", 1_345),
                                                            ("Interstitial Fibroblast (Int_FB)", 14_154),
                                                            ("Outflow Tract Fibroblast (OFT_FB)", 12_581),
                                                            ("PDE4Chigh Fibroblast (PDE4Chigh_FB)", 563),
                                                            ("Proliferating Fibroblast (Prol_FB)", 324),
                                                        ],
                                                        "Lazar_DL": [
                                                            ("Adv_FB_1", 2_129), ("Adv_FB_2", 918),
                                                            ("Int_FB_1", 2_463), ("Int_FB_2", 1_612), ("Int_FB_3", 257),
                                                            ("Prol_FB_1", 479), ("Prol_FB_2", 740),
                                                            ("AnnFibr_FB", 638), ("PDE4Chigh_FB", 696),
                                                            ("CALN1high_FB", 586), ("Infl_FB", 1_150), ("FAP", 634),
                                                        ],
                                                    },
                                                    "children": [],
                                                },
                                            ],
                                        },
                                        # Hematopoietic lineage
                                        {
                                            "name": "Hematopoietic Mesoderm",
                                            "pcw": "PCW 2–3",
                                            "missing": True,
                                            "datasets": {},
                                            "children": [
                                                {
                                                    "name": "Hematopoietic Cell",
                                                    "pcw": "PCW 3–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [
                                                            ("hematopoietic cell", 328),
                                                            ("cord blood hematopoietic stem cell", 6),
                                                            ("megakaryocyte", 439),
                                                        ],
                                                        "Tyser": [("hemogenic endothelial progenitor", 111)],
                                                    },
                                                    "children": [
                                                        {
                                                            "name": "Myeloid Cell",
                                                            "pcw": "PCW 4–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("myeloid cell", 4_621)],
                                                                "Lazar_HL": [("Myeloid Cell (MyC)", 2_016)],
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Monocyte",
                                                            "pcw": "PCW 6–40",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("monocyte", 1)]},
                                                            "children": [
                                                                {
                                                                    "name": "Macrophage",
                                                                    "pcw": "PCW 8–40",
                                                                    "missing": False,
                                                                    "datasets": {"CXG": [("macrophage", 112)]},
                                                                    "children": [],
                                                                }
                                                            ],
                                                        },
                                                        {
                                                            "name": "Neutrophil",
                                                            "pcw": "PCW 10–40",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("neutrophil", 5)]},
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Dendritic Cell",
                                                            "pcw": "PCW 8–40",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("dendritic cell", 9)]},
                                                            "children": [],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "name": "Professional APC",
                                                    "pcw": "PCW 8–40",
                                                    "missing": False,
                                                    "datasets": {"CXG": [("professional antigen presenting cell", 10)]},
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Leukocyte",
                                                    "pcw": "PCW 6–40",
                                                    "missing": False,
                                                    "datasets": {"CXG": [("leukocyte", 709)]},
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Innate Lymphoid Cell",
                                                    "pcw": "PCW 8–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("innate lymphoid cell", 3_333)],
                                                        "Lazar_HL": [("Lymphoid Cell (LyC)", 667)],
                                                    },
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Lymphoid Lineage",
                                                    "pcw": "",
                                                    "missing": True,
                                                    "datasets": {},
                                                    "children": [
                                                        {
                                                            "name": "T Cell",
                                                            "pcw": "PCW 10–40",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("T cell", 11)]},
                                                            "children": [],
                                                        }
                                                    ],
                                                },
                                                {
                                                    "name": "Erythroid Lineage",
                                                    "pcw": "",
                                                    "missing": True,
                                                    "datasets": {},
                                                    "children": [
                                                        {
                                                            "name": "Erythroid Progenitor Cell",
                                                            "pcw": "PCW 4–10",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("erythroid progenitor cell", 9)]},
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Erythroblast",
                                                            "pcw": "PCW 6–20",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("erythroblast", 7)]},
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Erythroid Lineage Cell",
                                                            "pcw": "",
                                                            "missing": False,
                                                            "datasets": {"CXG": [("erythroid lineage cell", 80)]},
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Erythrocyte",
                                                            "pcw": "PCW 8–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("erythrocyte", 99)],
                                                                "Tyser": [("erythrocyte (CS7)", 32)],
                                                            },
                                                            "children": [],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                # ── Splanchnic Mesoderm branch ────────────
                                {
                                    "name": "Splanchnic Mesoderm",
                                    "pcw": "PCW 2–3",
                                    "missing": True,
                                    "datasets": {},
                                    "children": [
                                        {
                                            "name": "Proepicardial Organ",
                                            "pcw": "PCW 4–5",
                                            "missing": True,
                                            "datasets": {},
                                            "children": [
                                                {
                                                    "name": "Epicardium",
                                                    "pcw": "PCW 4–8",
                                                    "missing": True,
                                                    "datasets": {},
                                                    "children": [
                                                        {
                                                            "name": "Mesothelial Cell of Epicardium",
                                                            "pcw": "PCW 8–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("mesothelial cell of epicardium", 2_276)],
                                                                "Xu": [("epicardium", 252)],
                                                                "Lazar_HL": [("Epicardial Cell (EpC)", 924)],
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "name": "Epicardium Derived Cell (EPDC)",
                                                            "pcw": "PCW 6–10",
                                                            "missing": False,
                                                            "datasets": {
                                                                "Xu": [("epicardial derived cell", 785)],
                                                                "Lazar_HL": [("Epicardium-Derived Cell (EPDC)", 1_956)],
                                                                "Lazar_DL": [("EPDC_1", 552), ("EPDC_2", 1_697)],
                                                            },
                                                            "children": [
                                                                {
                                                                    "name": "Cardiac Fibroblast",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {"CXG": [("fibroblast", 7_183)]},
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Vascular Smooth Muscle Cell",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "CXG": [("smooth muscle cell", 5_859)],
                                                                        "Lazar_HL": [("Coronary Artery SMC (CA_SMC)", 3_571)],
                                                                    },
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Pericyte",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": False,
                                                                    "datasets": {
                                                                        "CXG": [("pericyte", 1_134)],
                                                                        "Xu": [("pericyte (myocardium)", 17)],
                                                                        "Lazar_HL": [
                                                                            ("Pericyte (PC)", 501),
                                                                            ("Pericyte-like MC (Peric_MC)", 249),
                                                                        ],
                                                                        "Lazar_DL": [("Pericyte-like MC (Peric_MC)", 1_431)],
                                                                    },
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Coronary Endothelial Cell",
                                                                    "pcw": "PCW 10–40",
                                                                    "missing": True,
                                                                    "datasets": {},
                                                                    "children": [],
                                                                },
                                                                {
                                                                    "name": "Adipocyte",
                                                                    "pcw": "PCW 20–40",
                                                                    "missing": False,
                                                                    "datasets": {"CXG": [("adipocyte", 1)]},
                                                                    "children": [
                                                                        {
                                                                            "name": "Epicardial Adipocyte",
                                                                            "pcw": "PCW 20–40",
                                                                            "missing": False,
                                                                            "datasets": {"CXG": [("epicardial adipocyte", 2_358)]},
                                                                            "children": [],
                                                                        }
                                                                    ],
                                                                },
                                                            ],
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "name": "Vascular Endothelial Cell",
                                            "pcw": "PCW 8–40",
                                            "missing": False,
                                            "datasets": {
                                                "CXG": [
                                                    ("endothelial cell", 9_030),
                                                    ("endothelial cell of vascular tree", 6_100),
                                                ],
                                                "Lazar_HL": [
                                                    ("PDE4Chigh EC (PDE4Chigh_EC)", 1_658),
                                                    ("High TMSB10 Cluster 2 (TMSB10high_C_2)", 698),
                                                ],
                                            },
                                            "children": [
                                                {
                                                    "name": "Capillary Endothelial Cell",
                                                    "pcw": "PCW 8–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("capillary endothelial cell", 1_567)],
                                                        "Lazar_HL": [("Microvascular EC (MicroVasc_EC)", 4_553)],
                                                    },
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Arterial Endothelial Cell",
                                                    "pcw": "PCW 10–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("endothelial cell of artery", 903)],
                                                        "Lazar_HL": [("Macrovascular EC (MacroVasc_EC)", 2_120)],
                                                    },
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Venous Endothelial Cell",
                                                    "pcw": "PCW 10–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("vein endothelial cell", 248)],
                                                        "Lazar_DL": [
                                                            ("Venous EC (Ven_EC)", 166),
                                                            ("Venular EC (Venul_EC)", 133),
                                                        ],
                                                    },
                                                    "children": [],
                                                },
                                                {
                                                    "name": "Lymphatic Endothelial Cell",
                                                    "pcw": "PCW 10–40",
                                                    "missing": False,
                                                    "datasets": {
                                                        "CXG": [("endothelial cell of lymphatic vessel", 820)],
                                                        "Lazar_HL": [("Lymphatic EC (LEC)", 444)],
                                                    },
                                                    "children": [
                                                        {
                                                            "name": "Dermis Microvascular LEC",
                                                            "pcw": "PCW 10–40",
                                                            "missing": False,
                                                            "datasets": {
                                                                "CXG": [("dermis microvascular lymphatic vessel EC", 742)]
                                                            },
                                                            "children": [],
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                }
            ],
        },
        # ── Ectoderm branch ────────────────────────────────────────────────
        {
            "name": "Ectoderm",
            "pcw": "PCW 2–3",
            "missing": False,
            "datasets": {"Tyser": [("ectodermal cell", 29)]},
            "children": [
                {
                    "name": "Neural Lineage",
                    "pcw": "",
                    "missing": True,
                    "datasets": {},
                    "children": [
                        {
                            "name": "Neural Cell",
                            "pcw": "PCW 3–40",
                            "missing": False,
                            "datasets": {"CXG": [("neural cell", 1_000)]},
                            "children": [],
                        },
                        {
                            "name": "Neuron",
                            "pcw": "PCW 6–40",
                            "missing": False,
                            "datasets": {
                                "CXG": [("neuron", 2_394)],
                                "Lazar_HL": [("Neuroblast-Neuron (NB-N)", 362)],
                            },
                            "children": [
                                {
                                    "name": "Visceromotor Neuron",
                                    "pcw": "PCW 8–40",
                                    "missing": False,
                                    "datasets": {"CXG": [("visceromotor neuron", 439)]},
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "name": "Schwann Cell",
                            "pcw": "PCW 8–40",
                            "missing": False,
                            "datasets": {
                                "CXG": [("Schwann cell", 669)],
                                "Lazar_HL": [("Schwann Cell Precursor / Glia (SCP-GC)", 744)],
                            },
                            "children": [],
                        },
                    ],
                },
                {
                    "name": "Neural Crest",
                    "pcw": "PCW 3–4",
                    "missing": True,
                    "datasets": {},
                    "children": [
                        {
                            "name": "Cardiac Neural Crest Cell",
                            "pcw": "PCW 4–6",
                            "missing": True,
                            "datasets": {},
                            "children": [
                                {
                                    "name": "Outflow Tract SMC",
                                    "pcw": "PCW 8–40",
                                    "missing": False,
                                    "datasets": {
                                        "Lazar_HL": [("Outflow Tract SMC (OFT_SMC)", 3_507)]
                                    },
                                    "children": [],
                                }
                            ],
                        }
                    ],
                },
            ],
        },
    ],
}

# ── HTML rendering ─────────────────────────────────────────────────────────

DATASET_META: dict[str, tuple[str, str]] = {
    # source_key : (css_class, display_label)
    "CXG":      ("cxg",      "CXG"),
    "Tyser":    ("tyser",    "Tyser"),
    "Xu":       ("xu",       "Xu"),
    "Lazar_HL": ("lazar-hl", "Lázár HL"),
    "Lazar_DL": ("lazar-dl", "Lázár DL"),
}


def _node_to_html(node: dict) -> str:
    name = node["name"]
    pcw = node.get("pcw", "")
    missing = node.get("missing", False)
    datasets = node.get("datasets", {})
    children = node.get("children", [])

    missing_mark = " ✗" if missing else ""
    pcw_html = f'<span class="pcw">{pcw}</span>' if pcw else ""

    # Build dataset badges
    badges_html = ""
    for src, (css, label) in DATASET_META.items():
        if src not in datasets:
            continue
        entries = "".join(
            f'<div class="entry">'
            f'<span class="entry-label">{lbl}</span>'
            f'<span class="entry-count">n\u202f=\u202f{count:,}</span>'
            f'</div>'
            for lbl, count in datasets[src]
        )
        badges_html += (
            f'<div class="badge {css}">'
            f'<span class="badge-src">{label}</span>'
            f'{entries}'
            f'</div>'
        )

    has_children = bool(children)
    toggle_html = (
        '<span class="toggle" onclick="toggle(this)">&#9660;</span>'
        if has_children
        else '<span class="toggle-spacer"></span>'
    )

    node_class = "node-label missing" if missing else "node-label"
    children_html = ""
    if has_children:
        inner = "".join(_node_to_html(c) for c in children)
        children_html = f'<ul class="subtree">{inner}</ul>'

    return (
        f'<li class="tree-node">'
        f'<div class="{node_class}">'
        f'{toggle_html} '
        f'<span class="node-name">{name}{missing_mark}</span>'
        f'{pcw_html}'
        f'</div>'
        f'{badges_html}'
        f'{children_html}'
        f'</li>'
    )


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    background: #f8f9fa;
    color: #212529;
    padding: 20px;
}
h1 { font-size: 1.4rem; margin-bottom: 4px; color: #1a1a2e; }
.subtitle { color: #666; font-size: 0.85rem; margin-bottom: 12px; }

/* Legend */
.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
    align-items: center;
}
.legend-label { font-size: 0.78rem; font-weight: 600; color: #555; margin-right: 4px; }
.legend-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #fff;
}

/* Controls */
.controls { margin-bottom: 14px; }
.controls button {
    padding: 4px 12px;
    margin-right: 6px;
    font-size: 0.78rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
}
.controls button:hover { background: #e9ecef; }

/* Tree */
ul.tree, ul.subtree { list-style: none; padding-left: 0; }
ul.subtree { padding-left: 22px; border-left: 1px dashed #ced4da; margin-left: 8px; }

li.tree-node { padding: 3px 0; }

.node-label {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 3px 6px;
    border-radius: 4px;
    cursor: default;
}
.node-label:hover { background: #e9ecef; }
.node-label.missing { color: #9ca3af; }

.toggle {
    font-size: 0.7rem;
    cursor: pointer;
    color: #6c757d;
    user-select: none;
    width: 12px;
    display: inline-block;
    flex-shrink: 0;
}
.toggle-spacer { width: 12px; display: inline-block; flex-shrink: 0; }

.node-name { font-weight: 600; }
.node-label.missing .node-name { font-weight: 400; font-style: italic; }

.pcw {
    font-size: 0.72rem;
    color: #888;
    white-space: nowrap;
    padding: 1px 5px;
    background: #f0f0f0;
    border-radius: 3px;
}

/* Dataset badges */
.badge {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    gap: 4px;
    margin: 2px 0 2px 32px;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 0.72rem;
    border-left: 3px solid transparent;
}
.badge-src {
    font-weight: 700;
    font-size: 0.7rem;
    padding: 1px 5px;
    border-radius: 3px;
    color: #fff;
    white-space: nowrap;
    align-self: flex-start;
    margin-top: 1px;
}
.entry {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(255,255,255,0.55);
    border-radius: 3px;
    padding: 1px 5px;
}
.entry-label { color: #333; }
.entry-count { font-weight: 600; color: #555; }

/* Per-dataset colour scheme */
.cxg      { background: #e8f0fe; border-left-color: #4285f4; }
.cxg      .badge-src { background: #4285f4; }
.tyser    { background: #fef3e2; border-left-color: #f59e0b; }
.tyser    .badge-src { background: #f59e0b; }
.xu       { background: #e6f4ea; border-left-color: #34a853; }
.xu       .badge-src { background: #34a853; }
.lazar-hl { background: #f3e8ff; border-left-color: #8b5cf6; }
.lazar-hl .badge-src { background: #8b5cf6; }
.lazar-dl { background: #fce7f3; border-left-color: #ec4899; }
.lazar-dl .badge-src { background: #ec4899; }
"""

JS = """
function toggle(el) {
    const li = el.closest('.tree-node');
    const subtree = li.querySelector(':scope > .subtree');
    if (!subtree) return;
    const collapsed = subtree.style.display === 'none';
    subtree.style.display = collapsed ? '' : 'none';
    el.innerHTML = collapsed ? '&#9660;' : '&#9654;';
}

function expandAll() {
    document.querySelectorAll('.subtree').forEach(el => el.style.display = '');
    document.querySelectorAll('.toggle').forEach(el => el.innerHTML = '&#9660;');
}

function collapseAll() {
    // Collapse everything except the root's direct subtree
    const root = document.querySelector('ul.tree > li > ul.subtree');
    document.querySelectorAll('.subtree').forEach(el => {
        if (el !== root) el.style.display = 'none';
    });
    document.querySelectorAll('.toggle').forEach(el => el.innerHTML = '&#9654;');
    if (root) {
        root.style.display = '';
        const rootToggle = document.querySelector('ul.tree > li .toggle');
        if (rootToggle) rootToggle.innerHTML = '&#9660;';
    }
}
"""


def main() -> None:
    out_path = (
        Path(__file__).parent.parent
        / "cell_type_harmonization"
        / "lineage_tree_visualization.html"
    )

    tree_html = f'<ul class="tree">{_node_to_html(TREE)}</ul>'

    legend_badges = "".join(
        f'<span class="legend-badge" style="background:{color}">{label}</span>'
        for color, label in [
            ("#4285f4", "CXG — CellxGene heart-dev subset"),
            ("#f59e0b", "Tyser — Tyser et al. 2021"),
            ("#34a853", "Xu — Xu et al. 2023/24"),
            ("#8b5cf6", "Lázár HL — Heart-Lung Atlas (35 clusters)"),
            ("#ec4899", "Lázár DL — Deep-Learning sub-atlas (74 clusters)"),
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Human Heart Development Lineage Tree</title>
  <style>{CSS}</style>
</head>
<body>
  <h1>Human Heart Development Lineage Tree</h1>
  <p class="subtitle">
    Cell types available in our datasets, with author-assigned labels and cell counts.
    Italicised nodes marked <strong>✗</strong> have no cells in any of our four datasets.
  </p>

  <div class="legend">
    <span class="legend-label">Datasets:</span>
    {legend_badges}
  </div>

  <div class="controls">
    <button onclick="expandAll()">Expand all</button>
    <button onclick="collapseAll()">Collapse all</button>
  </div>

  {tree_html}

  <script>{JS}</script>
</body>
</html>"""

    out_path.write_text(html, encoding="utf-8")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
