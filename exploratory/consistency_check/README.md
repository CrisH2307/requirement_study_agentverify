# Consistency check (list only)

Goal: find tasks where runs with the **same failure** got **different labels**.
No label was changed. No final label is suggested. Cris decides.

## How to run

```
python3 exploratory/consistency_check/consistency_check.py
```

Run from the `Code/` folder. Full output is saved in `run_output.txt`.
Every number below comes from that output.

## Files

| File | What it is |
|---|---|
| `consistency_check.py` | The script. Checks counts, groups runs by task, flags tasks, merges verdicts. |
| `verdicts.csv` | One verdict per flagged task (written by Claude after reading FaaP's text). Judgment, not computed. |
| `consistency_list.csv` | **Main output.** Every run of every flagged task, with FaaP's description and the verdict. |
| `review_flagged.csv` | Same runs plus FaaP's `root_cause_label`. Used to make the verdicts. |
| `run_output.txt` | Script output with all counts. |

## Inputs

- `labels/labels_draft.csv` (final v4 labels). Columns used: `item_id, run_id, task, label, requirement_quote, note`.
- `data/raw/faap/traj_data_v2_all89tasks.json` (the FaaP file the frozen scripts use).
  Fields used: `trigger_mechanism` → `faap_trigger`, `primary_failure_category` → `faap_category`,
  `one_sentence_failure_summary` → `faap_failure_summary`, `root_cause_label` (review file only).

## Count check (passed)

- 411 labeled runs, 81 tasks. ANCHORED 165, NOT 239, UNCLEAR 7.
- NOT rows with note "implicit": 40 exact, 42 containing the word (L340, L354).
- The file also has 587 fully empty rows. The script skips them.

## Method

1. Group the 411 runs by task. All 81 tasks are checked.
2. Flag a task if:
   - its runs have more than one label, or
   - its ANCHORED runs quote different clauses. (Two quotes count as the same clause if one is part of the other,
     after lowercasing and removing punctuation.)
3. For each flagged task, read FaaP's failure summary for every run. Decide:
   - `likely_inconsistent`: runs with different labels (or different quotes) describe the same missed or broken thing.
   - `different_failures`: the labels differ because the failures differ.
   - `cannot_tell`: the failures overlap in part, or FaaP's text is too vague.
4. The verdict is for the whole task. The `reason` names the run IDs that match.

## Results

| | Tasks | Runs |
|---|---|---|
| Checked | 81 | 411 |
| Not flagged | 23 | 57 |
| Flagged | 58 | 354 |
| → flagged by mixed labels | 56 | |
| → flagged by different ANCHORED quotes | 19 | |

(A task can be flagged for both reasons.)

| Verdict | Tasks | Runs |
|---|---|---|
| likely_inconsistent | 23 | 188 |
| different_failures | 27 | 119 |
| cannot_tell | 8 | 47 |

Run counts are all runs in those tasks, not only the runs that disagree.

## The known case first: reshard-c4-data → likely_inconsistent

| item | label | requirement_quote | FaaP summary (short) |
|---|---|---|---|
| L001 | NOT | – | ~330 shard folders in the output root, over the 30-item limit |
| L045 | NOT | – | read the 30-item limit as per-file; 396 folders in the root |
| L117 | NOT | – | 330+ folders in the root, over the 30-item limit |
| L151 | NOT | – | never counted subfolders toward the 30-item limit |
| L282 | NOT | – | decompress.py does not restore file names |
| L379 | NOT | – | decompress.py leaves extra files behind |
| L089 | ANCHORED | "reverts it back to the original structure in-place" | restored to a sibling folder; **also** 130+ folders in the root |
| L142 | ANCHORED | "reverts it back to the original structure in-place" | restored to a new folder, not in place |
| L259 | ANCHORED | "Help me create two scripts ... /app/compress.py ... /app/decompress.py" | deleted the finished scripts |
| L405 | ANCHORED | "... Maximum 30 files or folders in each directory ..." | copied uncompressed files into part_* folders |

L001, L045, L117, L151 (NOT) broke the 30-item limit. L405 (ANCHORED) quotes that limit.

**This does not match the example in the task prompt.** The prompt said L089, L142, L259, L405 all quote
"Maximum 30 files or folders". In the file, only L405 does. L089 and L142 quote the "in-place" clause, and
L259 quotes the script-creation clause. Also, FaaP's summary for L405 is mainly about uncompressed copies,
not the 30-item limit. The verdict is still `likely_inconsistent`.

## Needs a human decision

1. **The 23 `likely_inconsistent` tasks.** See `consistency_list.csv`. Example: intrusion-detection, where
   NOT runs L006, L042, L104, L159, L164, L258, L340 and ANCHORED runs L146, L222 all wrote to /app/reports.
   Note: rare-mineral-allocation is `different_failures` (its ANCHORED run L039 is a different failure).
2. **Three kinds of disagreement inside `likely_inconsistent`:**
   - NOT vs ANCHORED (most tasks).
   - NOT vs UNCLEAR: movie-helper (L043), puzzle-solver (L338), vul-flink (L355).
   - Same label, different quotes for the same miss: acl-permissions-inheritance, gpt2-codegolf,
     hf-train-lora-adapter, multi-source-data-merger.
3. **The 8 `cannot_tell` tasks** need someone to read the trajectories, not just FaaP's one sentence.
4. **Two ANCHORED rows mention "implicit" in the note** (found by the count check):
   L048 (note is exactly "implicit") and L319 (long note that discusses NOT + implicit).
   The label and the note seem to disagree.

## Limits

- Verdicts use FaaP's one-sentence summary, trigger and category. They do not use the full trajectories.
  FaaP's summaries are LLM-written and can be wrong.
- The quote check is simple text matching. Two quotes for the same clause written differently would be flagged.
  The verdict step catches this.
- Out of scope, not checked: NOT runs that agree with each other but may all be wrong (for example,
  in audio-synth-stft-peaks, NOT runs L194, L218, L393, L400 broke the "RMS 0.2" rule). Also notes that differ between runs with the
  same label and same failure (install-windows-3.11: some monitor-socket runs say "implicit", some do not).
