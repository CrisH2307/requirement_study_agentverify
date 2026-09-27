# RQ1 plan (AgentVerify paper)

Status: **DRAFT**. It becomes final when tagged `rq1-plan-frozen` in git (Step 5), which happens before
any number in Step 6 is computed. After the tag, any change is reported in the paper as a change.

## Research question

**RQ1. Do requirement-related failures differ from other failures in when they start, how long they stay
fixable, and how often they stay silent?**

Why it matters: a failure that stays silent never raises an error, a failing test or a contradicting output,
so a monitor that waits for such a signal never sees it. If requirement-related failures are silent more
often, then catching them needs the requirement text itself, not only the run's signals.

## Data

- FaaP's released labels for 1,184 failed runs: 89 Terminal-Bench tasks, 3 agent frameworks, 7 models
  (87 tasks have at least one failure). Source and commit: `data/raw/faap/SOURCE.md`.
- The original task text for every task, pinned to one commit: `data/raw/task_text/SOURCE.md`.

## Who is in which group

| Group | Definition |
|---|---|
| **Requirement-related** | Shortlisted runs labeled **ANCHORED** in Step 3 (see `docs/labeling_guide.md`) |
| **Other** | Every other failed run. Shortlisted runs labeled UNCLEAR are left out and counted. |

How runs reach Step 3: we label every run on FaaP's shortlist (311 runs where FaaP's trigger is
`spec_neglect` or its failure category names the requirement), plus 100 random runs from outside the shortlist.
Those 100 are **only a measurement**: the share of them labeled ANCHORED estimates how many requirement failures
the shortlist misses. They do not join the requirement group (only 100 of the 873 runs outside the shortlist are
labeled, so adding them would treat runs unequally); all runs outside the shortlist stay in "Other". If some of
them are really requirement failures, the gap between groups shrinks, so our result is on the cautious side.
We report the estimated share.

## The three measures (FaaP's labels, used as-is)

| Measure | Plain meaning | From FaaP's labels |
|---|---|---|
| **Start step** | Step where the decisive mistake happens | `t_err` |
| **Fix window** | Steps between the mistake and the point of no return | `t_commit - t_err` |
| **Silent** | The run ends without any error, failing test or contradicting output | `t_surface` is empty |

## How we compare the groups

**1. One table.** For each group: median start step, median fix window, % silent. The **gap** is
requirement-related minus other.

**2. How sure are we? Redraw the tasks.** Runs from the same task look alike, so we treat the task, not the
run, as the unit. We draw 87 tasks at random with replacement, keep all their failed runs, and recompute the gap.
We repeat this 10,000 times (seed `20260925`) and report the range that holds the middle 95% of the gaps.
If that range does not include 0, the gap is not a quirk of which tasks happened to be in the benchmark.

**3. Four checks.** Each answers one doubt a reader would have:

| Check | The doubt | How we test it | Passes if |
|---|---|---|---|
| Same task | "Requirement failures just happen in harder tasks" | Tasks with at least 2 runs in each group: compare the two groups inside each task | The gap points the same way in more than half of those tasks |
| Drop top tasks | "One or two tasks drive it" | Remove the 5 tasks with the most requirement-related runs, recompute | The gap keeps its direction |
| Every model | "One bad model drives it" | Recompute the gap separately for each of the 7 models | At least 5 of 7 models show the same direction |
| Stricter group | "It depends on our labels" | Use only FaaP's `spec_neglect` runs as the requirement group | The gap keeps its direction |

Ties: a gap of exactly 0 does not "point the same way". If the overall gap is 0, no check can pass, and the
measure is reported as "no clear difference". The "every model" and "same task" checks only use models or tasks
that have runs in both groups (same task: at least 2 in each).

**4. What we claim.** For each measure we say "requirement-related failures differ" only if the redraw range
excludes 0 **and** all four checks pass. Otherwise we say "no clear difference", which is also a result.
The same rule applies to all three measures.

## How reliable are the labels (Step 4)

- Kundi labels 50 random checklist rows on his own (`labels/kundi_blind_50.csv`), without seeing anyone else's labels.
- We report the % of rows where Kundi and Cris agree, and Cohen's kappa (agreement after removing
  what two people would match by chance).
- Target: kappa of at least 0.61 (the usual line for "substantial" agreement). If it is lower, we fix the guide
  using the disagreements, relabel, and report both rounds.

## What we already looked at (disclosed)

Before this plan was written, we looked at FaaP's labels grouped by their trigger. In particular, `spec_neglect`
runs ended silent in 44% of cases vs 28% of all failed runs. That is why we ask RQ1. The ANCHORED group
does not exist yet, so none of its numbers has been seen.

## Known limits

- The three measures are FaaP's labels (drafted by LLMs, reviewed by 2 humans). We cannot re-check them,
  because FaaP did not release the raw runs. FaaP reports agreement of 0.78 to 0.94. The per-run agreement
  file in their repository could not be used to confirm it (see `docs/decision_log.md`, 2026-09-25).
- Step 3 labels are based on FaaP's written descriptions of each failure, not on the raw runs.
- Cris's labels start from drafts written by Claude, so Cris is not fully independent of the drafts.
  Kundi's labels are, which is why his agreement with Cris is the reliability number we report.
- One benchmark (Terminal-Bench). Other datasets come after this study is finished.
