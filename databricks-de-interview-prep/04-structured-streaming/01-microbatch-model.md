# Microbatch Model

## ✅ What you need to say in interview

- **Microbatch:** Structured Streaming processes data in **small batches** (micro-batches), not record-by-record. Each trigger interval fetches new data and processes it as a batch.
- **Trigger:** `ProcessingTime` (e.g., every 10 seconds) or `Once` (single batch) or `AvailableNow` (process all available then stop).
- **Continuous processing:** Alternative mode (experimental) for sub-millisecond latency; limited sinks.

## ⚙️ How it actually works

1. Source provides new data (files, Kafka offsets).
2. At trigger, Spark runs a micro-batch: read new data, run query, write to sink.
3. Checkpoint records progress.
4. Repeat on next trigger.

## ✅ When to use

- Near-real-time pipelines (seconds to minutes latency).
- File-based streaming (Auto Loader).
- Kafka/Kinesis ingestion.

## ❌ When to NEVER use

- Don't expect record-by-record latency—it's microbatch.
- Don't use for sub-second SLA without continuous processing (and its limitations).

## 🚩 Common interview pitfalls

- Confusing microbatch with continuous processing.
- Not knowing trigger options (ProcessingTime, Once, AvailableNow).

## 💻 Working example (SQL + PySpark)

```python
df = spark.readStream.format("cloudFiles").load("/landing/")
df.writeStream.trigger(processingTime="10 seconds").start()

# Or: process all available once
df.writeStream.trigger(availableNow=True).start()
```

## ❔ Actual interview questions + ideal answers

**Q: How does Structured Streaming process data?**

- **Junior:** It processes in small batches, like mini Spark jobs.
- **Senior:** **Microbatch model:** at each **trigger** (e.g., every 10 seconds), Spark reads **new data** from the source, runs the streaming query as a **batch job**, and writes to the sink. It's not record-by-record—each micro-batch is a Spark job. **Trigger options:** ProcessingTime (interval), Once (single batch), AvailableNow (all available then stop). Enables reuse of batch APIs and exactly-once semantics with checkpointing.

**Q: What is the difference between ProcessingTime and AvailableNow trigger?**

- **Junior:** ProcessingTime runs repeatedly; AvailableNow runs once.
- **Senior:** **ProcessingTime** runs **periodically** (e.g., every 10 sec)—continuous streaming. **AvailableNow** processes **all data currently available** from the source, then **stops** the stream. Useful for "catch-up" or batch-like streaming (e.g., process today's files then exit).

---

## 5-Minute Revision Cheat Sheet

- Microbatch = small batches per trigger.
- ProcessingTime, Once, AvailableNow.
- Not record-by-record.
