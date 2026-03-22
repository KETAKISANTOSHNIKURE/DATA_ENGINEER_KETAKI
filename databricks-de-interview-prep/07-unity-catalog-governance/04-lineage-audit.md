# Lineage and Audit

## ✅ What you need to say in interview

- **Lineage:** Tracks **data flow**—which tables feed which. Upstream (sources) and downstream (consumers). Used for impact analysis, debugging, compliance.
- **Audit:** **Who** accessed **what**, **when**. Logs for compliance (SOC2, GDPR).
- **Unity Catalog:** Lineage captured for tables, notebooks, jobs. Audit logs in cloud (e.g., Azure Monitor, CloudWatch) or Databricks audit log.
- **Use:** Impact analysis before schema change; compliance reporting; debugging data issues.

## ⚙️ How it actually works

1. Lineage: Spark/Databricks capture reads and writes; build graph. Available in UC UI and APIs.
2. Audit: Every access (query, table read) logged with user, timestamp, object. Export to SIEM or log store.
3. Retention per compliance needs.

## ✅ When to use

- Before dropping/altering tables—check downstream.
- Compliance audits—who accessed PII.
- Debugging—trace data origin.
- Data catalog integration.

## ❌ When to NEVER use

- Don't ignore lineage when making breaking changes.
- Don't skip audit log retention for regulated data.
- Avoid storing audit logs only in Databricks—export for long-term.

## 🚩 Common interview pitfalls

- Lineage vs audit—lineage = flow; audit = access log.
- Lineage can have gaps (e.g., some notebook runs).
- Audit logs are workspace/account level—configure export.

## 💻 Working example (SQL + PySpark)

```sql
-- Lineage: automatic when using UC tables
-- View in Databricks: Data → Table → Lineage tab

-- Audit: configure in account/workspace settings
-- Export to S3, Azure Log Analytics, etc.
```

## ❔ Actual interview questions + ideal answers

**Q: What is data lineage and why is it important?**

- **Junior:** Lineage shows where data comes from and goes. Important for impact analysis.
- **Senior:** **Lineage** tracks **data flow**—upstream sources and downstream consumers. Important for: (1) **Impact analysis**—before altering a table, see what breaks. (2) **Debugging**—trace bad data to source. (3) **Compliance**—demonstrate data provenance. Unity Catalog captures lineage for tables, notebooks, jobs. Use before schema changes or table drops.

**Q: How do you use audit logs in Databricks?**

- **Junior:** Audit logs show who accessed what. Export for compliance.
- **Senior:** **Audit logs** record **who** accessed **what** (tables, notebooks) and **when**. Required for **compliance** (SOC2, GDPR). Configure **export** to cloud (S3, Azure Monitor, CloudWatch) for retention and SIEM. Use for access reviews, incident investigation. Unity Catalog and workspace actions are logged. Retain per policy.

---

## 5-Minute Revision Cheat Sheet

- Lineage: data flow; upstream/downstream.
- Audit: who, what, when.
- Impact analysis before changes.
- Export audit for compliance.
