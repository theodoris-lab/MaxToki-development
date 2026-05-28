#!/bin/bash
# =============================================================================
# run_tokenize.sh — Pre-Stage 0: tokenize heart-dev source h5ads
# =============================================================================
# Tokenizes CXG (14 h5ads) and Xu (organogenesis_processed.h5ad) into
# HuggingFace .dataset files under $DATA_ROOT/tokenized/.
#
# Tyser is already tokenized (E-MTAB-9388.dataset) — skipped here.
# Lázár is R-object only — skipped until h5ad is prepared.
#
# This job runs on ctbatch (CPU-only); tokenization is memory-bound,
# not GPU-bound.
#
# Run this BEFORE submit_finetune_pipeline.sh.
# =============================================================================
#SBATCH --job-name=hd26_tokenize
#SBATCH --partition=ctbatch
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=192G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/tokenize_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/tokenize_%j.err

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
notify_step_start "heart-dev Stage 0: tokenize sources (job ${SLURM_JOB_ID})"

trap 'notify_step_exit "heart-dev Stage 0" $?' EXIT

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
TOKEN_DICT="${TOKEN_DICT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl}"
XU_H5AD="${XU_H5AD:-/gladstone/theodoris/lab/dwen/data/organogenesis_data/organogenesis/organogenesis_processed.h5ad}"
NPROC="${NPROC:-16}"
MODEL_INPUT_SIZE="${MODEL_INPUT_SIZE:-16384}"
OVERWRITE="${OVERWRITE:-}"   # set to --overwrite to re-tokenize existing datasets

echo "========================================"
echo " Heart-dev tokenization"
echo " DATA_ROOT       : ${DATA_ROOT}"
echo " TOKEN_DICT      : ${TOKEN_DICT}"
echo " XU_H5AD         : ${XU_H5AD}"
echo " NPROC           : ${NPROC}"
echo " MODEL_INPUT_SIZE: ${MODEL_INPUT_SIZE}"
echo "========================================"

python "${SRC_DIR}/tokenize_heart_dev_sources.py" \
    --data-root "${DATA_ROOT}" \
    --token-dict "${TOKEN_DICT}" \
    --xu-h5ad "${XU_H5AD}" \
    --sources cxg xu \
    --nproc "${NPROC}" \
    --model-input-size "${MODEL_INPUT_SIZE}" \
    ${OVERWRITE:+--overwrite}

echo ""
echo "Tokenization complete. Tokenized datasets written to:"
echo "  ${DATA_ROOT}/tokenized/"
