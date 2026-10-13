# Local difficulty pilot contract (full Task revision pending)

## Research scope

Optimize an executable visual playtesting policy, not game quality, creation
speed or a Codex-versus-Claude ranking. The falsifiable hypothesis is that
improved state estimation, planning and evidence selection increase verified
judgments under the same interaction budget as a fixed greedy baseline.
This is an evaluation-method research prototype motivated by AI-generated game
testing. It does not demonstrate recursive weight improvement or broad
cross-game generalization by itself.

## Assets and workload

`assets/manifest.json` records file digests and actual creation identities for
two previously reviewed public games: Codex CLI 0.155.1, gpt-6-astra and
gpt-6-sol, both medium effort. The public website iframe-height bridge was
removed; base game mechanics were preserved. Apache-2.0 release is authorized
by the contributor. All game code and assets are local, with no remote runtime
dependencies. Claude Code report extracts are contextual material; there is
no runnable Claude Code game in v0.1.

`gamebench/fixtures.py` defines three interventions per game: original mechanics,
row removal disabled, and clear reward disabled. These defects are task-authored,
not claims of defects in the original generated games. The verifier checks the
frozen asset digests, requires exactly one occurrence of each adaptation anchor,
and instruments lock events. Initial boards use four deterministic geometry families: stepped gaps,
separated floor gaps, reachable overhangs and uneven stacks. A feasibility-only
authoring search rejects initial full rows and immediate one-piece clears,
then finds a legal path within 32 actions. Board selection never uses any
control-policy score. Bag shuffling uses the original fixed PRNG.
Controls and game logic then run normally, with an explicitly controlled clock.
This is intervention-based testing, not historical natural gameplay replay.

Development: both games × three variants × seeds 10–17 = **48 cases**.
Planned later evaluation: both games × three variants × seeds 100–115 =
**96 cases**. It has not been authored or validated in this local pilot;
`--split judge` deliberately fails rather than returning an old-workload score.
The planned full workload would have 160 eligible requirement judgments: 96 passing
and 64 failing. Score-on-clear is excluded only for row-removal-disabled cases.
Both sets have a fixed shuffled order. Every case gets a fresh browser context
and candidate process, so state and browser storage do not carry between cases.
These are repeated interventions on **two implementations**, not 96 independent
games. Public fixture source and seed ranges are intentionally exposed for audit;
the split is not secret or free of prior exposure. Do not present it as one.

## Candidate boundary

Submit only a self-contained, standard-library `candidate/policy.py`, ≤1 MiB.
It consumes JSON on stdin and produces actions or a report on stdout. The
observations are rendered board cell-center RGB samples, frame number, visible
score/line counters and overlay text. Optional board PNGs show the same visible
board; every policy can request the same observation option. The reference
uses RGB samples. No JS state, source, labels, creator identities or variant
IDs are part of the policy API. The field `requirements` always contains both
requirements, including when one is ineligible, to avoid revealing a variant.

Allowed research changes include perception heuristics, placement search,
rotation/lookahead, exploration allocation and evidence assessment. Fix assets,
requirements, browser/dependencies, interventions, seeds, budgets and scorer.
Reading files/processes/environment/browser internals, importing task-owned
modules, identifying cases from their order or accessing oracle events from the
policy is prohibited. Candidate-visible development observations may be retained
for offline experiments. No new game collection, web search, external services
or paid model calls are permitted. No candidate model inference is required.

## Budget and lifecycle

Each case permits 32 actions and 30 wall seconds. A key press advances 32
simulated ms; a wait is 16–2000 simulated ms. The clock advances rAF callbacks
in steps ≤16 ms; it is fixed by the evaluator, not candidate-controlled beyond
bounded waiting. Allowed keys are Enter, ArrowLeft/Right/Down/Up and Space.
Restarting in-game, repeated actions and waiting consume the same action budget.
There are no automatic retries, substitutions or replacements. Returning a
valid report early ends the case; unfinished requirements may be unverified.
Deadline checks apply to every policy message. The full Judge deadline is 900 s.

The candidate is evaluated directly in a single pass. Solution copies the fixed
reference policy; it does not train, evaluate or run a live paired baseline.

## Independent reference checks and evidence

`tests/check_oracle.py` tests all six family/variant combinations independently
of the candidate. It sets an empty board and the first pieces I/J/L, then uses
normal start, movement and drop keys to complete the bottom row. It verifies
that original mechanics remove the row and add clear points, `no_clear` leaves
the full row, and `no_reward` removes the row without a clear bonus.

During candidate evaluation the oracle observes each actual lock. A certificate
exists only when at least one row was completed. Removal passes only when the
line counter advances and no full row remains. A clear reward passes only when
the score rises **inside lock**, after drop points have already been counted.
If removal fails, the reward requirement has no eligible event. The candidate
never receives these certificates. Every scored decision must cite the adjacent
frame pair before/after an event supporting that requirement and judgment.
Counter changes without a completed-row certificate receive no credit. The
certificate proves the scoped observed event, not all possible game behavior.

## Scalar and failures

For every eligible judgment, correctness is 1 only when both the label matches
and the cited event supports it. Otherwise correctness is 0. Optimize:

`0.5 × (correct passing judgments / 96 + correct failing judgments / 64)`

for the full evaluation. It is unitless in [0,1], higher is better. Development
uses its own fixed denominators (48 positive, 32 negative). Equal class weighting
prevents always-pass from benefiting from the positive majority. Abstentions,
unsupported claims and incorrect decisions earn no credit and are reported.

A missing/oversized policy, malformed report/action, invalid frame, process
crash, attributable Python failure, deadline or incomplete evaluation is
**unscored** with `score: null`. Infrastructure failures are measurement-unavailable,
also unscored. Neither is a game defect. A complete, valid but inaccurate or
unsupported report can receive a finite zero. The historical `tests/test.sh` full-Judge path is unavailable for this
development-only revision. No formal reward or full-Judge result is claimed.

Feedback: aggregate score, class/correct counts, eligible/abstention/unsupported
counts, total actions/time, policy digest, browser version and status. No
per-case identities, labels, certificates or outcomes are returned by default.
Public probe/source exposure remains disclosed. `--limit` is a smoke test and
is never marked `official_full_run`.

## Harness and limits

One native Chromium subprocess runs within the same task container. No Docker
socket, nested Docker, sidecar, added devices or privileged mode is required.
Work and Judge each use one physical node, 4 CPU cores, 8 GiB RAM, zero GPUs;
peak remains the same. Network is disabled at task runtime; a browser route also
aborts requests. Public dependency/image downloads occur during image build.

RSI-Harness uses the shared Work/Judge snapshot and Judge-only injected tests.
The public protocol and asset checks do not create an independent clean Base
or a secure execution boundary against malicious Work-root code. They reduce
accidental changes and false claims; final inclusion needs independent review
and reproduction. Public answers, only two implementations and adaptation to
seeded fixtures are substantial overfitting limits. Improvements here cannot
establish broad model capability or natural-gameplay generalization.
