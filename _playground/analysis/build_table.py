import csv
import json

# Run from the project root: python3 analysis/01_build_table.py
with open("data/raw/traj_data_v2_all89tasks.json") as f:
    data = json.load(f)

rows = []
for d in data:
    if d.get("t_commit") is None:  # PASS run, skip
        continue
    task, scaffold, model = d["case_id"].split("__")
    rows.append({
        "run_id": d["case_id"],
        "task": task,
        "scaffold": scaffold,
        "model": model,
        "trigger": d["trigger_mechanism"],
        "t_err": d["t_err"],
        "t_commit": d["t_commit"],
        "t_surface": d["t_surface"],  # None -> empty cell in the CSV
        "m": d["m"],
        "rel_onset": d["t_err"] / d["m"],
        "fix_window": d["t_commit"] - d["t_err"],
        "silent": d["t_surface"] is None,
        "group": "spec_neglect" if d["trigger_mechanism"] == "spec_neglect" else "other",
    })

with open("data/processed/faap_failed_runs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(len(rows), "rows written")
