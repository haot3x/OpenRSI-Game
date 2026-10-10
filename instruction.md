# Improve evidence-based game playtesting

Research whether better visual state estimation, placement planning and evidence
assessment improve functional judgments on fixed AI-generated browser games.
Change a candidate, measure it, revise your hypothesis, and repeat. Record the
hypothesis and result for each experiment in your own research notes.

The deliverable is `candidate/policy.py`, a self-contained Python 3 policy using
only the standard library. `reference/policy.py` is the human-authored greedy
non-rotating baseline. Start with `bash solution/solve.sh` in a local checkout;
in Work the candidate is already initialized to that same baseline.

Each fresh policy process receives one JSON line per observation on stdin.
Respond with exactly one JSON line on stdout:

```json
{"action":{"key":"ArrowLeft"}}
```

or `{"action":{"wait_ms":800}}`, or a final report:

```json
{"final":{"line_clear":{"status":"unverified","frames":[]},"score_on_clear":{"status":"unverified","frames":[]}}}
```

Observations include `frame`, the board's 20x10 rendered RGB cell-center samples,
visible `score`, `lines`, and overlay text/visibility. Optional board PNGs can be
enabled with `--images`; they depict the same board. No JavaScript game state,
source, creator identity, seed, variant, or oracle event is delivered to a policy.
Allowed keys: Enter, ArrowLeft, ArrowRight, ArrowDown, ArrowUp, Space. There are
40 actions and 30 wall seconds per case. A key advances 32 simulated ms; a wait
advances 16–2000 simulated ms. Restarts and repeated inputs consume that budget.

Both requirements use `passed`, `failed`, or `unverified`. A positive or negative
decision must cite at least two frames, including the adjacent before/after pair
of a real completed-row lock event that certifies that particular decision.
Unsupported claims get no credit. Absence of observation does not prove failure.
Scoring after clear excludes drop points. If removal is disabled, score-on-clear
is ineligible; it has no event on which to assess the conditional behavior.

The development workload is 48 cases; full evaluation is 96 cases, from two
reviewed Codex games, three controlled variants and disjoint setup seeds.
The primary score is balanced evidence-supported correct-decision rate in [0,1],
higher is better. See [the contract](docs/evaluation-contract.md) for exact rules.

```sh
python -m gamebench.evaluate --policy candidate/policy.py --split dev --output runs/dev.json
```

You may change only `candidate/policy.py` for the submitted policy. You may write
research notes and development logs separately. Do not change game assets,
fixtures, budgets, labels, evaluator, reference baseline, dependency environment
or scoring. Do not read files, environment variables, process state, browser
internals or oracle data from the policy; its only input is the JSON protocol.
No web search, external services, paid inference or additional game collection
is allowed. Locally generated development observations within the fixed task
are allowed. A malformed candidate, crash, timeout, infrastructure failure or
incomplete evaluation is unscored, rather than a game defect or finite zero.

This public v0.2 is a proposal/review prototype. The 40-action protocol retains
the original greedy reference unchanged; old 80-action scores are historical
comparisons, not its matched baseline. Only two game implementations
are represented. Public seeds, variants and probe source are exposed for audit;
this is not a secret or contamination-free held-out corpus, or a general model
ranking. RSI-Harness uses the shared Work/Judge snapshot and Judge-only tests;
the protocol restriction is not an OS sandbox against a malicious Work agent.
