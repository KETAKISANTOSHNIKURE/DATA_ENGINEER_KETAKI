# Partitioning Strategy

## ✅ What you need to say in interview

- **Partitioning:** Organize data by column values. Enables **partition pruning**—skip irrelevant partitions.
- **Choose key:** Column used in **WHERE** or **JOIN**. Often **date** for time-series.
- **Avoid:** (1) **Over-partitioning**—too many partitions (e.g., by high-cardinality id). (2) **Under-partitioning**—few huge partitions. (3) **Wrong key**—partition by column rarely filtered.
- **Delta:** Partition + **Z-ORDER** for additional columns.

## ⚙️ How it actually works

- Partition = directory structure (e.g., `date=2024-01-01/`).
- Query with `WHERE date = '2024-01-01'` skips other partitions.
- Spark uses partition stats for pruning.
- Too many partitions: small files, metadata overhead.

## ✅ When to use

- Time-series: partition by date.
- Dimension tables: rarely need partitioning (small).
- Fact tables: partition by commonly filtered column (date, region).

## ❌ When to NEVER use

- Don't partition by high-cardinality key (e.g., user_id)—thousands of partitions.
- Don't partition by column never used in filters.
- Don't partition if table is small—overhead not worth it.

## 🚩 Common interview pitfalls

- Partitioning by GUID or unique id—massive partitions.
- Not considering partition count (rule of thumb: <10K partitions for Delta).
- Ignoring Z-ORDER as complement to partitioning.

## 💻 Working example (SQL + PySpark)

```python
df.write.format("delta").partitionBy("date").save("/path/")

# Read with pruning
spark.read.format("delta").load("/path/").filter("date = '2024-01-01'")
```

```sql
CREATE TABLE fact (id INT, date DATE, amount DOUBLE)
USING DELTA PARTITIONED BY (date);
```

## ❔ Actual interview questions + ideal answers

**Q: How do you choose a partitioning strategy?**

- **Junior:** Partition by date or commonly filtered column.
- **Senior:** Choose a column used in **WHERE** or **JOIN**—enables **partition pruning**. For time-series: **date** (daily or monthly). Avoid **high cardinality** (e.g., user_id)—too many partitions. **Cardinality** should be modest (e.g., 100s–1000s of partition values). Complement with **Z-ORDER** for additional filter columns. Rule: partitions should be roughly equal size; avoid skew.

**Q: Partitioning vs Z-ORDER—when to use which?**

- **Junior:** Partition for main filter; Z-ORDER for others.
- **Senior:** **Partitioning** physically separates data into directories—best for **partition pruning** (skip entire partitions). Use for **low–medium cardinality** (date, region). **Z-ORDER** colocates within files—use for **additional** filter columns or when partitioning would create too many partitions. Often **both**: partition by date, Z-ORDER by customer_id or region.

---

## 5-Minute Revision Cheat Sheet

- Partition by filter/join column.
- Date for time-series.
- Avoid high-cardinality.
- Partition + Z-ORDER together.
