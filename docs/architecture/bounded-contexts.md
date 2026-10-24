# Range bounded contexts

- **Status**: proposed
- **Date**: 2026-10-24
- **Plan**: [Gradia Range](../plan/gradia-range.md)
- **Decisions**: [ADR index](../adr/README.md)

Range is a modular kernel. Each context owns its aggregates and publishes domain events. Contexts talk through those events and a small set of application services. The domain layer has no dependency on the board UI, the git host, or a lab's API.

```
┌─────────────────────────────────────────┐
│ Presentation                            │  board, Axiom report, maintainer notice
├─────────────────────────────────────────┤
│ Application                             │  use cases, one per command
├─────────────────────────────────────────┤
│ Domain                                  │  the contexts below
├─────────────────────────────────────────┤
│ Infrastructure                          │  twin runtime, git, object store, ledger DB
└─────────────────────────────────────────┘
```

Dependency direction is inward. Identity is not a column on Task. License is not a filter at the end of an export script. Both are contexts with their own doors.

## Context map

```
Catalog ──supplies──▶ Twin ──supplies──▶ Task ──supplies──▶ Attempt
                         │                  │                  │
                         │                  │                  ▼
                         │                  │               Verdict
                         │                  │                  │
                         ▼                  ▼                  ├──▶ Ledger
                      Identity ◀──read── Disclosure ◀──────────┘
                         │                  │
                         │                  ▼
                         │             Remediation
                         │
                         └── omitted from ── License ◀── Verdict
                                                  │
                                                  ▼
                                               Corpus drop
Solver ──────── participates in ──────── Attempt, Ledger, payout
```

| Upstream | Downstream | Relationship |
| --- | --- | --- |
| Catalog | Twin | Customer / supplier. A target revision is pinned, then booted |
| Twin | Task | Customer / supplier. A task names a twin revision and a win condition |
| Task | Attempt | Customer / supplier. An attempt is against one published task |
| Attempt | Verdict | Partnership. The verdict re-checks the win condition from the witness |
| Verdict | Ledger | Customer / supplier. Public rooms post. Private rooms do not |
| Verdict | Disclosure | Downstream. A fallen objective opens a report |
| Disclosure | Remediation | Customer / supplier. The fix is a separate offer of work |
| Verdict | License | Anti-corruption. Fields leave only as the license copies them |
| Identity | Disclosure, Axiom | Open host service, witnessed reads. Solvers are not principals |
| Solver | Attempt, Ledger | Shared kernel. Kind is human, agent, or swarm |

## Kernel

The kernel loads contexts, holds the event bus, and nothing else. Optional later: a lab-export plugin that depends on License, and a payout plugin that depends on Ledger. v1 can be the core contexts in one process.

```typescript
interface Domain {
  readonly name: string;
  initialize(container: Container): Promise<void>;
}

interface DomainEvent {
  readonly eventId: string;
  readonly aggregateId: string;
  readonly occurredOn: Date;
  readonly eventVersion: number;
}

interface RangeKernel {
  load(domain: Domain): Promise<void>;
  get<T extends Domain>(name: string): T;
}
```

Core contexts: catalog, twin, task, attempt, verdict, ledger, disclosure, remediation, license, identity, solver.

## 1. Catalog

What we are allowed to point at. Open-source projects now. Enterprise systems only after [ADR-010](../adr/ADR-010-open-source-cohort-before-enterprises.md).

```typescript
interface Catalog {
  Target: {
    id: string;
    roomDefault: "open" | "award" | "paid" | "private";
    upstreamUrl: string | null; // set for the open-source cohort
    disclosureContact: string;
    joinRuleMet: boolean;
  };
}
```

Join rule: we can boot a twin, load synthetic data, name a disclosure contact, and cut one atom with a machine-checkable win condition. `upstreamUrl` is public for the cohort. For a future private target it stays null here and lives in Identity.

Events: `TargetAccepted`, `TargetRetired`.

## 2. Twin

A boot we operate. Code plus trust boundaries. Synthetic fixtures. Generated secrets. Pinned revision on every witness.

```typescript
interface Twin {
  TwinEnv: {
    id: string;
    targetId: string;
    revision: string;
    fixtureSetId: string;
    status: "provisioning" | "ready" | "retired";
  };
}
```

The runtime (container, compose, or a later sandbox) is infrastructure. The domain cares that a revision and a fixture set identify the environment a verdict may cite.

Events: `TwinReady`, `TwinRetired`.

## 3. Task

The unit. See [ADR-002](../adr/ADR-002-task-is-the-unit.md) and [ADR-004](../adr/ADR-004-four-rooms.md).

```typescript
type Scale = "atom" | "chain" | "campaign";
type Room = "open" | "award" | "paid" | "private";

interface Task {
  TaskDef: {
    id: string;
    scale: Scale;
    room: Room;
    twinId: string;
    objective: string;
    winConditionId: string;
    parentIds: string[]; // chain links and campaign membership
    bounty: Money | null;
    award: Money | null;
    publishedAt: Date | null;
  };
}
```

Invariants:

- Open room: `bounty` and `award` are null.
- Award room: `award` is set before publication.
- Paid room: `bounty` is set before publication.
- Private room: `publishedAt` stays null on the public board.
- A campaign's room is the strictest room among its member tasks.
- A chain task unlocks its next id only after a standing verdict on the previous id.

Events: `TaskPublished`, `TaskUnlocked`, `TaskWithdrawn`.

## 4. Attempt

Append-only action stream for one solver on one task. Dead ends stay in the stream.

```typescript
interface Attempt {
  AttemptLog: {
    id: string;
    taskId: string;
    solverId: string;
    twinRevision: string;
    openedAt: Date;
    sealedAt: Date | null;
  };
}
```

Sealing freezes the stream. Verdict reads a sealed attempt. Edits after seal are a new attempt.

Events: `AttemptOpened`, `AttemptSealed`.

## 5. Verdict

Re-runs the win condition against the sealed attempt and the twin revision. The board and the corpus cite verdicts, not stories.

```typescript
interface Verdict {
  Result: {
    id: string;
    attemptId: string;
    taskId: string;
    outcome: "stood" | "fell" | "invalid";
    replayId: string;
  };
}
```

`fell` means the objective was met: the win condition fired. `stood` means the twin held. `invalid` means the witness cannot be replayed. Invalid attempts do not rank and do not enter a lab drop.

Events: `VerdictRecorded`.

## 6. Ledger

Two public boards and one private book.

```typescript
interface Ledger {
  Standing: {
    taskId: string;
    board: "human" | "agent";
    solverId: string;
    verdictId: string;
    houseLabeled: boolean;
  };
}
```

The human board and the agent board consume the same public tasks. A swarm posts on the agent board. Private verdicts write the private book only.

Payout is a record on Award and Paid tasks: amount, solver, worker kind, verdict id. Open tasks create standings and no payout.

Events: `StandingPosted`, `PayoutReleased`.

## 7. Disclosure

The report to the maintainer or, later, the client. Triggered by a `fell` verdict. Independent of payment ([ADR-007](../adr/ADR-007-report-does-not-wait-on-payment.md)).

```typescript
interface Disclosure {
  Report: {
    id: string;
    verdictId: string;
    sentAt: Date | null;
    fixWindowEnds: Date | null;
  };
}
```

Events: `ReportSent`, `FixWindowClosed`.

## 8. Remediation

Axiom's offer of work. Accepting it creates a fix engagement. Declining it leaves the report standing.

```typescript
interface Remediation {
  FixOffer: {
    id: string;
    reportId: string;
    status: "offered" | "accepted" | "declined" | "merged";
  };
}
```

The patch itself is a Factory artifact. The domain tracks the offer and the outcome, not the diff.

Events: `FixOffered`, `FixMerged`.

## 9. License

The only door from a verdict to a lab or a public benchmark drop ([ADR-008](../adr/ADR-008-traces-leave-after-the-fix-window.md)).

```typescript
interface License {
  Grant: {
    id: string;
    verdictIds: string[];
    traineeMayTrain: boolean;
    exclusive: boolean;
    nameProjects: boolean;
    room: Room;
  };
}
```

A grant is creatable when every included verdict has a sent report and a closed fix window, and when a Private room is covered by a client grant. The export copies the fields the grant allows. It does not query Identity.

Events: `GrantIssued`, `DropFrozen`.

## 10. Identity

The map. Solvers are not principals. Reads by Disclosure and by Axiom operators are witnessed.

```typescript
interface Identity {
  Binding: {
    taskId: string;
    targetId: string;
    clientName: string | null;
    rewriteTableId: string | null;
  };
}
```

Open-source cohort bindings store the upstream target and any fixture rewrite. `clientName` is null until a private engagement exists.

Events: `BindingWritten`, `IdentityRead`.

## 11. Solver

```typescript
type WorkerKind = "human" | "agent" | "swarm";

interface Solver {
  Worker: {
    id: string;
    kind: WorkerKind;
    memberIds: string[]; // swarm members
    house: boolean;
  };
}
```

Registration is free for the Open Set. Paid tasks add an acceptance of that task's terms before the attempt opens. Kind is declared at registration and copied into the witness. A contest before payout can flag a kind mismatch. v1 does not pretend to detect it automatically beyond the recorded tool boundary.

Events: `SolverRegistered`, `KindContested`.

## Application services in v1

Phase 1 needs six use cases. Everything else can wait.

| Use case | Contexts |
| --- | --- |
| Accept Twenty as a target | Catalog |
| Boot the Twenty twin on a synthetic workspace | Twin, Identity |
| Publish one atom, one chain, one campaign skeleton | Task |
| Seal a house attempt and record a verdict | Attempt, Verdict, Solver |
| Send the report and offer the fix | Disclosure, Remediation, Identity |
| Post the standing once the task's room is public | Ledger |

Phase 2 adds `PublishOpenTask` and the two board reads. Phase 5 adds `IssueGrant` and `FreezeDrop`. Phase 6 adds a private binding with a client name.

## Aggregates we refuse to merge

- Task does not embed the client.
- Ledger does not embed the trace body. It points at a verdict.
- License does not read Identity.
- Remediation does not gate Disclosure.
- The human board does not rank agent workers.

Those splits are the architecture. A convenience join that violates one of them is a defect, not a shortcut.

## Tests that lock the boundaries

Domain tests, with collaborators stubbed:

- An Open task rejects a bounty.
- A campaign that includes a Private atom is Private.
- A sealed attempt cannot be appended.
- An invalid verdict does not post a standing.
- A `fell` verdict can send a report with no fix offer accepted.
- A grant that includes a verdict with an open fix window is refused.
- A solver principal cannot load a binding.
- A swarm standing is written to the agent board only.

These are the phase-1 acceptance tests for the model. The Twenty boot is the acceptance test for the twin.
