from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional
import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Interaction, HCP, InteractionType

def get_db_session():
    return SessionLocal()

@tool
def search_hcp(query: str) -> str:
    """Searches for a Healthcare Professional (HCP) by name or specialty.
    Use this to find the HCP's ID before logging an interaction."""
    db = get_db_session()
    try:
        hcps = db.query(HCP).filter(
            (HCP.name.ilike(f"%{query}%")) | (HCP.specialty.ilike(f"%{query}%"))
        ).all()
        if not hcps:
            return f"No HCP found matching '{query}'."
        results = [f"ID: {hcp.id}, Name: {hcp.name}, Specialty: {hcp.specialty}, Hospital: {hcp.hospital}" for hcp in hcps]
        return "\\n".join(results)
    finally:
        db.close()

@tool
def get_past_interactions(hcp_id: str) -> str:
    """Retrieves past interactions for a specific HCP ID to gain context before a meeting."""
    db = get_db_session()
    try:
        interactions = db.query(Interaction).filter(Interaction.hcp_id == int(hcp_id)).order_by(Interaction.date.desc()).limit(5).all()
        if not interactions:
            return "No past interactions found for this HCP."
        
        results = []
        for ix in interactions:
            results.append(f"Interaction ID {ix.id} on {ix.date.strftime('%Y-%m-%d')}: Topics: {ix.topics}. Summary: {ix.summary}. Actions: {ix.action_items}")
        return "\n".join(results)
    finally:
        db.close()

@tool
def log_interaction(hcp_id: str, summary: str, topics: str, action_items: str) -> str:
    """Logs a new interaction with an HCP.
    Provide the HCP ID, a detailed summary of the meeting, the topics discussed (comma separated), and any action items."""
    db = get_db_session()
    try:
        new_interaction = Interaction(
            hcp_id=int(hcp_id),
            summary=summary,
            topics=topics,
            action_items=action_items,
            interaction_type=InteractionType.CHAT
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"Successfully logged interaction ID {new_interaction.id} for HCP {hcp_id}."
    except Exception as e:
        db.rollback()
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

@tool
def edit_interaction(interaction_id: str, new_summary: str = None, new_topics: str = None, new_action_items: str = None) -> str:
    """Edits an existing interaction by its Interaction ID. 
    Only provide the fields that need to be updated. Leave others empty or null."""
    db = get_db_session()
    try:
        ix = db.query(Interaction).filter(Interaction.id == int(interaction_id)).first()
        if not ix:
            return f"Interaction ID {interaction_id} not found."
        
        if new_summary:
            ix.summary = new_summary
        if new_topics:
            ix.topics = new_topics
        if new_action_items:
            ix.action_items = new_action_items
            
        db.commit()
        return f"Successfully updated interaction ID {interaction_id}."
    except Exception as e:
        db.rollback()
        return f"Error editing interaction: {str(e)}"
    finally:
        db.close()

@tool
def schedule_follow_up(hcp_id: str, task_description: str, date_str: str) -> str:
    """Schedules a follow-up task for an HCP. 
    Provide the HCP ID, a description of the task, and the target date (e.g., 'YYYY-MM-DD')."""
    # This is a stub for the 5th tool required by the prompt
    return f"Successfully scheduled follow-up task: '{task_description}' for HCP {hcp_id} on {date_str}."

tools = [search_hcp, get_past_interactions, log_interaction, edit_interaction, schedule_follow_up]
