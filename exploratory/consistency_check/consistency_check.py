"""Consistency check. Find tasks where the same failure got different labels. LIST ONLY: no label is changed.

Run from the Code/ folder:  python3 exploratory/consistency_check/consistency_check.py
Reads (never writes): labels/labels_draft.csv (final v4 labels), data/raw/faap/traj_data_v2_all89tasks.json
                      (same FaaP file the frozen scripts use, via data/processed/failed_runs.csv).

Step 1 (always): check the label counts, group the 411 runs by task, flag tasks.
   A task is flagged if its runs have more than one label, or if its ANCHORED runs quote
   different clauses (one quote is not a part of the other, after lowercasing and removing punctuation).
   Writes review_flagged.csv: every run of every flagged task, with FaaP's description. A human reads it.
Step 2 (only if verdicts.csv exists): verdicts.csv holds one verdict per flagged task, written by hand
   after reading review_flagged.csv. Writes consistency_list.csv and prints the counts.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path("exploratory/consistency_check")
EXPECTED = {"runs": 411, "tasks": 81, "ANCHORED": 165, "NOT": 239, "UNCLEAR": 7,
            "implicit_exact": 40, "implicit_any": 42}
VERDICTS = ("likely_inconsistent", "different_failures", "cannot_tell")

# ---------- load ----------
all_rows = list(csv.DictReader(open("labels/labels_draft.csv", encoding="utf-8-sig")))
rows = [r for r in all_rows if any((v or "").strip() for k, v in r.items() if k)]   # the file has fully empty rows
print(f"labels_draft.csv: {len(all_rows)} rows, {len(all_rows) - len(rows)} fully empty (skipped), {len(rows)} kept")
for r in rows:
    for k in ("label", "requirement_quote", "note"):
        r[k] = (r.get(k) or "").strip()
faap = {r["case_id"]: r for r in json.load(open("data/raw/faap/traj_data_v2_all89tasks.json"))}

# ---------- count check: stop if the file is not what we expect ----------
labels = Counter(r["label"] for r in rows)
found = {"runs": len(rows), "tasks": len({r["task"] for r in rows}),
         "ANCHORED": labels["ANCHORED"], "NOT": labels["NOT"], "UNCLEAR": labels["UNCLEAR"],
         "implicit_exact": sum(r["label"] == "NOT" and r["note"].lower() == "implicit" for r in rows),
         "implicit_any": sum(r["label"] == "NOT" and "implicit" in r["note"].lower() for r in rows)}
print("Count check (found / expected); 'implicit' counted on NOT rows, case-insensitive:")
for k in EXPECTED:
    print(f"  {k:15} {found[k]:4} / {EXPECTED[k]}")
print(f"  other labels: {dict((k, v) for k, v in labels.items() if k not in ('ANCHORED', 'NOT', 'UNCLEAR'))}")
print(f"  NOT rows with 'implicit' inside a longer note: "
      f"{[r['item_id'] for r in rows if r['label'] == 'NOT' and 'implicit' in r['note'].lower() and r['note'].lower() != 'implicit']}")
print(f"  NON-NOT rows whose note contains 'implicit' (needs a human look): "
      f"{[(r['item_id'], r['label'], r['note'][:40]) for r in rows if r['label'] != 'NOT' and 'implicit' in r['note'].lower()]}")
missing = [r["run_id"] for r in rows if r["run_id"] not in faap or faap[r["run_id"]].get("t_commit") is None]
if found != EXPECTED or len(labels) != 3 or missing or len({r["run_id"] for r in rows}) != len(rows):
    sys.exit(f"STOP: counts do not match, or runs missing/not failed in FaaP ({missing[:5]}), or duplicate run_ids.")
print("Counts match.\n")

# ---------- group and flag ----------
def norm(q):
    return " ".join(re.sub(r"[^a-z0-9/._ -]", " ", q.lower()).split())

def distinct_clauses(quotes):
    qs = sorted({norm(q) for q in quotes if norm(q)}, key=len)
    return [q for i, q in enumerate(qs) if not any(q in longer for longer in qs[i + 1:])]

by_task = defaultdict(list)
for r in rows:
    f = faap[r["run_id"]]
    r["faap_trigger"] = f["trigger_mechanism"]
    r["faap_category"] = f["primary_failure_category"]
    r["faap_failure_summary"] = f["one_sentence_failure_summary"]
    r["faap_root_cause"] = f["root_cause_label"]
    by_task[r["task"]].append(r)

flagged = {}
for task, rs in sorted(by_task.items()):
    why = []
    if len({r["label"] for r in rs}) > 1:
        why.append("mixed labels " + str(dict(Counter(r["label"] for r in rs))))
    clauses = distinct_clauses(r["requirement_quote"] for r in rs if r["label"] == "ANCHORED")
    if len(clauses) > 1:
        why.append(f"{len(clauses)} different ANCHORED quotes")
    if why:
        flagged[task] = "; ".join(why)

n_runs_flagged = sum(len(by_task[t]) for t in flagged)
print(f"Tasks checked: {len(by_task)} ({len(rows)} runs)")
print(f"Tasks flagged: {len(flagged)} ({n_runs_flagged} runs)")
print(f"  by mixed labels: {sum('mixed' in w for w in flagged.values())}")
print(f"  by different ANCHORED quotes: {sum('quotes' in w for w in flagged.values())}")
print(f"Tasks not flagged: {len(by_task) - len(flagged)} ({len(rows) - n_runs_flagged} runs)\n")

order = lambda t: (t != "reshard-c4-data", t)   # the known case first
LABEL_ORDER = {"NOT": 0, "UNCLEAR": 1, "ANCHORED": 2}
review_cols = ["task", "flag_reason", "item_id", "run_id", "label", "requirement_quote", "note",
               "faap_trigger", "faap_category", "faap_root_cause", "faap_failure_summary"]
with open(HERE / "review_flagged.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=review_cols, extrasaction="ignore")
    w.writeheader()
    for t in sorted(flagged, key=order):
        for r in sorted(by_task[t], key=lambda r: (LABEL_ORDER[r["label"]], r["item_id"])):
            w.writerow({**r, "flag_reason": flagged[t]})
print(f"Wrote {HERE / 'review_flagged.csv'}")

# ---------- step 2: merge hand-written verdicts ----------
vpath = HERE / "verdicts.csv"
if not vpath.exists():
    sys.exit("No verdicts.csv yet. Read review_flagged.csv, write verdicts.csv (task,verdict,reason), run again.")
verdicts = {v["task"]: v for v in csv.DictReader(open(vpath))}
bad = [t for t in flagged if t not in verdicts or verdicts[t]["verdict"] not in VERDICTS]
extra = [t for t in verdicts if t not in flagged]
if bad or extra:
    sys.exit(f"STOP: verdicts.csv does not match the flagged tasks. Missing/bad: {bad}. Not flagged: {extra}.")

out_cols = ["task", "item_id", "run_id", "label", "requirement_quote", "note", "faap_trigger",
            "faap_category", "faap_failure_summary", "verdict", "reason"]
with open(HERE / "consistency_list.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=out_cols, extrasaction="ignore")
    w.writeheader()
    for t in sorted(flagged, key=order):
        for r in sorted(by_task[t], key=lambda r: (LABEL_ORDER[r["label"]], r["item_id"])):
            w.writerow({**r, "verdict": verdicts[t]["verdict"], "reason": verdicts[t]["reason"]})
print(f"Wrote {HERE / 'consistency_list.csv'}\n")

print("Flagged tasks per verdict (tasks / runs):")
for v in VERDICTS:
    ts = [t for t in flagged if verdicts[t]["verdict"] == v]
    print(f"  {v:20} {len(ts):3} tasks / {sum(len(by_task[t]) for t in ts):3} runs")
