from textblob import TextBlob

def analyze_sentiment(text):
    """
    Basic sentiment analysis using TextBlob.
    Returns polarity score between -1.0 (negative) and 1.0 (positive).
    """
    if not text:
        return 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def detect_harmful_content(text):
    """
    Simple keyword-based harmful content detection.
    Returns True if harmful content detected, else False.
    """
    harmful_keywords = ['suicide', 'self-harm', 'kill myself', 'end my life', 'harm myself', 'die', 'depressed', 'hopeless']
    text_lower = text.lower()
    for keyword in harmful_keywords:
        if keyword in text_lower:
            return True
    return False
