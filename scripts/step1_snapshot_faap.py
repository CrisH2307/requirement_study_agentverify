"""Step 1a. Copy FaaP's released data into data/raw/faap/ and record where it came from.

Run from the Code/ folder:  python3 scripts/step1_snapshot_faap.py
We never edit files in data/raw/. Every later step reads from here.
"""
import hashlib
import shutil
import subprocess
from datetime import date
from pathlib import Path

SRC = Path("cli_trajectory_analysis")          # FaaP's replication package (git clone)
DST = Path("data/raw/faap")
FILES = {
    "data/traj_data_v2_all89tasks.json": "traj_data_v2_all89tasks.json",  # 1,794 labeled runs
    "data/merged_tasks.json": "merged_tasks.json",                        # 89 tasks
    "docs/CODEBOOK.md": "CODEBOOK.md",                                    # their label definitions
}

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.run(["git", "-C", str(SRC), *args], capture_output=True, text=True).stdout.strip()

DST.mkdir(parents=True, exist_ok=True)
lines = [
    "# Source of the FaaP data",
    "",
    "Paper: Failure as a Process: An Anatomy of CLI Coding Agent Trajectories (Zhao et al., arXiv 2607.09510).",
    f"Repository: {git('remote', 'get-url', 'origin')}",
    f"Commit: {git('rev-parse', 'HEAD')} ({git('log', '-1', '--format=%ci')})",
    f"Copied on: {date.today().isoformat()}",
    "",
    "| File | SHA-256 |",
    "|---|---|",
]
for src_rel, name in FILES.items():
    shutil.copy2(SRC / src_rel, DST / name)
    lines.append(f"| {name} | `{sha256(DST / name)}` |")

(DST / "SOURCE.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
