# emotion_analysis.py

from textblob import TextBlob

def analyze_emotion(text):
    """
    Analyzes the sentiment of the text using TextBlob.
    Returns: "positive", "negative", or "neutral".
    """
    if not text:
        return "neutral"
        
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    POSITIVE_THRESHOLD = 0.2
    NEGATIVE_THRESHOLD = -0.2
    
    if polarity > POSITIVE_THRESHOLD:
        return "positive"
    elif polarity < NEGATIVE_THRESHOLD:
        return "negative"
    else:
        return "neutral"