# Trimorious 2.0 — Sequential Colab development

Use these seven self-contained notebooks **in numerical order**. This is the controlled experimental QLoRA release path, split from the existing all-in-one implementation. No teacher inference or new dataset generation. Do not run the old notebook in parallel.

## Shared Drive workspace

`/content/drive/MyDrive/trimorious_PRIVATE_m1_4_1/`

Required source: `trimorious_m1_4_1_PRIVATE_GPU_partial_20261127T061605946898Z.zip` (already reported saved). The original source and `teacher_checkpoints.sqlite3` are read-only. Derived state, approved datasets, smoke receipts, checkpoints, evaluation DB and release package are written under `release_v2/`. Existing review decisions are retained; if the review selection changes, the notebook stops instead of overwriting them.

| Notebook | Runtime | What to do / gate |
|---|---|---|
| 01 M1.4.2 Recover and Review | CPU | Run all; inspect recovery.json and review_queue.csv. Default 288 development + 36 validation candidates. Fill decision, reviewer, notes after real review. |
| 02 M1.5 Dataset Approval | CPU | After review and rights confirmation set DATA_LICENSE_REVIEWED and DATA_REVIEW_APPROVED true. Run all. Verify dataset_approval.json. Review the proposed release thresholds before freezing. |
| 03 M2.0 QLoRA Smoke Test | T4 GPU | Clean runtime. Run all. Verify matching smoke_pass.json (10 optimizer steps). |
| 04 M2.0 Full QLoRA Training | T4 GPU | Clean runtime. Same training config as 03. Run all; if interrupted, rerun 04 unchanged. Verify training_complete.json and final_adapter. |
| 05 M2.3 Model Evaluation | T4 GPU | Clean runtime. Supply D07 ZIP plus externally authored fresh test and seal. Run all; if interrupted, rerun 05 unchanged. Review evaluation report and fill blinded rubric CSV. |
| 06 M2.3 Release Packaging | CPU | After review and redistribution rights confirmation set HUMAN_EVAL_APPROVED and DATA_LICENSE_REVIEWED true. Run all. Inspect package. |
| 07 M2.3 Hugging Face Publication | CPU | Add HF_TOKEN to Colab Secrets. Reconfirm review/rights; set PUBLISH_APPROVAL to PUBLISH TRIMORIOUS 2.0. First run with MAKE_PUBLIC false. Inspect verified private repository, then rerun with MAKE_PUBLIC true and PUBLIC_APPROVAL set to MAKE TRIMORIOUS 2.0 PUBLIC. |

The GPU stages run in separate Python processes. Do not run notebooks concurrently. Save notebooks to Drive. You may delete the runtime between stages after verifying the persistent outputs. Reconnect with a T4 for 03–05; GPU availability and quotas are not guaranteed. No purchases are initiated.

## Independent benchmark requirement

Save the original private `trimorious_m1_3_2_PRIVATE_full_1c3d70c27cc3c9f8.zip` to the project root before notebook 05. It is intentionally not included in this notebook bundle. In addition, obtain a new, independently authored and reviewed confirmation set (at least 100 objective questions and 10 templates) from a reviewer who has not seen the adapter's evaluation outputs. Prefer sealing before training; set the externally provided SHA-256 in notebook 02 if available. Notebook 05 checks the hash and lexical overlap. A separately authored test is not supplied here; the notebook must not generate its own confirmation set from training data.

Format: UTF-8 JSONL, one object per line, fields id, question, template, family, kind, gold, and for numeric questions atol and rtol. Choices use A–D options in the question with gold a single uppercase letter. The independent author must validate the answers and tolerances. Set the path, hash and independence attestation in notebook 05. Keep the test private. Do not tune or select checkpoints on it. No fabricated benchmark or automatic scientific approval.

## Scope and limitations

The initial SFT subset is intentionally conservative: numerical math, science and statistics; 2,250 supported candidate answers were locally recomputed, with a per-template cap selecting 324 for review. Existing teacher outputs, narrative data and tool traces are kept for audit but are not trained on. The notebooks do not generate a new 30,000-example dataset, implement semantic deduplication beyond the existing checks, run DPO/GRPO, publish source datasets, or export merged/GGUF weights. Optional optimization requires separate preference/reward data and validation; it should not be applied merely to force a release pass. The release is a PEFT adapter requiring the pinned Qwen3 foundation, not standalone weights. Full GPU training, evaluation and Hugging Face upload have not been executed locally. See CPU_validation.json for actual tests; test fixture approvals are not scientific approvals.

Publication is to a new repository only: `roime81/trimorious-research-4B-v2`. Original v1 and GitHub/Hugging Face assets remain unchanged. Never bypass a failed gate. The notebooks create small private audit ZIPs with report hashes after successful stages; source data and weights remain in Drive.