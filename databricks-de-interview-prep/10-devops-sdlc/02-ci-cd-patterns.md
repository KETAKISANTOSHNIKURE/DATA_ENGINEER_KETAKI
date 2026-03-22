# CI/CD Patterns

## ✅ What you need to say in interview

- **CI:** **Build** and **test** on commit/PR. Run unit tests, lint, integration tests.
- **CD:** **Deploy** to Databricks on merge. Push jobs, notebooks, config. Use **Jobs API** or **Databricks Asset Bundles (DAB)**.
- **Pattern:** GitHub Actions / Azure DevOps / Jenkins → run tests → deploy via Databricks API (Create/Reset Job, Repos update).
- **Testing:** Unit tests (pytest) for logic; integration tests on dev cluster; validate job runs.

## ⚙️ How it actually works

1. Dev pushes to branch; CI runs (lint, unit tests).
2. PR triggers CI; merge to main triggers CD.
3. CD: authenticate to Databricks (token/SPN); call Jobs API or deploy bundle; update job config, notebooks.
4. Jobs reference repo path or bundled assets.
5. Run job to validate deployment.

## ✅ When to use

- All production pipelines.
- Automated deployment.
- Catch bugs before prod.

## ❌ When to NEVER use

- Don't deploy to prod without tests.
- Don't store Databricks token in plain text—use secrets (GitHub Secrets, Azure Key Vault).
- Avoid manual deploy for production.
- Don't skip validation run after deploy.

## 🚩 Common interview pitfalls

- No testing before deploy.
- Token management (rotate, least privilege).
- Job config in code vs UI (prefer code for reproducibility).

## 💻 Working example (SQL + PySpark)

```yaml
# GitHub Actions
- run: pytest tests/
- name: Deploy to Databricks
  env:
    DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
    DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
  run: |
    databricks jobs create --json-file job_config.json
    # Or: databricks bundle deploy -t prod
```

## ❔ Actual interview questions + ideal answers

**Q: How do you implement CI/CD for Databricks?**

- **Junior:** Use GitHub Actions; run tests; deploy jobs via API.
- **Senior:** **CI:** On PR/commit, run **pytest** for unit tests, **lint**. **CD:** On merge to main, **authenticate** to Databricks (token in secrets), use **Jobs API** to create/update jobs or **Databricks Asset Bundles** to deploy. Jobs reference **repo path** or bundled notebooks. Run **smoke test** (trigger job, check success). Use **service principal** for prod; rotate tokens. Store config as code (JSON/YAML) in repo.

**Q: What is Databricks Asset Bundles?**

- **Junior:** A way to deploy Databricks assets as code.
- **Senior:** **DAB** (Databricks Asset Bundles) defines **jobs, notebooks, config** as **YAML/files** in a bundle. Deploy with `databricks bundle deploy -t prod`. Supports **targets** (dev, prod)—different clusters, config per env. **CI/CD** runs `bundle deploy` on merge. Reproducible, versioned deployments. Alternative to Jobs API for full-stack deployment.

---

## 5-Minute Revision Cheat Sheet

- CI: test on PR.
- CD: deploy on merge.
- Jobs API or DAB.
- Secrets for tokens.
- Smoke test after deploy.
