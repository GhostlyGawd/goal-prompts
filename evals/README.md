# evals/ — internal product QA (never a user-facing step)

The efficacy harness required by PRODUCT_ALIGNMENT.md ("Internal efficacy
testing") and the Gate B continuation prototypes. Compares a plain user
request against a Goal Prompt on frozen fixtures with answer keys, and
walks the GOAL_CONTRACT continuation scenarios end to end in scripted
multi-turn sessions. Nothing here appears in the user workflow (ledger
R44–R46); results inform rewrites, not marketing claims, until observed
externally (R43).

- fixtures/        frozen repos with seeded, documented defects
- answerkeys/      defect keys — NEVER copied into the run scratch
- prototypes/      contract-v2 prompt bodies under test (not in catalog)
- scenarios.json   BDD scenarios S1–S7 (multi-turn scripts)
- run.py           one arm, one fixture → report + transcript + usage
- score.py         mechanical scorer vs answer key
- driver.sh        full Gate B matrix
- results/, transcripts/  committed evidence (sanitized fixtures only)
