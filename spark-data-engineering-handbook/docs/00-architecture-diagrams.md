# Architecture Diagrams for Spark & Data Engineering

This section contains key diagrams used throughout the Spark Engineering Handbook.

These diagrams visualize how distributed data systems work in production.

---

## 1️⃣ Spark Cluster Architecture

This diagram shows how Spark applications run on a distributed cluster.

```mermaid
flowchart TD

Driver[Driver Program]

ClusterManager[Cluster Manager]

Worker1[Worker Node 1]
Worker2[Worker Node 2]
Worker3[Worker Node 3]

Executor1[Executor]
Executor2[Executor]
Executor3[Executor]

Driver --> ClusterManager

ClusterManager --> Worker1
ClusterManager --> Worker2
ClusterManager --> Worker3

Worker1 --> Executor1
Worker2 --> Executor2
Worker3 --> Executor3
```

**Explanation:**

- Driver controls the application
- Cluster manager allocates resources
- Worker nodes run executors
- Executors process tasks

---

## 2️⃣ Spark DAG Execution Flow

Spark converts transformations into a Directed Acyclic Graph (DAG) before execution.

```mermaid
flowchart LR

ReadData[Read Data]
Filter[Filter Records]
Map[Map Transformation]
GroupBy[Group By]
Aggregation[Aggregation]
Output[Write Result]

ReadData --> Filter
Filter --> Map
Map --> GroupBy
GroupBy --> Aggregation
Aggregation --> Output
```

**Key idea:** Spark builds the DAG first and executes it only when an action occurs.

---

## 3️⃣ Spark Job → Stage → Task Execution

Spark jobs are broken down into stages and tasks.

```mermaid
flowchart TD

Application[Application]
Job[Job]
Stage1[Stage 1]
Stage2[Stage 2]
Task1[Task 1]
Task2[Task 2]
Task3[Task 3]
Task4[Task 4]

Application --> Job
Job --> Stage1
Job --> Stage2
Stage1 --> Task1
Stage1 --> Task2
Stage2 --> Task3
Stage2 --> Task4
```

**Definitions:**

| Level | Description |
|-------|-------------|
| Application | entire Spark program |
| Job | triggered by an action |
| Stage | separated by shuffle |
| Task | smallest execution unit |

---

## 4️⃣ Spark Memory Architecture

Spark uses a Unified Memory Model.

```mermaid
flowchart TD

ExecutorMemory[Executor Memory]
UnifiedMemory[Unified Memory]
ExecutionMemory[Execution Memory]
StorageMemory[Storage Memory]

ExecutorMemory --> UnifiedMemory
UnifiedMemory --> ExecutionMemory
UnifiedMemory --> StorageMemory
```

- **Execution memory** used for: joins, aggregations, shuffle buffers
- **Storage memory** used for: caching, persisted datasets

---

## 5️⃣ Modern Data Engineering Pipeline

Typical data engineering architecture used by modern companies.

```mermaid
flowchart LR

Apps[Applications]
Kafka[Kafka Streaming]
Spark[Apache Spark]
DataLake[Data Lake]
Warehouse[Data Warehouse]
BI[BI Dashboards]

Apps --> Kafka
Kafka --> Spark
Spark --> DataLake
DataLake --> Warehouse
Warehouse --> BI
```

**Pipeline stages:** Applications → Kafka → Spark Processing → Data Lake → Data Warehouse → BI Dashboards

---

## 6️⃣ Streaming Data Pipeline

Real-time data pipelines process events continuously.

```mermaid
flowchart TD

EventSource[Event Source]
KafkaTopic[Kafka Topic]
SparkStreaming[Spark Streaming]
DataLake[Data Lake]
Analytics[Analytics]

EventSource --> KafkaTopic
KafkaTopic --> SparkStreaming
SparkStreaming --> DataLake
DataLake --> Analytics
```

**Example use cases:** fraud detection, real-time dashboards, clickstream analysis

---

## 7️⃣ Spark Query Optimization Pipeline

Spark SQL queries pass through multiple optimization stages.

```mermaid
flowchart TD

UserQuery[User Query]
LogicalPlan[Logical Plan]
CatalystOptimizer[Catalyst Optimizer]
PhysicalPlan[Physical Plan]
TungstenEngine[Tungsten Engine]
Execution[Execution]

UserQuery --> LogicalPlan
LogicalPlan --> CatalystOptimizer
CatalystOptimizer --> PhysicalPlan
PhysicalPlan --> TungstenEngine
TungstenEngine --> Execution
```

**Stages explained:**

| Stage | Purpose |
|-------|---------|
| Logical Plan | describes transformations |
| Catalyst Optimizer | optimizes query |
| Physical Plan | defines execution strategy |
| Execution | runs tasks on executors |

---

## Key Takeaway

These diagrams represent the core architecture behind Spark and modern data engineering systems.

Understanding them helps engineers:

- Design scalable pipelines
- Debug performance issues
- Optimize distributed processing
- Build production-grade data platforms
