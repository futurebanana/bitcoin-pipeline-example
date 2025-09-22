# Variables
VERSION ?= $(shell git rev-parse --short HEAD)
TAG ?= devel-$(VERSION)
DOCKER_FILE ?= Dockerfile
IMAGE_PREFIX ?= bitcoin-pipeline-example

# Default target
.PHONY: all
all: build volume scan run

# Build Docker images for all services
.PHONY: build
build:
	@echo "Building Docker image ..."
	cd docker/ && docker build -t $(IMAGE_PREFIX):$(TAG) .

.PHONY:	volume
volume:
	docker volume create bitcoin_data || true

.PHONY: run
run:
	@echo "Running Docker container ..."
	docker run --rm -d --name bitcoin-node \
	-p 8332:8332 -p 8333:8333 \
	-v bitcoin_data:/bitcoin/.bitcoin \
	$(IMAGE_PREFIX):$(TAG)

.PHONY: scan
scan:
	trivy image --severity HIGH,CRITICAL $(IMAGE_PREFIX):$(TAG)
