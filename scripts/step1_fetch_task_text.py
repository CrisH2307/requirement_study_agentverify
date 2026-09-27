"""Step 1b. Download the original task text (the requirement) for all 89 Terminal-Bench tasks.

Run from the Code/ folder:  python3 scripts/step1_fetch_task_text.py
Each task.yaml has an `instruction:` field. That text is what the agent was asked to do,
so it is the requirement we anchor failures to. We pin one commit so the text never changes.
"""
import json
import urllib.request
from datetime import date
from pathlib import Path

REPO = "harbor-framework/terminal-bench-1"   # formerly laude-institute/terminal-bench (GitHub redirects)
# Last commit that touched original-tasks/ (2026-01-22). Nothing in that folder changed after it,
# so this is the task text FaaP's agents saw (FaaP released on 2026-07-09).
COMMIT = "2af0e447794d89f71f7b982d5a5fdb684679d421"
DST = Path("data/raw/task_text")

tasks = [t["task_id"] for t in json.load(open("data/raw/faap/merged_tasks.json"))]
DST.mkdir(parents=True, exist_ok=True)
for task in tasks:
    url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/original-tasks/{task}/task.yaml"
    with urllib.request.urlopen(url, timeout=30) as r:
        (DST / f"{task}.yaml").write_bytes(r.read())

(DST / "SOURCE.md").write_text(
    "# Source of the task text\n\n"
    f"Repository: https://github.com/{REPO}\n"
    f"Commit: {COMMIT} (last change to original-tasks/, 2026-01-22)\n"
    f"Downloaded on: {date.today().isoformat()}\n"
    f"Tasks: {len(tasks)} files, one per task, named <task>.yaml\n"
    "The requirement is the `instruction:` field of each file.\n"
)
print(f"Downloaded {len(tasks)} task files into {DST}")
