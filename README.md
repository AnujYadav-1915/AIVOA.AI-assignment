# AI-First CRM HCP Module

This repository contains the solution for the AI-First CRM HCP Module assignment. It features a "Log Interaction Screen" allowing users to log meetings with Healthcare Professionals (HCPs) through a standard form or a conversational AI interface.

## Tech Stack
*   **Frontend:** React (Vite), Redux Toolkit, CSS (Google Inter Font)
*   **Backend:** Python, FastAPI, SQLAlchemy (SQLite configured by default)
*   **AI Framework:** LangGraph, LangChain
*   **LLM:** Groq (`gemma2-9b-it`)

## Folder Structure
*   `frontend/`: Contains the React + Redux UI.
*   `backend/`: Contains the FastAPI server, LangGraph agent, and database logic.

## Setup Instructions

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the Environment Variables:
   Open the `backend/.env` file and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```
5. Run the FastAPI server:
   ```bash
   python main.py
   ```
   The server will run on `http://localhost:8000`. The SQLite database will be initialized automatically with some dummy HCP data.

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open the provided localhost URL in your browser.

## LangGraph Tools Used
The AI agent uses 5 tools to perform tasks for the field representative:
1.  **Log Interaction:** Captures interaction data and saves it to the database.
2.  **Edit Interaction:** Modifies previously logged interaction data.
3.  **Search HCP:** Look up a Healthcare Professional by name or specialty to get their ID.
4.  **Get Past Interactions:** Retrieves the recent interaction history for a specific HCP.
5.  **Schedule Follow-up:** Schedules a follow-up task based on the meeting notes.

## GitHub Submission
Create a repository with these folders and push it to GitHub to complete Deliverable 1. Ensure you create a 10-15 minute video demonstrating this project running to complete Deliverable 2.
