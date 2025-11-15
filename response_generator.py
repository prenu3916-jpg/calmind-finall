# response_generator.py
# This file is not actively used in the Gemini-integrated version (app.py handles response)
# It is kept here for project structure consistency or as a simple fallback.

def generate_simple_response(emotion):
    """Provides simple, rule-based responses."""
    if emotion == "positive":
        return "That's wonderful! I'm glad you're feeling so positive."
    elif emotion == "negative":
        return "I hear you, and it's okay to feel down. Remember to take a moment for yourself."
    else: # neutral or unknown
        return "Thank you for sharing your thoughts. I'm here to listen anytime."