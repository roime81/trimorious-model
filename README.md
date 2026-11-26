---
base_model: unsloth/Qwen2.5-3B-Instruct-bnb-4bit
license: apache-2.0
language:
  - en
pipeline_tag: text-generation
tags:
  - trimorious
  - scientific-research
  - qlora
  - peft
  - unsloth
  - qwen
  - adapter
---

# Trimorious Research 4B

**Current artifact:** research-stage QLoRA/LoRA adapter for scientific and research-oriented text generation.

> **Release status:** This repository is the original research baseline. A complete independent benchmark, safety evaluation, end-to-end training reproduction and production inference validation have not yet been published. Do not treat the model as scientifically verified or production-certified.

## Model identity

| Property | Current documented value |
|---|---|
| Model repository | `roime81/trimorious-research-4B` |
| Artifact type | PEFT LoRA adapter |
| Declared base model | `unsloth/Qwen2.5-3B-Instruct-bnb-4bit` |
| Fine-tuning method | QLoRA / LoRA |
| Task | Causal language modelling / text generation |
| Language | English |
| Adapter rank | 16 |
| LoRA alpha | 16 |
| LoRA dropout | 0 |
| License metadata | Apache-2.0 (verify upstream and dataset rights separately) |

### Naming clarification

The public repository name contains `4B`, but the checked-in adapter configuration points to `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`. The name is retained for repository continuity; it is **not evidence of a verified 4-billion-parameter architecture**. The exact base checkpoint and parameter count must be confirmed in the release manifest before changing the name.

This repository contains adapter weights, not a standalone full-weight model. Inference requires the compatible base model and adapter-loading support (for example, PEFT/Unsloth).

## Adapter configuration

The checked-in `adapter_config.json` declares:

- PEFT type: `LORA`
- Task type: `CAUSAL_LM`
- Rank: `16`
- Alpha: `16`
- Dropout: `0`
- Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`

The model repository does not include the full base-model weights. Download the exact base model separately and use a compatible adapter loader.

## Training information currently available

The previous model documentation reports:

- Framework: Unsloth + TRL
- Per-device batch size: 2
- Gradient accumulation: 4
- Learning rate: 2e-4
- Scheduler: cosine
- Data source description: academic literature obtained through arXiv APIs and OpenAlex
- Document parsing: Docling

These are **reported configuration details, not a verified training run manifest**. The repository does not currently establish the exact training commit, seed, number of epochs/steps, optimizer settings, training sequence length, effective token count, exact dataset revisions, hardware, package lock or full logs. See `training_config.template.yaml` for the fields required to reconstruct a verifiable run.

## Context length

The tokenizer configuration declares a maximum length of 32,768 tokens, while the original inference example used 2,048 tokens. The base model's advertised context limit does not prove that this adapter was trained or evaluated successfully at 32K.

Until context benchmarks are published, use conservative context settings and validate memory/performance on your own hardware. Context performance at 8K, 16K and 32K remains unverified.

## Use and limitations

Potential research use:
- drafting and explaining scientific concepts;
- summarizing research material supplied by a user;
- exploring scientific methods and hypotheses;
- assisting with research workflows under human review.

Known limitations:
- Scientific or mathematical statements may be incorrect or fabricated.
- Citations and source claims must be independently checked.
- The current release has no published standardized benchmark results.
- Tool execution, agentic reliability and recovery behavior have not been independently validated.
- Safety, prompt-injection resistance, privacy and multilingual performance have not yet been certified.

Do not use the model as the sole authority for clinical, legal, financial, safety-critical, engineering or other high-impact decisions. A qualified human and independent verification are required.

## Evaluation status

No independently verified benchmark numbers are published in this repository at this stage. The machine-readable status is recorded in `evaluation_status.json`. Results will be added only after the original base model and this adapter are evaluated on the same frozen benchmark.

## Loading

The original release documentation uses the following Unsloth loading pattern. Validate it with the exact installed Unsloth, Transformers, PEFT and PyTorch versions before deployment:

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="roime81/trimorious-research-4B",
    max_seq_length=2048,
    load_in_4bit=True,
)

FastLanguageModel.for_inference(model)
```

For custom production deployments, pin the base model revision, adapter revision, tokenizer revision and package versions in your own environment.

## Reproducibility and lineage

A reproducible release must record:

1. exact base-model repository and commit SHA;
2. adapter and tokenizer revisions/checksums;
3. chat-template hash;
4. dataset repositories, immutable revisions, splits and filtering code;
5. complete training arguments, seeds and package versions;
6. GPU hardware, runtime, checkpoints and training logs;
7. evaluation benchmark revision, scoring code and results.

The current artifact is retained as the baseline while these details are reconstructed. Future upgrades will be released as versioned candidates rather than silently replacing the historical baseline.

## Licensing

The repository includes Apache-2.0 license metadata. This does not automatically grant redistribution rights to upstream base-model weights or third-party source documents used during training. Review the base model's terms and the provenance/license of all training materials independently before commercial or redistributed use.

## Project

Trimorious is being developed as a research-oriented scientific AI project. The engineering backlog, dataset schemas and release gates are maintained in the [Trimorious dataset engineering repository](https://github.com/roime81/trimorious-datasets).
