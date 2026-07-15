from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class InteractionType(str, enum.Enum):
    MEETING = "Meeting"
    EMAIL = "Email"
    PHONE = "Phone"
    CHAT = "Chat"

class HCP(Base):
    __tablename__ = "hcps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)
    hospital = Column(String)
    
    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    date = Column(Date, default=datetime.date.today)
    time = Column(Time, default=datetime.datetime.now().time())
    attendees = Column(String)
    interaction_type = Column(String, default="Meeting")
    topics = Column(Text) 
    summary = Column(Text) # from previous implementation
    materials_shared = Column(Text)
    samples_distributed = Column(Text)
    sentiment = Column(String) # Positive, Neutral, Negative
    outcomes = Column(Text)
    action_items = Column(Text) # follow_up_actions
    
    hcp = relationship("HCP", back_populates="interactions")
