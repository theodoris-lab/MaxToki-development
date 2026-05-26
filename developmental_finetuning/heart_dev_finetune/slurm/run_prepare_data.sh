#!/bin/bash
# =============================================================================
# run_prepare_data.sh — Stage 1: harmonise & split heart-dev source datasets
# =============================================================================
# Submits to ctbatch (CPU) partition.  No GPU needed.
# Expected wall-time: ~1–2 h depending on dataset sizes.
# =============================================================================
#SBATCH --job-name=hd26_prepare
#SBATCH --partition=ctbatch
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/prepare_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/prepare_%j.err

set -euo pipefail

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
CONDA_ENV="env_maxtoki"
PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${PIPELINE_DIR}/src"

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${CONDA_ENV}"

# ---------------------------------------------------------------------------
# Slack notification helper
# ---------------------------------------------------------------------------
source "${PIPELINE_DIR}/lib/slack_notify.sh"
notify_step_start "heart-dev Stage 1: prepare data (job ${SLURM_JOB_ID})"

trap 'notify_step_exit "heart-dev Stage 1" $?' EXIT

# ---------------------------------------------------------------------------
# Configurable overrides via environment variables
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
HARMONIZATION_MAP="${HARMONIZATION_MAP:-/gladstone/theodoris/home/eniyonkuru/maxtoki_development/cell_type_harmonization/cell_type_harmonization_map.json}"

echo "=== Heart-Dev Stage 1: prepare data ==="
echo "Data root:          ${DATA_ROOT}"
echo "Harmonization map:  ${HARMONIZATION_MAP}"
echo "SLURM job ID:       ${SLURM_JOB_ID:-local}"
echo "Date:               $(date)"

python "${SRC_DIR}/prepare_heart_dev_finetune_data.py" \
    --data-root "${DATA_ROOT}" \
    --harmonization-map "${HARMONIZATION_MAP}" \
    ${EXTRA_PREPARE_ARGS:-}

echo "Stage 1 complete: $(date)"
