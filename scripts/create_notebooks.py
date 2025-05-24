#!/usr/bin/env python3
import os
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

# ─── Notebook Definitions ───────────────────────────────────────────────────
NOTEBOOKS = [
    ("01_degree_distribution.ipynb",       "# 01 Degree Distribution"),
    ("02_global_summaries.ipynb",          "# 02 Global Network Summaries"),
    ("03_centrality.ipynb",                "# 03 Centrality Measures"),
    ("04_kcore.ipynb",                     "# 04 k-Core Decomposition"),
    ("05_clustering_assortativity.ipynb",  "# 05 Clustering & Assortativity"),
    ("06_communities.ipynb",               "# 06 Community Detection"),
    ("07_temporal_snapshots.ipynb",        "# 07 Temporal Snapshot Comparison"),
    ("08_robustness.ipynb",                "# 08 Robustness / Percolation"),
]

# ─── Paths Setup ────────────────────────────────────────────────────────────
repo_root = Path(__file__).parent.parent
nb_dir    = repo_root / "notebooks"
nb_dir.mkdir(exist_ok=True)

# ─── Common Path-Fix + Imports Cell ─────────────────────────────────────────
# Add project root (one level up from notebooks/) to sys.path
path_fix = """# ── Path-Fix for Imports ───────────────────────────────────────────────────
import sys
from pathlib import Path
# Prepend parent directory (repo root) to sys.path
sys.path.insert(0, str(Path().resolve().parent))

# ── Standard Imports ───────────────────────────────────────────────────────────
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.graph_utils import load_clean_df, build_unweighted_graph, build_weighted_graph

sns.set(style=\"whitegrid\")"""

# ─── Generate Notebooks ───────────────────────────────────────────────────── ─────────────────────────────────────────────────────
for fname, title in NOTEBOOKS:
    path = nb_dir / fname
    if path.exists():
        print(f"Skipping existing {fname}")
        continue

    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(title),
        new_code_cell(path_fix),
        new_markdown_cell("## Analysis goes here…"),
    ]

    with path.open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Created {fname}")

print("All notebooks generated in notebooks/")
