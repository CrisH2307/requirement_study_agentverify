# How the draft labels were made

Drafts are suggestions for Cris to confirm or change. They are not final labels and are not used for reliability.

- **Who drafted:** Claude (an LLM), split into 10 batches of about 42 rows, each batch drafted independently.
- **What the drafter saw:** only `labels/checklist.csv` (task text + FaaP's written failure description) and
  `docs/labeling_guide.md`. The drafter did **not** see FaaP's trigger/category labels, `labels/key.csv`,
  timing, or silence.
- **Two passes:**
  - Pass 1 used the first version of the guide (`labels/drafts/pass1_guide_v1.json`).
  - The guide then gained the tie-breaker and the "only the task text counts" rule (see `docs/decision_log.md`).
  - Pass 2 used the updated guide, drafted from scratch by new, independent drafters that could not see pass 1
    (`labels/drafts/pass2_guide_v2.json`).
- **Draft shown to Cris:** pass 2. Rows where the two passes disagree are marked `check_first = YES`.
- **Automatic checks on every ANCHORED draft:** the requirement quote is an exact piece of the task text, and the
  evidence quote is an exact piece of FaaP's text. All 411 rows passed.
- **Instruction given to each drafter (summary):** follow the labeling guide exactly; judge the decisive mistake,
  not later behavior; FaaP's words like "spec" or "neglect" are not evidence by themselves, so check the task text;
  copy quotes character for character; give a one-sentence reason.
