"""Independently exercise I/J/L row completion via normal keyboard input."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from gamebench import fixtures
from gamebench.browser import Game
from gamebench.fixtures import VARIANTS, labels, verify_assets

fixtures.ROOT = Path('/workspace/openrsi-game') if Path('/workspace/openrsi-game').exists() else Path(__file__).resolve().parents[1]
fixtures.ASSET_MANIFEST = Path(__file__).resolve().parent / 'assets-manifest.json'


def check():
    verify_assets()
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-dev-shm-usage"])
        try:
            for family in ("a", "b"):
                for variant in VARIANTS:
                    game = Game(browser, family, variant, 1, probe=True)
                    try:
                        game.act({"key": "Enter"})
                        for movement in ([-1] * 3, [1], [1] * 4):
                            for direction in movement:
                                game.act({"key": "ArrowLeft" if direction < 0 else "ArrowRight"})
                            game.act({"key": "Space"})
                        cert = list(game.certificates.values())[-1]
                        gold = labels(variant)
                        assert all(cert.get(k) == v for k, v in gold.items() if v is not None), (family, variant, cert)
                        obs = game.observe()
                        records.append({"family": family, "variant": variant,
                                        "score": obs["score"], "lines": obs["lines"], "certificate": cert})
                    finally:
                        game.close()
        finally:
            browser.close()
    return records


if __name__ == "__main__":
    print(json.dumps({"probe": "fixed I/J/L with normal input after controlled setup",
                      "results": check()}, indent=2))
