#!/bin/bash
# =============================================================================
# run_build_trajectories.sh — Stage 2: build MaxToki paragraph trajectories
# =============================================================================
# Submits to ctbatch (CPU) partition.  No GPU needed.
# Expected wall-time: ~2–4 h for 500K train trajectories.
# =============================================================================
#SBATCH --job-name=hd26_traj
#SBATCH --partition=ctbatch
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/traj_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/traj_%j.err

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
notify_step_start "heart-dev Stage 2: build trajectories (job ${SLURM_JOB_ID})"

trap 'notify_step_exit "heart-dev Stage 2" $?' EXIT

# ---------------------------------------------------------------------------
# Configurable overrides via environment variables
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
TOKEN_DICT="${TOKEN_DICT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl}"
TRAIN_EXAMPLES="${TRAIN_EXAMPLES:-500000}"
VAL_EXAMPLES="${VAL_EXAMPLES:-25000}"
TEST_EXAMPLES="${TEST_EXAMPLES:-10000}"

echo "=== Heart-Dev Stage 2: build trajectories ==="
echo "Data root:       ${DATA_ROOT}"
echo "Token dict:      ${TOKEN_DICT}"
echo "Train examples:  ${TRAIN_EXAMPLES}"
echo "Val examples:    ${VAL_EXAMPLES}"
echo "Test examples:   ${TEST_EXAMPLES}"
echo "SLURM job ID:    ${SLURM_JOB_ID:-local}"
echo "Date:            $(date)"

python "${SRC_DIR}/build_heart_dev_trajectories.py" \
    --data-root "${DATA_ROOT}" \
    --token-dictionary "${TOKEN_DICT}" \
    --max-train-examples "${TRAIN_EXAMPLES}" \
    --max-val-examples "${VAL_EXAMPLES}" \
    --max-test-examples "${TEST_EXAMPLES}" \
    ${EXTRA_TRAJ_ARGS:-}

echo "Stage 2 complete: $(date)"
