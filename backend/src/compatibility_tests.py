"""
Compatibility-testing conversation topics
These scenarios naturally reveal compatibility issues between twins
"""

from typing import List
import random

class CompatibilityTestScenarios:
    """Generate conversation topics that test compatibility"""

    # Topics that reveal lifestyle differences
    LIFESTYLE_TESTS = [
        "What does your ideal Friday night look like?",
        "How do you typically spend your weekends?",
        "Do you prefer big social gatherings or intimate hangouts with close friends?",
        "How much alone time do you need to recharge?",
        "What's your ideal work-life balance?",
    ]

    # Topics that test long-term compatibility
    FUTURE_PLANNING_TESTS = [
        "Where do you see yourself living in 5 years?",
        "What are your thoughts on having kids someday?",
        "How important is career advancement vs personal fulfillment to you?",
        "What does financial stability mean to you?",
        "What are your non-negotiables in a long-term relationship?",
    ]

    # Topics that reveal value differences
    VALUES_TESTS = [
        "What do you value most in a relationship?",
        "How do you handle conflict in relationships?",
        "What role does honesty vs kindness play when they conflict?",
        "How important is maintaining your independence in a relationship?",
        "What are your thoughts on traditional vs modern relationship roles?",
    ]

    # Topics that test communication compatibility
    COMMUNICATION_TESTS = [
        "How do you prefer to resolve disagreements?",
        "Do you need to talk through problems immediately or take time to think first?",
        "How much communication is too much vs too little for you?",
        "How do you show affection - words, actions, quality time, or physical touch?",
        "How comfortable are you with deep emotional conversations?",
    ]

    # Topics that reveal deal-breaker conflicts
    DEALBREAKER_TESTS = [
        "What are absolute deal-breakers for you in dating?",
        "What personality traits do you find most frustrating in others?",
        "What's something people often do that bothers you?",
        "What would make you end a relationship immediately?",
        "What behaviors or habits are you unwilling to compromise on?",
    ]

    @classmethod
    def get_test_for_day(cls, day: int) -> str:
        """
        Get an appropriate compatibility test question for a given day
        Early days: lighter lifestyle questions
        Later days: deeper values and future planning
        """
        if day <= 2:
            # Day 1-2: Lifestyle compatibility
            return random.choice(cls.LIFESTYLE_TESTS)
        elif day <= 4:
            # Day 3-4: Communication and values
            return random.choice(cls.COMMUNICATION_TESTS + cls.VALUES_TESTS)
        else:
            # Day 5+: Future planning and dealbreakers
            return random.choice(cls.FUTURE_PLANNING_TESTS + cls.DEALBREAKER_TESTS)

    @classmethod
    def get_context_for_test(cls, question: str) -> str:
        """Generate a context string for why this question is being asked"""
        contexts = [
            f"The conversation naturally turns to deeper topics. You find yourself asking: \"{question}\"",
            f"You're curious to know more about their perspective, so you ask: \"{question}\"",
            f"To understand them better, you bring up: \"{question}\"",
            f"The topic comes up naturally: \"{question}\"",
        ]
        return random.choice(contexts)

    @classmethod
    def inject_compatibility_test(cls, twin_response: str, day: int) -> str:
        """
        Optionally inject a compatibility test question into a twin's message
        Returns the enhanced message with a test question added
        """
        # 30% chance to add a compatibility test
        if random.random() < 0.3:
            test_question = cls.get_test_for_day(day)
            # Add the question naturally to their message
            return f"{twin_response} By the way, I'm curious - {test_question.lower()}"
        return twin_response
