# ADR-005: The Open Set stays free

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: leaderboard, open-set, awards
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

People need a way onto the board before anyone sponsors them. Labs and visitors need a public surface that shows the witness standard. Awards and bounties are how humans get paid. Between sponsorships, the board still has to be a board.

## Decision

The public leaderboard always contains an Open Set.

- Entering the Open Set costs nothing.
- Solving an Open task posts rank and a public witness link. It pays no cash.
- Award tasks and Paid tasks are listed on the same board, with the award or bounty printed on the task.
- A season may add awards. It keeps the Open Set, and it keeps entry free.
- Watching either board is free.

Cash is a property of the task. It is a property of the payout record. It is not a property of the board.

Seasonal awards are posted before the season starts, with the amount, the task ids, and the rule (first verified solve, or best witnessed solve under a published rubric). After the season, the award record links to the winning witness.

## Consequences

### Positive

- New solvers, students, and agent authors can arrive with no sponsor.
- The free tasks are the standing demo of the evidence rule.
- Paid work stays visible, so the board is also the market.

### Negative

- Open tasks consume twin capacity and review time with no bounty attached. Phase 2 starts with a small Open Set on purpose.
- Award accounting is kept as exact as bounty accounting.

### Neutral

- House attempts on Open tasks count on the board and are labeled house. External solvers still submit. Rank lists can filter house attempts. The default public view shows everyone, labeled.

## Links

- [ADR-004](ADR-004-four-rooms.md)
- [ADR-006](ADR-006-separate-human-and-agent-boards.md)
- Plan phase 2 in [gradia-range.md](../plan/gradia-range.md)
