# Questions 11–20: JOINs & Multiple Tables

---

## 11. 175 – Combine Two Tables

### How to Identify
- **Keywords:** "combine", "address", "person" – keep all persons
- **Pattern:** LEFT JOIN (preserve all from left)

### Best Approach
`LEFT JOIN` Person with Address. All persons appear even without address.

### Key Keywords & Tricks
- `LEFT JOIN` – keep all Person rows
- `ON Person.personId = Address.personId`
- Handle NULL for missing address

### Solution

```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```

### Explanation
`LEFT JOIN` ensures every person is returned. If no address, city and state are NULL. Use table aliases.

---

## 12. 1581 – Customer Visits Without Transactions

### How to Identify
- **Keywords:** "visited", "did not make transactions"
- **Pattern:** Anti-join

### Best Approach
`LEFT JOIN` Visits with Transactions. `WHERE transaction_id IS NULL`.

### Solution

```sql
SELECT customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY customer_id;
```

### Explanation
LEFT JOIN keeps visits without transactions. `visit_id IS NULL` from Transactions means no transaction. Count per customer.

---

## 13. 1141 – User Activity for the Past 30 Days I

### How to Identify
- **Keywords:** "past 30 days", "daily", "active users"
- **Pattern:** Date filter + GROUP BY

### Best Approach
Filter `WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'`, then `GROUP BY activity_date`, count distinct users.

### Key Keywords & Tricks
- `BETWEEN` or `DATEDIFF` for date range
- `COUNT(DISTINCT user_id)`
- `GROUP BY activity_date`

### Solution

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date;
```

### Explanation
Limit to 30-day window. Count unique users per day. Note: "past 30 days" usually means 30 days ending today.

---

## 14. 1693 – Daily Leads and Partners

### How to Identify
- **Keywords:** "daily", "unique leads", "unique partners" per date and make
- **Pattern:** GROUP BY + COUNT DISTINCT

### Best Approach
`GROUP BY date_id, make_name`, then `COUNT(DISTINCT lead_id)` and `COUNT(DISTINCT partner_id)`.

### Key Keywords & Tricks
- `COUNT(DISTINCT col)`
- `GROUP BY` multiple columns

### Solution

```sql
SELECT date_id, make_name, 
       COUNT(DISTINCT lead_id) AS unique_leads,
       COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name;
```

### Explanation
Group by date and make. Count distinct leads and partners per group. Handles duplicates within each group.

---

## 15. 570 – Managers with at Least 5 Direct Reports

### How to Identify
- **Keywords:** "manager", "at least 5", "direct reports"
- **Pattern:** Self-join + GROUP BY + HAVING

### Best Approach
Join Employee with itself on `managerId = id`. Group by manager, count reports, filter `HAVING COUNT(*) >= 5`.

### Key Keywords & Tricks
- Self-join: `Employee e1 JOIN Employee e2 ON e1.managerId = e2.id`
- `GROUP BY manager_id`
- `HAVING COUNT(*) >= 5`

### Solution

```sql
SELECT e2.name
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
GROUP BY e1.managerId, e2.name
HAVING COUNT(*) >= 5;
```

### Explanation
e1 = reports, e2 = manager. Join on managerId. Group by manager and count. HAVING filters managers with 5+ reports.

---

## 16. 1934 – Confirmation Rate

### How to Identify
- **Keywords:** "confirmation rate", "confirmed"
- **Pattern:** Aggregate with CASE for rate

### Best Approach
LEFT JOIN Signups with Confirmations. Compute `ROUND(SUM(confirmed)/COUNT(*), 2)`. Handle NULL with `IFNULL`.

### Key Keywords & Tricks
- `CASE WHEN action = 'confirmed' THEN 1 ELSE 0 END`
- `ROUND(..., 2)`
- `IFNULL(rate, 0)` for users with no confirmations

### Solution

```sql
SELECT s.user_id,
       ROUND(IFNULL(SUM(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END) / COUNT(c.user_id), 0), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id;
```

### Explanation
LEFT JOIN keeps all signups. For each user, count confirmed / total confirmation attempts. IFNULL handles no confirmations (0).

---

## 17. 619 – Biggest Single Number

### How to Identify
- **Keywords:** "single number", "appears once", "biggest"
- **Pattern:** GROUP BY + HAVING + MAX

### Best Approach
Find numbers appearing once: `GROUP BY num HAVING COUNT(*) = 1`. Then take `MAX(num)`.

### Key Keywords & Tricks
- `GROUP BY num HAVING COUNT(*) = 1`
- `SELECT MAX(num)` or subquery
- Handle empty result (NULL)

### Solution

```sql
SELECT MAX(num) AS num
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) t;
```

### Explanation
Subquery returns numbers that appear exactly once. MAX gives the largest. If none, MAX returns NULL.

---

## 18. 1045 – Customers Who Bought All Products

### How to Identify
- **Keywords:** "bought all products"
- **Pattern:** HAVING COUNT(DISTINCT product_key) = total products

### Best Approach
Count distinct products per customer. Compare with `(SELECT COUNT(*) FROM Product)`.

### Key Keywords & Tricks
- `GROUP BY customer_id`
- `HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product)`

### Solution

```sql
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);
```

### Explanation
For each customer, count distinct products. Only include customers whose count equals total number of products.

---

## 19. 1731 – The Number of Employees Which Report to Each Employee

### How to Identify
- **Keywords:** "report to", "each employee", "count"
- **Pattern:** Self-join + GROUP BY

### Best Approach
Self-join on `reports_to = id`. Group by manager, count reports.

### Solution

```sql
SELECT e2.employee_id, e2.name, COUNT(*) AS reports_count, e2.age
FROM Employees e1
JOIN Employees e2 ON e1.reports_to = e2.employee_id
GROUP BY e2.employee_id, e2.name, e2.age
ORDER BY e2.employee_id;
```

### Explanation
e1 = reporters, e2 = manager. Join on reports_to. Group by manager and count.

---

## 20. 1789 – Primary Department for Each Employee

### How to Identify
- **Keywords:** "primary", "each employee", "single department" vs "multiple"
- **Pattern:** CASE or filter – primary = only dept or primary_flag = 'Y'

### Best Approach
If only one department, that's primary. If multiple, use primary_flag. `WHERE primary_flag = 'Y' OR (employee_id) IN (single-dept employees)`.

### Solution

```sql
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
   OR employee_id IN (
       SELECT employee_id
       FROM Employee
       GROUP BY employee_id
       HAVING COUNT(*) = 1
   );
```

### Explanation
Include rows where primary_flag is Y, or employee has only one department (that becomes primary).

---

## Key Takeaway

**JOIN patterns:** LEFT JOIN (keep all), INNER JOIN (matches only), self-join (same table), anti-join (LEFT JOIN + IS NULL). Use GROUP BY + HAVING for "per group" conditions.
