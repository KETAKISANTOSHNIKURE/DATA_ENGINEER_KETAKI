# How to Identify SQL Problems & Keywords

This guide teaches you how to **recognize problem types** from the problem description and choose the right solution pattern.

---

## 1️⃣ Keyword → Solution Mapping

### "Second highest", "Nth highest", "Top N per group"

| Keywords | Solution | Trick |
|----------|----------|-------|
| second highest salary | `ORDER BY ... DESC LIMIT 1 OFFSET 1` | Or `DENSE_RANK() OVER (ORDER BY salary DESC)` |
| Nth highest | `LIMIT 1 OFFSET N-1` or `NTH_VALUE()` | Create function for dynamic N |
| top 3 per department | `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` | Filter `WHERE rn <= 3` |

**Identification:** Look for **"second", "third", "top N", "highest", "lowest"** + **"per group"** or **"each"**.

---

### "Duplicate", "More than once", "Appears twice"

| Keywords | Solution | Trick |
|----------|----------|-------|
| find duplicates | `GROUP BY col HAVING COUNT(*) > 1` | Or `COUNT(*) OVER (PARTITION BY col)` |
| remove duplicates | `DELETE` with self-join or `ROW_NUMBER()` | Keep min/max id |

**Identification:** **"duplicate", "repeated", "more than once"** → `GROUP BY` + `HAVING`.

---

### "Never", "Did not", "Without", "Not in"

| Keywords | Solution | Trick |
|----------|----------|-------|
| customers who never ordered | `LEFT JOIN orders` + `WHERE order_id IS NULL` | Or `WHERE id NOT IN (SELECT customer_id FROM orders)` |
| visited but did not make transaction | `LEFT JOIN transactions` + `WHERE transaction_id IS NULL` | Anti-join pattern |

**Identification:** **"never", "did not", "without"** → `LEFT JOIN` + `IS NULL` or `NOT IN` / `NOT EXISTS`.

---

### "Consecutive", "In a row", "Three times in a row"

| Keywords | Solution | Trick |
|----------|----------|-------|
| 3 consecutive numbers | Self-join 3 times on `id = id+1` and `id = id+2` | Or `LAG()` / `LEAD()` |
| consecutive dates | `DATEDIFF` or `LAG(date)` check | Compare with previous row |

**Identification:** **"consecutive", "in a row"** → Self-join or window `LAG`/`LEAD`.

---

### "Running total", "Cumulative", "Moving average"

| Keywords | Solution | Trick |
|----------|----------|-------|
| running sum | `SUM(amount) OVER (ORDER BY date)` | Window function with `ORDER BY` |
| 7-day moving average | `AVG() OVER (ORDER BY date ROWS 6 PRECEDING)` | Frame clause |

**Identification:** **"running", "cumulative", "moving"** → `OVER (ORDER BY ...)`.

---

### "Combine", "Merge", "Join two tables"

| Keywords | Solution | Trick |
|----------|----------|-------|
| combine two tables | `LEFT JOIN` (keep all from left) | Use `LEFT JOIN` when you need all rows from one table |
| get data from multiple tables | `INNER JOIN` or `LEFT JOIN` | Choose based on "all" vs "matching only" |

**Identification:** **"combine", "merge", "from both"** → `JOIN`.

---

### "Per group", "Each department", "For each"

| Keywords | Solution | Trick |
|----------|----------|-------|
| highest salary per department | `MAX(salary)` + `GROUP BY department` | Or `RANK() OVER (PARTITION BY dept)` |
| count per category | `GROUP BY category` | Aggregation + GROUP BY |

**Identification:** **"per", "each", "for every"** → `GROUP BY` or `PARTITION BY`.

---

### "Yesterday", "Rising", "Compare with previous"

| Keywords | Solution | Trick |
|----------|----------|-------|
| rising temperature | Self-join or `LAG()` | Compare today with yesterday |
| records with date = previous | `LAG(temperature) OVER (ORDER BY date)` | Window function |

**Identification:** **"compared to previous", "yesterday", "rising"** → Self-join or `LAG()`.

---

### "Rate", "Percentage", "Confirmation rate"

| Keywords | Solution | Trick |
|----------|----------|-------|
| confirmation rate | `ROUND(SUM(confirmed)/COUNT(*), 2)` | Use `CASE WHEN action='confirmed' THEN 1 ELSE 0 END` |
| percentage | `COUNT(CASE WHEN ...)*100.0/COUNT(*)` | Handle division by zero |

**Identification:** **"rate", "percentage", "ratio"** → Aggregate with `CASE` or `SUM(condition)`.

---

### "All", "Bought all products"

| Keywords | Solution | Trick |
|----------|----------|-------|
| customers who bought all products | `GROUP BY customer HAVING COUNT(DISTINCT product) = (SELECT COUNT(*) FROM products)` | Compare distinct count with total |

**Identification:** **"all", "every"** → `HAVING COUNT(DISTINCT x) = (total)`.

---

## 2️⃣ Problem Type Checklist

Before writing SQL, ask:

1. **Single table or multiple?** → JOIN needed?
2. **Filter rows or aggregate?** → `WHERE` vs `GROUP BY`
3. **Need ranking/order?** → `RANK`, `ROW_NUMBER`, `DENSE_RANK`
4. **Compare with previous/next row?** → `LAG`, `LEAD`
5. **Exclude rows (anti-join)?** → `LEFT JOIN` + `IS NULL` or `NOT IN`

---

## 3️⃣ Most Common Solution Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `SELECT ... WHERE` | Simple filter | Big countries, invalid tweets |
| `LEFT JOIN ... WHERE right.id IS NULL` | Find rows not in another table | Customers who never ordered |
| `GROUP BY ... HAVING COUNT(*) > 1` | Find duplicates | Duplicate emails |
| `RANK() OVER (PARTITION BY ... ORDER BY ...)` | Top N per group | Department top 3 salaries |
| `LAG(col) OVER (ORDER BY date)` | Compare with previous row | Rising temperature |
| `SUM() OVER (ORDER BY date)` | Running total | Restaurant growth |
| Subquery with `NOT IN` | Exclude | Customers who never ordered |
| `COALESCE` / `IFNULL` | Handle NULL | Combine two tables |

---

## Key Takeaway

**Read the problem → Identify keywords → Map to pattern → Write solution.**

Most LeetCode SQL problems use one of ~15 patterns. Master the keyword mapping and you can quickly identify the right approach.
