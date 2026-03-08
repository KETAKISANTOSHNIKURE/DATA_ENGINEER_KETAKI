# Chapter 09 – Spark RDD

RDD stands for **Resilient Distributed Dataset**.

RDD is the **core abstraction in Apache Spark** for distributed data processing.

RDD represents an **immutable distributed collection of objects**.

---

# 1️⃣ Key Properties of RDD

| Property    | Meaning                                |
| ----------- | -------------------------------------- |
| Resilient   | fault tolerant                         |
| Distributed | stored across cluster nodes            |
| Immutable   | cannot be modified                     |
| Lazy        | computed only when action is triggered |

---

# 2️⃣ Creating RDD

Example:

```python
rdd = sc.parallelize([1,2,3,4])
```

Spark distributes data across partitions.

---

# 3️⃣ Transformations

Transformations create new RDDs.

Examples:

```
map
filter
flatMap
```

Example:

```python
rdd.map(lambda x: x*2)
```

---

# 4️⃣ Actions

Actions trigger execution.

Examples:

```
collect
count
first
save
```

---

# 5️⃣ Fault Tolerance

RDDs are fault tolerant.

Spark tracks **lineage information**.

If a partition is lost:

Spark recomputes it using lineage instead of storing multiple copies.

---

# 6️⃣ Accumulators

Accumulators are variables used for **aggregating information across executors**.

Example:

```python
acc = sc.accumulator(0)

rdd.foreach(lambda x: acc.add(x))
```

Accumulators are commonly used for:

* counters
* debugging
* monitoring

---

# 7️⃣ Interview Questions

### What is RDD?

RDD is an immutable distributed dataset used for parallel processing.

### Why are RDDs fault tolerant?

Because Spark tracks lineage information.

---

# Key Takeaway

RDD is the foundational data structure that enables distributed data processing in Spark.

---

➡️ Next: `10-narrow-wide-transformations.md`
