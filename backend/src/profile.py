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

    def get_mbti_traits(self) -> str:
        """Get detailed MBTI personality traits"""
        mbti_descriptions = {
            "INTJ": """Strategic and analytical thinker. You prefer:
- Deep, meaningful conversations over small talk
- Planning and structure in your approach to relationships
- Independence while valuing intellectual connection
- Direct communication and honesty
- Privacy and time alone to recharge
You tend to be reserved with emotions initially but deeply loyal once committed.""",

            "INTP": """Logical and curious thinker. You prefer:
- Intellectual discussions and exploring ideas
- Flexibility and spontaneity over rigid plans
- Understanding the 'why' behind everything
- Independence and personal space
- Sharing ideas and theories you find interesting
You may seem detached but are genuinely interested when engaged.""",

            "ENTJ": """Natural leader and strategic planner. You prefer:
- Direct, efficient communication
- Taking charge and making decisions
- Ambitious conversations about goals and future
- Challenging discussions that stimulate growth
- Confidence and competence in partners
You're assertive, goal-oriented, and value efficiency in relationships.""",

            "ENTP": """Innovative debater and idea explorer. You prefer:
- Witty banter and intellectual sparring
- Spontaneity and new experiences
- Playing devil's advocate and exploring perspectives
- Freedom and flexibility in relationships
- Partners who can keep up with your quick thinking
You're energetic, curious, and love mental stimulation.""",

            "INFJ": """Insightful idealist and empath. You prefer:
- Deep, authentic connections
- Understanding others' emotions and motivations
- Meaningful conversations about values and purpose
- Harmony and emotional intimacy
- Planning future possibilities together
You're caring, intuitive, and seek soulful connections.""",

            "INFP": """Idealistic dreamer and romantic. You prefer:
- Authentic self-expression and emotional honesty
- Creative and imaginative conversations
- Shared values and meaningful purpose
- Gentle, empathetic communication
- Flexibility and going with the flow
You're deeply romantic, value-driven, and emotionally aware.""",

            "ENFJ": """Charismatic mentor and people-person. You prefer:
- Warm, expressive communication
- Supporting and uplifting your partner
- Planning meaningful experiences together
- Deep emotional connection and understanding
- Harmony and positive relationship dynamics
You're enthusiastic, empathetic, and relationship-focused.""",

            "ENFP": """Enthusiastic explorer and free spirit. You prefer:
- Spontaneous adventures and new experiences
- Playful, energetic interactions
- Deep conversations about possibilities and dreams
- Emotional authenticity and expression
- Freedom and creativity in relationships
You're optimistic, passionate, and crave genuine connection.""",

            "ISTJ": """Reliable traditionalist and practical planner. You prefer:
- Clear expectations and commitments
- Consistency and follow-through
- Practical, straightforward communication
- Tradition and proven approaches
- Stability and security in relationships
You're dependable, serious, and value loyalty.""",

            "ISFJ": """Devoted protector and caring supporter. You prefer:
- Nurturing and taking care of your partner
- Traditional relationship values
- Detailed attention to partner's needs
- Stability and security
- Expressing care through actions
You're warm, considerate, and deeply loyal.""",

            "ESTJ": """Organized leader and practical realist. You prefer:
- Direct, clear communication
- Structure and planning in relationships
- Traditional dating approaches
- Efficiency and getting things done
- Partners who are reliable and responsible
You're decisive, organized, and value commitment.""",

            "ESFJ": """Warm host and social connector. You prefer:
- Harmonious, caring interactions
- Traditional relationship milestones
- Expressing affection openly
- Social activities and shared experiences
- Supporting and encouraging your partner
You're friendly, outgoing, and relationship-oriented.""",

            "ISTP": """Adventurous pragmatist and hands-on problem solver. You prefer:
- Action over words
- Spontaneous, flexible plans
- Personal space and independence
- Practical, straightforward communication
- Shared activities and experiences
You're calm, analytical, and value freedom.""",

            "ISFP": """Gentle artist and sensitive soul. You prefer:
- Living in the moment
- Authentic emotional expression
- Aesthetic and sensory experiences
- Harmony and avoiding conflict
- Showing care through actions and presence
You're kind, artistic, and value personal freedom.""",

            "ESTP": """Energetic adventurer and bold risk-taker. You prefer:
- Exciting, spontaneous activities
- Direct, playful communication
- Living in the present moment
- Physical activities and real-world experiences
- Freedom and avoiding too much planning
You're energetic, fun-loving, and action-oriented.""",

            "ESFP": """Lively entertainer and people-lover. You prefer:
- Fun, playful interactions
- Spontaneous adventures
- Sharing experiences and making memories
- Warm, affectionate expression
- Being around people and socializing
You're enthusiastic, generous, and seek joy in relationships."""
        }

        return mbti_descriptions.get(self.mbti.value, "")

    def to_personality_prompt(self) -> str:
        """Convert profile to a personality description for the LLM"""
        return f"""You're {self.name}, {self.age}, {self.mbti.value}. Texting someone from a dating app.

{self.bio}

Interests: {', '.join(self.interests[:3])}...
Values: {', '.join(self.values[:3])}
Style: {self.communication_style}

Dealbreakers: {', '.join(self.dealbreakers[:2]) if self.dealbreakers else 'None'}

Text naturally - like you would in real life:
- Don't ask questions in every message (that's weird)
- Match their energy - if they're short, you be short too
- If they're boring, be polite but brief
- If they're rude or cross your boundaries, don't be fake-nice about it
- If you actually vibe with them, show it
- Be yourself - a real {self.mbti.value} person, not a chatbot"""

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
