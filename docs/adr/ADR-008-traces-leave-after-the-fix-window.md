# ADR-008: Traces leave after the fix window

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: corpus, license, intelligence
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

The corpus is a product for frontier labs. A trace of a fallen objective is also a procedure against a revision people may still be running. The brand requirement is that a trace which leaves the lab is evidence, replayable, and tied to a window the maintainer already knows about.

## Decision

A trace is eligible for a lab license and for a public benchmark drop only when all of the following hold:

1. The maintainer has the report ([ADR-007](ADR-007-report-does-not-wait-on-payment.md)).
2. The fix window has closed: the maintainer shipped a fix, or the window stated in the report has ended, whichever was recorded on the disclosure.
3. The licensed artifact is tied to a twin revision and a win condition, and it replays without production data ([ADR-003](ADR-003-twin-carries-no-production-data.md)).
4. The License record names train rights, exclusivity, and the room.

Private-room traces are eligible only under the client grant. Open-room traces may name the project or be de-identified. The license states which.

Failed attempts ship in the same bundle as the successful ones, labeled, once the window is open. A lab drop freezes the task ids and twin revisions. Later traces are a new drop.

## Consequences

### Positive

- Labs receive wins, failures, and a replay rule in one bundle.
- A maintainer can be told the public corpus waits for the window.
- Exclusive and trainable are explicit price terms.

### Negative

- Corpus revenue lags the finding. Phase 5 sits after the first reports on purpose.
- A missing window date blocks release.

### Neutral

- House research on our own twins can use traces immediately inside Gradia. "Leave" means leave to a lab or to a public drop.

## Links

- [ADR-003](ADR-003-twin-carries-no-production-data.md)
- [ADR-007](ADR-007-report-does-not-wait-on-payment.md)
- [ADR-009](ADR-009-identity-map-is-its-own-context.md)
