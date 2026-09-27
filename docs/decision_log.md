# Decision log

Newest at the bottom. One entry per decision: date, what, why.

**2026-09-25. Started RQ1 again from a clean structure.** Earlier experiments moved to `_playground/`, untouched.

**2026-09-25. Group = runs whose failure we can tie to a sentence of the task text (ANCHORED), not FaaP's
`spec_neglect` label alone.** FaaP labels failures twice: the trigger at the mistake and the failure category.
176 runs have trigger `spec_neglect`; 251 have a category that names the requirement; only 116 have both (311 in either). So `spec_neglect`
alone misses many requirement failures (for example, a run that used Qwen2 when the task said Qwen2.5 is
labeled `false_premise`). `spec_neglect` alone stays as the "stricter group" check.

**2026-09-25. Requirement text comes from the original task files, not FaaP's summary.** Pinned to
`harbor-framework/terminal-bench-1` commit `2af0e44` (last change to `original-tasks/`, 2026-01-22; FaaP
released 2026-07-09). Our anchor does not depend on FaaP's pipeline.

**2026-09-25. FaaP's per-run agreement file is not used as evidence.** In
`docs/kappa_agreement/dual_annotations.csv`, annotator B's timestamps differ from annotator A's in a pattern
that does not look like two independent people: for `t_err` the difference is only -1, 0 or +1 in 1,176 of
1,184 runs; for `t_lock` and `t_obs` the differences spread evenly between -10 and +10 and never go beyond
(1,183/1,184 and 852/852). It also has no rows on whether a run is silent. We cite the agreement reported in
the FaaP paper (0.78 to 0.94) and state that we could not confirm it from the release.

**2026-09-25. Simple statistics.** One method (redrawing tasks) for all three measures, plus four checks with
pass rules fixed in `docs/plan.md`. Replaces the earlier six-test design, which was hard to explain.

**2026-09-25. Kundi is the second labeler** (or another experienced researcher if he is unavailable).

**2026-09-25. The 100 random non-shortlisted runs are a measurement only.** They estimate how many requirement
failures the shortlist misses; ANCHORED ones among them do not join the requirement group, because only 100 of
873 runs outside the shortlist are labeled. (An earlier draft of `plan.md` was inconsistent on this; fixed.)

**2026-09-25. Added a tie-breaker and an "only the task text counts" rule to the labeling guide** (before any
human labeling). Reason: the first draft pass labeled the same pattern differently across runs, e.g. ignoring the
README in count-dataset-tokens. Tie-breaker: "If the agent's own plan had worked perfectly, would the stated
requirement be met? No = ANCHORED, yes = NOT."

**2026-09-25. Observation for the paper: FaaP's spec_neglect includes requirements that are not in the task
text.** In rare-mineral-allocation (FaaP's largest spec_neglect task, 17 runs) the task never says where to write
the answer; only the hidden test expects /app/solution.txt. We label such runs NOT with note `implicit` and will
report how many of FaaP's spec_neglect runs are implicit.

**2026-09-27. Analysis scripts written before any real comparison.** `scripts/step4_agreement.py` and
`scripts/step6_compare.py` implement docs/plan.md and were tested only with `--selftest` (fake labels, scrambled
measures). They are frozen together with the plan. Clarified in plan.md: a gap of exactly 0 does not count as
"pointing the same way".
