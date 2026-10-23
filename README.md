# PCForge

A PC build planner. Pick parts and it checks CPU socket, memory type, motherboard form factor,
GPU and cooler clearance, cooler mounting and PSU headroom. Built as the demo workload for an
EKS + Terraform + GitHub Actions + Argo CD pipeline.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
flask --app app run --port 8080          # http://localhost:8080
```

With Docker:

```bash
docker build --build-arg APP_VERSION=$(git rev-parse --short HEAD) -t pcforge .
docker run --rm -p 8080:8080 -e APP_ENV=local pcforge
```

## Endpoints

| Path | Purpose |
|---|---|
| `/` | UI |
| `/api/parts` | Catalog and presets |
| `POST /api/check` | `{"parts": {"cpu": "r7-7800x3d", ...}}` → status, issues, power, price |
| `/healthz` | Liveness: process is up |
| `/readyz` | Readiness: safe to receive traffic |
| `/metrics` | Prometheus metrics |
| `/version` | Version, environment, pod name |

Metrics: `pcforge_http_requests_total`, `pcforge_http_request_duration_seconds`,
`pcforge_build_checks_total{result}`, `pcforge_build_info{version,env}`.

## Layout

```
app/                 Flask app (compat.py holds the rules, pure functions)
tests/               pytest
Dockerfile           non-root, single gunicorn worker + threads
k8s/base/            Deployment + Service
k8s/overlays/dev/    1 replica, no Ingress (use port-forward)
k8s/overlays/prod/   3 replicas, PDB, ALB Ingress
```

Before deploying, replace `ACCOUNT_ID` and `REGION` in both overlays' `images:` block with your ECR repo.
CI updates `newTag` to the commit SHA; Argo CD picks up the change and rolls it out.

## Design choices worth knowing

- **Liveness vs readiness are separate.** Liveness only proves the process responds, so a slow
  dependency can never get pods restarted in a loop. Readiness controls whether the Service sends traffic.
- **`maxUnavailable: 0`, `maxSurge: 1`.** Rollouts add a new pod first and only remove an old one
  once the new pod passes readiness, so capacity never dips.
- **One gunicorn worker.** `prometheus_client` keeps counters in process memory; several workers
  would each report partial numbers. Scale horizontally with replicas instead.
- **Memory limit, no CPU limit.** Memory is incompressible, so it gets a hard limit. CPU limits cause
  CFS throttling and latency spikes; requests alone guarantee scheduling.
- **Hardened pod.** Non-root UID, read-only root filesystem (with an `emptyDir` for `/tmp`),
  all capabilities dropped, `RuntimeDefault` seccomp.
- **`target-type: ip` on the ALB.** The VPC CNI gives pods real VPC IPs, so the ALB targets pods
  directly instead of hopping through NodePorts.
- **Only prod has an Ingress.** Each Ingress creates an ALB that bills hourly; dev is reached with
  `kubectl -n pcforge-dev port-forward svc/pcforge 8080:80`.
- **Teardown order.** Delete the Ingress (or the prod Argo CD app) before `terraform destroy`,
  so the controller removes the ALB. Otherwise its ENIs and security groups block VPC deletion.

Prices in the catalog are illustrative sample prices in EUR.
