# 04 — Structured Streaming

**Interview weight:** High. Common for real-time pipelines.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Microbatch model | Critical |
| 02 | Checkpointing | Critical |
| 03 | Output modes | Critical |
| 04 | Watermarking, state | Critical |
| 05 | foreachBatch patterns | High |
| 06 | Streaming CDC, upserts | High |

## 5-Minute Revision Cheat Sheet

- **Microbatch:** Process in small batches (triggers); not record-by-record.
- **Checkpoint:** Offset + metadata; enables restart from last position.
- **Output modes:** Append (new rows), Update (upserts), Complete (full aggregate).
- **Watermark:** Drop late events; limits state for aggregations.
- **foreachBatch:** Use batch APIs (e.g., MERGE) in streaming.
- **Streaming CDC:** Auto Loader + MERGE; or CDF.
