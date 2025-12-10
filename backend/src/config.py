import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for Auralie simulation"""

    # LLM Settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # Model settings
    # Recommended OpenRouter models:
    # - meta-llama/llama-3.1-70b-instruct (fast, cheap, good quality)
    # - anthropic/claude-3.5-sonnet (best quality, more expensive)
    # - google/gemini-pro-1.5 (good balance)
    # - openai/gpt-4-turbo (high quality, expensive)
    # - mistralai/mixtral-8x7b-instruct (fast, cheap)
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct")

    # Optional: Your app name for OpenRouter stats
    OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Auralie")

    # Simulation settings
    SIMULATION_DAYS = int(os.getenv("SIMULATION_DAYS", "7"))
    TEXTING_SESSIONS_PER_DAY = 2  # Morning and evening
    ACTIVITIES_PER_WEEK = 3  # Physical meetups
    ENABLE_ACTIVITIES = os.getenv("ENABLE_ACTIVITIES", "true").lower() == "true"  # Enable/disable physical activities

    # Fondness System Controls
    FORCE_FONDNESS_EVALUATION = os.getenv("FORCE_FONDNESS_EVALUATION", "true").lower() == "true"
    AUTO_INCOMPATIBILITY_PENALTY = os.getenv("AUTO_INCOMPATIBILITY_PENALTY", "true").lower() == "true"
    ENABLE_COMPATIBILITY_TESTS = os.getenv("ENABLE_COMPATIBILITY_TESTS", "true").lower() == "true"
    ENFORCE_EMOTIONAL_TONE = os.getenv("ENFORCE_EMOTIONAL_TONE", "true").lower() == "true"

    # Starting fondness level (default: 50, range: 0-100)
    STARTING_FONDNESS = int(os.getenv("STARTING_FONDNESS", "40"))

    # Paths
    PROFILES_DIR = "profiles"
    SIMULATIONS_DIR = "simulations"
    OUTPUT_DIR = "output"

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.LLM_PROVIDER == "openrouter" and not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not set in .env file")
        return True
