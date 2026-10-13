# Local difficulty pilot — 2026-10-13

This isolated, development-only prototype responds to Discussion #209's
request for more research headroom after the old Agent's first formal Judge
submission scored 1.0. The earlier trajectory also shows pre-submission
iteration: full development accuracy improved from 0.8125 to 1.0. Both facts
are retained; first formal submission and first attempt are different.

## Fixed pilot protocol

Two already-public Codex games × three interventions × four structures ×
two fixed seeds = 48 development cases, 80 eligible judgments (48 positive,
32 negative). Every policy receives 32 actions and 30 wall seconds per case.
The observation protocol, seeded natural bag, game mechanics, evidence
certificates and balanced metric are unchanged. The reference algorithm is
unchanged. No private project files or other creation platforms are included.

The structure groups are stepped gaps, separated gaps, sparse overhangs and
uneven stacks. The feasibility-only generator uses the natural seeded bag to
find legal witness paths; it never uses control-policy scores to select cases.
Each selected board has no initial full row or immediate rotation/hard-drop
clear by its first piece. Witnesses are authoring validation material outside
candidate inputs. A witness has privileged seed knowledge, so it is not an
observation-only policy or a scored candidate result.

Version 1 allowed a nearly-full roof shortcut: both old strong controls scored
0.9375 and the overhang group scored 1.0. Version 2 uniformly replaces that
overhang rule with a sparse roof over a necessary floor gap. The other three
structure groups are byte-identical. Every attempted result is retained in
the local evidence; no individual failing case was cherry-picked.

## Measured version-2 results

Aggregate results and policy digests are recorded in
[the pilot measurement record](../baselines/difficulty-pilot.json).

All 48 legal witness replays passed in native Chromium 151.0.7922.34. The
longest path used 24 actions. No impossible or timed-out case was scored as
an ordinary game failure.

| Observation-only policy | Balanced score | Correct positive / negative | Wall seconds |
| --- | ---: | --- | ---: |
| Unchanged human greedy reference | 0.25 | 12/48; 8/32 | 8.041 |
| Old final-perfect control, budget-table extension only | 0.75 | 36/48; 24/32 | 9.146 |
| Same control plus legal motion search | 0.9375 | 45/48; 30/32 | 9.127 |

The original first-perfect control also scored 0.0 on the 12 newly changed
overhang cases. Reusing its 36 byte-identical version-1 cases yields a
composed development score of 0.6875. This is labeled evidence reuse, not a
fresh 48-case run.

The three table rows are complete 48-case development measurements with zero unsupported
decisions. These scores must not be called full-Judge results or directly
compared to the historical 0.625 full-Judge score from the old 16-action task.
The old final policy has one necessary compatibility adjustment: its existing
budget table is extended from 0..16 to 0..32; no planner or evidence rule is
changed. Its original SHA and adapted SHA are retained in the result record.

The motion extension is a hand-authored methodology prototype. It searches
legal rotation/down/horizontal paths for an immediate clear, then falls back
to the old planner when no such clear exists. Its only input is rendered
observation JSON; it reads no fixture, seed, file, witness or oracle. Its source
passed the private task's fixed syntax/import/access gate. It is not a new
Codex research-Agent experiment.

The overhang group's score rose from 0.25 to 1.0 with this extension, while
all three other group scores stayed the same. Thus there is a specific,
solvable planning weakness, rather than difficulty caused by infrastructure.
The final prototype still misses one separated-gap geometry (five eligible
judgments across its three interventions).

## Limits and next step

Two seeds per structure are too few to establish research difficulty or
cross-game generalization. Public fixtures and authoring-time controls are
not a hidden holdout. The generic extension already scores 0.9375, so a new
frontier Agent could still saturate quickly. This pilot supports the spatial
planning direction; it does not establish maintainer acceptance or sufficient
headroom for an eight-hour experiment.

Next, strengthen multi-piece/separated-cavity planning, author and validate
separate 96-case full fixtures, remeasure the unchanged baseline, and check a
short formal Codex run before spending the longer budget. The published private
task, bundled Harness, old experimental trajectory and Discussion proposal
remain unchanged by this local pilot.

Run only the development interface in this prototype. `--split judge`
deliberately fails because the full fixtures have not been authored. The
historical full-Judge entry point must not be used to claim readiness here.
