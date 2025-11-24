from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import json
import os

class MBTIType(str, Enum):
    """MBTI personality types"""
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"

class UserProfile(BaseModel):
    """User profile for creating digital twin"""

    # Basic info
    name: str = Field(..., description="User's name")
    age: int = Field(..., ge=18, le=100, description="User's age")
    gender: Gender = Field(..., description="User's gender")

    # Personality
    mbti: MBTIType = Field(..., description="MBTI personality type")
    bio: str = Field(..., description="Short bio or self-description")

    # Social media insights (simplified for MVP)
    instagram_style: str = Field(
        ...,
        description="Instagram profile vibe (e.g., 'travel enthusiast', 'foodie', 'fitness focused', 'artistic')"
    )
    linkedin_summary: str = Field(
        ...,
        description="Professional summary from LinkedIn"
    )

    # Interests and values
    interests: List[str] = Field(
        ...,
        min_length=3,
        max_length=10,
        description="List of hobbies and interests"
    )
    values: List[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="Core values (e.g., 'honesty', 'adventure', 'family')"
    )

    # Preferences
    love_language: str = Field(
        ...,
        description="Primary love language (words, touch, gifts, acts, quality time)"
    )
    dealbreakers: List[str] = Field(
        default_factory=list,
        description="Dating dealbreakers"
    )

    # Behavioral traits
    communication_style: str = Field(
        ...,
        description="How they communicate (e.g., 'direct and concise', 'warm and expressive', 'thoughtful and careful')"
    )
    spontaneity_level: int = Field(
        ...,
        ge=1,
        le=10,
        description="How spontaneous they are (1=very planned, 10=very spontaneous)"
    )
    emotional_expressiveness: int = Field(
        ...,
        ge=1,
        le=10,
        description="How emotionally expressive they are (1=reserved, 10=very expressive)"
    )

    def to_personality_prompt(self) -> str:
        """Convert profile to a personality description for the LLM"""
        return f"""You are {self.name}, a {self.age}-year-old {self.gender.value}.

PERSONALITY TYPE: {self.mbti.value}

BIO: {self.bio}

SOCIAL PRESENCE:
- Instagram: {self.instagram_style}
- Professional: {self.linkedin_summary}

INTERESTS: {', '.join(self.interests)}

VALUES: {', '.join(self.values)}

COMMUNICATION: {self.communication_style}
- Spontaneity level: {self.spontaneity_level}/10
- Emotional expressiveness: {self.emotional_expressiveness}/10
- Love language: {self.love_language}

DEALBREAKERS: {', '.join(self.dealbreakers) if self.dealbreakers else 'None specified'}

You should embody this personality consistently in all interactions. Stay true to these characteristics."""

    def save(self, directory: str = "profiles") -> str:
        """Save profile to JSON file"""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"{self.name.lower().replace(' ', '_')}.json")
        with open(filepath, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)
        return filepath

    @classmethod
    def load(cls, filepath: str) -> 'UserProfile':
        """Load profile from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)

    @classmethod
    def load_all(cls, directory: str = "profiles") -> List['UserProfile']:
        """Load all profiles from directory"""
        if not os.path.exists(directory):
            return []

        profiles = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                profiles.append(cls.load(filepath))
        return profiles
