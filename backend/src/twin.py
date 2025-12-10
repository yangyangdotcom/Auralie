from typing import List, Dict, Optional
from profile import UserProfile
from llm_client import LLMClient
import json
import re

class EmotionalState:
    """Track emotional state and fondness during interactions"""

    def __init__(self, name: str):
        from config import Config
        self.name = name
        self.current_emotion = "curious"
        self.fondness_level = Config.STARTING_FONDNESS  # 0-100 scale (configurable)
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
        self.partner_profile: Optional[UserProfile] = None

    def set_partner(self, partner_name: str, partner_profile: Optional[UserProfile] = None):
        """Set the partner's name and profile for context"""
        self.partner_name = partner_name
        self.partner_profile = partner_profile

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
        from config import Config
        recent_history = self._get_recent_history(5)

        # Build forced evaluation instruction if enabled
        forced_eval_text = ""
        if Config.FORCE_FONDNESS_EVALUATION:
            forced_eval_text = "\n⚠️ CRITICAL: fondness_change MUST be a non-zero value. Evaluate every message carefully - no neutral (0) responses allowed. Every interaction affects compatibility."

        # Build emotional tone enforcement if enabled
        tone_instruction = ""
        previous_context = ""
        if Config.ENFORCE_EMOTIONAL_TONE:
            from emotional_tone import EmotionalToneGuidelines
            tone_instruction = EmotionalToneGuidelines.get_tone_instruction(
                self.emotional_state.current_emotion,
                self.emotional_state.fondness_level
            )

            # Add previous interaction context
            if self.conversation_history:
                last_interaction = self.conversation_history[-1]
                last_thought = last_interaction.get("internal_thought", "")
                last_fondness_change = self.emotional_state.history[-1]["fondness_change"] if self.emotional_state.history else 0
                previous_context = EmotionalToneGuidelines.get_previous_context(last_thought, last_fondness_change)

        prompt = f"""Day {day}, {context}

They said: "{partner_message}"

Recent chat:
{recent_history}

How you feel right now: {self.emotional_state.current_emotion}, fondness {self.emotional_state.fondness_level}/100

Reply naturally. Don't overthink it. Text back like you would on a dating app.

JSON format:
{{
    "message": "your text (1-2 sentences usually, don't ask questions every time)",
    "emotion": "one word (happy/bored/annoyed/excited/etc)",
    "internal_thought": "what you're really thinking",
    "fondness_change": integer from -10 to +10 based on how you feel about their message
}}"""

        system_prompt = self.profile.to_personality_prompt()

        response_text = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.9,  # Higher temperature for more varied, emotional responses
            max_tokens=500
        )

        # Parse JSON response
        try:
            response_data = self._extract_json(response_text)

            # Apply automatic incompatibility penalty if enabled
            fondness_change = response_data.get("fondness_change", 0)
            llm_decision = fondness_change
            value_penalty = 0
            dealbreaker_penalty = 0

            if Config.AUTO_INCOMPATIBILITY_PENALTY and self.partner_profile:
                from compatibility import CompatibilityAnalyzer

                # Get individual penalties
                value_mismatch = CompatibilityAnalyzer.calculate_value_mismatch(
                    self.profile, self.partner_profile
                )
                dealbreaker = CompatibilityAnalyzer.check_dealbreaker_violation(
                    self.profile, self.partner_profile
                )

                value_penalty = value_mismatch
                dealbreaker_penalty = dealbreaker

                # Apply penalties (cumulative with LLM's assessment)
                fondness_change += value_penalty + dealbreaker_penalty
                # Cap at -10 to 10 range
                fondness_change = max(-10, min(10, fondness_change))

            # Update emotional state
            self.emotional_state.update(
                emotion=response_data.get("emotion", "neutral"),
                fondness_change=fondness_change,
                context=f"Responded to: {partner_message[:50]}..."
            )

            # Add to conversation history
            message = response_data["message"]
            self.conversation_history.append({
                "day": day,
                "context": context,
                "partner_message": partner_message,
                "my_response": message,
                "emotion": response_data["emotion"],
                "internal_thought": response_data["internal_thought"],
                "fondness_level": self.emotional_state.fondness_level
            })

            # Update response data with potentially modified message and breakdown
            response_data["message"] = message
            response_data["fondness_breakdown"] = {
                "total": fondness_change,
                "llm_decision": llm_decision,
                "value_penalty": value_penalty,
                "dealbreaker_penalty": dealbreaker_penalty
            }

            return response_data

        except Exception as e:
            # Fallback if JSON parsing fails
            print(f"⚠️  JSON parsing failed for {self.profile.name}: {str(e)}")
            print(f"Raw response: {response_text[:200]}...")
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
        from config import Config

        # Build emotional tone enforcement if enabled
        tone_instruction = ""
        previous_context = ""
        if Config.ENFORCE_EMOTIONAL_TONE:
            from emotional_tone import EmotionalToneGuidelines
            tone_instruction = EmotionalToneGuidelines.get_tone_instruction(
                self.emotional_state.current_emotion,
                self.emotional_state.fondness_level
            )

            # Add previous interaction context
            if self.conversation_history:
                last_interaction = self.conversation_history[-1]
                last_thought = last_interaction.get("internal_thought", "")
                last_fondness_change = self.emotional_state.history[-1]["fondness_change"] if self.emotional_state.history else 0
                previous_context = EmotionalToneGuidelines.get_previous_context(last_thought, last_fondness_change)

        prompt = f"""Day {day}, {context}. You're starting the conversation with {self.partner_name}.

You're feeling: {self.emotional_state.current_emotion}, fondness {self.emotional_state.fondness_level}/100

Send a text. Keep it natural and casual.

JSON format:
{{
    "message": "your opening text (keep it simple, 1-2 sentences)",
    "emotion": "one word",
    "internal_thought": "what you're thinking",
    "fondness_change": integer from -5 to +5
}}"""

        system_prompt = self.profile.to_personality_prompt()

        response_text = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.9,  # Higher temperature for more varied, emotional responses
            max_tokens=500
        )

        try:
            response_data = self._extract_json(response_text)

            self.emotional_state.update(
                emotion=response_data.get("emotion", "curious"),
                fondness_change=response_data.get("fondness_change", 0),
                context=f"Initiated conversation: {context}"
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
            print(f"⚠️  JSON parsing failed for {self.profile.name}: {str(e)}")
            print(f"Raw response: {response_text[:200]}...")
            return {
                "message": response_text,
                "emotion": "curious",
                "internal_thought": "Looking forward to this...",
                "fondness_change": 0
            }

    def _get_recent_history(self, n: int = 5) -> str:
        """Get recent conversation history as a formatted string"""
        if not self.conversation_history:
            return "No previous conversation."

        recent = self.conversation_history[-n:]
        lines = []
        for entry in recent:
            if entry.get("partner_message"):
                lines.append(f"{self.partner_name}: {entry['partner_message']}")
            lines.append(f"You: {entry['my_response']}")
        return "\n".join(lines)

    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from LLM response"""
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_text = json_match.group()
            # Fix common JSON issues: remove leading + signs from numbers
            json_text = re.sub(r':\s*\+(\d+)', r': \1', json_text)
            return json.loads(json_text)
        # If no JSON found, try parsing the whole thing
        text = re.sub(r':\s*\+(\d+)', r': \1', text)
        return json.loads(text)

    def get_final_assessment(self) -> str:
        """Get final assessment of the relationship"""
        from config import Config

        prompt = f"""After spending {Config.SIMULATION_DAYS} days getting to know {self.partner_name}, provide your final assessment.

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

        return assessment.strip()
