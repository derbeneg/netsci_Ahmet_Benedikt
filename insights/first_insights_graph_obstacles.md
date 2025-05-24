# Small Report on First Graph Obstacles

When we first built the unweighted graph by aggregating edges (one edge per unique `(from, to)`), we discovered:

## Collapsed structure

* All 88,821 unique address pairs collapsed into exactly 88,821 edges → every node became its own connected component.
  **Implication:** No meaningful connectivity, no clustering, no GCC.

## Deduplication hides activity

* High-volume senders/receivers looked like they only ever transacted once.
  **Implication:** Degree and centrality measures were trivial (all degrees = 1), breaking our core analyses.

## Self-loops distort counts

* We hadn’t removed transactions where `from_address == to_address`.
  **Implication:** Inflated self-degrees, further skewing any connectivity.

---

## How the new script handles this

1. **Keeps every transfer individually** (no dedup), so degree = true tx count
2. **Removes self-transfers** to clean up noise
3. **Optionally filters out low-activity addresses** (e.g. `min_degree=5`) to focus on a real giant component
4. **Drops unused cols** to slim memory and speed up downstream code

---

## Next steps

1. Load the cleaned DataFrame
2. Build two graphs:

   * **Unweighted:** one edge per transfer row
   * **Weighted:** aggregate `value_token` per pair
3. Re-compute and inspect basic stats (density, components) to confirm we now have a Giant Weakly Connected Component
4. Move on to plotting degree distributions and deeper centrality/clustering analyses.
