"""Step 2b. Build the list of runs a person labels in Step 3, and Kundi's blind subset.

Run from the Code/ folder:  python3 scripts/step2_build_checklist.py
Outputs (in labels/):
  checklist.csv        every run to label: the task's requirement text + FaaP's written evidence
  kundi_blind_50.csv   50 random rows of the checklist, for the second rater
  key.csv              which rows were candidates and FaaP's labels. DO NOT OPEN until labeling is done.

What the labeler sees: the requirement text and FaaP's free-text description of the failure.
What the labeler does NOT see: FaaP's trigger/category labels, whether the row is a candidate,
the start step, the fix window, or whether the run was silent. So labels cannot be steered
by the result we will test.
"""
import csv
import json
import random

import yaml

SEED = 20260925          # fixed, so anyone rerunning gets the same rows
N_OTHERS = 100           # random non-candidates, to estimate how many requirement failures the shortlist misses
N_KUNDI = 50
# Runs used as worked examples in docs/labeling_guide.md. Kundi must not get these (he would see the answer).
GUIDE_EXAMPLES = {"count-dataset-tokens__terminus2__gemini", "build-cython-ext__miniswe__gemini",
                  "install-windows-3.11__terminus2__kimi", "create-bucket__miniswe__gpt5"}

runs = {r["case_id"]: r for r in json.load(open("data/raw/faap/traj_data_v2_all89tasks.json"))}
table = list(csv.DictReader(open("data/processed/failed_runs.csv")))
rng = random.Random(SEED)

candidates = [r for r in table if r["candidate"] == "True"]
others = rng.sample([r for r in table if r["candidate"] == "False"], N_OTHERS)
items = candidates + others
rng.shuffle(items)       # mix candidates and others so the order gives nothing away

def requirement_text(task):
    return yaml.safe_load(open(f"data/raw/task_text/{task}.yaml"))["instruction"].strip()

LABEL_COLS = ["label", "requirement_quote", "evidence_quote", "note"]   # filled in Step 3
checklist, key = [], []
for i, r in enumerate(items, 1):
    src = runs[r["run_id"]]
    item_id = f"L{i:03d}"
    checklist.append({
        "item_id": item_id, "run_id": r["run_id"], "task": r["task"],
        "requirement_text": requirement_text(r["task"]),
        "failure_summary": src["one_sentence_failure_summary"],
        "mistake_explanation": src["trigger_explanation"],
        "mistake_quote": src["t_err_evidence"],
        **{c: "" for c in LABEL_COLS},
    })
    key.append({"item_id": item_id, "run_id": r["run_id"],
                "source": "candidate" if r["candidate"] == "True" else "random_other",
                "faap_trigger": r["faap_trigger"], "faap_category": r["faap_category"]})

def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

write("labels/checklist.csv", checklist)
write("labels/key.csv", key)
kundi = sorted(rng.sample(checklist, N_KUNDI), key=lambda r: r["item_id"])
assert not {r["run_id"] for r in kundi} & GUIDE_EXAMPLES, "a guide example landed in Kundi's subset"
write("labels/kundi_blind_50.csv", kundi)
print(f"checklist: {len(checklist)} rows ({len(candidates)} candidates + {N_OTHERS} random others); "
      f"Kundi subset: {N_KUNDI} rows")
