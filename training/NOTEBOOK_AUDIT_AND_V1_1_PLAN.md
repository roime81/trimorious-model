# Trimorious notebook audit and v1.1 rebuild plan

## Source reviewed

Uploaded notebook: `tremorious_model_latest(1).ipynb` (52 cells). The notebook records successful QLoRA SFT runs on a Tesla T4 for the D01-derived instruction set (3,335 train / 371 validation examples) and the knowledge-base-derived set (7,005 train / 779 validation examples). It also records generation of 225 agentic trajectories for training and 25 for evaluation.

The notebook's cell outputs show a prior Hugging Face upload of an adapter and README to `roime81/trimorious-research-4B`. That upload happened before the later knowledge-base SFT pass. The final knowledge-base adapter was saved to Google Drive, but the notebook does not show that later adapter being uploaded. This repository therefore treats the currently published model as the historical baseline until remote artifacts are explicitly checked.

## Findings requiring correction

1. **GRPO reward hacking:** the XML reward favours `<thought>` tags; the symbolic reward checks for LaTeX and the literal derivative token rather than comparing against a verified answer. These are format heuristics, not correctness rewards.
2. **GRPO failure:** the recorded run ended with `CUDA error: an illegal memory access was encountered`. It must not be described as a successful alignment run.
3. **Tool loop bug:** `messages.append("assistant", response_text)` passes two arguments to list.append and fails. Tool observations are then appended as user messages rather than a clearly typed tool result.
4. **Unsafe symbolic evaluation:** `sympy.sympify` is not a security sandbox for untrusted model-generated expressions. Tool execution needs strict parsing, allow-listed operations, timeouts and resource limits.
5. **Hidden-reasoning targets:** multiple generated answers explicitly train on `<thought>` traces. The v1.1 pipeline strips these and trains on user-facing explanations/final answers only.
6. **Synthetic data quality:** several generated answers assert generic scientific conclusions not demonstrated by the cited abstract/section. D01/D02 require audit and sampling; D04 is excluded from the first retraining pass pending trajectory validation.
7. **Knowledge-base misuse:** D03 is a retrieval corpus, not automatically a supervised answer dataset. Keep it separate for RAG and evaluate retrieval/source attribution independently.
8. **Socratic overfit:** the Socratic dataset contains only two examples. Ten steps over two examples are not evidence of robust clarification behaviour.
9. **Evaluation gap:** the notebook's qualitative outputs do not establish a reproducible benchmark improvement against the exact base model. The final test also reloads `trimorious-final-kb-adapter`, not the Socratic checkpoint, so it does not validate the Socratic fine-tune.
10. **Release lineage:** the initial adapter was uploaded before later training stages. The subsequent adapter saved to Drive is not shown being published. Record immutable base/dataset revisions, package versions, hyperparameters, hashes and benchmark outputs for every candidate.

## v1.1 execution policy

- Preserve the current Hugging Face baseline; do not overwrite `main`.
- First audit D01–D04 and normalize D01/D02 only.
- Exclude D03 from SFT and retain it as a separately versioned retrieval corpus.
- Exclude D04 and GRPO until tool traces have real tool observations and verifiable outcomes.
- Remove internal `<thought>`/`<analysis>` blocks from training targets.
- Run one controlled QLoRA SFT pass, save a candidate adapter to a separate Drive directory, and compare against the base model on the same fixed prompts.
- Publish only to a versioned candidate revision after human review and explicit approval.

The accompanying Colab notebook implements this gated first pass. Training is disabled by default and no Hugging Face publishing action is included.
