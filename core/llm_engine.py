from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

def get_pro_llm():
    """Initialize and return the Gemini-2.5-pro-LLM."""
    return ChatGoogleGenerativeAI(
        model = "gemini-2.5-pro-latest",
        google_api_key = GOOGLE_API_KEY,
        temperature = 0.75,
        convert_system_message_to_human=True 
        )
def get_flash_llm():
    """Initialize and return the Gemini-2.5-flash-LLM."""
    return ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash-latest",
        google_api_key = GOOGLE_API_KEY,
        temperature = 0.75,
        convert_system_message_to_human=True     
    )
