# Questions 21–30: Aggregation & GROUP BY

---

## 21. 182 – Duplicate Emails

### How to Identify
- **Keywords:** "duplicate", "more than once"
- **Pattern:** GROUP BY + HAVING COUNT(*) > 1

### Best Approach
`GROUP BY email HAVING COUNT(*) > 1`. Return distinct emails.

### Key Keywords & Tricks
- `GROUP BY email`
- `HAVING COUNT(*) > 1`
- No need for DISTINCT if grouping by email

### Solution

```sql
SELECT email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

### Explanation
Group by email. Emails with more than one row are duplicates. HAVING filters groups.

---

## 22. 1050 – Actors and Directors Who Cooperated At Least Three Times

### How to Identify
- **Keywords:** "at least three times", "cooperated"
- **Pattern:** GROUP BY multiple columns + HAVING

### Best Approach
`GROUP BY actor_id, director_id HAVING COUNT(*) >= 3`.

### Key Keywords & Tricks
- `GROUP BY actor_id, director_id`
- `HAVING COUNT(*) >= 3`

### Solution

```sql
SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3;
```

### Explanation
Each (actor_id, director_id) pair can appear multiple times. Filter pairs with 3+ cooperations.

---

## 23. 1587 – Bank Account Summary II

### How to Identify
- **Keywords:** "balance", "sum", "above 10000"
- **Pattern:** JOIN + GROUP BY + HAVING

### Best Approach
Join Users with Transactions. Sum amount (credit positive, debit negative) per account. `HAVING balance > 10000`.

### Key Keywords & Tricks
- `SUM(CASE WHEN type = 'deposit' THEN amount ELSE -amount END)`
- `GROUP BY account`
- `HAVING balance > 10000`

### Solution

```sql
SELECT u.name, SUM(t.amount) AS balance
FROM Users u
JOIN Transactions t ON u.account = t.account
GROUP BY u.account, u.name
HAVING balance > 10000;
```

### Explanation
Sum amounts per account (Transactions may use debit as negative). Filter accounts with balance > 10000. Note: Adjust for deposit/withdrawal logic per problem.

---

## 24. 1084 – Sales Analysis III

### How to Identify
- **Keywords:** "only", "first quarter", "product not sold in Q2"
- **Pattern:** NOT IN or EXCEPT for exclusion

### Best Approach
Products sold in Q1 but not in Q2. `WHERE product_id IN (Q1 sales) AND product_id NOT IN (Q2 sales)`.

### Solution

```sql
SELECT DISTINCT p.product_id, p.product_name
FROM Product p
JOIN Sales s ON p.product_id = s.product_id
WHERE s.sale_date BETWEEN '2019-01-01' AND '2019-03-31'
  AND p.product_id NOT IN (
      SELECT product_id FROM Sales
      WHERE sale_date NOT BETWEEN '2019-01-01' AND '2019-03-31'
  );
```

### Explanation
Include products sold in Q1. Exclude products sold outside Q1 (i.e. in Q2+). Result: products sold only in Q1.

---

## 25. 1148 – Article Views I (Distinct Authors)

### How to Identify
- Same as Q4 – self-view + DISTINCT

### Solution

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;
```

---

## 26. 1978 – Employees Whose Manager Left the Company

### How to Identify
- **Keywords:** "manager left", "salary < 30000"
- **Pattern:** Subquery for managers who left + filter employees

### Best Approach
Managers who left: salary < 30000. Employees whose manager_id in that set.

### Solution

```sql
SELECT employee_id
FROM Employees
WHERE manager_id NOT IN (SELECT employee_id FROM Employees)
  AND salary < 30000
ORDER BY employee_id;
```

### Explanation
Managers who left are not in Employees. Employees with such manager_id and salary < 30000. Note: Problem may define "left" differently – adjust filter.

---

## 27. 602 – Friend Requests II: Who Has the Most Friends

### How to Identify
- **Keywords:** "most friends", "accepters and requesters"
- **Pattern:** UNION ALL + GROUP BY + ORDER BY + LIMIT

### Best Approach
Union request_id and accepter_id (both are "friends"). Count per id. Order by count DESC, LIMIT 1.

### Key Keywords & Tricks
- `UNION ALL` – combine requester and accepter
- `GROUP BY` + `COUNT`
- `ORDER BY COUNT(*) DESC LIMIT 1`

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

### Explanation
Each row creates two friendships (requester-accepter). UNION ALL counts both directions. Person with max count has most friends.

---

## 28. 1341 – Movie Rating

### How to Identify
- **Keywords:** "most movies", "highest average", "February 2020"
- **Pattern:** Multiple aggregates, different filters

### Best Approach
Two queries or UNION: (1) user with most movie ratings, (2) movie with highest avg in Feb 2020.

### Solution

```sql
(SELECT name AS results
 FROM Users u
 JOIN MovieRating mr ON u.user_id = mr.user_id
 WHERE created_at LIKE '2020-02%'
 GROUP BY u.user_id, name
 ORDER BY COUNT(*) DESC, name
 LIMIT 1)
UNION ALL
(SELECT title AS results
 FROM Movies m
 JOIN MovieRating mr ON m.movie_id = mr.movie_id
 WHERE created_at LIKE '2020-02%'
 GROUP BY m.movie_id, title
 ORDER BY AVG(rating) DESC, title
 LIMIT 1);
```

### Explanation
First subquery: user with most ratings in Feb 2020, tiebreak by name. Second: movie with highest avg rating in Feb 2020, tiebreak by title.

---

## 29. 586 – Customer Placing the Largest Number of Orders

### How to Identify
- **Keywords:** "largest number of orders"
- **Pattern:** GROUP BY + ORDER BY COUNT + LIMIT

### Best Approach
`GROUP BY customer_number ORDER BY COUNT(*) DESC LIMIT 1`.

### Solution

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

### Explanation
Count orders per customer. Return customer with max count. Handle ties as required (e.g. MIN customer_number).

---

## 30. 1543 – Fix Product Name Format

### How to Identify
- **Keywords:** "format", "trim", "lowercase"
- **Pattern:** String functions + GROUP BY

### Best Approach
`LOWER(TRIM(product_name))`, fix 'sale' spelling, GROUP BY, ORDER BY.

### Solution

```sql
SELECT LOWER(TRIM(REPLACE(product_name, ' ', ''))) AS product_name,
       sale_date,
       COUNT(*) AS total
FROM Sales
GROUP BY 1, sale_date
ORDER BY 1, sale_date;
```

### Explanation
Normalize product name (lowercase, trim, remove spaces). Group by normalized name and date. Adjust REPLACE per problem (e.g. fix "sale").

---

## Key Takeaway

**Aggregation patterns:** GROUP BY, HAVING COUNT, SUM/CASE for conditional sums, UNION ALL for combining counts. Use ORDER BY + LIMIT for "top 1" or "most".
