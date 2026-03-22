# Unity Catalog Object Model

## ✅ What you need to say in interview

- **Unity Catalog (UC):** Unified **governance** layer for data and AI assets across workspaces.
- **Hierarchy:** **Metastore** (top level) → **Catalog** → **Schema** → **Table/View/Volume**. Three-level namespace: `catalog.schema.table`.
- **Metastore:** Contains catalogs; attached to workspaces. One metastore per region/account typically.
- **Catalog:** Container for schemas. E.g., `hive_metastore` (legacy) or custom `prod`, `dev`.
- **Schema:** Container for tables, views, functions.
- **Volume:** Directory for unstructured data (files).

## ⚙️ How it actually works

- UC replaces Hive metastore for governed tables.
- All access goes through UC—permissions, audit.
- External locations and storage credentials link cloud storage to UC.
- `USE CATALOG x; USE SCHEMA y;` or `catalog.schema.table`.

## ✅ When to use

- All new tables in UC catalogs for governance.
- Separate catalogs for dev/prod.
- Schemas for logical grouping (e.g., bronze, silver, gold).

## ❌ When to NEVER use

- Don't mix UC and legacy metastore without migration plan.
- Don't put sensitive data in ungoverned locations.
- Avoid deeply nested schemas—keep simple.

## 🚩 Common interview pitfalls

- Confusing metastore with catalog.
- Not knowing three-level naming: catalog.schema.table.
- Volume vs table (volume = files; table = structured data).

## 💻 Working example (SQL + PySpark)

```sql
CREATE CATALOG IF NOT EXISTS prod;
CREATE SCHEMA IF NOT EXISTS prod.silver;
CREATE TABLE prod.silver.orders (id INT, amount DOUBLE);

-- Use
USE CATALOG prod;
SELECT * FROM silver.orders;
```

```python
spark.sql("CREATE TABLE prod.silver.orders ...")
df = spark.table("prod.silver.orders")
```

## ❔ Actual interview questions + ideal answers

**Q: What is Unity Catalog and its object model?**

- **Junior:** Unity Catalog is governance. Catalog, schema, table.
- **Senior:** **Unity Catalog** is the **unified governance** layer—permissions, audit, lineage. **Object model:** **Metastore** (top) → **Catalog** → **Schema** → **Table/View/Volume**. Three-level name: `catalog.schema.table`. **Metastore** is attached to workspaces; **catalog** holds schemas; **schema** holds tables. **Volume** for unstructured files. Replaces Hive metastore for governed data.

**Q: What is the difference between catalog and schema?**

- **Junior:** Catalog is bigger; schema holds tables.
- **Senior:** **Catalog** is the top-level container—holds multiple **schemas**. Use catalogs for environments (dev, prod) or domains. **Schema** holds **tables, views, functions**. Typical use: `prod.silver.orders` = catalog prod, schema silver, table orders. Schema is like a database in legacy terms.

---

## 5-Minute Revision Cheat Sheet

- Metastore → Catalog → Schema → Table.
- catalog.schema.table.
- Volume for files.
- UC = governance layer.
