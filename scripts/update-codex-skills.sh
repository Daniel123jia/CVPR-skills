#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_SKILLS_DIR="${PROJECT_ROOT}/skills"
TARGET_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
STAMP="$(date +%Y%m%d%H%M%S)"

install_dir() {
  local name="$1"
  local source="${SOURCE_SKILLS_DIR}/${name}"
  local target="${TARGET_SKILLS_DIR}/${name}"

  if [[ ! -d "${source}" ]]; then
    echo "Missing source directory: ${source}" >&2
    return 1
  fi

  mkdir -p "${TARGET_SKILLS_DIR}"

  if [[ -e "${target}" ]]; then
    local backup="${target}.bak.${STAMP}"
    echo "Backing up existing ${target} to ${backup}"
    cp -R "${target}" "${backup}"
  else
    mkdir -p "${target}"
  fi

  cp -R "${source}/." "${target}/"
  echo "Installed ${name} to ${target}"
}

for source in "${SOURCE_SKILLS_DIR}"/*; do
  [[ -d "${source}" ]] || continue
  install_dir "$(basename "${source}")"
done

echo "Installed ai-conference-skills."
