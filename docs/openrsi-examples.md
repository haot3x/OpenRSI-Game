# Source Repositories in OpenRSI Task Discussions

A read-only inspection on October 10, 2026 found 105 discussions in the Task Ideas category. Of these, 102 proposal bodies contained a GitHub repository link outside OpenRSI-Index. This is a link count, not a claim that every linked repository is public, reachable or sufficient for admission.

The three bodies without such links were discussions #137, #3 and #1. The current review of #137 rejects the missing source evidence; #3 is an early rejected test. The older test #1 received an Accept review under an earlier process, so the historical discussion set does not support the absolute claim that every accepted discussion includes a public repository link.

## Representative cases

| Discussion | Source and review evidence |
| --- | --- |
| [Graph of Skills #180](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/180) | Pins the public [Graph of Skills repository](https://github.com/davidliuk/graph-of-skills) and concrete artifact sources; the Source Repository gate passes and task preparation produces a private task repository. |
| [Capability profile estimation #194](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/194) | Pins the public [AutoJudger repository](https://github.com/IMNearth/AutoJudger) and response data; the review accepts a task-owned CPU adaptation of the upstream method. |
| [KV cache throughput #137](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/137) | Names a technology and baseline idea but provides no repository URL or exact revision; the Source Repository gate fails. |
| [Early test #1](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/1) | An older transformed-code coding task without a source URL received an Accept review. It is not evidence that the current source gate permits an unspecified codebase. |

The first two source repositories were independently confirmed public during this inspection. Links in other proposals were not all independently checked for present-day availability.

## Current rule and its implication

The [current proposal rubric](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/.agents/skills/proposal-agent/references/task-proposal-rubric.md) requires an auditable open-source codebase for the starting environment, baseline and research target. It permits a public benchmark-owned overlay, matched harness or clean-room task implementation when necessary for evaluation research and explicitly related to its upstream project. Required assets and services must be public and usable or have a concrete existing delivery/access interface.

This permits a focused public evaluation project rather than publication of a complete company application. A public repository containing only a research idea does not yet establish a runnable baseline or usable game assets.

The proposal's source repository and the generated task repository serve different purposes. The [contribution workflow](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md) generates a private task repository after review; that private repository does not replace the proposal's auditable source and asset evidence.
