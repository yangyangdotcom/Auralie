#!/usr/bin/env python3
"""
Auralie FastAPI Backend
REST API for the mobile app
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from profile import UserProfile
from simulator import DatingSimulation
from user_chat import UserTwinChat
from output_formatter import OutputFormatter

app = FastAPI(
    title="Auralie API",
    description="AI-powered dating simulator API",
    version="1.0.0"
)

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for running simulations in background
executor = ThreadPoolExecutor(max_workers=3)

# In-memory storage for simulation status (in production, use a database)
simulation_status: Dict[str, Dict] = {}

# In-memory storage for active chats
active_chats: Dict[str, UserTwinChat] = {}

# API Models
class SimulationRequest(BaseModel):
    profile1_id: str
    profile2_id: str

class SimulationStatus(BaseModel):
    simulation_id: str
    status: str  # "pending", "running", "completed", "failed"
    profile1_id: str
    profile2_id: str
    profile1: str  # Display name
    profile2: str  # Display name
    compatibility_score: Optional[float] = None
    completed_days: int = 0
    created_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None

class SimulationResponse(BaseModel):
    simulation_id: str
    status: str
    message: str

class ChatStartRequest(BaseModel):
    profile_id: str
    user_name: Optional[str] = "You"

class ChatMessageRequest(BaseModel):
    message: str
    context: Optional[str] = "texting"

class ChatMessageResponse(BaseModel):
    message: str
    emotion: str
    internal_thought: str
    fondness_change: int
    fondness_level: int

# Helper functions
def get_profile_id_from_name(name: str) -> str:
    """Convert profile name to ID format"""
    return name.lower().replace(' ', '_')

def load_profile_by_id(profile_id: str) -> UserProfile:
    """Load a profile by ID"""
    profiles_dir = "profiles"
    filepath = os.path.join(profiles_dir, f"{profile_id}.json")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")

    return UserProfile.load(filepath)

def run_simulation_sync(profile1: UserProfile, profile2: UserProfile, simulation_id: str):
    """Run simulation synchronously (called in background thread)"""
    try:
        simulation_status[simulation_id]["status"] = "running"

        simulation = DatingSimulation(profile1, profile2)
        result = simulation.run_simulation()

        # Save formatted output
        output_dir = "src/output"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"{output_dir}/{simulation.simulation_id}.json"

        # Save as JSON for API access
        with open(output_filename, 'w') as f:
            json.dump(result, f, indent=2)

        # Also save formatted text output
        text_output = f"{output_dir}/{simulation.simulation_id}.txt"
        OutputFormatter.save_formatted_output(result, text_output)

        simulation_status[simulation_id]["status"] = "completed"
        simulation_status[simulation_id]["completed_at"] = datetime.now().isoformat()
        simulation_status[simulation_id]["compatibility_score"] = result.get("compatibility", {}).get("score", None)
        simulation_status[simulation_id]["completed_days"] = result.get("completed_days", 0)
        simulation_status[simulation_id]["result"] = result

    except Exception as e:
        simulation_status[simulation_id]["status"] = "failed"
        simulation_status[simulation_id]["error"] = str(e)
        simulation_status[simulation_id]["completed_at"] = datetime.now().isoformat()

# API Endpoints
@app.get("/")
def root():
    """Health check endpoint"""
    return {"message": "Auralie API", "version": "1.0.0", "status": "running"}

@app.get("/api/profiles")
def list_profiles():
    """Get all available profiles"""
    try:
        profiles = UserProfile.load_all("profiles")
        # Add id field to each profile (derived from name)
        return [
            {
                "id": get_profile_id_from_name(profile.name),
                **profile.model_dump()
            }
            for profile in profiles
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading profiles: {str(e)}")

@app.get("/api/profiles/{profile_id}", response_model=UserProfile)
def get_profile(profile_id: str):
    """Get a specific profile by ID"""
    return load_profile_by_id(profile_id)

@app.post("/api/profiles", response_model=UserProfile)
def create_profile(profile: UserProfile):
    """Create a new profile"""
    try:
        profile.save("profiles")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving profile: {str(e)}")

@app.post("/api/simulations", response_model=SimulationResponse)
async def create_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """Start a new simulation"""
    try:
        # Load profiles
        profile1 = load_profile_by_id(request.profile1_id)
        profile2 = load_profile_by_id(request.profile2_id)

        # Create simulation ID
        simulation_id = f"{request.profile1_id}_{request.profile2_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize status
        simulation_status[simulation_id] = {
            "simulation_id": simulation_id,
            "status": "pending",
            "profile1_id": request.profile1_id,
            "profile2_id": request.profile2_id,
            "profile1": profile1.name,
            "profile2": profile2.name,
            "compatibility_score": None,
            "completed_days": 0,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "error": None
        }

        # Run simulation in background
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, run_simulation_sync, profile1, profile2, simulation_id)

        return SimulationResponse(
            simulation_id=simulation_id,
            status="pending",
            message="Simulation started. Use GET /api/simulations/{simulation_id} to check status."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting simulation: {str(e)}")

@app.get("/api/simulations", response_model=List[SimulationStatus])
def list_simulations():
    """Get all simulations"""
    simulations = []

    # Add in-memory simulations
    for status in simulation_status.values():
        simulations.append(SimulationStatus(**status))

    # Add simulations from disk that aren't in memory
    if os.path.exists("simulations"):
        for filename in os.listdir("simulations"):
            if filename.endswith(".json"):
                sim_id = filename[:-5]  # Remove .json extension

                # Skip if already in memory
                if sim_id in simulation_status:
                    continue

                try:
                    with open(os.path.join("simulations", filename), 'r') as f:
                        result = json.load(f)

                    profile1_name = result.get("participants", {}).get("person1", "")
                    profile2_name = result.get("participants", {}).get("person2", "")
                    compatibility_score = result.get("compatibility", {}).get("score", None)
                    completed_days = result.get("completed_days", 0)

                    simulations.append(SimulationStatus(
                        simulation_id=sim_id,
                        status=result.get("status", "completed"),
                        profile1_id=profile1_name.lower().replace(" ", "_"),
                        profile2_id=profile2_name.lower().replace(" ", "_"),
                        profile1=profile1_name,
                        profile2=profile2_name,
                        compatibility_score=compatibility_score,
                        completed_days=completed_days,
                        created_at=result.get("start_time", ""),
                        completed_at=result.get("end_time", ""),
                        error=result.get("error", None)
                    ))
                except Exception as e:
                    print(f"Error loading simulation {filename}: {e}")
                    continue

    # Sort by created_at in descending order (most recent first)
    simulations.sort(key=lambda x: x.created_at, reverse=True)

    return simulations

@app.get("/api/simulations/{simulation_id}")
def get_simulation(simulation_id: str):
    """Get simulation status and results"""
    # Check in-memory first
    if simulation_id in simulation_status:
        status = simulation_status[simulation_id]

        # If completed, return full results
        if status["status"] == "completed" and "result" in status:
            return {
                **status,
                "result": status["result"]
            }

        # Otherwise return status only
        return status

    # If not in memory, try to load from disk
    simulation_file = os.path.join("simulations", f"{simulation_id}.json")
    if os.path.exists(simulation_file):
        try:
            with open(simulation_file, 'r') as f:
                result = json.load(f)

            # Return the loaded simulation
            return {
                "simulation_id": simulation_id,
                "status": result.get("status", "completed"),
                "profile1_id": result.get("participants", {}).get("person1", "").lower().replace(" ", "_"),
                "profile2_id": result.get("participants", {}).get("person2", "").lower().replace(" ", "_"),
                "created_at": result.get("start_time", ""),
                "completed_at": result.get("end_time", ""),
                "error": result.get("error", None),
                "result": result
            }
        except Exception as e:
            print(f"Error loading simulation from disk: {e}")
            raise HTTPException(status_code=500, detail=f"Error loading simulation: {str(e)}")

    # Not found in memory or on disk
    raise HTTPException(status_code=404, detail="Simulation not found")

@app.delete("/api/simulations/{simulation_id}")
def delete_simulation(simulation_id: str):
    """Delete a simulation"""
    if simulation_id not in simulation_status:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Delete from memory
    del simulation_status[simulation_id]

    # Try to delete output files
    output_dir = "src/output"
    for ext in [".json", ".txt"]:
        filepath = f"{output_dir}/{simulation_id}{ext}"
        if os.path.exists(filepath):
            os.remove(filepath)

    return {"message": "Simulation deleted successfully"}

# Chat Endpoints
@app.post("/api/chats/start")
def start_chat(request: ChatStartRequest):
    """Start a new chat with a digital twin"""
    try:
        # Load profile
        profile = load_profile_by_id(request.profile_id)

        # Create chat session
        chat = UserTwinChat(profile, request.user_name)
        chat_id = chat.chat_id

        # Store in memory
        active_chats[chat_id] = chat

        return {
            "chat_id": chat_id,
            "profile_name": profile.name,
            "profile_mbti": profile.mbti.value,
            "initial_fondness": chat.get_current_fondness(),
            "message": f"Chat started with {profile.name}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting chat: {str(e)}")

@app.post("/api/chats/{chat_id}/message", response_model=ChatMessageResponse)
def send_message(chat_id: str, request: ChatMessageRequest):
    """Send a message to the twin"""
    if chat_id not in active_chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        chat = active_chats[chat_id]
        exchange = chat.send_message(request.message, request.context)

        return ChatMessageResponse(
            message=exchange["twin_response"]["message"],
            emotion=exchange["twin_response"]["emotion"],
            internal_thought=exchange["twin_response"]["internal_thought"],
            fondness_change=exchange["twin_response"]["fondness_change"],
            fondness_level=exchange["twin_response"]["fondness_level"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@app.get("/api/chats/{chat_id}/history")
def get_chat_history(chat_id: str):
    """Get the full conversation history"""
    if chat_id not in active_chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat = active_chats[chat_id]
    return {
        "chat_id": chat_id,
        "profile_name": chat.profile.name,
        "conversation": chat.get_conversation_history(),
        "current_fondness": chat.get_current_fondness(),
        "message_count": len(chat.conversation)
    }

@app.get("/api/chats/{chat_id}/fondness")
def get_fondness_history(chat_id: str):
    """Get the fondness history"""
    if chat_id not in active_chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat = active_chats[chat_id]
    return {
        "chat_id": chat_id,
        "current_fondness": chat.get_current_fondness(),
        "fondness_history": chat.get_fondness_history()
    }

@app.delete("/api/chats/{chat_id}")
def end_chat(chat_id: str):
    """End a chat session"""
    if chat_id not in active_chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Save chat before deleting
    chat = active_chats[chat_id]
    filepath = chat.save_chat()

    # Delete from memory
    del active_chats[chat_id]

    return {
        "message": "Chat ended successfully",
        "saved_to": filepath,
        "final_fondness": chat.get_current_fondness()
    }

@app.get("/api/chats")
def list_chats():
    """Get all active chats"""
    return [
        {
            "chat_id": chat_id,
            "profile_name": chat.profile.name,
            "message_count": len(chat.conversation),
            "current_fondness": chat.get_current_fondness()
        }
        for chat_id, chat in active_chats.items()
    ]

# For development/debugging
@app.get("/api/debug/status")
def debug_status():
    """Get server status and configuration"""
    return {
        "profiles_count": len(UserProfile.load_all("profiles")),
        "simulations_count": len(simulation_status),
        "active_simulations": sum(1 for s in simulation_status.values() if s["status"] == "running"),
        "working_directory": os.getcwd(),
    }

if __name__ == "__main__":
    import uvicorn

    # Change to backend directory if not already there
    backend_dir = Path(__file__).parent.parent.parent
    os.chdir(backend_dir)

    print("\n" + "=" * 70)
    print("🚀 Starting Auralie API Server")
    print("=" * 70)
    print(f"\nWorking directory: {os.getcwd()}")
    print(f"Profiles directory: {os.path.join(os.getcwd(), 'profiles')}")
    print(f"\nAPI Documentation: http://localhost:8000/docs")
    print("=" * 70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
