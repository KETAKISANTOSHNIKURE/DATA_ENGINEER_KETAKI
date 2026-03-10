# Questions 41–50: Advanced – CTEs, Dates & Complex

---

## 41. 262 – Trips and Users

### How to Identify
- **Keywords:** "cancellation rate", "banned", "between dates"
- **Pattern:** Multiple filters + rate calculation

### Best Approach
Filter banned users. Filter date range. Compute cancellation rate = cancelled / total per (client, driver) or per day.

### Key Keywords & Tricks
- `JOIN` or subquery to exclude banned
- `CASE WHEN status LIKE 'cancelled%' THEN 1 ELSE 0 END`
- `ROUND(100.0 * cancelled / total, 2)`
- Handle zero total (return 0)

### Solution

```sql
SELECT request_at AS Day,
       ROUND(SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 'Cancellation Rate'
FROM Trips t
JOIN Users u1 ON t.client_id = u1.users_id AND u1.role = 'client'
JOIN Users u2 ON t.driver_id = u2.users_id AND u2.role = 'driver'
WHERE u1.banned = 'No' AND u2.banned = 'No'
  AND request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY request_at;
```

### Explanation
Exclude banned clients and drivers. Filter date range. Cancellation = non-completed. Rate = cancelled/total per day. Use IFNULL for zero division.

---

## 42. 601 – Human Traffic of Stadium

### How to Identify
- **Keywords:** "consecutive", "at least 3", "100 or more"
- **Pattern:** Consecutive rows – LAG/LEAD or self-join

### Best Approach
Three consecutive rows with people >= 100. Use LAG/LEAD to check prev and next, or self-join on id = id+1, id+2.

### Solution

```sql
SELECT DISTINCT a.id, a.visit_date, a.people
FROM Stadium a
JOIN Stadium b ON a.id = b.id - 1 AND b.people >= 100
JOIN Stadium c ON a.id = c.id - 2 AND c.people >= 100
WHERE a.people >= 100
ORDER BY a.id;
```

### Explanation
Self-join: a, b, c where b = a+1, c = a+2. All three must have people >= 100. DISTINCT removes duplicate sequences. Alternative: LAG(id,1), LAG(id,2) and check consecutive ids.

---

## 43. 183 – Customers Who Never Order

### How to Identify
- **Keywords:** "never order", "customers"
- **Pattern:** Anti-join – LEFT JOIN + IS NULL or NOT IN

### Best Approach
`LEFT JOIN Orders ON Customers.id = Orders.customerId` then `WHERE Orders.id IS NULL`.

### Key Keywords & Tricks
- `LEFT JOIN` + `WHERE right.id IS NULL`
- Or `WHERE id NOT IN (SELECT customerId FROM Orders)`

### Solution

```sql
SELECT name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.id IS NULL;
```

### Explanation
LEFT JOIN keeps all customers. Where no order, Orders columns are NULL. Filter those rows.

---

## 44. 196 – Delete Duplicate Emails

### How to Identify
- **Keywords:** "delete", "duplicate", "keep one"
- **Pattern:** DELETE with subquery – keep min id per email

### Best Approach
Delete rows where (id, email) not in (SELECT MIN(id), email FROM Person GROUP BY email).

### Key Keywords & Tricks
- `DELETE FROM table WHERE ...`
- Keep MIN(id) or MAX(id) per email
- MySQL: delete from same table in subquery – use alias

### Solution

```sql
DELETE p1 FROM Person p1
JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id;
```

### Explanation
Self-join: p1.id > p2.id. Delete p1 where same email (keeps p2 = row with smaller id). Alternative: DELETE WHERE id NOT IN (SELECT MIN(id) ...).

---

## 45. 181 – Employees Earning More Than Their Managers

### How to Identify
- **Keywords:** "earn more", "than their manager"
- **Pattern:** Self-join to compare employee vs manager salary

### Best Approach
Self-join: Employee e1 (employee), Employee e2 (manager) where e1.managerId = e2.id. Filter e1.salary > e2.salary.

### Key Keywords & Tricks
- Self-join: `e1.managerId = e2.id`
- `WHERE e1.salary > e2.salary`

### Solution

```sql
SELECT e1.name AS Employee
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary;
```

### Explanation
e1 = employee, e2 = manager. Join on managerId. Keep employees with higher salary than manager.

---

## 46. 512 – Game Play Analysis II

### How to Identify
- **Keywords:** "first login", "device"
- **Pattern:** First row per group – ROW_NUMBER or MIN + GROUP BY

### Best Approach
`ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date)` then filter rn = 1. Or MIN(event_date) per player + join.

### Solution

```sql
SELECT player_id, device_id
FROM (
    SELECT player_id, device_id,
           ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date) AS rn
    FROM Activity
) t
WHERE rn = 1;
```

### Explanation
ROW_NUMBER assigns 1 to first login per player. Filter rn = 1 to get first device.

---

## 47. 550 – Game Play Analysis IV

### How to Identify
- **Keywords:** "first day", "logged in again", "fraction"
- **Pattern:** Count players with login on day 1 and day 2, divide by total

### Best Approach
Find min date per player. Count players with (player_id, min_date+1) in Activity. Fraction = count / total distinct players.

### Solution

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
) a2 ON a1.player_id = a2.player_id AND DATEDIFF(a1.event_date, a2.first_date) = 1;
```

### Explanation
Subquery: first login per player. Join Activity where event_date = first_date + 1. Count distinct players who logged in next day. Divide by total players.

---

## 48. 1164 – Product Price at a Given Date

### How to Identify
- **Keywords:** "given date", "change", "before"
- **Pattern:** Latest price on or before given date per product

### Best Approach
For each product, find max(change_date) where change_date <= '2019-08-16'. Join to get price. Handle products with no change before date (use default 10).

### Solution

```sql
SELECT DISTINCT p.product_id, IFNULL(t.new_price, 10) AS price
FROM Products p
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

### Explanation
Subquery: (product_id, max change_date <= given date). Join to get price. LEFT JOIN + IFNULL for products never changed (price 10).

---

## 49. 1204 – Last Person to Fit in the Bus

### How to Identify
- **Keywords:** "queue", "weight limit", "last person"
- **Pattern:** Running sum, find last person where cumulative <= 1000

### Best Approach
`SUM(weight) OVER (ORDER BY turn)` for running total. Filter rows where running total <= 1000. Take last row.

### Solution

```sql
SELECT person_name
FROM (
    SELECT person_name, turn,
           SUM(weight) OVER (ORDER BY turn) AS running_weight
    FROM Queue
) t
WHERE running_weight <= 1000
ORDER BY turn DESC
LIMIT 1;
```

### Explanation
Running sum of weight by turn. Filter running_weight <= 1000. Last such row = last person to fit. ORDER BY turn DESC LIMIT 1.

---

## 50. 1907 – Count Salary Categories

### How to Identify
- **Keywords:** "count", "categories", "Low/Average/High"
- **Pattern:** CASE for buckets + COUNT or UNION of category counts

### Best Approach
CASE WHEN salary < 20000 THEN 'Low' WHEN salary <= 50000 THEN 'Average' ELSE 'High'. GROUP BY category. Include categories with 0 – use UNION with base categories.

### Solution

```sql
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count
FROM Accounts WHERE income < 20000
UNION ALL
SELECT 'Average Salary', COUNT(*)
FROM Accounts WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'High Salary', COUNT(*)
FROM Accounts WHERE income > 50000;
```

### Explanation
Three separate counts for each bucket. UNION ALL combines. If a category has 0, COUNT returns 0. To always show all categories, use a categories table and LEFT JOIN.

---

## Key Takeaway

**Advanced patterns:** Complex JOINs, DELETE with self-join, running sum with frame, conditional aggregation, date arithmetic, handling NULL/0 with IFNULL/COALESCE. Break problems into subqueries/CTEs.
