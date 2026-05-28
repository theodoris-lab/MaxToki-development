#!/bin/bash
# =============================================================================
# run_smoke_test.sh — Smoke test for Stage 3 fine-tuning (~10 min on ctdev)
# =============================================================================
# Runs ~8 gradient steps over 512 training examples to verify the entire
# training loop (model load, data, forward/backward, checkpoint save) works
# before committing a full job to ctbatch.
# =============================================================================
#SBATCH --job-name=hd26_smoke
#SBATCH --partition=ctdev
#SBATCH --time=0:20:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:A100:4
#SBATCH --cpus-per-task=8
#SBATCH --mem=256G
#SBATCH --output=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/smoke_%j.out
#SBATCH --error=/gladstone/theodoris/home/eniyonkuru/maxtoki_development/developmental_finetuning/heart_dev_finetune/logs/slurm/smoke_%j.err

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
notify_step_start "heart-dev smoke test (job ${SLURM_JOB_ID}, ${SLURM_NTASKS} GPUs)"

trap 'notify_step_exit "heart-dev smoke test" $?' EXIT

# ---------------------------------------------------------------------------
# NCCL / distributed training settings
# ---------------------------------------------------------------------------
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export NCCL_IB_DISABLE="${NCCL_IB_DISABLE:-0}"
export NCCL_NET_GDR_LEVEL="${NCCL_NET_GDR_LEVEL:-2}"
export MASTER_PORT="${MASTER_PORT:-29500}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-8}"

# ---------------------------------------------------------------------------
# Smoke-test settings (small — ~8 gradient steps total)
#   global_batch = per_device_bs(1) × GAS(64) × world_size(4) = 256
#   steps = ceil(512 / 256) = 2 full steps, but logging_fraction forces ≥1 log
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
TOKEN_DICT="${TOKEN_DICT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/token_dictionary_aging_gc95M.pkl}"
FOUNDATIONAL_MODEL="${FOUNDATIONAL_MODEL:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data/foundational_94M_model}"
OUTPUT_DIR="${OUTPUT_DIR:-${DATA_ROOT}/finetuning_heart_dev/smoke_test_model}"
TRAIN_DATASET="${TRAIN_DATASET:-${DATA_ROOT}/finetuning_heart_dev/trajectories/train/train_heart_dev_masked.dataset}"
VAL_DATASET="${VAL_DATASET:-${DATA_ROOT}/finetuning_heart_dev/trajectories/val/val_heart_dev_masked.dataset}"

echo "=== Heart-Dev Smoke Test ==="
echo "Train dataset:   ${TRAIN_DATASET}"
echo "Output dir:      ${OUTPUT_DIR}"
echo "GPUs:            ${SLURM_NTASKS}"
echo "SLURM job ID:    ${SLURM_JOB_ID:-local}"
echo "Date:            $(date)"
echo ""
echo "Config: 512 train samples, GAS=64 → ~2 gradient steps (global_batch=256)"

deepspeed \
    --num_gpus "${SLURM_NTASKS}" \
    "${SRC_DIR}/finetune_heart_dev.py" \
    --train-dataset        "${TRAIN_DATASET}" \
    --val-dataset          "${VAL_DATASET}" \
    --token-dictionary     "${TOKEN_DICT}" \
    --foundational-model   "${FOUNDATIONAL_MODEL}" \
    --output-dir           "${OUTPUT_DIR}" \
    --max-train-samples    512 \
    --max-val-samples      256 \
    --epochs               1 \
    --gradient-accumulation-steps 64 \
    --learning-rate        0.00016 \
    --warmup-ratio         0.007 \
    --weight-decay         0.044 \
    --freeze-layers        0 \
    --bf16 \
    --deepspeed            "${DS_CONFIG}"

echo "Smoke test PASSED: $(date)"
echo "If training loss was finite and a checkpoint was saved, submit the real job:"
echo "  sbatch slurm/run_train.sh  (on ctbatch)"
