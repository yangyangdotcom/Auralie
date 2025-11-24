from typing import List, Dict
import random

class ActivityScenario:
    """Defines different date/activity scenarios"""

    ACTIVITIES = {
        1: [
            {
                "name": "Coffee date",
                "description": "Meeting for coffee at a cozy local cafe",
                "intimacy_level": 2,
                "suitable_for_day": [1, 2]
            },
            {
                "name": "Dog walking at the park",
                "description": "Walking dogs together at Winston Park",
                "intimacy_level": 3,
                "suitable_for_day": [1, 2, 3]
            }
        ],
        2: [
            {
                "name": "Dinner date",
                "description": "Having dinner at a nice restaurant",
                "intimacy_level": 5,
                "suitable_for_day": [3, 4, 5]
            },
            {
                "name": "Movie night",
                "description": "Watching a movie together at the cinema",
                "intimacy_level": 4,
                "suitable_for_day": [3, 4, 5]
            },
            {
                "name": "Museum visit",
                "description": "Exploring an art museum together",
                "intimacy_level": 4,
                "suitable_for_day": [3, 4, 5]
            },
            {
                "name": "Hiking adventure",
                "description": "Going on a scenic hike together",
                "intimacy_level": 5,
                "suitable_for_day": [4, 5, 6]
            }
        ],
        3: [
            {
                "name": "Cooking together",
                "description": "Cooking dinner together at someone's place",
                "intimacy_level": 7,
                "suitable_for_day": [5, 6, 7]
            },
            {
                "name": "Weekend getaway",
                "description": "Taking a short trip to a nearby town",
                "intimacy_level": 8,
                "suitable_for_day": [6, 7]
            },
            {
                "name": "Intimate evening",
                "description": "Spending quality intimate time together",
                "intimacy_level": 9,
                "suitable_for_day": [6, 7]
            }
        ]
    }

    @classmethod
    def get_activity_for_day(cls, day: int, fondness_avg: int) -> Dict:
        """
        Get an appropriate activity based on day and relationship progress

        Args:
            day: Current day (1-7)
            fondness_avg: Average fondness level between both people (0-100)
        """

        # Determine intimacy tier based on fondness
        if fondness_avg >= 70:
            tier = 3
        elif fondness_avg >= 50:
            tier = 2
        else:
            tier = 1

        # Get activities for this tier
        available_activities = cls.ACTIVITIES.get(tier, cls.ACTIVITIES[1])

        # Filter by suitable day
        suitable = [a for a in available_activities if day in a["suitable_for_day"]]

        if not suitable:
            suitable = available_activities

        return random.choice(suitable)

    @classmethod
    def get_texting_context(cls, day: int, time_of_day: str) -> str:
        """Get context for texting based on day and time"""

        contexts = {
            1: {
                "morning": "Just matched and starting to text for the first time",
                "evening": "Continuing the conversation after a day of texting"
            },
            2: {
                "morning": "Good morning text after yesterday's conversation",
                "evening": "Evening chat, getting more comfortable"
            },
            3: {
                "morning": "Morning check-in, building connection",
                "evening": "Planning or discussing recent activities"
            },
            4: {
                "morning": "Warm morning greeting",
                "evening": "Deeper conversation in the evening"
            },
            5: {
                "morning": "Familiar morning text",
                "evening": "Comfortable evening chat"
            },
            6: {
                "morning": "Affectionate morning message",
                "evening": "Intimate evening conversation"
            },
            7: {
                "morning": "Close morning connection",
                "evening": "Reflecting on the week together"
            }
        }

        return contexts.get(day, contexts[1])[time_of_day]
