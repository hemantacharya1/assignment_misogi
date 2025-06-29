# Research Notes: LLM Inference Calculator

## 📌 Goals

Understand how LLM inference behaves across different model sizes and hardware to estimate latency, memory usage, and cost.

---

## 🤖 Model Sizes Compared

| Model | Parameters | Notes                           |
| ----- | ---------- | ------------------------------- |
| 7B    | 7 Billion  | Common open-source size (LLaMA) |
| 13B   | 13 Billion | Higher accuracy, more memory    |
| GPT-4 | \~175B     | Proprietary, very high-end      |

---

## ⚙️ Hardware Overview

| GPU      | VRAM (GB) | Notes                        |
| -------- | --------- | ---------------------------- |
| A100     | 80        | Standard for cloud inference |
| T4       | 16        | Budget GPU in GCP/AWS        |
| RTX 4090 | 24        | High-end consumer GPU        |

---

## 📏 Estimation Assumptions

* **Parameter memory** = 2 bytes/parameter (FP16)
* **Latency** = `tokens × batch × per-token latency` (empirical)
* **Memory usage** = Model size + buffer per batch
* **Cost** = Based on GPU hourly price × usage time

---

## 📉 Latency per Token (Empirical)

| GPU      | Latency per token (ms) |
| -------- | ---------------------- |
| A100     | 0.5                    |
| T4       | 1.2                    |
| RTX 4090 | 0.8                    |

---

## 💵 GPU Hourly Pricing (Estimated)

| GPU      | Cloud Price (USD/hr) |
| -------- | -------------------- |
| A100     | 3.0                  |
| T4       | 0.6                  |
| RTX 4090 | 1.2                  |

---

## 🛠 Deployment Mode Assumptions

* `cloud`: full price
* `local`: 50% discount (owned hardware)

---

## 🔍 Sources

* Hugging Face Inference API
* Lambda Labs Pricing & Benchmarks
* MosaicML Benchmark Blogs
* OpenAI Model Docs
* NVIDIA Hardware Specs
