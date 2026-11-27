# Research results — recorded audit evidence

As of 27 November 2026. The following values were recorded in the supplied Colab release audit and reviewed for consistency; this is not an independent rerun of the trained model. Raw evaluation responses and human review evidence were not supplied.

| Model | TSIB D07 objective accuracy |
|---|---:|
| Trimorious v1 (historical) | 45.80% |
| Qwen2.5 foundation (historical) | 51.02% |
| Phi-4-mini (historical) | 62.27% |
| Qwen3 foundation | 69.09% |
| Trimorious 2.0 | 69.32% |

D07: 610/880 versus 608/880, +0.23 percentage points; six wins and four losses; exact McNemar p=0.75390625; template bootstrap 95% interval [-0.35,+0.89] percentage points. Fresh test: 78/100 versus 75/100, p=0.25; benchmark independence not established by supplied artifacts. Neither overall comparison establishes statistically significant improvement.

| Capability | Base | Adapter |
|---|---:|---:|
| Mathematical reasoning | 20.50% | 19.50% |
| Scientific reasoning | 54.67% | 56.67% |
| Statistics | 74.17% | 74.17% |
| Scientific verification | 86% | 87% |
| Strict protocol compliance | 99.9% | 96.7% |
| Mean latency | 1.90 s | 3.44 s |

Training: pinned Qwen/Qwen3-4B-Instruct-2507 revision cdbee75f17c01a7cc42f958dc650907174af0554; 288 training examples, 36 validation examples; 24 training templates; one epoch; 18 optimizer steps; NF4 FP16, rank 8, alpha 16, dropout 0.05, maximum sequence length 512, gradient accumulation 16, learning rate 0.0001. Reported peak PyTorch allocated memory 4.28 GiB; runtime 276.21 s; final validation loss 2.65846. No teacher-generated responses or multi-tool trajectories were trained. DPO and GRPO skipped.

Adapter weights SHA-256 as recorded in the audit: 5ce2eadc1ca1f33d28b2a6a517eaad53a73263441c5519c3dc662590514a609d. Actual remote weights and private Hub commit not independently verified.

**Experimental scope only.** Most improvement over v1 is attributable to the foundation model change. Outstanding evidence: rubric review discrepancy (120 pending in evaluation report), raw responses, independent benchmark provenance, release threshold history, upload receipt, clean reload, safety and serving validation. Do not assert production readiness or full hybrid intelligence.
