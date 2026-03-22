# Watermarking and State

## ✅ What you need to say in interview

- **Watermark:** Threshold for **late data**. Events with `event_time < max_event_time - watermark` are **dropped** (or not processed for aggregation). **Limits state**—old state can be purged.
- **State:** For aggregations and joins, Spark holds **intermediate state** (e.g., partial aggregates). Watermark allows **state cleanup** to avoid unbounded growth.
- **State store:** Backed by HDFS/cloud; checkpoint includes state.

## ⚙️ How it actually works

1. Watermark = max(event_time) - threshold.
2. For aggregation: windows with max event time < watermark are finalized and emitted; state for those windows is dropped.
3. For stream-stream join: rows from one side are joined with the other; state purged by watermark.

## ✅ When to use

- Aggregations in Append mode.
- Stream-stream joins.
- Any query needing bounded state.

## ❌ When to NEVER use

- Don't set watermark = 0 if you expect late data—drops everything.
- Don't set very large watermark without considering state size (until cleanup).
- Watermark doesn't help with Update or Complete mode aggregation (different semantics).

## 🚩 Common interview pitfalls

- Watermark is per-query, not global.
- Late data is dropped—no "allowed lateness" update in standard Append.
- State = memory/disk; skew can cause one partition to hold more state.

## 💻 Working example (SQL + PySpark)

```python
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes"), "key") \
  .count() \
  .writeStream.outputMode("append").start()
```

## ❔ Actual interview questions + ideal answers

**Q: What is the purpose of watermark in Structured Streaming?**

- **Junior:** To drop late events and limit state.
- **Senior:** **Watermark** defines how late data can be—`event_time < max - watermark` is considered too late. It (1) **limits state**—Spark can purge state for finalized windows, avoiding OOM; (2) **enables Append output** for aggregations—Spark knows when to emit finalized results. Trade-off: larger watermark = more late data accepted but more state; smaller = less state but more late data dropped.

**Q: What happens to state when the stream stops?**

- **Junior:** It's in the checkpoint.
- **Senior:** **State** is stored in the **checkpoint** (and state store). When the stream **stops gracefully**, state is persisted. On **restart**, state is restored from checkpoint. If the stream **fails**, the last committed checkpoint has the state—restart resumes from there. State is **partitioned** by key; skew in keys can cause one task to hold disproportionate state.

---

## 5-Minute Revision Cheat Sheet

- Watermark = "too late" threshold.
- Limits state; enables Append for aggregations.
- State in checkpoint.
- Trade-off: late data vs state size.
