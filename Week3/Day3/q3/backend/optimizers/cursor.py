# optimizers/cursor.py

def optimize_prompt(base_prompt: str) -> dict:
    """
    Optimize the prompt specifically for Cursor AI.

    Cursor performs best when given:
    - Very clear, step-by-step natural language
    - Full function/class stubs
    - Instructions with intent (refactor, fix, comment)
    - Requests for multi-line or batch edits
    """

    # Heuristically transform the base prompt
    if "function" not in base_prompt.lower():
        optimized = f"Please write a complete, well-documented function in Python that does the following:\n\n{base_prompt.strip()}.\n\n" \
                    "Add inline comments to explain each step."
    else:
        optimized = f"{base_prompt.strip()} Please ensure the function is self-contained, well-commented, and uses idiomatic Python."

    explanation = (
        "Cursor prefers complete, natural-language prompts that clarify intent and structure. "
        "We added instructions for full function generation and inline comments to match Cursor's strengths."
    )

    return {
        "optimized_prompt": optimized,
        "explanation": explanation
    }
