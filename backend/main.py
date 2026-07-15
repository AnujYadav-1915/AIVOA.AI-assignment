from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Interaction, HCP, InteractionType
from agent import get_agent
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import uvicorn
import datetime
import os
from typing import Optional

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Populate some initial HCP data if empty
def init_db():
    db = next(get_db())
    if db.query(HCP).count() == 0:
        db.add_all([
            HCP(name="Dr. Smith", specialty="Cardiology", hospital="City General"),
            HCP(name="Dr. Sharma", specialty="Neurology", hospital="Metro Health"),
            HCP(name="Dr. Emily Davis", specialty="Oncology", hospital="Cancer Center"),
        ])
        db.commit()

init_db()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class LogInteractionRequest(BaseModel):
    hcp_id: Optional[int] = None
    interaction_type: str = "Meeting"
    date: str
    time: str
    attendees: str
    topics: str
    materials_shared: str
    samples_distributed: str
    sentiment: str
    outcomes: str
    action_items: str

class ExtractionModel(BaseModel):
    hcp_name: Optional[str] = Field(description="Name of the Healthcare Professional discussed", default="")
    interaction_type: Optional[str] = Field(description="Type of interaction (Meeting, Email, Phone)", default="Meeting")
    topics: Optional[str] = Field(description="Topics discussed", default="")
    sentiment: Optional[str] = Field(description="Inferred sentiment (Positive, Neutral, Negative)", default="Neutral")
    materials_shared: Optional[str] = Field(description="Materials shared", default="")
    samples_distributed: Optional[str] = Field(description="Samples distributed", default="")
    outcomes: Optional[str] = Field(description="Key outcomes", default="")
    action_items: Optional[str] = Field(description="Follow-up actions or next steps", default="")

@app.get("/api/hcps")
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

@app.post("/api/interactions")
def log_interaction_form(req: LogInteractionRequest, db: Session = Depends(get_db)):
    if not req.hcp_id:
        raise HTTPException(status_code=400, detail="HCP ID is required")
        
    hcp = db.query(HCP).filter(HCP.id == req.hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
        
    date_obj = datetime.datetime.strptime(req.date, "%Y-%m-%d").date() if req.date else datetime.date.today()
    time_obj = datetime.datetime.strptime(req.time, "%H:%M").time() if req.time else datetime.datetime.now().time()
    
    new_interaction = Interaction(
        hcp_id=req.hcp_id,
        interaction_type=req.interaction_type,
        date=date_obj,
        time=time_obj,
        attendees=req.attendees,
        topics=req.topics,
        materials_shared=req.materials_shared,
        samples_distributed=req.samples_distributed,
        sentiment=req.sentiment,
        outcomes=req.outcomes,
        action_items=req.action_items,
        summary=""
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return {"message": "Interaction logged successfully", "interaction_id": new_interaction.id}

@app.post("/api/chat")
def chat_with_agent(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        form_data = {}
        
        # 1. Extraction Pipeline to populate form
        if groq_api_key and groq_api_key != "your_groq_api_key_here":
            try:
                llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant", temperature=0)
                extractor = llm.with_structured_output(ExtractionModel)
                prompt = f"Extract the following information from the user's message. If not mentioned, leave empty.\n\nMessage: {req.message}"
                extraction_res = extractor.invoke(prompt)
                
                if extraction_res:
                    form_data = extraction_res.dict()
                    # Map HCP Name to ID if possible
                    if form_data.get("hcp_name"):
                        # Basic matching
                        search_name = form_data["hcp_name"].split(" ")[-1] # match last name
                        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{search_name}%")).first()
                        if hcp:
                            form_data["hcp_id"] = hcp.id
            except Exception as ex:
                print(f"Extraction error: {ex}")
                pass
        
        # 2. Agent Workflow
        from langchain_core.messages import SystemMessage
        agent = get_agent()
        config = {"configurable": {"thread_id": req.session_id}}
        
        sys_msg = SystemMessage(content="You are an AI assistant for a CRM. If the user provides details about an interaction, you MUST use the log_interaction tool immediately. Do not ask for permission. CRITICAL: DO NOT nest tool calls. If you need an ID, call search_hcp first, wait for the response, and then call log_interaction.")
        
        response = agent.invoke({"messages": [sys_msg, HumanMessage(content=req.message)]}, config)
        ai_message = response["messages"][-1].content
        
        return {"response": ai_message, "form_data": form_data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
