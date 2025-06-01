from transformers import pipeline

# Load the model once when the module is imported
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_crime_related(text, threshold=0.75):
    """
    Check if the text is related to crime or terrorism using zero-shot classification.

    Parameters:
    - text (str): The text to classify.
    - threshold (float): Minimum confidence required to be considered 'crime related'.

    Returns:
    - bool: True if related to crime or terrorism, False otherwise.
    """
    labels = ["crime", "terrorism", "sports", "entertainment", "politics"]
    try:
        result = classifier(text, labels)
        top_label = result['labels'][0]
        score = result['scores'][0]
        return top_label in ["crime", "terrorism"] and score >= threshold
    except Exception as e:
        print(f"[Classifier Error] {e}")
        return False
