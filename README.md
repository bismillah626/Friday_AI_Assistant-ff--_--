Friday AI Assistant
A modular and intelligent voice assistant powered by Python, LangChain, and Google's Gemini Pro. "Friday" evolves from a simple command-based script into a conversational agent capable of using tools to interact with real-world APIs.

About The Project
This project began as a simple Python script for a voice assistant that could handle a few hard-coded commands. It has been refactored into a sophisticated AI agent using the LangChain framework.

Instead of relying on if/elif statements, Friday now uses a Large Language Model (Google's Gemini Pro) as its reasoning engine. The LLM decides which "tool" (like getting the weather or playing a song) is best suited to fulfill a user's request, making the assistant far more flexible, conversational, and easy to extend.

Features
Voice-Activated: Listens for the wake word "Friday" before accepting commands.

Conversational Memory: Remembers the context of the current conversation to answer follow-up questions.

Tool-Based Architecture: Uses a set of tools to perform actions:

🎵 Spotify Control: Play songs and pause music.

🌦️ Real-time Weather: Fetches the current weather for your location.

🧠 Wikipedia Search: Answers general knowledge questions.

😄 Joke Generator: Tells a random programming joke.

Extensible: Easily add new tools or a personalized knowledge base.

Powered by Gemini: Uses Google's gemini-pro model for advanced reasoning and natural language understanding.

Tech Stack
Core: Python

AI Framework: LangChain

LLM: Google Gemini Pro

Voice Recognition: SpeechRecognition

Text-to-Speech: pyttsx3

APIs & Services:

Spotify API (via spotipy)

Open-Meteo Weather API

Wikipedia API
