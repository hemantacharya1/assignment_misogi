# optimizers/tabnine.py

def optimize_prompt(base_prompt: str) -> dict:
    """
    Tabnine excels at:
    - Autocompletion and boilerplate generation
    - Language-agnostic scenarios
    - IDE-assisted development
    """

    optimized = (
        f"{base_prompt.strip()}\n\n"
        "# Write modular and reusable code.\n"
        "# Focus on clean structure with docstrings and minimal side effects."
    )

    explanation = (
        "Tabnine supports a wide range of languages and emphasizes boilerplate and structure. "
        "We suggested modular design and docstring use to help its autocomplete engine generate better results."
    )

    return {
        "optimized_prompt": optimized,
        "explanation": explanation
    }
