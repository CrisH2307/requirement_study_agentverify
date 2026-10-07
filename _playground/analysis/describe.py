import os

import pandas as pd

# Run from the project root after build_table.py: python3 analysis/describe.py
# Pooled over all failed runs on purpose: no split by group before the plan is frozen.
df = pd.read_csv("data/processed/faap_failed_runs.csv")

lines = [f"Pooled descriptives, all failed runs (n = {len(df)})", ""]
lines.append(f"{'Variable':12} {'Median':>8} {'Q1':>8} {'Q3':>8} {'IQR':>8}")
for col in ["m", "t_err", "fix_window"]:
    q1, med, q3 = df[col].quantile([0.25, 0.5, 0.75])
    lines.append(f"{col:12} {med:>8.1f} {q1:>8.1f} {q3:>8.1f} {q3 - q1:>8.1f}")

os.makedirs("results", exist_ok=True)
with open("results/descriptives_pooled.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines))
