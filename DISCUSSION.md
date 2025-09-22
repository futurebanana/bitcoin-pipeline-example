# Trade-offs

Used community Docker image from:

https://github.com/kylemanna/docker-bitcoind

FROM ubuntu:latest is not minimal image

Sensible defailts /var/lib/bitcoin

29.0 != 29.1

healtcheck:

Local/dev & CI: docker run, docker compose, GitHub Actions, Docker Hub, etc. can surface health via docker ps without K8s.

Non-K8s runtimes: ECS, Nomad, Swarm, plain Docker hosts can use it.

Self-documenting: Encodes a canonical “is bitcoind up?” check right in the image.

Your acceptance criteria asked for a lightweight health check in the image.

# K8s

In practice for Bitcoin node

First time the PVC is mounted, Kubernetes will adjust ownership so that /bitcoin/.bitcoin is writable by GID 1000.
On subsequent pod restarts, if the PVC root dir is still GID 1000, Kubernetes won’t waste time re-chowning the entire blockchain directory.
That means faster restarts, and your non-root bitcoin user can still write blocks, wallets, etc.

using builtin health check for minikube

# Sources

https://minikube.sigs.k8s.io/docs/tutorials/setup_minikube_in_github_actions/
https://github.com/kylemanna/docker-bitcoind
