# Labeling examples: 26 hard cases decided by Cris

These are rows where two independent AI drafts disagreed, so they are the hardest cases in the set. They show how
the guide (`docs/labeling_guide.md`) was applied. They are not the only right answers: if you disagree with one,
raise it with the team instead of copying it. Rows in the blind reliability set are left out on purpose.

| Item | Task | Label | Task text (exact words) | Why |
|---|---|---|---|---|
| L026 | `extract-elf` | **ANCHORED** | You need to extract at least 75% of the memory values that are present in the reference solution | Agent: "Step 7 creates extract.js that explicitly skips .text ('.text' // '.init' // '.fini' are excluded) while only targeting …" |
| L060 | `chem-rf` | **ANCHORED** | the model must get a spearman correlation score less than -0.57 on the test set | Agent: "model = RandomForestRegressor(...); model.fit(X_train, train_targets) predicting target_enrichment with standard featuri…" |
| L124 | `constraints-scheduling` | **ANCHORED** | The meeting must not conflict with existing calendar entries and must satisfy ALL availability constraints. | Agent: "Jan 16 10:00-11:00" |
| L169 | `heterogeneous-dates` | **ANCHORED** | daily high and daily low temperatures | Agent: "Since both have same number of rows, we can assume they are paired by line order (excluding header). That's likely the i…" |
| L284 | `mcmc-sampling-stan` | **ANCHORED** | Install the RStan package (version 2.32.7) for R and the required dependencies for Stan | Agent: "Step 5 attempts to install cmdstanr (the wrong package) from a non-standard repo with type='binary' (unsupported on Linu…" |
| L330 | `triton-interpret` | **ANCHORED** | You are NOT allowed to use triton.language.sum (tl.sum) | Agent: "tl.sum" |
| L405 | `reshard-c4-data` | **ANCHORED** | Maximum 30 files or folders in each directory | Agent: "compress.py created with flat part_* layout, creating hundreds of subdirs at root, violating <=30 constraint" |
| L017 | `add-benchmark-lm-eval-harness` | **NOT** | (nothing in the task text) | implicit. Draft reason: Agent's wrong beliefs about the data files and the README's Task 2 filter drove the failure, not a dropped task-text requirement. |
| L029 | `count-dataset-tokens` | **NOT** | (nothing in the task text) | implicit. Draft reason: The metadata configuration is only described in the README; the task's README pointer is a hint, not a requirement. |
| L059 | `count-dataset-tokens` | **NOT** | (nothing in the task text) | implicit. Draft reason: Agent tried to filter science content; the metadata config and fields are README knowledge, not task text. |
| L078 | `count-dataset-tokens` | **NOT** | (nothing in the task text) | implicit. Draft reason: Agent tried to identify science entries; the metadata config and fields come from the README, not task text. |
| L091 | `path-tracing-reverse` | **NOT** | (nothing in the task text) | (see failure_summary in the CSV) |
| L256 | `count-dataset-tokens` | **NOT** | (nothing in the task text) | implicit. Draft reason: README hint is not a requirement; agent aimed at science-domain count but missed the metadata config. |
| L266 | `chem-rf` | **NOT** | (nothing in the task text) | implicit. Draft reason: Task says the evaluator runs the script; a pre-produced trained_model.pkl is not clearly required by the text. |
| L271 | `count-dataset-tokens` | **NOT** | (nothing in the task text) | implicit. Draft reason: README hint is not a requirement; agent aimed at science-domain count but missed the metadata config. |
| L296 | `build-cython-ext` | **NOT** | They should still pass after fixing compatibility issues | implicit |
| L314 | `intrusion-detection` | **NOT** | (nothing in the task text) | implicit. Draft reason: Threshold and timeframe fields live only in the rules data file, not the task text. |
| L326 | `mteb-leaderboard` | **NOT** | according to the Scandinavian MTEB leaderboard (i.e. highest Mean (Task)) as of August 2025 | Agent aimed at finding the answer but chose an ineffective local search; the task does not state how to look it up.. Draft reason: Agent aimed at finding the answer but c… |
| L340 | `intrusion-detection` | **NOT** | (nothing in the task text) | I feel that the task names the incident report as incident_<IP>_<timestamp>.txt but does not specify a folder. The agent used /app/reports/, so the folder was implicit. |
| L374 | `chess-best-move` | **NOT** | (nothing in the task text) | (see failure_summary in the CSV) |
| L411 | `winning-avg-corewars` | **NOT** | (nothing in the task text) | Draft reason: Agent aimed at the 75% threshold but misjudged 73 as passing. |
| L008 | `git-workflow-hack` | **UNCLEAR** | modify workflows if necessary | ask says modify workflows, but does not clearly say deleting the workflow is forbidden. Draft reason: Agent deleted the malicious workflow rather than editing it; task on… |
| L020 | `add-benchmark-lm-eval-harness` | **UNCLEAR** | (nothing in the task text) | unclear whether the benchmark requirement was ignored or never reached. Draft reason: Agent started with the dataset step and was stuck on network timeouts; cannot tell i… |
| L043 | `movie-helper` | **UNCLEAR** | (nothing in the task text) | task text does not clearly say how the full matrix must be reconstructed. Draft reason: Task text never says matrix completion; unclear if random data matching statistics… |
| L338 | `puzzle-solver` | **UNCLEAR** | Each row represents a move in the optimal solution step | task text does not clearly specify these exact formatting/termination details. Draft reason: Task says rows are moves but also numbers steps from 0; the layer stop-at-goa… |
| L355 | `vul-flink` | **UNCLEAR** | After making the code change, rebuild the Flink distribution so the runtime jars include the fix. | Explanation identifies the skipped distribution rebuild, while mistake_quote identifies the incomplete regex sanitization; the decisive mistake is unclear.. Draft reason:… |
