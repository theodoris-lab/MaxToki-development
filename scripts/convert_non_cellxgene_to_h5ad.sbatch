#!/usr/bin/env bash
#SBATCH --job-name=maxtoki_h5ad_convert
#SBATCH --cpus-per-task=4
#SBATCH --mem=128G
#SBATCH --time=72:00:00

set -Eeuo pipefail

REPO_DIR="/gladstone/theodoris/home/eniyonkuru/maxtoki_development"
PYTHON="/gladstone/theodoris/home/eniyonkuru/miniconda3/envs/env_maxtoki/bin/python"

cd "$REPO_DIR"
exec "$PYTHON" "$REPO_DIR/scripts/convert_non_cellxgene_to_h5ad.py" "$@"
