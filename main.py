import speech_recognition as sr
import pyttsx3
from agents.friday_agent import create_friday_agent
from memory.memory_manager import MemoryManager
from core.llm_engine import get_flash_llm, get_pro_llm 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Wake Word and Other Constants ---
WAKE_WORD = "friday"

# --- Initialize Speech Engine ---
from agents.friday_agent import create_friday_agent
from memory.memory_manager import MemoryManager
from core.llm_engine import get_flash_llm, get_pro_llm 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Wake Word and Other Constants ---
WAKE_WORD = "friday"

# --- Initialize Speech Engine ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # Set a female voice


def speak(text: str):
    """Converts text to speech."""
    print(f"Friday: {text}")
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    """Listens for a user's command *after* the wake word is detected."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for your command...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing command...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query.lower()
    except Exception:
        return ""

def select_model(user_input: str, llm) -> str:
    """Uses a fast LLM to decide if a query requires a powerful model."""
    prompt_template = """
    You are a decision-making AI that routes user queries to the correct model.
    Based on the user's query, decide if a standard, fast model is sufficient or if a more powerful, in-depth model is required.

    - Queries asking for simple facts, jokes, opening websites, playing music, or weather should use the 'standard' model.
    - Queries that use phrases like 'explain in detail', 'comprehensive analysis', 'break it down for me', 'in depth', or ask complex, multi-step reasoning questions should use the 'powerful' model.

    User Query: "{query}"

    Respond with only the single word: 'standard' or 'powerful'.
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["query"])
    router_chain = LLMChain(llm=llm, prompt=prompt)
    
    response = router_chain.invoke({"query": user_input})
    decision = response['text'].strip().lower()
    
    if "powerful" in decision:
        return "powerful"
    return "standard"

# --- Main Interaction Loop ---
if __name__ == "__main__":
    memory_manager = MemoryManager()
    
    print("Initializing LLM models...")
    flash_llm = get_flash_llm()
    pro_llm = get_pro_llm()

    print("Creating agent instances...")
    flash_agent = create_friday_agent(flash_llm, memory_manager.conversational_memory)
    pro_agent = create_friday_agent(pro_llm, memory_manager.conversational_memory)

    speak("Initializing Friday AI. Say my name to activate.")
    
    mode = input("Choose mode: 'v' for voice or 't' for text: ").strip().lower()

    while True:
        user_input = ""
        
        if mode == 'v':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print(f"\nListening silently for '{WAKE_WORD}'...")
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                try:
                    audio = r.listen(source, phrase_time_limit=2)
                    heard_phrase = r.recognize_google(audio).lower()

                    if WAKE_WORD in heard_phrase:
                        speak("I'm here.")
                        user_input = listen()
                    else:
                        continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Error during wake word detection: {e}")
                    continue
        else:
            user_input = input("You: ").strip().lower()

        if "exit" in user_input or "quit" in user_input:
            speak("Goodbye! Shutting down.")
            break
            
        if user_input:
            chosen_model = select_model(user_input, flash_llm)

            if chosen_model == "powerful":
                print("[System] Powerful model selected by router.")
                speak("Okay, this requires a more detailed answer.")
                active_agent = pro_agent
            else:
                print("[System] Standard model selected by router.")
                active_agent = flash_agent

            retriever = memory_manager.get_vector_retriever()
            retrieved_docs = retriever.invoke(user_input)
            retrieved_context = "\n".join([doc.page_content for doc in retrieved_docs])
            
            agent_input = (
                f"Relevant context from past conversations:\n"
                f"{retrieved_context}\n\n"
                f"User's current query: {user_input}"
            )
            
            response = active_agent.invoke({"input": agent_input})
            speak(response['output'])
            memory_manager.save_interaction(user_input, response['output'])