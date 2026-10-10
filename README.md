# OpenRSI-Game

Public methodology and preparation materials for an OpenRSI game-evaluation task. This repository is intended for task creation and proposal review.

**Status: draft for review.** The repository currently contains documents and a proposed report schema. It does not yet contain an executable benchmark, a frozen game corpus, reference labels or a runnable baseline.

## Research direction

Can a research agent improve browser exploration and evidence assessment so that a playtester verifies more game requirements correctly under a fixed interaction and inference budget?

The proposed game creation scope is limited to **Codex and Claude**. The research target is the evaluation method: action planning, reaching relevant game states and deciding whether observations support a requirement. Exact tool and model identities must be fixed before selecting the corpus; a tool name alone does not identify its underlying model.

[AI Game Bench](https://aigamebench.com/) provides the contributor's domain background. Its [public methodology](https://www.aigamebench.com/methodology) emphasizes real outcomes, fair comparison and transparent evidence. This repository develops that motivation into a proposed, auditable research task.

## Review materials

| Material | Purpose |
| --- | --- |
| [Task concept](docs/task-concept.md) | Scientific question, research loop, baseline and evaluation design |
| [Methodology](docs/methodology.md) | Evidence requirements, judgment states and comparison conditions |
| [Task preparation](docs/task-preparation.md) | Concrete steps to complete code, assets, baseline and scoring |
| [OpenRSI discussion examples](docs/openrsi-examples.md) | Source-repository requirements and observed review precedents |
| [Proposed report schema](schemas/playtest-report.schema.json) | Draft structure for candidate reports; not an evaluator |

## Contributor

**Haotian Xu**, creator of AI Game Bench.

- Publication email: ht@mopan.ai
- Professional profile: [LinkedIn](https://www.linkedin.com/in/xuhaotian/)

## Publication scope

Publish only independently prepared methodology, reviewed examples and task-specific materials suitable for public use. Keep credentials, account information, internal services, creator conversations, raw historical runs and private project files outside this repository.

These materials have not been submitted as an OpenRSI Discussion and no approval or task-generation result is claimed. The full scientific contract, usable source and asset delivery must be established before the final proposal is submitted through [the contribution workflow](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md).
