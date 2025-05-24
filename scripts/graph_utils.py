# scripts/graph_utils.py

import pandas as pd
import networkx as nx
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent
CLEAN_DIR = REPO_ROOT / "data" / "clean"
CACHE_DIR = CLEAN_DIR / "graph_cache"
CACHE_DIR.mkdir(exist_ok=True)

def load_clean_df(threshold=0, start_date=None, end_date=None):
    """Load the preprocessed pickle and optionally slice by date."""
    fn = CLEAN_DIR / f"pepe_clean_min{threshold}.pkl"
    df = pd.read_pickle(fn)
    if start_date:
        df = df[df.date >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.date <= pd.to_datetime(end_date)]
    return df

def _cache_path(threshold, kind, start_date, end_date):
    """Helper to pick a cache filename."""
    name = f"G_{kind}_min{threshold}"
    if start_date or end_date:
        name += f"_{start_date or ''}_{end_date or ''}"
    return CACHE_DIR / f"{name}.gpickle"

def build_unweighted_graph(df, threshold=0, start_date=None, end_date=None, use_cache=True):
    """
    Build (or load) the unweighted DiGraph for this df slice.
    If use_cache=True, first try to load a .gpickle; if missing, build+save.
    """
    cache = _cache_path(threshold, "unw", start_date, end_date)
    if use_cache and cache.exists():
        return nx.read_gpickle(cache)

    G = nx.DiGraph()
    G.add_edges_from(zip(df.from_address, df.to_address))

    if use_cache:
        nx.write_gpickle(G, cache)
    return G

def build_weighted_graph(df, threshold=0, start_date=None, end_date=None, use_cache=True):
    """
    Build (or load) the weighted DiGraph for this df slice.
    Edge attribute `weight` = sum of value_token.
    """
    cache = _cache_path(threshold, "w", start_date, end_date)
    if use_cache and cache.exists():
        return nx.read_gpickle(cache)

    G = nx.DiGraph()
    for u, v, w in zip(df.from_address, df.to_address, df.value_token):
        if G.has_edge(u, v):
            G[u][v]["weight"] += w
        else:
            G.add_edge(u, v, weight=w)

    if use_cache:
        nx.write_gpickle(G, cache)
    return G
