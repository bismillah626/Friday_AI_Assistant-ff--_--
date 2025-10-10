Friday AI Assistant

**Overview**
 Friday AI– Intelligent Voice Assistant Built an advanced, modular LLM-driven voice assistant designed for
 natural, emotionally aware interaction and contextual reasoning. Utilized LangChain as the core framework
 to integrate multiple modules — enabling conversational chains, task orchestration, and dynamic API routing.
 Implemented multi-layered memory systems including short-term (ConversationBufferMemory) and long-term
 recall using ChromaDB/Pinecone vector databases, enhancing continuity across sessions.
 Integrated Hugging Face Transformers and Gemini API keys for natural language understanding, sentiment
 analysis, summarization, and emotion-aware text generation. Used SentenceTransformers for vector embed
dings to represent and retrieve conversational history semantically. Applied LangChain Prompt Templates for
 adaptive personality-driven interactions (e.g., friendly, professional, or technical tones)



**Tech_Stack**

| Category | Technology |
|-----------|-------------|
| **Core Language** | Python |
| **AI Framework** | LangChain |
| **LLM Provider** | Hugging Face (Transformers) |
| **Vector Database** | FAISS / ChromaDB |
| **Voice Recognition** | SpeechRecognition |
| **Text-to-Speech (TTS)** | pyttsx3 |
| **APIs & Integrations** | Spotify API, Open-Meteo Weather API, Wikipedia API |
| **Environment Management** | python-dotenv |
| **Memory Handling** | LangChain Memory + Vector DB |

---

 **Features
**
 **Voice Activation** – Responds when the wake word **“Friday”** is detected.  
 **Conversational Memory** – Maintains context using vector embeddings for meaningful follow-ups.  
 **Tool-Based Architecture** – Uses modular tools (Spotify, Weather, Wikipedia, etc.) registered with LangChain.  
 **Music Control** – Play, pause, or resume tracks using the **Spotify API**.  
 **Weather Assistant** – Fetches real-time weather data using the **Open-Meteo API**.  
 **Knowledge Search** – Retrieves concise answers from **Wikipedia** using LangChain’s retriever tools.  
 **Joke Generator** – Tells random programming jokes for casual interactions.  
 **Extensible** – Add your own tools or connect more APIs without changing the core logic.  

---

##  Project Architecture

Friday_AI_Assistant/
│
├── core/
│ ├── agent_manager.py # LangChain agent logic and reasoning
│ ├── memory_manager.py # Vector DB + conversational memory
│ ├── voice_engine.py # SpeechRecognition + pyttsx3
│ └── tool_registry.py # Tool setup and registration
│
├── tools/
│ ├── spotify_tool.py
│ ├── weather_tool.py
│ ├── wiki_tool.py
│ └── joke_tool.py
│
├── embeddings/
│ ├── vector_store.faiss
│ └── documents/ # Stored user or knowledge base data
│
├── main.py # Entry point
├── requirements.txt
├── .env.example
└── README.md

