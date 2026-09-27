"""Step 4. How often do Cris and Kundi agree on the same 50 runs?

Run from the Code/ folder:
  python3 scripts/step4_agreement.py [cris_file] [kundi_file]
Defaults: labels/labels_draft.csv (Cris's `label` column) and labels/labels_kundi.csv
(Kundi's copy of kundi_blind_50.csv with his `label` column filled in).
Output: results/agreement.txt

Reports, in plain terms:
  - % of rows where both chose the same label
  - Cohen's kappa: agreement after removing what two people would match by chance
    (target from docs/plan.md: at least 0.61)
  - the same two numbers for the simpler question "ANCHORED or not"
  - a table of who chose what, and every row where they disagree
"""
import csv
import sys
from collections import Counter
from pathlib import Path

LABELS = ["ANCHORED", "NOT", "UNCLEAR"]
TARGET = 0.61

cris_path = sys.argv[1] if len(sys.argv) > 1 else "labels/labels_draft.csv"
kundi_path = sys.argv[2] if len(sys.argv) > 2 else "labels/labels_kundi.csv"
cris = {r["item_id"]: r["label"].strip() for r in csv.DictReader(open(cris_path, encoding="utf-8-sig"))}
kundi = {r["item_id"]: r["label"].strip() for r in csv.DictReader(open(kundi_path, encoding="utf-8-sig"))}

items = sorted(kundi)
bad = [i for i in items if cris.get(i) not in LABELS or kundi[i] not in LABELS]
if bad:
    sys.exit(f"Not labeled (or typo) by one of the raters: {bad}. Fix these first.")

def agreement(a, b, labels):
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    chance = sum(ca[k] * cb[k] for k in labels) / n ** 2
    kappa = (observed - chance) / (1 - chance) if chance < 1 else 1.0
    return observed, kappa

a = [cris[i] for i in items]
b = [kundi[i] for i in items]
obs3, k3 = agreement(a, b, LABELS)
a2 = ["ANCHORED" if x == "ANCHORED" else "OTHER" for x in a]
b2 = ["ANCHORED" if x == "ANCHORED" else "OTHER" for x in b]
obs2, k2 = agreement(a2, b2, ["ANCHORED", "OTHER"])

lines = [
    f"Rows compared: {len(items)}",
    "",
    f"Three labels (ANCHORED / NOT / UNCLEAR): same label on {obs3:.1%} of rows, Cohen's kappa = {k3:.2f}",
    f"ANCHORED or not:                        same label on {obs2:.1%} of rows, Cohen's kappa = {k2:.2f}",
    f"Target (docs/plan.md): kappa >= {TARGET} -> {'MET' if k3 >= TARGET else 'NOT MET: fix the guide using the disagreements, relabel, report both rounds'}",
    "",
    "Who chose what (rows = Cris, columns = Kundi):",
    f"{'':10}" + "".join(f"{l:>10}" for l in LABELS),
]
pairs = Counter(zip(a, b))
for x in LABELS:
    lines.append(f"{x:10}" + "".join(f"{pairs[(x, y)]:>10}" for y in LABELS))
lines += ["", "Disagreements (item: Cris vs Kundi):"]
lines += [f"  {i}: {cris[i]} vs {kundi[i]}" for i in items if cris[i] != kundi[i]] or ["  none"]

Path("results").mkdir(exist_ok=True)
Path("results/agreement.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
