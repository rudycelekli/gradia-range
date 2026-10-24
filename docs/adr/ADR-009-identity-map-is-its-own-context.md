# ADR-009: The identity map is its own context

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: identity, privacy, enterprise
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

Open-source tasks name the project. Enterprise tasks keep the client's name, internal hostnames, and the grouping of tasks off the solver's desk except inside a written scope. If that mapping lives on the task record, every board query, every lab export, and every solver API is a leak path. A separate context with a one-way door is small enough to audit.

## Decision

Identity is a bounded context. It stores the link between a task id and the real system: client, repository, original names, and the rewrite table used to build the twin.

- Catalog, Twin, Task, Attempt, Ledger, and License store task ids and twin ids.
- They do not store the client name on a Private task.
- A solver principal can read a task environment. It cannot call Identity.
- Disclosure and Axiom engagements read Identity through an explicit service, and that read is witnessed.
- A lab export runs through License. License may attach a project name for Open rooms. It omits Identity for Private rooms unless the grant copies specific fields.

Open-source cohort tasks may store the upstream project name on the task, because the report is addressed to that project. Identity still holds any rewrite made for the twin.

## Consequences

### Positive

- Private work uses the same task and ledger code as the Open Board.
- A board query has no client column to select.
- A chain reveals the next environment at unlock time. The client architecture diagram stays in Identity.

### Negative

- A client portfolio is a privileged tool, not a join in the public database.
- Operators need a break-glass path that is witnessed.

### Neutral

- For the Twenty cohort, Identity is thin: upstream URL, revision, fixture set, disclosure contact. The context exists in phase 1 so phase 6 inherits it.

## Links

- [ADR-003](ADR-003-twin-carries-no-production-data.md)
- [ADR-004](ADR-004-four-rooms.md)
- [ADR-008](ADR-008-traces-leave-after-the-fix-window.md)
