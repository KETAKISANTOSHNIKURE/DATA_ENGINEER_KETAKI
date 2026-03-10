# Questions 1–10: Basic SELECT & Filtering

---

## 1. 1757 – Recyclable and Low Fat Products

### How to Identify
- **Keywords:** "low fat", "recyclable", filter products
- **Pattern:** Simple `WHERE` with multiple conditions

### Best Approach
Filter with `AND` for both conditions.

### Key Keywords & Tricks
- `WHERE` + multiple `AND`
- `product_id` as primary key

### Solution

```sql
SELECT product_id
FROM Products
WHERE low_fats = 'Y' AND recyclable = 'Y';
```

### Explanation
Simple row filter. Both conditions must be true – use `AND`. No JOIN or aggregation needed.

---

## 2. 584 – Find Customer Referee

### How to Identify
- **Keywords:** "referee_id", "not 2", handle NULL
- **Pattern:** Filter with NULL handling

### Best Approach
Use `referee_id IS NULL OR referee_id != 2`. **Trick:** `referee_id = 2` excludes NULL because `NULL = 2` is unknown (not TRUE).

### Key Keywords & Tricks
- `IS NULL` – NULL-safe check
- `OR` – include rows where referee_id is NULL or not 2
- **Avoid:** `referee_id != 2` alone (excludes NULL)

### Solution

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL OR referee_id != 2;
```

### Explanation
`referee_id != 2` returns NULL for NULL values, so those rows are filtered out. Must explicitly add `referee_id IS NULL` to include them.

---

## 3. 595 – Big Countries

### How to Identify
- **Keywords:** "area", "population", "big" (OR condition)
- **Pattern:** Filter with OR

### Best Approach
`WHERE area >= 3000000 OR population >= 25000000`

### Key Keywords & Tricks
- `OR` – either condition
- `>=` – inclusive

### Solution

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000 OR population >= 25000000;
```

### Explanation
A country is "big" if it meets either condition. `OR` includes rows satisfying at least one.

---

## 4. 1148 – Article Views I

### How to Identify
- **Keywords:** "viewed their own", "author_id = viewer_id"
- **Pattern:** Self-view + DISTINCT

### Best Approach
Filter where `author_id = viewer_id`, then `DISTINCT author_id`.

### Key Keywords & Tricks
- `author_id = viewer_id` – self-join condition
- `DISTINCT` – remove duplicates
- `ORDER BY` – sorted output

### Solution

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;
```

### Explanation
Self-view means author and viewer are the same. `DISTINCT` removes duplicate author_ids. Sort as required.

---

## 5. 1683 – Invalid Tweets

### How to Identify
- **Keywords:** "invalid", "content length"
- **Pattern:** String length filter

### Best Approach
`WHERE CHAR_LENGTH(content) > 15` or `LENGTH(content) > 15`

### Key Keywords & Tricks
- `CHAR_LENGTH()` or `LENGTH()` – string length
- Filter on computed value

### Solution

```sql
SELECT tweet_id
FROM Tweets
WHERE CHAR_LENGTH(content) > 15;
```

### Explanation
Filter tweets where content has more than 15 characters. `CHAR_LENGTH` counts characters (Unicode-safe).

---

## 6. 1378 – Replace Employee ID With The Unique Identifier

### How to Identify
- **Keywords:** "replace", "unique identifier", "employee id"
- **Pattern:** LEFT JOIN to get optional data

### Best Approach
`LEFT JOIN` Employees with EmployeeUNI on `id` to get `unique_id`. Keep all employees even without unique_id.

### Key Keywords & Tricks
- `LEFT JOIN` – keep all from left table
- `ON Employees.id = EmployeeUNI.id`

### Solution

```sql
SELECT eu.unique_id, e.name
FROM Employees e
LEFT JOIN EmployeeUNI eu ON e.id = eu.id;
```

### Explanation
`LEFT JOIN` ensures every employee appears. If no match in EmployeeUNI, `unique_id` is NULL. Use alias for clarity.

---

## 7. 1068 – Product Sales Analysis I

### How to Identify
- **Keywords:** "product name", "year", "price" from Sales and Product
- **Pattern:** INNER JOIN to combine tables

### Best Approach
`INNER JOIN` Sales with Product on `product_id`.

### Key Keywords & Tricks
- `INNER JOIN` – only rows with matching product
- Select from both tables

### Solution

```sql
SELECT p.product_name, s.year, s.price
FROM Sales s
INNER JOIN Product p ON s.product_id = p.product_id;
```

### Explanation
Every sale has a product_id, so INNER JOIN is appropriate. Get product_name from Product, year and price from Sales.

---

## 8. 1581 – Customer Who Visited but Did Not Make Transactions

### How to Identify
- **Keywords:** "visited", "did not make", "transactions"
- **Pattern:** Anti-join (LEFT JOIN + IS NULL)

### Best Approach
`LEFT JOIN` Visits with Transactions. Rows with `transaction_id IS NULL` are visits without transactions.

### Key Keywords & Tricks
- `LEFT JOIN` – keep all visits
- `WHERE transaction_id IS NULL` – no matching transaction
- `COUNT` + `GROUP BY customer_id`

### Solution

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

### Explanation
LEFT JOIN keeps all visits. Where no transaction exists, `transaction_id` is NULL. Group by customer and count.

---

## 9. 197 – Rising Temperature

### How to Identify
- **Keywords:** "rising", "yesterday", "compare"
- **Pattern:** Compare with previous row (LAG or self-join)

### Best Approach
Use `LAG(temperature) OVER (ORDER BY recordDate)` to get yesterday's temperature. Compare with today.

### Key Keywords & Tricks
- `LAG()` – previous row value
- `DATEDIFF` or date comparison – ensure consecutive days
- `OVER (ORDER BY recordDate)`

### Solution

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

### Explanation
`LAG` gets previous row's temperature and date. Filter where today's temp > yesterday's AND dates are consecutive (DATEDIFF = 1).

---

## 10. 1661 – Average Time of Process per Machine

### How to Identify
- **Keywords:** "average", "process", "per machine"
- **Pattern:** Calculate time difference + GROUP BY

### Best Approach
Match `start` and `end` activities by machine_id and process_id. Compute `end - start`, then `AVG` per machine.

### Key Keywords & Tricks
- Self-join or `CASE` to pivot start/end
- `TIMESTAMPDIFF` or subtract timestamps
- `GROUP BY machine_id`

### Solution

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

### Explanation
Self-join matches start with end for same machine and process. `b.timestamp - a.timestamp` gives process time. Average per machine.

---

## Key Takeaway

**Basic patterns:** `WHERE`, `AND`/`OR`, `IS NULL`, `LEFT JOIN` + `IS NULL`, `LAG()` for previous row, `GROUP BY` + aggregate.
