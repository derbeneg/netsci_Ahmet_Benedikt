#!/usr/bin/env python3
"""
scripts/preprocess.py  (full debug version)

We added debug statements to verify that:
  1. We have the correct CSV in data/
  2. The CSV contains the expected columns and mixed from/to pairs
  3. Only then do we proceed to remove self-transfers, etc.
"""

import pandas as pd
from pathlib import Path

def transform_data(df: pd.DataFrame, min_degree: int = 0) -> pd.DataFrame:
    df = df.copy()
    print(f"[transform_data] Starting with {len(df)} rows, min_degree={min_degree}")

    # 1) Parse dates
    df["date"] = pd.to_datetime(df["date"])
    print(f"[transform_data] Dates parsed, nulls: {df['date'].isna().sum()}")

    # 2) Keep only core columns
    df = df[["date", "from_address", "to_address", "value_token"]]
    print(f"[transform_data] Kept columns, row count still: {len(df)}")

    # 3) Count raw self-loops
    raw_loops = (df["from_address"] == df["to_address"]).sum()
    print(f"[transform_data] Raw self-loops: {raw_loops}/{len(df)} rows")

    # 4) Show a small sample to eyeball
    print(df[["from_address","to_address"]].sample(5, random_state=42).to_string(index=False))

    # 5) Remove self-transfers
    df = df[df["from_address"] != df["to_address"]]
    print(f"[transform_data] After removing self-loops: {len(df)} rows")

    # 6) Activity filter if needed
    if min_degree > 0:
        counts = pd.concat([
                df["from_address"].value_counts(),
                df["to_address"].value_counts()
            ]).groupby(level=0).sum()
        active = counts[counts >= min_degree].index
        print(f"[transform_data] Addresses with ≥{min_degree} tx: {len(active)}")
        before = len(df)
        df = df[
            df["from_address"].isin(active) |
            df["to_address"].isin(active)
        ]
        print(f"[transform_data] After activity filter: {len(df)} (was {before})")

    return df

def main():
    repo_root = Path(__file__).parent.parent.resolve()
    data_dir  = repo_root / "data"
    raw_csv   = data_dir / "pepe-transfers-etherscan.csv"
    clean_dir = data_dir / "clean"

    # A) List files in data/ to confirm we have the right CSV
    print(f"[main] Files in {data_dir}:")
    for f in data_dir.iterdir():
        print("   ", f.name)
    print()

    # B) Load raw CSV and inspect columns & head
    print(f"[main] Loading raw CSV from {raw_csv}")
    df_raw = pd.read_csv(raw_csv)
    print(f"[main] Raw shape: {df_raw.shape}")
    print(f"[main] Columns: {list(df_raw.columns)}")
    print("[main] First 5 rows:")
    print(df_raw.head().to_string(index=False))
    print()

    # Prepare clean directory
    clean_dir.mkdir(parents=True, exist_ok=True)

    # C) Process thresholds
    thresholds = [0, 5, 10, 20]
    for thr in thresholds:
        print(f"[main] ----- Processing threshold {thr} -----")
        df_clean = transform_data(df_raw, min_degree=thr)
        out_path = clean_dir / f"pepe_clean_min{thr}.pkl"
        df_clean.to_pickle(out_path)
        print(f"[main] --> Saved min_degree={thr} → {len(df_clean)} rows to {out_path.name}\n")

if __name__ == "__main__":
    main()
