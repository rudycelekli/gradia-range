# ADR-002: The task is the unit of work

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: task, graph, scoring
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

A whole-system engagement is hard to score, hard to compare across solvers, and hard to hand to a lab as a benchmark item. A pile of unrelated bugs loses the path. Solvers, including agent swarms, need an objective with a win condition. Maintainers and enterprises still care about the architecture, not only the isolated component.

## Decision

The task is the unit. Every task has an objective, a twin revision, a room, and a machine-checkable win condition.

Tasks form one graph with three scales:

- An **atom** is one component and one objective.
- A **chain** unlocks the next atom from the previous verdict. The stored object is the attempt family, dead ends included.
- A **campaign** is the graph of a whole twin, scored as the set of its atoms and chains plus one campaign-level objective.

Leaderboards, bounties, awards, and lab drops all point at tasks. A campaign is a task that references other tasks. It is the same type, at the top of the graph.

## Consequences

### Positive

- Solvers can be compared on the same atom.
- Chains preserve the multi-step trace labs lack.
- A private campaign can hide the client and still be built from the same task type.
- Partial credit is a chain with some atoms stood and some fallen.

### Negative

- Cutting atoms well is the real work. A vague objective produces a vague witness.
- Campaign scores need a published rule so a long chain does not drown a hard atom.

### Neutral

- v1 can ship atoms first. Chains and the Twenty campaign are part of phase 1 so the graph exists once.

## Links

- [ADR-004](ADR-004-four-rooms.md)
- [ADR-006](ADR-006-separate-human-and-agent-boards.md)
- [Bounded contexts](../architecture/bounded-contexts.md)
