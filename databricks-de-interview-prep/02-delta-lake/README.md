# 02 — Delta Lake

**Interview weight:** Critical. Delta is core to Databricks.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Transaction log, ACID | Critical |
| 02 | Schema enforcement, evolution | Critical |
| 03 | Time travel, RESTORE | Critical |
| 04 | MERGE INTO, upserts, CDC | Critical |
| 05 | OPTIMIZE, compaction | Critical |
| 06 | Z-ORDER | High |
| 07 | VACUUM, retention | High |
| 08 | Delete/Update performance | High |
| 09 | Delta table properties | Medium |

## 5-Minute Revision Cheat Sheet

- **Transaction log:** JSON in `_delta_log/`; ACID via optimistic concurrency.
- **Schema enforcement:** Reject writes that don't match. **Evolution:** `mergeSchema` or `overwriteSchema`.
- **Time travel:** `VERSION AS OF n` or `TIMESTAMP AS OF 'ts'`. **RESTORE** to rollback.
- **MERGE:** Upsert by key; `whenMatched`, `whenNotMatched`.
- **OPTIMIZE:** Compacts small files. **Z-ORDER:** Colocate data by column(s).
- **VACUUM:** Remove files not in retention (default 7 days). **Retention:** `delta.deletedFileRetentionDuration`.
