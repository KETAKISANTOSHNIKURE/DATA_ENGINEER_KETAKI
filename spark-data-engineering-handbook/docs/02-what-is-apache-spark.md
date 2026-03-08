# Chapter 02 – What is Apache Spark

Apache Spark is an **open-source distributed data processing engine** designed for large-scale data processing.

It allows organizations to process **terabytes and petabytes of data across clusters of machines**.

Spark is widely used in:

* Data Engineering
* Machine Learning
* Real-time analytics
* ETL pipelines

Spark was developed at **UC Berkeley AMPLab** and later donated to the Apache Software Foundation.

---

# 1️⃣ Key Characteristics of Spark

Apache Spark provides several powerful features.

| Feature                | Description                                     |
| ---------------------- | ----------------------------------------------- |
| Distributed Processing | Runs computations across multiple machines      |
| In-Memory Computing    | Processes data in memory for faster performance |
| Fault Tolerance        | Recovers lost data using lineage                |
| Multiple APIs          | Supports Python, Scala, Java, SQL               |

---

# 2️⃣ Spark Ecosystem

Spark includes multiple components.

| Component       | Purpose                            |
| --------------- | ---------------------------------- |
| Spark Core      | basic distributed computing engine |
| Spark SQL       | structured data processing         |
| Spark Streaming | real-time data processing          |
| MLlib           | machine learning algorithms        |
| GraphX          | graph analytics                    |

---

# 3️⃣ Why Distributed Systems Need Scaling

Large datasets cannot be processed efficiently on a single machine.

Systems scale in two ways:

### Vertical Scaling

Vertical scaling increases resources of a single machine.

Example:

```
CPU: 4 cores → 32 cores
RAM: 8 GB → 128 GB
```

Limitations:

* expensive hardware
* single machine failure risk
* hardware limits

---

### Horizontal Scaling

Horizontal scaling adds **multiple machines to a cluster**.

Example cluster:

| Node    | CPU      | RAM  |
| ------- | -------- | ---- |
| Worker1 | 16 cores | 64GB |
| Worker2 | 16 cores | 64GB |
| Worker3 | 16 cores | 64GB |

Spark uses **horizontal scaling** to process massive datasets efficiently.

---

# 4️⃣ Spark Execution Example

Suppose we process:

```
1 TB dataset
```

Spark splits the dataset into partitions.

Each executor processes partitions in parallel.

This enables **fast distributed processing**.

---

# 5️⃣ Real Production Example

Large companies process huge datasets using Spark.

Example use cases:

* ETL pipelines
* clickstream analysis
* recommendation systems
* fraud detection

---

# 6️⃣ Interview Questions

### What is Apache Spark?

Apache Spark is a distributed computing framework used for large-scale data processing.

### Why is Spark faster than traditional systems?

Because Spark performs **in-memory computation** and parallel processing across clusters.

---

# Key Takeaway

Apache Spark enables scalable, distributed data processing across clusters using horizontal scaling.

---

➡️ Next: `03-spark-vs-hadoop.md`
