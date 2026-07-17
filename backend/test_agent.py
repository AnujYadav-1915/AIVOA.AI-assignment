import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import get_agent
from langchain_core.messages import SystemMessage, HumanMessage

agent = get_agent()
sys_msg = SystemMessage(content="You are an AI assistant for a CRM. If the user provides details about an interaction, you MUST use the log_interaction tool immediately. Do not ask for permission. CRITICAL: DO NOT nest tool calls. If you need an ID, call search_hcp first, wait for the response, and then call log_interaction.")

message = "I met with Dr. Sharma today. We had a highly positive meeting discussing the efficacy of new OncoBoost trial. I gave him a brochure and we agreed to schedule a follow-up meeting in two weeks."

config = {"configurable": {"thread_id": "test12345"}}

print("Invoking agent...")
try:
    response = agent.invoke({"messages": [sys_msg, HumanMessage(content=message)]}, config)
    print("Agent Response:", response["messages"][-1].content)
except Exception as e:
    import traceback
    traceback.print_exc()
