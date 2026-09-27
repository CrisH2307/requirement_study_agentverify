"""Step 2a. One table of FaaP's 1,184 failed runs, with the three measures and the candidate flag.

Run from the Code/ folder:  python3 scripts/step2_build_runs_table.py
Output: data/processed/failed_runs.csv (one row per failed run)

The three measures (FaaP's labels, used as-is):
  start_step   = t_err                  step where the decisive mistake happens
  fix_window   = t_commit - t_err       steps between the mistake and the point of no return
  silent       = t_surface is empty     no error, failing test or contradicting output before the run ends

Candidate = FaaP already points at a requirement, in either of its two labels:
  the trigger is spec_neglect, OR the failure category is one of REQUIREMENT_CATEGORIES.
Candidates are only a shortlist. Step 3 (anchoring) decides which runs are requirement-related.
"""
import csv
import json

REQUIREMENT_CATEGORIES = {   # every FaaP category name that refers to the task's requirements
    "spec_violation", "task_understanding", "spec_neglect", "spec_compliance",
    "requirement_abandonment", "requirement_misinterpretation", "constraint_violation",
    "wrong_problem_formulation",
}

runs = json.load(open("data/raw/faap/traj_data_v2_all89tasks.json"))
rows = []
for r in runs:
    if r.get("t_commit") is None:          # no lock-in step = the run passed; skip
        continue
    task, scaffold, model = r["case_id"].split("__")
    rows.append({
        "run_id": r["case_id"], "task": task, "scaffold": scaffold, "model": model,
        "faap_trigger": r["trigger_mechanism"],
        "faap_category": r["primary_failure_category"],
        "candidate": r["trigger_mechanism"] == "spec_neglect"
                     or r["primary_failure_category"] in REQUIREMENT_CATEGORIES,
        "steps_total": r["m"],
        "start_step": r["t_err"],
        "lock_step": r["t_commit"],
        "fix_window": r["t_commit"] - r["t_err"],
        "silent": r["t_surface"] is None,
    })

with open("data/processed/failed_runs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print(f"{len(rows)} failed runs, {len({r['task'] for r in rows})} tasks, "
      f"{sum(r['candidate'] for r in rows)} candidates")
