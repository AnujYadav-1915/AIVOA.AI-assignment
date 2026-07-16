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
    
    # Use the stable 70b model. Mixtral is decommissioned, 8b enters recursion loops.
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    
    # create_react_agent wires up the LLM with the tools into a LangGraph state graph
    agent = create_react_agent(llm, tools)
    return agent
