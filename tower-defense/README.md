# Experimental twelve-wave tower-defense benchmark

Research candidate for OpenRSI Discussion209. This changes the prior Task's goal from single-event evidence classification to complete-campaign strategy optimization; maintainer scope approval and inclusion remain pending. It is not the canonical Tetris task.

Base game: [Tiny Tower Defense](https://aigamebench.com/play/tiny-tower-defense), publicly displayed creator metadata **Codex / GPT-6.1 Sol / High effort**. Original public-only game assets are pinned in source.json. The twelve-wave campaign, two routes, randomized build sites, resistance/forecast and resale rules are benchmark-authored additions. They do not describe defects in the original game.

Optimize the mean fraction of the whole campaign's predeclared enemy threat intercepted. Threat is an enemy's base-damage weight, counted once on a kill. All later unspawned threats remain in the denominator if the base falls. The policy handles economy, placement, upgrades, Arrow/Magic resistance tradeoffs and a two-wave forecast. No model service or GPU is required for gameplay evaluation. Read instruction.md for the fixed policy boundary and budget.

Run the cost-free development evaluator on CPU:

```sh
docker build --platform linux/amd64 -t openrsi-tower:pilot tower-defense
mkdir -p tower-results
docker run --rm --platform linux/amd64 --network none --cpus 4 --memory 8g --shm-size 1g \
 -v "$PWD/tower-results:/results" openrsi-tower:pilot \
 python3 -B towerbench.py --policy candidate/policy.py --seeds 8100 8101 8102 8103 --pressure 2 --output /results/dev.json
```

A fixed coverage-greedy reference scored **0.521505376344086** on these four development campaigns. Separate private full-Judge acceptance on eight frozen campaigns measured **0.2553763440860215**. These are baseline/control validations, not an Agent improvement curve or maintainer acceptance. Fresh cold-Agent difficulty results are still pending. All exposed pressure calibrations, including a rejected near-saturated easy variant, are retained in the private review evidence.

The Foundation private experimental branch contains the complete Harbor wrapper, injected scope-protected Judge, separately frozen Judge cases, validation and RSI-Harness trajectory. Judge seeds and per-case feedback are excluded from Work; this public repository supplies the generator, all mechanics and development cases. No secret benchmark corpus, broad game transfer or malicious-code isolation is claimed. Candidate policies must not reverse seeds or use case-specific solution tables.

Only public game assets and independently authored methodology/code are published here. No company internals, raw Bench jobs, user accounts, commercial reports or mixed operator conversations are included. Earlier Tetris code, tasks and experiments remain preserved.

Contributor: Haotian Xu, creator of https://aigamebench.com/ and cofounder of https://mopan.ai/.
