# Questions 31–40: Window Functions & Ranking

---

## 31. 176 – Second Highest Salary

### How to Identify
- **Keywords:** "second highest", "salary"
- **Pattern:** LIMIT OFFSET or DENSE_RANK

### Best Approach
`ORDER BY salary DESC LIMIT 1 OFFSET 1`. Wrap in subquery to return NULL when no second.

### Key Keywords & Tricks
- `ORDER BY salary DESC`
- `LIMIT 1 OFFSET 1` – skip first, take second
- `SELECT (...) AS SecondHighestSalary` – handles NULL

### Solution

```sql
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

### Explanation
Subquery returns second row after sorting by salary descending. If only one row, OFFSET 1 returns empty → NULL. DISTINCT handles duplicate top salary.

---

## 32. 177 – Nth Highest Salary

### How to Identify
- **Keywords:** "Nth highest", function
- **Pattern:** Same as 176 but parameterized N

### Best Approach
Create function with parameter N. Use `LIMIT 1 OFFSET N-1`.

### Key Keywords & Tricks
- `LIMIT 1 OFFSET N-1`
- Function parameter
- `DISTINCT` for unique salaries

### Solution

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

### Explanation
MySQL does not allow OFFSET with variable directly. Use DECLARE M = N-1. Same logic as second highest.

---

## 33. 178 – Rank Scores

### How to Identify
- **Keywords:** "rank", "no gaps" or "with gaps"
- **Pattern:** DENSE_RANK (no gaps) or RANK (with gaps)

### Best Approach
`DENSE_RANK() OVER (ORDER BY score DESC)` – same score = same rank, no gaps.

### Key Keywords & Tricks
- `DENSE_RANK() OVER (ORDER BY score DESC)`
- `RANK()` – gaps for ties
- `ROW_NUMBER()` – unique numbers

### Solution

```sql
SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM Scores;
```

### Explanation
DENSE_RANK assigns same rank to ties, next rank continues without gap. ORDER BY score DESC for highest first.

---

## 34. 184 – Department Highest Salary

### How to Identify
- **Keywords:** "highest salary", "each department"
- **Pattern:** RANK/DENSE_RANK per department or subquery with MAX

### Best Approach
`MAX(salary)` per department, then join to get (department, employee) with that salary.

### Key Keywords & Tricks
- `PARTITION BY departmentId` in window function
- Or: subquery `(departmentId, MAX(salary))` + JOIN

### Solution

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

### Explanation
Subquery finds max salary per department. Main query keeps employees whose (departmentId, salary) matches. Alternative: RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) = 1.

---

## 35. 180 – Consecutive Numbers

### How to Identify
- **Keywords:** "consecutive", "three times", "appears at least"
- **Pattern:** Self-join or LAG/LEAD

### Best Approach
Self-join: a.id = b.id-1 and b.id = c.id-1 (three consecutive). Or LAG to get prev two values.

### Key Keywords & Tricks
- Self-join on `id = id+1`
- `LAG(num, 1)` and `LAG(num, 2)` – two previous rows
- `DISTINCT` – avoid duplicate sequences

### Solution (LAG)

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

### Explanation
LAG gets previous 1 and 2 rows. If num = prev1 = prev2, we have three consecutive same values.

---

## 36. 585 – Investments in 2016

### How to Identify
- **Keywords:** "2016", "unique", "same lat/lon"
- **Pattern:** Filter + GROUP BY + HAVING for uniqueness

### Best Approach
Filter tiv_2016. Sum tiv_2015 where (lat, lon) is unique in 2015 and (lat, lon) appears in 2016.

### Solution

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

### Explanation
Sum tiv_2016 for policies where tiv_2015 is duplicated (multiple policies same value) but (lat, lon) is unique. Logic may vary per problem.

---

## 37. 185 – Department Top Three Salaries

### How to Identify
- **Keywords:** "top three", "each department"
- **Pattern:** DENSE_RANK with PARTITION BY

### Best Approach
`DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)`. Filter rn <= 3.

### Key Keywords & Tricks
- `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)`
- `WHERE rn <= 3`
- Use CTE for readability

### Solution

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

### Explanation
DENSE_RANK assigns 1,2,3 per department by salary. Top 3 salaries per department have rn <= 3.

---

## 38. 1321 – Restaurant Growth

### How to Identify
- **Keywords:** "moving average", "7 days", "amount"
- **Pattern:** Window frame – ROWS BETWEEN 6 PRECEDING AND CURRENT ROW

### Best Approach
`SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`. Filter to days with 7+ rows.

### Key Keywords & Tricks
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`
- `RANGE` for date-based window
- Need at least 7 days of data

### Solution

```sql
SELECT visited_on,
       SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
       ROUND(AVG(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount
FROM Customer
ORDER BY visited_on
LIMIT 999 OFFSET 6;
```

### Explanation
Running sum/avg over 7-day window. OFFSET 6 skips first 6 days (incomplete windows). Adjust for exact problem requirements.

---

## 39. 602 – Friend Requests II (Most Popular)

### How to Identify
- Same as Q27 – most friends via UNION ALL + GROUP BY.

### Solution

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

---

## 40. 534 – Game Play Analysis III

### How to Identify
- **Keywords:** "running total", "games played", "cumulative"
- **Pattern:** SUM() OVER (ORDER BY event_date)

### Best Approach
`SUM(games_played) OVER (PARTITION BY player_id ORDER BY event_date)`.

### Key Keywords & Tricks
- `SUM() OVER (PARTITION BY ... ORDER BY ...)`
- No frame = default RANGE UNBOUNDED PRECEDING (running total)

### Solution

```sql
SELECT player_id, event_date,
       SUM(games_played) OVER (PARTITION BY player_id ORDER BY event_date) AS games_played_so_far
FROM Activity;
```

### Explanation
Per player, order by date. Running sum of games_played gives cumulative total.

---

## Key Takeaway

**Window patterns:** RANK/DENSE_RANK/ROW_NUMBER for top-N, LAG/LEAD for previous/next row, SUM/AVG OVER (ORDER BY) for running totals, ROWS/RANGE for frame.
