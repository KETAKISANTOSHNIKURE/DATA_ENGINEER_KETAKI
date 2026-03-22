# Environment Promotion

## ✅ What you need to say in interview

- **Environments:** **Dev** → **Staging** → **Prod**. Separate **catalogs**, **clusters**, **secrets**, **storage**.
- **Promotion:** Move **code** (and optionally **data**) from dev to prod. Code via Git (merge). Data: backfill or copy.
- **Config per env:** Use **variables** (widgets, bundle targets) for catalog name, cluster ID, secret scope. Same code; different config.
- **Validation:** Test in staging before prod. Run same jobs; compare results or validate schema.

## ⚙️ How it actually works

1. Dev: develop in dev catalog, dev cluster. Branch in Repos.
2. Staging: merge to staging branch; deploy to staging workspace/target. Run full pipeline; validate.
3. Prod: merge to main; deploy to prod. Use prod catalog, prod secrets, prod cluster.
4. Databricks Asset Bundles: define targets (dev, prod) with different configs.

## ✅ When to use

- All production pipelines.
- Isolate dev from prod.
- Validate before prod.

## ❌ When to NEVER use

- Don't develop directly in prod.
- Don't share prod credentials with dev.
- Avoid promoting without staging validation.
- Don't hardcode env-specific values in code.

## 🚩 Common interview pitfalls

- Same catalog for dev and prod—data pollution.
- No validation gate (staging) before prod.
- Secrets: different scopes per env.

## 💻 Working example (SQL + PySpark)

```python
# Config by env
env = dbutils.widgets.get("env", "dev")
catalog = "dev_catalog" if env == "dev" else "prod_catalog"
table = f"{catalog}.silver.orders"
```

```yaml
# DAB targets
targets:
  dev:
    catalog: dev_catalog
    cluster_id: dev-cluster
  prod:
    catalog: prod_catalog
    cluster_id: prod-cluster
```

## ❔ Actual interview questions + ideal answers

**Q: How do you promote from dev to prod in Databricks?**

- **Junior:** Use different catalogs and clusters. Promote code via Git.
- **Senior:** **Code:** Develop in dev branch; **PR** to main; **merge** triggers CD; deploy to prod. **Config:** Use **catalog**, **cluster**, **secret scope** per env—variables or DAB targets. **Data:** Prod has own data; backfill or incremental load. **Validation:** Run pipeline in **staging**; validate schema, row counts; then promote. **Secrets:** Different scope per env; prod scope has prod credentials.

**Q: What config differs between dev and prod?**

- **Junior:** Catalog, cluster, secrets.
- **Senior:** **Catalog** (dev vs prod), **cluster** (smaller dev, larger prod), **secret scope** (dev vs prod credentials), **storage paths** (dev bucket vs prod bucket), **job schedule** (dev manual, prod cron). Use **variables** or **bundle targets** so code is identical; only config differs. Never hardcode env-specific values.

---

## 5-Minute Revision Cheat Sheet

- Dev → Staging → Prod.
- Separate catalog, cluster, secrets.
- Promote via Git merge.
- Validate in staging.
- Config via variables/targets.
