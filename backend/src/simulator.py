from typing import List, Dict, Tuple
from profile import UserProfile
from twin import DigitalTwin
from llm_client import LLMClient
from activities import ActivityScenario
from config import Config
from datetime import datetime
import json
import os

class DatingSimulation:
    """Simulates a dating experience between two digital twins"""

    def __init__(self, profile1: UserProfile, profile2: UserProfile):
        self.profile1 = profile1
        self.profile2 = profile2

        self.llm = LLMClient()

        self.twin1 = DigitalTwin(profile1, self.llm)
        self.twin2 = DigitalTwin(profile2, self.llm)

        self.twin1.set_partner(profile2.name, profile2)
        self.twin2.set_partner(profile1.name, profile1)

        self.simulation_log: List[Dict] = []
        self.simulation_id = f"{profile1.name}_{profile2.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def simulate_texting_exchange(
        self,
        day: int,
        time_of_day: str,
        num_exchanges: int = 4
    ) -> List[Dict]:
        """Simulate a texting conversation between the twins"""

        context = ActivityScenario.get_texting_context(day, time_of_day)
        exchanges = []

        print(f"  💬 {time_of_day.capitalize()} texting session...")

        # First person initiates (alternate who starts based on time_of_day)
        if time_of_day == "morning":
            initiator = self.twin1
            responder = self.twin2
        else:
            initiator = self.twin2
            responder = self.twin1

        # Initial message
        init_response = initiator.initiate_conversation(context=f"texting - {context}", day=day)
        exchanges.append({
            "sender": initiator.profile.name,
            "message": init_response["message"],
            "emotion": init_response["emotion"],
            "internal_thought": init_response["internal_thought"],
            "fondness_level": initiator.emotional_state.fondness_level,
            "fondness_breakdown": init_response.get("fondness_breakdown")
        })

        # Back and forth exchanges
        for i in range(num_exchanges):
            # Responder replies
            resp_response = responder.respond_to_message(
                partner_message=exchanges[-1]["message"],
                context=f"texting - {context}",
                day=day
            )
            exchanges.append({
                "sender": responder.profile.name,
                "message": resp_response["message"],
                "emotion": resp_response["emotion"],
                "internal_thought": resp_response["internal_thought"],
                "fondness_level": responder.emotional_state.fondness_level,
                "fondness_breakdown": resp_response.get("fondness_breakdown")
            })

            # Initiator replies (except on last exchange)
            if i < num_exchanges - 1:
                init_response = initiator.respond_to_message(
                    partner_message=exchanges[-1]["message"],
                    context=f"texting - {context}",
                    day=day
                )
                exchanges.append({
                    "sender": initiator.profile.name,
                    "message": init_response["message"],
                    "emotion": init_response["emotion"],
                    "internal_thought": init_response["internal_thought"],
                    "fondness_level": initiator.emotional_state.fondness_level,
                    "fondness_breakdown": init_response.get("fondness_breakdown")
                })

        return exchanges

    def simulate_activity(self, day: int, activity: Dict) -> List[Dict]:
        """Simulate a physical activity/date"""

        print(f"  🎯 {activity['name']}...")

        interactions = []

        # Generate a narrative of the activity with 4-5 interaction points
        for round_num in range(4):
            if round_num == 0:
                # Person 1 starts the activity
                response1 = self.twin1.initiate_conversation(
                    context=f"{activity['name']} - {activity['description']}",
                    day=day
                )
                interactions.append({
                    "sender": self.twin1.profile.name,
                    "message": response1["message"],
                    "emotion": response1["emotion"],
                    "internal_thought": response1["internal_thought"],
                    "fondness_level": self.twin1.emotional_state.fondness_level
                })
            else:
                # Person 2 responds
                response2 = self.twin2.respond_to_message(
                    partner_message=interactions[-1]["message"],
                    context=f"{activity['name']} - {activity['description']}",
                    day=day
                )
                interactions.append({
                    "sender": self.twin2.profile.name,
                    "message": response2["message"],
                    "emotion": response2["emotion"],
                    "internal_thought": response2["internal_thought"],
                    "fondness_level": self.twin2.emotional_state.fondness_level
                })

                # Person 1 responds
                if round_num < 3:
                    response1 = self.twin1.respond_to_message(
                        partner_message=interactions[-1]["message"],
                        context=f"{activity['name']} - {activity['description']}",
                        day=day
                    )
                    interactions.append({
                        "sender": self.twin1.profile.name,
                        "message": response1["message"],
                        "emotion": response1["emotion"],
                        "internal_thought": response1["internal_thought"],
                        "fondness_level": self.twin1.emotional_state.fondness_level
                    })

        return interactions

    def generate_date_suggestions(self) -> List[str]:
        """Generate specific conversation starters for the actual date based on simulation"""

        # Build conversation summary
        conversation_summary = []
        for day_log in self.simulation_log:
            for session in day_log.get("texting_sessions", []):
                for exchange in session.get("exchanges", []):
                    # Handle fondness_breakdown being None
                    breakdown = exchange.get("fondness_breakdown") or {}
                    conversation_summary.append({
                        "sender": exchange["sender"],
                        "message": exchange["message"],
                        "fondness_change": breakdown.get("total", 0)
                    })
            for activity in day_log.get("activities", []):
                for interaction in activity.get("interactions", []):
                    conversation_summary.append({
                        "sender": interaction["sender"],
                        "message": interaction["message"],
                        "fondness_change": 0
                    })

        # Format conversation highlights (positive moments)
        highlights = []
        for msg in conversation_summary:
            if msg.get("fondness_change", 0) > 3:  # Strong positive reactions
                highlights.append(f"{msg['sender']}: {msg['message']}")

        # Build prompt for LLM
        prompt = f"""Based on this dating simulation between {self.profile1.name} and {self.profile2.name}, generate 5-7 SPECIFIC conversation starters they can use on their actual first date.

PROFILES:
{self.profile1.name}:
- Interests: {', '.join(self.profile1.interests[:5])}
- Values: {', '.join(self.profile1.values)}

{self.profile2.name}:
- Interests: {', '.join(self.profile2.interests[:5])}
- Values: {', '.join(self.profile2.values)}

CONVERSATION HIGHLIGHTS (topics that went well):
{chr(10).join(highlights[:10]) if highlights else "No strong positive moments"}

RECENT CONVERSATION SAMPLE:
{chr(10).join([f"{m['sender']}: {m['message']}" for m in conversation_summary[-15:]])}

Generate 5-7 specific, actionable conversation starters. Each should:
1. Reference something concrete from their profiles or conversation
2. Be specific (mention actual hobbies, books, places, activities discussed)
3. Be natural and casual
4. Help them connect deeper on topics they both care about

Format as a JSON array of strings:
["suggestion 1", "suggestion 2", ...]

Examples of GOOD suggestions:
- "Ask about her pottery class she mentioned - see if she'd teach you to make something"
- "Bring up the hiking trail at Yosemite you both talked about - suggest planning a trip"
- "She recommended The Alchemist - ask what resonated with her about it"

Examples of BAD suggestions (too generic):
- "Talk about your hobbies"
- "Ask about her interests"
- "Discuss your values"
"""

        system_prompt = "You are a dating coach who gives specific, personalized advice based on real conversations and profiles."

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            temperature=0.7,
            max_tokens=800
        )

        # Parse JSON response
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                suggestions = json.loads(json_match.group())
                return suggestions[:7]  # Cap at 7
            else:
                # Fallback: split by newlines and clean up
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                suggestions = [line.lstrip('- ').lstrip('• ').lstrip('1234567890. ') for line in lines if len(line) > 20]
                return suggestions[:7]
        except Exception as e:
            print(f"⚠️  Failed to parse date suggestions: {e}")
            return [
                f"Ask about {self.profile2.interests[0] if self.profile2.interests else 'their hobbies'}",
                f"Discuss your shared interest in {self.profile1.interests[0] if self.profile1.interests else 'common topics'}",
                "Share a story from your week and see what they've been up to"
            ]

    def simulate_day(self, day: int) -> Dict:
        """Simulate one complete day"""

        print(f"\n📅 DAY {day}")
        day_log = {
            "day": day,
            "texting_sessions": [],
            "activities": []
        }

        # Morning texting
        morning_texts = self.simulate_texting_exchange(day, "morning", num_exchanges=3)
        day_log["texting_sessions"].append({
            "time": "morning",
            "exchanges": morning_texts
        })

        # Physical activity every 2-3 days (if enabled)
        if Config.ENABLE_ACTIVITIES and day in [2, 4, 6]:
            avg_fondness = (
                self.twin1.emotional_state.fondness_level +
                self.twin2.emotional_state.fondness_level
            ) // 2

            activity = ActivityScenario.get_activity_for_day(day, avg_fondness)
            activity_log = self.simulate_activity(day, activity)
            day_log["activities"].append({
                "activity": activity,
                "interactions": activity_log
            })

        # Evening texting
        evening_texts = self.simulate_texting_exchange(day, "evening", num_exchanges=3)
        day_log["texting_sessions"].append({
            "time": "evening",
            "exchanges": evening_texts
        })

        return day_log

    def run_simulation(self) -> Dict:
        """Run the complete simulation"""

        print(f"\n{'='*60}")
        print(f"🎭 AURALIE SIMULATION ({Config.SIMULATION_DAYS} DAYS)")
        print(f"{'='*60}")
        print(f"👤 {self.profile1.name} ({self.profile1.mbti.value})")
        print(f"💕 {self.profile2.name} ({self.profile2.mbti.value})")
        print(f"{'='*60}\n")

        simulation_result = {
            "simulation_id": self.simulation_id,
            "participants": {
                "person1": self.profile1.name,
                "person2": self.profile2.name
            },
            "start_time": datetime.now().isoformat(),
            "days": [],
            "status": "in_progress"
        }

        # Simulate each day with error handling
        completed_days = 0
        try:
            for day in range(1, Config.SIMULATION_DAYS + 1):
                print(f"\n📅 DAY {day}")
                day_log = self.simulate_day(day)
                simulation_result["days"].append(day_log)
                self.simulation_log.append(day_log)
                completed_days = day

                # Save progress after each day
                if day % 2 == 0:  # Save every 2 days
                    self.save_simulation(simulation_result)

        except Exception as e:
            simulation_result["status"] = "failed"
            simulation_result["error"] = str(e)
            simulation_result["completed_days"] = completed_days
            print(f"\n⚠️  Simulation stopped at day {completed_days}: {str(e)}")

            # Save partial results
            self.save_simulation(simulation_result)
            raise  # Re-raise to let caller know it failed

        # Final assessments
        print(f"\n{'='*60}")
        print(f"📊 FINAL ASSESSMENT")
        print(f"{'='*60}\n")

        assessment1 = self.twin1.get_final_assessment()
        assessment2 = self.twin2.get_final_assessment()

        simulation_result["final_assessment"] = {
            self.profile1.name: {
                "statement": assessment1,
                "final_fondness": self.twin1.emotional_state.fondness_level
            },
            self.profile2.name: {
                "statement": assessment2,
                "final_fondness": self.twin2.emotional_state.fondness_level
            }
        }

        # Calculate compatibility
        avg_fondness = (
            self.twin1.emotional_state.fondness_level +
            self.twin2.emotional_state.fondness_level
        ) / 2

        if avg_fondness >= 75:
            compatibility = "Highly compatible"
        elif avg_fondness >= 60:
            compatibility = "Compatible"
        elif avg_fondness >= 40:
            compatibility = "Moderately compatible"
        else:
            compatibility = "Not compatible"

        simulation_result["compatibility"] = {
            "rating": compatibility,
            "score": avg_fondness
        }

        # Generate date suggestions
        print(f"\n💡 Generating date conversation suggestions...")
        try:
            date_suggestions = self.generate_date_suggestions()
            simulation_result["date_suggestions"] = date_suggestions
            print(f"   Generated {len(date_suggestions)} suggestions")
        except Exception as e:
            print(f"⚠️  Failed to generate date suggestions: {e}")
            simulation_result["date_suggestions"] = []

        simulation_result["status"] = "completed"
        simulation_result["completed_days"] = Config.SIMULATION_DAYS
        simulation_result["end_time"] = datetime.now().isoformat()

        # Save simulation
        self.save_simulation(simulation_result)

        return simulation_result

    def save_simulation(self, result: Dict):
        """Save simulation results to file"""
        os.makedirs("simulations", exist_ok=True)
        filepath = f"simulations/{self.simulation_id}.json"

        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)

        status = result.get("status", "unknown")
        days = result.get("completed_days", len(result.get("days", [])))

        if status == "completed":
            print(f"\n💾 Simulation saved to: {filepath}")
        else:
            print(f"\n💾 Partial simulation ({days} days) saved to: {filepath}")
