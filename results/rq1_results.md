# RQ1 results

Group A (requirement-related): 148 runs; Group B (other): 1029 runs; left out (UNCLEAR): 7; tasks: 87; redraws used: 10000 of 10000

| Measure | A | B | Gap (A - B) | Range over task redraws (middle 95%) | Verdict |
|---|---|---|---|---|---|
| Median start step | 8.0 | 7.0 | +1.0 steps | -2.0 to +2.0 | **no clear difference** |
| Median fix window | 3.0 | 1.0 | +2.0 steps | -1.0 to +2.0 | **no clear difference** |
| % silent | 35.8 | 26.7 | +9.1 points | +0.0 to +18.4 | **DIFFERS** |

## Checks

**Median start step** (range excludes 0: no)
- Same task: pass (18 of 33 tasks)
- Drop top 5 tasks: fail (gap without top 5 = +0.0 steps)
- Every model: fail (2 of 7 models)
- Stricter group: fail (gap = -1.5 steps)

**Median fix window** (range excludes 0: no)
- Same task: fail (15 of 33 tasks)
- Drop top 5 tasks: fail (gap without top 5 = +0.0 steps)
- Every model: fail (4 of 7 models)
- Stricter group: fail (gap = +0.0 steps)

**% silent** (range excludes 0: yes)
- Same task: pass (20 of 33 tasks)
- Drop top 5 tasks: pass (gap without top 5 = +11.7 points)
- Every model: pass (5 of 7 models)
- Stricter group: pass (gap = +19.1 points)

## Other counts

- Random non-shortlisted runs labeled ANCHORED: 17 of 100 (estimated share of requirement failures the shortlist misses)
- FaaP spec_neglect runs labeled NOT with note 'implicit' (requirement not in the task text): 36 of 176
- Top 5 tasks by requirement-related runs: chess-best-move, mteb-retrieve, protein-assembly, triton-interpret, add-benchmark-lm-eval-harness
