# AgentVerify paper: RQ1 analysis

**RQ1. Do requirement-related failures differ from other failures in when they start, how long they stay
fixable, and how often they stay silent?**

Data: the released labels of *Failure as a Process* (FaaP): 1,184 failed runs of coding agents on
Terminal-Bench, plus the original text of each task.

Read these files to follow the whole study:
1. `docs/plan.md`: what we compare and how, in plain words
2. `docs/labeling_guide.md`: how a run is judged "requirement-related"
3. `docs/decision_log.md`: every decision and why
4. `docs/drafting.md`: how the draft labels were made

## The steps

Run everything from this folder (`Code/`). Each step only reads what earlier steps wrote.

| Step | What happens | Command / who | Output | Status |
|---|---|---|---|---|
| 1 | Copy FaaP's data and download the task text, recording exact versions | `python3 scripts/step1_snapshot_faap.py` then `python3 scripts/step1_fetch_task_text.py` | `data/raw/` | Done |
| 2 | Table of failed runs; list of runs to label | `python3 scripts/step2_build_runs_table.py` then `python3 scripts/step2_build_checklist.py` | `data/processed/failed_runs.csv`, `labels/` | Done |
| 3 | Label each run ANCHORED / NOT / UNCLEAR | Claude drafted (2 passes, see `docs/drafting.md`); Cris fills `label` column | `labels/labels_draft.csv` | Drafts done; Cris next |
| 4 | Second labeler on 50 runs, measure agreement | Kundi labels blind, then `python3 scripts/step4_agreement.py` | `labels/labels_kundi.csv`, `results/agreement.txt` | Script ready; waiting for labels |
| 5 | Freeze the plan | `git tag rq1-plan-frozen`, send to Kundi | tagged `docs/plan.md` | To do |
| 6 | Compare the groups: one table, task redraws, four checks | `python3 scripts/step6_compare.py` (test: `--selftest`) | `results/rq1_results.md` | Script ready; runs only after Step 5 |
| 7 | Write each finding as one sentence plus one real example run | Cris | paper draft | To do |

## Folder map

```
data/raw/faap/         FaaP's files, never edited (SOURCE.md = commit + checksums)
data/raw/task_text/    89 task files from Terminal-Bench, never edited (SOURCE.md = commit)
data/processed/        tables built by scripts
labels/                checklist to label, labels, and key.csv (hidden until labeling is done)
scripts/               one script per step, numbered
docs/                  plan, labeling guide, decision log
results/               outputs of Steps 4 and 6
cli_trajectory_analysis/   FaaP's repository as cloned (reference only, not tracked)
_playground/           earlier experiments, kept as they were
```

Requirements: Python 3.10+, `pyyaml` (Step 1b needs internet access to GitHub).
