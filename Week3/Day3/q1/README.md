# LLM Inference Calculator

Estimate latency, memory usage, and cost for running large language models (LLMs) on various hardware and deployment settings.

---

## 📦 Features

* Support for popular model sizes: 7B, 13B, GPT-4
* Cost, latency, and memory usage estimation
* Hardware compatibility checking
* Configurable for local vs cloud deployment

---

## 📥 Inputs

* `model_size`: "7B", "13B", "gpt-4"
* `tokens`: Number of tokens in the request (e.g., 500)
* `batch_size`: Number of parallel inferences
* `hardware_type`: e.g., "A100", "T4", "RTX 4090"
* `deployment_mode`: "local" or "cloud"

---

## 📤 Outputs

* `latency_ms`: Estimated latency in milliseconds
* `memory_gb`: Estimated GPU memory usage in GB
* `cost_usd`: Estimated cost per request (USD)
* `hardware_compatible`: Boolean — whether the model fits into GPU memory

---

## 🚀 How to Run

```bash
python inference_calculator.py
```

Modify the test cases in the `__main__` block to try different configurations.

---

## 🧠 Assumptions

* 2 bytes per parameter (fp16)
* Static latency per token by GPU type (empirical)
* Cost derived from GPU hourly rates
* Local hardware assumed to be 50% cheaper than cloud

See `research_notes.md` for details.

---

## 📊 Use Case Scenarios

Run `scenario_analysis.md` for 3 pre-defined comparisons:

* Efficient batch inference (7B on A100)
* GPT-4 on cloud A100 (incompatible)
* 13B on RTX 4090 (too large)

---

## 📁 File Structure

```
├── inference_calculator.py   # Python calculator module
├── research_notes.md         # Research sources and assumptions
├── scenario_analysis.md      # 3 test cases and insights
├── README.md                 # Project overview and instructions
```

---

## ✅ To Do / Extend

* Add UI using Streamlit or CLI arguments
* Use real benchmark data for latency and memory
* Support quantized models (4-bit, 8-bit)
