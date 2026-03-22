# Row and Column-Level Security

## ✅ What you need to say in interview

- **Row-Level Security (RLS):** Filter rows by user/group. User sees only rows they're allowed (e.g., by region, tenant).
- **Column-Level Security (CLS):** Mask or hide columns (e.g., PII). Different users see different column values.
- **Implementation:** **Delta RLS** uses **filter functions** (return predicate). **CLS** uses **mask functions** or **column permissions** (restrict access entirely).
- **Use case:** Multi-tenant data; PII; regulatory (GDPR, HIPAA).

## ⚙️ How it actually works

1. RLS: Define filter function (e.g., `region = current_user_region()`). Attach to table. Spark rewrites queries to add filter.
2. CLS: Mask function returns value (e.g., mask for non-authorized). Or revoke SELECT on specific columns (where supported).
3. Filters apply at query time; transparent to user.

## ✅ When to use

- **RLS:** Multi-tenant (tenant_id filter); department/region isolation.
- **CLS:** PII (SSN, email); mask for analysts; full for authorized.
- Compliance requirements.

## ❌ When to NEVER use

- Don't implement RLS/CLS in application logic only—bypass risk. Use UC.
- Don't forget to test as different users.
- Avoid complex filters that hurt performance (pushdown).

## 🚩 Common interview pitfalls

- Confusing RLS (rows) with CLS (columns).
- Thinking RLS duplicates data (it doesn't—filter at read).
- Not knowing Delta RLS is available (Unity Catalog).

## 💻 Working example (SQL + PySpark)

```sql
-- RLS: filter function
CREATE FUNCTION region_filter(region STRING)
RETURN region = current_user_region();

ALTER TABLE orders SET ROW FILTER region_filter ON (region);

-- CLS: mask (simplified)
-- Use masking or column grants where supported
```

## ❔ Actual interview questions + ideal answers

**Q: What is Row-Level Security and when do you use it?**

- **Junior:** Filter rows by user. Use for multi-tenant or region.
- **Senior:** **RLS** restricts which **rows** a user sees via a **filter function**—e.g., `region = current_user_region()`. Attach to table; Spark rewrites queries to add the filter. Use for **multi-tenant** (tenant_id), **department/region** isolation, **compliance**. Transparent to users; enforced at query time. Delta RLS in Unity Catalog.

**Q: How does Column-Level Security differ from RLS?**

- **Junior:** RLS filters rows; CLS hides or masks columns.
- **Senior:** **RLS** filters **rows**—user sees subset of rows. **CLS** controls **columns**—mask (e.g., `***` for SSN) or revoke access entirely. Use CLS for **PII**—analysts see masked data; authorized users see full. RLS for tenant/region; CLS for column-level sensitivity.

---

## 5-Minute Revision Cheat Sheet

- RLS: filter rows by user.
- CLS: mask or hide columns.
- Filter/mask functions.
- Multi-tenant, PII, compliance.
