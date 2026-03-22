# 03 — Data Engineering Patterns

**Interview weight:** Critical. Shows production experience.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Medallion architecture | Critical |
| 02 | Idempotent pipelines | Critical |
| 03 | Incremental load strategies | Critical |
| 04 | Deduplication patterns | Critical |
| 05 | Late-arriving data | High |
| 06 | Backfill strategy | High |
| 07 | Data quality, quarantine | High |

## 5-Minute Revision Cheat Sheet

- **Medallion:** Bronze (raw) → Silver (cleaned, deduped) → Gold (aggregated, business).
- **Idempotent:** Same input → same output; MERGE, overwrite by partition.
- **Incremental:** Watermark/CDC/timestamp; only new/changed data.
- **Dedup:** Window + MERGE, or `dropDuplicates` with deterministic ordering.
- **Late-arriving:** Watermark + allowed lateness; or reconciliation batch.
- **Backfill:** Re-process by partition; idempotent design.
- **Quarantine:** Bad rows to separate table; alert; fix and reload.
