# Worker Node vs Executor vs Core in Spark

## Simple Analogy

```
Cluster Manager = CEO        (decides who does what)
Worker Node     = Building   (physical space/machine)
Executor        = Employee   (does actual work)
Task            = Assignment (one piece of work)
Core            = Hands      (how many tasks at once)
```

---

## Spark Architecture

```
Driver Program (Master)
        ↓
Cluster Manager (YARN / Kubernetes / Standalone)
        ↓
┌──────────────────────────────────────┐
│          Worker Node 1               │
│  ┌────────────┐   ┌────────────┐    │
│  │ Executor 1 │   │ Executor 2 │    │
│  │  Core1→T1  │   │  Core1→T5  │    │
│  │  Core2→T2  │   │  Core2→T6  │    │
│  │  Core3→T3  │   │  Core3→T7  │    │
│  │  Core4→T4  │   │  Core4→T8  │    │
│  └────────────┘   └────────────┘    │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│          Worker Node 2               │
│  ┌────────────┐   ┌────────────┐    │
│  │ Executor 3 │   │ Executor 4 │    │
│  │  Core1→T9  │   │  Core1→T13 │    │
│  │  Core2→T10 │   │  Core2→T14 │    │
│  │  Core3→T11 │   │  Core3→T15 │    │
│  │  Core4→T12 │   │  Core4→T16 │    │
│  └────────────┘   └────────────┘    │
└──────────────────────────────────────┘
```

---

## Key Differences

| | Worker Node | Executor | Core |
|---|---|---|---|
| What it is | Physical/Virtual machine | JVM process on worker | CPU compute unit |
| Nature | Hardware/Infrastructure | Software process | Hardware unit |
| Count | Fixed in cluster | Multiple per worker | Fixed by hardware |
| Does work? | No — hosts executors | Yes — runs tasks | Yes — 1 task at a time |
| Managed by | Cluster Manager | Spark Driver | Hardware |
| Example | EC2 instance | JVM process on EC2 | CPU thread |

---

## What is a Core?

> A core is the fundamental computing unit that can execute ONE task at a time.

```
Physical Core  = Actual hardware on CPU chip
Virtual Core   = Hyper-threaded — 2 virtual per physical

Your Laptop:    8 physical → 16 virtual cores
AWS m5.4xlarge: 8 physical → 16 virtual cores
```

### Core in Spark Context
```
1 Core = 1 Task running at a time

Executor with 4 cores:
├── Core1 → processes Partition 1
├── Core2 → processes Partition 2
├── Core3 → processes Partition 3
└── Core4 → processes Partition 4
= 4 tasks SIMULTANEOUSLY
```

---

## Real Cluster Example

```
Setup:
- 3 Worker Nodes
- Each: 16 CPU cores, 64 GB RAM
- 2 Executors per Worker Node
- Each Executor: 4 cores, 20 GB RAM

Total:
- Worker Nodes  = 3
- Executors     = 3 × 2  = 6
- Total Cores   = 6 × 4  = 24 cores (parallel tasks)
- Total Memory  = 6 × 20 = 120 GB
```

---

## Executor Memory Layout

```
Executor Memory (20GB):
├── Execution Memory (60%) = 12GB
│   └── Shuffles, joins, sorts, aggregations
├── Storage Memory (40%) = 8GB
│   └── Caching DataFrames
└── Reserved Memory = 300MB
    └── Spark internal objects
```

---

## How Tasks and Cores Work Together

```
DataFrame: 100 partitions
Cluster: 6 executors × 4 cores = 24 parallel tasks

Round 1 → processes partitions 1–24
Round 2 → processes partitions 25–48
Round 3 → processes partitions 49–72
Round 4 → processes partitions 73–96
Round 5 → processes partitions 97–100

= ~5 rounds total
```

---

## Configuring Cores in Spark

```python
spark = SparkSession.builder \
    .appName("MyJob") \
    .config("spark.executor.cores", "4")      # Cores per executor
    .config("spark.executor.instances", "6")  # Total executors
    .config("spark.executor.memory", "20g")   # Memory per executor
    .config("spark.driver.cores", "2")        # Driver cores
    .getOrCreate()

# Check total available cores
print(spark.sparkContext.defaultParallelism)
```

---

## Best Practice — Cores Per Executor

```
❌ Too many cores (16 per executor):
   - HDFS limit: 5 concurrent reads per node
   - 16 tasks compete for 5 connections → bottleneck
   - GC pressure increases

❌ Too few cores (1 per executor):
   - Too many tiny executors
   - High overhead
   - No multi-threading benefit

✅ Sweet spot: 4-5 cores per executor
   - Good parallelism
   - Optimal HDFS throughput
   - Less GC pressure
   - Industry standard
```

---

## Optimal Cluster Config Formula

```
Given: 4 Worker Nodes, each 16 cores, 64GB RAM

Step 1 — Cores per Executor
= 4 or 5 (recommended)
→ executor.cores = 4

Step 2 — Executors per Worker
= (16 cores - 1 reserved) / 4 = 3 executors

Step 3 — Total Executors
= 3 × 4 nodes - 1 for driver = 11 executors

Step 4 — Memory per Executor
= (64GB - 4GB overhead) / 3 = 20GB

Final Config:
spark.executor.cores     = 4
spark.executor.instances = 11
spark.executor.memory    = 20g
```

---

## Common Issues

```python
# Issue: Executor Lost
# ERROR: ExecutorLostFailure
# Fix:
spark.conf.set("spark.executor.memory", "16g")  # Increase memory
spark.conf.set("spark.speculation", "true")      # Re-launch slow tasks

# Issue: GC overhead
# Symptom: GC time > 10% in Spark UI
# Fix: Reduce cores or increase memory per executor

# Issue: Too few partitions
# Symptom: Most cores idle
# Fix: Repartition data
df = df.repartition(spark.sparkContext.defaultParallelism * 2)
```

---

## Interview Answer

> "A Worker Node is the physical or virtual machine — the infrastructure. An Executor is
> a JVM process running ON the worker node — the software doing computation. One worker node
> can have multiple executors. A Core is the fundamental unit inside an executor — each core
> runs one task at a time. So if I have 4 cores per executor and 6 executors, I have 24
> tasks running simultaneously. In our project we use 4 cores per executor which is the
> industry sweet spot — beyond 5 cores HDFS throughput becomes a bottleneck."
