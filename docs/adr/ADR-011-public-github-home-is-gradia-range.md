# ADR-011: The public GitHub home is gradia-range

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: github, brand, evaluation
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

Gradia is an evaluation lab: benchmarks, score validity, and evidence good enough to keep. Range is that work pointed at systems, so it belongs under Gradia. On GitHub the picture is split. The programme repository `rudycelekli/gradia` is private. The public record is a set of named repositories: `gradia-guard`, `gradia-wind-tunnel`, `gradia-lens`, `gradia-blocks`, and the others. Upstream pull requests from the same person often read as personal fixes, with no line back to the lab. There is no Gradia organization. `gradiahq` returns not found.

A new company name on GitHub would hide the evaluation programme we already publish. Leaving Range only in a private repository would continue the gap this decision is here to close.

## Decision

The public GitHub home for this work is `rudycelekli/gradia-range`. It sits beside the other public Gradia repositories and links to https://www.gradiahq.com.

- The repository is public.
- Its README states the maturity in force: a specification, with phase 1 (a Twenty twin, one witnessed attempt, one report, one fix offer) still ahead. It does not describe a live board or an onboarded cohort.
- The private programme repository `rudycelekli/gradia` stays the programme. Range is not a second copy of that codebase.
- Upstream fix pull requests keep a normal fix title. The body includes the Gradia block defined in the plan: lab, Range repository, task id, witness id.
- A Gradia GitHub organization is a later decision. This ADR does not create one.

## Consequences

### Positive

- Search and the profile can show a Gradia evaluation repository for this programme.
- Fix pull requests point at the lab without pretending each one is a benchmark result.
- The public claim stays inside the brand sheet: evaluation, evidence, replay.

### Negative

- Until an organization exists, Gradia on GitHub is still a prefix on a personal account.
- A public specification can be mistaken for a running product. The README has to keep the maturity line current.

### Neutral

- Profile pins and the generated frontier block on `rudycelekli/rudycelekli` are separate surfaces. This ADR publishes the repository. It does not rewrite those generators.

## Links

- [ADR-001](ADR-001-range-is-a-gradia-product.md)
- [Plan](../plan/gradia-range.md)
- Public siblings: https://github.com/rudycelekli/gradia-guard , https://github.com/rudycelekli/gradia-wind-tunnel
- Programme repository: https://github.com/rudycelekli/gradia (private)
