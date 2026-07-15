from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Interaction, HCP, InteractionType
from agent import get_agent
from langchain_core.messages import HumanMessage
import uvicorn
import datetime
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
    hcp_id: int
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

@app.get("/api/hcps")
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

@app.post("/api/interactions")
def log_interaction_form(req: LogInteractionRequest, db: Session = Depends(get_db)):
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
def chat_with_agent(req: ChatRequest):
    try:
        agent = get_agent()
        config = {"configurable": {"thread_id": req.session_id}}
        
        # Invoke agent
        response = agent.invoke({"messages": [HumanMessage(content=req.message)]}, config)
        
        # The agent response has 'messages' list, the last one is the AI response
        ai_message = response["messages"][-1].content
        return {"response": ai_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
