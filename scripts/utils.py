#!/usr/bin/env python3
"""Shared utility functions for data-curation scripts."""

from __future__ import annotations

import re
import unicodedata


def strip_accents(text: str) -> str:
    """Convert accented characters to ASCII equivalents (e.g. á → a)."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )


def normalize_label(text: str) -> str:
    """Normalize a cell-type label for fuzzy matching.

    Strips asterisks, punctuation, parentheticals, slashes, hyphens, and
    extra whitespace, then lowercases for case-insensitive comparison.
    """
    text = text.strip().replace("*", "")
    text = re.sub(r"['`\"]", "'", text)
    text = re.sub(r"\(.*?\)", " ", text)
    text = text.replace("/", " ").replace("-", " ")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()
