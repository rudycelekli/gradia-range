# ADR-018: The frontier cut is a paired universe

- **Status**: proposed
- **Date**: 2026-10-24
- **Deciders**: Rudy Celekli
- **Tags**: scoring, harbor, rubric, rl
- **Recall**: 2026-10-24 decision consult returned unavailable. History is UNKNOWN. Global Ruflo was unavailable.

## Context

The phase-1 Twenty tasks pass a report contract that accepts an empty findings list. That witnesses the loop. It does not give a training signal or a frontier benchmark. Terminal-Bench requires a binary Harbor reward and an outcome check. DeepSWE trains on a sparse 0 or 1 from held-out tests. Gradia's rubric gate already freezes required and optional criteria, caps the episode when a required gate fails, and refuses a criterion that copies its own answer key. Gradia Universes already record a world that changes during an attempt. The reward loop already refuses a proxy that passes while the oracle is wrong.

A security attempt and a detection attempt are two views of one run. Harbor runs one agent per task. The shared world has to live under the tasks.

## Decision

A frontier Range task is a hosted app with two Harbor tasks on it.

- Range boots the app, loads synthetic databases, and keeps that copy moving: rows change, jobs run, and a deploy can land mid-episode.
- The solver's workspace is the running system: its URL, a fixture account, and the product's own interface. The verifier reads that live state.
- The watcher protects the same host while the episode is open, from the audit, the database and fixture telemetry, and the deploy feed. A revoke, a freeze, a secret roll, or a deploy is itself an event in the app.
- Each required criterion is a Gradia criterion bound to a gate. Optional criteria stay on the vector and do not flip the episode reward.
- The solver's `reward` is 1 when the verifier's condition holds in the running system.
- The watcher's `reward` is 1 when, after that moment, a clearing action lands inside the task's `block_window_sec`. If the condition never holds, the watcher reward is not graded.
- `report` stays a separate score for the maintainer. It does not flip either role's reward.
- A lab drop is the frozen tasks plus both trajectories. The license is priced in the thousands of dollars, and the figure is printed when a drop exists.
- Humans play these same tasks after one witnessed pair exists. Their board stays separate from the agent board.
- A rubric enters an RL export only after the reward-loop check: a pass on the score still agrees with the oracle.
- When the solver's verifier condition holds, the branch seals without a procedure. That seal is compiled into the watcher's Harbor task. The board entry is the detection task, after the fix window, as a synthetic replay or a post-fix variant.
- The instruction and the rubric describe the outcome. They do not describe a method.
- A pass rate is unpublished until five named models have run on the frozen revision and rubric hash.

The phase-1 report-contract tasks remain the loop witness. They are not this cut.

## Consequences

### Positive

- Solver traces and watcher traces come from the same branch and the same clock.
- A reached objective becomes a detection task Gradia can score with the rubric it already lints.
- The RL reward matches the binary reward Harbor, Terminal-Bench, and DeepSWE can aggregate.

### Negative

- Harbor's mean across steps is a fraction. Range has to threshold the episode at the conjunction before writing `reward`.
- The watcher task for a later replay exists only after a seal. A campaign whose objective stays 0 still has the live pair, and it has no detection label for that replay.
- Two agents on one host require a runner outside a single Harbor task, plus a real boot of the app and its databases.

### Neutral

- [ADR-013](ADR-013-two-scores-objective-and-report.md) stands. `objective` and `report` remain separate scores inside the criterion map.

## Links

- [Plan](../plan/gradia-range.md)
- [ADR-013](ADR-013-two-scores-objective-and-report.md)
- Gradia rubric gate: `gradia/schemas/rubric.py` in `rudycelekli/gradia`
- [Gradia Universes](https://github.com/rudycelekli/gradia-universes-work-sample)
- [Gradia reward loop](https://github.com/rudycelekli/gradia-reward-loop)
- Terminal-Bench task rubric: `rubrics/task-implementation.toml` in `harbor-framework/terminal-bench`
