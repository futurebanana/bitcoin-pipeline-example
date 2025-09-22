# Bitcoin Pipeline Example

This repository contains an example pipeline for running a **Bitcoin Core node** in Docker/Kubernetes, with supporting CI/CD, pre-commit checks, and a small Python log analysis tool.

It is intended as a technical reference for:
- Building reproducible container images of Bitcoin Core
- Deploying to Kubernetes (tested with Minikube)
- Running automated scans with [Trivy](https://aquasecurity.github.io/trivy)
- Using pre-commit hooks for linting and conventions
- Simple Python scripting for log/IP aggregation

---

## Project Structure

```

.
├── docker/              # Dockerfile + entrypoint scripts for Bitcoin Core
├── orchestration/       # Example Kubernetes manifests (Minikube-focused)
├── scripts/             # Utility scripts (e.g., IP log counter)
├── .github/             # CI/CD workflows
├── .devcontainer/       # Devcontainer setup (VS Code, Docker, minikube, trivy)
├── Makefile             # Build, run, deploy automation
└── requirements.txt     # Python dependencies

````

---

## Prerequisites

- **Docker** (with Buildx support)
- **Python 3.11+**
- **kubectl** and **minikube** (for Kubernetes deployment)
- **trivy** (for image vulnerability scans)
- **pre-commit** (optional, for contributing)

If using [Dev Containers](https://containers.dev/), these dependencies are automatically installed by `.devcontainer/postCreateCommand.sh`.

---

## Build and Run with Docker

### Build image

```bash
make build
````

This will build the Bitcoin Core container image and tag it as:

* `karstenjakobsen/bitcoin-pipeline-example:<git-sha>`
* `karstenjakobsen/bitcoin-pipeline-example:latest`

### Run container

```bash
make run
```

This will:

* Create a `bitcoin_data` volume
* Start a Bitcoin Core node named `bitcoin-node`
* Expose ports `8332` (RPC) and `8333` (P2P)

Logs can be inspected with:

```bash
docker logs -f bitcoin-node
```

### Security scan

```bash
make scan
```

Runs a [Trivy](https://aquasecurity.github.io/trivy) scan on the local image and fails on `HIGH` or `CRITICAL` findings.

---

## Kubernetes Deployment (Minikube)

> The manifests in `orchestration/` are **examples only**.
> They provide a minimal deployment suitable for local clusters (e.g. Minikube).

Deploy:

```bash
make deploy
```

Tear down:

```bash
make down
```

This deploys:

* `Deployment`: one Bitcoin node container
* `Service`: exposes RPC/P2P ports inside the cluster
* `PersistentVolumeClaim`: stores blockchain data
* Basic `NetworkPolicies`

---

## Python Log Analyzer (`ipcount.py`)

The script in `scripts/ipcount.py` extracts and counts IPv4 addresses from logs. It can read from stdin or from a file.

### Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

Basic example (count IPs from `example.log`):

```bash
python scripts/ipcount.py -f scripts/example.log
```

Output:

```
4 10.32.89.34
2 10.0.0.1
1 121.89.25.43
1 172.16.0.5
1 172.32.9.12
1 192.168.22.11
```

### Options

* `--file, -f` : input file (default: stdin)
* `--top N` : show only the top N IPs (default: all)
* `--sort {count,ip}` : sort by frequency or by IP
* `--strict/--no-strict` : enforce valid IPv4 octets (0–255)

#### Example: Top 3 IPs, sorted by count

```bash
python scripts/ipcount.py -f scripts/example.log --top 3 --sort count
```

#### Example: Strict validation, sorted by IP

```bash
cat scripts/example.log | python scripts/ipcount.py --strict --sort ip
```

---

## Development

### Pre-commit hooks

Install hooks:

```bash
pre-commit install
```

This enforces:

* No trailing whitespace
* No merge conflicts
* Shellcheck linting
* Python linting (flake8)
* Commit message conventions

### Run tests

```bash
pytest scripts/test_ipcount.py
```

---

## CI/CD

* **CI Entrypoint (`ci.yaml`)**

  * Build Docker image with Buildx
  * Scan with Trivy
  * Deploy to Minikube and verify readiness

* **Linters (`linters.yaml`)**

  * Check PR titles against conventions
  * Run pre-commit hooks
