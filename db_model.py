# db_model.py

from mongoengine import Document, StringField, connect
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Attempt to connect using a URI from .env, or fall back to local default
MONGODB_URI = os.getenv("MONGODB_URI", 'calmind_db')

try:
    if MONGODB_URI.startswith('mongodb://') or MONGODB_URI.startswith('mongodb+srv://'):
        # For a full connection string
        connect(host=MONGODB_URI)
    else:
        # For a simple database name (assumes local host/port)
        connect(MONGODB_URI)
except Exception as e:
    print(f"MongoDB connection error: {e}")
    # Connection failure is not critical for running the Flask app, but logging will fail.

class MoodLog(Document):
    """
    Defines the MongoDB document structure for storing each user interaction.
    """
    text = StringField(required=True)
    emotion = StringField(required=True)
    timestamp = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    meta = {
        'collection': 'mood_logs'
    }
    