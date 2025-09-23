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

https://minikube.sigs.k8s.io/docs/tutorials/setup_minikube_in_github_actions/
https://github.com/kylemanna/docker-bitcoind

## AI Generated Parts

* Python Aggregator function + refactoring for test *NOT the CLI scaffold
* Sparring and checking for requirements
* Discussion
