# Tower-defense strategy benchmark source, v2.0.1

Public source, assets, fixed reference and development protocol for the current
twelve-wave tower-defense submission. This version studies complete-campaign
economy, placement, upgrades/conversions and multi-wave planning. Review status
is pending; no benchmark inclusion is claimed.

The public source includes only this game's code and public development cases.
The formal Harbor Task and complete current experiment are in the Foundation's
private review repository. Current review:
https://github.com/OpenRSI-Foundation/game-playtest-evidence-d209
Discussion: https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/209

## Run the public development evaluator

From this directory:

```bash
docker build --platform linux/amd64 -t openrsi-tower:v2.0.1 .
mkdir -p runs
docker run --rm --platform linux/amd64 --network none --cpus 4 --memory 8g \
  -v "$PWD/runs:/workspace/openrsi-game/runs" openrsi-tower:v2.0.1 \
  python -B towerbench.py --policy candidate/policy.py --seeds 8100 8101 8102 8103 \
  --pressure 2 --output runs/development.json
```

These four development campaigns differ from the eight-case formal Judge and
32-case independent audit. Their scores are not interchangeable. See instruction.md
for the unchanged metric, observation/action restrictions, resource limits and
the eight-hour research budget. Public development evaluation needs no model API.

The public core module, original assets and reference are byte-identical to the
validated private Task v2.0.1. VERSION.json and publication-manifest.json identify
the code; hidden Judge cases and raw experiment logs are not copied here.
All current formal rewards are fractional, range0.2553763440860215–0.719758064516129;
103 scored submissions, zero equal1. Current32-case audit: reference0.3343413978494624,
final0.5618279569892473. These are reported measurements, not independent acceptance.

Source/provenance: source.json, NOTICE and LICENSE. The task uses contributor-owned
public Tiny Tower Defense assets plus independently authored benchmark mechanics.
No company internals, mixed report history, account data or credentials are included.
