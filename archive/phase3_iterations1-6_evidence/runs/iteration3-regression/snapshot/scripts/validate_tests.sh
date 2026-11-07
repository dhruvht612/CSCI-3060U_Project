#!/usr/bin/env bash
# Validate a saved run without executing the application or rewriting evidence.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -n "${PYTHON:-}" ]]; then
    PY="$PYTHON"
elif command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi
exec "$PY" scripts/phase3_tests.py validate "$@"
