# optimizers/replit.py

def optimize_prompt(base_prompt: str) -> dict:
    """
    Replit Ghostwriter/Agent performs well when:
    - Given REPL-friendly, step-by-step instructions
    - The prompt includes examples or expected outputs
    """

    optimized = (
        f"{base_prompt.strip()}\n\n"
        "# Provide example input/output if possible.\n"
        "# Ensure the code can run in a REPL environment with print statements."
    )

    explanation = (
        "Replit works well in interactive REPL settings. "
        "We added a suggestion to use print statements and examples to make the prompt more testable and interpretable in a browser-based IDE."
    )

    return {
        "optimized_prompt": optimized,
        "explanation": explanation
    }
