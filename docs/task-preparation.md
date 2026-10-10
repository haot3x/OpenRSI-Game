# Delivery and approval workflow

## Current delivery

- Executable code: native Chromium browser interface, candidate JSON protocol,
  evidence certificates, validator and balanced scorer in `gamebench/`.
- Public assets: four approved game-only files and file digests in `assets/`.
- Baseline: human-authored greedy non-rotating policy in `reference/policy.py`;
  Solution materializes it by copying, without training or evaluation.
- Scoring: [fixed v0.3 contract](evaluation-contract.md), 48 development cases,
  96 full evaluation cases, two behavioral requirements, 16 actions per case.
- Harness package: schema 1.4 task, ordinary Docker environment, shared
  Work/Judge, zero GPUs and Judge-only injected tests. The deterministic source
  archive supports the standard environment-only Docker build context.
- Selected reports: Codex and Claude Code [publication extracts](../reports/README.md).
- Measured execution and format results are recorded in [validation.md](validation.md).

There is no runnable Claude Code game in v0.3. New model calls and broader game
collection are not part of this submission. Counting controlled variants as
independently generated games would misrepresent corpus size.

## Official sequence

1. Submit the complete proposal to the OpenRSI-Index **Task Ideas Discussion**.
   It must link this public source at an immutable commit and define the
   baseline, objective, metric, boundaries, assets and compute.
2. Their dispatcher reviews the scientific and execution contract. Revisions
   must address its actual feedback; an executable package alone does not
   establish scientific eligibility.
3. After proposal PASS, the official workflow can automatically create a
   task repository and build/review the environment. This local package is
   contributor-provided source, not a claim that official task generation ran.
4. The pipeline later requests the complete native proposal-session trajectory.
   Use a separate public-only session. A session that read private local material
   must not be uploaded or filtered into an apparently safe native trajectory.
5. The maintainers independently review and reproduce the task. Proposal PASS,
   trajectory delivery and final benchmark inclusion are separate results.

The contributor explicitly authorized direct Discussion submission and runnable
Task publication in this session; another permission round is not needed for
those actions. No approval or inclusion is claimed before it occurs.

Follow [CONTRIBUTING.md](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md)
and the [official discussion lifecycle](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/.agents/skills/proposal-agent/references/discussion-lifecycle.md).
