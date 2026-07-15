import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import tools
from dotenv import load_dotenv

load_dotenv()

# We need the Groq API key to be set in the environment
# The prompt specified using gemma2-9b-it
def get_agent():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY is not set in the environment.")
    
    llm = ChatGroq(
        api_key=groq_api_key,
        model="gemma2-9b-it",
        temperature=0
    )
    
    # create_react_agent wires up the LLM with the tools into a LangGraph state graph
    system_message = "You are a helpful AI assistant for pharmaceutical field representatives. You help manage interactions with Healthcare Professionals (HCPs)."
    agent = create_react_agent(llm, tools, state_modifier=system_message)
    return agent
