import webbrowser
import requests
import os
import pyjokes
import wikipedia
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langchain.tools import Tool
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import subprocess
# === Spotify Client Setup ===
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
    ))
except Exception as e:
    print(f"[Spotify Auth Error] Please check your credentials. {e}")
    sp = None
def get_location_by_ip():
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        loc = ip_info["loc"].split(",")
        latitude = float(loc[0])
        longitude = float(loc[1])
        return latitude, longitude
    except Exception as e:
        print(f"[Location Error] {e}")
        return 28.61, 77.20  # fallback to Delhi
#Defining the weather function
def get_weather(location: str = "auto")-> str:
    """Useful for when you need to get the current weather. The location is inferred automatically if not provided."""
    try:
        # Using geocoding to find lat/lon for the location string
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = requests.get(geo_url).json()
        if not geo_response.get('results'):
            return f"Could not find location: {location}"

        loc_data = geo_response['results'][0]
        lat, lon = loc_data['latitude'], loc_data['longitude']
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(weather_url, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes
        
        data = response.json().get("current_weather", {})
        temp = data.get("temperature")
        wind = data.get("windspeed")

        return f"Current temperature in {loc_data['name']} is {temp}°C with a wind speed of {wind} km/h."
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather. Error: {e}"
# Function to find the path of an application
def find_app_path(app_name):
    try:
        result = subprocess.check_output(f'where {app_name}', shell=True, universal_newlines=True)
        return result.strip().split('\n')[0]
    except subprocess.CalledProcessError:
        return None
#Find app using the path genetrtaed from the above function
def open_app(item):
   item = item.strip().lower()
   if os.path.exists(item):
       os.startfile(item)
       return f"Opening {item}..."
   else:
       path = find_app_path(item)
       if path:
           os.startfile(path)
           return f"Opening {item} from {path}..."
       else:
           return f"Could not find the application: {item}"
#A function for playing song on spotify
def play_song_spotify(song_name):
    try:
        # Force Spotify to treat the search as a track search
        query = f'track:"{song_name}"'
        results = sp.search(q=query, limit=5, type='track')

        if results['tracks']['items']:
            # Find the best match by checking name similarity
            from difflib import SequenceMatcher

            best_match = max(
                results['tracks']['items'],
                key=lambda track: SequenceMatcher(None, song_name.lower(), track['name'].lower()).ratio()
            )

            uri = best_match['uri']
            sp.start_playback(uris=[uri])   
    except Exception as e:
        print(f"[Spotify Error] {e}")

def pause_spotify(query: str = "") -> str:
    """Useful for pausing the current music on Spotify."""
    if not sp:
        return "Spotify is not connected."
    try:
        sp.pause_playback()
        return "Music paused on Spotify."
    except Exception as e:
        return f"Could not pause Spotify. Maybe nothing is playing? Error: {e}"

def open_website(url: str) -> str:
    """Opens a given URL in the web browser."""
    if not url.startswith("http"):
        url = f"https://{url}"
    webbrowser.open(url)
    return f"Opening {url}..."


#------Wrapping langchain around these functions to make them tools-------#
weather_tool =Tool(
    name = "Weather",
    func = get_weather, 
    description = "Useful for when you need to get the current weather. The location is inferred automatically if not provided."
)
spotify_play_tool = Tool(
    name = "SpotifyPlayer",
    func = play_song_spotify,
    description="Useful for playing a song on Spotify. Input should be the name of the song."
)
spotify_pause_tool = Tool(
    name = "SpotifyPauser",
    func = pause_spotify,
    description="Useful for pausing the current music on Spotify. No input is required."
)
website_open_tool = Tool(
    name = "WebsiteOpener",
    func = open_website,
    description="Useful for opening a website. Input should be the URL of the website."
)
app_finder_tool = Tool(
    name = "AppFinder",
    func = find_app_path,
    description="Useful for finding the installation path of an application on Windows. Input should be the name of the application executable, e.g., 'notepad.exe'."
)
app_opening_tool =Tool(
    name = "AppOpener",
    func = open_app,
    description="Useful for opening an application on Windows. Input should be the name of the application executable, e.g., 'notepad.exe'."
)
#LIST of all tools that the agent can use
all_tools = [
    weather_tool,
    app_finder_tool,
    app_opening_tool,
    spotify_play_tool,
    spotify_pause_tool, 
    website_open_tool,  
]