
````md

<img width="1536" height="709" alt="image" src="https://github.com/user-attachments/assets/661bd125-4dae-41fd-9855-f686757addc3" />
<img width="1536" height="709" alt="image" src="https://github.com/user-attachments/assets/661bd125-4dae-41fd-9855-f686757addc3" />
<img width="1536" height="709" alt="image" src="https://github.com/user-attachments/assets/661bd125-4dae-41fd-9855-f686757addc3" />
![SQL Interview Notes](https://github.com/user-attachments/assets/661bd125-4dae-41fd-9855-f686757addc3)


# SQL Interview Preparation – Part 1  
## Table Creation & Duplicate Handling

This repository contains commonly asked SQL interview questions with clear explanations, examples, and common interviewer traps.

---

## 1. Create New Table Structure From Existing Table (Schema Only)

### Question  
How to create a new table structure based on an existing table without copying data?

### Answer
```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table
WHERE 1 = 0;
````

### Explanation

* `SELECT * FROM old_table` copies the table structure
* `WHERE 1 = 0` ensures no rows are copied
* Result: only schema is created, no data

### Alternative (MySQL / PostgreSQL)

```sql
CREATE TABLE new_table LIKE old_table;
```

### Interview Traps / Counter Questions

* Why use `WHERE 1 = 0`?
  → To avoid copying data and create only structure
* Are primary keys, foreign keys, indexes copied?
  → No, constraints are not copied
* Difference between `LIKE` and `CTAS`?
  → `LIKE` preserves structure more accurately, `CTAS` is generic

---

## 2. Create New Table From Existing Table (With Data)

### Question

How to create a new table and copy data from an existing table?

### Answer

```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table;
```

### With Condition

```sql
CREATE TABLE new_table AS
SELECT *
FROM old_table
WHERE status = 'ACTIVE';
```

### Explanation

* Copies both structure and data
* Constraints are not copied

### Interview Traps

* Does it copy indexes or constraints?
  → No
* How to copy data into an already existing table?
  → Use `INSERT INTO new_table SELECT ...`

---

## 3. Find Duplicate Records in a Table

### Question

How to check whether duplicate records exist in a table?

### Answer

```sql
SELECT emp_id, COUNT(*)
FROM employee
GROUP BY emp_id
HAVING COUNT(*) > 1;
```

### Explanation

* `GROUP BY` groups same values
* `HAVING COUNT(*) > 1` identifies duplicates

### Interview Traps

* Why `HAVING` and not `WHERE`?
  → `WHERE` filters rows, `HAVING` filters grouped data
* What if query returns no rows?
  → No duplicates exist

---

## 4. Find Records Repeated Multiple Times

### Question

How to find duplicate records along with how many times they are repeated?

### Answer

```sql
SELECT emp_id, COUNT(*) AS duplicate_count
FROM employee
GROUP BY emp_id
HAVING COUNT(*) > 1;
```

### Explanation

* Same as duplicate detection
* Added count to know frequency

### Interview Traps

* Can results be sorted by highest duplicates?
  → Yes, using `ORDER BY duplicate_count DESC`

---

## 5. Remove Duplicate Records From Table

### Question

How to delete duplicate rows and keep only one record?

### Answer (Best Practice)

```sql
DELETE FROM employee
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY id) AS rn
        FROM employee
    ) t
    WHERE rn > 1
);
```

### Explanation

* `PARTITION BY emp_id` groups duplicate records
* `ROW_NUMBER()` assigns unique numbers
* `rn > 1` marks duplicate rows
* Keeps one row per `emp_id`

### Interview Traps

* Which row is retained?
  → The row with the lowest `id`
* How to keep the latest record instead?
  → Change `ORDER BY id` to `ORDER BY created_date DESC`
* Why is subquery required?
  → Window functions cannot be directly used in DELETE
* Why `ROW_NUMBER` and not `DENSE_RANK` here?
  → We want exactly one record per group

---

## Key Learnings

* `CTAS` copies structure and data but not constraints
* `HAVING` is used for aggregate filtering
* `ROW_NUMBER()` is ideal for deleting duplicates
* `ORDER BY` controls which record is retained
* Always think about duplicates and determinism

---

## Author Notes

This repository is built for interview preparation with focus on:

* Clarity of logic
* Interview-oriented explanations
* Common traps and follow-up questions

```

---

### 🔥 Strict mentor note
- This README alone is **enough to clear SQL round basics**
- Commit this today
- Next you’ll add **Salary + Window Functions** as Part-2

When you’re ready, say:  
**“Give me Part-2 README (Salary + Window Functions)”**  
and we continue.
```

Perfect. **Part-2 is where interviews are actually won or lost.**
Below is a **copy-paste ready `README.md` (Part-2)** written **slow, clear, and interview-proof**.
No shortcuts. This will *lock in* window functions in your brain.

---

````md
# SQL Interview Preparation – Part 2  
## Salary Problems & Window Functions

This section focuses on salary-based SQL interview questions and proper usage of window functions like ROW_NUMBER, RANK, and DENSE_RANK, along with common interviewer traps.

---

## 1. Find the 2nd Highest Salary

### Question  
How to find the 2nd highest salary from the employee table?

---

### Method 1: Using DENSE_RANK (Recommended)

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
    FROM employee
) t
WHERE dr = 2;
````

### Explanation

* Salaries are ordered from highest to lowest
* `DENSE_RANK()` assigns the same rank to duplicate salaries
* Rank = 2 gives the 2nd highest **distinct** salary

### Interview Traps

* Why not `ROW_NUMBER()`?
  → It gives different numbers even for same salary
* What if multiple employees have same 2nd highest salary?
  → All will be returned

---

### Method 2: Using Subquery (Classic but risky)

```sql
SELECT MAX(salary)
FROM employee
WHERE salary < (SELECT MAX(salary) FROM employee);
```

### Trap

* Fails when highest salary is duplicated
* Interviewers prefer window functions

---

## 2. Find the 3rd Highest Salary

### Answer

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
    FROM employee
) t
WHERE dr = 3;
```

### Explanation

* Same logic as 2nd highest
* Change rank value only

### Interview Trap

* Using `ROW_NUMBER()` instead of `DENSE_RANK()` when duplicates exist

---

## 3. Find the 2nd Highest Salary in Each Department

### Question

Find the 2nd highest salary **department-wise**.

### Answer

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
    FROM employee
) t
WHERE dr = 2;
```

### Explanation

* `PARTITION BY dept` separates data by department
* Ranking resets for each department
* `DENSE_RANK()` handles duplicate salaries

### Interview Traps

* What happens if PARTITION BY is removed?
  → Ranking becomes global, not department-wise
* Why not GROUP BY?
  → GROUP BY collapses rows, window functions do not

---

## 4. Find the Bottom 2 Salaries

### Question

How to find employees with the lowest 2 salaries?

### Answer

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY salary ASC) AS rn
    FROM employee
) t
WHERE rn <= 2;
```

### Explanation

* Salaries ordered from lowest to highest
* `ROW_NUMBER()` is enough because order matters, not duplicates

### Interview Trap

* Using `TOP 2` without `ORDER BY` is non-deterministic

---

## 5. Difference Between ROW_NUMBER, RANK, and DENSE_RANK

| Function   | Duplicate Values | Rank Gap |
| ---------- | ---------------- | -------- |
| ROW_NUMBER | ❌ No             | ❌ No     |
| RANK       | ✅ Yes            | ✅ Yes    |
| DENSE_RANK | ✅ Yes            | ❌ No     |

### When to Use

* ROW_NUMBER → deleting duplicates, pagination
* DENSE_RANK → salary, marks, ranking problems
* RANK → rarely used in interviews

---

## 6. Why ORDER BY is Mandatory

### Wrong

```sql
SELECT TOP 2 *
FROM employee;
```

### Correct

```sql
SELECT TOP 2 *
FROM employee
ORDER BY salary DESC;
```

### Explanation

* Tables are unordered
* Without ORDER BY, results are unpredictable

### Interview Line (Memorize)

> “Without ORDER BY, SQL results are non-deterministic.”

---

## 7. Common Interview Traps (Must Remember)

* Using ROW_NUMBER when duplicate salaries exist
* Forgetting PARTITION BY in department-based questions
* Using TOP or LIMIT without ORDER BY
* Solving ranking problems using only subqueries

---

## Key Learnings

* DENSE_RANK is best for salary problems
* PARTITION BY controls grouping in window functions
* ORDER BY controls ranking and determinism
* Window functions are preferred over subqueries

---

## Author Notes

This section is written to:

* Build correct mental models
* Avoid common interview mistakes
* Explain logic clearly, not just syntax

```
<img width="618" height="348" alt="image" src="https://github.com/user-attachments/assets/d6dccf8c-bfce-4f12-a723-2e9983e643f3" />



Good. These are **classic SQL salary questions**.
I’ll teach you **how to answer**, **what to write**, and **what traps interviewers set** — all in **GitHub-ready language**.

Below is a **Part-2 continuation section** you can directly add after your existing Part-2 README.

---

## ✅ SQL – PART 2 (Answer + Interview Traps)

Copy-paste this into GitHub 👇

````md
# SQL Interview Preparation – Part 2 (Extended)
## Salary Problems – Answers & Interview Traps

---

## Query 1: Find 2nd Highest Salary (Different Ways)

### Method 1: Using DENSE_RANK (Recommended)
```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS r
    FROM employee
) t
WHERE r = 2;
````

### Why this works

* Orders salaries from highest to lowest
* Same salaries get same rank
* Rank = 2 gives 2nd highest **distinct** salary

### Interview Traps

* ❌ Using ROW_NUMBER when duplicate salaries exist
* ❌ Using TOP without ORDER BY
* ✔ Interviewers prefer window functions over subqueries

---

## Query 2: Find 3rd Highest Salary

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS r
    FROM employee
) t
WHERE r = 3;
```

### Interview Traps

* What if there is no 3rd highest salary?
  → Query returns no rows
* Why not ROW_NUMBER?
  → It ignores duplicate salaries

---

## Query 3: Find 2nd Highest Salary Based on Each Department

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS r
    FROM employee
) t
WHERE r = 2;
```

### Why PARTITION BY is required

* Ranking resets inside each department
* Without PARTITION BY → global ranking (wrong)

### Interview Traps

* ❌ Forgetting PARTITION BY
* ❌ Using GROUP BY (loses row-level data)

---

## Query 4: Find Bottom 2 Salary Employee Details

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY salary ASC) AS rn
    FROM employee
) t
WHERE rn <= 2;
```

### Why ROW_NUMBER is OK here

* We just want lowest two rows
* Duplicate salary handling is not critical

### Interview Traps

* ❌ Using TOP 2 without ORDER BY
* ✔ Always mention determinism

---

## Query 5: Find Top 2 Salary Employee Details

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
    FROM employee
) t
WHERE rn <= 2;
```

### Interview Traps

* If interviewer asks “what if salaries are same?”
  → Switch to DENSE_RANK

```sql
DENSE_RANK() OVER (ORDER BY salary DESC)
```

---

## Query 6: Find Lowest Salary Employee in Each Department

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary ASC) AS rn
    FROM employee
) t
WHERE rn = 1;
```

### Why this works

* PARTITION BY → department-wise
* ORDER BY salary ASC → lowest first
* rn = 1 → lowest salary employee

### Interview Traps

* What if multiple employees have same lowest salary?
  → Use DENSE_RANK instead of ROW_NUMBER

---

## Query 7: Find 3rd to 5th Salary Employees

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS r
    FROM employee
) t
WHERE r BETWEEN 3 AND 5;
```

### Why DENSE_RANK

* Maintains correct ranking even with duplicates
* BETWEEN helps range-based selection

### Interview Traps

* ❌ Using ROW_NUMBER gives wrong range if duplicates exist
* ✔ Clarify whether interviewer wants distinct salaries

---

## Common Interview Trap Questions (Must Remember)

* Why DENSE_RANK over ROW_NUMBER?
  → When duplicate values matter
* Why ORDER BY is mandatory?
  → SQL tables are unordered
* Why window functions preferred?
  → Cleaner, scalable, readable
* Difference between GROUP BY and PARTITION BY?
  → GROUP BY reduces rows, PARTITION BY does not

---

## Final Mental Rule (Memorize)

* Ranking + duplicates → DENSE_RANK
* Per group logic → PARTITION BY
* Deterministic result → ORDER BY
* Just numbering rows → ROW_NUMBER

```

---

## 🔥 Brutally honest mentor note
If you can **explain these 7 queries calmly**, you are:
- ✅ Safe for SQL rounds
- ✅ Better than average TCS → product-company candidates
- ❌ Still rejected if you panic (we’ll fix that next)

---

### What I recommend next (important)
Choose ONE:
1. **JOINs with interview traps (very high priority)**
2. **SQL execution order (FROM → WHERE → GROUP BY…)**
3. **Mock SQL interview (I ask, you answer, I correct)**

Reply with **1 / 2 / 3**.
```

