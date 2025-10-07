from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

def get_gemini_llm():
    """Initialize and return the Gemini LLM."""
    return ChatGoogleGenerativeAI(
        model = "gemini-pro",
        google_api_key = GOOGLE_API_KEY,
        temperature = 0.75,
        convert_system_message_to_human=True 
        )
