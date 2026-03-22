# Output Modes

## ✅ What you need to say in interview

- **Append:** Only **new rows** are written. For aggregations, requires **watermark** (late data dropped).
- **Update:** Only **changed rows** (upserts). Sink must support it (e.g., Delta, some databases). No aggregation.
- **Complete:** **Full result** written each batch. For aggregations; output grows with state.
- **Not all sinks support all modes:** File sink = Append. ForeachBatch = flexible.

## ⚙️ How it actually works

1. Append: each micro-batch outputs new rows; no updates to previous output.
2. Update: only rows that changed (insert/update) are written.
3. Complete: entire result table rewritten each batch.

## ✅ When to use

- **Append:** Insert-only, or aggregation with watermark.
- **Update:** Upserts to Delta, database.
- **Complete:** Small result set, full aggregation (e.g., dashboard).

## ❌ When to NEVER use

- Don't use Complete for large unbounded aggregations—state and output grow.
- Append for aggregation without watermark—Spark doesn't know when "late" rows are done.
- Update with aggregation—not supported.

## 🚩 Common interview pitfalls

- Append + aggregation without watermark = error.
- Confusing Update (changed rows) with Complete (full table).

## 💻 Working example (SQL + PySpark)

```python
# Append (default for many sinks)
df.writeStream.outputMode("append").start()

# Update (Delta, etc.)
df.writeStream.outputMode("update").toTable("my_table")

# Complete (full aggregate)
df.groupBy("key").count().writeStream.outputMode("complete").start()
```

## ❔ Actual interview questions + ideal answers

**Q: When do you use Append vs Update vs Complete?**

- **Junior:** Append for new rows, Update for changes, Complete for full results.
- **Senior:** **Append:** insert-only streams; aggregations with **watermark** (outputs finalized windows). **Update:** upserts (e.g., Delta); only changed rows written; no aggregation. **Complete:** full result each batch—use for **small** aggregations (e.g., counts); state grows. Append + aggregation requires watermark so Spark knows when to emit.

**Q: Why does Append mode require a watermark for aggregations?**

- **Junior:** To handle late data.
- **Senior:** For aggregations, Spark must know when a **window is complete** to output it. Without watermark, it would wait forever (unbounded state). **Watermark** says "rows older than X are late"—Spark can **finalize** and output windows whose max event time is before the watermark. Append then emits only those finalized rows.

---

## 5-Minute Revision Cheat Sheet

- Append: new rows; aggregation needs watermark.
- Update: changed rows; no aggregation.
- Complete: full result; small aggregates only.
