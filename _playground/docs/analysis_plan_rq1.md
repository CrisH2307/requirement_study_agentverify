# RQ1 Analysis Plan (pre-registered)

Written before any group comparison was run. Frozen with the git tag `rq1-plan-frozen` (Sept 30, 2026).
Nothing below may change after the tag. Any deviation is reported as a deviation.

## Data

- Source: `data/processed/faap_failed_runs.csv`, built by `analysis/build_table.py` from the snapshot in `data/raw/`.
- Units: the 1184 failed runs (records with `t_commit`) from 87 tasks. The other 2 of the 89 tasks (`fix-git`, `csv-to-parquet`) have no failed runs.
- Groups: `spec_neglect` (trigger = spec_neglect) vs `other` (every other trigger).
  **Group 1 = `spec_neglect`, group 2 = `other`** in every test below.

## Measures

| ID | Measure | Definition |
|----|---------|------------|
| M1 | t_err | step where the first error happens |
| M2 | fix_window | t_commit − t_err |
| M3 | silent | t_surface is empty (the error never surfaces) |
| supporting | rel_onset | t_err / m |

## General settings

- All tests two-sided, α = 0.05.
- Fixed random seed: `20260930`.

## M1 and M2 (and rel_onset)

- Test: Mann-Whitney U, `scipy.stats.mannwhitneyu(x_spec_neglect, x_other, alternative="two-sided")`.
- Effect size: Cliff's δ = 2U/(n₁n₂) − 1, where U is the U of group 1.
  δ > 0 means spec_neglect values tend to be larger.
- 95% CI for δ: bootstrap with 10,000 resamples. Resample within each group separately, and take the 2.5th and 97.5th percentiles of δ.
- rel_onset uses the same test, but it is **supporting only** and is **not** part of the Holm correction.

## M3 (silent)

- Test: Fisher's exact test, `scipy.stats.fisher_exact` on the 2×2 table (group × silent).
- Effect size: risk difference = P(silent | spec_neglect) − P(silent | other).
- 95% CI: Newcombe method, `statsmodels.stats.proportion.confint_proportions_2indep(..., method="newcomb", compare="diff")`.

## Multiple testing

- Holm correction over the three p-values (M1, M2, M3):
  `statsmodels.stats.multitest.multipletests([p1, p2, p3], method="holm")`.

## Within-task check for M3

- Eligible tasks: tasks with at least 1 spec_neglect run **and** at least 1 other run (52 tasks).
- One 2×2 table (group × silent) per eligible task, combined with `statsmodels.stats.contingency_tables.StratifiedTable`.
- Report:
  - CMH test p-value: `test_null_odds()`.
  - Mantel-Haenszel pooled odds ratio: `oddsratio_pooled`, with its 95% CI from `oddsratio_pooled_confint()`.
    OR > 1 means spec_neglect runs have higher odds of being silent.
  - Descriptive only: the number of tasks where the silent rate is higher for spec_neglect than for other.
- **The within-task direction holds if:** CMH p < 0.05 **and** the pooled OR > 1 **and** its 95% CI excludes 1.
- Why not "the direction holds in X% of tasks": 18 of the 52 eligible tasks have only 1 spec_neglect run,
  so their per-task direction is mostly noise and produces many ties. CMH weights each task by its size instead.

## Decision rule

The claim is supported **only if all three hold**:

1. M3 is significant after Holm (adjusted p < 0.05).
2. The risk-difference 95% CI excludes 0.
3. The within-task direction holds (as defined above).
