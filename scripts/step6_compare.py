"""Step 6. Compare requirement-related failures (A) with other failures (B). Implements docs/plan.md.

Run from the Code/ folder, ONLY after the plan is frozen (git tag rq1-plan-frozen):
  python3 scripts/step6_compare.py [labels_file]          default: labels/labels_draft.csv
  python3 scripts/step6_compare.py --selftest             fake labels + scrambled measures, to test the code
Output: results/rq1_results.md   (selftest: results/selftest_rq1_results.md)

Who is in which group (docs/plan.md):
  A = shortlisted runs labeled ANCHORED
  B = every other failed run (shortlisted NOT, the 100 random runs, all unlabeled runs)
  Shortlisted runs labeled UNCLEAR are left out and counted.

For each of the three measures (start step, fix window, % silent):
  1. Gap = A minus B (medians for the two step measures, percentage points for silent).
  2. Redraw the tasks 10,000 times (with replacement, seed 20260925); range = middle 95% of the gaps.
  3. Four checks: same task, drop top 5 tasks, every model, stricter group (FaaP spec_neglect as A).
  4. Rule: "differs" only if the range excludes 0 AND all four checks pass.
"""
import csv
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

SEED = 20260925
N_REDRAWS = 10_000
MEASURES = [("start_step", "Median start step", "steps"),
            ("fix_window", "Median fix window", "steps"),
            ("silent", "% silent", "points")]

selftest = "--selftest" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
labels_path = args[0] if args else "labels/labels_draft.csv"
rng = random.Random(SEED)

# ---------- load ----------
runs = list(csv.DictReader(open("data/processed/failed_runs.csv")))
for r in runs:
    r["start_step"] = int(r["start_step"])
    r["fix_window"] = int(r["fix_window"])
    r["silent"] = r["silent"] == "True"
key = {r["run_id"]: r for r in csv.DictReader(open("labels/key.csv"))}

if selftest:
    # Fake labels and scrambled measures: the output means nothing, it only proves the code runs.
    fake = random.Random(1)
    labels = {k["item_id"]: fake.choices(["ANCHORED", "NOT", "UNCLEAR"], [0.45, 0.5, 0.05])[0] for k in key.values()}
    notes = {i: "" for i in labels}
    triples = [(r["start_step"], r["fix_window"], r["silent"]) for r in runs]
    fake.shuffle(triples)
    for r, (s, f, q) in zip(runs, triples):
        r["start_step"], r["fix_window"], r["silent"] = s, f, q
else:
    rows = list(csv.DictReader(open(labels_path, encoding="utf-8-sig")))
    labels = {r["item_id"]: r["label"].strip() for r in rows}
    notes = {r["item_id"]: r["note"].strip().lower() for r in rows}
    missing = [k["item_id"] for k in key.values() if labels.get(k["item_id"]) not in ("ANCHORED", "NOT", "UNCLEAR")]
    if missing:
        sys.exit(f"{len(missing)} checklist rows are not labeled yet (first: {missing[:10]}). Finish Step 3 first.")

# ---------- groups ----------
for r in runs:
    k = key.get(r["run_id"])
    r["label"] = labels[k["item_id"]] if k else ""
    if k and k["source"] == "candidate":
        r["group"] = {"ANCHORED": "A", "NOT": "B", "UNCLEAR": None}[r["label"]]
    else:
        r["group"] = "B"
    r["strict_group"] = "A" if r["faap_trigger"] == "spec_neglect" else "B"
kept = [r for r in runs if r["group"]]

def value(rs, m):
    if m == "silent":
        return 100 * sum(r["silent"] for r in rs) / len(rs)
    return median(r[m] for r in rs)

def gap(rs, m, g="group"):
    a = [r for r in rs if r[g] == "A"]
    b = [r for r in rs if r[g] == "B"]
    if not a or not b:
        return None
    return value(a, m) - value(b, m)

sign = lambda x: (x > 0) - (x < 0)

# ---------- task redraws ----------
by_task = defaultdict(list)
for r in kept:
    by_task[r["task"]].append(r)
tasks = sorted(by_task)
redraw_gaps = {m: [] for m, _, _ in MEASURES}
skipped = 0
for _ in range(N_REDRAWS):
    sample = [r for t in rng.choices(tasks, k=len(tasks)) for r in by_task[t]]
    gs = {m: gap(sample, m) for m, _, _ in MEASURES}
    if any(g is None for g in gs.values()):
        skipped += 1
        continue
    for m in gs:
        redraw_gaps[m].append(gs[m])

def middle95(xs):
    xs = sorted(xs)
    return xs[int(0.025 * (len(xs) - 1))], xs[int(0.975 * (len(xs) - 1))]

# ---------- checks ----------
count_a = Counter(r["task"] for r in kept if r["group"] == "A")
top5 = [t for t, _ in sorted(count_a.items(), key=lambda kv: (-kv[1], kv[0]))[:5]]
models = sorted({r["model"] for r in kept})

report = {}
for m, name, unit in MEASURES:
    observed = gap(kept, m)
    d = sign(observed)
    lo, hi = middle95(redraw_gaps[m])
    # same task
    eligible = [t for t in tasks if sum(r["group"] == "A" for r in by_task[t]) >= 2
                and sum(r["group"] == "B" for r in by_task[t]) >= 2]
    same = sum(d != 0 and sign(gap(by_task[t], m)) == d for t in eligible)
    c_same = (d != 0 and eligible and same > len(eligible) / 2, f"{same} of {len(eligible)} tasks")
    # drop top 5
    g_drop = gap([r for r in kept if r["task"] not in top5], m)
    c_drop = (d != 0 and g_drop is not None and sign(g_drop) == d, f"gap without top 5 = {g_drop:+.1f} {unit}")
    # every model
    per_model = {mo: gap([r for r in kept if r["model"] == mo], m) for mo in models}
    agree = sum(d != 0 and g is not None and sign(g) == d for g in per_model.values())
    c_model = (agree >= 5, f"{agree} of {len(models)} models")
    # stricter group: FaaP spec_neglect vs all other failed runs
    g_strict = gap(runs, m, "strict_group")
    c_strict = (d != 0 and sign(g_strict) == d, f"gap = {g_strict:+.1f} {unit}")
    checks = {"Same task": c_same, "Drop top 5 tasks": c_drop, "Every model": c_model, "Stricter group": c_strict}
    excludes0 = lo > 0 or hi < 0
    verdict = "DIFFERS" if excludes0 and all(bool(c[0]) for c in checks.values()) else "no clear difference"
    report[m] = dict(name=name, unit=unit, A=value([r for r in kept if r["group"] == "A"], m),
                     B=value([r for r in kept if r["group"] == "B"], m), gap=observed, lo=lo, hi=hi,
                     excludes0=excludes0, checks=checks, verdict=verdict, per_model=per_model)

# ---------- counts for the paper ----------
cand = [k for k in key.values() if k["source"] == "candidate"]
rand = [k for k in key.values() if k["source"] == "random_other"]
n_unclear = sum(labels[k["item_id"]] == "UNCLEAR" for k in cand)
rand_anch = sum(labels[k["item_id"]] == "ANCHORED" for k in rand)
sn_implicit = sum(k["faap_trigger"] == "spec_neglect" and labels[k["item_id"]] == "NOT"
                  and "implicit" in notes[k["item_id"]] for k in cand)
sn_total = sum(k["faap_trigger"] == "spec_neglect" for k in cand)

# ---------- write ----------
out = ["# RQ1 results" + (" (SELFTEST: fake labels, scrambled measures, MEANINGLESS)" if selftest else ""), "",
       f"Group A (requirement-related): {sum(r['group'] == 'A' for r in kept)} runs; "
       f"Group B (other): {sum(r['group'] == 'B' for r in kept)} runs; "
       f"left out (UNCLEAR): {n_unclear}; tasks: {len(tasks)}; redraws used: {N_REDRAWS - skipped} of {N_REDRAWS}", "",
       "| Measure | A | B | Gap (A - B) | Range over task redraws (middle 95%) | Verdict |",
       "|---|---|---|---|---|---|"]
for m in report.values():
    out.append(f"| {m['name']} | {m['A']:.1f} | {m['B']:.1f} | {m['gap']:+.1f} {m['unit']} | "
               f"{m['lo']:+.1f} to {m['hi']:+.1f} | **{m['verdict']}** |")
out += ["", "## Checks", ""]
for m in report.values():
    out.append(f"**{m['name']}** (range excludes 0: {'yes' if m['excludes0'] else 'no'})")
    for cname, (ok, detail) in m["checks"].items():
        out.append(f"- {cname}: {'pass' if ok else 'fail'} ({detail})")
    out.append("")
out += ["## Other counts", "",
        f"- Random non-shortlisted runs labeled ANCHORED: {rand_anch} of {len(rand)} "
        f"(estimated share of requirement failures the shortlist misses)",
        f"- FaaP spec_neglect runs labeled NOT with note 'implicit' (requirement not in the task text): "
        f"{sn_implicit} of {sn_total}",
        f"- Top 5 tasks by requirement-related runs: {', '.join(top5)}", ""]

Path("results").mkdir(exist_ok=True)
path = Path("results/selftest_rq1_results.md" if selftest else "results/rq1_results.md")
path.write_text("\n".join(out))
print(f"Wrote {path}")
