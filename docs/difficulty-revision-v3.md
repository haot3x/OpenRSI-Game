# Spatial-difficulty revision 3

Revision 3 strengthens the board distribution uniformly, retaining the two
already-public Codex games, three interventions, observation interface,
32-action/30-second per-case budget, unchanged greedy reference and evidence
metric. It imports no additional games or private company material.

Stepped/uneven gaps widen to 7–9 columns with 4–7-row exterior stacks.
Separated cavities use alternating floor gaps with 2–6-row exterior posts.
Authoring accepts stepped witness paths using at least three pieces and
separated/uneven paths using at least four. This is a constraint on the found
witness, not a proof that every possible solution needs that many pieces.
Sparse overhangs remain, with a legal entry corridor adjusted for asymmetric
S/Z pieces. A failed full witness check (93/96) is retained; the corridor fix
changes the witness route, not the board geometries or measured policy scores.

All 48 development and 96 full witness replays passed in the actual browser;
the longest full witness used 26 of 32 actions.

The authoring search uses the natural seeded bags only to establish feasibility.
It never selects boards by a control-policy score. Solvability witnesses remain
outside candidate inputs. The dataset is public and authoring-time calibration
is not a hidden holdout.

| Policy | Development (48 cases) | Local public full protocol (96 cases) |
| --- | ---: | ---: |
| Unchanged greedy reference | 0.1875 | 0.21875 |
| Old final-perfect control, budget-table extension only | 0.50 | 0.5625 |
| Same control plus legal motion search | 0.6875 | 0.8125 |

All scored measurements completed with the same policy identities and fixed
budgets, no timeouts, and zero unsupported decisions. Full evaluation retains
160 eligible judgments, 96 positive and 64 negative. Full policy measurements
run in about 18 seconds on the local ARM image under 4 CPU / 8 GiB limits.
These are public-protocol measurements, not private Harbor Judge acceptance
or new autonomous RSI research. [Aggregate records](../baselines/difficulty-pilot-v3.json).

The larger unresolved group is multi-piece/separated-cavity planning. This
revision has more room for improvement than v2, whose motion extension scored
0.9375 on development. A short formal Codex pilot should establish actual
first-submission behavior before a longer experiment. The configured research
budget is eight hours; a separately disclosed short CLI override can be used
for that pilot. No long run is started by authoring this revision.

Earlier pilot evidence remains in [the historical v2 record](difficulty-pilot.md)
and its JSON. Do not reinterpret historical scores as matched v0.4 baselines.
