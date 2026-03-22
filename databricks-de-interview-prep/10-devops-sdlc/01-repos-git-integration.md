# Repos and Git Integration

## ✅ What you need to say in interview

- **Repos:** Databricks **Git integration**. Sync workspace folders with **Git** (GitHub, Azure DevOps, Bitbucket). **Branch**, **PR**, **merge**.
- **Use:** Version control for notebooks, config. **CI/CD**—deploy from repo. **Collaboration**—branch per feature.
- **Sync:** Repo folder in workspace mirrors remote. Push/pull, or auto-sync.
- **Notebooks as files:** Stored as source (JSON) in Git; diffable.

## ⚙️ How it actually works

1. Create repo in workspace; link to remote Git.
2. Clone or link; folder syncs with branch.
3. Edit in workspace or locally; push to Git.
4. CI/CD can pull from repo and deploy.
5. Branch workflows: create branch, develop, PR, merge to main.

## ✅ When to use

- All production code—version control.
- CI/CD pipelines (trigger from Git).
- Team collaboration (branch, review).
- Reproducibility (tag = release).

## ❌ When to NEVER use

- Don't store secrets in repos.
- Don't commit large files or data.
- Avoid editing same notebook in workspace and Git without sync—conflicts.
- Don't skip PR process for production.

## 🚩 Common interview pitfalls

- Repos vs workspace files—Repos = Git-backed.
- Conflict resolution (workspace vs Git).
- Not knowing notebooks are JSON in Git.

## 💻 Working example (SQL + PySpark)

```
# Repo structure
/repo
  notebooks/
    bronze_ingest.py
    silver_transform.py
  conf/
    config.yml
# Git: push, PR, merge to main
# CI: on merge, run tests, deploy
```

## ❔ Actual interview questions + ideal answers

**Q: What is Databricks Repos and why use it?**

- **Junior:** Git integration for notebooks. Version control and collaboration.
- **Senior:** **Repos** integrates **Git** with the workspace. Sync notebooks and config with GitHub/Azure DevOps. Enables **branching**, **PRs**, **version control**. Use for **CI/CD**—deploy from repo on merge. Notebooks stored as source (JSON) in Git—diffable. Essential for **production** code and **reproducibility** (tag = release).

**Q: How do you handle multiple environments with Repos?**

- **Junior:** Different branches or repos per env.
- **Senior:** Use **branches** (main=prod, dev=staging) or **folders** per env. **Deploy** from branch—CI runs on merge to main, deploys to prod. Or use **Databricks Asset Bundles** with targets (dev, prod). **Secrets** and **cluster config** differ per env—use workspace-specific config or deployment variables. Same code; different targets.

---

## 5-Minute Revision Cheat Sheet

- Repos = Git in workspace.
- Branch, PR, sync.
- CI/CD from repo.
- No secrets in repo.
