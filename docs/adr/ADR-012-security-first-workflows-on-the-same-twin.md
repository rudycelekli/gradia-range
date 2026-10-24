# ADR-012: Security first, workflows on the same twin

- **Status**: proposed, workflow family narrowed by [ADR-015](ADR-015-cyber-company-is-a-gradia-company.md)
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: security, workflows, gradia
- **Recall**: 2026-10-24 decision consult returned unavailable. History is UNKNOWN. Global Ruflo was unavailable.

## Context

Gradia evaluates whether work holds. Buyers in security can be shown a finding, a severity, and a fix, which matches the open-source record already on the Rudy Celekli ledger. Buyers in other departments want to know whether an agent can complete their workflow. Those are different questions. They are the same codebase, the same fixture accounts, and the same witness once a twin exists.

Building a second lab for workflows would split Gradia. Starting with workflows would ask a buyer to trust a twin before a security report has made that twin concrete.

## Decision

Range emits two task families onto one twin.

- The security family is first. Its campaign question is whether an agent can take the whole twin.
- The workflow family is second. Its campaign question is whether an agent can carry that department's job across the same twin.
- Atoms, chains, and campaigns exist in both families. A workflow task is added only after the security report for that twin exists.
- Fixture services stand in for declared integrations. Live customer accounts are not connected.
- Public trust stays on two surfaces that already exist: the Rudy Celekli contribution ledger and site, and Gradia as the lab. Axiom invoices the report and the fix.

## Consequences

### Positive

- Security is a door we can open with the work the ledger already shows.
- A later department sale reuses the twin instead of starting a second clone.
- Harbor tasks stay the unit for both families.

### Negative

- Workflow revenue waits on a security report. That delay is the trust sequence.
- Two families mean two objectives to specify per campaign. The converter emits security first and leaves the workflow objective unwritten until someone states the job.

### Neutral

- The private Gradia programme repository remains the product for customer workflow benchmarks. Range is the task and twin surface.

## Links

- [ADR-001](ADR-001-range-is-a-gradia-product.md)
- [ADR-010](ADR-010-open-source-cohort-before-enterprises.md)
- [ADR-013](ADR-013-two-scores-objective-and-report.md)
- [Plan](../plan/gradia-range.md)
