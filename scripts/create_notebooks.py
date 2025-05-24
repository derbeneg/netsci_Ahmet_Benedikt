#!/usr/bin/env python3
import os
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

# 1. Define your notebook specs (filename → title)
NOTEBOOKS = [
    ("01_degree_distribution.ipynb", "# 01 Degree Distribution"),
    ("02_global_summaries.ipynb", "# 02 Global Network Summaries"),
    ("03_centrality.ipynb", "# 03 Centrality Measures"),
    ("04_kcore.ipynb", "# 04 k-Core Decomposition"),
    ("05_clustering_assortativity.ipynb", "# 05 Clustering & Assortativity"),
    ("06_communities.ipynb", "# 06 Community Detection"),
    ("07_temporal_snapshots.ipynb", "# 07 Temporal Snapshot Comparison"),
    ("08_robustness.ipynb", "# 08 Robustness / Percolation"),
    # add any extras here
]

# 2. Make sure the notebooks/ dir exists
repo_root = Path(__file__).parent.parent
nb_dir = repo_root / "notebooks"
nb_dir.mkdir(exist_ok=True)

# 3. Common import cell
imports = """\
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.graph_utils import load_clean_df, build_unweighted_graph, build_weighted_graph

sns.set(style="whitegrid")
"""

for fname, title in NOTEBOOKS:
    path = nb_dir / fname
    if path.exists():
        print(f"Skipping existing {fname}")
        continue

    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(title),
        new_code_cell(imports),
        new_markdown_cell("## Analysis goes here…"),
    ]

    with path.open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Created {fname}")

print("All notebooks generated in notebooks/")  
