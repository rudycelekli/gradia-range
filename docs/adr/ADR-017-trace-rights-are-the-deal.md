# ADR-017: Trace rights are the deal

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: pricing, traces, grants
- **Recall**: 2026-10-24 decision consult returned unavailable. History is UNKNOWN. Global Ruflo was unavailable.

## Context

The company gets good by repetition: create Harbor tasks for an open-source repo, attempt them in a sandbox, send the severity report, and land the fix when the maintainer accepts. That loop is the proof. Enterprises and startups are the same loop sold later, on a private twin.

Buyers will differ on the traces. Some will trade a lower price for letting the company use them. Some will pay more so the work stays theirs. The traces in question are attempt records from the sandbox. Production data, live tenants, and live accounts are already excluded by [ADR-003](ADR-003-twin-carries-no-production-data.md).

## Decision

One loop. Three grants. The grant is a field on the contract, chosen before the twin is booted.

| Grant | When | Traces after the fix window |
| --- | --- | --- |
| Open | Public repo, no engagement | Usable for the board, Gradia evaluations, and a lab drop. The published task is a synthetic twin or a post-fix variant |
| Startup | Private twin, lower price | De-identified traces usable for the benchmark and Gradia evaluations |
| Exclusive | Private twin, higher price | Purely for the client. No lab training, no Gradia reuse, no public board |

The report still goes to the maintainer or the client whether or not they buy the fix, as in [ADR-007](ADR-007-report-does-not-wait-on-payment.md). The fix window in [ADR-008](ADR-008-traces-leave-after-the-fix-window.md) still applies to every grant that allows use. An exclusive grant never reaches that door.

Paid twins are offered after the loop has run across the open-source cohort, not after a single repo. Startup and exclusive are both real offers. The sandbox is the one already used in the open.

A startup grant names what "de-identified" removes: client name, hostnames, and the identity map. It does not include their production rows, because those were never in the twin.

## Consequences

### Positive

- The price has a reason. Cheap means the traces can be used. Exclusive means they cannot.
- Open-source volume is the rehearsal for the paid work, on the same machinery.
- Gradia and the labs only receive traces a grant already allows.

### Negative

- A startup that later wants exclusive terms needs a new grant. Traces already released under the old grant stay released.
- Two price levels have to be written down before the first paid twin, or "cheap" becomes a discount with no rule.

### Neutral

- Dollar amounts are not part of this decision. The order is: open volume, then startup below exclusive, exclusive highest.

## Links

- [ADR-003](ADR-003-twin-carries-no-production-data.md)
- [ADR-007](ADR-007-report-does-not-wait-on-payment.md)
- [ADR-008](ADR-008-traces-leave-after-the-fix-window.md)
- [ADR-010](ADR-010-open-source-cohort-before-enterprises.md)
- [ADR-015](ADR-015-cyber-company-is-a-gradia-company.md)
- [Plan](../plan/gradia-range.md)
