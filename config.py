import os
from dotenv import load_dotenv

load_dotenv()

#API keys 
GOOGLE_API_KEYS = os.getenv("GEMINI_API_KEYS")
HUGGINGFACE_API_KEYS = os.getenv("HUGGINGFACE_API_KEYS")  
  
#spotify client setup
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")  