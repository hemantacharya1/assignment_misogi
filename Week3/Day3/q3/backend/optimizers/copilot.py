# optimizers/copilot.py

def optimize_prompt(base_prompt: str) -> dict:
    """
    GitHub Copilot works best with:
    - Clear function/class headers
    - Inline comments for intent
    - Descriptive naming and typing hints (if applicable)
    """

    optimized = f"{base_prompt.strip()}\n\n" \
                "# Please write this using Python best practices.\n" \
                "# Add type hints and inline comments to clarify each step."

    explanation = (
        "Copilot benefits from inline comments and clear structure to predict the next lines. "
        "We've instructed it to use Pythonic patterns, type hints, and commentary."
    )

    return {
        "optimized_prompt": optimized,
        "explanation": explanation
    }
