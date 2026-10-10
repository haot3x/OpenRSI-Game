# Local validation — October 10, 2026

This is contributor-side validation, not OpenRSI approval, independent maintainer
reproduction or an official research-agent run. Containers used Linux/arm64,
4 CPU cores and an 8 GiB memory limit, zero GPUs and `--network none`.
The pinned Playwright 1.62.0 image reported Chromium 151.0.7922.34.
Memory consumption was not separately profiled; 8 GiB is the imposed limit.

## Historical 80-action baseline reproduction

The reference is the human-authored greedy, non-rotating visual policy in
`reference/policy.py`, SHA-256
`4c40a0f2ccc2605493fb37be29f4d807218a4cd64e359a311cf199488ac6a493`.
Candidate and reference use the same observations, budgets and scorer.

| Protocol | Cases | Eligible judgments | Correct positive / total | Correct negative / total | Score | Local elapsed |
| --- | --- | --- | --- | --- | --- | --- |
| Development | 48 | 80 | 39 / 48 | 26 / 32 | 0.8125 | 9.039 s |
| Full evaluation | 96 | 160 | 84 / 96 | 56 / 64 | 0.875 | 15.515 s |

Full evaluation recorded 2,385 actions, 20 abstentions and zero unsupported
decisions. Development recorded 1,383 actions, 15 abstentions and zero unsupported
decisions. These are two measured executions of the declared protocol, not
across-run variance estimates. The completeness field `official_full_run` in
the JSON means the full local protocol ran; it does not mean Foundation approval.

The full run invoked the actual Judge entry point:

```sh
docker run --rm --network none --cpus 4 --memory 8g \
  -v "$PWD/tests:/tests:ro" -v "$PWD/runs/final:/logs/verifier" \
  openrsi-game:0.1 bash /tests/test.sh
```

Records: [development](../baselines/greedy-dev.json),
[full evaluation](../baselines/greedy-judge.json).

## Correctness and boundary checks

- All six independent I/J/L controlled probes passed: two game families ×
  original, removal-disabled and reward-disabled mechanics. They used normal
  keys after an explicitly intervened initial setup. [Records](../baselines/oracle-checks.json).
- Five scoring tests passed, covering unsupported claims, adjacent-frame
  certificates, conditional eligibility, malformed references and balanced
  aggregation/abstention.
- A policy submitting unsupported positive decisions on all 48 development
  cases scored 0 with 80 unsupported judgments. It did not earn credit for
  correctly guessing the positive class.
- An invalid/exiting candidate produced `candidate_invalid` with `score: null`.
- Replacing Work's public `aggregate` with an always-one function did not affect
  injected Judge scoring: development remained 0.8125. This tests that specific
  bypass, not general malicious-code isolation.

## Format compatibility

The official RSI-Harness `HarborTaskCompiler` at OpenRSI-Index commit
`dcfbc43b117b92d276837aa0d48f291d544fcf7a` successfully compiled this task using
its Harbor 0.21.0 dependency and schema 1.4. It resolved the standard
`environment/` build context, `/workspace/openrsi-game` working directory,
Work/Judge zero GPUs and disabled network. No full paid-agent Harness run was
performed. The normal offline container image build and exact Judge script were
tested separately; this is stronger than just checking TOML syntax, but does
not assert every production deployment path has been tested.

## Budget estimate

Plan one physical node with 4 CPU cores, 8 GiB RAM and zero GPUs in both phases.
Reserve up to 30 minutes for Work hypothesis/code/development experiments,
15 minutes for full Judge (its enforced deadline), and 5 minutes overhead per
adaptive research loop. This is a planning estimate, not measured agent time.
It allows at least 20 complete loops in 24 hours or 40 in 48 hours with margin.
Default research budget is 24 hours, normally extendable to 48. Baseline scoring
was much faster locally; new policies may take longer and are still budgeted.

This validation cannot resolve the two-game corpus limitation, public fixture
exposure, transfer to other genres or need for a future Claude Code game artifact.
Those remain scientific review considerations.

## 40-action revision

Version 0.2 retains the exact same greedy reference, games, fixture seeds,
evidence rules and balanced scoring, with 40 actions per case for every policy.
A paired 48-case development exploration measured 0.8125 at 80 actions and
0.6875 at 40 actions; both had zero unsupported judgments. This exploration
used the pinned original source with only its action counter/limit adjusted.
The full revised Judge baseline and validation status are not yet measured
at this source-package revision. The 0.875 historical result must not be used
as the matched 40-action baseline. See [the revision](budget-revision.md) and
the public repository's submission record for subsequent validation results.
