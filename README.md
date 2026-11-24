---
base_model: unsloth/Qwen2.5-3B-Instruct-bnb-4bit
tags:
- trimorious
- scientific-research
- qlora
- unsloth
- text-generation-inference
- transformers
- qwen
license: apache-2.0
language:
- en
---

# trimorious-research-4B

**trimorious** is a domain-adapted scientific research language model trained on top of `unsloth/Qwen2.5-3B-Instruct-bnb-4bit` using efficient QLoRA techniques with `unsloth`.

## Model Details
- **Developed by:** scientific community / trimorious project
- **Model Type:** Causal Language Model via QLoRA tuning
- **Base Model:** `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`
- **Languages:** English
- **License:** Apache 2.0

## Training & Dataset Specifications
- **Tuning Framework:** Unsloth + TRL
- **Parameters:** LoRA Rank 16, Alpha 16
- **Batch Size:** 2 (Accumulation: 4)
- **Learning Rate:** 2e-4 (Cosine)
- **Dataset Sources:** Academic literature downloaded directly from arXiv APIs and OpenAlex.
- **Data Preprocessing:** Handled via the high-fidelity `docling` parser for perfect math transcription.

## How to Use
```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "YOUR_HF_USERNAME/trimorious-research-4B",
    max_seq_length = 2048,
    load_in_4bit = True
)
FastLanguageModel.for_inference(model)
```

## Scientific Limitations & Disclaimers
Trimorious is tailored to synthesize papers and analyze methodologies but may inherit mathematical hallucination tendencies typical of foundational models. Critical research should be cross-referenced mathematically using symbolic verification.
