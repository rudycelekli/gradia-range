# Gradia Range

Adversarial evaluation for [Gradia](https://www.gradiahq.com). A system is cloned into a twin with synthetic data, cut into tasks, and scored by a verdict that can be replayed. Humans and agents attempt the same tasks on separate boards. A free Open Set stays on the public board. Frontier labs can license traces after the fix window. Maintainers receive a report either way, and can hire the fix.

**Maturity, 2026-10-24:** specification. Phase 1 has not started. There is no live board, no sealed witness, and no project has joined the cohort. Twenty is the proposed first twin.

## Where this sits

| Pillar | Proves | Repo |
| --- | --- | --- |
| Gradia Guard | The record was not tampered with | [gradia-guard](https://github.com/rudycelekli/gradia-guard) |
| Wind Tunnel | The scorekeeper holds | [gradia-wind-tunnel](https://github.com/rudycelekli/gradia-wind-tunnel) |
| **Range** (this) | **A system holds, and the attempt is evidence** | this repo |

Gradia evaluates whether work holds and whether a score is real. Range is that evaluation pointed at a running system. A task is a benchmark item. A twin is the frozen world. A number we cannot replay is withheld.

## Read

- [Plan](docs/plan/gradia-range.md)
- [Decisions](docs/adr/README.md)
- [Bounded contexts](docs/architecture/bounded-contexts.md)

## Claim boundary

"Built" waits on a public twin, a witness, and a bounded result. The cohort list in the plan is a proposal. Repository stars elsewhere are not credit for this repository.
