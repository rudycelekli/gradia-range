# Gradia Range

- **Status**: proposed
- **Date**: 2026-10-24
- **Owner**: Rudy Celekli
- **Brand source**: [brand.md](https://rudycelekli.github.io/brand.md), [brand.json](https://github.com/rudycelekli/rudycelekli.github.io/blob/main/brand.json)
- **Decisions**: [ADR index](../adr/README.md)
- **Model**: [bounded contexts](../architecture/bounded-contexts.md)

Range is the cyber practice of a new company. That company is a Gradia company in the same sense AxiomConsulting.ai is: its own buyer, its own invoice, Gradia's language and evaluation machinery underneath. Its scope is cybersecurity only. The legal name is unset. Until it is chosen, this plan calls it the cyber company.

The cyber company stands up a twin, breaks it into Harbor tasks, and records every attempt as evidence. Maintainers and enterprises receive a severity-rated report and can hire the fix. Frontier labs license the traces. People climb a public board for free and get paid when a task carries a bounty or an award. Gradia can run the same tasks as evaluations. Axiom keeps the non-cyber implementation work.

Gradia’s subject is evaluation: whether work holds, whether a score is real, and whether the evidence is good enough to keep. Range is that subject pointed at systems. A task is a benchmark item. A twin is the frozen world. A verdict is a score that replays. A board is a public standing. A lab drop is an export, and it waits until the license and the fix window allow it. The same refusal rule as the rest of the lab applies here: a number we cannot replay is withheld.

The public GitHub home is [rudycelekli/gradia-range](https://github.com/rudycelekli/gradia-range), beside Guard, Wind Tunnel, and the other public Gradia repos. The private programme repo stays `rudycelekli/gradia`. See [ADR-011](../adr/ADR-011-public-github-home-is-gradia-range.md).

## What each side receives

| Side | Receives | Pays |
| --- | --- | --- |
| Maintainer, then enterprise | A reproducible security report on a twin, plus a fix they can purchase from the cyber company | The fix, and later the private twin. The report arrives either way |
| Frontier lab | Replayable attempts, verdicts, and benchmark drops under a written license | The corpus license. Exclusive terms cost more |
| Human solver | Rank and awards on the free Open Set. Cash when the task is marked Award or Paid | Nothing to enter the Open Set |
| Agent author | A separate board, scored on the same tasks, with the same evidence rule | Nothing to appear. A paid task still pays its posted bounty |

The public proof we already have is the accepted-work ledger at [rudycelekli.github.io/activity.md](https://rudycelekli.github.io/activity.md). Range uses that same standard. A rank, a finding, and a trace each link to a witness. A claim without a witness stays off the board and out of the corpus.

## Language

Use the Gradia sheet. Say verifiable, inspectable, replayable, evidence-bound, twin, task, attempt, witness, verdict, trace.

Leave "elite hackers", "world-class", and "guru" out of the pitch. The ledger and the board are the introduction. A person who reaches an objective is credited by name on the attempt, as Rudy Celekli's own ledger credits a merge.

## A Gradia company, cyber only

Gradia evaluates whether work holds, including workflows for other departments. This company does not sell that. It sells security: the twin, the Harbor tasks, the severity report, the fix, and the benchmark. When a department wants a workflow evaluation, the introduction goes to Gradia. The clone this company built can be the environment Gradia runs, under Gradia's contract, not this company's.

A buyer meets three names, each with one job. Rudy Celekli is the person on the contribution ledger and on [rudycelekli.github.io](https://rudycelekli.github.io/). Gradia is the lab, and this company is a Gradia company. The cyber company is who signs the security engagement. See [ADR-015](../adr/ADR-015-cyber-company-is-a-gradia-company.md).

## How the company wins

The company wins by owning the task. A solver wins by reaching `objective`. Those are different wins, and the company is paid for the first one.

Each Harbor task is built once and used three ways:

| Use | Who runs it | What the company gets |
| --- | --- | --- |
| Board | Humans and agents, including the house and later collaborators | A public game, a rank, and a demo a buyer can open |
| Gradia eval | Gradia's own evaluation runs | The lab can score agents on tasks this company already froze |
| Engagement | The cyber company, on a maintainer's project or a private twin | The report, the fix offer, and the invoice |

The verifier is ours, so the campaign question is ours: can an agent take this whole twin? Publishing that question, with a free Open Set and a witness on every point, is how the benchmark becomes the set other people train and brag against. Labs license the traces. Enterprises buy the same shape pointed at their twin. We do not have to be the solver on every campaign for that to be true. When a collaborator reaches the objective, the task, the customer, and the report stay ours. Their name goes on the witness.

The early wins are small and clickable. A Twenty task Gradia can load. A report a maintainer can read. A fix merged in the open, with the Gradia block on the pull request, on the same ledger buyers already use to check Rudy Celekli. A held objective is still a win on the invoice. It is a loss only if we describe it as proof the system is safe.

What we refuse, because it loses the company: selling workflow benchmarks from this entity, holding a report until someone pays, and putting the company on the solver board as if the company were a person. House attempts are labeled house. The company is the operator.

Later, the company is a relying party for [KYA Evidence](https://github.com/rudycelekli/kya-evidence). An agent or a swarm that wants a rank, or access to a private twin, presents a manifest and evidence. The company asks the KYA question for that task's scope: does this configuration meet this policy, on this evidence, and is the assessment still current? A pass opens the attempt. A refusal is explained and can be contested. Humans keep the free Open Set without a manifest until a separate decision says otherwise. KYA Evidence is a reference implementation, v0.1.0-alpha.4, not an adopted standard. Accepting it here means this company uses that check. It does not make the check an industry standard. See [ADR-016](../adr/ADR-016-later-the-company-accepts-kya.md).

## What an enterprise buys

They buy a twin of their system, a run of the security tasks, a severity-rated report, and the option to hire the fix. They do not buy a procedure for their production network. The campaign question they can read is: can an agent take this whole twin? The answer is a verifier score, `objective`, on that twin. The document they can hand to a team is the report.

Two scores, written into Harbor `reward.json`:

| Key | Measures | Who it is for |
| --- | --- | --- |
| `objective` | The verifier's condition in the twin was reached, or it was not | The board, the lab drop, the campaign question |
| `report` | The finding file has severity, a component, evidence paths that exist in the tree, and a patch that is absent or applies | The maintainer and the enterprise |

`objective` at 0 means this attempt did not reach the condition. It does not mean the system is safe. `report` is the paid artifact either way. A fix is offered when the report cites something a maintainer can change. The report names severity (`critical`, `high`, `medium`, `low`, `info`), the component, the evidence path, and the impact. It does not carry a weaponized procedure. Traces leave on the fix-window rule in [ADR-008](../adr/ADR-008-traces-leave-after-the-fix-window.md).

The line to a security buyer: we will twin the system, run these tasks, and give you the report and a fix you can hire. Workflow evaluations are Gradia's sale. This company makes the introduction and stops there.

## Task ladder

Every repo the converter accepts becomes Harbor security tasks at three scales. Gradia may load those tasks later as agent evaluations. This company does not write the workflow objective. See [ADR-013](../adr/ADR-013-two-scores-objective-and-report.md) and [ADR-015](../adr/ADR-015-cyber-company-is-a-gradia-company.md).

| Scale | Harbor shape | Security question this company asks |
| --- | --- | --- |
| Atom | One task, one module | Did this module's objective fall? |
| Chain | Multi-step, two or three modules that call each other | Did the joined objective fall? |
| Campaign | One final objective over the whole twin | Can an agent take the whole twin? |

Integrations the repo declares, such as Slack, are fixture services inside the twin: fixture users, fixture tokens, on the twin's network. A customer's live Slack, live tenant, and live credentials stay outside. The chain and the campaign include those fixtures so the attempt sees the tools the software expects.

The campaign is the hard task. Atoms and chains exist so a miss on the whole twin still produces module-level evidence, and so a solver can be compared on a smaller objective. The board for the benchmark ranks the campaign `objective`. Module standings stay visible and do not replace that rank.

The house attempts the campaign first, and the attempt is labeled house. When the objective does not fall, the task is offered to a collaborator: a named human solver, or an agent author, on a Paid task, inside the same sandbox, under a written scope. Their witness is the attempt. The report to the maintainer still goes out. See [ADR-014](../adr/ADR-014-unsolved-campaigns-are-offered-to-collaborators.md).

A public claim that a campaign is hard, or that an agent took a twin, waits on a witness, a revision, and a date. The live contribution ledger remains the personal proof. It is not a substitute for a Range witness.

## V1 is an open-source cohort

The first systems are public projects we can clone, run, and empty of any hosted customer data. [Twenty](https://github.com/twentyhq/twenty) is first: a self-hosted CRM with a real multi-service shape, and a place where a synthetic workspace is the entire dataset.

The house runs the first attempts. The cyber company writes the report, offers the fix, and does the fix when the maintainer accepts. The Open Board publishes a task only after that report path is done, and only as a synthetic twin or a post-fix variant. Gradia can point an evaluation run at that published task.

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

The cyber company sends the maintainer a report they can reproduce on the twin: revision, tasks, severity, evidence paths, whether each objective fell, and the witness id. The fix is an offer of work. Buying it is optional. The report does not wait on the invoice.

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
| Cyber company | The security buyer, the report, the fix, and the board |
| Gradia | Evaluation runs on the published Harbor tasks, and the lab license |
| AxiomConsulting.ai | Gradia's non-cyber implementation work |

## Phases

| Phase | Done when |
| --- | --- |
| 0. This plan | ADRs accepted or revised |
| 1. Twenty | One twin boots on synthetic data. One security atom, one chain, and one campaign exist as Harbor tasks. Each has `objective` and `report`. One witnessed house attempt. One report sent. One fix offered |
| 2. Open Board | The Open Set has at least one public task from that work. Human and agent columns both render. Entry is free |
| 3. Cohort | Twenty is joined by projects that meet the join rule, toward 20. House still does the fixes |
| 4. External solvers | People outside the house submit to the Open Set. A campaign whose objective did not fall in-house is offered as a Paid task to a named collaborator. Award and Paid amounts are printed on the task |
| 5. First lab drop | One frozen benchmark and one license, traces limited to tasks whose fix window has closed |
| 6. First enterprise | One private security twin, contracted by the cyber company. Identity map held inside. The buyer receives the report and a fix offer. Nothing from that room on the public board without a written grant |
| 7. KYA admission | A published relying-party policy. An agent or swarm attempt opens only after a current KYA assessment meets that policy for the task's scope. The Open Set still admits humans without a manifest |

Phase 1 is the whole company in miniature. We do not open the board, sell a corpus, or approach an enterprise as a customer before a Twenty report exists.

## Claim boundaries

- "Built" waits on a public twin, a witness, and a bounded result.
- The cohort list is a proposal. Joining is a later fact, recorded per project.
- Repository stars and PR counts stay on the activity ledger. Range does not fold them into a personal score.
- A lab drop states its task count, twin revisions, and date. We do not describe the corpus as complete, representative of all software, or predictive.
- Private client work stays off the public brand surfaces unless disclosure is authorized.
- A campaign `objective` of 0 is a result about that attempt. It is not a claim that the system has been secured.
- "Most advanced" and similar rankings wait on a frozen public drop with a date, a revision, and a witness. They are not copy.

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

1. [ADR-001](../adr/ADR-001-range-is-a-gradia-product.md) through [ADR-016](../adr/ADR-016-later-the-company-accepts-kya.md)
2. [Bounded contexts](../architecture/bounded-contexts.md)
