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
Good, this is an **important window function** and many people *think* they know it but actually don’t.
I’ll explain **slowly, clearly, with a table**, then give you **interview traps + revision notes**.

---

# LAG() and LEAD() — Explained Like You’re New

Think of your data as **people standing in a line**.

* **LAG** → look **back** (previous person)
* **LEAD** → look **ahead** (next person)

No joins. No subqueries. Just looking left or right.

---

## Example Data (Employee Salaries)

| emp_id | emp_name | salary |
| ------ | -------- | ------ |
| 101    | A        | 50,000 |
| 102    | B        | 60,000 |
| 103    | C        | 55,000 |
| 104    | D        | 70,000 |

---

## 1️⃣ LAG() – Look at Previous Row

### Question

👉 “Show each employee’s salary and the **previous employee’s salary**”

### Query

```sql
SELECT
    emp_id,
    emp_name,
    salary,
    LAG(salary) OVER (ORDER BY emp_id) AS prev_salary
FROM employee;
```

### Result

| emp_id | salary | prev_salary |
| ------ | ------ | ----------- |
| 101    | 50,000 | NULL        |
| 102    | 60,000 | 50,000      |
| 103    | 55,000 | 60,000      |
| 104    | 70,000 | 55,000      |

### Explanation

* First row has **no previous row** → NULL
* Every row looks **one row back**

---

## 2️⃣ LEAD() – Look at Next Row

### Question

👉 “Show each employee’s salary and the **next employee’s salary**”

### Query

```sql
SELECT
    emp_id,
    emp_name,
    salary,
    LEAD(salary) OVER (ORDER BY emp_id) AS next_salary
FROM employee;
```

### Result

| emp_id | salary | next_salary |
| ------ | ------ | ----------- |
| 101    | 50,000 | 60,000      |
| 102    | 60,000 | 55,000      |
| 103    | 55,000 | 70,000      |
| 104    | 70,000 | NULL        |

### Explanation

* Last row has **no next row** → NULL
* Every row looks **one row ahead**

---

## 3️⃣ LAG / LEAD with Default Value

Instead of NULL, you can give a default value.

### LAG with default

```sql
LAG(salary, 1, 0) OVER (ORDER BY emp_id)
```

### LEAD with default

```sql
LEAD(salary, 1, 0) OVER (ORDER BY emp_id)
```

### Meaning

* Look 1 row back/forward
* If not found → return `0`

---

## 4️⃣ Real Interview Example – Salary Difference

### Question

👉 “Find salary difference compared to previous employee”

```sql
SELECT
    emp_id,
    salary,
    salary - LAG(salary) OVER (ORDER BY emp_id) AS salary_diff
FROM employee;
```

### Result (important logic)

* Positive → salary increased
* Negative → salary decreased

---

## 5️⃣ Department-wise LAG / LEAD (VERY IMPORTANT)

### Data

| emp_id | dept | salary |
| ------ | ---- | ------ |
| 1      | IT   | 50,000 |
| 2      | IT   | 60,000 |
| 3      | HR   | 40,000 |
| 4      | HR   | 45,000 |

### Query

```sql
SELECT
    emp_id,
    dept,
    salary,
    LAG(salary) OVER (PARTITION BY dept ORDER BY emp_id) AS prev_dept_salary
FROM employee;
```

### Why PARTITION BY?

* Resets comparison **inside each department**
* HR doesn’t compare with IT

---

## 🔥 INTERVIEW TRAPS (VERY IMPORTANT)

### Trap 1: Missing ORDER BY ❌

```sql
LAG(salary) OVER ()
```

➡️ Result is **meaningless**

👉 Always specify ORDER BY

---

### Trap 2: Using self-join instead of LAG ❌

❌ Old way:

```sql
FROM emp e1
JOIN emp e2 ON e1.emp_id = e2.emp_id + 1
```

✅ Better:

```sql
LAG() / LEAD()
```

---

### Trap 3: Wrong ordering

* Ordering by `salary` vs `emp_id` changes meaning
* Always confirm **business logic**

---

## 🧠 One-Line Interview Answers (MEMORIZE)

* **LAG**

  > “LAG fetches data from the previous row without self-joins.”

* **LEAD**

  > “LEAD fetches data from the next row for comparison.”

* **Why use them**

  > “They simplify row-to-row comparison and improve readability.”

---

## 📝 Ultra-Short Revision Notes (Put in SQL.md)

```md
LAG(col)  → previous row value
LEAD(col) → next row value
Always use ORDER BY
Use PARTITION BY for group-wise comparison
Avoid self-joins
```

---

### Mentor verdict (honest)

If you can:

* Draw this table on paper
* Explain prev vs next row calmly

👉 You will **not get stuck** on LAG/LEAD questions.

---

<img width="635" height="738" alt="image" src="https://github.com/user-attachments/assets/c373e1dd-6397-4f1c-bb09-6dd535b4fa97" />


<img width="940" height="1058" alt="image" src="https://github.com/user-attachments/assets/3c351468-59ad-4fd0-bd4e-5ed98ad1bec1" />
<img width="925" height="295" alt="image" src="https://github.com/user-attachments/assets/be080429-095c-4a86-b7e2-603a66516d9c" />
<img width="638" height="738" alt="image" src="https://github.com/user-attachments/assets/fd2f7c60-a947-44ad-960b-d6ba0751aedb" />
<img width="924" height="317" alt="image" src="https://github.com/user-attachments/assets/70bab5f1-292f-4152-a707-1be9dbf8dfa5" />
<img width="631" height="253" alt="image" src="https://github.com/user-attachments/assets/90181bdd-30d0-4e11-8c6e-4b98f0dd2948" />
<img width="940" height="1104" alt="image" src="https://github.com/user-attachments/assets/3eb4bb6a-67ff-451f-b8be-563774c5cf52" />
<img width="940" height="1094" alt="image" src="https://github.com/user-attachments/assets/cba541eb-8eec-4829-a6d6-a0345e44fd69" />


<img width="940" height="1094" alt="image" src="https://github.com/user-attachments/assets/272592aa-526f-45f3-a353-f87d82119f7a" />

<img width="934" height="517" alt="image" src="https://github.com/user-attachments/assets/a478e751-ce9c-43ac-8379-6108b6065ffa" />
<img width="940" height="1093" alt="image" src="https://github.com/user-attachments/assets/e1fa3628-9158-48b9-8043-1162f64ebc2c" />
<img width="620" height="444" alt="image" src="https://github.com/user-attachments/assets/b827d53b-9c08-4cf6-bd59-79b8dbeb2227" />
<img width="940" height="1099" alt="image" src="https://github.com/user-attachments/assets/305e1745-1672-411f-9aaf-c11854e3543f" />
<img width="616" height="532" alt="image" src="https://github.com/user-attachments/assets/ea512437-0c18-42fd-a11a-f8a500c02125" />



Great question 👍
`OFFSET` and `LIMIT` are **very common hands-on interview questions**, especially for **pagination**. I’ll explain **slowly, with examples, traps, and interview lines** so you don’t get confused.

---

# OFFSET and LIMIT — Explained Simply

Think of a **list of records** and you want to **skip some rows and then pick a few**.

* **OFFSET** → how many rows to **skip**
* **LIMIT** → how many rows to **return**

---

## Example Table: `employee`

| emp_id | name | salary |
| ------ | ---- | ------ |
| 1      | A    | 10000  |
| 2      | B    | 20000  |
| 3      | C    | 30000  |
| 4      | D    | 40000  |
| 5      | E    | 50000  |
| 6      | F    | 60000  |

---

## 1️⃣ LIMIT only

### Question

👉 “Give me first 3 employees”

```sql
SELECT *
FROM employee
ORDER BY emp_id
LIMIT 3;
```

### Result

```
1, 2, 3
```

---

## 2️⃣ OFFSET only

### Question

👉 “Skip first 3 employees”

```sql
SELECT *
FROM employee
ORDER BY emp_id
OFFSET 3;
```

### Result

```
4, 5, 6
```

---

## 3️⃣ OFFSET + LIMIT (MOST IMPORTANT)

### Question

👉 “Skip first 2 employees and show next 3”

```sql
SELECT *
FROM employee
ORDER BY emp_id
LIMIT 3 OFFSET 2;
```

### Result

```
3, 4, 5
```

---

## 4️⃣ Pagination Example (VERY COMMON)

### Page size = 2

| Page   | OFFSET | LIMIT |
| ------ | ------ | ----- |
| Page 1 | 0      | 2     |
| Page 2 | 2      | 2     |
| Page 3 | 4      | 2     |

### Page-2 query

```sql
SELECT *
FROM employee
ORDER BY emp_id
LIMIT 2 OFFSET 2;
```

---

## 5️⃣ OFFSET + LIMIT for Nth Highest Salary

### 2nd highest salary

```sql
SELECT *
FROM employee
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

### Explanation

* Order salaries DESC
* Skip highest
* Pick next one

⚠️ Works **only if no duplicates**

---

## 6️⃣ Oracle Equivalent (VERY IMPORTANT)

Oracle does **NOT support LIMIT/OFFSET directly**.

### Using FETCH FIRST (Oracle 12c+)

```sql
SELECT *
FROM employee
ORDER BY emp_id
OFFSET 2 ROWS FETCH NEXT 3 ROWS ONLY;
```

### First 3 rows

```sql
FETCH FIRST 3 ROWS ONLY;
```

---

## 🔥 INTERVIEW TRAPS (VERY IMPORTANT)

### Trap 1: Using OFFSET without ORDER BY ❌

```sql
SELECT * FROM employee LIMIT 3 OFFSET 2;
```

👉 Result is **non-deterministic**

✅ Always use ORDER BY

---

### Trap 2: Performance issue with large OFFSET

```sql
OFFSET 1000000
```

👉 Database still scans skipped rows
👉 Bad for large data

**Interview line**

> “OFFSET is inefficient for deep pagination.”

---

### Trap 3: Duplicate values problem

OFFSET + LIMIT fails when duplicates matter

❌ For salary ranking
✅ Use `DENSE_RANK`

---

## 🧠 OFFSET vs LIMIT (One-Line)

* `LIMIT` → how many rows to return
* `OFFSET` → how many rows to skip

---

## 🧠 Interview One-Liners (Memorize)

* “OFFSET and LIMIT are mainly used for pagination.”
* “Always combine OFFSET with ORDER BY.”
* “For large datasets, keyset pagination is better.”

---

## 📝 Mini Revision Note (Put in SQL.md)

```md
LIMIT N        → return N rows
OFFSET M       → skip M rows
Always use ORDER BY
OFFSET is slow for deep pagination
Oracle uses FETCH FIRST / OFFSET
```

---




 
  
 
 
 
 
 



 
 
 
 
 
 
