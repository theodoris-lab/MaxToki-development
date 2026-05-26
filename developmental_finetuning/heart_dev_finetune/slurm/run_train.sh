#!/bin/bash
# =============================================================================
# run_train.sh — Stage 3: fine-tune MaxToki on heart-development trajectories
# =============================================================================
# Submits to pod partition.  Uses DeepSpeed ZeRO-3 + BF16 on H200 GPUs.
# Requires 4–8 GPUs for the default batch configuration (GAS=256).
# =============================================================================
#SBATCH --job-name=hd26_train
#SBATCH --partition=pod
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:H200:4
#SBATCH --cpus-per-task=8
#SBATCH --mem=320G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/train_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/train_%j.err

set -euo pipefail

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
CONDA_ENV="env_maxtoki"
PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${PIPELINE_DIR}/src"
DS_CONFIG="${PIPELINE_DIR}/config/ds_config_zero3_bf16.json"

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${CONDA_ENV}"

# ---------------------------------------------------------------------------
# Slack notification helper
# ---------------------------------------------------------------------------
source "${PIPELINE_DIR}/lib/slack_notify.sh"
notify_step_start "heart-dev Stage 3: training (job ${SLURM_JOB_ID}, ${SLURM_NTASKS} GPUs)"

trap 'notify_step_exit "heart-dev Stage 3" $?' EXIT

# ---------------------------------------------------------------------------
# NCCL / distributed training settings
# ---------------------------------------------------------------------------
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export NCCL_IB_DISABLE="${NCCL_IB_DISABLE:-0}"
export NCCL_NET_GDR_LEVEL="${NCCL_NET_GDR_LEVEL:-2}"
export MASTER_PORT="${MASTER_PORT:-29500}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-8}"

# ---------------------------------------------------------------------------
# Configurable overrides via environment variables
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
TOKEN_DICT="${TOKEN_DICT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl}"
FOUNDATIONAL_MODEL="${FOUNDATIONAL_MODEL:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/foundational_94M_model}"
PRIOR_SAFETENSORS="${PRIOR_SAFETENSORS:-}"  # empty = first round, start from foundational model
OUTPUT_DIR="${OUTPUT_DIR:-${DATA_ROOT}/finetuning_heart_dev/model}"
TRAIN_DATASET="${TRAIN_DATASET:-${DATA_ROOT}/finetuning_heart_dev/trajectories/train/train_heart_dev_masked.dataset}"
VAL_DATASET="${VAL_DATASET:-${DATA_ROOT}/finetuning_heart_dev/trajectories/val/val_heart_dev_masked.dataset}"
MAX_TRAIN="${MAX_TRAIN:-500000}"
MAX_VAL="${MAX_VAL:-10000}"
EPOCHS="${EPOCHS:-1}"
GAS="${GAS:-256}"
LR="${LR:-0.00016}"
WARMUP="${WARMUP:-0.007}"
WD="${WD:-0.044}"
FREEZE_LAYERS="${FREEZE_LAYERS:-0}"
DO_EVAL="${DO_EVAL:-}"  # set to --do-eval to enable mid-training eval

echo "=== Heart-Dev Stage 3: training ==="
echo "Data root:            ${DATA_ROOT}"
echo "Train dataset:        ${TRAIN_DATASET}"
echo "Val dataset:          ${VAL_DATASET}"
echo "Prior safetensors:    ${PRIOR_SAFETENSORS:-<none, using foundational model>}"
echo "Output dir:           ${OUTPUT_DIR}"
echo "Max train examples:   ${MAX_TRAIN}"
echo "Max val examples:     ${MAX_VAL}"
echo "Epochs:               ${EPOCHS}"
echo "Gradient accum steps: ${GAS}"
echo "Learning rate:        ${LR}"
echo "GPUs:                 ${SLURM_NTASKS}"
echo "SLURM job ID:         ${SLURM_JOB_ID:-local}"
echo "Date:                 $(date)"

# Build optional prior-safetensors argument
PRIOR_ARGS=()
if [[ -n "${PRIOR_SAFETENSORS}" ]]; then
    PRIOR_ARGS=(--prior-model-safetensors "${PRIOR_SAFETENSORS}")
fi

deepspeed \
    --num_gpus "${SLURM_NTASKS}" \
    "${SRC_DIR}/finetune_heart_dev.py" \
    --train-dataset "${TRAIN_DATASET}" \
    --val-dataset "${VAL_DATASET}" \
    --token-dictionary "${TOKEN_DICT}" \
    --foundational-model "${FOUNDATIONAL_MODEL}" \
    "${PRIOR_ARGS[@]}" \
    --output-dir "${OUTPUT_DIR}" \
    --max-train-samples "${MAX_TRAIN}" \
    --max-val-samples "${MAX_VAL}" \
    --epochs "${EPOCHS}" \
    --gradient-accumulation-steps "${GAS}" \
    --learning-rate "${LR}" \
    --warmup-ratio "${WARMUP}" \
    --weight-decay "${WD}" \
    --freeze-layers "${FREEZE_LAYERS}" \
    --bf16 \
    --deepspeed "${DS_CONFIG}" \
    ${DO_EVAL} \
    ${EXTRA_TRAIN_ARGS:-}

echo "Stage 3 complete: $(date)"
