#!/bin/bash
set -euo pipefail
cd /workspace/openrsi-game
mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/reward.json
python -I /tests/evaluate.py --policy candidate/policy.py --split judge --output /logs/verifier/result.json
python - <<'PY'
import json
from pathlib import Path
p=Path('/logs/verifier'); result=json.loads((p/'result.json').read_text())
if result['status']!='scored' or not result['official_full_run']:
    raise SystemExit('Full measurement unavailable; no finite reward emitted')
(p/'reward.txt').write_text(str(result['score'])+'\n')
(p/'reward.json').write_text(json.dumps({'reward':result['score']})+'\n')
PY
