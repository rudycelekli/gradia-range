# ADR-007: The report does not wait on payment

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: disclosure, remediation, axiom
- **Recall**: 2026-10-24 decision consult returned not-adopted. History is UNKNOWN. No project memory db.

## Context

V1 finds issues in open-source projects and can sell the fix. Axiom does the fix work for now. The report has to reach the maintainer as a report. The thing Axiom sells is the repair: a patch against the twin, priced as work. Maintainers can hire that work because it is faster than staffing it, and because the witness is already in hand.

## Decision

When a verdict says an objective fell, Disclosure sends the maintainer a report they can reproduce. The report names the twin revision, the task, the witness id, and what held. Sending it is independent of an invoice.

Remediation is a separate offer. Axiom prices the fix as work. The maintainer may take the report and repair it themselves, merge our patch, or decline. The Open Board lists a public task for that objective only as a synthetic twin or a post-fix variant. The original witness stays internal until [ADR-008](ADR-008-traces-leave-after-the-fix-window.md) releases it.

## Consequences

### Positive

- Maintainers can trust the first contact.
- The paid product is labor and a standing range, which Axiom can invoice as services.
- Later enterprise conversations inherit the same rule.

### Negative

- Some findings will be fixed by the maintainer with no revenue. That cost is part of running the cohort.
- Phase 2 needs a disclosure contact and a publication check, so the board does not become the disclosure channel.

### Neutral

- Severity changes how fast the report goes out. The report remains a report at every severity.

## Links

- [ADR-001](ADR-001-range-is-a-gradia-product.md)
- [ADR-008](ADR-008-traces-leave-after-the-fix-window.md)
- [ADR-010](ADR-010-open-source-cohort-before-enterprises.md)
