# app.py
import os
import pandas as pd
import json
from flask import Flask, request, jsonify, render_template
from google import genai
from datetime import datetime
from dotenv import load_dotenv

# Import your custom modules
# We keep these modular for clean organization, though the functions are simple
from emotion_analysis import analyze_emotion
from db_model import MoodLog 

# Load environment variables from .env file
load_dotenv()

# --- INITIALIZATION ---
app = Flask(__name__)

# Configure Gemini API
# The client will automatically pick up the GEMINI_API_KEY environment variable.
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

# --- CSV LOGGING FUNCTION ---

def log_to_csv(text, emotion):
    """Saves user input and emotion to the mood_logs.csv file."""
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)
    
    file_path = "data/mood_logs.csv"
    
    # Check if the file needs a header (i.e., if it does not exist)
    file_exists = os.path.exists(file_path)
    
    # Create a DataFrame for the current log entry
    log_df = pd.DataFrame([[text, emotion, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], 
                          columns=["Text", "Emotion", "Timestamp"])
                          
    # Append the log to the CSV file
    log_df.to_csv(
        file_path, 
        mode='a', 
        header=not file_exists, # Write header only if the file is new
        index=False
    )

# --- GEMINI RESPONSE GENERATION ---

def generate_calmind_response(emotion, user_text):
    """Generates a contextual, calming response using Gemini."""
    if client is None:
        return "The AI service is unavailable due to a missing or invalid API key."

    # System prompt guides the AI's persona and goal
    system_prompt = (
        "You are 'Calmind', a supportive and empathetic AI assistant. "
        "Your goal is to provide a brief, calming, and constructive response. "
        "The user's emotional state is detected as: {}. Use this context to reply.".format(emotion)
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"Sorry, the AI service encountered an error while generating a reply."


# --- FLASK ROUTES (API ENDPOINTS) ---

@app.route('/')
def index():
    """Route to serve the main HTML page from the templates folder."""
    return render_template('index.html')

@app.route('/api/calmind', methods=['POST'])
def calmind_chat():
    """Main API endpoint for the frontend to send user input."""
    data = request.get_json()
    user_text = data.get('text', '')

    if not user_text:
        return jsonify({"response": "Please provide some text input."}), 400

    # 1. Analyze Emotion
    emotion = analyze_emotion(user_text)

    # 2. Generate Response using Gemini
    ai_reply = generate_calmind_response(emotion, user_text)

    # 3. Save Logs (MongoDB and CSV)
    log_to_csv(user_text, emotion)
    
    try:
        # Save to MongoDB
        MoodLog(text=user_text, emotion=emotion).save()
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        # Note: In a production app, you'd handle this error better.

    # 4. Return response to the frontend
    return jsonify({
        "response": ai_reply,
        "emotion": emotion,
        "raw_text": user_text
    })

if __name__ == '__main__':
    # You will need to start your local MongoDB service before running this.
    app.run(debug=True, port=5001)
    