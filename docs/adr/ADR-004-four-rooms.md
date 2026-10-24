# ADR-004: Four rooms on one task graph

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: rooms, access, board
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

The same task shape has to serve a free public board, seasonal awards, paid bounties, and client work whose name stays inside the company. A separate product for each room would fork the witness format and the corpus.

## Decision

A task has one room:

| Room | Audience | Compensation | Public board |
| --- | --- | --- | --- |
| Open | Anyone | Rank only | Listed |
| Award | Anyone | Rank and a posted award | Listed |
| Paid | Solvers who accept the task terms | Rank and a posted bounty | Listed, bounty visible |
| Private | Named solvers, written scope | Engagement fee or bounty | Unlisted |

Room is set before publication. Moving a task from Private to a public room requires a written grant and a fresh publication. Attempt history from the private room stays put unless the grant copies it.

Open-source tasks in v1 use Open, Award, or Paid, and they name the project. Enterprise tasks use Private until a grant says otherwise.

## Consequences

### Positive

- One schema for scoring, payout, and licensing.
- The board can show money while entry to the Open Set stays free.
- Client identity stays in the Private room plus the Identity context.

### Negative

- A mis-tagged Private task is a disclosure incident. Room is an explicit field, checked at publish time.
- Public rooms pass a publication check (report sent, live issue withheld from the board) before listing. See [ADR-007](ADR-007-report-does-not-wait-on-payment.md) and [ADR-008](ADR-008-traces-leave-after-the-fix-window.md).

### Neutral

- A campaign's room is the strictest room of its atoms. A campaign that contains a Private atom is Private.

## Links

- [ADR-002](ADR-002-task-is-the-unit.md)
- [ADR-005](ADR-005-open-set-stays-free.md)
- [ADR-009](ADR-009-identity-map-is-its-own-context.md)
