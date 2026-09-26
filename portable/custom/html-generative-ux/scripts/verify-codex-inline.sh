#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: verify-codex-inline.sh <YYYY/MM/DD> <thread-id> <basename.html>" >&2
  exit 64
fi

date_path=$1
thread_id=$2
basename=$3

if [[ ! $date_path =~ ^[0-9]{4}/[0-9]{2}/[0-9]{2}$ ]]; then
  echo "error: date must use YYYY/MM/DD" >&2
  exit 65
fi

if [[ ! $thread_id =~ ^[A-Za-z0-9-]+$ ]]; then
  echo "error: invalid thread id" >&2
  exit 65
fi

if [[ ! $basename =~ ^[a-z0-9][a-z0-9-]*\.html$ ]]; then
  echo "error: basename must be lowercase ASCII hyphen-case and end in .html" >&2
  exit 65
fi

windows_root=${CODEX_WINDOWS_VIS_ROOT:-}
wsl_root=${CODEX_WSL_VIS_ROOT:-$HOME/.codex/visualizations}
if [[ -z $windows_root ]]; then
  echo "error: set CODEX_WINDOWS_VIS_ROOT to the Windows visualization directory" >&2
  exit 64
fi
windows_file="$windows_root/$date_path/$thread_id/$basename"
wsl_file="$wsl_root/$date_path/$thread_id/$basename"

for required_file in "$windows_file" "$wsl_file"; do
  if [[ ! -f $required_file ]]; then
    echo "error: missing thread mirror: $required_file" >&2
    exit 66
  fi
done

windows_hash=$(sha256sum "$windows_file" | awk '{print $1}')
wsl_hash=$(sha256sum "$wsl_file" | awk '{print $1}')

if [[ $windows_hash != "$wsl_hash" ]]; then
  echo "error: Windows and WSL visualization hashes differ" >&2
  echo "windows_sha256=$windows_hash" >&2
  echo "wsl_sha256=$wsl_hash" >&2
  exit 67
fi

byte_size=$(stat -c '%s' "$windows_file")
if (( byte_size >= 1048576 )); then
  echo "error: fragment is $byte_size bytes; keep inline visualizations below 1 MiB" >&2
  exit 68
fi

if rg -qi '<!doctype|<html([[:space:]>])|<head([[:space:]>])|<body([[:space:]>])' "$windows_file"; then
  echo "error: expected an HTML fragment, but a document-shell tag was found" >&2
  exit 69
fi

echo "resolver=codex-inline-vis"
echo "windows_path=$windows_file"
echo "wsl_path=$wsl_file"
echo "bytes=$byte_size"
echo "sha256=$windows_hash"
echo "directive=::codex-inline-vis{file=\"$basename\"}"
