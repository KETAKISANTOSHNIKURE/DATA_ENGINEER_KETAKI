# Small Files Problem

## ✅ What you need to say in interview

- **Problem:** Many small files (KB–MB) cause **metadata overhead**, slow **listing**, and poor **scan performance**.
- **Causes:** Streaming, small batch appends, many partitions with little data.
- **Solutions:** (1) **OPTIMIZE** (Delta)—compact. (2) **coalesce** before write. (3) **delta.autoOptimize.optimizeWrite**—coalesce on write. (4) **delta.autoOptimize.autoCompact**—OPTIMIZE after writes.

## ⚙️ How it actually works

- Each file has metadata; many files = many metadata ops.
- Listing 10K files is slow; reading 10K small files is inefficient (overhead per file).
- OPTIMIZE/coalesce merges small files into larger ones.

## ✅ When to use

- After streaming or append-heavy workloads.
- Before large reads.
- Enable autoOptimize for append-heavy tables.

## ❌ When to NEVER use

- Don't coalesce to 1 for large datasets—single bottleneck.
- Don't OPTIMIZE too frequently—expensive.
- Avoid creating small files in the first place (optimize write).

## 🚩 Common interview pitfalls

- Saying "small files are fine" for Delta—they hurt performance.
- Not knowing autoOptimize options.
- Coalesce vs repartition for reducing files (coalesce = no shuffle).

## 💻 Working example (SQL + PySpark)

```python
# Before write
df.coalesce(10).write.format("delta").save("/path/")

# After the fact
spark.sql("OPTIMIZE my_table")

# Table property
spark.sql("ALTER TABLE my_table SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true')")
```

## ❔ Actual interview questions + ideal answers

**Q: How do you solve the small files problem in Delta?**

- **Junior:** Run OPTIMIZE; use coalesce before write.
- **Senior:** (1) **OPTIMIZE** compacts existing small files. (2) **coalesce** before write to limit output files. (3) **delta.autoOptimize.optimizeWrite** coalesces during write. (4) **delta.autoOptimize.autoCompact** runs OPTIMIZE after writes. For streaming, enable optimizeWrite. For batch, coalesce or OPTIMIZE on schedule. Target ~128MB per file.

**Q: Why are small files a problem?**

- **Junior:** They slow down reads and listing.
- **Senior:** **Metadata overhead**—each file has object store metadata; listing 100K files is slow. **Scan inefficiency**—opening many files adds per-file overhead; fewer larger files = fewer opens. **Partition pruning** less effective—many tiny files per partition. **Driver** can be stressed listing for planning.

---

## 5-Minute Revision Cheat Sheet

- Many small files = metadata + scan overhead.
- OPTIMIZE, coalesce, autoOptimize.
- Target ~128MB per file.
- optimizeWrite for append-heavy.
