# Selected AI Game Bench report findings

These are contributor-authorized extracts of the reviewed local publication
reports, limited to Codex and Claude Code. They contain selected outcomes and
methodological context, not raw runs, creator conversations, account records,
internal paths, services, or other creation platforms. No new historical
evaluation was performed for this export.

## Report 001 — September 22, 2026

| Creation tool | Actual model / effort | Creation time | Evaluator claims: pass / fail / unverified | Provisional total |
| --- | --- | --- | --- | --- |
| Codex CLI 0.155.1 | gpt-6-astra / low | 240.269 s | 9 / 0 / 0 | 91.8315 |
| Claude Code 2.1.220 | MiniMax-M3 / unspecified | 197.811 s | 9 / 0 / 0 | 92.6263 |

Both were assessed by Codex CLI 0.153.4, gpt-6-astra at medium effort, using
screenshots in Chrome 153 at 1280×720. Recorded actions were 45 and 64,
respectively. The nine checks covered opening, gravity/new pieces, movement
bounds, rotation, stacking, clearing, clear reward, game over and restart.

The Claude Code row identifies the **tool**, not an Anthropic Claude model.
The underlying model in this record was MiniMax-M3. Do not use this row to make
claims about Claude model capability.

Totals are retrospective, platform-aware provisional scores normalized over
80/100 available weight. Actual creation charges were unknown; cost weight was
excluded. The initial browser state was operator-prepared rather than frozen.
There was one creation per tool. These are evaluator claims, not calibrated
ground truth or a capability ranking. `report_valid` checks reporting validity;
it does not establish that every claimed pass is semantically correct.
The selected records later reused in Report 003 are the same observations, not
a second independent trial.

Exact extracted checks and notes: [001-codex-claude-code.json](001-codex-claude-code.json).

## Report 002 — September 23, 2026

Both games were created with Codex CLI 0.155.1 at medium effort, one creation
and no repair prompts per model. The request was “A classic Tetris game”.
Evaluation used Codex CLI 0.153.4, gpt-6-astra at medium effort, Chromium 151,
1280×720, at most 60 actions and 300 seconds, one attempt and no automatic retries.

| Actual creation model | Creation time | Pass / fail / unverified | Demonstrated core points | Recorded actions |
| --- | --- | --- | --- | --- |
| gpt-6-astra | 210.111 s | 9 / 0 / 0 | 40 / 40 | 60 |
| gpt-6-sol | 185.029 s | 7 / 0 / 2 | 29 / 40 | 38 |

The Sol evaluator did not demonstrate line clearing or its associated reward.
The randomized run did not complete a row, and its initial viewport cut off the
board bottom. Drop points alone cannot establish a clear reward. These two
judgments were **unverified**, not observed defects.

A separate controlled QA check fixed the first pieces to I, J and L and then
used normal game inputs. Both games cleared a line. The visible scores changed
72→208 for Astra and 76→214 for Sol; those transitions also include drop points.
This establishes behavior under that intervention, not a new independent
natural-run result. The historical evaluator judgments remain unchanged.

There is no full 100-point total because subjective ratings and actual charges
are absent. The protocol differs from Report 001, so do not combine their totals.
One game per model cannot establish general relative capability.

Exact extracted checks and summaries: [002-codex-models.json](002-codex-models.json).
The two reviewed game-only artifacts are [available here](../assets/manifest.json).

## What this motivates

A functioning feature can remain unverified because an evaluator did not reach
the necessary state. Better exploration, viewport handling and separation of
clear rewards from drop points are testable evaluation-method hypotheses.
Historical AI claims are **not** the new task's answer key or matched baseline.
The runnable task independently exercises the two games and benchmark-authored
defects, using controlled setup and task-owned event certificates.
