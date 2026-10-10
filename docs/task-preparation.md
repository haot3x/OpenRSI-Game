# Steps to Complete the OpenRSI Task Package

The public documentation and report interface draft are available in this repository. Four substantive components still need completion before the proposal can define a reproducible task: executable code, game assets, a reference baseline and a fixed scoring protocol.

## 1 Prepare independent public code

Build a small implementation containing only the task's browser observation/input interface, evidence recorder, report validation, reference policy and scoring logic. Develop it independently in this repository or use a suitable public upstream with documented provenance. Do not move an internal application or copy its service integrations into this project.

Required evidence for review:

- Public source files and an immutable commit.
- Dependency versions, installation instructions and declared licensing.
- The launch and evaluation paths, with expected artifact/report interfaces.
- A verified execution route compatible with the current RSI-Harness.

A JSON schema and methodology documents are useful preparation, but do not constitute an executable reference environment.

## 2 Deliver a frozen game corpus

Confirm whether Claude means the Claude Code tool or an official Claude model before admitting samples. Every sample must record the actual tool, model and version. Keep the two creation-system families as Codex and Claude.

For each eligible game, provide a reviewed, game-only artifact and a manifest containing an opaque case ID, file hashes, requested requirements, provenance, usage rights and relevant creation conditions. Remove account details, credentials, creator conversations, private assets and internal service dependencies.

Use existing approved public games where their delivery and rights are sufficient. New generation is not required merely to write the proposal. If it is necessary, define a bounded collection plan separately before making model calls.

Independently establish labels with a documented deterministic probe or review. Include positive and negative coverage. Freeze manifests, splits and labels, record prior exposure, and verify eligible distinct case counts before choosing a workload size. Keep label delivery separate from candidate-visible inputs.

There is currently no game corpus or reference-label delivery in this repository.

## 3 Freeze the reference baseline

Select one reference method before optimizing candidates. Its source, configuration and invocation must be pinned, and its outputs must be scoreable by the same evaluator as candidates.

Possible starting design: a human-authored policy that explores each requirement in a fixed order, records observations and abstains when sufficient evidence is missing. This is a design option, not an existing baseline.

Document what the research agent may change and what stays fixed. Task generation should be able to materialize the baseline without making another scientific choice. Label any reported result as unreproduced until it is actually reproduced.

## 4 Confirm and implement the scoring protocol

Resolve these choices before final submission:

- The optimized scalar, direction, units and aggregation across games and requirements.
- The fixed workload and inference/interaction/time budgets, including retry and replacement accounting.
- What counts as sufficient evidence and how independent reference labels are established.
- The distinction between incorrect decisions, unverified decisions and unavailable measurements.
- Invalid-candidate behavior, feedback returned to Work and the answer boundary.
- Model/service access, network and additional-data rules.
- Work and Judge resources and contributor-estimated duration of a complete scoreable experiment.

The balanced correct-decision rate in [the task concept](task-concept.md) is a proposed metric. No score or measured improvement is currently published.

## Submission sequence

1. Complete and pin the necessary source, baseline and concrete asset delivery.
2. Confirm the scientific contract and check it against the [official rubric](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/.agents/skills/proposal-agent/references/task-proposal-rubric.md).
3. Use a dedicated proposal session containing only approved public materials. Review and confirm the complete official proposal before Discussion submission.
4. Submit to Task Ideas through the [contribution workflow](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md).

The workflow later uploads the complete original proposal session. A session that has read private material must not be used for that upload, and its native history must not be filtered. See the [official trajectory instructions](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/.agents/skills/proposal-agent/references/discussion-lifecycle.md).
