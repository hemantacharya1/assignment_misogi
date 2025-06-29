# optimizers/codewhisperer.py

def optimize_prompt(base_prompt: str) -> dict:
    """
    Amazon CodeWhisperer is focused on:
    - Secure, compliant code generation
    - Cloud (especially AWS) workflows
    - Clear and safe coding instructions
    """

    optimized = (
        f"{base_prompt.strip()}\n\n"
        "# Ensure the code adheres to security best practices.\n"
        "# Use AWS SDK (if applicable) and follow standard error handling."
    )

    explanation = (
        "CodeWhisperer emphasizes security and AWS readiness. "
        "We've added security-conscious wording and encouraged use of SDKs and safe coding practices."
    )

    return {
        "optimized_prompt": optimized,
        "explanation": explanation
    }
