# Spark Master Architecture

This diagram shows the **complete flow of Apache Spark execution**, connecting:

* Spark Architecture
* DAG Execution
* Job → Stage → Task hierarchy
* Memory management
* Query optimization
* Cluster execution

It summarizes the entire Spark system.

---

# 1️⃣ Spark Master Architecture Overview

```mermaid
flowchart TD

UserApplication[User Application]

SparkSession[SparkSession]

Driver[Driver Program]

DAGScheduler[DAG Scheduler]

TaskScheduler[Task Scheduler]

ClusterManager[Cluster Manager]

WorkerNodes[Worker Nodes]

Executors[Executors]

Tasks[Tasks]

UserApplication --> SparkSession

SparkSession --> Driver

Driver --> DAGScheduler

DAGScheduler --> TaskScheduler

TaskScheduler --> ClusterManager

ClusterManager --> WorkerNodes

WorkerNodes --> Executors

Executors --> Tasks
```

---

# 2️⃣ Execution Flow Explained

Spark execution follows a structured pipeline.

```text
User Application
      ↓
SparkSession
      ↓
Driver Program
      ↓
DAG Creation
      ↓
Job → Stage → Task
      ↓
Cluster Manager
      ↓
Executors
      ↓
Task Execution
```

---

# 3️⃣ Data Processing Pipeline

```mermaid
flowchart LR

DataSource

Transformations

DAG

Stages

Tasks

Results

DataSource --> Transformations
Transformations --> DAG
DAG --> Stages
Stages --> Tasks
Tasks --> Results
```

---

# 4️⃣ Spark Memory Architecture

```mermaid
flowchart TD

ExecutorMemory

UnifiedMemory

ExecutionMemory
StorageMemory

ExecutorMemory --> UnifiedMemory

UnifiedMemory --> ExecutionMemory
UnifiedMemory --> StorageMemory
```

Execution memory handles:

* joins
* aggregations
* shuffle operations

Storage memory handles:

* cached datasets
* persisted RDDs

---

# 5️⃣ Query Optimization Pipeline

```mermaid
flowchart TD

SQLQuery

LogicalPlan

CatalystOptimizer

PhysicalPlan

TungstenEngine

Execution

SQLQuery --> LogicalPlan
LogicalPlan --> CatalystOptimizer
CatalystOptimizer --> PhysicalPlan
PhysicalPlan --> TungstenEngine
TungstenEngine --> Execution
```

Spark SQL optimizes queries before execution.

---

# 6️⃣ Join Execution Strategies

Spark supports multiple join strategies.

```mermaid
flowchart LR

JoinOperation

ShuffleJoin
BroadcastJoin

JoinOperation --> ShuffleJoin
JoinOperation --> BroadcastJoin
```

Broadcast join is used when one dataset is small.

---

# 7️⃣ Performance Optimization Layer

Spark uses multiple optimizations:

```text
Dynamic Partition Pruning
Adaptive Query Execution
Broadcast Joins
Caching
Partitioning
Salting
```

These optimizations improve large-scale data processing performance.

---

# 8️⃣ Spark Execution Hierarchy

```mermaid
flowchart TD

Application

Job

Stage

Task

Application --> Job
Job --> Stage
Stage --> Task
```

Each task processes a partition.

---

# 9️⃣ Cluster Execution Model

Spark runs on clusters managed by:

* Hadoop YARN
* Kubernetes
* Spark Standalone

Cluster manager allocates resources to executors.

---

# 🔟 Complete Spark Stack

Spark consists of multiple layers:

| Layer              | Components            |
| ------------------ | --------------------- |
| Application Layer  | SparkSession, APIs    |
| Execution Layer    | Driver, DAG Scheduler |
| Resource Layer     | Cluster Manager       |
| Compute Layer      | Executors             |
| Optimization Layer | Catalyst, AQE         |
| Memory Layer       | Unified Memory        |

---

# Key Takeaway

Apache Spark processes large-scale data using:

```text
Distributed architecture
Parallel task execution
Advanced query optimization
Dynamic memory management
```

Understanding this architecture allows engineers to **debug performance issues, optimize pipelines, and design scalable data systems**.

---

➡️ Next: `01-introduction.md`
