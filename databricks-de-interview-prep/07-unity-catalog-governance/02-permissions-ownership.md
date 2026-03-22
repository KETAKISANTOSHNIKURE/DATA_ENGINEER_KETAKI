# Permissions and Ownership

## ✅ What you need to say in interview

- **Securable objects:** Metastore, catalog, schema, table, view, volume, function. **Permissions** apply at each level.
- **Key privileges:** **SELECT** (read), **MODIFY** (write, alter), **CREATE** (create children), **USAGE** (use catalog/schema), **ALL PRIVILEGES**.
- **Principals:** Users, groups, service principals.
- **Ownership:** Owner has full control; can grant to others. Transfer with `ALTER ... SET OWNER`.
- **Inheritance:** USAGE on parent (catalog, schema) required to access children.
- **Grant:** `GRANT SELECT ON catalog.schema.table TO group;`

## ⚙️ How it actually works

1. To access table: need USAGE on catalog, USAGE on schema, SELECT on table.
2. Grants can be at table, schema (applies to all in schema), or catalog.
3. Deny overrides grant (where supported).
4. Owner bypasses explicit grants.

## ✅ When to use

- Grant least privilege—only what's needed.
- Use groups, not individual users.
- Separate read vs write (SELECT vs MODIFY).
- Ownership for data ownership model.

## ❌ When to NEVER use

- Don't grant ALL PRIVILEGES broadly.
- Don't grant at metastore level unless intended.
- Avoid individual user grants when groups work.
- Don't forget USAGE on parent objects.

## 🚩 Common interview pitfalls

- Forgetting USAGE on catalog/schema.
- MODIFY vs CREATE—MODIFY = change data; CREATE = create new objects.
- Inheritance: child doesn't inherit parent grants; need explicit or schema-level.

## 💻 Working example (SQL + PySpark)

```sql
GRANT USAGE ON CATALOG prod TO `analytics-team`;
GRANT USAGE ON SCHEMA prod.silver TO `analytics-team`;
GRANT SELECT ON TABLE prod.silver.orders TO `analytics-team`;

GRANT MODIFY ON TABLE prod.silver.orders TO `etl-service-principal`;

-- Ownership
ALTER TABLE prod.silver.orders SET OWNER TO `data-engineers`;
```

## ❔ Actual interview questions + ideal answers

**Q: How do you grant read-only access to a table in Unity Catalog?**

- **Junior:** GRANT SELECT on the table. Also need USAGE on catalog and schema.
- **Senior:** Need **USAGE** on catalog and schema, and **SELECT** on table. Example: `GRANT USAGE ON CATALOG prod TO group; GRANT USAGE ON SCHEMA prod.silver TO group; GRANT SELECT ON TABLE prod.silver.orders TO group;` Use **groups** for manageability. For schema-wide read: `GRANT SELECT ON ALL TABLES IN SCHEMA prod.silver TO group;`

**Q: What is the difference between MODIFY and CREATE?**

- **Junior:** MODIFY is change; CREATE is create new.
- **Senior:** **MODIFY** allows **writing** to existing tables (insert, update, delete), altering table, dropping. **CREATE** allows **creating** new tables/views in the schema. A pipeline needs MODIFY on target table, CREATE on schema if creating new tables. Read-only users need only SELECT.

---

## 5-Minute Revision Cheat Sheet

- USAGE (catalog, schema) + SELECT (table).
- MODIFY = write; CREATE = create objects.
- Use groups; least privilege.
- Owner has full control.
