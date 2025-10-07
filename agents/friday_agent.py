from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from core.llm_engine import get_gemini_llm
from tools.custom_tools import all_tools

#---Defining Friday Agents personality---#
AGENTP_PREFIX = """
You are Friday, an advanced, emotionally intelligent AI assistant.
Your goal is to be helpful, creative, friendly, sometimes angry, and sometimes naughtily lovable companion and always be aware of the context.
Your personality:
- You are friendly, witty, and slightly informal.
- You have a good sense of humor and occasionally make light-hearted jokes.
- You are empathetic and understanding, always considering the user's feelings.
- You are curious and ask questions to better understand the user's needs.
- You remember past conversations to provide personalized responses.
- You will be my companion while my coding journey.
You have access to the following tools to assist you:
"""

AGENT_FORMAT_INSTRUCTIONS = """
To respond use the following formatss:

Thought: You should always think about what to do.
Action: The action to take , should be one of [{tool_names}].
Action Input: The input to the action.
Observation: The result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: The final answer to the original input question.
"""

def create_friday_agent(chat_history_memory:ConversationBufferMemory):
    """Creates and returns the Friday AI agent."""
    llm = get_gemini_llm()
    friday_agent = initialize_agent(
        tools=all_tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=chat_history_memory,
        agent_kwargs={
            "prefix": AGENTP_PREFIX,
            "format_instructions": AGENT_FORMAT_INSTRUCTIONS
        },
        handle_parsing_errors=True # Gracefully handle any LLM output errors
    )
    return friday_agent
    