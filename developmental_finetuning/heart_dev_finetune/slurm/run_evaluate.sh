#!/bin/bash
# =============================================================================
# run_evaluate.sh — Stage 4: evaluate a fine-tuned heart-dev MaxToki model
# =============================================================================
# Production run on ctbatch.  Uses 1× A100 GPU.
# Expected wall-time: ~1–2 h for 10K examples.
# =============================================================================
#SBATCH --job-name=hd26_eval
#SBATCH --partition=ctbatch
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:A100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/eval_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/eval_%j.err

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
notify_step_start "heart-dev Stage 4: evaluation (job ${SLURM_JOB_ID})"

trap 'notify_step_exit "heart-dev Stage 4" $?' EXIT

# ---------------------------------------------------------------------------
# Configurable overrides via environment variables
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
TOKEN_DICT="${TOKEN_DICT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl}"
FOUNDATIONAL_MODEL="${FOUNDATIONAL_MODEL:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/foundational_94M_model}"
MODEL_OUTPUT_ROOT="${MODEL_OUTPUT_ROOT:-${DATA_ROOT}/finetuning_heart_dev/model}"

# Resolve model safetensors: explicit path wins, otherwise use latest_final_model_dir.txt
MODEL_SAFETENSORS="${MODEL_SAFETENSORS:-}"
if [[ -z "${MODEL_SAFETENSORS}" ]]; then
    LATEST_FILE="${MODEL_OUTPUT_ROOT}/latest_final_model_dir.txt"
    if [[ -f "${LATEST_FILE}" ]]; then
        MODEL_DIR="$(cat "${LATEST_FILE}")"
        MODEL_SAFETENSORS="${MODEL_DIR}/model.safetensors"
        echo "Auto-resolved model: ${MODEL_SAFETENSORS}"
    fi
fi

EVAL_DATASET="${EVAL_DATASET:-${DATA_ROOT}/finetuning_heart_dev/trajectories/val/val_heart_dev_masked.dataset}"
EVAL_OUTPUT="${EVAL_OUTPUT:-${DATA_ROOT}/finetuning_heart_dev/evaluation}"
MAX_EXAMPLES="${MAX_EXAMPLES:-10000}"
EVAL_SPLIT="${EVAL_SPLIT:-val}"  # informational label only

echo "=== Heart-Dev Stage 4: evaluation ==="
echo "Eval split:      ${EVAL_SPLIT}"
echo "Dataset:         ${EVAL_DATASET}"
echo "Model:           ${MODEL_SAFETENSORS:-<auto-resolve>}"
echo "Output:          ${EVAL_OUTPUT}"
echo "Max examples:    ${MAX_EXAMPLES}"
echo "SLURM job ID:    ${SLURM_JOB_ID:-local}"
echo "Date:            $(date)"

SAFETENSORS_ARGS=()
if [[ -n "${MODEL_SAFETENSORS}" ]]; then
    SAFETENSORS_ARGS=(--model-safetensors "${MODEL_SAFETENSORS}")
fi

python "${SRC_DIR}/evaluate_heart_dev.py" \
    --dataset "${EVAL_DATASET}" \
    "${SAFETENSORS_ARGS[@]}" \
    --model-output-root "${MODEL_OUTPUT_ROOT}" \
    --foundational-model "${FOUNDATIONAL_MODEL}" \
    --token-dictionary "${TOKEN_DICT}" \
    --output-dir "${EVAL_OUTPUT}" \
    --max-examples "${MAX_EXAMPLES}" \
    --bf16 \
    ${EXTRA_EVAL_ARGS:-}

echo "Stage 4 complete: $(date)"
