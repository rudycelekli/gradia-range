# Gradia Range

- **Status**: proposed
- **Date**: 2026-10-24
- **Owner**: Rudy Celekli
- **Brand source**: [brand.md](https://rudycelekli.github.io/brand.md), [brand.json](https://github.com/rudycelekli/rudycelekli.github.io/blob/main/brand.json)
- **Decisions**: [ADR index](../adr/README.md)
- **Model**: [bounded contexts](../architecture/bounded-contexts.md)

Gradia Range is a Verify surface. It stands up a twin of a real system, breaks that twin into tasks, and records every attempt as evidence. Maintainers and, later, enterprises receive findings they can reproduce and a fix they can buy. Frontier labs license the traces and the benchmarks. People climb a public board for free and get paid when a task carries a bounty or an award.

AxiomConsulting.ai is the arm that delivers the report and the fix. Gradia keeps the lab, the board, and the corpus.

Gradia’s subject is evaluation: whether work holds, whether a score is real, and whether the evidence is good enough to keep. Range is that subject pointed at systems. A task is a benchmark item. A twin is the frozen world. A verdict is a score that replays. A board is a public standing. A lab drop is an export, and it waits until the license and the fix window allow it. The same refusal rule as the rest of the lab applies here: a number we cannot replay is withheld.

The public GitHub home is [rudycelekli/gradia-range](https://github.com/rudycelekli/gradia-range), beside Guard, Wind Tunnel, and the other public Gradia repos. The private programme repo stays `rudycelekli/gradia`. See [ADR-011](../adr/ADR-011-public-github-home-is-gradia-range.md).

## What each side receives

| Side | Receives | Pays |
| --- | --- | --- |
| Maintainer, then enterprise | A reproducible report on a twin, plus a fix they can purchase from Axiom | The fix, and later the private twin. The report arrives either way |
| Frontier lab | Replayable attempts, verdicts, and benchmark drops under a written license | The corpus license. Exclusive terms cost more |
| Human solver | Rank and awards on the free Open Set. Cash when the task is marked Award or Paid | Nothing to enter the Open Set |
| Agent author | A separate board, scored on the same tasks, with the same evidence rule | Nothing to appear. A paid task still pays its posted bounty |

The public proof we already have is the accepted-work ledger at [rudycelekli.github.io/activity.md](https://rudycelekli.github.io/activity.md). Range uses that same standard. A rank, a finding, and a trace each link to a witness. A claim without a witness stays off the board and out of the corpus.

## Language

Use the Gradia sheet. Say verifiable, inspectable, replayable, evidence-bound, twin, task, attempt, witness, verdict, trace.

Leave "elite hackers", "world-class", and "guru" out of the pitch. The ledger and the board are the introduction.

## V1 is an open-source cohort

The first systems are public projects we can clone, run, and empty of any hosted customer data. [Twenty](https://github.com/twentyhq/twenty) is first: a self-hosted CRM with a real multi-service shape, and a place where a synthetic workspace is the entire dataset.

The house runs the first attempts. Axiom writes the report, offers the fix, and does the fix when the maintainer accepts. The Open Board publishes a task only after that report path is done, and only as a synthetic twin or a post-fix variant.

Target cohort size is 20. The other 19 are proposed, not onboarded:

1. twentyhq/twenty
2. calcom/cal.com
3. documenso/documenso
4. makeplane/plane
5. chatwoot/chatwoot
6. outline/outline
7. n8n-io/n8n
8. windmill-labs/windmill
9. directus/directus
10. novuhq/novu
11. infisical/infisical
12. gitea/gitea
13. keycloak/keycloak
14. formbricks/formbricks
15. dubinc/dub
16. triggerdotdev/trigger.dev
17. umami-software/umami
18. hoppscotch/hoppscotch
19. appwrite/appwrite
20. mattermost/mattermost

A project joins the cohort when we can boot a twin, load synthetic data, name a disclosure contact, and cut at least one atom task with a machine-checkable win condition. Star count is not a qualification.

## Four rooms, one graph

Every task lives in one room. The graph underneath is the same: atoms, chains, and a campaign.

| Room | Who sees it | Solver receives | On the public board |
| --- | --- | --- | --- |
| Open | Anyone | Rank. No cash | Yes |
| Award | Anyone | Rank plus a posted award | Yes |
| Paid | Anyone who accepts the task terms | Rank plus the posted bounty | Yes, with the bounty visible |
| Private | Named solvers under a written scope | Bounty or engagement fee | No |

The Open Set is a standing part of the board. It is free to enter and free to solve. Paid and award tasks sit beside it. They do not replace it. A season can ship with a thin Open Set. It cannot ship with an empty one.

Private rooms are how an enterprise twin stays unnamed. The solver sees the task environment. The map from that environment back to the client stays in the Identity context. Open-source rooms name the project, because the report is for that project.

## Task graph

- **Atom.** One component, one objective, one twin, one win condition. This is the unit we score.
- **Chain.** Solving an atom unlocks the next environment. The trace that matters here is the path, including the dead ends.
- **Campaign.** The whole architecture, still inside one twin. House-run in v1. Invite-only once external solvers exist. Private when the system belongs to a client.

A chain is a first-class task. Its score depends on the atoms, and its trace is stored as one attempt family. Labs license atoms, chains, and campaigns as separate drops. Chains are the scarce ones.

## Twin

A twin is the code and the trust boundaries, booted by us, with synthetic fixtures. Secrets in the twin are generated for the twin. Names that would identify a later client are rewritten, and the rewrite table stays in Identity.

Twenty v1 is a single synthetic workspace. No import of a hosted tenant. No customer records. No production credentials.

## Evidence

An attempt is append-only. The witness records the action stream, the observations, the tool boundary, the twin revision, and the verdict. A verdict is a check against the win condition, re-runnable from the witness. The board posts the verdict. It does not post a score we cannot replay.

Human attempts and agent attempts share the witness format and use separate boards. An agent swarm is one solver identity with its members listed in the witness. Mixing the two boards would make both ranks meaningless. XBOW's public account of an autonomous system reaching the top of a US bug-bounty leaderboard (company blog, 2025-06-24) is the reason the split exists: agents are already on these boards.

## Report and fix

Axiom sends the maintainer a report they can reproduce on the twin: what was attempted, what held, what fell, and the witness id. The fix is an offer of work. Buying it is optional. The report does not wait on the invoice.

We publish an Open, Award, or Paid task for that finding after the maintainer has the report, and in a form that does not hand the live, unfixed project to the board. The usual form is a synthetic twin or a variant written against the fixed revision, with the original embargoed until the fix window closes.

## Lab corpus

Intelligence receives attempts only through the License context. A trace leaves after the fix window in [ADR-008](../adr/ADR-008-traces-leave-after-the-fix-window.md). The license states three things in writing: whether the lab may train, whether the drop is exclusive, and which room the traces came from. Private-room traces move only under the client grant. Open-room traces can be de-identified or project-named, and the license says which.

The benchmark drop is a frozen set of tasks, twin revisions, win conditions, and a baseline solver. A later drop can add traces. It does not silently rewrite the frozen set.

## How this sits in the factory

| Gradia piece | Range role |
| --- | --- |
| Blocks | The task definition: objective, room, win condition, twin revision |
| Verify | Twin, attempt, witness, verdict |
| Workers | Human solvers and agent swarms |
| Intelligence | Licensed traces and benchmark drops |
| Factory | The fix, as a patch the maintainer can merge |
| AxiomConsulting.ai | The report, the fix engagement, and later the enterprise twin |

## Phases

| Phase | Done when |
| --- | --- |
| 0. This plan | ADRs accepted or revised |
| 1. Twenty | One twin boots on synthetic data. One atom, one chain, and one campaign exist. One witnessed attempt. One report sent. One fix offered |
| 2. Open Board | The Open Set has at least one public task from that work. Human and agent columns both render. Entry is free |
| 3. Cohort | Twenty is joined by projects that meet the join rule, toward 20. House still does the fixes |
| 4. External solvers | People outside the house submit to the Open Set. Award and Paid tasks exist, with the cash amount posted on the task |
| 5. First lab drop | One frozen benchmark and one license, traces limited to tasks whose fix window has closed |
| 6. First enterprise | One private twin. Identity map held inside. Nothing from that room on the public board without a written grant |

Phase 1 is the whole company in miniature. We do not open the board, sell a corpus, or approach an enterprise as a customer before a Twenty report exists.

## Claim boundaries

- "Built" waits on a public twin, a witness, and a bounded result.
- The cohort list is a proposal. Joining is a later fact, recorded per project.
- Repository stars and PR counts stay on the activity ledger. Range does not fold them into a personal score.
- A lab drop states its task count, twin revisions, and date. We do not describe the corpus as complete, representative of all software, or predictive.
- Private client work stays off the public brand surfaces unless disclosure is authorized.

## Landscape, as it bears on the plan

Public bug-bounty platforms already host human and, increasingly, agent solvers. Training ranges already publish standings. Security consultancies already sell the fix. Evaluation labs already buy task sets. Range is the place those four meet under one witness format, with a free Open Set that never empties, a fix that is work rather than silence, and a corpus that can leave the building only after the fix window.

## GitHub

Public Gradia work already lives in named repos under `rudycelekli`: Guard, Wind Tunnel, Lens, Blocks, and the others. Range joins that line. There is no Gradia organization on GitHub yet. This decision does not create one.

Upstream fix pull requests stay ordinary fixes in the target project. The body carries a Gradia block so the evaluation is visible where the code review happens:

```text
Gradia evaluation
Lab: https://www.gradiahq.com
Range: https://github.com/rudycelekli/gradia-range
Task: <id, or "house review, task not yet published">
Witness: <id, or "not yet sealed">
```

The private `rudycelekli/gradia` repository remains the programme. Range does not fork a second lab inside it.

## Read next

1. [ADR-001](../adr/ADR-001-range-is-a-gradia-product.md) through [ADR-011](../adr/ADR-011-public-github-home-is-gradia-range.md)
2. [Bounded contexts](../architecture/bounded-contexts.md)
