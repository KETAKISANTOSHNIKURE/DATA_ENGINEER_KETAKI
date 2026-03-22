# Z-ORDER

## ✅ What you need to say in interview

- **Z-ORDER:** **Colocates** data by column(s) using Z-order curve (space-filling curve). Improves **data locality** for filters/joins on those columns.
- **Effect:** Rows with similar values in Z-ordered columns are stored together. **Predicate pushdown** and **file pruning** become more effective.
- **OPTIMIZE ... ZORDER BY (col1, col2):** Does compaction + Z-order. Order of columns matters—first column has highest impact.

## ⚙️ How it actually works

1. Data is sorted by Z-order curve of specified columns.
2. Similar values end up in same or adjacent files.
3. When filtering on Z-ordered column, fewer files need to be read.
4. Combines with OPTIMIZE (compaction + Z-order in one pass).

## ✅ When to use

- Columns used frequently in WHERE or JOIN.
- High-cardinality columns (e.g., id, date) for pruning.
- After identifying hot query patterns.

## ❌ When to NEVER use

- Don't Z-ORDER on low-cardinality columns only—less benefit.
- Don't Z-ORDER too many columns—first 1–2 matter most; more = diminishing returns.
- Don't Z-ORDER instead of partitioning for partition pruning—partitioning is more effective for partition keys.

## 🚩 Common interview pitfalls

- Saying Z-ORDER is the same as partitioning (different: Z-order colocates within files; partitioning separates files).
- Z-ORDERing columns that are rarely filtered.
- Expecting Z-ORDER to fix skew (it doesn't).

## 💻 Working example (SQL + PySpark)

```sql
OPTIMIZE my_table ZORDER BY (date, region);

-- Date first if most queries filter by date
-- Region second if often used with date
```

## ❔ Actual interview questions + ideal answers

**Q: What is Z-ORDER and when do you use it?**

- **Junior:** Z-ORDER sorts data by columns to improve reads. Use on filter columns.
- **Senior:** **Z-ORDER** uses a space-filling curve to **colocate** data by specified columns. Rows with similar values end up in the same files, improving **file pruning** and **predicate pushdown** for filters/joins on those columns. Use on **high-cardinality** columns that appear in WHERE/JOIN. **Order matters**—put the most selective/frequent column first. Combine with OPTIMIZE.

**Q: Z-ORDER vs partitioning—when to use which?**

- **Junior:** Partition for partition keys; Z-ORDER for other filter columns.
- **Senior:** **Partitioning** physically separates data into directories by partition key—best for **partition pruning** (e.g., date). Use when you have a clear partition key and want to skip entire partitions. **Z-ORDER** colocates within files—use for **additional** filter columns or when partitioning would create too many partitions (e.g., high cardinality). Often use **both**: partition by date, Z-ORDER by region/customer_id.

---

## 5-Minute Revision Cheat Sheet

- Z-ORDER = colocate by column(s).
- Improves file pruning for filters.
- Order of columns matters.
- Use with OPTIMIZE; 1–2 columns usually enough.
