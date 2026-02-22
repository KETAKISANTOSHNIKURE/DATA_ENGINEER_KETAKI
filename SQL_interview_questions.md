Here's the complete `.md` file script for your GitHub repository:

```markdown
# 🧠 SQL Interview Questions & Answers

> A curated collection of SQL interview questions asked at **FAANG+ companies** (Amazon, Google, Meta, Microsoft, Uber, PayPal, Adobe, Walmart) with corrected and optimized answers.

---

## 📋 Table of Contents

| #  | Question | Company | Difficulty |
|----|----------|---------|------------|
| 1  | [Find Duplicate Records](#1-find-duplicate-records-in-a-table) | Amazon | Easy |
| 2  | [Second Highest Salary](#2-retrieve-the-second-highest-salary-from-employee-table) | Amazon | Easy |
| 3  | [Employees Without Department](#3-find-employees-without-department) | Uber | Easy |
| 4  | [Total Revenue Per Product](#4-calculate-the-total-revenue-per-product) | PayPal | Easy |
| 5  | [Top 3 Highest-Paid Employees](#5-get-the-top-3-highest-paid-employees) | Google | Easy |
| 7  | [Count Orders Per Customer](#7-show-the-count-of-orders-per-customer) | Meta | Easy |
| 8  | [Employees Joined in 2023](#8-retrieve-all-employees-who-joined-in-2023) | Amazon | Easy |
| 9  | [Average Order Value Per Customer](#9-calculate-average-order-value-per-customer) | Microsoft | Easy |
| 10 | [Latest Order Per Customer](#10-get-the-latest-order-placed-by-each-customer) | Uber | Medium |
| 11 | [Products Never Sold](#11-find-products-that-were-never-sold) | Amazon | Easy |
| 12 | [Most Selling Product](#12-identify-the-most-selling-product) | Adobe/Walmart | Medium |
| 13 | [Revenue & Orders Per Region](#13-get-total-revenue-and-number-of-orders-per-region) | Meta | Easy |
| 14 | [Customers With 5+ Orders](#14-count-customers-with-more-than-5-orders) | Amazon | Easy |
| 15 | [Orders Above Average Value](#15-retrieve-customers-with-orders-above-average-order-value) | PayPal | Medium |
| 16 | [Employees Hired on Weekends](#16-find-all-employees-hired-on-weekends) | Google | Easy |
| 17 | [Salary Between Range](#17-find-all-employees-with-salary-between-50000-and-100000) | Microsoft | Easy |
| 18 | [Monthly Sales Revenue](#18-get-monthly-sales-revenue-and-order-count) | Google | Medium |
| 19 | [Rank Employees by Salary](#19-rank-employees-by-salary-within-each-department) | Amazon | Medium |
| 20 | [Customers Ordered Every Month](#20-find-customers-who-placed-orders-every-month-in-2023) | Meta | Hard |
| 21 | [Moving Average of Sales](#21-find-moving-average-of-sales-over-the-last-3-days) | Microsoft | Medium |
| 22 | [First & Last Order Date](#22-identify-the-first-and-last-order-date-for-each-customer) | Uber | Easy |
| 23 | [Product Sales Distribution](#23-show-product-sales-distribution-percent-of-total-revenue) | PayPal | Medium |
| 24 | [Consecutive Purchases](#24-retrieve-customers-who-made-consecutive-purchases) | Walmart | Hard |
| 25 | [Churned Customers](#25-find-churned-customers-no-orders-in-the-last-6-months) | Amazon | Medium |
| 26 | [Cumulative Revenue by Day](#26-calculate-cumulative-revenue-by-day) | Adobe | Medium |
| 27 | [Top Departments by Avg Salary](#27-identify-top-performing-departments-by-average-salary) | Google | Easy |
| 28 | [Above Average Orders](#28-find-customers-who-ordered-more-than-the-average-number-of-orders) | Meta | Medium |
| 29 | [Revenue from New Customers](#29-calculate-revenue-generated-from-new-customers) | Microsoft | Medium |
| 30 | [Employee Percentage Per Dept](#30-find-the-percentage-of-employees-in-each-department) | Uber | Medium |
| 31 | [Max Salary Difference](#31-retrieve-the-maximum-salary-difference-within-each-department) | PayPal | Easy |
| 32 | [80% Revenue Products (Pareto)](#32-find-products-that-contribute-to-80-of-the-revenue-pareto-principle) | Walmart | Hard |
| 33 | [Avg Time Between Purchases](#33-calculate-average-time-between-two-purchases-for-each-customer) | Meta | Hard |
| 34 | [Last Purchase with Amount](#34-show-last-purchase-for-each-customer-along-with-order-amount) | Google | Medium |
| 35 | [Year-Over-Year Growth](#35-calculate-year-over-year-growth-in-revenue) | Microsoft | Hard |
| 36 | [Above 90th Percentile Purchase](#36-detect-customers-whose-purchase-amount-is-higher-than-their-historical-90th-percentile) | Amazon | Hard |
| 37 | [Longest Gap Between Orders](#37-retrieve-the-longest-gap-between-orders-for-each-customer) | Meta | Hard |
| 38 | [Revenue Below 10th Percentile](#38-identify-customers-with-revenue-below-the-10th-percentile) | Google | Hard |

---

## 🟢 Easy Questions

---

### 1. Find Duplicate Records in a Table
**Company:** Amazon | **Difficulty:** Easy

```sql
SELECT column1, column2, COUNT(*) AS duplicate_count
FROM your_table
GROUP BY column1, column2
HAVING COUNT(*) > 1;
```

**💡 Explanation:**
- `GROUP BY` groups identical rows together.
- `HAVING COUNT(*) > 1` filters only groups with more than one occurrence (duplicates).

---

### 2. Retrieve the Second Highest Salary from Employee Table
**Company:** Amazon | **Difficulty:** Easy

**Approach 1: Subquery**
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

**Approach 2: DENSE_RANK (Recommended for Interviews)**
```sql
SELECT salary AS SecondHighestSalary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM Employee
) t
WHERE rnk = 2;
```

**Approach 3: OFFSET-FETCH (SQL Server / PostgreSQL)**
```sql
SELECT DISTINCT salary AS SecondHighestSalary
FROM Employee
ORDER BY salary DESC
OFFSET 1 ROW FETCH NEXT 1 ROW ONLY;
```

**💡 Key Point:** `DENSE_RANK()` handles ties correctly, unlike `ROW_NUMBER()`.

---

### 3. Find Employees Without Department
**Company:** Uber | **Difficulty:** Easy

**Approach 1: LEFT JOIN**
```sql
SELECT e.*
FROM Employee e
LEFT JOIN Department d ON e.department_id = d.department_id
WHERE d.department_id IS NULL;
```

**Approach 2: NOT EXISTS (Often Preferred)**
```sql
SELECT *
FROM Employee e
WHERE NOT EXISTS (
    SELECT 1 FROM Department d WHERE d.department_id = e.department_id
);
```

**Approach 3: NOT IN**
```sql
SELECT *
FROM Employee
WHERE department_id NOT IN (SELECT department_id FROM Department);
```

> ⚠️ **Warning:** `NOT IN` can produce unexpected results if the subquery returns `NULL` values. Prefer `NOT EXISTS` in production.

---

### 4. Calculate the Total Revenue Per Product
**Company:** PayPal | **Difficulty:** Easy

```sql
SELECT product_id, SUM(quantity * price) AS total_revenue
FROM Sales
GROUP BY product_id;
```

---

### 5. Get the Top 3 Highest-Paid Employees
**Company:** Google | **Difficulty:** Easy

**Basic Approach (SQL Server — doesn't handle ties):**
```sql
SELECT TOP 3 *
FROM Employee
ORDER BY salary DESC;
```

**Recommended Approach (handles ties):**
```sql
SELECT *
FROM (
    SELECT *, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM Employee
) t
WHERE rnk <= 3;
```

**MySQL:**
```sql
SELECT *
FROM Employee
ORDER BY salary DESC
LIMIT 3;
```

**Standard SQL (with ties):**
```sql
SELECT *
FROM Employee
ORDER BY salary DESC
FETCH FIRST 3 ROWS WITH TIES;
```

> 💡 **Interview Tip:** Always mention how you'd handle ties — interviewers love this.

---

### 7. Show the Count of Orders Per Customer
**Company:** Meta | **Difficulty:** Easy

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM Orders
GROUP BY customer_id;
```

---

### 8. Retrieve All Employees Who Joined in 2023
**Company:** Amazon | **Difficulty:** Easy

**❌ Common but Non-Optimal Approach:**
```sql
SELECT *
FROM Employee
WHERE YEAR(hire_date) = 2023;
```

> ⚠️ Using `YEAR()` on the column prevents **index usage** (not sargable).

**✅ Optimized Approach (Sargable):**
```sql
SELECT *
FROM Employee
WHERE hire_date >= '2023-01-01' AND hire_date < '2024-01-01';
```

> 💡 **Interview Tip:** Mention sargability — it shows awareness of query performance.

---

### 9. Calculate Average Order Value Per Customer
**Company:** Microsoft | **Difficulty:** Easy

```sql
SELECT customer_id, AVG(total_amount) AS avg_order_value
FROM Orders
GROUP BY customer_id;
```

---

### 11. Find Products That Were Never Sold
**Company:** Amazon | **Difficulty:** Easy

**Approach 1: LEFT JOIN**
```sql
SELECT p.product_id, p.product_name
FROM Products p
LEFT JOIN Sales s ON p.product_id = s.product_id
WHERE s.product_id IS NULL;
```

**Approach 2: NOT EXISTS (Preferred)**
```sql
SELECT product_id, product_name
FROM Products p
WHERE NOT EXISTS (
    SELECT 1 FROM Sales s WHERE s.product_id = p.product_id
);
```

---

### 16. Find All Employees Hired on Weekends
**Company:** Google | **Difficulty:** Easy

**SQL Server:**
```sql
SELECT *
FROM Employee
WHERE DATENAME(WEEKDAY, hire_date) IN ('Saturday', 'Sunday');
```

**MySQL:**
```sql
SELECT *
FROM Employee
WHERE DAYOFWEEK(hire_date) IN (1, 7);
```

**PostgreSQL:**
```sql
SELECT *
FROM Employee
WHERE EXTRACT(DOW FROM hire_date) IN (0, 6);
```

---

### 17. Find All Employees with Salary Between 50000 and 100000
**Company:** Microsoft | **Difficulty:** Easy

```sql
SELECT *
FROM Employee
WHERE salary BETWEEN 50000 AND 100000;
```

> 💡 **Note:** `BETWEEN` is inclusive on both ends.

---

### 22. Identify the First and Last Order Date for Each Customer
**Company:** Uber | **Difficulty:** Easy

```sql
SELECT customer_id,
       MIN(order_date) AS first_order,
       MAX(order_date) AS last_order
FROM Orders
GROUP BY customer_id;
```

---

### 27. Identify Top-Performing Departments by Average Salary
**Company:** Google | **Difficulty:** Easy

```sql
SELECT department_id, AVG(salary) AS avg_salary
FROM Employee
GROUP BY department_id
ORDER BY avg_salary DESC;
```

**To get only the top department:**
```sql
SELECT TOP 1 department_id, AVG(salary) AS avg_salary
FROM Employee
GROUP BY department_id
ORDER BY avg_salary DESC;
```

---

### 31. Retrieve the Maximum Salary Difference Within Each Department
**Company:** PayPal | **Difficulty:** Easy

```sql
SELECT department_id,
       MAX(salary) - MIN(salary) AS salary_diff
FROM Employee
GROUP BY department_id;
```

---

## 🟡 Medium Questions

---

### 10. Get the Latest Order Placed by Each Customer
**Company:** Uber | **Difficulty:** Medium

**Basic Approach (only returns date):**
```sql
SELECT customer_id, MAX(order_date) AS latest_order_date
FROM Orders
GROUP BY customer_id;
```

**Recommended Approach (returns full order details):**
```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM Orders
)
SELECT *
FROM ranked
WHERE rn = 1;
```

> 💡 **Interview Tip:** Interviewers typically expect the complete order record, not just the date.

---

### 12. Identify the Most Selling Product
**Company:** Adobe / Walmart | **Difficulty:** Medium

**Basic Approach (SQL Server):**
```sql
SELECT TOP 1 product_id, SUM(quantity) AS total_qty
FROM Sales
GROUP BY product_id
ORDER BY total_qty DESC;
```

**Recommended Approach (handles ties):**
```sql
WITH product_sales AS (
    SELECT product_id, SUM(quantity) AS total_qty,
           RANK() OVER (ORDER BY SUM(quantity) DESC) AS rnk
    FROM Sales
    GROUP BY product_id
)
SELECT product_id, total_qty
FROM product_sales
WHERE rnk = 1;
```

---

### 13. Get Total Revenue and Number of Orders Per Region
**Company:** Meta | **Difficulty:** Easy

```sql
SELECT region,
       SUM(total_amount) AS total_revenue,
       COUNT(*) AS order_count
FROM Orders
GROUP BY region;
```

---

### 14. Count Customers with More Than 5 Orders
**Company:** Amazon | **Difficulty:** Easy

```sql
SELECT COUNT(*) AS customer_count
FROM (
    SELECT customer_id
    FROM Orders
    GROUP BY customer_id
    HAVING COUNT(*) > 5
) AS active_customers;
```

---

### 15. Retrieve Customers with Orders Above Average Order Value
**Company:** PayPal | **Difficulty:** Medium

```sql
SELECT *
FROM Orders
WHERE total_amount > (SELECT AVG(total_amount) FROM Orders);
```

---

### 18. Get Monthly Sales Revenue and Order Count
**Company:** Google | **Difficulty:** Medium

**SQL Server:**
```sql
SELECT FORMAT(order_date, 'yyyy-MM') AS month,
       SUM(amount) AS total_revenue,
       COUNT(order_id) AS order_count
FROM Orders
GROUP BY FORMAT(order_date, 'yyyy-MM')
ORDER BY month;
```

**MySQL:**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       SUM(amount) AS total_revenue,
       COUNT(order_id) AS order_count
FROM Orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

---

### 19. Rank Employees by Salary Within Each Department
**Company:** Amazon | **Difficulty:** Medium

```sql
SELECT employee_id, department_id, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
FROM Employee;
```

> 💡 **Interview Tip:** Be ready to explain the difference:
> - `ROW_NUMBER()` — unique sequential numbers, no ties
> - `RANK()` — same rank for ties, skips next rank(s)
> - `DENSE_RANK()` — same rank for ties, does NOT skip

---

### 21. Find Moving Average of Sales Over the Last 3 Days
**Company:** Microsoft | **Difficulty:** Medium

```sql
SELECT order_date,
       total_amount,
       AVG(total_amount) OVER (
           ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3days
FROM Orders;
```

**💡 Explanation:**
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` creates a sliding window of 3 rows (current + 2 previous).

---

### 23. Show Product Sales Distribution (Percent of Total Revenue)
**Company:** PayPal | **Difficulty:** Medium

**Approach 1: CTE with CROSS JOIN**
```sql
WITH TotalRevenue AS (
    SELECT SUM(quantity * price) AS total FROM Sales
)
SELECT s.product_id,
       SUM(s.quantity * s.price) AS revenue,
       ROUND(SUM(s.quantity * s.price) * 100.0 / t.total, 2) AS revenue_pct
FROM Sales s
CROSS JOIN TotalRevenue t
GROUP BY s.product_id, t.total;
```

**Approach 2: Window Function (More Elegant)**
```sql
SELECT product_id,
       SUM(quantity * price) AS revenue,
       ROUND(SUM(quantity * price) * 100.0 / SUM(SUM(quantity * price)) OVER (), 2) AS revenue_pct
FROM Sales
GROUP BY product_id;
```

---

### 25. Find Churned Customers (No Orders in the Last 6 Months)
**Company:** Amazon | **Difficulty:** Medium

**SQL Server:**
```sql
SELECT customer_id
FROM Orders
GROUP BY customer_id
HAVING MAX(order_date) < DATEADD(MONTH, -6, GETDATE());
```

**MySQL:**
```sql
SELECT customer_id
FROM Orders
GROUP BY customer_id
HAVING MAX(order_date) < DATE_SUB(CURDATE(), INTERVAL 6 MONTH);
```

---

### 26. Calculate Cumulative Revenue by Day
**Company:** Adobe | **Difficulty:** Medium

**Basic (may have issues with multiple rows per day):**
```sql
SELECT order_date,
       SUM(total_amount) OVER (ORDER BY order_date) AS cumulative_revenue
FROM Orders;
```

**Recommended (aggregate daily first):**
```sql
SELECT order_date,
       SUM(total_amount) AS daily_revenue,
       SUM(SUM(total_amount)) OVER (ORDER BY order_date) AS cumulative_revenue
FROM Orders
GROUP BY order_date;
```

---

### 28. Find Customers Who Ordered More Than the Average Number of Orders
**Company:** Meta | **Difficulty:** Medium

```sql
WITH customer_orders AS (
    SELECT customer_id, COUNT(*) AS order_count
    FROM Orders
    GROUP BY customer_id
)
SELECT *
FROM customer_orders
WHERE order_count > (SELECT AVG(order_count) FROM customer_orders);
```

---

### 29. Calculate Revenue Generated from New Customers (First-Time Orders)
**Company:** Microsoft | **Difficulty:** Medium

```sql
WITH first_orders AS (
    SELECT customer_id, MIN(order_date) AS first_order_date
    FROM Orders
    GROUP BY customer_id
)
SELECT SUM(o.total_amount) AS new_customer_revenue
FROM Orders o
JOIN first_orders f
    ON o.customer_id = f.customer_id
    AND o.order_date = f.first_order_date;
```

---

### 30. Find the Percentage of Employees in Each Department
**Company:** Uber | **Difficulty:** Medium

**Approach 1: Subquery**
```sql
SELECT department_id,
       COUNT(*) AS emp_count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Employee), 2) AS pct
FROM Employee
GROUP BY department_id;
```

**Approach 2: Window Function**
```sql
SELECT department_id,
       COUNT(*) AS emp_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
FROM Employee
GROUP BY department_id;
```

---

### 34. Show Last Purchase for Each Customer Along with Order Amount
**Company:** Google | **Difficulty:** Medium

```sql
WITH ranked_orders AS (
    SELECT customer_id, order_id, order_date, total_amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM Orders
)
SELECT customer_id, order_id, order_date, total_amount
FROM ranked_orders
WHERE rn = 1;
```

---

## 🔴 Hard Questions

---

### 20. Find Customers Who Placed Orders Every Month in 2023
**Company:** Meta | **Difficulty:** Hard

**SQL Server:**
```sql
SELECT customer_id
FROM Orders
WHERE YEAR(order_date) = 2023
GROUP BY customer_id
HAVING COUNT(DISTINCT FORMAT(order_date, 'yyyy-MM')) = 12;
```

**MySQL:**
```sql
SELECT customer_id
FROM Orders
WHERE YEAR(order_date) = 2023
GROUP BY customer_id
HAVING COUNT(DISTINCT MONTH(order_date)) = 12;
```

---

### 24. Retrieve Customers Who Made Consecutive Purchases (Within 2 Days)
**Company:** Walmart | **Difficulty:** Hard

```sql
WITH cte AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date
    FROM Orders
)
SELECT DISTINCT customer_id
FROM cte
WHERE DATEDIFF(DAY, prev_order_date, order_date) <= 2;
```

**For strictly consecutive days (difference = 1):**
```sql
WITH cte AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date
    FROM Orders
)
SELECT DISTINCT customer_id
FROM cte
WHERE DATEDIFF(DAY, prev_order_date, order_date) = 1;
```

---

### 32. Find Products That Contribute to 80% of the Revenue (Pareto Principle)
**Company:** Walmart | **Difficulty:** Hard

> ⚠️ **Common Mistake:** You CANNOT use a window function in a `WHERE` clause.

**✅ Correct Approach:**
```sql
WITH sales_cte AS (
    SELECT product_id, SUM(quantity * price) AS revenue
    FROM Sales
    GROUP BY product_id
),
total_revenue AS (
    SELECT SUM(revenue) AS total FROM sales_cte
),
cumulative AS (
    SELECT s.product_id,
           s.revenue,
           SUM(s.revenue) OVER (ORDER BY s.revenue DESC) AS running_total,
           t.total
    FROM sales_cte s
    CROSS JOIN total_revenue t
)
SELECT product_id,
       revenue,
       running_total,
       ROUND(running_total * 100.0 / total, 2) AS cumulative_pct
FROM cumulative
WHERE running_total <= total * 0.8;
```

---

### 33. Calculate Average Time Between Two Purchases for Each Customer
**Company:** Meta | **Difficulty:** Hard

```sql
WITH cte AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_date
    FROM Orders
)
SELECT customer_id,
       AVG(DATEDIFF(DAY, prev_date, order_date)) AS avg_gap_days
FROM cte
WHERE prev_date IS NOT NULL
GROUP BY customer_id;
```

---

### 35. Calculate Year-Over-Year Growth in Revenue
**Company:** Microsoft | **Difficulty:** Hard

```sql
WITH yearly_revenue AS (
    SELECT YEAR(order_date) AS yr,
           SUM(total_amount) AS revenue
    FROM Orders
    GROUP BY YEAR(order_date)
)
SELECT yr,
       revenue,
       LAG(revenue) OVER (ORDER BY yr) AS prev_year_revenue,
       revenue - LAG(revenue) OVER (ORDER BY yr) AS yoy_growth,
       ROUND(
           (revenue - LAG(revenue) OVER (ORDER BY yr)) * 100.0
           / LAG(revenue) OVER (ORDER BY yr), 2
       ) AS yoy_growth_pct
FROM yearly_revenue;
```

---

### 36. Detect Customers Whose Purchase Amount is Higher Than Their Historical 90th Percentile
**Company:** Amazon | **Difficulty:** Hard

**Approach 1: Using NTILE (Approximate)**
```sql
WITH ranked_orders AS (
    SELECT customer_id, order_id, total_amount,
           NTILE(10) OVER (PARTITION BY customer_id ORDER BY total_amount) AS decile
    FROM Orders
)
SELECT customer_id, order_id, total_amount
FROM ranked_orders
WHERE decile = 10;
```

**Approach 2: Using PERCENT_RANK (More Precise)**
```sql
WITH ranked AS (
    SELECT customer_id, order_id, total_amount,
           PERCENT_RANK() OVER (PARTITION BY customer_id ORDER BY total_amount) AS pct_rank
    FROM Orders
)
SELECT customer_id, order_id, total_amount
FROM ranked
WHERE pct_rank > 0.9;
```

---

### 37. Retrieve the Longest Gap Between Orders for Each Customer
**Company:** Meta | **Difficulty:** Hard

```sql
WITH cte AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date
    FROM Orders
)
SELECT customer_id,
       MAX(DATEDIFF(DAY, prev_order_date, order_date)) AS max_gap_days
FROM cte
WHERE prev_order_date IS NOT NULL
GROUP BY customer_id;
```

---

### 38. Identify Customers with Revenue Below the 10th Percentile
**Company:** Google | **Difficulty:** Hard

**SQL Server / PostgreSQL / Oracle:**
```sql
WITH cte AS (
    SELECT customer_id, SUM(total_amount) AS total_revenue
    FROM Orders
    GROUP BY customer_id
)
SELECT customer_id, total_revenue
FROM cte
WHERE total_revenue < (
    SELECT PERCENTILE_CONT(0.1) WITHIN GROUP (ORDER BY total_revenue) FROM cte
);
```

**MySQL Alternative (no PERCENTILE_CONT):**
```sql
WITH cte AS (
    SELECT customer_id, SUM(total_amount) AS total_revenue
    FROM Orders
    GROUP BY customer_id
),
ranked AS (
    SELECT total_revenue,
           PERCENT_RANK() OVER (ORDER BY total_revenue) AS pct
    FROM cte
)
SELECT c.customer_id, c.total_revenue
FROM cte c
WHERE c.total_revenue <= (
    SELECT MIN(total_revenue) FROM ranked WHERE pct >= 0.1
);
```

---

## 📊 Issues Summary from Original PDF

| Q# | Issue | Severity |
|----|-------|----------|
| 5 | Doesn't handle ties with `TOP 3` | ⚠️ Minor |
| 8 | `YEAR()` on column prevents index usage (not sargable) | ⚠️ Minor |
| 10 | Only returns date, not full order details | ⚠️ Minor |
| 11 | Typo: `Productsp` instead of `Products p` | 📝 Typo |
| 23 | Typos: `Saless`, `TotalRevenuet` | 📝 Typo |
| 24 | Uses `id` instead of `customer_id`; mismatch with "2 days" | ⚠️ Minor |
| 26 | Doesn't aggregate daily before cumulative sum | ⚠️ Minor |
| 32 | **Window function in WHERE clause — won't execute** | 🔴 **Critical** |
| 35 | Missing alias; no percentage calculation | ⚠️ Minor |

---

## 🔑 Key Concepts to Remember

### Window Functions
| Function | Behavior |
|----------|----------|
| `ROW_NUMBER()` | Unique sequential numbers, no ties |
| `RANK()` | Same rank for ties, **skips** next rank(s) |
| `DENSE_RANK()` | Same rank for ties, does **NOT** skip |
| `NTILE(n)` | Divides rows into `n` roughly equal groups |
| `LAG()` | Access previous row value |
| `LEAD()` | Access next row value |
| `PERCENT_RANK()` | Relative rank as a percentage (0 to 1) |

### Sargable vs Non-Sargable Queries
```sql
-- ❌ Non-Sargable (can't use index)
WHERE YEAR(hire_date) = 2023

-- ✅ Sargable (can use index)
WHERE hire_date >= '2023-01-01' AND hire_date < '2024-01-01'
```

### NULL Handling with NOT IN vs NOT EXISTS
```sql
-- ⚠️ Risky if subquery returns NULL
WHERE id NOT IN (SELECT id FROM table2)

-- ✅ Safe alternative
WHERE NOT EXISTS (SELECT 1 FROM table2 WHERE table2.id = table1.id)
```

---

## 📚 Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQL Server Documentation](https://docs.microsoft.com/en-us/sql/)
- [LeetCode SQL Problems](https://leetcode.com/problemset/database/)
- [HackerRank SQL](https://www.hackerrank.com/domains/sql)

---

## 🤝 Contributing

Feel free to submit a pull request if you'd like to:
- Add more questions
- Improve existing answers
- Add solutions for different SQL dialects
- Fix any errors

---

## ⭐ Star This Repo

If you found this helpful, please give it a ⭐ — it helps others find it too!

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> **Disclaimer:** These questions are commonly asked in interviews at the mentioned companies. The company names indicate where similar questions have been reported, not official endorsements.
```

---

## 📂 How to Use This in GitHub

### Step 1: Create the file
Save the above content as `SQL_Interview_Questions.md` or `README.md`

### Step 2: Repository structure
```
sql-interview-prep/
├── README.md          (paste the above content here)
├── LICENSE            (MIT License)
└── scripts/
    ├── easy/
    ├── medium/
    └── hard/
```

### Step 3: Git commands
```bash
mkdir sql-interview-prep
cd sql-interview-prep
git init
# Create README.md and paste the content
git add .
git commit -m "Add SQL interview questions with corrected answers"
git remote add origin https://github.com/YOUR_USERNAME/sql-interview-prep.git
git push -u origin main
```

This is a complete, ready-to-use `.md` file with proper formatting, table of contents, corrected answers, and all the interview tips included! 🚀
