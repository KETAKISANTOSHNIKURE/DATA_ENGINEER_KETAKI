# SQL Interview Preparation

> Focus: **What to write + What interviewer traps you on**

---

## PART 1: Table Creation & Duplicate Handling

---

## 1️⃣ Create Table Structure Only (No Data)

```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table
WHERE 1 = 0;
```

**Why**

* Copies schema only
* No data copied

**Traps**

* Constraints (PK, FK, Index) ❌ NOT copied
* `WHERE 1=0` is mandatory

---

## 2️⃣ Create Table With Data

```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table;
```

**With condition**

```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table
WHERE status = 'ACTIVE';
```

**Traps**

* Indexes / constraints ❌ not copied
* Existing table → use `INSERT INTO ... SELECT`

---

## 3️⃣ Find Duplicate Records

```sql
SELECT emp_id, COUNT(*)
FROM employee
GROUP BY emp_id
HAVING COUNT(*) > 1;
```

**Why**

* `HAVING` filters aggregated data

**Trap**

* `WHERE COUNT(*) > 1` ❌ wrong

---

## 4️⃣ Find Duplicate Count

```sql
SELECT emp_id, COUNT(*) AS duplicate_count
FROM employee
GROUP BY emp_id
HAVING COUNT(*) > 1;
```

---

## 5️⃣ Delete Duplicates (Keep One)

```sql
DELETE FROM employee
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY id) rn
        FROM employee
    )
    WHERE rn > 1
);
```

**Why**

* Keeps lowest `id`
* Deterministic delete

**Traps**

* Window functions need subquery
* Use `ROW_NUMBER` (not `DENSE_RANK`) for deletion

---

## PART 2: Salary & Window Functions

---

## 6️⃣ 2nd Highest Salary

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) r
    FROM employee
)
WHERE r = 2;
```

**Why**

* Handles duplicate salaries

**Trap**

* `ROW_NUMBER` ❌ when duplicates exist

---

## 7️⃣ 3rd Highest Salary

```sql
WHERE r = 3;
```

(Same logic as above)

---

## 8️⃣ 2nd Highest Salary per Department

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) r
    FROM employee
)
WHERE r = 2;
```

**Trap**

* Forgetting `PARTITION BY` ❌

---

## 9️⃣ Bottom 2 Salaries

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY salary ASC) rn
    FROM employee
)
WHERE rn <= 2;
```

---

## 🔟 Top 2 Salaries

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY salary DESC) rn
    FROM employee
)
WHERE rn <= 2;
```

**Trap**

* Without `ORDER BY` → non-deterministic

---

## 1️⃣1️⃣ ROW_NUMBER vs RANK vs DENSE_RANK

| Function   | Handles Duplicates | Gaps |
| ---------- | ------------------ | ---- |
| ROW_NUMBER | ❌                  | ❌    |
| RANK       | ✅                  | ✅    |
| DENSE_RANK | ✅                  | ❌    |

**Use**

* Delete duplicates → `ROW_NUMBER`
* Salary ranking → `DENSE_RANK`

---

## PART 3: Oracle Date & NULL Handling

---

## 1️⃣2️⃣ Last N Days (Oracle)

```sql
WHERE hire_date >= SYSDATE - N;
```

---

## 1️⃣3️⃣ Last N Months (Oracle)

```sql
WHERE hire_date >= ADD_MONTHS(SYSDATE, -N);
```

---

## 1️⃣4️⃣ Last N Years (Oracle)

```sql
WHERE hire_date >= ADD_MONTHS(SYSDATE, -12*N);
```

**Trap**

* `EXTRACT(YEAR FROM date)` ❌
* `SYSDATE - 365*N` ❌

---

## 1️⃣5️⃣ NULL Handling (Name Logic)

```sql
SELECT COALESCE(fname, lname, 'UNKNOWN') AS name, salary
FROM employee;
```

**Why**

* First non-NULL value
* Portable SQL

---

## PART 4: JOIN COUNT TRAPS (VERY IMPORTANT)

---

### Rule (MEMORIZE)

> **Join rows = matching rows × matching rows**

---

### CASE 1: Duplicates

T1: 6 rows of `10`
T2: 3 rows of `10`

👉 Result = `6 × 3 = 18`

| Join  | Rows |
| ----- | ---- |
| INNER | 18   |
| LEFT  | 18   |
| RIGHT | 18   |
| FULL  | 18   |

---

### CASE 2: NULLs

* NULL never matches NULL

| Join  | Rows |
| ----- | ---- |
| INNER | 8    |
| LEFT  | 10   |
| RIGHT | 9    |
| FULL  | 11   |

---

### CASE 3: Different Values

| Join  | Rows |
| ----- | ---- |
| INNER | 9    |
| LEFT  | 10   |
| RIGHT | 9    |
| FULL  | 10   |

---

## FINAL INTERVIEW RULES (1-Minute Revision)

* `WHERE` → rows
* `HAVING` → groups
* `DENSE_RANK` → salary
* `ROW_NUMBER` → delete duplicates
* `ADD_MONTHS` → months/years
* `SYSDATE - N` → days
* NULL ≠ NULL
* JOIN = multiplication, not addition

---

## ✅ How to use this file

* **Daily**: skim headings
* **Before interview**: read only code blocks + rules
* **During interview**: explain WHY, not syntax

---
Perfect request 👍
You’re thinking like someone who actually wants to **revise fast and not panic**.
Below is an **UPDATED + CLEAN SQL.md** where I’ve **added**:

* ✅ **Partitioning vs Bucketing**
* ✅ **LEAD / LAG**
* ✅ **SQL Query Optimization (practical, interview-safe)**

I’ve **kept the same style** as your cleaned file:

* Short
* Bullet-heavy
* Zero fluff
* Easy to skim before interview

👉 You can **append this directly** to the **end of your current SQL.md**.

---

# ➕ ADD THIS TO YOUR `SQL.md`

---

## PART 5: Partitioning vs Bucketing (Big Data / Hive / Spark)

---

## 1️⃣ Partitioning

**What**

* Splits table into **separate directories**
* Based on column value

**Example**

```sql
PARTITIONED BY (country)
```

**Why**

* Reduces data scan
* Used with WHERE clause

**Good For**

* Low-cardinality columns (country, date)

**Trap**

* ❌ Partitioning on high-cardinality columns (id, timestamp)
* Too many small files = bad performance

---

## 2️⃣ Bucketing

**What**

* Splits data into **fixed number of files**
* Uses hash function

**Example**

```sql
CLUSTERED BY (id) INTO 4 BUCKETS;
```

**Why**

* Improves JOIN & GROUP BY
* Reduces shuffle in Spark

**Trap**

* Bucketing does NOT reduce data scan
* Must enable bucketing (Hive)

---

## 3️⃣ Partitioning vs Bucketing (Difference)

| Feature    | Partitioning    | Bucketing         |
| ---------- | --------------- | ----------------- |
| Storage    | Directories     | Files             |
| Based on   | Column value    | Hash              |
| Number     | Dynamic         | Fixed             |
| Used for   | WHERE filtering | JOIN optimization |
| Skips data | ✅ Yes           | ❌ No              |

**Interview Line**

> “Partitioning filters data, bucketing optimizes processing.”

---

## PART 6: LEAD() & LAG() (Window Functions)

---

## 4️⃣ LAG()

**What**

* Access previous row value

**Example**

```sql
SELECT emp_id,
       salary,
       LAG(salary) OVER (ORDER BY emp_id) AS prev_salary
FROM employee;
```

**Use Case**

* Salary comparison
* Trend analysis

---

## 5️⃣ LEAD()

**What**

* Access next row value

```sql
SELECT emp_id,
       salary,
       LEAD(salary) OVER (ORDER BY emp_id) AS next_salary
FROM employee;
```

---

## 6️⃣ LEAD / LAG with Default Value

```sql
LAG(salary, 1, 0) OVER (ORDER BY emp_id)
```

**Trap**

* Without ORDER BY → meaningless result

---

## LEAD vs LAG Summary

| Function | Looks        |
| -------- | ------------ |
| LAG      | Previous row |
| LEAD     | Next row     |

**Interview Line**

> “LEAD and LAG help compare rows without self-joins.”

---

## PART 7: SQL Query Optimization (INTERVIEW MUST)

---

## 7️⃣ Use Index-Friendly Conditions

❌ BAD

```sql
WHERE YEAR(hire_date) = 2024
```

✅ GOOD

```sql
WHERE hire_date >= DATE '2024-01-01'
AND hire_date < DATE '2025-01-01';
```

---

## 8️⃣ Avoid SELECT *

❌ BAD

```sql
SELECT *
FROM employee;
```

✅ GOOD

```sql
SELECT emp_id, salary
FROM employee;
```

---

## 9️⃣ WHERE vs HAVING

* `WHERE` → filters rows (early)
* `HAVING` → filters groups (late)

❌ BAD

```sql
HAVING salary > 50000
```

✅ GOOD

```sql
WHERE salary > 50000
```

---

## 🔟 NOT IN vs NOT EXISTS

❌ BAD (NULL issue)

```sql
WHERE id NOT IN (SELECT id FROM orders)
```

✅ GOOD

```sql
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.id = e.id
)
```

---

## 1️⃣1️⃣ Use EXISTS instead of IN (Large Data)

* `IN` → materializes subquery
* `EXISTS` → stops at first match

---

## 1️⃣2️⃣ JOIN before SUBQUERY

❌ BAD

```sql
SELECT * FROM emp
WHERE dept_id IN (SELECT dept_id FROM dept);
```

✅ GOOD

```sql
SELECT e.*
FROM emp e
JOIN dept d ON e.dept_id = d.dept_id;
```

---

## FINAL OPTIMIZATION RULES (MEMORIZE)

* Filter early (`WHERE`)
* Reduce columns
* Use indexes
* Avoid functions on indexed columns
* Prefer `EXISTS` over `IN`
* Use `JOIN` instead of correlated subqueries
* Partition → filter
* Bucket → join

---

## 🧠 30-SECOND INTERVIEW CHEAT

* Salary → `DENSE_RANK`
* Delete duplicates → `ROW_NUMBER`
* Previous / Next row → `LAG / LEAD`
* Big tables → Partition
* Joins → Bucket
* NULL-safe anti-join → `NOT EXISTS`

---
