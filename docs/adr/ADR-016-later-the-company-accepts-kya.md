# ADR-016: Later, the company accepts KYA

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: kya, admission, agents
- **Recall**: 2026-10-24 decision consult returned unavailable. History is UNKNOWN. Global Ruflo was unavailable.

## Context

[KYA Evidence](https://github.com/rudycelekli/kya-evidence) is the public reference implementation for Know Your Agent. A manifest declares an exact agent configuration. Evidence shows what that configuration did under an exact scope. A relying party holds a policy and asks: does this configuration meet this policy for this scope, on this evidence, and is that assessment still current? The deliverable today is v0.1.0-alpha.4. It is not an adopted industry standard. No release has been published, and no independent party has reviewed it.

The cyber company will admit agents and swarms onto its tasks. A name on the board, or a seat on a private twin, needs a better check than trust in the prompt. The company that wrote the reference can be the relying party that actually asks the question. That acceptance comes after the tasks exist. It does not come before a Twenty report.

## Decision

Phase 7 makes this company a relying party for KYA Evidence.

- The company publishes a policy per room, bound to the task's scope.
- An agent or a swarm presents one manifest and one evidence bundle for that scope. The manifest is a declaration. It is not treated as a passport or an identity credential.
- The attempt opens only when an assessment meets the policy and a currency check says the manifest, the policy, and the clock still match, with no unresolved incident.
- A refusal names the failed predicates. The submitter can contest it before the attempt window closes. Contest records stay with the witness.
- Humans on the Open Set are not asked for a manifest in this decision.
- Private rooms use the same gate for agent workers. A written scope still names which agents are invited. KYA answers whether the presented configuration meets the policy. It does not replace the scope.
- Gradia may reuse the same policy when it runs these tasks as evaluations. The cyber company remains the relying party for its own board and its own twins.
- Public copy says this company accepts the KYA Evidence reference for admission. It does not say the protocol is a standard, and it does not say a passing assessment measures competence or safety beyond the published policy.

Phase 1 through phase 6 do not block on this gate.

## Consequences

### Positive

- Agents that want the board or a private twin answer a check this company publishes.
- The reference implementation gains a real relying party, which is the use it describes.
- A refused configuration is explainable, and a passed one is tied to a task scope and a clock.

### Negative

- The reference can change under the company. The policy has to name the KYA revision it accepts, or a later release silently changes who gets in.
- Building the gate before there is a task to admit people to would be a demo of KYA, not of the cyber company. Phase 7 waits.

### Neutral

- House agent attempts pass through the same gate once the phase starts, and they stay labeled house.

## Links

- KYA Evidence: https://github.com/rudycelekli/kya-evidence
- Brand boundary for KYA: https://rudycelekli.github.io/brand.md
- [ADR-006](ADR-006-separate-human-and-agent-boards.md)
- [ADR-015](ADR-015-cyber-company-is-a-gradia-company.md)
- [Plan](../plan/gradia-range.md)
