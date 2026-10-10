# Methodology for Evidence Based Game Evaluation

Evaluate what a game demonstrably does under a declared protocol. Keep game behavior, evaluator judgment and report validity separate so that a failure to explore is not reported as proof of a game defect.

## Separate creation from evaluation

Freeze the delivered game and its requested behaviors before playtesting. Evaluate it in a fresh session that does not receive the creator's conversation, self-assessment or previous evaluation verdicts.

Record the creation tool, actual model, revision and relevant settings separately. Limit corpus creation systems to Codex and Claude. Independent sessions reduce context leakage but do not, by themselves, establish an unbiased or calibrated judge.

## Define observable requirements

Each requirement needs an operational definition and a condition under which evidence is sufficient. For example, scoring after a line clear needs evidence of the row clearing and its associated score change; a score increase after a hard drop is insufficient.

Avoid using one screenshot to infer behavior that requires a sequence. Record the relevant state before an action, the action and its timing, and the resulting observations. Only evaluate behaviors required by the task.

## Keep three judgment states

| State | Meaning |
| --- | --- |
| Passed | Observations support the declared requirement within the tested scope |
| Failed | Observations demonstrate a violation of the declared requirement |
| Unverified | The observations do not establish either conclusion |

Budget exhaustion, unsuccessful exploration and a missing critical observation can produce unverified judgments. They are not interchangeable with an observed defect. If a scoring policy assigns no points to unverified decisions, preserve their meaning and report them separately.

Infrastructure errors, incomplete trials and invalid evidence are unavailable measurements. Keep their counts and causes visible rather than silently replacing trials or converting them into game failures.

## Link decisions to independent evidence

Use observation identifiers assigned by the browser recorder. The recorder should retain the input, timing, before/after observations and applicable conditions. Validate that report references belong to the correct case and resolve to the retained evidence.

Structural validation confirms that a report has the expected fields. Evidence validation confirms that observations exist and match the record. Semantic validation asks whether they justify the decision. These checks serve different purposes.

The [draft report schema](../schemas/playtest-report.schema.json) defines a proposed structure only. It does not validate the behavior of a game or the truth of a claim.

## Hold comparison conditions fixed

Pin game bytes, requirement versions, browser/model/tool versions, viewport, initial-state policy, randomization, inference settings, budgets and retry accounting. Distinguish source-controlled artifacts from mutable hosted previews.

A controlled setup used for diagnosis or reference-label establishment must be documented separately from ordinary independent play. It may establish a bounded behavior under that setup; it must not overwrite the outcome of an earlier trial with different conditions.

Keep cost estimates separate from actual charges. Record unknown values as unknown. Do not normalize an incomplete score into a full capability claim without explaining its coverage and denominator.

## Calibrate the evaluator

Freeze reference labels independently of the candidate. Include known passing and known failing cases for the behaviors being measured. Track missed defects, false alarms, abstention, decision coverage and repeat stability.

Repeated requirement judgments from the same game are correlated observations. A small development suite does not establish general game-quality accuracy, and exposed development cases cannot become holdouts by renaming them.

Any candidate improvement must use matched conditions and a declared feedback boundary. Repeat evaluation when observed variability could change the conclusion, and preserve previous records rather than relabeling them to fit the model.
