Python is the glue language for DevOps and Site Reliability Engineering (SRE)—bridging the gap where Bash scripts become too fragile and full-blown microservices are overkill. It excels at interacting with REST APIs, automating container/Kubernetes lifecycles, parsing structured logs or YAML/JSON configs, and executing repetitive operational runbooks safely.

---

### Core DevOps Automation Domains & Key Python Libraries

| Domain | Primary Libraries | Common Automation Tasks |
| --- | --- | --- |
| **Containers & Orchestration** | `docker` (Docker SDK for Python), `kubernetes` | Cleaning up dangling images, inspecting container health, automating `kind`/cluster deployments, watching Pod events. |
| **CI/CD & GitOps APIs** | `requests`, `httpx`, `PyGithub`, `python-gitlab` | Triggering Jenkins/GitLab pipelines, checking commit statuses, automating release tags, pruning stale branches. |
| **Infrastructure & Cloud** | `boto3` (AWS), `google-cloud-*` (GCP), `paramiko` / `fabric` | Provisioning cloud resources, rotating IAM keys, running SSH health checks across Linux hosts. |
| **Config & Data Parsing** | `PyYAML`, `pydantic`, `json`, `re` | Validating Kubernetes manifests and `docker-compose.yml` files before deployment, parsing structured logs. |
| **CLI Tooling & Scheduling** | `typer` / `click`, `subprocess`, `rich` | Turning ad-hoc operational scripts into clean, self-documenting internal CLI tools with exit-code handling. |

---

### Practical Example 1: Automating Docker Hygiene & Health Checks (Docker SDK)

Instead of chaining `grep` and `awk` around `docker ps`, the official `docker` SDK gives you structured objects and proper error handling. In your Ubuntu 24.04 environment (where `hua` is already in the `docker` group), this script audits running containers and prunes unused images:

---

### Practical Example 2: Kubernetes Pod Health Watcher (`kubernetes` Client)

When managing multi-node clusters (like your local `kind` clusters), Python can monitor namespaces for crashing or pending pods and surface actionable diagnostics automatically:

---

### Practical Example 3: Triggering & Polling a Jenkins Build via REST API

You can integrate Python directly into your CI/CD workflow—for instance, triggering a Jenkins job via its REST API and blocking until the build succeeds or fails (useful for release scripts or pre-deploy checks):

---

### Best Practices for Production-Grade DevOps Scripts

* **Always enforce timeouts on network calls:** Never call `requests.get(url)` without `timeout=...`—an unresponsive internal API can hang a CI/CD worker indefinitely.
* **Use `subprocess.run(..., check=True)` instead of `os.system`:** Passing arguments as a list (`["git", "status"]`) prevents shell-injection bugs, and `check=True` immediately raises `CalledProcessError` on non-zero exit codes.
* **Design for idempotency:** Ensure running the same script twice produces the exact same end state without duplicating resources or crashing if a container/file already exists.
* **Return meaningful exit codes:** Exit with `0` on success and non-zero (`sys.exit(1)`) on operational failure so Jenkins, GitLab CI, or cron jobs immediately detect broken runs.