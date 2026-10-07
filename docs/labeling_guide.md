# Labeling guide: is this failure requirement-related?

## Short version (read this first)

For each row:
1. Read `requirement_text`: what the agent was asked to do.
2. Read `failure_summary` and `mistake_explanation`: what went wrong.
3. Ask: **did the agent stop doing something the task text clearly asked for?**
   - **Yes** (it skipped it, forgot it, misread it, or did something else instead): write `ANCHORED`,
     copy the task's words into `requirement_quote` and the words showing what the agent did into `evidence_quote`.
   - **No**, it was trying to do what was asked but failed for another reason (broken environment, missing
     know-how, buggy code): write `NOT`.
   - **Can't tell** from the text: write `UNCLEAR` and say why in `note`.
4. **Tie-breaker when unsure between ANCHORED and NOT:** imagine the agent's own plan had worked perfectly.
   Would the task text's requirement then be met?
   - **No** (its plan targets something else: another version, another input, a made-up position or data,
     a narrower or wider scope): `ANCHORED`.
   - **Yes** (the plan targets the right thing; only the execution, knowledge or environment failed): `NOT`.
5. **Only the task text counts.** A hint such as "X is installed" or "the README has details" is not a
   requirement by itself. If what the agent missed is only in a README, a data file or the hidden test
   (for example, an output file name the task never mentions), write `NOT` and `implicit` in `note`.
6. Label alone. Don't look at anyone else's labels.

Example ANCHORED: task says "use the Qwen2.5 tokenizer", agent used Qwen2.
Example NOT: task says "create an S3 bucket", agent tried but wrongly assumed it needed real AWS credentials.

The rest of this guide explains the same rule in more detail, for hard cases.


## What you get for each row (`labels/checklist.csv`)

| Column | What it is |
|---|---|
| `requirement_text` | What the agent was asked to do, copied from the Terminal-Bench task file |
| `failure_summary` | FaaP's one-sentence description of how the run failed |
| `mistake_explanation` | FaaP's explanation of the decisive mistake (the step where the run went wrong) |
| `mistake_quote` | FaaP's quote from the run at that step |

You do **not** see FaaP's labels or anything about timing or silence. That is on purpose.

## The one question

> **At the decisive mistake, did the agent stop working toward something the task text explicitly asked for?**

Answer it with three checks, in order:

1. **Point to the requirement.** Is there a sentence or phrase in `requirement_text` that the agent's work did not satisfy?
   If no, the label is **NOT**.
2. **Was the agent aiming at it?** At the decisive mistake, was the agent still working toward that sentence as written?
   - **No**: it ignored, forgot, misread, replaced, narrowed or gave up on it. The label is **ANCHORED**.
   - **Yes**, but it failed for another reason (the environment, missing know-how, a bug in its code). The label is **NOT**.
   - Unsure? Use the tie-breaker: if the agent's own plan had worked perfectly, would the requirement be met?
     No means ANCHORED, yes means NOT.
3. **Not enough information** to answer check 1 or 2? The label is **UNCLEAR**.

Judge the **decisive mistake**, not what happened afterwards. If the agent made a coding error first and faked a result
later, the decisive mistake is the coding error (NOT).
Judge **what the agent did to the requirement**, not why. If a wrong belief made the agent drop a stated requirement,
it is still ANCHORED.

## What to fill in

| Column | ANCHORED | NOT | UNCLEAR |
|---|---|---|---|
| `label` | `ANCHORED` | `NOT` | `UNCLEAR` |
| `requirement_quote` | Required: the exact words from `requirement_text` | Optional | Optional |
| `evidence_quote` | Required: the exact words from FaaP's text showing the agent did not aim at it | Optional | Optional |
| `note` | Optional | Write `implicit` if the missed expectation is not written in the task text | Say what is missing |

## Worked examples

**ANCHORED: `count-dataset-tokens__terminus2__gemini`**
- Requirement: "You should use the Qwen2.5-1.5B-Instruct tokenizer"
- Evidence: "writes token_counter.py using 'Qwen/Qwen2-1.5B-Instruct' instead of the task-specified 'Qwen2.5-1.5B-Instruct'"
- Why: the agent replaced a stated requirement with something else. Nothing errors, and the answer is just wrong.

**ANCHORED: `build-cython-ext__miniswe__gemini`** (harder case)
- Requirement: "install pyknotid from source to system's global python environment"
- Evidence: "agent runs 'pip uninstall -y pyknotid' ... planning to use 'python setup.py build_ext --inplace' instead"
- Why: FaaP calls the cause a false belief about an import error, but what the agent *did* at the decisive
  mistake was drop the global install the task asked for. We label what happened to the requirement.

**NOT: `install-windows-3.11__terminus2__kimi`**
- Requirement: "Configure QEMU to accept keyboard input programmatically"
- Evidence: "The agent understood the requirement for programmatic keyboard input and planned to configure it, but lacked the specific domain knowledge"
- Why: the agent was aiming at the requirement and missed it for lack of know-how.
  Note `implicit`: the test expects a specific monitor socket that the task text never names.

**NOT: `create-bucket__miniswe__gpt5`**
- Requirement: "Create an S3 bucket named "sample-bucket" using the aws cli and set it to public read."
- Evidence: "assumed the task environment required real AWS credentials ... without first probing the environment"
- Why: the agent aimed at the right goal. It failed on a wrong belief about the environment, not on the requirement.

These four runs are fixed as examples. 

## Rules for labelers

- Label on your own. Do not look at another person's labels, or at `labels/key.csv`, until both of you are finished.
- If a row is hard, choose UNCLEAR and write why. Do not guess.
- Do not change this guide while labeling. Write problems in `docs/decision_log.md` and fix them after both labelers finish.

## Rules added 2026-10-07

### Rule P1: The environment failed, then the agent improvised

Label what the agent delivered, not why it happened.
- If the final output fakes or replaces something the task text names, label
  ANCHORED and quote that clause.
- If the agent delivered nothing because the environment stopped it, label NOT.
- In both cases, write "env" in the note.

Example: the task says "Save the parsed results to /app/results.csv". A package
fails to install, so the agent writes made-up numbers to /app/results.csv.
-> ANCHORED, quote "Save the parsed results to /app/results.csv", note "env".

Example: a build times out and the agent stops without producing any output.
-> NOT, note "env".

### Rule P2: The agent ignored the task details

The quote must be a specific clause the output violates, never a header or
an intro line. If you cannot name a specific clause, label NOT.

Example: the task says "Create directory /data with the following properties:"
followed by a list. The agent creates /data but ignores the list.
-> ANCHORED, quote the specific list item it broke (for example
"owned by group devs"), not the "following properties" line.
