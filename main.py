import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import wikipedia
import spotipy
import requests
from transformers import pipeline
from spotipy.oauth2 import SpotifyOAuth
import pyjokes
from dotenv import load_dotenv
import json
import google.generativeai as genai
import re
from colorama import init, Fore, Style

#Setting the mode to switch between voice and text

mode = "voice"


recogniser = sr.Recognizer()
engine = pyttsx3.init()
# Get available voices
voices = engine.getProperty('voices')

# Print all available voices
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} - {voice.gender} - {voice.id}")

# Set the voice to female (usually index 1 on Windows)
engine.setProperty('voice', voices[1].id)  
def speak(text):
    if(mode == "voice"):
        engine.say (text)
        engine.runAndWait()
#Setting the wake_word
Wake_word ="Friday"
#Seting Chatbot for generating falback Response
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

load_dotenv() 
# ---Implementing gemini API keys on friday---
genai.configure(api_key=os.getenv("GEMINI_API_KEYS"))

# --> function to ask gemini as a genie who will obey your orders
def ask_gemini(prompt, mode="flash"):
    try:
        model_name = "gemini-2.5-flash" if mode == "flash" else "gemini-2.5-pro"
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # Extract text safely
        if hasattr(response, "candidates") and response.candidates:
            parts = []
            for cand in response.candidates:
                if hasattr(cand, "content") and hasattr(cand.content, "parts"):
                    for part in cand.content.parts:
                        if hasattr(part, "text"):
                            parts.append(part.text)
            return "\n".join(parts).strip() if parts else "No text returned by Gemini."
        
        return "No candidates returned by Gemini."

    except Exception as e:
        return f"Error communicating with Gemini: {e}"
    
# Initialize colorama for Windows too
init(autoreset=True)


def friday_brain(user_input):
    user_input_lower = user_input.lower()
    #redirecting to use pro if codeing related problem is asked
    if re.search(r'\b(code|programming|python|javascript|java|c\+\+|c#|debug|function|class|algorithm|dsa|program|codeforces|codechef|leetcode)\b', user_input_lower):
        return ask_gemini(user_input, mode="pro")
    else:
        return ask_gemini(user_input, mode="flash")
#implementing gemini so that it can print code in terminal
    
def process_user_input(user_input):
    response = friday_brain(user_input)

    if not response:
        print(Fore.RED + "⚠️ No response from Gemini.")
        return

    # Split into text/code blocks
    parts = re.split(r"```(?:\w*\n)?(.*?)```", response, flags=re.DOTALL)

    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue

        if i % 2 == 1:  # Code block
            print(Fore.CYAN + "\n💻 Generated Code:\n" + Style.RESET_ALL)
            print(Fore.GREEN + part + Style.RESET_ALL)
        else:  # Text block
            print(Fore.YELLOW + "\n📝 Response:\n" + Style.RESET_ALL)
            print(Fore.WHITE + part + Style.RESET_ALL)
            
# === Spotify Client Setup ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))
# Ensure the Spotify client is authenticated
# === Get Location Dynamically ===
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
def get_weather():
    try:
        lat, lon = get_location_by_ip()
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            speak("Weather service is currently unreachable.")
            print(f"[Weather Error] HTTP {response.status_code}")
            return

        data = response.json()
        if "current_weather" in data:
            temp = data["current_weather"].get("temperature")
            wind = data["current_weather"].get("windspeed")
            speak(f"Current temperature is {temp} degrees Celsius with a wind speed of {wind} km/h.")
        else:
            speak("Couldn't retrieve current weather data.")
            print("[Weather Error] Unexpected JSON format:", data)

    except Exception as e:
        speak("Sorry, I couldn't fetch the weather.")
        print(f"[Weather Exception] {e}")


# Function to search Wikipedia and speak the summary
def search_wikipedia(query):
    pass
# Function to find the path of an application
import subprocess
def find_app_path(app_name):
    try:
        result = subprocess.check_output(f'where {app_name}', shell=True, universal_newlines=True)
        return result.strip().split('\n')[0]
    except subprocess.CalledProcessError:
        return None
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
            speak(f"Playing {best_match['name']} by {best_match['artists'][0]['name']} on Spotify.")
        else:
            speak("Couldn't find the song on Spotify.")
    except Exception as e:
        speak("There was a problem connecting to Spotify.")
        print(f"[Spotify Error] {e}")

 
def processCommand(command):
    global mode
    command = command.lower()
     # Mode switching
    if "switch to text mode" in command:
        mode = "text"
        speak("Switching to text mode. I will no longer speak out loud.")
        return "TEXT_MODE"
    elif "switch to voice mode" in command:
        mode = "voice"
        speak("Switching to voice mode. I will now speak responses.")
        return "VOICE_MODE"
    reply = None
#Now we can open any preinstalled app on desktop
    if "open" in command:
        item = command.replace("open", "").strip().lower()
        if os.path.exists(item):
            os.startfile(item)
            speak(f"Opening {item}")
            return
        else:
            path = find_app_path(item)
        if path:
            os.startfile(path)
            speak(f"Launching {item}")
            return 
        else:
            speak(f"I couldn’t find {item} on your system. Let me search it online.")
            search_url = f"https://www.google.com/search?q=download+{item}"
            webbrowser.open(search_url)
            return 

#COMMANDS BEGIN HERE
    elif "what's the weather" in command or "weather today" in command:
        get_weather()
        return 

    elif "play" in command:
        song = command.replace("play", "").strip()    
        play_song_spotify(song)
        return
    elif "pause" in command:
        try:
            sp.pause_playback()
            speak("Paused the music.")
        except Exception as e:
            speak("I couldn't pause it because no device is playing.")
            print(f"[Spotify Pause Error] {e}")  
            return     
    elif "nice work friday" in command:
        speak("Thank u boss")
        return
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        reply = None
        try:
        # Try Gemini first
            reply = friday_brain(command)  # Uses Gemini API
            print(f" {reply}")
            if not reply or reply.strip() == "":
                raise Exception("Empty Gemini response")

        except Exception as e:
            print(f"[ Error] {e}, falling back to DialoGPT...")
            # Fall back to DialoGPT if Gemini fails
            try:
                response = chatbot(command, max_length=100, do_sample=True, truncation=True)
                reply = response[0]['generated_text']
            except Exception as e2:
                print(f"[DialoGPT Error] {e2}")
                reply = "Sorry, I couldn't process your request right now."

    speak(reply)
    #print(reply)


if __name__ == "__main__":
    speak("Initializing the Friday AI Assistant...")
    Wake_word = "Friday"
    recognizer = sr.Recognizer()
    command = ""
    mode = input("Enter mode 'v' for voice or 't' for text mode :\n").strip().lower()
    
    while True:
         # TEXT MODE
        if mode == 't':  # TEXT MODE
            command = input("Commands: ").strip().lower()
            if command:
                mode_signal=processCommand(command)
            if mode_signal == "VOICE_MODE":
                mode = 'v'
                speak("Switched to voice mode.")
        # VOICE MODE
        elif mode == 'v':
            try:
                with sr.Microphone() as source:
                    # Adjust for ambient noise once to improve recognition
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("\nListening for wake word 'Friday'...")
                    
                    # 1. Listen for the wake word
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
                    heard_text = recognizer.recognize_google(audio).lower()

                    # 2. If wake word is detected, proceed to listen for the command
                    if Wake_word.lower() in heard_text:
                        speak("Yes?")
                        print("Wake word detected. Listening for command...")
                        
                        # 3. Listen for the actyal command
                        audio_command = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio_command).lower()
                        print(f"You: {command}")

                        # 4. process the comand EXACTLY ONCE
                        # This is the single, correct place to process a voice command
                        mode_signal = processCommand(command)
                        
                        # 5. Check if the commsnd was to switch modes
                        if mode_signal == "TEXT_MODE":
                            mode = 't'
                            speak("Switched to text mode.")

            except sr.WaitTimeoutError:
                # This is not an error. It just means the user didn't speak
                # 'pass' tells the loop to simply continue and listen again
                pass
            except sr.UnknownValueError:
                # This means speech was heard but couldn't be understood
                # Also not a critical error, so we just listen again
                pass
            except Exception as e:
                # For any other unexpected errors, print it and continue
                print(f"[ERROR in voice loop]: {e}")

