from typing import List, Dict
from profile import UserProfile
from twin import DigitalTwin
from llm_client import LLMClient
from datetime import datetime
import json
import os

class UserTwinChat:
    """Manages a chat conversation between a user and a digital twin"""

    def __init__(self, profile: UserProfile, user_name: str = "You"):
        self.profile = profile
        self.user_name = user_name
        self.llm = LLMClient()
        self.twin = DigitalTwin(profile, self.llm)
        self.twin.set_partner(user_name)
        self.chat_id = f"chat_{profile.name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversation: List[Dict] = []

    def send_message(self, user_message: str, context: str = "texting") -> Dict:
        """
        Send a message to the twin and get their response

        Returns:
        {
            "user_message": str,
            "twin_response": {
                "message": str,
                "emotion": str,
                "internal_thought": str,
                "fondness_change": int,
                "fondness_level": int
            }
        }
        """
        # Get twin's response
        response = self.twin.respond_to_message(
            partner_message=user_message,
            context=context,
            day=len(self.conversation) // 10 + 1  # Rough day estimation
        )

        # Save the exchange
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "twin_response": {
                "message": response["message"],
                "emotion": response["emotion"],
                "internal_thought": response["internal_thought"],
                "fondness_change": response.get("fondness_change", 0),
                "fondness_level": self.twin.emotional_state.fondness_level
            }
        }

        self.conversation.append(exchange)
        return exchange

    def get_conversation_history(self) -> List[Dict]:
        """Get the full conversation history"""
        return self.conversation

    def get_current_fondness(self) -> int:
        """Get the twin's current fondness level"""
        return self.twin.emotional_state.fondness_level

    def get_fondness_history(self) -> List[Dict]:
        """Get the history of fondness changes"""
        return self.twin.emotional_state.history

    def save_chat(self, directory: str = "chats") -> str:
        """Save the chat to a JSON file"""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"{self.chat_id}.json")

        chat_data = {
            "chat_id": self.chat_id,
            "profile_name": self.profile.name,
            "user_name": self.user_name,
            "start_time": self.conversation[0]["timestamp"] if self.conversation else None,
            "conversation": self.conversation,
            "final_fondness": self.twin.emotional_state.fondness_level,
            "message_count": len(self.conversation)
        }

        with open(filepath, 'w') as f:
            json.dump(chat_data, f, indent=2)

        return filepath

    @classmethod
    def load_chat(cls, filepath: str) -> 'UserTwinChat':
        """Load a saved chat from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Reconstruct the profile (you'd need to load it from profiles directory)
        profile_name = data["profile_name"]
        profile = UserProfile.load(f"profiles/{profile_name.lower().replace(' ', '_')}.json")

        chat = cls(profile, data["user_name"])
        chat.chat_id = data["chat_id"]
        chat.conversation = data["conversation"]

        # Restore twin's fondness level
        if data.get("final_fondness"):
            chat.twin.emotional_state.fondness_level = data["final_fondness"]

        return chat
