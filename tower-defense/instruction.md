# Twelve-wave tower-defense strategy optimization

Improve a reusable controller's complete-campaign defense across randomized maps, tower sites and enemy compositions. Optimize mean intercepted enemy threat divided by the entire campaign's fixed total threat. A killed enemy earns its base-damage weight once. Leaks, surviving enemies and unspawned future enemies earn zero. Maximize [0,1]. There is no score bonus for ending early. This is strategy-policy optimization, not game repair or a model/platform ranking.

The base is the owner's publicly served Codex Tiny Tower Defense. The benchmark-authored extension has twelve waves, two route layouts, sixteen build sites, Arrow/Magic towers with three levels, physical/magic resistance, and a two-wave visible forecast. Initial gold150/base health24. Fixed difficulty pressure2. Combat is deterministic at30Hz. Actions occur between waves; every start advances the whole next wave, then pauses. Enemy themes and quantities vary. See source.json for provenance. No original-game defects are alleged.

Deliver only /workspace/openrsi-game/candidate/policy.py, a regular self-contained Python file <=1MiB. It starts as the fixed reference. Notes and local results belong only in research/ or runs/. All other files, source, assets, dependencies and reference remain immutable. Policy inputs are only its observation stream and standard-library computation. No files/environment/process/network/browser internals, seed/case recognition or fixed per-case answer tables. Work may inspect public source and run development experiments; all candidate selection happens in Work. A fresh policy process is used per campaign.

Each stdin line is {"observation":...}. Visible observation includes gold,health,completed_waves,wave_count,actions_remaining,route,pads and existing tower types/levels,tower_types static stats, and aggregate count/HP/speed/resistance/threat summaries of the next2 waves. It excludes scenario IDs,seeds,future spawn order and later waves. The research UI displays the same information. No vision model or external inference is needed.

Each response is one newline-delimited JSON object <=64KiB:
{"actions":[{"type":"build","pad":3,"kind":"magic"},{"type":"upgrade","pad":3}],"start_wave":true}

Use at most8 actions per response and72 across the campaign. Build uses exactly type,pad,kind (arrow or magic); upgrade uses type,pad; sell uses type,pad and refunds floor(55% of original build+paid upgrades). Only legal affordable operations are accepted. Empty actions are allowed. All feedback is objective strategy performance; invalid commands/crashes/timeouts receive no partial score. The campaign ends in won/lost after at most12 responses. Per-case wall deadline30secs; full Judge experiment300secs with a360sec container timeout. CPU4, RAM8GiB, zero GPUs, offline policy/evaluation.

Development command (4 fixed cases):
python -B towerbench.py --policy candidate/policy.py --seeds 8100 8101 8102 8103 --pressure 2 --output runs/dev.json

The fixed full Judge uses8 separately frozen campaigns, aggregate-only feedback, no per-case identities or future states. Fixed Judge seeds are not shipped in Work. Public generator and development seeds are exposed; broad transfer, malicious-code isolation and a contamination-free research corpus are not claimed.

Develop normally, test hypotheses, and call rsi-submit when your candidate is valid and ready. Inspect rsi-submit --list and its feedback. Continue improving policy quality and efficiency through the supplied research budget. Agent budget28800secs (eight-hour research experiment); Judge calls unlimited. This is a local research candidate, with final benchmark inclusion pending independent maintainer review.
