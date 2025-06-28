"""
LLM Inference Calculator
This module estimates latency, memory usage, and cost for different language models on various hardware configurations.
"""

# Constants (estimated values based on common sources)
MODEL_PARAMS = {
    "7B": 7e9,
    "13B": 13e9,
    "gpt-4": 175e9  # Approximate parameter count for GPT-4
}

GPU_MEMORY = {
    "A100": 80,
    "T4": 16,
    "RTX 4090": 24
}

GPU_LATENCY_PER_TOKEN = {
    "A100": 0.5,       # ms/token
    "T4": 1.2,
    "RTX 4090": 0.8
}

GPU_COST_PER_HOUR = {
    "A100": 3.0,      # USD/hour (cloud estimate)
    "T4": 0.6,
    "RTX 4090": 1.2
}

def estimate_memory_usage(model_size: str, batch_size: int) -> float:
    """Estimate memory usage in GB."""
    params = MODEL_PARAMS.get(model_size, 0)
    param_memory = params * 2 / 1e9  # Assuming 2 bytes per param (fp16)
    return round(param_memory + batch_size * 0.1, 2)  # Batch buffer overhead

def estimate_latency(tokens: int, batch_size: int, hardware: str) -> float:
    """Estimate inference latency in milliseconds."""
    per_token_latency = GPU_LATENCY_PER_TOKEN.get(hardware, 1.0)
    return round(tokens * batch_size * per_token_latency, 2)

def estimate_cost(latency_ms: float, hardware: str, deployment: str) -> float:
    """Estimate cost of a single request in USD."""
    cost_per_hr = GPU_COST_PER_HOUR.get(hardware, 1.0)
    latency_hr = latency_ms / (1000 * 60 * 60)
    multiplier = 1.0 if deployment == "cloud" else 0.5
    return round(latency_hr * cost_per_hr * multiplier, 4)

def check_compatibility(model_size: str, hardware: str, batch_size: int) -> bool:
    """Check if model fits into GPU memory."""
    required_mem = estimate_memory_usage(model_size, batch_size)
    available_mem = GPU_MEMORY.get(hardware, 0)
    return required_mem <= available_mem

def run_inference_calculation(model_size: str, tokens: int, batch_size: int, hardware: str, deployment: str) -> dict:
    """Run full inference cost and performance estimation."""
    latency = estimate_latency(tokens, batch_size, hardware)
    memory = estimate_memory_usage(model_size, batch_size)
    cost = estimate_cost(latency, hardware, deployment)
    compatible = check_compatibility(model_size, hardware, batch_size)
    return {
        "latency_ms": latency,
        "memory_gb": memory,
        "cost_usd": cost,
        "hardware_compatible": compatible
    }

if __name__ == "__main__":
    test_cases = [
        ("7B", 500, 4, "A100", "local"),
        ("gpt-4", 1000, 1, "A100", "cloud"),
        ("13B", 300, 2, "RTX 4090", "local")
    ]

    for model, tokens, batch, gpu, mode in test_cases:
        result = run_inference_calculation(model, tokens, batch, gpu, mode)
        print(f"\nModel: {model} | Tokens: {tokens} | Batch: {batch} | GPU: {gpu} | Mode: {mode}")
        for k, v in result.items():
            print(f"{k}: {v}")