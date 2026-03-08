# Chapter 07 – Lazy Evaluation and Actions

One of the most important concepts in Apache Spark is **Lazy Evaluation**.

Spark does **not execute operations immediately**.

Instead, it builds a **logical execution plan (DAG)** and runs it only when an **action** is called.

---

# 1️⃣ What is Lazy Evaluation?

Lazy evaluation means:

Spark **delays execution of transformations until an action is triggered**.

Example:

```python id="a1x7m9"
df = spark.read.csv("sales.csv")

filtered = df.filter("amount > 100")

grouped = filtered.groupBy("city").count()
```

At this point:

❌ Spark has **not executed anything yet**.

Spark is only **building the DAG**.

---

# 2️⃣ When Does Spark Execute?

Execution happens when an **action** is called.

Example:

```python id="p9h2sq"
grouped.sho
```
