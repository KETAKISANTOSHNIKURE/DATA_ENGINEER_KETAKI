# SQL LeetCode Top 50 – Interview Handbook

A complete guide to the 50 most common SQL interview patterns, with solutions, pitfalls, and mental shortcuts for data engineering interviews.

---

## Table of Contents

### Introduction & Patterns
- [Introduction](#introduction)
- [Pattern Overview](#pattern-overview)

### Problems by Section
- [Basics (1–10)](#basics-110)
- [Aggregations (11–20)](#aggregations-1120)
- [JOINs (21–30)](#joins-2130)
- [Window Functions (31–40)](#window-functions-3140)
- [Advanced (41–50)](#advanced-4150)

### Recap
- [Cheat Sheet – All 50 Problems](#cheat-sheet--all-50-problems)
- [Pattern → Solution Templates](#pattern--solution-templates)

---

## Introduction

### How SQL Interview Problems Are Structured

SQL interview questions typically combine 2–3 core concepts:

- **Selection & Filtering** – `WHERE`, `AND`, `OR`, `IN`, `IS NULL`
- **Aggregation** – `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- **Grouping** – `GROUP BY`, `HAVING`
- **Joins** – `INNER JOIN`, `LEFT JOIN`, self-join, anti-join
- **Subqueries** – `IN`, `EXISTS`, `NOT EXISTS`, correlated subqueries
- **Window Functions** – `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `SUM OVER`

Most problems are solvable in 5–15 lines once you recognize the pattern. The key skill is **mapping keywords in the question to the right pattern**.

---

## Pattern Overview

| Pattern | When to Use | One-Liner |
|---------|-------------|-----------|
| **Selection & Filtering** | Simple row conditions | `WHERE col = value AND col2 > 0` |
| **Aggregation** | Summarize data | `SELECT col, COUNT(*) FROM t GROUP BY col` |
| **GROUP BY + HAVING** | Filter groups | `GROUP BY x HAVING COUNT(*) > 1` |
| **INNER JOIN** | Combine matching rows only | `FROM A JOIN B ON A.id = B.a_id` |
| **LEFT JOIN + IS NULL** | Anti-join (rows NOT in B) | `LEFT JOIN B ... WHERE B.id IS NULL` |
| **Self-Join** | Compare rows in same table | `FROM Emp e1 JOIN Emp e2 ON e1.manager_id = e2.id` |
| **Subquery IN** | Filter by derived set | `WHERE id IN (SELECT ...)` |
| **NOT EXISTS** | Rows with no match | `WHERE NOT EXISTS (SELECT 1 FROM B WHERE ...)` |
| **ROW_NUMBER** | Top 1 per group, first row | `ROW_NUMBER() OVER (PARTITION BY grp ORDER BY col)` |
| **DENSE_RANK** | Top N per group, ties same rank | `DENSE_RANK() OVER (PARTITION BY grp ORDER BY col DESC)` |
| **LAG / LEAD** | Compare with previous/next row | `LAG(col) OVER (ORDER BY date)` |
| **SUM OVER** | Running total | `SUM(amt) OVER (ORDER BY date)` |

---

## Basics (1–10)

---

### Problem 1 – Recyclable and Low Fat Products

**One-sentence summary:** Return product IDs where both low_fats and recyclable are 'Y'.

**Difficulty:** Beginner  
**Patterns:** `Selection`, `Filtering`

#### Recognize by these keywords
- "low fat", "recyclable"
- "both", "and"
- "filter products"

#### Schema & Example Data

```text
Table: Products
Columns:
  - product_id (int, PK)
  - low_fats (char 'Y'/'N')
  - recyclable (char 'Y'/'N')
```

| product_id | low_fats | recyclable |
|------------|----------|------------|
| 0 | Y | N |
| 1 | Y | Y |
| 2 | N | Y |
| 3 | Y | Y |
| 4 | N | N |

**Expected output:**

| product_id |
|------------|
| 1 |
| 3 |

#### Thought Process (Before the SQL)
1. Grouping: None – row-level filter.
2. Join/Subquery: Not needed.
3. Plan: Filter rows where `low_fats = 'Y'` AND `recyclable = 'Y'`, return `product_id`.

#### Best SQL Solution

```sql
SELECT product_id
FROM Products
WHERE low_fats = 'Y'
  AND recyclable = 'Y';
```

#### Step-by-Step Explanation
1. `FROM Products` reads the table.
2. `WHERE low_fats = 'Y' AND recyclable = 'Y'` keeps rows 1 and 3.
3. `SELECT product_id` returns 1 and 3.

#### Common Pitfalls
- Using `OR` instead of `AND`.
- Selecting extra columns.

#### Mental Tricks
- "Both" / "and" → `AND`.
- No aggregation → simple `WHERE`.

#### Variation
**Q:** Return products that are either low-fat OR recyclable?  
**A:** Change `AND` to `OR`.

---

### Problem 2 – Find Customer Referee

**One-sentence summary:** Return customers whose referee_id is NULL or not 2.

**Difficulty:** Beginner  
**Patterns:** `Selection`, `NULL Handling`

#### Recognize by these keywords
- "referee_id", "not 2"
- "exclude referee 2"
- "include NULL"

#### Schema & Example Data

```text
Table: Customer
Columns:
  - id (int, PK)
  - name (varchar)
  - referee_id (int, nullable, FK)
```

| id | name | referee_id |
|----|------|------------|
| 1 | Will | NULL |
| 2 | Jane | NULL |
| 3 | Alex | 2 |
| 4 | Bill | 1 |
| 5 | Zack | 1 |

**Expected output:**

| name |
|------|
| Will |
| Jane |
| Bill |
| Zack |

#### Thought Process (Before the SQL)
1. Grouping: None.
2. Pattern: Filter where `referee_id IS NULL OR referee_id != 2`.
3. Must handle NULL explicitly; `referee_id != 2` alone drops NULLs.

#### Best SQL Solution

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL
   OR referee_id != 2;
```

#### Step-by-Step Explanation
1. `referee_id IS NULL` includes Will, Jane.
2. `referee_id != 2` includes Bill, Zack; excludes Alex (referee 2).
3. Combined with `OR`, we get Will, Jane, Bill, Zack.

#### Common Pitfalls
- Using only `referee_id != 2` – NULL evaluates to UNKNOWN, so NULL rows are excluded.
- Confusing `!=` with `NOT IN (2)` when NULL is in subquery.

#### Mental Tricks
- "Exclude X but keep NULL" → `col IS NULL OR col != X`.

#### Variation
**Q:** Exclude both referee 1 and 2 but keep NULL?  
**A:** `WHERE referee_id IS NULL OR referee_id NOT IN (1, 2)`.

#### Wrong Answer Example

```sql
SELECT name FROM Customer WHERE referee_id != 2;  -- WRONG
```

This drops Will and Jane because `NULL != 2` is UNKNOWN (treated as FALSE).

---

### Problem 3 – Big Countries

**One-sentence summary:** Return countries where area >= 3M OR population >= 25M.

**Difficulty:** Beginner  
**Patterns:** `Selection`, `Filtering`

#### Recognize by these keywords
- "big country"
- "area OR population"
- "either condition"

#### Schema & Example Data

```text
Table: World
Columns:
  - name (varchar, PK)
  - continent (varchar)
  - area (bigint)
  - population (bigint)
  - gdp (bigint)
```

| name | continent | area | population | gdp |
|------|-----------|------|------------|-----|
| Afghanistan | Asia | 652230 | 25500100 | 20343000 |
| Albania | Europe | 28748 | 2831741 | 12960000 |
| Algeria | Africa | 2381741 | 37100000 | 188681000 |
| Andorra | Europe | 468 | 78115 | 3712000 |

**Expected output:**

| name | population | area |
|------|------------|------|
| Afghanistan | 25500100 | 652230 |
| Algeria | 37100000 | 2381741 |

#### Thought Process (Before the SQL)
1. No grouping; row-level filter.
2. Single table; no join.
3. Plan: WHERE with OR for two numeric conditions.

#### Best SQL Solution

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000
   OR population >= 25000000;
```

#### Step-by-Step Explanation
1. Filter rows where area >= 3M (Algeria) OR population >= 25M (Afghanistan, Algeria).
2. Select name, population, area for matching rows.

#### Common Pitfalls
- Using `AND` instead of `OR` (would require both; Afghanistan would be excluded).

#### Mental Tricks
- "Big if either X or Y" → `OR`.

#### Variation
**Q:** Return only countries meeting BOTH conditions?  
**A:** Change `OR` to `AND`.

---

### Problem 4 – Article Views I (Self-View)

**One-sentence summary:** Return distinct author IDs who viewed their own article.

**Difficulty:** Beginner  
**Patterns:** `Selection`, `DISTINCT`, `Self-Condition`

#### Recognize by these keywords
- "viewed their own"
- "author_id = viewer_id"
- "distinct authors"

#### Schema & Example Data

```text
Table: Views
Columns:
  - article_id (int)
  - author_id (int)
  - viewer_id (int)
  - view_date (date)
```

| article_id | author_id | viewer_id | view_date |
|------------|-----------|-----------|-----------|
| 1 | 3 | 5 | 2019-08-01 |
| 1 | 3 | 6 | 2019-08-02 |
| 2 | 7 | 7 | 2019-08-01 |
| 3 | 7 | 6 | 2019-08-02 |

**Expected output:**

| id |
|----|
| 7 |

(Author 7 viewed their own article 2; author 3 did not.)

#### Best SQL Solution

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;
```

#### Common Pitfalls
- Forgetting `DISTINCT` when an author views their article multiple times.

#### Mental Tricks
- "Their own" → same-table comparison `col1 = col2`.

---

### Problem 5 – Invalid Tweets

**One-sentence summary:** Return tweet IDs where content length > 15.

**Difficulty:** Beginner  
**Patterns:** `Selection`, `String Functions`

#### Recognize by these keywords
- "invalid"
- "content length"
- "character count"

#### Best SQL Solution

```sql
SELECT tweet_id
FROM Tweets
WHERE CHAR_LENGTH(content) > 15;
```

#### Mental Tricks
- "Invalid if too long" → `CHAR_LENGTH(col) > N`.

---

### Problem 6 – Replace Employee ID With Unique Identifier

**One-sentence summary:** For each employee, show unique_id and name; keep all employees (NULL if no unique_id).

**Difficulty:** Beginner  
**Patterns:** `LEFT JOIN`

#### Recognize by these keywords
- "replace", "unique identifier"
- "may not have"
- "keep all"

#### Schema & Example Data

```text
Table: Employees (id, name)
Table: EmployeeUNI (id, unique_id)
```

| Employees | | EmployeeUNI | |
|-----------|---|-------------|---|
| id | name | id | unique_id |
| 1 | Alice | 1 | 101 |
| 2 | Bob | 2 | 102 |
| 3 | Meir | 4 | 103 |

**Expected output:** Alice (101), Bob (102), Meir (NULL).

#### Best SQL Solution

```sql
SELECT eu.unique_id, e.name
FROM Employees e
LEFT JOIN EmployeeUNI eu ON e.id = eu.id;
```

#### Mental Tricks
- "Keep all from A, add optional B" → `LEFT JOIN`.

---

### Problem 7 – Product Sales Analysis I

**One-sentence summary:** For each sale, return product_name, year, and price.

**Difficulty:** Beginner  
**Patterns:** `INNER JOIN`

#### Best SQL Solution

```sql
SELECT p.product_name, s.year, s.price
FROM Sales s
INNER JOIN Product p ON s.product_id = p.product_id;
```

---

### Problem 8 – Customer Who Visited but Did Not Make Transactions

**One-sentence summary:** Count visits per customer that have no transaction.

**Difficulty:** Intermediate  
**Patterns:** `LEFT JOIN`, `Anti-Join`, `GROUP BY`

#### Recognize by these keywords
- "visited but did not"
- "no transactions"
- "count per customer"

#### Schema & Example Data

```text
Table: Visits (visit_id, customer_id)
Table: Transactions (transaction_id, visit_id, amount)
```

| Visits | | Transactions | |
|--------|---|--------------|---|
| visit_id | customer_id | transaction_id | visit_id |
| 1 | 23 | 2 | 5 |
| 2 | 9 | 3 | 5 |
| 3 | 30 | | |
| 4 | 54 | | |
| 5 | 96 | | |

**Expected output:** customer 23 (1 no-trans visit), customer 9 (1), customer 30 (1), etc.

#### Best SQL Solution

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

#### Thought Process
1. Need all visits; left join Transactions.
2. `WHERE t.transaction_id IS NULL` keeps only visits with no transaction.
3. Group by customer and count.

#### Mental Tricks
- "Did not", "never" → `LEFT JOIN` + `WHERE right.id IS NULL`.

---

### Problem 9 – Rising Temperature

**One-sentence summary:** Return IDs where temperature is higher than the previous day.

**Difficulty:** Intermediate  
**Patterns:** `Window Function`, `LAG`

#### Recognize by these keywords
- "rising", "higher than yesterday"
- "previous day"
- "consecutive dates"

#### Schema & Example Data

```text
Table: Weather
Columns:
  - id (int, PK)
  - recordDate (date)
  - temperature (int)
```

| id | recordDate | temperature |
|----|------------|-------------|
| 1 | 2015-01-01 | 10 |
| 2 | 2015-01-02 | 25 |
| 3 | 2015-01-03 | 20 |
| 4 | 2015-01-04 | 30 |

**Expected output:** 2 (25 > 10), 4 (30 > 20).

#### Best SQL Solution

```sql
SELECT id
FROM (
    SELECT id, recordDate, temperature,
           LAG(temperature) OVER (ORDER BY recordDate) AS prev_temp,
           LAG(recordDate) OVER (ORDER BY recordDate) AS prev_date
    FROM Weather
) t
WHERE temperature > prev_temp
  AND DATEDIFF(recordDate, prev_date) = 1;
```

#### Mental Tricks
- "Compare with previous row" → `LAG`. Use `DATEDIFF` to ensure consecutive days.

---

### Problem 10 – Average Time of Process per Machine

**One-sentence summary:** For each machine, return average (end - start) time per process.

**Difficulty:** Intermediate  
**Patterns:** `Self-Join`, `Aggregation`

#### Recognize by these keywords
- "average time", "per machine"
- "start" and "end" activities

#### Best SQL Solution

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

---

## Aggregations (11–20)

---

### Problem 11 – Duplicate Emails

**One-sentence summary:** Return emails that appear more than once.

**Difficulty:** Beginner  
**Patterns:** `Aggregation`, `GROUP BY`, `HAVING`

#### Recognize by these keywords
- "duplicate", "more than once"
- "appears twice"

#### Schema & Example Data

```text
Table: Person (id, email)
```

| id | email |
|----|-------|
| 1 | a@b.com |
| 2 | c@d.com |
| 3 | a@b.com |

**Expected output:**

| email |
|-------|
| a@b.com |

#### Best SQL Solution

```sql
SELECT email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

#### Common Pitfalls
- Using `WHERE COUNT(*) > 1` (invalid; use HAVING for aggregates).

#### Mental Tricks
- "Duplicate" / "more than once" → `GROUP BY col HAVING COUNT(*) > 1`.

---

### Problem 12 – Actors and Directors Who Cooperated At Least Three Times

**One-sentence summary:** Return (actor_id, director_id) pairs with 3+ cooperations.

**Difficulty:** Beginner  
**Patterns:** `GROUP BY`, `HAVING`

#### Best SQL Solution

```sql
SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3;
```

#### Mental Tricks
- "At least N" → `HAVING COUNT(*) >= N`.

---

### Problem 13 – Customers Who Never Order

**One-sentence summary:** Return customers who have no orders.

**Difficulty:** Beginner  
**Patterns:** `Anti-Join`, `LEFT JOIN`, `Subquery`

#### Recognize by these keywords
- "never order"
- "no orders"
- "customers"

#### Best SQL Solution

```sql
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.id IS NULL;
```

#### Mental Tricks
- "Never" → `LEFT JOIN` + `WHERE right.id IS NULL` or `NOT EXISTS`.

---

### Problem 14 – Bank Account Summary II

**One-sentence summary:** Return users whose balance exceeds 10000.

**Difficulty:** Intermediate  
**Patterns:** `JOIN`, `Aggregation`, `HAVING`

#### Best SQL Solution

```sql
SELECT u.name, SUM(t.amount) AS balance
FROM Users u
JOIN Transactions t ON u.account = t.account
GROUP BY u.account, u.name
HAVING balance > 10000;
```

*Note: Adjust SUM for deposit/withdrawal logic if schema uses type.*

---

### Problem 15 – Customers Who Bought All Products

**One-sentence summary:** Return customers who bought every product.

**Difficulty:** Intermediate  
**Patterns:** `GROUP BY`, `HAVING`, `Subquery`

#### Recognize by these keywords
- "bought all"
- "every product"

#### Best SQL Solution

```sql
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);
```

#### Mental Tricks
- "Bought all" → `COUNT(DISTINCT product) = total product count`.

---

### Problem 16 – Friend Requests II: Who Has the Most Friends

**One-sentence summary:** Return the person with the most friends (count requester + accepter).

**Difficulty:** Intermediate  
**Patterns:** `UNION ALL`, `GROUP BY`, `ORDER BY`, `LIMIT`

#### Best SQL Solution

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

#### Mental Tricks
- "Count from both columns" → `UNION ALL` then `GROUP BY` + `COUNT`.

---

### Problem 17 – Customer Placing the Largest Number of Orders

**One-sentence summary:** Return the customer with the most orders.

**Difficulty:** Beginner  
**Patterns:** `GROUP BY`, `ORDER BY`, `LIMIT`

#### Best SQL Solution

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

---

### Problem 18 – Confirmation Rate

**One-sentence summary:** For each user, return confirmation rate (confirmed / total).

**Difficulty:** Intermediate  
**Patterns:** `LEFT JOIN`, `CASE`, `Aggregation`

#### Best SQL Solution

```sql
SELECT s.user_id,
       ROUND(IFNULL(SUM(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END) / COUNT(c.user_id), 0), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id;
```

#### Common Pitfalls
- Division by zero; use `IFNULL` or `NULLIF`.
- Using `COUNT(*)` in denominator instead of `COUNT(c.user_id)` for LEFT JOIN.

---

### Problem 19 – Biggest Single Number

**One-sentence summary:** Return the largest number that appears exactly once, or NULL.

**Difficulty:** Intermediate  
**Patterns:** `Subquery`, `GROUP BY`, `HAVING`, `MAX`

#### Best SQL Solution

```sql
SELECT MAX(num) AS num
FROM (
    SELECT num FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) t;
```

#### Mental Tricks
- "Appears once" → `GROUP BY num HAVING COUNT(*) = 1`. "Largest" → wrap in `MAX()`.

---

### Problem 20 – Game Play Analysis III (Running Total)

**One-sentence summary:** For each row, return running total of games_played per player.

**Difficulty:** Intermediate  
**Patterns:** `Window Function`, `SUM OVER`

#### Best SQL Solution

```sql
SELECT player_id, event_date,
       SUM(games_played) OVER (PARTITION BY player_id ORDER BY event_date) AS games_played_so_far
FROM Activity;
```

#### Mental Tricks
- "Running total" → `SUM() OVER (PARTITION BY ... ORDER BY ...)`.

---

## JOINs (21–30)

---

### Problem 21 – Combine Two Tables

**One-sentence summary:** For each person, return name and address; keep all persons.

**Difficulty:** Beginner  
**Patterns:** `LEFT JOIN`

#### Best SQL Solution

```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

---

### Problem 22 – Employees Earning More Than Their Managers

**One-sentence summary:** Return employees whose salary exceeds their manager's salary.

**Difficulty:** Intermediate  
**Patterns:** `Self-Join`

#### Recognize by these keywords
- "earn more than manager"
- "compare with manager"

#### Schema & Example Data

```text
Table: Employee (id, name, salary, managerId)
```

| id | name | salary | managerId |
|----|------|--------|-----------|
| 1 | Joe | 70000 | 3 |
| 2 | Henry | 80000 | 4 |
| 3 | Sam | 60000 | NULL |
| 4 | Max | 90000 | NULL |

**Expected output:** Joe (70000 > 60000).

#### Best SQL Solution

```sql
SELECT e1.name AS Employee
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary;
```

#### Mental Tricks
- "Compare with another row in same table" → self-join.

---

### Problem 23 – Department Highest Salary

**One-sentence summary:** For each department, return employees with the highest salary.

**Difficulty:** Intermediate  
**Patterns:** `JOIN`, `Subquery`, `IN`

#### Best SQL Solution

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

#### Mental Tricks
- "Highest per group" → subquery `(group_col, MAX(metric))` + `IN`.

---

### Problem 24 – Department Top Three Salaries

**One-sentence summary:** For each department, return employees with top 3 salaries (include ties).

**Difficulty:** Advanced  
**Patterns:** `Window Function`, `DENSE_RANK`, `JOIN`

#### Best SQL Solution

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

#### Common Pitfalls
- Using `RANK` (gaps after ties) instead of `DENSE_RANK`.
- Using `ROW_NUMBER` when ties should get same rank.

#### Mental Tricks
- "Top N per group" → `DENSE_RANK() OVER (PARTITION BY group ORDER BY metric DESC)` then `rn <= N`.

---

### Problem 25 – Second Highest Salary

**One-sentence summary:** Return the second highest salary, or NULL if none.

**Difficulty:** Intermediate  
**Patterns:** `Subquery`, `ORDER BY`, `LIMIT`, `OFFSET`

#### Best SQL Solution

```sql
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

#### Mental Tricks
- "Nth highest" → `ORDER BY col DESC LIMIT 1 OFFSET N-1`. Wrap in `SELECT (...)` for NULL.

---

### Problem 26 – Nth Highest Salary

**One-sentence summary:** Create a function that returns the Nth highest salary.

**Difficulty:** Intermediate  
**Patterns:** `Function`, `Subquery`

#### Best SQL Solution (MySQL)

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

---

### Problem 27 – Rank Scores

**One-sentence summary:** Return scores with dense rank (same score = same rank, no gaps).

**Difficulty:** Intermediate  
**Patterns:** `Window Function`, `DENSE_RANK`

#### Best SQL Solution

```sql
SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM Scores
ORDER BY score DESC;
```

---

### Problem 28 – Consecutive Numbers

**One-sentence summary:** Return numbers that appear at least 3 times consecutively (by id).

**Difficulty:** Advanced  
**Patterns:** `Window Function`, `LAG`

#### Best SQL Solution

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

#### Mental Tricks
- "N consecutive same" → `LAG` N-1 times, check all equal.

---

### Problem 29 – Delete Duplicate Emails

**One-sentence summary:** Delete duplicate emails, keeping the row with the smallest id.

**Difficulty:** Intermediate  
**Patterns:** `DELETE`, `Self-Join`

#### Best SQL Solution

```sql
DELETE p1 FROM Person p1
JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id;
```

#### Mental Tricks
- "Keep smallest id" → delete rows where `id > min_id` for that email.

---

### Problem 30 – Game Play Analysis II (First Device)

**One-sentence summary:** For each player, return the device used on first login.

**Difficulty:** Intermediate  
**Patterns:** `Window Function`, `ROW_NUMBER`

#### Best SQL Solution

```sql
SELECT player_id, device_id
FROM (
    SELECT player_id, device_id,
           ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date) AS rn
    FROM Activity
) t
WHERE rn = 1;
```

#### Mental Tricks
- "First per group" → `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY date)` then `rn = 1`.

---

## Window Functions (31–40)

---

### Problem 31 – Game Play Analysis IV (Day-After-First Login)

**One-sentence summary:** Return fraction of players who logged in on the day after their first login.

**Difficulty:** Advanced  
**Patterns:** `Subquery`, `JOIN`, `Aggregation`

#### Best SQL Solution

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

#### Mental Tricks
- "Day after first" → `MIN(date)` + join on `date = first_date + 1`.

---

### Problem 32 – Restaurant Growth (7-Day Moving Average)

**One-sentence summary:** For each day (from day 7), return 7-day sum and average.

**Difficulty:** Advanced  
**Patterns:** `Window Function`, `Frame`

#### Best SQL Solution

```sql
SELECT visited_on,
       SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
       ROUND(AVG(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount
FROM (SELECT visited_on, SUM(amount) AS amount FROM Customer GROUP BY visited_on) t
ORDER BY visited_on
LIMIT 999 OFFSET 6;
```

#### Mental Tricks
- "Last N rows" → `ROWS BETWEEN N-1 PRECEDING AND CURRENT ROW`.

---

### Problem 33 – Trips and Users (Cancellation Rate)

**One-sentence summary:** Per day, return cancellation rate (excluding banned users/drivers).

**Difficulty:** Advanced  
**Patterns:** `JOIN`, `CASE`, `GROUP BY`, `Date Filter`

#### Best SQL Solution

```sql
SELECT request_at AS Day,
       ROUND(SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS 'Cancellation Rate'
FROM Trips t
JOIN Users u1 ON t.client_id = u1.users_id AND u1.role = 'client'
JOIN Users u2 ON t.driver_id = u2.users_id AND u2.role = 'driver'
WHERE u1.banned = 'No' AND u2.banned = 'No'
  AND request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY request_at;
```

---

### Problem 34 – Human Traffic of Stadium

**One-sentence summary:** Return rows in sequences of 3+ consecutive rows with people >= 100.

**Difficulty:** Advanced  
**Patterns:** `Self-Join`, `Consecutive`

#### Best SQL Solution

```sql
SELECT DISTINCT a.id, a.visit_date, a.people
FROM Stadium a
JOIN Stadium b ON a.id = b.id - 1 AND b.people >= 100
JOIN Stadium c ON a.id = c.id - 2 AND c.people >= 100
WHERE a.people >= 100
ORDER BY a.id;
```

---

### Problem 35 – Product Price at a Given Date

**One-sentence summary:** For each product, return price as of given date (default 10 if no change).

**Difficulty:** Advanced  
**Patterns:** `Subquery`, `LEFT JOIN`, `Date Logic`

#### Best SQL Solution

```sql
SELECT DISTINCT p.product_id, IFNULL(t.new_price, 10) AS price
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

#### Mental Tricks
- "As of date" → max change_date <= date per product, then join.

---

### Problem 36 – Last Person to Fit in the Bus

**One-sentence summary:** Return the last person in queue where cumulative weight <= 1000.

**Difficulty:** Advanced  
**Patterns:** `Window Function`, `Running Sum`

#### Best SQL Solution

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

---

### Problem 37 – Sales Analysis III (Only in Q1)

**One-sentence summary:** Return products sold only in Q1 2019.

**Difficulty:** Intermediate  
**Patterns:** `Subquery`, `IN`, `NOT IN`

#### Best SQL Solution

```sql
SELECT p.product_id, p.product_name
FROM Product p
WHERE p.product_id IN (SELECT product_id FROM Sales WHERE sale_date BETWEEN '2019-01-01' AND '2019-03-31')
  AND p.product_id NOT IN (SELECT product_id FROM Sales WHERE sale_date NOT BETWEEN '2019-01-01' AND '2019-03-31');
```

---

### Problem 38 – Count Salary Categories

**One-sentence summary:** Count accounts in Low (<20k), Average (20–50k), High (>50k).

**Difficulty:** Beginner  
**Patterns:** `UNION`, `CASE`

#### Best SQL Solution

```sql
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count FROM Accounts WHERE income < 20000
UNION ALL
SELECT 'Average Salary', COUNT(*) FROM Accounts WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'High Salary', COUNT(*) FROM Accounts WHERE income > 50000;
```

---

### Problem 39 – Employees Whose Manager Left

**One-sentence summary:** Return employees whose manager_id is not in Employees, with salary < 30000.

**Difficulty:** Intermediate  
**Patterns:** `Subquery`, `NOT IN`

#### Best SQL Solution

```sql
SELECT employee_id
FROM Employees
WHERE manager_id NOT IN (SELECT employee_id FROM Employees WHERE employee_id IS NOT NULL)
  AND salary < 30000
ORDER BY employee_id;
```

*Note: `IS NOT NULL` avoids NOT IN issues if subquery returns NULL.*

---

### Problem 40 – Movie Rating (Two Top-1 Queries)

**One-sentence summary:** (1) User with most ratings in Feb 2020; (2) Movie with highest avg rating in Feb 2020.

**Difficulty:** Advanced  
**Patterns:** `UNION`, `GROUP BY`, `ORDER BY`, `LIMIT`

#### Best SQL Solution

```sql
(SELECT name AS results FROM Users u
 JOIN MovieRating mr ON u.user_id = mr.user_id
 WHERE mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
 GROUP BY u.user_id, name
 ORDER BY COUNT(*) DESC, name LIMIT 1)
UNION ALL
(SELECT title AS results FROM Movies m
 JOIN MovieRating mr ON m.movie_id = mr.movie_id
 WHERE mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
 GROUP BY m.movie_id, title
 ORDER BY AVG(rating) DESC, title LIMIT 1);
```

---

## Advanced (41–50)

---

### Problem 41 – User Activity Past 30 Days

**One-sentence summary:** Per day in past 30 days, return distinct active users count.

**Difficulty:** Beginner  
**Patterns:** `Date Filter`, `GROUP BY`, `COUNT DISTINCT`

#### Best SQL Solution

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date;
```

---

### Problem 42 – Daily Leads and Partners

**One-sentence summary:** Per date and make, return unique leads and partners count.

**Difficulty:** Beginner  
**Patterns:** `GROUP BY`, `COUNT DISTINCT`

#### Best SQL Solution

```sql
SELECT date_id, make_name,
       COUNT(DISTINCT lead_id) AS unique_leads,
       COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name;
```

---

### Problem 43 – Managers with at Least 5 Direct Reports

**One-sentence summary:** Return managers with 5+ direct reports.

**Difficulty:** Intermediate  
**Patterns:** `Self-Join`, `GROUP BY`, `HAVING`

#### Best SQL Solution

```sql
SELECT e2.name
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
GROUP BY e1.managerId, e2.name
HAVING COUNT(*) >= 5;
```

---

### Problem 44 – Employees Reporting to Each Employee

**One-sentence summary:** Per manager, return report count.

**Difficulty:** Intermediate  
**Patterns:** `Self-Join`, `GROUP BY`

#### Best SQL Solution

```sql
SELECT e2.employee_id, e2.name, COUNT(*) AS reports_count
FROM Employee e1
JOIN Employee e2 ON e1.reports_to = e2.employee_id
GROUP BY e2.employee_id, e2.name
ORDER BY e2.employee_id;
```

---

### Problem 45 – Primary Department for Each Employee

**One-sentence summary:** Return department for each employee (primary_flag = Y or only dept).

**Difficulty:** Intermediate  
**Patterns:** `UNION`, `Subquery`

#### Best SQL Solution

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

### Problem 46 – Investments in 2016

**One-sentence summary:** Sum tiv_2016 where tiv_2015 is duplicated and (lat, lon) is unique.

**Difficulty:** Advanced  
**Patterns:** `Subquery`, `IN`, `Aggregation`

#### Best SQL Solution

```sql
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance
WHERE tiv_2015 IN (
    SELECT tiv_2015 FROM Insurance GROUP BY tiv_2015 HAVING COUNT(*) > 1
)
AND (lat, lon) IN (
    SELECT lat, lon FROM Insurance GROUP BY lat, lon HAVING COUNT(*) = 1
);
```

---

### Problem 47 – Fix Product Name Format

**One-sentence summary:** Normalize product name (lower, trim) and aggregate.

**Difficulty:** Beginner  
**Patterns:** `String Functions`, `GROUP BY`

#### Best SQL Solution

```sql
SELECT LOWER(TRIM(product_name)) AS product_name,
       DATE_FORMAT(sale_date, '%Y-%m') AS sale_date,
       COUNT(*) AS total
FROM Sales
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

### Problem 48 – Market Analysis I (Orders in 2019)

**One-sentence summary:** Per buyer, return count of orders in 2019.

**Difficulty:** Intermediate  
**Patterns:** `LEFT JOIN`, `Date Filter`, `GROUP BY`

#### Best SQL Solution

```sql
SELECT u.user_id AS buyer_id, u.join_date,
       IFNULL(COUNT(o.order_id), 0) AS orders_in_2019
FROM Users u
LEFT JOIN Orders o ON u.user_id = o.buyer_id AND YEAR(o.order_date) = 2019
GROUP BY u.user_id, u.join_date;
```

---

### Problem 49 – Market Analysis II (Favorite Category)

**One-sentence summary:** Per user, return favorite category (most orders) and count.

**Difficulty:** Advanced  
**Patterns:** `Window Function`, `RANK`, `JOIN`

#### Best SQL Solution

```sql
WITH Ranked AS (
    SELECT o.buyer_id, i.item_brand,
           RANK() OVER (PARTITION BY o.buyer_id ORDER BY COUNT(*) DESC, MIN(o.order_date) DESC) AS rn
    FROM Orders o
    JOIN Items i ON o.item_id = i.item_id
    GROUP BY o.buyer_id, i.item_brand
)
SELECT u.user_id AS buyer_id, u.join_date, r.item_brand AS favorite_brand
FROM Users u
LEFT JOIN Ranked r ON u.user_id = r.buyer_id AND r.rn = 1;
```

---

### Problem 50 – Percentage of Users Attended a Contest

**One-sentence summary:** Per contest, return percentage of users who attended.

**Difficulty:** Intermediate  
**Patterns:** `JOIN`, `COUNT`, `GROUP BY`, `Percentage`

#### Best SQL Solution

```sql
SELECT contest_id,
       ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM Users), 2) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id;
```

---

## Cheat Sheet – All 50 Problems

| # | Title | Difficulty | Main Patterns | Key Functions |
|---|-------|------------|---------------|---------------|
| 1 | Recyclable and Low Fat Products | Beginner | Selection | WHERE, AND |
| 2 | Find Customer Referee | Beginner | NULL | IS NULL, OR |
| 3 | Big Countries | Beginner | Filtering | OR |
| 4 | Article Views I | Beginner | DISTINCT | author_id = viewer_id |
| 5 | Invalid Tweets | Beginner | String | CHAR_LENGTH |
| 6 | Replace Employee ID | Beginner | LEFT JOIN | LEFT JOIN |
| 7 | Product Sales Analysis I | Beginner | INNER JOIN | JOIN |
| 8 | Customer Visited No Trans | Intermediate | Anti-join | LEFT JOIN, IS NULL |
| 9 | Rising Temperature | Intermediate | LAG | LAG, DATEDIFF |
| 10 | Avg Process Time | Intermediate | Self-join | Self-join, AVG |
| 11 | Duplicate Emails | Beginner | HAVING | GROUP BY, HAVING |
| 12 | Actors Directors 3+ | Beginner | HAVING | COUNT >= 3 |
| 13 | Customers Never Order | Beginner | Anti-join | LEFT JOIN, IS NULL |
| 14 | Bank Account Summary | Intermediate | SUM, HAVING | GROUP BY, HAVING |
| 15 | Bought All Products | Intermediate | HAVING | COUNT DISTINCT = total |
| 16 | Most Friends | Intermediate | UNION ALL | UNION ALL, GROUP BY |
| 17 | Largest Orders | Beginner | GROUP BY | ORDER BY COUNT, LIMIT |
| 18 | Confirmation Rate | Intermediate | CASE | SUM(CASE), ROUND |
| 19 | Biggest Single Number | Intermediate | Subquery | MAX, HAVING COUNT=1 |
| 20 | Games Played So Far | Intermediate | Window | SUM OVER |
| 21 | Combine Two Tables | Beginner | LEFT JOIN | LEFT JOIN |
| 22 | Earn More Than Manager | Intermediate | Self-join | Self-join |
| 23 | Dept Highest Salary | Intermediate | Subquery | IN (dept, MAX) |
| 24 | Dept Top 3 Salaries | Advanced | DENSE_RANK | PARTITION BY |
| 25 | Second Highest Salary | Intermediate | LIMIT OFFSET | OFFSET 1 |
| 26 | Nth Highest Salary | Intermediate | Function | LIMIT OFFSET |
| 27 | Rank Scores | Intermediate | DENSE_RANK | DENSE_RANK |
| 28 | Consecutive Numbers | Advanced | LAG | LAG(x, 1), LAG(x, 2) |
| 29 | Delete Duplicate Emails | Intermediate | DELETE | Self-join DELETE |
| 30 | First Device | Intermediate | ROW_NUMBER | rn = 1 |
| 31 | Day-After-First Login | Advanced | Subquery, JOIN | MIN, DATEDIFF |
| 32 | Restaurant Growth | Advanced | Frame | ROWS 6 PRECEDING |
| 33 | Trips and Users | Advanced | JOIN, CASE | Cancellation rate |
| 34 | Human Traffic Stadium | Advanced | Self-join | 3 consecutive |
| 35 | Price at Given Date | Advanced | Subquery | MAX(change_date) |
| 36 | Last Person in Bus | Advanced | Running sum | SUM OVER |
| 37 | Sales Analysis III | Intermediate | IN, NOT IN | Only in period |
| 38 | Count Salary Categories | Beginner | UNION | 3 buckets |
| 39 | Manager Left | Intermediate | NOT IN | Subquery |
| 40 | Movie Rating | Advanced | UNION | Two top-1 |
| 41 | User Activity 30 Days | Beginner | Date, GROUP BY | BETWEEN |
| 42 | Daily Leads Partners | Beginner | COUNT DISTINCT | GROUP BY |
| 43 | Managers 5+ Reports | Intermediate | Self-join | HAVING >= 5 |
| 44 | Reports per Employee | Intermediate | Self-join | GROUP BY |
| 45 | Primary Department | Intermediate | UNION, Subquery | primary_flag |
| 46 | Investments 2016 | Advanced | Subquery IN | Dual HAVING |
| 47 | Fix Product Name | Beginner | LOWER, TRIM | GROUP BY |
| 48 | Orders in 2019 | Intermediate | LEFT JOIN | YEAR filter |
| 49 | Favorite Category | Advanced | RANK | RANK, PARTITION |
| 50 | Contest Percentage | Intermediate | Percentage | COUNT / total |

---

## Pattern → Solution Templates

| Pattern | Template |
|---------|----------|
| **Top 1 per group** | `ROW_NUMBER() OVER (PARTITION BY grp ORDER BY col) = 1` |
| **Top N per group** | `DENSE_RANK() OVER (PARTITION BY grp ORDER BY col DESC) <= N` |
| **Nth highest** | `ORDER BY col DESC LIMIT 1 OFFSET N-1` |
| **Never did X** | `LEFT JOIN X ... WHERE x.id IS NULL` or `NOT EXISTS` |
| **Duplicate** | `GROUP BY col HAVING COUNT(*) > 1` |
| **Bought all** | `HAVING COUNT(DISTINCT product) = (SELECT COUNT(*) FROM Products)` |
| **Compare previous row** | `LAG(col) OVER (ORDER BY date)` |
| **Running total** | `SUM(col) OVER (ORDER BY date)` |
| **Consecutive N same** | `LAG` N-1 times, filter where all equal |
| **Only in period** | `IN (period)` AND `NOT IN (non-period)` |
| **Rate/Percentage** | `SUM(CASE WHEN ... THEN 1 ELSE 0 END) / COUNT(*)` with ROUND |
| **Self-join** | `FROM T a JOIN T b ON a.manager_id = b.id` |

---

*End of SQL LeetCode Top 50 Handbook*
