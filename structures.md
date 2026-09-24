## Project folder
```
agentverify-paper/
  data/raw/         downloads, never edited
  data/processed/   tables built by scripts
  analysis/         scripts
  results/          output tables and figures
  docs/             analysis plan, decision log, codebook v2, pre-registration
  README.md         sources, versions, download dates
```


### Study 1 (RQ1): FaaP's released data
1. Snapshot the data. Copy these from their repository into `data/raw`, and record the commit hash and date:
+ `traj_data_v2_all89tasks.json`
+ `merged_tasks.json`
+ `CODEBOOK.md`
+ `the kappa_agreement/ folder`

2. Build one table of failed runs in `data/processed/faap_failed_runs.csv`. One row per run:
+ Columns from their data: `run id`, `task`, `scaffold`, `model`, `trigger`, `t_err`, `t_commit`, `t_surface`, `total steps`.
+ Columns you add: relative onset `(t_err / steps)`, fixable window `(t_commit - t_err)`, silent (`t_surface` is empty), and group (`spec_neglect` vs other).

3. Sanity checks. Save them to a log file:
+ 1,184 rows
+ 176 `spec_neglect`
+ 332 silent
+ 89 tasks
+ no negative fixable windows
  
4. Stop there until the plan is frozen. Building the table and counting rows is safe. Comparing the two groups is not.

5. After the freeze: run the tests. Re-runs them from the plan file only, as an independent check.

### Studies 2 and 3 (RQ2, RQ3): Nebius Draw 2
1. Before computing any agreement, add two lines to the pre-registration patch:
+ Report agreement three ways: exact, `±k`, and weighted.
+ Report runs that end with the agent's submit and runs that don't separately.

2. Keep the outcome in a separate key file. For each of the 20 runs, record `instance id`, `model`, `exit_status`, and resolved `yes or no`. Neither rater opens this file until both have finished.

3. After both raters finish:
+ Run `compute_agreement.py` for RQ2.
+ Join the labels with the key file for RQ3: does each run contain a divergence step, which form, and did it pass or fail? With 20 runs, this is descriptive only.