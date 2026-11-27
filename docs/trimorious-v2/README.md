# Trimorious 2.0 — Scientific intelligence research edition

This directory documents the November 2026 experimental QLoRA adapter and its development pipeline. The existing Qwen2.5-based model on the default branch remains the original baseline. The Qwen3 adapter is **not** supplied here; its target Hub repository is [roime81/trimorious-research-4B-v2](https://huggingface.co/roime81/trimorious-research-4B-v2). The supplied audit records a private upload, not an independently verified public release.

## Start here

- [Scientific Intelligence Handbook — full text companion](../book/Trimorious_2_0_The_Scientific_Intelligence_Handbook.txt)
- [Book PDF information](../book/README.md)
- [Complete seven-stage Colab notebook](../../notebooks/Trimorious_2_0_Complete_Seven_Stage_Release.ipynb)
- [Sequential workflow guide](../../notebooks/sequence/START_HERE.md)
- [CPU playground](../../notebooks/Trimorious_2_0_CPU_Playground.ipynb)
- [GPU Gradio playground](../../notebooks/Trimorious_2_0_Gradio_Playground.ipynb)
- [Dataset engineering companion repository](https://github.com/roime81/trimorious-datasets/tree/docs/trimorious-v2-data-engineering)
- [Research results and limitations](RESULTS.md)

Use the combined notebook OR the numbered sequence, not both. Archived notebooks are retained for history; do not rerun teacher augmentation or regenerate approved data unnecessarily. The release notebooks require privately retained source archives, benchmark materials and genuine approvals. They are not self-contained public benchmark distributions. Run outputs and credentials are excluded.

## Architecture

Current scope: Qwen3-4B-Instruct-2507 with a PEFT LoRA adapter, trained with 4-bit NF4 QLoRA on a Tesla T4. External symbolic engines were used for offline dataset checks. Runtime RAG, adaptive routing, scientific agents, specialist models, MCP, simulation and the research studio are planned, not delivered by this adapter.

## Release policy

Do not substitute this documentation for scientific review. Preserve the original model and datasets; do not publish a private benchmark, gold answers, unapproved training records, reviewer identities, credentials or private audit archives. Model and dataset licensing and redistribution rights must be reviewed independently. Publication requires explicit approval.
