# Evidence-based game-playtesting research

The scientific question is whether improved visual exploration and evidence
assessment increase correct judgments of game mechanics under a fixed budget.
The current concrete implementation is defined in [the v0.1 contract](evaluation-contract.md).

A policy must place falling blocks to create a completed row, then establish
whether it disappears and whether clearing produces a separate score reward.
The human-authored baseline greedily chooses horizontal placements without
rotation or lookahead. Research candidates can test hypotheses about perception,
rotation/search, exploration order, budget allocation and evidence selection.

This relates to OpenRSI as evaluation-method research: an outer research agent
iteratively improves another agent's reusable testing policy. The intended
comparison is a policy versus a matched reference, not a once-only comparison of
Codex and Claude game-generation scores. No model weights are trained in v0.1.

Historical [selected report findings](../reports/README.md) motivate the task:
a natural run left working line-clear behavior unverified, while a later
controlled probe demonstrated it. Historical AI claims do not become gold labels.

The public corpus has only two Codex-generated base games. Claude Code findings
are contextual, with their actual MiniMax-M3 provenance preserved. The controlled
mutants, starting boards and disjoint seeds enable reproducible experiments,
but they are not a broad game benchmark or evidence of cross-model generality.
Final scientific usefulness and inclusion remain subject to independent review.
