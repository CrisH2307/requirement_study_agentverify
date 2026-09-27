# RQ1 results (SELFTEST: fake labels, scrambled measures, MEANINGLESS)

Group A (requirement-related): 141 runs; Group B (other): 1029 runs; left out (UNCLEAR): 14; tasks: 87; redraws used: 10000 of 10000

| Measure | A | B | Gap (A - B) | Range over task redraws (middle 95%) | Verdict |
|---|---|---|---|---|---|
| Median start step | 7.0 | 7.0 | +0.0 steps | -3.0 to +1.0 | **no clear difference** |
| Median fix window | 2.0 | 1.0 | +1.0 steps | -1.0 to +2.0 | **no clear difference** |
| % silent | 27.0 | 28.3 | -1.3 points | -8.9 to +6.8 | **no clear difference** |

## Checks

**Median start step** (range excludes 0: no)
- Same task: fail (0 of 31 tasks)
- Drop top 5 tasks: fail (gap without top 5 = +0.0 steps)
- Every model: fail (0 of 7 models)
- Stricter group: fail (gap = +1.0 steps)

**Median fix window** (range excludes 0: no)
- Same task: pass (17 of 31 tasks)
- Drop top 5 tasks: pass (gap without top 5 = +0.5 steps)
- Every model: fail (3 of 7 models)
- Stricter group: pass (gap = +1.0 steps)

**% silent** (range excludes 0: no)
- Same task: fail (15 of 31 tasks)
- Drop top 5 tasks: pass (gap without top 5 = -0.1 points)
- Every model: fail (4 of 7 models)
- Stricter group: pass (gap = -2.2 points)

## Other counts

- Random non-shortlisted runs labeled ANCHORED: 51 of 100 (estimated share of requirement failures the shortlist misses)
- FaaP spec_neglect runs labeled NOT with note 'implicit' (requirement not in the task text): 0 of 176
- Top 5 tasks by requirement-related runs: rare-mineral-allocation, count-dataset-tokens, reshard-c4-data, install-windows-3.11, intrusion-detection
