#!/usr/bin/env bash
#SBATCH --job-name=maxtoki_data_download
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=24:00:00

set -Eeuo pipefail

REPO_DIR="/gladstone/theodoris/home/eniyonkuru/maxtoki_development"
cd "$REPO_DIR"

exec "$REPO_DIR/scripts/download_datasets.sh" "$@"
