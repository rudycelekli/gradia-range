# ADR-003: A twin carries no production data

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: twin, sandbox, data
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

The useful environment is realistic: same code, same trust boundaries, same way components call each other. Production data, production secrets, and customer identity do not belong in an environment that outside solvers will enter. A lab trace has to be replayable without a customer's records inside it.

## Decision

A twin is a boot of a pinned revision that we operate. It is loaded with synthetic fixtures. Secrets are generated for that twin. Hosted customer data, production credentials, and live tenant exports stay out of every room.

For a later enterprise, names that identify the client are rewritten at the twin boundary. The rewrite table lives in the Identity context ([ADR-009](ADR-009-identity-map-is-its-own-context.md)).

The twin revision is part of the witness. A verdict names the revision it was checked against.

## Consequences

### Positive

- Open-source work can start from a public clone.
- Traces can be licensed without a later scrub of customer rows.
- A solver receives an environment whose contents we can afford to lose.

### Negative

- Findings transfer to production where the behavior lives in the code and the configuration we reproduced. A behavior that depends on data outside the fixtures waits until a fixture covers that shape.
- Building fixtures is ongoing work, especially for Twenty's data model.

### Neutral

- A maintainer may later grant a scrubbed snapshot. That grant is a new decision. The snapshot becomes a fixture set with its own revision.

## Links

- [ADR-008](ADR-008-traces-leave-after-the-fix-window.md)
- [ADR-009](ADR-009-identity-map-is-its-own-context.md)
- [ADR-010](ADR-010-open-source-cohort-before-enterprises.md)
