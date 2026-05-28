#!/bin/bash
# =============================================================================
# setup_env.sh — Install training dependencies into env_maxtoki
# =============================================================================
# Run this ONCE (on the login node) before submitting any Slurm jobs.
#
# What this does
# --------------
#  1. Activates env_maxtoki.
#  2. Installs PyTorch 2.x with CUDA 12.1 support (compatible with A100 GPUs).
#  3. Installs the MaxToki package (editable install from local clone).
#  4. Installs HuggingFace training stack + other pipeline deps.
#  5. Verifies the installation.
#
# Usage
# -----
#   cd developmental_finetuning/heart_dev_finetune
#   bash bash_scripts/setup_env.sh
#
# Environment variable overrides
# --------------------------------
#   TORCH_INDEX_URL   PyTorch wheel index (default: cu121)
#   MAXTOKI_DIR       Path to MaxToki checkout (default: ~/maxtoki_brain_aging/MaxToki)
# =============================================================================

set -euo pipefail

CONDA_BASE="${HOME}/miniconda3"
ENV_NAME="env_maxtoki"
ENV_PATH="${CONDA_BASE}/envs/${ENV_NAME}"
TORCH_INDEX_URL="${TORCH_INDEX_URL:-https://download.pytorch.org/whl/cu121}"
MAXTOKI_DIR="${MAXTOKI_DIR:-${HOME}/maxtoki_brain_aging/MaxToki}"

# ---------------------------------------------------------------------------
# Activate conda
# ---------------------------------------------------------------------------
eval "$(${CONDA_BASE}/bin/conda shell.bash hook)"

if ! conda env list | grep -q "${ENV_PATH}"; then
    echo "ERROR: env_maxtoki not found at ${ENV_PATH}."
    echo "Create it first:  conda create -n env_maxtoki python=3.10 -y"
    exit 1
fi

conda activate "${ENV_NAME}"
echo "Activated: ${ENV_NAME}  (Python $(python --version 2>&1))"

# ---------------------------------------------------------------------------
# Install PyTorch
# ---------------------------------------------------------------------------
echo ""
echo "Installing PyTorch (CUDA 12.1) ..."
pip install torch torchvision torchaudio --index-url "${TORCH_INDEX_URL}"

# ---------------------------------------------------------------------------
# Install MaxToki (editable so local changes take effect immediately)
# ---------------------------------------------------------------------------
echo ""
if [[ -d "${MAXTOKI_DIR}" ]]; then
    echo "Installing MaxToki from local clone: ${MAXTOKI_DIR}"
    pip install -e "${MAXTOKI_DIR}"
else
    echo "ERROR: MaxToki clone not found at ${MAXTOKI_DIR}."
    echo "       Set MAXTOKI_DIR=/path/to/MaxToki before running this script."
    exit 1
fi

# ---------------------------------------------------------------------------
# Install HuggingFace training stack + pipeline deps
# ---------------------------------------------------------------------------
echo ""
echo "Installing training stack and pipeline dependencies ..."
pip install \
    "transformers>=4.56.1" \
    safetensors \
    datasets \
    accelerate \
    deepspeed \
    scipy \
    statsmodels \
    pandas \
    tqdm \
    tabulate

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------
echo ""
echo "=== Verification ==="
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"
python -c "import transformers; print(f'Transformers {transformers.__version__}')"
python -c "import datasets; print(f'Datasets {datasets.__version__}')"
python -c "import safetensors; print('safetensors OK')"
python -c "import deepspeed; print(f'DeepSpeed {deepspeed.__version__}')"
python -c "import accelerate; print(f'Accelerate {accelerate.__version__}')"
python -c "import scipy; print(f'SciPy {scipy.__version__}')"
python -c "import maxtoki; print('MaxToki OK')"
python -c "from maxtoki.tokenizer import TranscriptomeTokenizer; print('TranscriptomeTokenizer OK')"

echo ""
echo "Setup complete.  Activate with:  conda activate ${ENV_NAME}"
