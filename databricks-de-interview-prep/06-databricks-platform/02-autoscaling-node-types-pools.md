# Autoscaling, Node Types, Pools

## ✅ What you need to say in interview

- **Autoscaling:** Cluster scales between **min** and **max** workers based on **load** (pending tasks). Reduces cost when idle.
- **Node types:** **Driver** and **worker** can differ. **Standard** (D-series) for general; **memory-optimized** (E-series) for large data; **compute-optimized** for CPU-heavy. **Photon** workers for Photon acceleration.
- **Pools (Cluster pools):** **Pre-provisioned** idle nodes. Jobs/clusters **attach** to pool for **faster startup** (no cold start). Good for frequent short jobs.

## ⚙️ How it actually works

1. Autoscaling: Spark requests workers; Databricks adds/removes based on backlog.
2. Node types: choose for workload (memory, CPU, disk).
3. Pools: maintain a set of idle nodes; new cluster uses them instead of provisioning new VMs.

## ✅ When to use

- **Autoscaling:** Variable workloads; avoid over-provisioning.
- **Memory-optimized:** Large shuffles, OOM issues.
- **Pools:** Many short jobs; reduce startup time.

## ❌ When to NEVER use

- Don't set max workers too low for spikey workloads.
- Don't use compute-optimized for memory-bound jobs.
- Pools have cost for idle nodes—use when startup time matters.

## 🚩 Common interview pitfalls

- Not knowing pools reduce startup time.
- Confusing driver and worker node types.
- Autoscaling doesn't scale to zero (min workers).

## 💻 Working example (SQL + PySpark)

```python
# Cluster config (UI or API)
# Autoscaling: min_workers=2, max_workers=8
# Node: workers = standard_DS4_v2 or memory_optimized
# Pool: specify pool_id in cluster config
```

## ❔ Actual interview questions + ideal answers

**Q: What is cluster autoscaling?**

- **Junior:** The cluster adds or removes workers based on load.
- **Senior:** **Autoscaling** scales workers between **min** and **max** based on **pending Spark tasks**. When the scheduler has a backlog, it adds workers; when idle, it removes them. Reduces cost for variable workloads. Configure min/max. **Note:** scales down, not to zero—min workers always run.

**Q: What are cluster pools and when do you use them?**

- **Junior:** Pools pre-provision nodes for faster startup.
- **Senior:** **Cluster pools** maintain a set of **idle nodes**. When a cluster starts, it **attaches** to the pool instead of provisioning new VMs—**faster startup** (seconds vs minutes). Use for **frequent short jobs** where cold start is a significant fraction of run time. Trade-off: pool nodes incur cost while idle; size appropriately.

---

## 5-Minute Revision Cheat Sheet

- Autoscaling: min–max workers by load.
- Node types: standard, memory-opt, compute-opt, Photon.
- Pools: pre-provision; fast startup.
- Pools for frequent short jobs.
