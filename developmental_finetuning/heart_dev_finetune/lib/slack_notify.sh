#!/bin/bash

notify_slack() {
  local msg="$1"
  local webhook="${SLACK_WEBHOOK_URL:-}"

  if [[ -z "${webhook}" && -n "${SLACK_WEBHOOK_B64:-}" ]]; then
    webhook="$(printf '%s' "${SLACK_WEBHOOK_B64}" | base64 --decode 2>/dev/null || true)"
  fi

  if [[ -z "${webhook}" && -n "${SLACK_WEBHOOK_FILE:-}" && -r "${SLACK_WEBHOOK_FILE}" ]]; then
    webhook="$(<"${SLACK_WEBHOOK_FILE}")"
  fi

  if [[ -z "${webhook}" && -n "${SCRIPT_DIR:-}" && -r "${SCRIPT_DIR}/.slack_webhook_url" ]]; then
    webhook="$(<"${SCRIPT_DIR}/.slack_webhook_url")"
  fi

  if [[ -z "${webhook}" ]]; then
    echo "SLACK disabled: ${msg}"
    return 0
  fi

  local escaped payload
  escaped="${msg//\\/\\\\}"
  escaped="${escaped//\"/\\\"}"
  payload="{\"text\":\"${escaped}\"}"
  curl -sS -X POST -H 'Content-type: application/json' --data "${payload}" "${webhook}" >/dev/null 2>&1 || true
}

notify_step_start() {
  local step_name="$1"
  notify_slack "START ${step_name} on $(hostname) | job=${SLURM_JOB_ID:-local} | output=${SLURM_JOB_NAME:-unknown}_${SLURM_JOB_ID:-local}"
}

notify_step_exit() {
  local status="$1"
  local step_name="$2"

  if [[ "${status}" -eq 0 ]]; then
    notify_slack "DONE ${step_name} | job=${SLURM_JOB_ID:-local}"
  else
    notify_slack "FAILED ${step_name} | job=${SLURM_JOB_ID:-local} | exit=${status} | check ${SLURM_JOB_NAME:-unknown}_${SLURM_JOB_ID:-unknown}.err"
  fi
}
