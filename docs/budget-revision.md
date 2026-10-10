# Fixed interaction-budget revision

The 40-action protocol tests whether improved perception, placement planning
and evidence assessment can make more reliable mechanic judgments with fewer
interactions. The same budget applies to the unchanged human-authored greedy
reference and every candidate. The policy has not been weakened; its SHA-256
remains `4c40a0f2ccc2605493fb37be29f4d807218a4cd64e359a311cf199488ac6a493`.

Only the action budget changes from 80 to 40. Both games, three controlled
interventions, 48 development cases, 96 Judge cases, seeds, 30-second case
limit, observation API, certificate requirements and balanced score remain
fixed. No examples are dropped because of their outcome. Valid abstentions
retain zero credit; invalid and incomplete evaluations remain unscored.

Paired development exploration measured 0.8125 at 80 actions and 0.6875 at
40 actions over the same 48 cases. The tighter budget was selected from
development measurements before evaluating the revised full Judge. A lower
development score does not prove that the full baseline satisfies the
validator's headroom requirement, and is not an Agent improvement result.

The original 80-action full score of 0.875 remains a historical comparison.
The revised full baseline must be reproduced separately. This source revision
does not claim revised proposal acceptance, an Agent trajectory or final
OpenRSI-Index inclusion. Subsequent validation records are separate from the
historical baseline files.
