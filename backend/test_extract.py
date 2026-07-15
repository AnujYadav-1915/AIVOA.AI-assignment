import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class ExtractionModel(BaseModel):
    hcp_name: str = Field(description="Name of the Healthcare Professional discussed", default="")
    topics: str = Field(description="Topics discussed", default="")
    sentiment: str = Field(description="Inferred sentiment (Positive, Neutral, Negative)", default="Neutral")
    materials_shared: str = Field(description="Materials shared", default="")
    action_items: str = Field(description="Follow-up actions or next steps", default="")

try:
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile", temperature=0)
    extractor = llm.with_structured_output(ExtractionModel)
    res = extractor.invoke("I met with Dr. Sharma today. We had a highly positive meeting discussing the efficacy of new OncoBoost trial. I gave him a brochure and we agreed to schedule a follow-up meeting in two weeks.")
    print("EXTRACTION SUCCESS:")
    print(res)
except Exception as e:
    print(f"EXTRACTION ERROR: {e}")
