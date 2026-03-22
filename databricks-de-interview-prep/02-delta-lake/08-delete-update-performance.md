# Delete and Update Performance

## ✅ What you need to say in interview

- **Delete/Update:** Delta **rewrites** only the files that contain rows to delete/update. Doesn't rewrite entire table.
- **File-level granularity:** If a file has 1 row to delete, entire file is rewritten (Parquet is immutable).
- **Performance:** Depends on how many files contain target rows. **Partitioning** and **Z-ORDER** help—fewer files to rewrite.
- **Predicate pushdown:** `DELETE WHERE partition = x` only touches files in that partition.

## ⚙️ How it actually works

1. Delta finds files containing matching rows (using stats in log).
2. Reads those files, applies delete/update, writes new files.
3. Log updated: remove old files, add new.
4. Better stats = better pruning = fewer files touched.

## ✅ When to use

- Partition by columns used in DELETE/UPDATE predicates.
- Z-ORDER for non-partition columns in WHERE.
- Use MERGE for bulk upserts instead of row-by-row updates.

## ❌ When to NEVER use

- Don't DELETE/UPDATE without predicate on large tables—rewrites everything.
- Don't forget OPTIMIZE after many deletes—many small files.
- Avoid updating a column that is not in stats—full file scan.

## 🚩 Common interview pitfalls

- Saying Delta updates in place (it rewrites files).
- Not knowing partitioning helps delete/update performance.

## 💻 Working example (SQL + PySpark)

```sql
-- Efficient: partition pruning
DELETE FROM my_table WHERE date = '2024-01-01';

-- Efficient: uses stats
DELETE FROM my_table WHERE id = 123;

-- Expensive: no pruning
DELETE FROM my_table WHERE some_column = 'value';  -- if not partitioned/Z-ordered
```

## ❔ Actual interview questions + ideal answers

**Q: How does Delta perform DELETE and UPDATE?**

- **Junior:** It rewrites the files that contain the rows.
- **Senior:** Delta **does not update in place**. It **rewrites** only the Parquet files that contain matching rows. Uses **stats** in the transaction log for pruning. **Partitioning** and **Z-ORDER** reduce the number of files to rewrite. A file with even one row to delete is fully rewritten (Parquet immutability). Design tables with delete/update patterns in mind.

**Q: How do you make DELETE faster on a large Delta table?**

- **Junior:** Partition and add good WHERE clauses.
- **Senior:** (1) **Partition** by columns in DELETE predicate—partition pruning limits files. (2) **Z-ORDER** by filter columns for better file pruning. (3) **OPTIMIZE** periodically—many small files mean more files to check. (4) Use **MERGE** for bulk operations instead of many single-row deletes.

---

## 5-Minute Revision Cheat Sheet

- Delete/Update = rewrite affected files.
- Partition + Z-ORDER reduce files to rewrite.
- Predicate pushdown via stats.
- One row change = entire file rewrite.
