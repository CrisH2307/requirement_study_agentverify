## Data Legends

| Field (in JSON) |	Meaning | Paper name | Codebook section |
| --- | --- | --- | --- |
| t_err	| Step of the decisive error | t_err | §2 |
| t_commit	| Step after which the failure is locked in | t_lock| §2 |
| t_surface |	First step with a visible failure signal; empty = silent | t_obs | §2 |

## Data Regulation:
- steps are started from 1

## Run identifier (`case_id`)
Each record is one **run** = one model, inside one scaffold, attempting one task.
`case_id` has 3 parts separated by `__` (double underscore):

`<task>__<scaffold>__<model>` — e.g. `acl-permissions-inheritance__miniswe__gemini`

| part | meaning | values |
|---|---|---|
| task | Terminal-Bench task; **use this to group runs by task** | 89 tasks; matches `task_id` in `data/raw/merged_tasks.json` |
| scaffold | agent framework that runs the model | `miniswe`, `openhands`, `terminus2` |
| model | base LLM | `claude`, `gpt5`, `gemini`, `qwen`, `kimi`, `devstral`, `deepseek-v3.2` |

- Get the task: `case_id.split("__")[0]`
- Design is 89 × 3 × 7 = 1869 runs, but the data has 1794 → 75 runs missing.


## Observation
- In Corpus dataset from Failure as a Process, there are 89 tasks in full
- However, we observed that there are 2 tasks with NO failed run, and 87 tasks with at least one failed run. Which is all 21 runs of csv-to-parquet and fix-git passed

## Fields in both
| field | type | example | meaning |

## FAIL-only fields
| field | type | example | meaning |

## PASS-only fields
| field | type | example | meaning |