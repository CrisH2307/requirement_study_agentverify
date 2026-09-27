"""Step 3 check. Run any time while labeling; it only reads, never changes your file.

Run from the Code/ folder:  python3 scripts/step3_check_labels.py [labels/labels_draft.csv]
Reports: how many rows are done, typos in `label`, ANCHORED rows whose quotes are not exact words from the
source text (spaces and line breaks are ignored when comparing), and UNCLEAR rows without a note.
"""
import csv
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "labels/labels_draft.csv"
rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
VALID = {"ANCHORED", "NOT", "UNCLEAR"}
squash = lambda s: re.sub(r"\s+", " ", s).strip()

done = [r for r in rows if r["label"].strip() in VALID]
typos = [(r["item_id"], r["label"]) for r in rows if r["label"].strip() and r["label"].strip() not in VALID]
problems = []
for r in rows:
    if r["label"].strip() != "ANCHORED":
        continue
    req, ev = squash(r["requirement_quote"]), squash(r["evidence_quote"])
    faap = squash(" | ".join([r["failure_summary"], r["mistake_explanation"], r["mistake_quote"]]))
    if not req or req not in squash(r["requirement_text"]):
        problems.append((r["item_id"], "requirement_quote is not exact words from requirement_text"))
    if not ev or not any(ev in squash(r[k]) for k in ["failure_summary", "mistake_explanation", "mistake_quote"]):
        problems.append((r["item_id"], "evidence_quote is not exact words from FaaP's text"))
no_note = [r["item_id"] for r in rows if r["label"].strip() == "UNCLEAR" and not r["note"].strip()]

print(f"Labeled: {len(done)} of {len(rows)}   (check_first rows done: "
      f"{sum(r['check_first'] == 'YES' and r in done for r in rows)} of {sum(r['check_first'] == 'YES' for r in rows)})")
print(f"Typos in label: {typos or 'none'}")
print(f"Quote problems ({len(problems)}):" if problems else "Quote problems: none")
for item, msg in problems:
    print(f"  {item}: {msg}")
print(f"UNCLEAR without note: {no_note or 'none'}")
