#!/usr/bin/env bash
set -Eeuo pipefail

DEFAULT_DEST="/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data"
DEST="${MAXTOKI_DATA_DIR:-$DEFAULT_DEST}"
REPO_DIR="/gladstone/theodoris/home/eniyonkuru/maxtoki_development"
SBATCH_SCRIPT="$REPO_DIR/scripts/download_datasets.sbatch"
LOG_DIR=""
DOWNLOAD_ARGS=()

usage() {
  cat <<'USAGE'
Submit the Maxtoki dataset downloader as a Slurm job.

Usage:
  scripts/submit_download_datasets_job.sh [download_datasets.sh options]

Common options passed through to download_datasets.sh:
  --dest DIR
  --only cellxgene,hca,ucsc,lab
  --overwrite

Environment:
  SLACK_WEBHOOK_URL     Optional Slack incoming-webhook URL for completion alerts.
  MAXTOKI_SLURM_TIME    Slurm time limit. Default: 24:00:00.
  MAXTOKI_SLURM_MEM     Slurm memory request. Default: 8G.
  MAXTOKI_SLURM_CPUS    Slurm CPUs per task. Default: 2.
  MAXTOKI_SLURM_PARTITION
                       Slurm partition. Default: ctbatch.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      [[ $# -ge 2 ]] || { printf 'ERROR: --dest requires a directory\n' >&2; exit 1; }
      DEST="$2"
      DOWNLOAD_ARGS+=("$1" "$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      DOWNLOAD_ARGS+=("$1")
      shift
      ;;
  esac
done

command -v sbatch >/dev/null 2>&1 || {
  printf 'ERROR: sbatch was not found on PATH\n' >&2
  exit 1
}

LOG_DIR="${MAXTOKI_LOG_DIR:-$DEST/logs}"
mkdir -p "$LOG_DIR"

job_id="$(
  sbatch \
    --parsable \
    --job-name=maxtoki_data_download \
    --output="$LOG_DIR/slurm-%x-%j.out" \
    --error="$LOG_DIR/slurm-%x-%j.err" \
    --partition="${MAXTOKI_SLURM_PARTITION:-ctbatch}" \
    --time="${MAXTOKI_SLURM_TIME:-24:00:00}" \
    --mem="${MAXTOKI_SLURM_MEM:-8G}" \
    --cpus-per-task="${MAXTOKI_SLURM_CPUS:-2}" \
    --export=ALL,MAXTOKI_DATA_DIR="$DEST" \
    "$SBATCH_SCRIPT" \
    "${DOWNLOAD_ARGS[@]}"
)"

printf 'Submitted Slurm job: %s\n' "$job_id"
printf 'Slurm logs: %s/slurm-maxtoki_data_download-%s.out and .err\n' "$LOG_DIR" "$job_id"
printf 'Downloader logs will be written under: %s\n' "$LOG_DIR"
