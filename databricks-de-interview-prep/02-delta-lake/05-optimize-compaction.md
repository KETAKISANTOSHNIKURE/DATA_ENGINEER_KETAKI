# OPTIMIZE and Compaction

## ✅ What you need to say in interview

- **OPTIMIZE:** **Compacts small files** into larger ones. Reduces file count, improves read performance.
- **Compaction:** Process of merging small files. OPTIMIZE does this.
- **Why needed:** Append-heavy workloads create many small files; too many files = slow metadata + scan overhead.

## ⚙️ How it actually works

1. OPTIMIZE reads small files in a partition (or whole table).
2. Rewrites them into fewer, larger files (target ~128MB–1GB).
3. Transaction log updated: remove old files, add new.
4. `OPTIMIZE ... ZORDER BY col` does compaction + Z-ORDER.

## ✅ When to use

- After many appends (streaming, incremental loads).
- Before large reads/joins.
- On schedule (daily/weekly) for append-heavy tables.

## ❌ When to NEVER use

- Don't OPTIMIZE too frequently—costly, and new appends create more small files.
- Don't OPTIMIZE without Z-ORDER if you have a common filter/join column—miss optimization.
- Don't OPTIMIZE entire huge table at once if partitioned—use `WHERE` for incremental OPTIMIZE.

## 🚩 Common interview pitfalls

- Saying OPTIMIZE fixes skew (it doesn't—it fixes small files).
- Not knowing OPTIMIZE creates a new version (time travel still works).

## 💻 Working example (SQL + PySpark)

```sql
-- Full table
OPTIMIZE my_table;

-- Partitioned table — incremental
OPTIMIZE my_table WHERE date >= '2024-01-01';

-- With Z-ORDER
OPTIMIZE my_table ZORDER BY (region, date);
```

```python
# PySpark
from delta.tables import DeltaTable
DeltaTable.forPath(spark, "/path").optimize().executeCompaction()
```

## ❔ Actual interview questions + ideal answers

**Q: What does OPTIMIZE do and when do you use it?**

- **Junior:** OPTIMIZE combines small files. Use after lots of appends.
- **Senior:** **OPTIMIZE** compacts small Parquet files into larger ones (~128MB–1GB). It reduces file count, which improves **metadata overhead** and **scan performance**. Use after **append-heavy** workloads (streaming, incremental). For partitioned tables, use **OPTIMIZE ... WHERE partition = value** to optimize incrementally. Run on a schedule (e.g., nightly).

**Q: Why do we get many small files in Delta?**

- **Junior:** Because each write adds new files.
- **Senior:** Delta is **append-only** at the file level. Each **append/merge** adds new files; it doesn't rewrite existing ones. Streaming, small batch writes, and MERGE create many small files. **OPTIMIZE** compacts them. Trade-off: OPTIMIZE is expensive; balance frequency with read performance.

---

## 5-Minute Revision Cheat Sheet

- OPTIMIZE = compact small files.
- Use after appends/streaming.
- Use WHERE for partitioned tables.
- Target ~128MB–1GB per file.
