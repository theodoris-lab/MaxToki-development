#!/bin/bash
# =============================================================================
# submit_finetune_pipeline.sh
# =============================================================================
# One-shot pipeline submitter for the 4-stage heart-dev fine-tune.
# Each stage is submitted with --dependency=afterok: on the previous stage.
#
# Usage
# -----
#   cd developmental_finetuning/heart_dev_finetune
#   bash slurm/submit_finetune_pipeline.sh            # run all 4 stages
#   bash slurm/submit_finetune_pipeline.sh --skip-prepare   # skip Stage 1
#   bash slurm/submit_finetune_pipeline.sh --eval-test      # evaluate test split instead of val
#
# Environment variable overrides
# --------------------------------
# Anything accepted by the individual run_*.sh scripts works here too, e.g.:
#   MAX_TRAIN=200000 bash slurm/submit_finetune_pipeline.sh
# =============================================================================

set -euo pipefail

PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLURM_DIR="${PIPELINE_DIR}/slurm"

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
SKIP_TOKENIZE=false
SKIP_PREPARE=false
SKIP_TRAJ=false
EVAL_TEST=false
PRIOR_STAGE_JOB_ID=""  # optional: start dependency chain from an existing job ID

for arg in "$@"; do
    case "${arg}" in
        --skip-tokenize)   SKIP_TOKENIZE=true ;;
        --skip-prepare)    SKIP_PREPARE=true ;;
        --skip-traj)       SKIP_TRAJ=true ;;
        --eval-test)       EVAL_TEST=true ;;
        --prior-job=*)     PRIOR_STAGE_JOB_ID="${arg#*=}" ;;
        *)
            echo "Unknown argument: ${arg}" >&2
            echo "Usage: $0 [--skip-tokenize] [--skip-prepare] [--skip-traj] [--eval-test] [--prior-job=<JOB_ID>]" >&2
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Set up evaluation dataset path based on split
# ---------------------------------------------------------------------------
DATA_ROOT="${DATA_ROOT:-/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data}"
if [[ "${EVAL_TEST}" == true ]]; then
    EVAL_DATASET="${DATA_ROOT}/finetuning_heart_dev/trajectories/test/test_heart_dev_masked.dataset"
    EVAL_SPLIT="test"
else
    EVAL_DATASET="${DATA_ROOT}/finetuning_heart_dev/trajectories/val/val_heart_dev_masked.dataset"
    EVAL_SPLIT="val"
fi
export EVAL_DATASET EVAL_SPLIT

# ---------------------------------------------------------------------------
# Stage 0 — tokenize (CPU; prerequisite for Stage 1)
# ---------------------------------------------------------------------------
TOKENIZE_JOB_ID=""
if [[ "${SKIP_TOKENIZE}" == false ]]; then
    PRIOR_DEP=""
    if [[ -n "${PRIOR_STAGE_JOB_ID}" ]]; then
        PRIOR_DEP="--dependency=afterok:${PRIOR_STAGE_JOB_ID}"
    fi
    TOKENIZE_JOB_ID=$(
        sbatch --parsable ${PRIOR_DEP} "${SLURM_DIR}/run_tokenize.sh"
    )
    echo "Submitted Stage 0 (tokenize sources): job ${TOKENIZE_JOB_ID}"
fi

# ---------------------------------------------------------------------------
# Stage 1 — prepare data
# ---------------------------------------------------------------------------
PREPARE_DEP=""
if [[ -n "${TOKENIZE_JOB_ID}" ]]; then
    PREPARE_DEP="--dependency=afterok:${TOKENIZE_JOB_ID}"
elif [[ -n "${PRIOR_STAGE_JOB_ID}" && "${SKIP_TOKENIZE}" == true ]]; then
    PREPARE_DEP="--dependency=afterok:${PRIOR_STAGE_JOB_ID}"
fi

PREPARE_JOB_ID=""
if [[ "${SKIP_PREPARE}" == false ]]; then
    PREPARE_JOB_ID=$(
        sbatch --parsable ${PREPARE_DEP} "${SLURM_DIR}/run_prepare_data.sh"
    )
    echo "Submitted Stage 1 (prepare data): job ${PREPARE_JOB_ID}"
fi

# ---------------------------------------------------------------------------
# Stage 2 — build trajectories
# ---------------------------------------------------------------------------
TRAJ_DEP=""
if [[ -n "${PREPARE_JOB_ID}" ]]; then
    TRAJ_DEP="--dependency=afterok:${PREPARE_JOB_ID}"
elif [[ -n "${PRIOR_STAGE_JOB_ID}" ]]; then
    TRAJ_DEP="--dependency=afterok:${PRIOR_STAGE_JOB_ID}"
fi

TRAJ_JOB_ID=""
if [[ "${SKIP_TRAJ}" == false ]]; then
    TRAJ_JOB_ID=$(
        sbatch --parsable ${TRAJ_DEP} "${SLURM_DIR}/run_build_trajectories.sh"
    )
    echo "Submitted Stage 2 (build trajectories): job ${TRAJ_JOB_ID}"
fi

# ---------------------------------------------------------------------------
# Stage 3 — training
# ---------------------------------------------------------------------------
TRAIN_DEP=""
if [[ -n "${TRAJ_JOB_ID}" ]]; then
    TRAIN_DEP="--dependency=afterok:${TRAJ_JOB_ID}"
fi

TRAIN_JOB_ID=$(
    sbatch --parsable ${TRAIN_DEP} "${SLURM_DIR}/run_train.sh"
)
echo "Submitted Stage 3 (training): job ${TRAIN_JOB_ID}"

# ---------------------------------------------------------------------------
# Stage 4 — evaluation
# ---------------------------------------------------------------------------
EVAL_JOB_ID=$(
    sbatch --parsable \
        --dependency=afterok:${TRAIN_JOB_ID} \
        "${SLURM_DIR}/run_evaluate.sh"
)
echo "Submitted Stage 4 (evaluation, split=${EVAL_SPLIT}): job ${EVAL_JOB_ID}"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "Pipeline submitted successfully:"
[[ -n "${TOKENIZE_JOB_ID}" ]]  && echo "  Stage 0 (tokenize):        ${TOKENIZE_JOB_ID}"
[[ -n "${PREPARE_JOB_ID}" ]] && echo "  Stage 1 (prepare):         ${PREPARE_JOB_ID}"
[[ -n "${TRAJ_JOB_ID}" ]]    && echo "  Stage 2 (trajectories):    ${TRAJ_JOB_ID}"
echo "  Stage 3 (training):        ${TRAIN_JOB_ID}"
echo "  Stage 4 (evaluation):      ${EVAL_JOB_ID}"
echo ""
echo "Monitor with:  squeue -u ${USER} | grep hd26"
echo "Logs under:    ${PIPELINE_DIR}/logs/slurm/"
