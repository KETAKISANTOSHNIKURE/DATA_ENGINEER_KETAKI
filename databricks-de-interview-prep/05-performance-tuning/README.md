# 05 — Performance Tuning

**Interview weight:** High. Shows hands-on experience.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Shuffle reduction | Critical |
| 02 | Partition sizing | Critical |
| 03 | Small files problem | Critical |
| 04 | Data skew handling | Critical |
| 05 | Partitioning strategy | High |
| 06 | Photon runtime | High |

## 5-Minute Revision Cheat Sheet

- **Shuffle:** Minimize; broadcast small tables; repartition by join key.
- **Partition size:** ~128–200MB; total_size / 128MB ≈ partitions.
- **Small files:** OPTIMIZE, coalesce before write, autoOptimize.
- **Skew:** Salting, AQE skew join, split skewed keys.
- **Partitioning:** By filter/join column; avoid over-partitioning.
- **Photon:** Databricks-native engine; SQL/DataFrame; enable on cluster.
