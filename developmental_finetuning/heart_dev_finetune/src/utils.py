#!/usr/bin/env python3
"""Shared utilities for the heart-development fine-tuning pipeline."""

from __future__ import annotations

import pickle
from pathlib import Path


def load_token_dictionary(path: Path) -> dict:
    """Load a Geneformer/MaxToki token dictionary from a pickle file."""
    with path.open("rb") as handle:
        return pickle.load(handle)
