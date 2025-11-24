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

# API Models
class SimulationRequest(BaseModel):
    profile1_id: str
    profile2_id: str

class SimulationStatus(BaseModel):
    simulation_id: str
    status: str  # "pending", "running", "completed", "failed"
    profile1_id: str
    profile2_id: str
    created_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None

class SimulationResponse(BaseModel):
    simulation_id: str
    status: str
    message: str

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

@app.get("/api/profiles", response_model=List[UserProfile])
def list_profiles():
    """Get all available profiles"""
    try:
        profiles = UserProfile.load_all("profiles")
        return profiles
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
    return [
        SimulationStatus(**status)
        for status in simulation_status.values()
    ]

@app.get("/api/simulations/{simulation_id}")
def get_simulation(simulation_id: str):
    """Get simulation status and results"""
    if simulation_id not in simulation_status:
        raise HTTPException(status_code=404, detail="Simulation not found")

    status = simulation_status[simulation_id]

    # If completed, return full results
    if status["status"] == "completed" and "result" in status:
        return {
            **status,
            "result": status["result"]
        }

    # Otherwise return status only
    return status

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
