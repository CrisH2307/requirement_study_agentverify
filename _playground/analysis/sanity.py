import csv
import os

# Run from the project root after build_table.py: python3 analysis/sanity.py
with open("data/processed/faap_failed_runs.csv") as f:
    rows = list(csv.DictReader(f))

silent = sum(r["silent"] == "True" for r in rows)

# (check, expected, got)
checks = [
    ("Failed runs", 1184, len(rows)),
    ("spec_neglect", 176, sum(r["group"] == "spec_neglect" for r in rows)),
    ("Silent (all failed runs)", 332, silent),
    ("Tasks", 89, len({r["task"] for r in rows})),
    ("Negative fix_window", 0, sum(int(r["fix_window"]) < 0 for r in rows)),
    ("Missing t_err, t_commit, or m", 0, sum(r["t_err"] == "" or r["t_commit"] == "" or r["m"] == "" for r in rows)),
]

lines = [f"{'Check':32} {'Expected':>8} {'Got':>8}  Result"]
for name, expected, got in checks:
    lines.append(f"{name:32} {expected:>8} {got:>8}  {'OK' if got == expected else 'DIFFERENT'}")
lines.append(f"Silent rate: {silent / len(rows):.1%} (expected 28.0%)")

os.makedirs("results", exist_ok=True)
with open("results/sanity_log.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines))
