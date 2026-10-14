# OpenRSI-Game

A public CPU-only research task for improving evidence-based playtesting of
AI-generated browser games. Built for OpenRSI task creation and proposal review.

**Status: v0.5 spawn-safe difficulty revision, acceptance pending.**
Development has 48 cases; full evaluation has 96 cases / 160 judgments. The new seed ranges were fixed before control scoring. Measurements from v0.4 belong to that older workload. See [revision details](docs/difficulty-revision-v4.md).

## Research question

Can better visual state estimation, placement planning and evidence assessment
improve functional judgments under a fixed browser-interaction budget?
A research agent changes a playtesting policy, measures it against a fixed
baseline, observes feedback and revises its hypothesis. The optimized scalar is
balanced evidence-supported correct-decision rate, not a platform ranking.

The initial executable corpus contains two previously reviewed public **Codex**
Tetris games and independently checked, task-authored defect variants. Selected
**Codex and Claude Code** historical report findings motivate the methodology.
The Claude Code record used MiniMax-M3, not an Anthropic Claude model. No runnable
Claude Code game is included in v0.3; only two base game implementations are
represented. These limitations are part of the proposal, not hidden by counting
seeded variants as additional independently generated games.

## Run locally

Docker runs the browser inside one ordinary container. No API key or paid model
call is required. Build downloads pinned public dependencies; runtime is offline.

```sh
python3 scripts/package_environment.py
docker build -t openrsi-game:difficulty-pilot environment/
mkdir -p runs
docker run --rm --network none --cpus 4 --memory 8g \
  -v "$PWD/runs:/results" openrsi-game:difficulty-pilot \
  python -m gamebench.evaluate --policy candidate/policy.py --split dev \
  --output /results/dev.json
```

The image initializes the candidate to the fixed reference policy. To iterate
on your local candidate, copy the reference once with `bash solution/solve.sh`,
then mount only that candidate directory into the container:

```sh
docker run --rm --network none --cpus 4 --memory 8g \
  -v "$PWD/candidate:/workspace/openrsi-game/candidate:ro" \
  -v "$PWD/runs:/results" openrsi-game:difficulty-pilot \
  python -m gamebench.evaluate --policy candidate/policy.py --split dev \
  --output /results/dev.json
```

Run the public fixed full evaluation (the private Task has additional scope and process supervision):

```sh
docker run --rm --network none --cpus 4 --memory 8g \
  -v "$PWD/tests:/tests:ro" -v "$PWD/runs:/logs/verifier" \
  openrsi-game:difficulty-pilot python -B -m gamebench.evaluate \
  --policy candidate/policy.py --split judge --output /logs/verifier/public-full.json
```

## Materials

| Material | Purpose |
| --- | --- |
| [Task instructions](instruction.md) | Candidate API, research loop and allowed changes |
| [Evaluation contract](docs/evaluation-contract.md) | Fixed workload, metric, evidence, budgets and limitations |
| [Selected reports](reports/README.md) | Authorized Codex/Claude Code outcomes and caveats |
| [Asset manifest](assets/manifest.json) | Frozen files, digests and model provenance |
| [Methodology](docs/methodology.md) | Evidence and judgment principles |
| [Preparation and approval](docs/task-preparation.md) | Delivery state and official workflow |
| [OpenRSI examples](docs/openrsi-examples.md) | Source requirements and observed review precedents |
| [Validation](docs/validation.md) | Measured baseline and compatibility checks, when recorded |
| [Budget revision](docs/budget-revision.md) | Matched 16-action protocol and historical-score separation |

`task.toml`, `instruction.md`, `environment/`, `solution/` and `tests/test.sh`
follow the Harbor schema 1.4 / RSI-Harness shared Work/Judge task layout.
Judge receives its own injected evaluator copies and pinned asset manifest;
Work's public evaluator is for development. No independent clean Base or
malicious-code isolation is claimed. See the contract for residual limits.

## Contributor and publication

**Haotian Xu**, creator of [AI Game Bench](https://aigamebench.com/).
Publication email: ht@mopan.ai. [LinkedIn](https://www.linkedin.com/in/xuhaotian/).

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). This repository publishes
independently prepared task code, approved game-only artifacts and selected
report findings. It excludes raw runs, creator conversations, credentials,
account data, internal services and company implementation details.

Task submission follows [OpenRSI CONTRIBUTING.md](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md).
Proposal approval, successful task generation and final benchmark inclusion are
separate stages. A small runnable prototype does not guarantee inclusion.
