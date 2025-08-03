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
    engine.say (text)
    engine.runAndWait()
#Setting the wake_word
Wake_word ="Friday"
#Seting Chatbot for generating falback Response
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

load_dotenv() 

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

#Joke generating function 
def Genertae_Random_Jokes():
    speak("Generating a random joke for you...")
    joke = pyjokes.get_joke()
    speak(joke)
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
def play_song_spotify(song_name ):
    try:
        results = sp.search(q=song_name, limit=1, type='track')
        if results['tracks']['items']:
            uri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[uri])
            speak(f"Playing {song_name} on Spotify.")
        else:
            speak("Couldn't find the song on Spotify.")
    except Exception as e:
        speak("There was a problem connecting to Spotify.")
        print(f"[Spotify Error] {e}")
 
def processCommand(command):
    command = command.lower()
#Now we can open any preinstalled app on desktop
    if "open" in command:
        item = command.replace("open", "").strip().lower()
        if os.path.exists(item):
            os.startfile(item)
            speak(f"Opening {item}")
        else:
            path = find_app_path(item)
        if path:
            os.startfile(path)
            speak(f"Launching {item}")
        else:
            speak(f"I couldn’t find {item} on your system. Let me search it online.")
            search_url = f"https://www.google.com/search?q=download+{item}"
            webbrowser.open(search_url)


    elif "what's the weather" in command or "weather today" in command:
        get_weather()
    elif "tell me joke" in  command:
        Genertae_Random_Jokes()
    elif "tell me about" in command or "what is" in command:
        topic = command.replace("tell me about", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=False)
            speak(summary)
        except Exception as e:
            print(f"[Wikipedia Error] {e}")
            prompt = f"Tell me about {topic}"
            response = chatbot(prompt, max_length=100, do_sample=True, truncation=True)
            speak(response[0]['generated_text'])
    elif "play" in command:
        song = command.replace("play", "").strip()    
        play_song_spotify(song)
    elif "pause" in command:
        try:
            sp.pause_playback()
            speak("Paused the music.")
        except Exception as e:
            speak("I couldn't pause it because no device is playing.")
            print(f"[Spotify Pause Error] {e}")      
    elif "nice work friday" in command:
        speak("Thank u boss")
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        response = chatbot(command, max_length=100, do_sample=True, truncation=True)
        reply = response[0]['generated_text']
        speak(reply)


if __name__ == "__main__":
    speak("Initializing the Friday AI Assistant...")
    mode = input("Enter mode 'v' for voice or 't' for text mode")
    if mode == 't':
        while True:
            command = input("You: ").strip().lower()
            if command:
                processCommand(command)
        #voice mode            
    elif mode == 'v':
        speak("Voice mode activated. Please say the wake word to start.")
        while True:
            # obtain audio from the microphone
            r = sr.Recognizer()
            print("Recognizing....")    

            # recognize speech using google
            try:
                #listening for the wake word friday
                with sr.Microphone() as source:
                    print("Listening....")
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                    word = r.recognize_google(audio)
                    if(word.lower() == Wake_word.lower()):
                        speak("yeah i am here")
                #listen for the command
                with sr.Microphone() as source:
                    speak("Friday is active....")
                    audio = r.listen(source, timeout=5, phrase_time_limit=4)
                    command = r.recognize_google(audio)
                    processCommand(command)
                    
            except Exception as e:
                print("Error; {0}".format(e))