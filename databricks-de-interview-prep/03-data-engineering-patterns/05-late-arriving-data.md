# Late-Arriving Data

## ✅ What you need to say in interview

- **Late-arriving:** Data that arrives **after** the window/run that should have processed it.
- **Streaming:** Use **watermark** + **allowedLateness** (in some APIs) to hold state for late events.
- **Batch:** Use **overlap window** (re-process last N hours) or **reconciliation job**.
- **Trade-off:** Latency vs completeness. Strict watermark = drop late; large watermark = more state.

## ⚙️ How it actually works

1. Watermark: events with timestamp < (max_seen - watermark) are considered "too late" and dropped (or in allowedLateness, still processed with delayed output).
2. Overlap: each batch re-processes `[last_run - overlap, now]`; idempotent write.
3. Reconciliation: periodic full or incremental backfill to catch stragglers.

## ✅ When to use

- Event streams (events can arrive out of order).
- Batch pipelines with delayed source commits.
- When completeness matters more than latency.

## ❌ When to NEVER use

- Don't set watermark = 0 if you expect late data—drops everything.
- Don't set watermark very large without considering state size (Spark streaming).
- Avoid ignoring late data in financial/audit use cases without a reconciliation path.

## 🚩 Common interview pitfalls

- Confusing watermark with retention (watermark = "too late" threshold).
- Not having a reconciliation strategy when late data is critical.
- Watermark in append mode: late data is dropped; no "update" of past windows.

## 💻 Working example (SQL + PySpark)

```python
# Structured Streaming: watermark + allowedLateness concept
df.withWatermark("event_time", "10 minutes")
  .groupBy(window("event_time", "5 minutes"), "key")
  .count()
# Events 10+ min late are dropped (in append mode)
```

```sql
-- Batch overlap: re-process last 2 days
INSERT OVERWRITE silver PARTITION (date)
SELECT ... FROM bronze
WHERE date >= current_date() - 2;
-- Idempotent if overwrite by partition
```

## ❔ Actual interview questions + ideal answers

**Q: How do you handle late-arriving data in streaming?**

- **Junior:** Use a watermark. Late data might be dropped.
- **Senior:** **Watermark** tells Spark how late we'll accept data—e.g., 10 minutes. Events older than `max_event_time - watermark` are dropped (in append mode). **allowedLateness** (where supported) lets late data update previous windows but adds state. Trade-off: larger watermark = more state, longer wait. For critical completeness, add a **reconciliation batch** job that processes late arrivals into a separate table or backfills.

**Q: How do you handle late data in batch incremental loads?**

- **Junior:** Re-process last few days.
- **Senior:** **Overlap window:** each run re-processes `[last_run - N days, now]` so late rows are picked up. Requires **idempotent writes** (partition overwrite or MERGE). **Reconciliation job:** periodic (e.g., weekly) job that checks for late-arriving keys and merges them. Choice depends on how late data arrives and SLA.

---

## 5-Minute Revision Cheat Sheet

- Watermark = "too late" threshold in streaming.
- Overlap window in batch.
- Reconciliation for critical late data.
- Trade-off: latency vs completeness.
