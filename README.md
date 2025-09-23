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

## Discussion

This assignment was timeboxed to ~4 hours, so I made a few pragmatic tradeoffs:

- **Base image choice**:
  Rather than reading the documentation and building Bitcoin Core 29.0 entirely from scratch, I used a popular community-maintained Docker project to move faster while keeping reasonable security. I see this as a reasonable tradeoff for this assignment since I could have spent most (if not more) time on reading docs and having to figure out which libraries to include.

- **Filesystem paths vs. “sensible defaults”**:
  I followed the community image’s conventions (e.g., data/config under `/bitcoin`) instead of the assignment’s suggested defaults (`/var/lib/bitcoin` and `/etc/bitcoin/bitcoin.conf`).
  **If extending:** either adopt the suggested paths, add symlinks, or pass explicit flags (`-datadir`/`-conf`) and adjust entrypoint/manifests.

- **CI/CD scope**:
  Implemented a lean build → scan → deploy -> verify pipeline and skipped a richer release flow (e.g., `release-please`). There’s a known limitation where Minikube didn’t build-and-use the image locally. With more time, I’d add a local registry or `minikube image load`

Overall, the goal was to demonstrate working containerization, orchestration, and CI rather than full production hardening.

## Skipped Tasks

To keep within ~4 hours, I deliberately skipped:

- **Log analysis (shell, Task 4)**:
  Doing this by hand would have taken me too long so I focused on the general-purpose implementation and delivered the **Python CLI (Task 5)**

- **Terraform IAM module (optional, Task 6)**:
  Useful but out of scope given time—proper version pinning, tagging, idempotency, and outputs take non-trivial effort.

- **Nomad job (alternative to k8s, Task 7)**:
  I prioritized Kubernetes; a proper Nomad spec and validation would add setup and testing overhead.

These were deprioritized to focus on the core deliverables (image, k8s manifests, and CI pipeline).

## Sources

* https://minikube.sigs.k8s.io/docs/tutorials/setup_minikube_in_github_actions/
* https://github.com/kylemanna/docker-bitcoind
* https://github.com/aquasecurity/trivy-action

## AI Generated Parts

* Python Aggregator function + refactoring for test *NOT the CLI scaffold
* Sparring and checking for requirements
* Discussion
* README.md
