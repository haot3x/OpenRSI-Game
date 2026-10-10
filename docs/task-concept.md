# Proposed Research Task for Evidence Based Game Playtesting

This task would study how an agent explores a game and assesses the evidence it gathers. Game creation systems in the proposed corpus are limited to Codex and Claude. The scientific contract below is a draft; the corpus, reference implementation, score and compute budget remain to be confirmed.

## Scientific question

Can improved browser exploration and evidence assessment increase correct requirement judgments on frozen game artifacts under a fixed model, tool interface and experiment budget?

Testing a game requires reaching relevant states. A playtester may fail to observe a functioning mechanic, mistake incidental score changes for the required behavior, or mark a feature as passed without demonstrating it. The proposed task tests whether different exploration and evidence strategies reduce these errors.

## First experimental scope

A bounded falling-block game task is a candidate starting point. Observable requirements may include opening and starting, gravity, movement bounds, rotation, locking and stacking, line clearing, scoring, game over and restart.

Use a frozen corpus with independently verified working and defective behaviors. State which examples are development material and which are evaluation material, and record prior exposure. Do not claim hidden evaluation merely because labels are absent from the playtester interface.

The two creation systems identify the origin of corpus games. They are not the optimization target in this task. Withhold creator identity from the playtester where practical. A small corpus does not support a general ranking of Codex and Claude.

## Research loop and action space

The research agent forms a hypothesis, changes the candidate playtesting method, runs the fixed experiment, observes bounded feedback and updates the hypothesis.

Candidate changes may include action planning, exploration order, allocation of the interaction budget, when to wait or use an in-game restart, and the reasoning that connects evidence to a requirement. The deliverable would be an executable policy and evidence-linked requirement reports.

Keep game bytes, requirements, reference labels, model and tool versions, budgets and scoring fixed. Game repair, label changes, answer hard-coding, evaluator tampering and fabricated results are prohibited.

## Reference baseline

Before submission, identify a pinned reference implementation that performs the same task with the same observations and budget. Document its source files, invocation, model configuration, report interface and relationship to the candidate.

A human-authored requirement-by-requirement exploration policy is a possible baseline. It has not yet been implemented or selected in this repository. A raw historical comparison score cannot substitute for a matched baseline.

Baseline reproduction is a later execution step. The proposal must make the reference materializable without inventing a measured score or requiring the task builder to choose the scientific baseline.

## Proposed scoring approach

One candidate metric is balanced correct-decision rate over independently labeled passing and failing requirements:

`0.5 × (correct passed decisions / known passing requirements + correct failed decisions / known failing requirements)`

This requires positive denominators for both classes. An unverified decision receives no correctness credit and stays visible as an abstention. The exact unit of aggregation, weighting across games and requirements, eligible population and handling of invalid candidates must be confirmed before this becomes the task score.

Report missed defects, false alarms, decision coverage and observation cost alongside the optimized scalar. Separate infrastructure, timeout and incomplete evaluation from game defects. By default, invalid candidate artifacts are unscored; the final contract must make this explicit.

The task-owned evaluator compares candidate reports with fixed reference labels and validates declared evidence. A structurally valid report is not proof that its decisions are correct. Independent labels must come from a documented deterministic probe or review within the declared behavior scope.

## Execution and feedback

Define the playtester's observations and allowed inputs before implementing the task. A candidate interface is screenshot observation plus coordinate clicks, bounded key inputs, waiting and in-game restart. Evaluation should not reveal creator conversations, hidden answers or undeclared game state.

Specify the action, wall-time and inference budgets and whether every retry, replacement and resampling consumes them. Return aggregate scores and bounded diagnostics sufficient for research, with the answer boundary defined in advance.

The execution path must work in the current RSI-Harness. A native browser process inside a task container is a possible adaptation, pending validation. Do not assume a host Docker socket, privileged nested Docker or sidecars. The current shared Work/Judge snapshot and Judge-only injected tests do not provide an independent clean-base verifier; integrity claims must respect that limitation.

Record Work and Judge resources and estimated runtime separately. The admitted lane is one physical node with no more than eight GPUs at peak; CPU-only tasks are eligible. The proposed budget should support repeated research loops. Exact resources and timing are unresolved.

These execution requirements follow the [official proposal rubric](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/.agents/skills/proposal-agent/references/task-proposal-rubric.md).
