from transformers import pipeline

# Define the intent labels
INTENT_LABELS = [
    "tech_support",
    "billing",
    "feature_requests"
]

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_intent(text: str):
    result = classifier(text, INTENT_LABELS)
    # result["labels"] is a ranked list, best match is first
    top_label = result["labels"][0]
    confidence = result["scores"][0]
    return top_label, confidence
