#!/usr/bin/env bash
set -Eeuo pipefail

DEFAULT_DEST="/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data"
DEST="${MAXTOKI_DATA_DIR:-$DEFAULT_DEST}"
DRY_RUN=0
OVERWRITE=0
ONLY=""
RUN_ID="${MAXTOKI_RUN_ID:-$(date '+%Y%m%d_%H%M%S')}"
LOG_DIR="${MAXTOKI_LOG_DIR:-$DEST/logs}"
RUN_LOG=""
REPORT_LOG=""
FILE_SIZE_LOG=""
START_EPOCH="$(date +%s)"
START_AT="$(date '+%Y-%m-%dT%H:%M:%S%z')"
LAST_DURATION_HMS=""
LAST_TOTAL_HUMAN=""
CURL_ATTEMPTS="${MAXTOKI_CURL_ATTEMPTS:-10}"
CURL_ATTEMPT_DELAY="${MAXTOKI_CURL_ATTEMPT_DELAY:-60}"

HCA_MANIFEST_URL="https://service.azul.data.humancellatlas.org/manifest/files/ksQwlKVkY3A1OKRjdXJsxBDcPM8M8a9TIKm6MrnjQ2LOxBB6Q4VF6pRdTLwdCUJZ8BnnxCCZfSJCZ17uFNzShxfsWzhVHmDHhXYH9p8RdfkXq6ZUPw"

usage() {
  cat <<'USAGE'
Download the Maxtoki development datasets into one directory.

Usage:
  scripts/download_datasets.sh [options]

Options:
  --dest DIR       Destination directory.
                   Default: /gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data
                   You can also set MAXTOKI_DATA_DIR.
  --only LIST      Comma-separated sources to run:
                   cellxgene,hca,ucsc,lab
  --overwrite      Re-download or re-copy files that already exist.
  --dry-run        Print what would be done without downloading/copying.
  -h, --help       Show this help text.

Logging and notification:
  Each real run writes logs under DEST/logs by default:
    download_<run_id>.log
    download_report_<run_id>.tsv
    download_file_sizes_<run_id>.tsv

  If SLACK_WEBHOOK_URL is set, the script sends a Slack message when the
  run finishes or fails.

Examples:
  scripts/download_datasets.sh
  scripts/download_datasets.sh --only cellxgene,ucsc
  scripts/download_datasets.sh --dest /path/to/data --dry-run
USAGE
}

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"
}

retry_curl() {
  local attempt

  for ((attempt = 1; attempt <= CURL_ATTEMPTS; attempt++)); do
    if curl "$@"; then
      return 0
    fi

    if [[ "$attempt" -lt "$CURL_ATTEMPTS" ]]; then
      log "curl attempt $attempt failed; retrying in ${CURL_ATTEMPT_DELAY}s"
      sleep "$CURL_ATTEMPT_DELAY"
    fi
  done

  log "curl failed after $CURL_ATTEMPTS attempts"
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      [[ $# -ge 2 ]] || die "--dest requires a directory"
      DEST="$2"
      shift 2
      ;;
    --only)
      [[ $# -ge 2 ]] || die "--only requires a comma-separated source list"
      ONLY="$2"
      shift 2
      ;;
    --overwrite)
      OVERWRITE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown option: $1"
      ;;
  esac
done

if [[ -z "${MAXTOKI_LOG_DIR:-}" ]]; then
  LOG_DIR="$DEST/logs"
fi

duration_hms() {
  local seconds="$1"
  local hours minutes

  hours=$((seconds / 3600))
  minutes=$(((seconds % 3600) / 60))
  seconds=$((seconds % 60))
  printf '%02d:%02d:%02d' "$hours" "$minutes" "$seconds"
}

setup_file_logging() {
  [[ "$DRY_RUN" -eq 1 ]] && return 0

  mkdir -p "$LOG_DIR"
  RUN_LOG="$LOG_DIR/download_${RUN_ID}.log"
  REPORT_LOG="$LOG_DIR/download_report_${RUN_ID}.tsv"
  FILE_SIZE_LOG="$LOG_DIR/download_file_sizes_${RUN_ID}.tsv"

  exec > >(tee -a "$RUN_LOG") 2>&1
}

write_run_report() {
  local status="$1"
  local end_epoch end_at duration total_bytes file_count partial_count status_label
  local slurm_job_id

  [[ "$DRY_RUN" -eq 1 ]] && return 0

  end_epoch="$(date +%s)"
  end_at="$(date '+%Y-%m-%dT%H:%M:%S%z')"
  duration=$((end_epoch - START_EPOCH))
  LAST_DURATION_HMS="$(duration_hms "$duration")"
  status_label="success"
  [[ "$status" -ne 0 ]] && status_label="failed"
  slurm_job_id="${SLURM_JOB_ID:-}"

  total_bytes="$(du -sb "$DEST" 2>/dev/null | awk 'NR == 1 {print $1}')"
  total_bytes="${total_bytes:-0}"
  LAST_TOTAL_HUMAN="$(du -sh "$DEST" 2>/dev/null | awk 'NR == 1 {print $1}')"
  LAST_TOTAL_HUMAN="${LAST_TOTAL_HUMAN:-0}"
  file_count="$(find "$DEST" -type f ! -path "$LOG_DIR/*" 2>/dev/null | wc -l | awk '{print $1}')"
  partial_count="$(find "$DEST" -type f -name '*.part' 2>/dev/null | wc -l | awk '{print $1}')"

  {
    printf 'metric\tvalue\n'
    printf 'status\t%s\n' "$status_label"
    printf 'exit_code\t%s\n' "$status"
    printf 'slurm_job_id\t%s\n' "$slurm_job_id"
    printf 'destination\t%s\n' "$DEST"
    printf 'started_at\t%s\n' "$START_AT"
    printf 'ended_at\t%s\n' "$end_at"
    printf 'duration_seconds\t%s\n' "$duration"
    printf 'duration_hms\t%s\n' "$LAST_DURATION_HMS"
    printf 'total_size_bytes\t%s\n' "$total_bytes"
    printf 'total_size_human\t%s\n' "$LAST_TOTAL_HUMAN"
    printf 'file_count_excluding_logs\t%s\n' "$file_count"
    printf 'partial_file_count\t%s\n' "$partial_count"
    printf 'run_log\t%s\n' "$RUN_LOG"
    printf 'file_size_log\t%s\n' "$FILE_SIZE_LOG"
  } > "$REPORT_LOG"

  {
    printf 'bytes\tpath\n'
    find "$DEST" -type f ! -path "$LOG_DIR/*" -printf '%s\t%p\n' 2>/dev/null | sort -k2
  } > "$FILE_SIZE_LOG"

  log "Wrote run report: $REPORT_LOG"
  log "Wrote file-size log: $FILE_SIZE_LOG"
}

notify_slack() {
  local status="$1"
  local webhook="${SLACK_WEBHOOK_URL:-}"
  local status_label emoji text payload slurm_job_id

  [[ "$DRY_RUN" -eq 1 ]] && return 0
  [[ -z "$webhook" ]] && return 0

  if ! command -v curl >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
    log "WARNING: Slack notification skipped because curl or jq is unavailable"
    return 0
  fi

  status_label="SUCCESS"
  emoji=":white_check_mark:"
  if [[ "$status" -ne 0 ]]; then
    status_label="FAILED"
    emoji=":x:"
  fi

  slurm_job_id="${SLURM_JOB_ID:-not_slurm}"
  text="${emoji} Maxtoki dataset download ${status_label}
Job: ${slurm_job_id}
Destination: ${DEST}
Duration: ${LAST_DURATION_HMS:-unknown}
Total size: ${LAST_TOTAL_HUMAN:-unknown}
Report: ${REPORT_LOG}
Log: ${RUN_LOG}"

  payload="$(jq -n --arg text "$text" '{text: $text}')"
  if curl --silent --show-error --fail \
      --request POST \
      --header 'Content-type: application/json' \
      --data "$payload" \
      "$webhook" >/dev/null; then
    log "Sent Slack notification"
  else
    log "WARNING: Slack notification failed"
  fi
}

on_exit() {
  local status="$?"
  set +e
  write_run_report "$status"
  notify_slack "$status"
  exit "$status"
}

should_run() {
  local source="$1"
  local item

  [[ -z "$ONLY" ]] && return 0

  IFS=',' read -r -a items <<< "$ONLY"
  for item in "${items[@]}"; do
    item="${item//[[:space:]]/}"
    [[ "$item" == "$source" ]] && return 0
  done

  return 1
}

ensure_dir() {
  local dir="$1"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "Would create directory: $dir"
  else
    mkdir -p "$dir"
  fi
}

curl_download() {
  local name="$1"
  local url="$2"
  local output_dir="$3"
  local filename="$4"
  local final_path="$output_dir/$filename"
  local partial_path="$final_path.part"
  local curl_args=()

  require_command curl
  ensure_dir "$output_dir"

  if [[ -s "$final_path" && "$OVERWRITE" -eq 0 ]]; then
    log "Skipping existing file: $final_path"
    return 0
  fi

  if [[ -f "$final_path" && ! -s "$final_path" && "$OVERWRITE" -eq 0 ]]; then
    log "Removing empty existing file before retrying: $final_path"
    rm -f "$final_path"
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "Would download: $name"
    log "  URL: $url"
    log "  To:  $final_path"
    return 0
  fi

  if [[ "$OVERWRITE" -eq 1 ]]; then
    rm -f "$final_path" "$partial_path"
  fi

  log "Downloading: $name"
  curl_args=(
      --location \
      --fail \
      --retry 15 \
      --retry-delay 10 \
      --connect-timeout 30 \
      --output "$partial_path" \
      "$url"
  )

  if [[ -s "$partial_path" ]]; then
    curl_args=(--continue-at - "${curl_args[@]}")
  fi

  if ! retry_curl "${curl_args[@]}"; then
    if [[ -s "$partial_path" ]]; then
      log "Resume failed for $name; restarting from byte 0"
      rm -f "$partial_path"
      retry_curl \
        --location \
        --fail \
        --retry 15 \
        --retry-delay 10 \
        --connect-timeout 30 \
        --output "$partial_path" \
        "$url"
    else
      return 1
    fi
  fi

  mv "$partial_path" "$final_path"
  log "Saved: $final_path"
}

copy_local_item() {
  local name="$1"
  local source_path="$2"
  local output_dir="$3"
  local output_name="$4"
  local final_path="$output_dir/$output_name"

  ensure_dir "$output_dir"

  if [[ ! -e "$source_path" ]]; then
    die "Local source does not exist: $source_path"
  fi

  if [[ -f "$source_path" && -s "$final_path" && "$OVERWRITE" -eq 0 ]]; then
    log "Skipping existing local file: $final_path"
    return 0
  fi

  if [[ -f "$source_path" && -f "$final_path" && ! -s "$final_path" && "$OVERWRITE" -eq 0 ]]; then
    log "Removing empty existing local file before retrying: $final_path"
    rm -f "$final_path"
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "Would copy: $name"
    log "  From: $source_path"
    log "  To:   $final_path"
    return 0
  fi

  log "Copying: $name"
  if command -v rsync >/dev/null 2>&1; then
    if [[ -d "$source_path" ]]; then
      mkdir -p "$final_path"
      rsync -a --info=progress2 "$source_path"/ "$final_path"/
    else
      mkdir -p "$(dirname "$final_path")"
      rsync -a --info=progress2 "$source_path" "$final_path"
    fi
  else
    if [[ -d "$source_path" ]]; then
      mkdir -p "$final_path"
      cp -a "$source_path"/. "$final_path"/
    else
      mkdir -p "$(dirname "$final_path")"
      cp -p "$source_path" "$final_path"
    fi
  fi
  log "Copied: $final_path"
}

write_manifest() {
  local manifest="$DEST/download_manifest.tsv"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "Would write manifest: $manifest"
    return 0
  fi

  cat > "$manifest" <<'MANIFEST'
source	dataset	location
cellxgene	Construction of a human cell landscape at single-cell level	source_1_cellxgene/01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad
cellxgene	Survey of human embryonic development (1 million cells subset)	source_1_cellxgene/02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad
cellxgene	Survey of human embryonic development	source_1_cellxgene/03_survey_of_human_embryonic_development.h5ad
cellxgene	Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor	source_1_cellxgene/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad
cellxgene	Integrated adult and foetal hearts	source_1_cellxgene/05_integrated_adult_and_foetal_hearts.h5ad
cellxgene	Rotem_12W_heart_C1	source_1_cellxgene/06_rotem_12w_heart_c1.h5ad
cellxgene	Rotem_12W_heart_B1	source_1_cellxgene/07_rotem_12w_heart_b1.h5ad
cellxgene	Rotem_12W_heart_D1	source_1_cellxgene/08_rotem_12w_heart_d1.h5ad
cellxgene	Rotem_12W_heart_A1	source_1_cellxgene/09_rotem_12w_heart_a1.h5ad
cellxgene	Single-nuclei RNA-seq of the human outflow tract and aortic valve tissue	source_1_cellxgene/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad
hca	Human Early Embryogenesis Atlas	source_2_human_early_embryogenesis_atlas/
ucsc	Human Cardiogenesis in vitro	source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz
ucsc	Human Cardiogenesis in vivo	source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz
ucsc	Multiomic Human Heart in snRNA-seq matrix	source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.mtx.gz
ucsc	Multiomic Human Heart in snATAC-seq matrix	source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.mtx.gz
ucsc	Multiomic Human Heart subset matrix	source_3_ucsc_cells/05_multiomic_human_heart_subset_matrix.mtx.gz
ucsc	Multiomic Human Heart in snRNA-seq h5ad	source_3_ucsc_cells/06_multiomic_human_heart_snrna_seq_integrated_rna_adata.h5ad
ucsc	Multiomic Human Heart in snATAC-seq h5ad	source_3_ucsc_cells/07_multiomic_human_heart_snatac_seq_integrated_atac_adata.h5ad
ucsc	Multiomic Human Heart subset h5ad	source_3_ucsc_cells/08_multiomic_human_heart_subset_integrated_400k_rna_adata.h5ad
lab	Human Fetal Cis-Regulatory Elements	source_4_lab_directory/01_human_fetal_cis_regulatory_elements.loom
lab	Human Fetal Striatum Atlas	source_4_lab_directory/02_human_fetal_striatum_atlas.loom
lab	Human Megakaryocyte Development	source_4_lab_directory/03_human_megakaryocyte_development/
lab	Fetal vs. Adult Human Epicardium	source_4_lab_directory/04_fetal_vs_adult_human_epicardium.loom
lab	Tyser et al. 2021 Gastrulation Atlas	source_4_lab_directory/05_tyser_2021_gastrulation_atlas/
MANIFEST
  log "Wrote manifest: $manifest"
}

download_cellxgene() {
  local output_dir="$DEST/source_1_cellxgene"
  local item name url filename
  local items=(
    "Construction of a human cell landscape at single-cell level|https://datasets.cellxgene.cziscience.com/74c3403a-451c-4a62-84e0-d8a8e45c7ea7.h5ad|01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad"
    "Survey of human embryonic development (1 million cells subset)|https://datasets.cellxgene.cziscience.com/c3bf819d-423d-435f-b8d0-e36ad6088138.h5ad|02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad"
    "Survey of human embryonic development|https://datasets.cellxgene.cziscience.com/dd2564a6-27a0-433a-893c-72475e4a39fe.h5ad|03_survey_of_human_embryonic_development.h5ad"
    "Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor|https://datasets.cellxgene.cziscience.com/d61a74ab-e1ef-4ced-9131-698bf7d94be2.h5ad|04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad"
    "Integrated adult and foetal hearts|https://datasets.cellxgene.cziscience.com/51073d23-97b7-4c05-84eb-5a18024e966c.h5ad|05_integrated_adult_and_foetal_hearts.h5ad"
    "Rotem_12W_heart_C1|https://datasets.cellxgene.cziscience.com/380b448b-85de-4953-8e82-2fda20276a12.h5ad|06_rotem_12w_heart_c1.h5ad"
    "Rotem_12W_heart_B1|https://datasets.cellxgene.cziscience.com/57c7e31e-6bf5-4498-a2d3-2a3728c64ded.h5ad|07_rotem_12w_heart_b1.h5ad"
    "Rotem_12W_heart_D1|https://datasets.cellxgene.cziscience.com/72e35ce5-fb20-46d0-adf9-a8c7f44af287.h5ad|08_rotem_12w_heart_d1.h5ad"
    "Rotem_12W_heart_A1|https://datasets.cellxgene.cziscience.com/731fb49f-4a81-48d5-9f28-ee1b08f1018d.h5ad|09_rotem_12w_heart_a1.h5ad"
    "Single-nuclei RNA-seq of the human outflow tract and aortic valve tissue|https://datasets.cellxgene.cziscience.com/e6c07fbd-c90b-48c0-b6e3-b03b2d7218c5.h5ad|10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad"
  )

  log "Source 1: CellxGene"
  for item in "${items[@]}"; do
    IFS='|' read -r name url filename <<< "$item"
    curl_download "$name" "$url" "$output_dir" "$filename"
  done
}

download_hca() {
  local output_dir="$DEST/source_2_human_early_embryogenesis_atlas"
  local marker="$output_dir/.download_complete"
  local manifest_config="$output_dir/hca_manifest_${RUN_ID}.curl_config"

  require_command curl
  ensure_dir "$output_dir"

  if [[ -f "$marker" && "$OVERWRITE" -eq 0 ]]; then
    log "Skipping HCA manifest download because marker exists: $marker"
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "Would run HCA/Azul manifest download in: $output_dir"
    log "  Manifest: $HCA_MANIFEST_URL"
    return 0
  fi

  if [[ "$OVERWRITE" -eq 1 ]]; then
    rm -f "$marker"
  fi

  log "Source 2: Human Early Embryogenesis Atlas"
  retry_curl --location --fail --output "$manifest_config" "$HCA_MANIFEST_URL"
  (
    cd "$output_dir"
    retry_curl --retry 15 --retry-delay 10 --location --fail --config "$manifest_config"
  )
  rm -f "$manifest_config"
  date '+%Y-%m-%d %H:%M:%S' > "$marker"
  log "Completed HCA manifest download: $output_dir"
}

download_ucsc() {
  local output_dir="$DEST/source_3_ucsc_cells"
  local item name url filename
  local items=(
    "Human Cardiogenesis in vitro|https://cells.ucsc.edu/cardiogenesis-atac/in-vitro/exprMatrix.tsv.gz|01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz"
    "Human Cardiogenesis in vivo|https://cells.ucsc.edu/cardiogenesis-atac/in-vivo/exprMatrix.tsv.gz|02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz"
    "Multiomic Human Heart in snRNA-seq matrix|https://cells.ucsc.edu/multiomic-human-heart/rna/matrix.mtx.gz|03_multiomic_human_heart_snrna_seq_matrix.mtx.gz"
    "Multiomic Human Heart in snATAC-seq matrix|https://cells.ucsc.edu/multiomic-human-heart/atac/matrix.mtx.gz|04_multiomic_human_heart_snatac_seq_matrix.mtx.gz"
    "Multiomic Human Heart subset matrix|https://cells.ucsc.edu/multiomic-human-heart/subset/matrix.mtx.gz|05_multiomic_human_heart_subset_matrix.mtx.gz"
    "Multiomic Human Heart in snRNA-seq h5ad|https://cells.ucsc.edu/multiomic-human-heart/rna/integrated_RNA_adata.h5ad|06_multiomic_human_heart_snrna_seq_integrated_rna_adata.h5ad"
    "Multiomic Human Heart in snATAC-seq h5ad|https://cells.ucsc.edu/multiomic-human-heart/atac/integrated_ATAC_adata.h5ad|07_multiomic_human_heart_snatac_seq_integrated_atac_adata.h5ad"
    "Multiomic Human Heart subset h5ad|https://cells.ucsc.edu/multiomic-human-heart/subset/integrated_400K_RNA_adata.h5ad|08_multiomic_human_heart_subset_integrated_400k_rna_adata.h5ad"
  )

  log "Source 3: UCSC Cells"
  for item in "${items[@]}"; do
    IFS='|' read -r name url filename <<< "$item"
    curl_download "$name" "$url" "$output_dir" "$filename"
  done
}

copy_lab_directory() {
  local output_dir="$DEST/source_4_lab_directory"
  local item name source_path output_name
  local items=(
    "Human Fetal Cis-Regulatory Elements|/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/9010519993/File_S3_Matrix.Gene_Raw_Counts_of_Cells.loom|01_human_fetal_cis_regulatory_elements.loom"
    "Human Fetal Striatum Atlas|/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/E-MTAB-8894/E-MTAB-8894.loom|02_human_fetal_striatum_atlas.loom"
    "Human Megakaryocyte Development|/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/4110056855|03_human_megakaryocyte_development"
    "Fetal vs. Adult Human Epicardium|/gladstone/theodoris/lab/genecorpus_XM/corpus_loom_files/genecorpus_95M_loom/cxg/5500c673-1610-40a0-86d9-64d987ae50e6.loom|04_fetal_vs_adult_human_epicardium.loom"
    "Tyser et al. 2021 Gastrulation Atlas|/gladstone/theodoris/lab/ctheodoris/validation/gastrulation|05_tyser_2021_gastrulation_atlas"
  )

  log "Source 4: Lab directory"
  for item in "${items[@]}"; do
    IFS='|' read -r name source_path output_name <<< "$item"
    copy_local_item "$name" "$source_path" "$output_dir" "$output_name"
  done
}

validate_only_values() {
  local item

  [[ -z "$ONLY" ]] && return 0

  IFS=',' read -r -a items <<< "$ONLY"
  for item in "${items[@]}"; do
    item="${item//[[:space:]]/}"
    case "$item" in
      cellxgene|hca|ucsc|lab) ;;
      *) die "Unknown --only source '$item'. Expected one of: cellxgene,hca,ucsc,lab" ;;
    esac
  done
}

main() {
  validate_only_values
  ensure_dir "$DEST"
  setup_file_logging
  trap on_exit EXIT

  log "Starting dataset download"
  log "Destination: $DEST"
  log "Run log: $RUN_LOG"

  should_run cellxgene && download_cellxgene
  should_run hca && download_hca
  should_run ucsc && download_ucsc
  should_run lab && copy_lab_directory

  write_manifest
  log "Done. Dataset directory: $DEST"
}

main "$@"
