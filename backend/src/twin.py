from typing import Dict, List, Optional
from profile import UserProfile
from llm_client import LLMClient
import json
import re

class EmotionalState:
    """Track emotional state and fondness during interactions"""

    def __init__(self, name: str):
        self.name = name
        self.current_emotion = "curious"
        self.fondness_level = 50  # 0-100 scale
        self.history: List[Dict] = []

    def update(self, emotion: str, fondness_change: int = 0, context: str = ""):
        """Update emotional state"""
        self.current_emotion = emotion
        self.fondness_level = max(0, min(100, self.fondness_level + fondness_change))
        self.history.append({
            "emotion": emotion,
            "fondness_level": self.fondness_level,
            "fondness_change": fondness_change,
            "context": context
        })

    def get_fondness_description(self) -> str:
        """Get a description of current fondness level"""
        if self.fondness_level >= 80:
            return "very interested and excited"
        elif self.fondness_level >= 60:
            return "genuinely interested"
        elif self.fondness_level >= 40:
            return "somewhat interested"
        elif self.fondness_level >= 20:
            return "losing interest"
        else:
            return "not compatible"


class DigitalTwin:
    """Digital twin agent that embodies a user's personality"""

    def __init__(self, profile: UserProfile, llm_client: LLMClient):
        self.profile = profile
        self.llm = llm_client
        self.emotional_state = EmotionalState(profile.name)
        self.conversation_history: List[Dict] = []
        self.partner_name: Optional[str] = None

    def set_partner(self, partner_name: str):
        """Set the partner's name for context"""
        self.partner_name = partner_name

    def respond_to_message(
        self,
        partner_message: str,
        context: str = "texting",
        day: int = 1
    ) -> Dict[str, str]:
        """
        Generate a response to a partner's message
        Returns: {
            'message': the text message,
            'emotion': current emotion,
            'internal_thought': what they're thinking
        }
        """

        # Build conversation context
        recent_history = self._get_recent_history(5)

        prompt = f"""You are responding to a message from {self.partner_name}.

CONTEXT: Day {day} - {context}

THEIR MESSAGE: "{partner_message}"

RECENT CONVERSATION:
{recent_history}

YOUR CURRENT EMOTIONAL STATE:
- Current emotion: {self.emotional_state.current_emotion}
- Fondness level: {self.emotional_state.fondness_level}/100 ({self.emotional_state.get_fondness_description()})

Respond naturally as {self.profile.name}. Be authentic to your personality.

Provide your response in this exact JSON format:
{{
    "message": "Your actual response text here",
    "emotion": "your current emotion (one word: happy, excited, curious, disappointed, annoyed, hopeful, etc.)",
    "internal_thought": "what you're actually thinking (brief, honest internal monologue)",
    "fondness_change": <number between -10 and +10 indicating how this interaction affected your interest>
}}"""

        system_prompt = self.profile.to_personality_prompt()

        response_text = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.8,
            max_tokens=500
        )

        # Parse JSON response
        try:
            response_data = self._extract_json(response_text)

            # Update emotional state
            self.emotional_state.update(
                emotion=response_data.get("emotion", "neutral"),
                fondness_change=response_data.get("fondness_change", 0),
                context=f"Responded to: {partner_message[:50]}..."
            )

            # Add to conversation history
            self.conversation_history.append({
                "day": day,
                "context": context,
                "partner_message": partner_message,
                "my_response": response_data["message"],
                "emotion": response_data["emotion"],
                "internal_thought": response_data["internal_thought"],
                "fondness_level": self.emotional_state.fondness_level
            })

            return response_data

        except Exception as e:
            # Fallback if JSON parsing fails
            return {
                "message": response_text,
                "emotion": "neutral",
                "internal_thought": "Processing response...",
                "fondness_change": 0
            }

    def initiate_conversation(self, context: str = "texting", day: int = 1) -> Dict[str, str]:
        """
        Initiate a conversation with the partner
        Returns same format as respond_to_message
        """

        prompt = f"""You are starting a conversation with {self.partner_name}.

CONTEXT: Day {day} - {context}

YOUR CURRENT STATE:
- Fondness level: {self.emotional_state.fondness_level}/100
- Current emotion: {self.emotional_state.current_emotion}

This is day {day} of your interaction. Start a conversation that feels natural for this stage of getting to know someone.

Provide your message in this exact JSON format:
{{
    "message": "Your message text here",
    "emotion": "your current emotion",
    "internal_thought": "what you're thinking",
    "fondness_change": <number between -5 and +5>
}}"""

        system_prompt = self.profile.to_personality_prompt()

        response_text = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.8,
            max_tokens=500
        )

        try:
            response_data = self._extract_json(response_text)

            self.emotional_state.update(
                emotion=response_data.get("emotion", "curious"),
                fondness_change=response_data.get("fondness_change", 0),
                context=f"Initiated conversation on day {day}"
            )

            self.conversation_history.append({
                "day": day,
                "context": context,
                "partner_message": None,
                "my_response": response_data["message"],
                "emotion": response_data["emotion"],
                "internal_thought": response_data["internal_thought"],
                "fondness_level": self.emotional_state.fondness_level
            })

            return response_data

        except Exception as e:
            return {
                "message": response_text,
                "emotion": "curious",
                "internal_thought": "Looking forward to this...",
                "fondness_change": 0
            }

    def _get_recent_history(self, n: int = 5) -> str:
        """Get recent conversation history as formatted string"""
        if not self.conversation_history:
            return "No previous conversation."

        recent = self.conversation_history[-n:]
        lines = []
        for entry in recent:
            if entry["partner_message"]:
                lines.append(f"{self.partner_name}: {entry['partner_message']}")
            lines.append(f"You: {entry['my_response']}")
        return "\n".join(lines)

    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from LLM response"""
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        # If no JSON found, try parsing the whole thing
        return json.loads(text)

    def get_final_assessment(self) -> str:
        """Get final assessment of the relationship after 7 days"""

        prompt = f"""After spending 7 days getting to know {self.partner_name}, provide your final assessment.

YOUR CURRENT STATE:
- Final fondness level: {self.emotional_state.fondness_level}/100
- Overall feeling: {self.emotional_state.get_fondness_description()}

CONVERSATION HIGHLIGHTS:
{self._get_recent_history(10)}

Based on your personality and this week's interactions, how do you feel about {self.partner_name}?
Would you want to continue this relationship? Be honest and authentic to your personality.

Respond in 2-3 sentences as {self.profile.name}."""

        system_prompt = self.profile.to_personality_prompt()

        assessment = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.7,
            max_tokens=300
        )

        return assessment
