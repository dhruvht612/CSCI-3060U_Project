#!/usr/bin/env bash
# Run every Phase 1 case in isolation; Python supplies portable timeout/capture.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -n "${PYTHON:-}" ]]; then
    PY="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi
exec "$PY" scripts/phase3_tests.py run "$@"
