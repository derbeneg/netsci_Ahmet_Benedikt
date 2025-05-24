import time
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path


# ─── CONFIG ────────────────────────────────────────────────────────
API_KEY    = "RQHXUAGGC...TWUQ7EB6WK5BFR" # shortened for security
CONTRACT   = "0x6982508145454ce325ddbe47a25d4ec3d2311933"  # PEPE token
BASE_URL   = "https://api.etherscan.io/api"
OUT_CSV     = Path(__file__).parent.parent / "data" / "pepe-transfers-etherscan.csv"

# Time window (inclusive)
START_DT = datetime(2023, 4, 14, 0, 0, 0)
END_DT   = datetime(2023, 5, 31, 23, 59, 59)

# ─── FETCH & FILTER ───────────────────────────────────────────────
all_txs = []
per_page = 10_000
start_block = 0     # initial startblock
end_block   = 99999999

print("🔍 Starting fetch from Etherscan…\n")
while True:
    params = {
        "module":          "account",
        "action":          "tokentx",
        "contractaddress": CONTRACT,
        "page":            1,
        "offset":          per_page,
        "startblock":      start_block,
        "endblock":        99999999,
        "sort":            "asc",
        "apikey":          API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=15)
    js   = resp.json()
    if js.get("status") != "1" or js.get("result") is None:
        print(f"⚠️ API error or no data: {js.get('message')}\n")
        break

    batch = js["result"]
    if not batch:
        print("⏹ No more transactions; exiting loop.\n")
        break

    # Process this batch
    max_block = start_block
    new_count = 0
    for tx in batch:
        blk = int(tx["blockNumber"])
        ts  = int(tx["timeStamp"])
        dt  = datetime.utcfromtimestamp(ts)
        max_block = max(max_block, blk)

        # Skip pre-start
        if dt < START_DT:
            continue
        # If beyond end date, signal full stop
        if dt > END_DT:
            print("⏹ Reached end date in data; stopping fetch.\n")
            batch = []      # clear so we know to break outer
            start_block = max_block + 1
            break

        # Otherwise keep it
        all_txs.append({
            "block_number": blk,
            "timestamp":    ts,
            "date":         dt.isoformat(),
            "from_address": tx["from"],
            "to_address":   tx["to"],
            "value_token":  int(tx["value"]) / 10**int(tx.get("tokenDecimal", 18)),
            "transaction_hash": tx["hash"],
        })
        new_count += 1

    print(f"→ Fetched blocks {start_block}–{max_block}: "
          f"batch={len(batch)} tx, kept={new_count}\n")

    # If we flagged end-date, batch is empty and we break outer
    if not batch:
        break

    # Otherwise advance to next block window
    start_block = max_block + 1
    time.sleep(0.3)

# ─── SAVE ─────────────────────────────────────────────────────────
df = pd.DataFrame(all_txs)
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)
print(f"✅ Done! Saved {len(df)} transfers to {OUT_CSV}\n")