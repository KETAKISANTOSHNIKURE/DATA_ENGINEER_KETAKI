# Chapter 15 – Spark SQL Engine

Spark SQL enables structured data processing using SQL and DataFrames.

It includes an advanced optimization engine called **Catalyst Optimizer**.

---

# 1️⃣ Query Execution Pipeline

Spark SQL processes queries in stages.

```
SQL Query
   ↓
Logical Plan
   ↓
Optimized Plan
   ↓
Physical Plan
   ↓
Execution
```

---

# 2️⃣ Catalyst Optimizer

Catalyst performs query optimization.

Examples:

* filter pushdown
* column pruning
* constant folding

---

# 3️⃣ Predicate Pushdown

Predicate pushdown pushes filters to the data source.

Example:

```python
df.filter("age > 30")
```

Instead of loading the entire dataset, Spark pushes the filter to the storage layer.

This reduces data scanning.

---

# 4️⃣ Tungsten Engine

Tungsten improves Spark performance using:

* binary memory format
* CPU cache optimization
* code generation

---

# 5️⃣ Interview Questions

### What is Catalyst Optimizer?

Catalyst is Spark's query optimization engine.

### What is predicate pushdown?

It pushes filters to the data source to reduce data scanning.

---

# Key Takeaway

Spark SQL optimizes queries using Catalyst and Tungsten engines to execute large-scale queries efficiently.

---

➡️ Next: `16-driver-memory.md`
