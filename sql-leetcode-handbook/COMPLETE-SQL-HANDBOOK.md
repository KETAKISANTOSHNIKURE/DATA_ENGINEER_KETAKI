# Complete SQL Interview Handbook
## Top 50 LeetCode-Style Questions with Patterns, Solutions & Tricks

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Pattern Overview](#2-pattern-overview)
3. [Top 50 SQL LeetCode Problems](#3-top-50-sql-leetcode-problems)
   - [Basic SELECT & Filtering (1–10)](#basic-select--filtering-110)
   - [JOINs (11–20)](#joins-1120)
   - [Aggregation & GROUP BY (21–30)](#aggregation--group-by-2130)
   - [Window Functions & Ranking (31–40)](#window-functions--ranking-3140)
   - [Advanced (41–50)](#advanced-4150)

---

## 1. Introduction

### How SQL Interview Problems Are Structured

SQL interview questions typically test your ability to:

- **Select** and **filter** data from one or more tables
- **Aggregate** with `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- **Group** results with `GROUP BY` and filter groups with `HAVING`
- **Join** tables (INNER, LEFT, self-join)
- **Nest** queries (subqueries, CTEs)
- **Apply window functions** (ranking, running totals, lead/lag)
- **Handle edge cases** (NULL, duplicates, empty sets, ties)

Most problems combine 2–3 of these concepts. Recognizing the **pattern** from keywords in the question is the fastest way to choose the right approach.

### Main Patterns

| Pattern | Core Concept |
|---------|--------------|
| **Selection & Filtering** | `WHERE`, `AND`, `OR`, `IN`, `BETWEEN`, `LIKE`, `IS NULL` |
| **Aggregation** | `COUNT`, `SUM`, `AVG`, `MAX`, `MIN` |
| **Grouping** | `GROUP BY` + `HAVING` |
| **Joins** | `INNER JOIN`, `LEFT JOIN`, multiple tables |
| **Self-join** | Same table joined to itself (e.g., employee vs manager) |
| **Subquery** | Query inside `WHERE`, `FROM`, or `SELECT` |
| **Window functions** | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `SUM OVER`, `COUNT OVER` |
| **Case expression** | `CASE WHEN ... THEN ... ELSE ... END` for conditional logic |

---

## 2. Pattern Overview

| Pattern | When to Use | Intuition |
|---------|-------------|-----------|
| **Basic SELECT** | Simple row filtering | "Find rows where column = value" → `WHERE` |
| **Aggregation** | Summarize data | "Count", "sum", "average" → `COUNT`, `SUM`, `AVG` + `GROUP BY` |
| **GROUP BY + HAVING** | Filter groups | "Duplicates", "at least N", "more than once" → `HAVING COUNT(*) > 1` |
| **LEFT JOIN + NULL** | Anti-join (rows NOT in another table) | "Never", "did not", "without" → `LEFT JOIN` + `WHERE right.id IS NULL` |
| **Self-join** | Compare rows within same table | "Manager", "previous day", "consecutive" → join table to itself |
| **Subquery** | Filter or compute from derived set | "Highest", "in list" → `WHERE col IN (SELECT ...)` or `WHERE col = (SELECT MAX(...))` |
| **ROW_NUMBER / RANK** | Top N, Nth highest, first per group | "Second highest", "top 3 per department" → `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` |
| **LAG / LEAD** | Compare with previous/next row | "Rising", "yesterday", "consecutive" → `LAG(col) OVER (ORDER BY date)` |
| **Running sum** | Cumulative totals | "Running total", "moving average" → `SUM() OVER (ORDER BY date)` |
| **UNION / UNION ALL** | Combine result sets | "Both", "either table" → `UNION` (distinct) or `UNION ALL` (with dupes) |

---

## 3. Top 50 SQL LeetCode Problems

---

### Basic SELECT & Filtering (1–10)

---

#### Problem 1 – Recyclable and Low Fat Products (LeetCode 1757)

- **Pattern(s):** Basic SELECT + WHERE (multiple conditions)
- **Recognize by these keywords:**
  - "low fat", "recyclable"
  - "filter products"
  - "both conditions"

- **Typical schema (simplified):**

```text
Table: Products
Columns:
  - product_id (PK)
  - low_fats ('Y' / 'N')
  - recyclable ('Y' / 'N')
```

- **Goal in plain English:** Return product_ids where low_fats = 'Y' AND recyclable = 'Y'.

##### SQL Solution

```sql
SELECT product_id
FROM Products
WHERE low_fats = 'Y'
  AND recyclable = 'Y';
```

##### Step-by-Step Explanation

1. Read from `Products`.
2. `WHERE` keeps only rows with both conditions true.
3. Return `product_id` only.

##### Common Pitfalls

- Forgetting `AND` (using `OR` would include products with only one attribute).
- Selecting extra columns when only `product_id` is required.

##### Interview Tricks

- "Both" / "all conditions" → `AND`. "Either" → `OR`.
- Single-table filter with no aggregation → simple `WHERE`.

---

#### Problem 2 – Find Customer Referee (LeetCode 584)

- **Pattern(s):** Basic SELECT + WHERE with NULL handling
- **Recognize by these keywords:**
  - "referee_id", "not 2"
  - "exclude referee_id = 2"
  - "include NULL referee"

- **Typical schema (simplified):**

```text
Table: Customer
Columns:
  - id (PK)
  - name
  - referee_id (FK, nullable)
```

- **Goal in plain English:** Return customers whose referee_id is NULL or not 2.

##### SQL Solution

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL
   OR referee_id != 2;
```

##### Step-by-Step Explanation

1. From `Customer`, filter rows.
2. `referee_id IS NULL` includes customers with no referee.
3. `referee_id != 2` excludes referee 2. `OR` means either condition passes.

##### Common Pitfalls

- Using only `referee_id != 2` drops NULLs because `NULL != 2` is UNKNOWN (treated as FALSE in WHERE).

##### Interview Tricks

- Whenever you "exclude value X" but want to keep NULLs → add `OR col IS NULL`.
- Mental shortcut: "NOT 2 but keep NULL" → `(referee_id IS NULL OR referee_id != 2)`.

---

#### Problem 3 – Big Countries (LeetCode 595)

- **Pattern(s):** Basic SELECT + WHERE (OR condition)
- **Recognize by these keywords:**
  - "big country"
  - "area OR population threshold"
  - "either condition"

- **Typical schema (simplified):**

```text
Table: World
Columns:
  - name (PK)
  - continent
  - area
  - population
  - gdp
```

- **Goal in plain English:** Return countries where area >= 3,000,000 OR population >= 25,000,000.

##### SQL Solution

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000
   OR population >= 25000000;
```

##### Step-by-Step Explanation

1. From `World`, filter rows.
2. `OR` includes rows that satisfy either condition (or both).

##### Common Pitfalls

- Using `AND` instead of `OR` would require both conditions (too strict).

##### Interview Tricks

- "Big if either X or Y" → `OR`. "Must satisfy both" → `AND`.

---

#### Problem 4 – Article Views I (LeetCode 1148)

- **Pattern(s):** Basic SELECT + WHERE (self-condition) + DISTINCT
- **Recognize by these keywords:**
  - "viewed their own article"
  - "author_id = viewer_id"
  - "distinct authors"

- **Typical schema (simplified):**

```text
Table: Views
Columns:
  - article_id
  - author_id
  - viewer_id
  - view_date
```

- **Goal in plain English:** Return distinct author_ids who viewed their own article (author_id = viewer_id), sorted.

##### SQL Solution

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;
```

##### Step-by-Step Explanation

1. Filter where author and viewer are the same.
2. `DISTINCT` removes duplicate author_ids.
3. `ORDER BY id` sorts the result.

##### Common Pitfalls

- Omitting `DISTINCT` when an author can view their article multiple times.

##### Interview Tricks

- "Their own" → same-column comparison: `col1 = col2`.
- "Distinct" / "unique" → `DISTINCT` or `GROUP BY`.

---

#### Problem 5 – Invalid Tweets (LeetCode 1683)

- **Pattern(s):** Basic SELECT + WHERE (string length)
- **Recognize by these keywords:**
  - "invalid"
  - "content length", "character count"
  - "greater than 15"

- **Typical schema (simplified):**

```text
Table: Tweets
Columns:
  - tweet_id (PK)
  - content
```

- **Goal in plain English:** Return tweet_ids where content has more than 15 characters.

##### SQL Solution

```sql
SELECT tweet_id
FROM Tweets
WHERE CHAR_LENGTH(content) > 15;
```

##### Step-by-Step Explanation

1. `CHAR_LENGTH(content)` counts characters (use `LENGTH` for bytes if needed).
2. Filter rows with length > 15.

##### Common Pitfalls

- Using `LENGTH` when multi-byte characters matter (prefer `CHAR_LENGTH`).
- Storing length in a variable when a simple expression is enough.

##### Interview Tricks

- "Invalid if too long/short" → `CHAR_LENGTH(col) > N` or `< N`.
- MySQL: `CHAR_LENGTH` / `LENGTH`. PostgreSQL: `LENGTH` / `CHAR_LENGTH`.

---

#### Problem 6 – Replace Employee ID With The Unique Identifier (LeetCode 1378)

- **Pattern(s):** LEFT JOIN
- **Recognize by these keywords:**
  - "replace", "unique identifier"
  - "optional" / "may not have"
  - "keep all employees"

- **Typical schema (simplified):**

```text
Table: Employees (id, name)
Table: EmployeeUNI (id, unique_id)
```

- **Goal in plain English:** For each employee, show unique_id (NULL if none) and name. Keep all employees.

##### SQL Solution

```sql
SELECT eu.unique_id, e.name
FROM Employees e
LEFT JOIN EmployeeUNI eu ON e.id = eu.id;
```

##### Step-by-Step Explanation

1. `LEFT JOIN` keeps every row from `Employees`.
2. Rows without a match in `EmployeeUNI` get NULL for `unique_id`.
3. Return `unique_id` and `name`.

##### Common Pitfalls

- Using `INNER JOIN` drops employees without a unique_id.

##### Interview Tricks

- "Keep all from A, add optional B" → `LEFT JOIN`.
- "Only rows that exist in both" → `INNER JOIN`.

---

#### Problem 7 – Product Sales Analysis I (LeetCode 1068)

- **Pattern(s):** INNER JOIN
- **Recognize by these keywords:**
  - "product name", "year", "price"
  - "combine Sales and Product"
  - "for each sale"

- **Typical schema (simplified):**

```text
Table: Sales (sale_id, product_id, year, quantity, price)
Table: Product (product_id, product_name)
```

- **Goal in plain English:** For each sale, return product_name, year, and price.

##### SQL Solution

```sql
SELECT p.product_name, s.year, s.price
FROM Sales s
INNER JOIN Product p ON s.product_id = p.product_id;
```

##### Step-by-Step Explanation

1. Join Sales to Product on `product_id`.
2. `INNER JOIN` keeps only sales with a matching product.
3. Select `product_name` from Product, `year` and `price` from Sales.

##### Common Pitfalls

- Selecting from the wrong table (e.g., product_name from Sales).

##### Interview Tricks

- "Enrich rows with lookup data" → `INNER JOIN` when every row must have a match.

---

#### Problem 8 – Customer Who Visited but Did Not Make Transactions (LeetCode 1581)

- **Pattern(s):** LEFT JOIN + anti-join (WHERE right IS NULL)
- **Recognize by these keywords:**
  - "visited but did not"
  - "no transactions"
  - "count per customer"

- **Typical schema (simplified):**

```text
Table: Visits (visit_id, customer_id)
Table: Transactions (transaction_id, visit_id, amount)
```

- **Goal in plain English:** Count visits per customer that have no corresponding transaction.

##### SQL Solution

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

##### Step-by-Step Explanation

1. `LEFT JOIN` keeps all visits.
2. Where no transaction exists, `t.transaction_id` is NULL.
3. `WHERE t.transaction_id IS NULL` keeps only such visits.
4. `GROUP BY customer_id` and `COUNT(*)` gives count per customer.

##### Common Pitfalls

- Forgetting `GROUP BY customer_id` when counting per customer.
- Using `WHERE visit_id IS NULL` instead of a column from the right table.

##### Interview Tricks

- "Did not", "never", "without" → anti-join: `LEFT JOIN` + `WHERE right.id IS NULL`.
- Alternative: `WHERE id NOT IN (SELECT ...)`.

---

#### Problem 9 – Rising Temperature (LeetCode 197)

- **Pattern(s):** Self-comparison with LAG (window function)
- **Recognize by these keywords:**
  - "rising", "higher than yesterday"
  - "previous day", "compare with yesterday"
  - "consecutive dates"

- **Typical schema (simplified):**

```text
Table: Weather
Columns:
  - id (PK)
  - recordDate (date)
  - temperature
```

- **Goal in plain English:** Return ids where temperature is higher than the previous day's temperature.

##### SQL Solution

```sql
SELECT id
FROM (
    SELECT id,
           recordDate,
           temperature,
           LAG(temperature) OVER (ORDER BY recordDate) AS prev_temp,
           LAG(recordDate) OVER (ORDER BY recordDate) AS prev_date
    FROM Weather
) t
WHERE temperature > prev_temp
  AND DATEDIFF(recordDate, prev_date) = 1;
```

##### Step-by-Step Explanation

1. `LAG(temperature)` and `LAG(recordDate)` get previous row values by date.
2. Filter where current temp > prev temp.
3. `DATEDIFF = 1` ensures rows are consecutive days (handles gaps).

##### Common Pitfalls

- Ignoring date gaps (e.g., weekend) — compare only with true yesterday.
- Wrong order in `LAG` (must `ORDER BY recordDate`).

##### Interview Tricks

- "Compared to previous row" → `LAG` or `LEAD`.
- "Consecutive days" → use `DATEDIFF` or equivalent to validate.

---

#### Problem 10 – Average Time of Process per Machine (LeetCode 1661)

- **Pattern(s):** Self-join to match start/end + aggregation
- **Recognize by these keywords:**
  - "average time", "per machine"
  - "start" and "end" activities
  - "process"

- **Typical schema (simplified):**

```text
Table: Activity
Columns:
  - machine_id
  - process_id
  - activity_type ('start' / 'end')
  - timestamp
```

- **Goal in plain English:** For each machine, average (end - start) time per process.

##### SQL Solution

```sql
SELECT a.machine_id,
       ROUND(AVG(b.timestamp - a.timestamp), 3) AS processing_time
FROM Activity a
JOIN Activity b ON a.machine_id = b.machine_id
               AND a.process_id = b.process_id
               AND a.activity_type = 'start'
               AND b.activity_type = 'end'
GROUP BY a.machine_id;
```

##### Step-by-Step Explanation

1. Self-join: match start and end for same machine and process.
2. `b.timestamp - a.timestamp` is process duration.
3. `AVG` and `GROUP BY machine_id` yield average per machine.
4. `ROUND(..., 3)` formats the result.

##### Common Pitfalls

- Joining only on machine_id (must also match process_id).
- Subtracting timestamps in wrong order.

##### Interview Tricks

- "Start and end" pairs → self-join with different filters for each activity type.

---

### JOINs (11–20)

---

#### Problem 11 – Combine Two Tables (LeetCode 175)

- **Pattern(s):** LEFT JOIN
- **Recognize by these keywords:**
  - "combine", "address"
  - "person may not have address"
  - "all persons"

- **Typical schema (simplified):**

```text
Table: Person (personId, firstName, lastName)
Table: Address (addressId, personId, city, state)
```

- **Goal in plain English:** For each person, return firstName, lastName, city, state. Keep all persons; address can be NULL.

##### SQL Solution

```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

##### Step-by-Step Explanation

1. `LEFT JOIN` keeps all persons.
2. Missing address → NULL for city, state.
3. Select requested columns.

##### Common Pitfalls

- Using `INNER JOIN` drops persons without an address.

##### Interview Tricks

- "All from A, optional B" → `LEFT JOIN`. Same as Problem 6.

---

#### Problem 12 – Duplicate Emails (LeetCode 182)

- **Pattern(s):** Aggregation + GROUP BY + HAVING
- **Recognize by these keywords:**
  - "duplicate", "more than once"
  - "appears twice"

- **Typical schema (simplified):**

```text
Table: Person
Columns:
  - id (PK)
  - email
```

- **Goal in plain English:** Return emails that appear more than once.

##### SQL Solution

```sql
SELECT email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

##### Step-by-Step Explanation

1. `GROUP BY email` groups rows by email.
2. `HAVING COUNT(*) > 1` keeps only groups with 2+ rows.
3. Return those emails.

##### Common Pitfalls

- Using `WHERE COUNT(*) > 1` (invalid; `COUNT` in `HAVING`).

##### Interview Tricks

- "Duplicate" / "more than once" → `GROUP BY col HAVING COUNT(*) > 1`.

---

#### Problem 13 – Customers Who Never Order (LeetCode 183)

- **Pattern(s):** Anti-join (LEFT JOIN + IS NULL or NOT IN)
- **Recognize by these keywords:**
  - "never order"
  - "customers"
  - "no orders"

- **Typical schema (simplified):**

```text
Table: Customers (id, name)
Table: Orders (id, customerId)
```

- **Goal in plain English:** Return customers who have no orders.

##### SQL Solution

```sql
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.id IS NULL;
```

##### Step-by-Step Explanation

1. `LEFT JOIN` keeps all customers.
2. Customers with no orders get NULL for `o.id`.
3. `WHERE o.id IS NULL` keeps only those.

##### Common Pitfalls

- `NOT IN` with NULL in subquery yields no rows when subquery returns NULL.

##### Interview Tricks

- "Never" / "did not" → anti-join: `LEFT JOIN` + `WHERE right.id IS NULL`.
- Safer alternative: `NOT EXISTS (SELECT 1 FROM Orders WHERE customerId = c.id)`.

---

#### Problem 14 – Employees Earning More Than Their Managers (LeetCode 181)

- **Pattern(s):** Self-join
- **Recognize by these keywords:**
  - "earn more than their manager"
  - "manager", "employee"
  - "compare salary"

- **Typical schema (simplified):**

```text
Table: Employee
Columns:
  - id (PK)
  - name
  - salary
  - managerId (FK → Employee.id)
```

- **Goal in plain English:** Return employees whose salary is greater than their manager's salary.

##### SQL Solution

```sql
SELECT e1.name AS Employee
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary;
```

##### Step-by-Step Explanation

1. `e1` = employee, `e2` = manager.
2. Join on `e1.managerId = e2.id`.
3. Filter `e1.salary > e2.salary`.

##### Common Pitfalls

- Swapping e1 and e2 roles or join condition.
- Using LEFT JOIN when every employee has a manager (INNER is correct).

##### Interview Tricks

- "Compare row with another row in same table" → self-join.
- "Employee vs manager" → join on `employee.managerId = manager.id`.

---

#### Problem 15 – Department Highest Salary (LeetCode 184)

- **Pattern(s):** Subquery or window function (MAX per group)
- **Recognize by these keywords:**
  - "highest salary", "each department"
  - "per group"

- **Typical schema (simplified):**

```text
Table: Employee (id, name, salary, departmentId)
Table: Department (id, name)
```

- **Goal in plain English:** For each department, return employees who have the highest salary in that department.

##### SQL Solution

```sql
SELECT d.name AS Department, e.name AS Employee, e.salary
FROM Employee e
JOIN Department d ON e.departmentId = d.id
WHERE (e.departmentId, e.salary) IN (
    SELECT departmentId, MAX(salary)
    FROM Employee
    GROUP BY departmentId
);
```

##### Step-by-Step Explanation

1. Subquery: max salary per department.
2. Main query: keep employees whose (departmentId, salary) matches.
3. Join Department for department name.

##### Common Pitfalls

- Ties: multiple employees can have the same max salary; both should be returned (this solution handles that).

##### Interview Tricks

- "Highest per group" → `(group_col, MAX(metric))` subquery + `IN`.
- Alternative: `RANK() OVER (PARTITION BY dept ORDER BY salary DESC) = 1`.

---

#### Problem 16 – Department Top Three Salaries (LeetCode 185)

- **Pattern(s):** Window function (DENSE_RANK) + JOIN
- **Recognize by these keywords:**
  - "top three", "each department"
  - "highest salaries"

- **Typical schema (simplified):**

```text
Table: Employee (id, name, salary, departmentId)
Table: Department (id, name)
```

- **Goal in plain English:** For each department, return employees with top 3 salaries (include ties).

##### SQL Solution

```sql
WITH Ranked AS (
    SELECT d.name AS Department, e.name AS Employee, e.salary,
           DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) AS rn
    FROM Employee e
    JOIN Department d ON e.departmentId = d.id
)
SELECT Department, Employee, salary AS Salary
FROM Ranked
WHERE rn <= 3;
```

##### Step-by-Step Explanation

1. `DENSE_RANK()` assigns 1, 2, 3, … per department by salary (ties get same rank, no gap).
2. Filter `rn <= 3` for top 3.
3. Join Department for name.

##### Common Pitfalls

- `RANK` skips ranks after ties (e.g., 1, 2, 2, 4). Use `DENSE_RANK` for "top 3" including ties.
- `ROW_NUMBER` forces unique ranks; ties get different numbers (use only if ties must be broken).

##### Interview Tricks

- "Top N per group" → `DENSE_RANK() OVER (PARTITION BY group ORDER BY metric DESC)` then `rn <= N`.
- Ties matter → DENSE_RANK. Ties break arbitrarily → ROW_NUMBER.

---

#### Problem 17 – Second Highest Salary (LeetCode 176)

- **Pattern(s):** Subquery with ORDER BY + LIMIT OFFSET (or DENSE_RANK)
- **Recognize by these keywords:**
  - "second highest"
  - "salary"
  - "NULL if not found"

- **Typical schema (simplified):**

```text
Table: Employee
Columns:
  - id (PK)
  - salary
```

- **Goal in plain English:** Return the second highest salary, or NULL if there is none.

##### SQL Solution

```sql
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

##### Step-by-Step Explanation

1. Subquery: order by salary DESC, skip 1, take 1 → second row.
2. `DISTINCT` removes duplicate top salaries so second is correct.
3. Wrapping in `SELECT (...)` returns NULL when subquery is empty.

##### Common Pitfalls

- Forgetting `DISTINCT` when top salary repeats (then "second" would still be top).
- Not handling empty result; outer `SELECT` wrapper yields NULL.

##### Interview Tricks

- "Nth highest" → `ORDER BY col DESC LIMIT 1 OFFSET N-1`.
- Or `DENSE_RANK() OVER (ORDER BY salary DESC) = N` and take one row.

---

#### Problem 18 – Nth Highest Salary (LeetCode 177)

- **Pattern(s):** Same as 17, but parameterized N (function/procedure)
- **Recognize by these keywords:**
  - "Nth highest"
  - "create function"

##### SQL Solution (MySQL)

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  DECLARE M INT;
  SET M = N - 1;
  RETURN (
      SELECT DISTINCT salary
      FROM Employee
      ORDER BY salary DESC
      LIMIT 1 OFFSET M
  );
END
```

##### Step-by-Step Explanation

1. `OFFSET` needs a constant in some DBs; use variable `M = N - 1`.
2. Same logic as second highest: `LIMIT 1 OFFSET M`.

##### Common Pitfalls

- MySQL: `LIMIT/OFFSET` with expressions may not work; use a variable.

##### Interview Tricks

- "Nth" → generalize second-highest pattern with `OFFSET N-1`.

---

#### Problem 19 – Rank Scores (LeetCode 178)

- **Pattern(s):** Window function (DENSE_RANK)
- **Recognize by these keywords:**
  - "rank"
  - "same score same rank"
  - "no gaps"

- **Typical schema (simplified):**

```text
Table: Scores
Columns:
  - id (PK)
  - score
```

- **Goal in plain English:** Return scores with their rank. Same score = same rank; next rank has no gap.

##### SQL Solution

```sql
SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM Scores
ORDER BY score DESC;
```

##### Step-by-Step Explanation

1. `DENSE_RANK() OVER (ORDER BY score DESC)` assigns 1, 2, 3… with ties getting same rank and no gaps.
2. Order result by score DESC.

##### Common Pitfalls

- `RANK` leaves gaps after ties. Use `DENSE_RANK` for "no gaps".
- `ORDER BY` in window and outer query should match for consistent presentation.

##### Interview Tricks

- "Rank with no gaps" → `DENSE_RANK`. "Rank with gaps" → `RANK`.

---

#### Problem 20 – Consecutive Numbers (LeetCode 180)

- **Pattern(s):** Window function (LAG) or self-join
- **Recognize by these keywords:**
  - "consecutive"
  - "at least 3"
  - "same value"

- **Typical schema (simplified):**

```text
Table: Logs
Columns:
  - id (PK)
  - num
```

- **Goal in plain English:** Return numbers that appear at least 3 times consecutively (by id).

##### SQL Solution (LAG)

```sql
SELECT DISTINCT num AS ConsecutiveNums
FROM (
    SELECT num,
           LAG(num, 1) OVER (ORDER BY id) AS prev1,
           LAG(num, 2) OVER (ORDER BY id) AS prev2
    FROM Logs
) t
WHERE num = prev1 AND num = prev2;
```

##### Step-by-Step Explanation

1. `LAG(num, 1)` and `LAG(num, 2)` get the previous 1 and 2 rows by id.
2. When `num = prev1 = prev2`, we have three consecutive same values.
3. `DISTINCT` avoids duplicate sequences.

##### Common Pitfalls

- Assuming consecutive ids; use `ORDER BY id` in `LAG`.
- Forgetting `DISTINCT` when the same num appears in multiple sequences.

##### Interview Tricks

- "N consecutive" → `LAG(col, 1)…LAG(col, N-1)` and check all equal.
- Alternative: self-join N times on `id = id+1, id+2, …`.

---

### Aggregation & GROUP BY (21–30)

---

#### Problem 21 – Find Customer Referee (Duplicate Pattern – 584)

*(See Problem 2)*

---

#### Problem 22 – Actors and Directors Who Cooperated At Least Three Times (LeetCode 1050)

- **Pattern(s):** GROUP BY + HAVING
- **Recognize by these keywords:**
  - "at least three times"
  - "cooperated"
  - "actor and director pair"

- **Typical schema (simplified):**

```text
Table: ActorDirector
Columns:
  - actor_id
  - director_id
  - timestamp
```

- **Goal in plain English:** Return (actor_id, director_id) pairs that cooperated at least 3 times.

##### SQL Solution

```sql
SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3;
```

##### Step-by-Step Explanation

1. `GROUP BY actor_id, director_id` groups by pair.
2. `HAVING COUNT(*) >= 3` keeps pairs with 3+ rows.

##### Common Pitfalls

- Grouping by only one column and losing the pair.

##### Interview Tricks

- "At least N times" → `GROUP BY` + `HAVING COUNT(*) >= N`.

---

#### Problem 23 – Bank Account Summary II (LeetCode 1587)

- **Pattern(s):** JOIN + GROUP BY + HAVING
- **Recognize by these keywords:**
  - "balance"
  - "above 10000"
  - "sum of transactions"

- **Typical schema (simplified):**

```text
Table: Users (account, name)
Table: Transactions (trans_id, account, amount, type)
```

- **Goal in plain English:** Return users whose balance (sum of transaction amounts, accounting for type) exceeds 10000.

##### SQL Solution

```sql
SELECT u.name, SUM(t.amount) AS balance
FROM Users u
JOIN Transactions t ON u.account = t.account
GROUP BY u.account, u.name
HAVING balance > 10000;
```

*Note: Adjust for deposit/withdrawal logic; some schemas use type and sign of amount.*

##### Step-by-Step Explanation

1. Join Users and Transactions.
2. `SUM(amount)` per account (or `SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END)`).
3. Filter with `HAVING balance > 10000`.

##### Common Pitfalls

- Omitting `GROUP BY` columns that appear in SELECT.
- Misinterpreting transaction types (deposit vs withdrawal).

##### Interview Tricks

- "Balance" / "above threshold" → `SUM` + `GROUP BY` + `HAVING`.

---

#### Problem 24 – Customers Who Bought All Products (LeetCode 1045)

- **Pattern(s):** GROUP BY + HAVING (compare COUNT DISTINCT to total)
- **Recognize by these keywords:**
  - "bought all products"
  - "every product"

- **Typical schema (simplified):**

```text
Table: Customer (customer_id, product_key)
Table: Product (product_key)
```

- **Goal in plain English:** Return customers who bought every product.

##### SQL Solution

```sql
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);
```

##### Step-by-Step Explanation

1. Count distinct products per customer.
2. Compare to total product count.
3. Keep only customers whose count equals total.

##### Common Pitfalls

- Using `COUNT(*)` instead of `COUNT(DISTINCT product_key)` when a customer can buy the same product multiple times.

##### Interview Tricks

- "Bought all" / "every product" → `COUNT(DISTINCT product) = (SELECT COUNT(*) FROM Product)`.

---

#### Problem 25 – Friend Requests II: Who Has the Most Friends (LeetCode 602)

- **Pattern(s):** UNION ALL + GROUP BY + ORDER BY + LIMIT
- **Recognize by these keywords:**
  - "most friends"
  - "requesters and accepters"
  - "both sides"

- **Typical schema (simplified):**

```text
Table: RequestAccepted
Columns:
  - requester_id
  - accepter_id
  - accept_date
```

- **Goal in plain English:** Return the person (or people) with the most friends. A friend is either requester or accepter.

##### SQL Solution

```sql
SELECT id, COUNT(*) AS num
FROM (
    SELECT requester_id AS id FROM RequestAccepted
    UNION ALL
    SELECT accepter_id AS id FROM RequestAccepted
) t
GROUP BY id
ORDER BY num DESC
LIMIT 1;
```

##### Step-by-Step Explanation

1. `UNION ALL` stacks requester_id and accepter_id (each person counted for each friendship).
2. `GROUP BY id` and `COUNT(*)` = friend count.
3. `ORDER BY num DESC LIMIT 1` returns the top.

##### Common Pitfalls

- Using `UNION` (distinct) would undercount if same pair appears multiple times.
- For ties, use `ORDER BY num DESC` and consider `LIMIT` or a tie-breaking rule.

##### Interview Tricks

- "Count from both columns" → `UNION ALL` then `GROUP BY` + `COUNT`.

---

#### Problem 26 – Customer Placing the Largest Number of Orders (LeetCode 586)

- **Pattern(s):** GROUP BY + ORDER BY + LIMIT
- **Recognize by these keywords:**
  - "largest number of orders"
  - "most orders"

- **Typical schema (simplified):**

```text
Table: Orders
Columns:
  - order_number (PK)
  - customer_number
```

- **Goal in plain English:** Return the customer_number with the most orders.

##### SQL Solution

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

##### Step-by-Step Explanation

1. Group by customer.
2. Order by count descending.
3. Take first row.

##### Common Pitfalls

- Ties: clarify whether one or all top customers are required.

##### Interview Tricks

- "Most" / "largest count" → `GROUP BY` + `ORDER BY COUNT(*) DESC LIMIT 1`.

---

#### Problem 27 – Confirmation Rate (LeetCode 1934)

- **Pattern(s):** LEFT JOIN + CASE + aggregation (rate)
- **Recognize by these keywords:**
  - "confirmation rate"
  - "confirmed" / "timeout"
  - "per user"

- **Typical schema (simplified):**

```text
Table: Signups (user_id, time_stamp)
Table: Confirmations (user_id, time_stamp, action 'confirmed'|'timeout')
```

- **Goal in plain English:** For each user, return confirmation rate = confirmed / total requests. 0 if no requests.

##### SQL Solution

```sql
SELECT s.user_id,
       ROUND(IFNULL(SUM(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END) / COUNT(c.user_id), 0), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id;
```

##### Step-by-Step Explanation

1. `LEFT JOIN` keeps all signups.
2. `CASE WHEN action = 'confirmed' THEN 1 ELSE 0 END` counts confirmed.
3. `SUM(...) / COUNT(c.user_id)` = rate (COUNT excludes NULL from non-matching join).
4. `IFNULL(..., 0)` for users with no confirmations.
5. `ROUND(..., 2)` for output format.

##### Common Pitfalls

- Division by zero when user has no confirmations.
- Using `COUNT(*)` in denominator instead of `COUNT(c.user_id)`.

##### Interview Tricks

- "Rate" = numerator / denominator; handle zero with `IFNULL` or `NULLIF`.
- "Per user" → `GROUP BY user_id`.

---

#### Problem 28 – Biggest Single Number (LeetCode 619)

- **Pattern(s):** Subquery + GROUP BY + HAVING + MAX
- **Recognize by these keywords:**
  - "single number"
  - "appears once"
  - "biggest"

- **Typical schema (simplified):**

```text
Table: MyNumbers
Columns:
  - num
```

- **Goal in plain English:** Return the largest number that appears exactly once, or NULL.

##### SQL Solution

```sql
SELECT MAX(num) AS num
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) t;
```

##### Step-by-Step Explanation

1. Subquery: numbers with `COUNT(*) = 1`.
2. `MAX(num)` gets largest; NULL if subquery empty.

##### Common Pitfalls

- Returning multiple rows when only one (or NULL) is expected; MAX handles that.

##### Interview Tricks

- "Appears once" → `GROUP BY num HAVING COUNT(*) = 1`.
- "Largest such" → wrap in `SELECT MAX(...)`.

---

#### Problem 29 – Game Play Analysis III (LeetCode 534)

- **Pattern(s):** Window function (running sum)
- **Recognize by these keywords:**
  - "games played so far"
  - "running total"
  - "cumulative"

- **Typical schema (simplified):**

```text
Table: Activity
Columns:
  - player_id
  - device_id
  - event_date
  - games_played
```

- **Goal in plain English:** For each row, return running total of games_played per player up to that date.

##### SQL Solution

```sql
SELECT player_id, event_date,
       SUM(games_played) OVER (PARTITION BY player_id ORDER BY event_date) AS games_played_so_far
FROM Activity;
```

##### Step-by-Step Explanation

1. `PARTITION BY player_id` resets per player.
2. `ORDER BY event_date` defines order.
3. Default frame: `ROWS UNBOUNDED PRECEDING` → running sum from first row to current.

##### Common Pitfalls

- Missing `PARTITION BY` would compute one global running sum.

##### Interview Tricks

- "Running total" / "so far" → `SUM() OVER (PARTITION BY ... ORDER BY ...)`.

---

#### Problem 30 – Restaurant Growth (LeetCode 1321)

- **Pattern(s):** Window function with frame (moving average/sum)
- **Recognize by these keywords:**
  - "7 days"
  - "moving average"
  - "average amount"

- **Typical schema (simplified):**

```text
Table: Customer
Columns:
  - customer_id
  - name
  - visited_on
  - amount
```

- **Goal in plain English:** For each day (from day 7 onward), return 7-day sum and average of amount.

##### SQL Solution

```sql
SELECT visited_on,
       SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
       ROUND(AVG(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount
FROM (
    SELECT visited_on, SUM(amount) AS amount
    FROM Customer
    GROUP BY visited_on
) t
ORDER BY visited_on
LIMIT 999 OFFSET 6;
```

##### Step-by-Step Explanation

1. Aggregate amount per day (if multiple rows per day).
2. `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` = 7-day window.
3. `OFFSET 6` skips first 6 days (incomplete windows).

##### Common Pitfalls

- Using `RANGE` vs `ROWS`: `ROWS` counts 7 rows; `RANGE` can span more days if there are gaps.

##### Interview Tricks

- "Last N rows" → `ROWS BETWEEN N-1 PRECEDING AND CURRENT ROW`.
- "From day N onward" → `OFFSET N-1` or filter in outer query.

---

### Window Functions & Ranking (31–40)

*Problems 31–34 and 36–37 covered above (Second Highest, Nth Highest, Rank Scores, Department Highest/Top 3, Consecutive Numbers, etc.).*

#### Problem 35 – Delete Duplicate Emails (LeetCode 196)

- **Pattern(s):** DELETE with self-join or subquery
- **Recognize by these keywords:**
  - "delete"
  - "duplicate"
  - "keep one"

- **Typical schema (simplified):**

```text
Table: Person
Columns:
  - id (PK)
  - email
```

- **Goal in plain English:** Delete duplicate emails, keeping the row with the smallest id.

##### SQL Solution

```sql
DELETE p1 FROM Person p1
JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id;
```

##### Step-by-Step Explanation

1. Self-join: p1 and p2 same email, p1.id > p2.id.
2. Delete p1 (keep p2 = smaller id).

##### Common Pitfalls

- Deleting from same table in subquery: some DBs disallow; self-join DELETE is safer.
- Deleting both rows of a duplicate pair; join ensures we keep the smaller id.

##### Interview Tricks

- "Keep smallest id" → delete where `id > min_id` for that email.
- MySQL: `DELETE t1 FROM t1 JOIN t2 ON ...` deletes from t1.

---

#### Problem 36 – Game Play Analysis II (LeetCode 512)

- **Pattern(s):** Window function (ROW_NUMBER for first row per group)
- **Recognize by these keywords:**
  - "first login"
  - "device"

- **Typical schema (simplified):**

```text
Table: Activity
Columns:
  - player_id
  - device_id
  - event_date
  - games_played
```

- **Goal in plain English:** For each player, return the device_id used on their first login date.

##### SQL Solution

```sql
SELECT player_id, device_id
FROM (
    SELECT player_id, device_id,
           ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date) AS rn
    FROM Activity
) t
WHERE rn = 1;
```

##### Step-by-Step Explanation

1. `ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date)` assigns 1 to first date.
2. Filter `rn = 1`.

##### Common Pitfalls

- Multiple rows on first date: ROW_NUMBER picks one (add tiebreaker in ORDER BY if needed).

##### Interview Tricks

- "First" / "earliest" per group → `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY date)` then `rn = 1`.

---

#### Problem 37 – Game Play Analysis IV (LeetCode 550)

- **Pattern(s):** Subquery + JOIN (first day + next day)
- **Recognize by these keywords:**
  - "first day"
  - "logged in again"
  - "fraction"

- **Typical schema (simplified):**

```text
Table: Activity
Columns:
  - player_id
  - device_id
  - event_date
  - games_played
```

- **Goal in plain English:** Return fraction of players who logged in on the day after their first login.

##### SQL Solution

```sql
SELECT ROUND(
    COUNT(DISTINCT a1.player_id) * 1.0 / (SELECT COUNT(DISTINCT player_id) FROM Activity),
    2
) AS fraction
FROM Activity a1
JOIN (
    SELECT player_id, MIN(event_date) AS first_date
    FROM Activity
    GROUP BY player_id
) a2 ON a1.player_id = a2.player_id
    AND DATEDIFF(a1.event_date, a2.first_date) = 1;
```

##### Step-by-Step Explanation

1. Subquery: first login date per player.
2. Join Activity where event_date = first_date + 1.
3. Count distinct such players.
4. Divide by total distinct players.
5. `* 1.0` for float division; `ROUND(..., 2)` for format.

##### Common Pitfalls

- Integer division truncating to 0.
- Counting players who logged in on first_date+1 more than once (use DISTINCT).

##### Interview Tricks

- "Fraction" → count / total; ensure float division.
- "Day after first" → MIN(date) + join on date + 1.

---

#### Problem 38 – Trips and Users (LeetCode 262)

- **Pattern(s):** JOIN + date filter + rate calculation + GROUP BY
- **Recognize by these keywords:**
  - "cancellation rate"
  - "banned"
  - "between dates"

- **Typical schema (simplified):**

```text
Table: Trips (id, client_id, driver_id, city_id, status, request_at)
Table: Users (users_id, banned, role)
```

- **Goal in plain English:** For each day in range, return cancellation rate (excluding banned users/drivers).

##### SQL Solution

```sql
SELECT request_at AS Day,
       ROUND(
           SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
           2
       ) AS 'Cancellation Rate'
FROM Trips t
JOIN Users u1 ON t.client_id = u1.users_id AND u1.role = 'client'
JOIN Users u2 ON t.driver_id = u2.users_id AND u2.role = 'driver'
WHERE u1.banned = 'No' AND u2.banned = 'No'
  AND request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY request_at;
```

##### Step-by-Step Explanation

1. Join Trips to Users for client and driver.
2. Filter banned = 'No' and date range.
3. Group by request_at.
4. Cancellation rate = non-completed / total per day.

##### Common Pitfalls

- Excluding banned users/drivers incorrectly.
- Integer division; use `* 1.0` or `CAST`.

##### Interview Tricks

- "Rate" with filters → filter first, then compute rate in SELECT with GROUP BY.

---

#### Problem 39 – Human Traffic of Stadium (LeetCode 601)

- **Pattern(s):** Consecutive rows (LAG/LEAD or self-join)
- **Recognize by these keywords:**
  - "consecutive"
  - "at least 3"
  - "100 or more"

- **Typical schema (simplified):**

```text
Table: Stadium
Columns:
  - id (PK)
  - visit_date
  - people
```

- **Goal in plain English:** Return rows that are part of a sequence of at least 3 consecutive rows with people >= 100.

##### SQL Solution (self-join)

```sql
SELECT DISTINCT a.id, a.visit_date, a.people
FROM Stadium a
JOIN Stadium b ON a.id = b.id - 1 AND b.people >= 100
JOIN Stadium c ON a.id = c.id - 2 AND c.people >= 100
WHERE a.people >= 100
ORDER BY a.id;
```

##### Step-by-Step Explanation

1. Self-join: a, b (id-1), c (id-2).
2. All three must have people >= 100.
3. Any of a, b, c can be the "start" of a 3-row sequence; join ensures we capture all rows in such sequences.
4. DISTINCT removes duplicates from overlapping sequences.

##### Common Pitfalls

- Assuming consecutive ids; problem defines "consecutive" by id.
- Missing rows at boundaries of sequences.

##### Interview Tricks

- "3 consecutive" → self-join 3 rows on id, id-1, id-2 (or use LAG twice).

---

#### Problem 40 – Product Price at a Given Date (LeetCode 1164)

- **Pattern(s):** Subquery for latest change before date + LEFT JOIN
- **Recognize by these keywords:**
  - "at a given date"
  - "change"
  - "default 10"

- **Typical schema (simplified):**

```text
Table: Products
Columns:
  - product_id
  - new_price
  - change_date
```

- **Goal in plain English:** For each product, return price as of given date (latest change on or before that date; 10 if none).

##### SQL Solution

```sql
SELECT DISTINCT p.product_id,
       IFNULL(t.new_price, 10) AS price
FROM (SELECT DISTINCT product_id FROM Products) p
LEFT JOIN (
    SELECT product_id, new_price
    FROM Products
    WHERE (product_id, change_date) IN (
        SELECT product_id, MAX(change_date)
        FROM Products
        WHERE change_date <= '2019-08-16'
        GROUP BY product_id
    )
) t ON p.product_id = t.product_id;
```

##### Step-by-Step Explanation

1. Subquery: (product_id, max change_date) where change_date <= given date.
2. Join to get new_price.
3. Products with no change before date get NULL → `IFNULL(..., 10)`.

##### Common Pitfalls

- Products that never had a change before the date (use full product list and LEFT JOIN).
- Using `change_date = given date` instead of "on or before".

##### Interview Tricks

- "As of date" → max date <= given date per entity, then join to get value.

---

### Advanced (41–50)

---

#### Problem 41 – Sales Analysis III (LeetCode 1084)

- **Pattern(s):** Subquery with NOT IN (exclusion)
- **Recognize by these keywords:**
  - "only", "exclusively"
  - "first quarter"
  - "not sold in"

- **Typical schema (simplified):**

```text
Table: Product (product_id, product_name)
Table: Sales (sale_id, product_id, year, quantity, price)
```

- **Goal in plain English:** Return products sold only in Q1 2019 (not in any other quarter).

##### SQL Solution

```sql
SELECT p.product_id, p.product_name
FROM Product p
WHERE p.product_id IN (
    SELECT product_id FROM Sales
    WHERE sale_date BETWEEN '2019-01-01' AND '2019-03-31'
)
AND p.product_id NOT IN (
    SELECT product_id FROM Sales
    WHERE sale_date NOT BETWEEN '2019-01-01' AND '2019-03-31'
);
```

##### Step-by-Step Explanation

1. Products sold in Q1: `IN` subquery.
2. Products sold outside Q1: `NOT IN` subquery.
3. Combine: in Q1 AND not outside Q1 = only Q1.

##### Common Pitfalls

- `NOT IN` with NULL in subquery returns no rows; ensure subquery has no NULLs.

##### Interview Tricks

- "Only in X" → `IN (X)` AND `NOT IN (non-X)`.

---

#### Problem 42 – User Activity for the Past 30 Days I (LeetCode 1141)

- **Pattern(s):** Date filter + GROUP BY + COUNT DISTINCT
- **Recognize by these keywords:**
  - "past 30 days"
  - "daily"
  - "active users"

- **Typical schema (simplified):**

```text
Table: Activity
Columns:
  - user_id
  - session_id
  - activity_date
  - activity_type
```

- **Goal in plain English:** For each day in the past 30 days, return count of distinct active users.

##### SQL Solution

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date;
```

##### Step-by-Step Explanation

1. Filter date range (30-day window).
2. `GROUP BY activity_date`.
3. `COUNT(DISTINCT user_id)` per day.

##### Common Pitfalls

- Off-by-one in date range; "past 30 days" usually excludes today.

##### Interview Tricks

- "Per day" → `GROUP BY date`. "Active users" → `COUNT(DISTINCT user_id)`.

---

#### Problem 43 – Daily Leads and Partners (LeetCode 1693)

- **Pattern(s):** GROUP BY + COUNT DISTINCT (multiple columns)
- **Recognize by these keywords:**
  - "daily"
  - "unique leads", "unique partners"
  - "per date and make"

##### SQL Solution

```sql
SELECT date_id, make_name,
       COUNT(DISTINCT lead_id) AS unique_leads,
       COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name;
```

##### Interview Tricks

- "Unique X per group" → `COUNT(DISTINCT x)` with `GROUP BY` group columns.

---

#### Problem 44 – Managers with at Least 5 Direct Reports (LeetCode 570)

- **Pattern(s):** Self-join + GROUP BY + HAVING
- **Recognize by these keywords:**
  - "manager"
  - "at least 5"
  - "direct reports"

##### SQL Solution

```sql
SELECT e2.name
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
GROUP BY e1.managerId, e2.name
HAVING COUNT(*) >= 5;
```

##### Interview Tricks

- "Reports to" → self-join on managerId. "At least N" → `HAVING COUNT(*) >= N`.

---

#### Problem 45 – The Number of Employees Which Report to Each Employee (LeetCode 1731)

- **Pattern(s):** Self-join + GROUP BY
- **Recognize by these keywords:**
  - "report to"
  - "each employee"
  - "count"

##### SQL Solution

```sql
SELECT e2.employee_id, e2.name, COUNT(*) AS reports_count
FROM Employee e1
JOIN Employee e2 ON e1.reports_to = e2.employee_id
GROUP BY e2.employee_id, e2.name
ORDER BY e2.employee_id;
```

---

#### Problem 46 – Primary Department for Each Employee (LeetCode 1789)

- **Pattern(s):** UNION / OR (primary_flag or single dept)
- **Recognize by these keywords:**
  - "primary department"
  - "single" vs "multiple"

##### SQL Solution

```sql
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
   OR employee_id IN (
       SELECT employee_id FROM Employee
       GROUP BY employee_id HAVING COUNT(*) = 1
   );
```

---

#### Problem 47 – Last Person to Fit in the Bus (LeetCode 1204)

- **Pattern(s):** Window function (running sum) + filter + last row
- **Recognize by these keywords:**
  - "queue"
  - "weight limit"
  - "last person"

- **Typical schema (simplified):**

```text
Table: Queue
Columns:
  - person_id
  - person_name
  - weight
  - turn
```

- **Goal in plain English:** Return the last person who can fit (cumulative weight <= 1000).

##### SQL Solution

```sql
SELECT person_name
FROM (
    SELECT person_name,
           SUM(weight) OVER (ORDER BY turn) AS running_weight
    FROM Queue
) t
WHERE running_weight <= 1000
ORDER BY turn DESC
LIMIT 1;
```

##### Interview Tricks

- "Last that fits" → running sum, filter where sum <= limit, take last row.

---

#### Problem 48 – Count Salary Categories (LeetCode 1907)

- **Pattern(s):** CASE + UNION or multiple aggregations
- **Recognize by these keywords:**
  - "Low", "Average", "High"
  - "count per category"

##### SQL Solution

```sql
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count
FROM Accounts WHERE income < 20000
UNION ALL
SELECT 'Average Salary', COUNT(*) FROM Accounts
WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'High Salary', COUNT(*) FROM Accounts WHERE income > 50000;
```

##### Interview Tricks

- "Count per bucket" → separate queries with UNION, or `CASE WHEN` + `GROUP BY`.

---

#### Problem 49 – Employees Whose Manager Left the Company (LeetCode 1978)

- **Pattern(s):** Subquery (managers who left) + filter
- **Recognize by these keywords:**
  - "manager left"
  - "salary < 30000"

##### SQL Solution

```sql
SELECT employee_id
FROM Employees
WHERE manager_id NOT IN (SELECT employee_id FROM Employees)
  AND salary < 30000
ORDER BY employee_id;
```

##### Interview Tricks

- "Manager left" = manager_id not in Employees. Handle NOT IN + NULL if needed.

---

#### Problem 50 – Movie Rating (LeetCode 1341)

- **Pattern(s):** Multiple aggregations (two different "top 1" queries) + UNION
- **Recognize by these keywords:**
  - "most movies"
  - "highest average"
  - "February 2020"

##### SQL Solution

```sql
(SELECT name AS results
 FROM Users u
 JOIN MovieRating mr ON u.user_id = mr.user_id
 WHERE mr.created_at LIKE '2020-02%'
 GROUP BY u.user_id, name
 ORDER BY COUNT(*) DESC, name
 LIMIT 1)
UNION ALL
(SELECT title AS results
 FROM Movies m
 JOIN MovieRating mr ON m.movie_id = mr.movie_id
 WHERE mr.created_at LIKE '2020-02%'
 GROUP BY m.movie_id, title
 ORDER BY AVG(rating) DESC, title
 LIMIT 1);
```

##### Interview Tricks

- "Two different top-1" → two subqueries with UNION.

---

## Summary: Pattern Quick Reference

| Keywords | Pattern | Solution |
|----------|---------|----------|
| "second highest", "Nth" | Top-N | `LIMIT 1 OFFSET N-1` or `DENSE_RANK = N` |
| "duplicate", "more than once" | Aggregation | `GROUP BY HAVING COUNT(*) > 1` |
| "never", "did not" | Anti-join | `LEFT JOIN` + `WHERE right.id IS NULL` |
| "consecutive", "in a row" | Lead/Lag | `LAG`/`LEAD` or self-join |
| "top N per group" | Window | `DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)` |
| "running total" | Window | `SUM() OVER (ORDER BY ...)` |
| "rate", "percentage" | CASE + aggregate | `SUM(CASE WHEN ... THEN 1 ELSE 0 END) / COUNT(*)` |
| "bought all" | Compare counts | `HAVING COUNT(DISTINCT x) = (SELECT COUNT(*) ...)` |
| "first" per group | Window | `ROW_NUMBER() = 1` |
| "compare with previous" | Lead/Lag | `LAG(col)` or `LEAD(col)` |

---

*End of SQL Interview Handbook*
