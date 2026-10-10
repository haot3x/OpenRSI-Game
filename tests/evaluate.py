"""Judge-only bootstrap: use injected evaluator copies, never Work evaluator code."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gamebench import fixtures
from gamebench.evaluate import main

fixtures.ROOT = Path("/workspace/openrsi-game")
fixtures.ASSET_MANIFEST = Path(__file__).resolve().parent / "assets-manifest.json"

if __name__ == "__main__":
    raise SystemExit(main())
