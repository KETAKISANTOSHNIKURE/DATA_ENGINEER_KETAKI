# 07 — Unity Catalog and Governance

**Interview weight:** High. Governance is key for enterprise.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | UC object model | Critical |
| 02 | Permissions, ownership | Critical |
| 03 | Row/column-level security | High |
| 04 | Lineage, audit | High |

## 5-Minute Revision Cheat Sheet

- **UC:** Catalog → Schema → Table. Metastore at top.
- **Grants:** SELECT, MODIFY, CREATE, USAGE, etc. Securable objects: catalog, schema, table, view, volume.
- **Ownership:** Owner has full control; can grant.
- **RLS/CLS:** Row/column filters; use for PII, multi-tenant.
- **Lineage:** Data flow; audit for compliance.
