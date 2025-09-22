#!/bin/bash
set -e

sudo apt-get update && sudo apt-get install -y shellcheck

pip3 install -r requirements.txt

pre-commit install

echo "Welcome to the jungle..."
