# Secrets Management

## ✅ What you need to say in interview

- **Secret scope:** Container for secrets. Can be **Databricks-backed** (workspace) or **Azure Key Vault / AWS Secrets Manager** linked.
- **Secret:** Key-value. Access via `dbutils.secrets.get(scope, key)`.
- **Best practice:** Never store secrets in code or notebooks. Use secrets; reference in code. Restrict scope access via ACLs.
- **Scoped access:** Grant scope access to groups/clusters; not all users need all secrets.

## ⚙️ How it actually works

1. Create scope (Databricks or link to Key Vault/Secrets Manager).
2. Store secrets (key-value). In Key Vault, secrets live there; scope is a reference.
3. In notebook: `dbutils.secrets.get("scope", "key")` returns value. Redacted in logs/UI.
4. Cluster needs access to scope to fetch secrets.

## ✅ When to use

- API keys, DB credentials, tokens.
- Any sensitive config.
- Different scopes for dev/prod.

## ❌ When to NEVER use

- Don't hardcode secrets.
- Don't print or log `dbutils.secrets.get` result.
- Don't store secrets in table properties or config files in repos.
- Don't grant broad scope access.

## 🚩 Common interview pitfalls

- Storing secrets in notebook parameters (visible in history).
- Not knowing scope can link to Key Vault/Secrets Manager.
- Confusing scope with key.

## 💻 Working example (SQL + PySpark)

```python
# Get secret
conn_string = dbutils.secrets.get(scope="kv-scope", key="sql-connection")
# Redacted in logs: [REDACTED]

# Spark config with secret
spark.conf.set("fs.azure.account.key...", dbutils.secrets.get("scope", "storage-key"))
```

```bash
# Create scope (CLI)
databricks secrets create-scope my-scope
databricks secrets put-secret my-scope my-key --string-value "xxx"
```

## ❔ Actual interview questions + ideal answers

**Q: How do you manage secrets in Databricks?**

- **Junior:** Use secret scopes and dbutils.secrets.get.
- **Senior:** Create a **secret scope** (Databricks-backed or linked to **Azure Key Vault / AWS Secrets Manager**). Store secrets as key-value. In code, use `dbutils.secrets.get(scope, key)`—value is **redacted** in logs. Restrict **scope ACLs** so only required groups/clusters can access. Never hardcode or log secrets. For cloud storage keys, use scope in Spark config or service principal where possible.

**Q: Why use Key Vault–linked scope vs Databricks-backed?**

- **Junior:** Key Vault for central management.
- **Senior:** **Key Vault / Secrets Manager** integration gives **centralized** secret management—same secrets for non-Databricks apps, audit, rotation. **Databricks-backed** scope is simpler for Databricks-only use. Enterprise often prefers Key Vault for compliance and unified governance.

---

## 5-Minute Revision Cheat Sheet

- Scope: container; can link Key Vault.
- dbutils.secrets.get(scope, key).
- Never log; redacted in UI.
- ACLs for scope access.
