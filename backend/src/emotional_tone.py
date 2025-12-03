"""
Emotional tone enforcement guidelines
Maps emotions to specific message tone requirements
"""

class EmotionalToneGuidelines:
    """Define how message tone should match emotional state"""

    TONE_RULES = {
        # Positive emotions
        "happy": {
            "length": "medium to long",
            "style": "warm, friendly, expressive",
            "questions": "yes - show interest",
            "emojis": "appropriate, 1-2 max",
            "example": "Use exclamation points, share enthusiastically, ask follow-up questions"
        },
        "excited": {
            "length": "long, detailed",
            "style": "enthusiastic, energetic, animated",
            "questions": "yes - lots of curiosity",
            "emojis": "appropriate, 2-3 max",
            "example": "Show genuine enthusiasm, ask multiple questions, share stories"
        },
        "delighted": {
            "length": "medium to long",
            "style": "warm, appreciative, positive",
            "questions": "yes - engaged interest",
            "emojis": "appropriate, 1-2 max",
            "example": "Express appreciation, build on their topic, show you're listening"
        },
        "intrigued": {
            "length": "medium",
            "style": "curious, engaged, thoughtful",
            "questions": "yes - probing questions",
            "emojis": "minimal or none",
            "example": "Ask clarifying questions, show intellectual curiosity"
        },
        "curious": {
            "length": "short to medium",
            "style": "inquisitive, open",
            "questions": "yes - direct questions",
            "emojis": "minimal or none",
            "example": "Ask questions to learn more, keep it simple"
        },
        "hopeful": {
            "length": "medium",
            "style": "optimistic, warm, tentative",
            "questions": "yes - gentle inquiries",
            "emojis": "appropriate, 1 max",
            "example": "Express optimism about connection, suggest possibilities"
        },

        # Neutral emotions
        "neutral": {
            "length": "short to medium",
            "style": "polite but reserved, factual",
            "questions": "optional - if relevant",
            "emojis": "none",
            "example": "Respond appropriately but don't overextend, keep it balanced"
        },
        "thoughtful": {
            "length": "medium",
            "style": "reflective, measured, sincere",
            "questions": "yes - meaningful questions",
            "emojis": "none",
            "example": "Take their point seriously, respond with depth"
        },
        "contemplative": {
            "length": "short to medium",
            "style": "reflective, internal, measured",
            "questions": "minimal",
            "emojis": "none",
            "example": "Share your thoughts but keep some reserve"
        },
        "unsure": {
            "length": "short",
            "style": "hesitant, uncertain, cautious",
            "questions": "maybe - seeking clarity",
            "emojis": "none",
            "example": "Express uncertainty, ask for clarification, be tentative"
        },

        # Negative emotions (critical for realism)
        "annoyed": {
            "length": "short - 1-2 sentences MAX",
            "style": "curt, direct, less warm",
            "questions": "NO - you're not interested in extending this",
            "emojis": "NONE",
            "example": "Keep it brief, no exclamation points, minimal enthusiasm. Example: 'Sure.' or 'That's fine.'"
        },
        "frustrated": {
            "length": "short to medium",
            "style": "direct, firm, possibly sharp",
            "questions": "only if challenging them",
            "emojis": "NONE",
            "example": "Be direct about the issue, don't sugarcoat. Example: 'I don't think that's what I meant.'"
        },
        "bored": {
            "length": "very short - 1 sentence",
            "style": "generic, minimal effort, disengaged",
            "questions": "NO - you're not invested",
            "emojis": "NONE",
            "example": "Give bare minimum response. Example: 'Cool.' or 'Yeah, I guess.'"
        },
        "disappointed": {
            "length": "short",
            "style": "subdued, less enthusiastic, distant",
            "questions": "minimal - low engagement",
            "emojis": "NONE",
            "example": "Show lack of enthusiasm, pull back. Example: 'Oh. That's different than I expected.'"
        },
        "offended": {
            "length": "short to medium",
            "style": "firm, clear boundaries, possibly cold",
            "questions": "NO - you're addressing the offense",
            "emojis": "NONE",
            "example": "Call out the behavior, set boundaries. Example: 'I don't appreciate that comment.'"
        },
        "unimpressed": {
            "length": "very short",
            "style": "neutral to slightly dismissive",
            "questions": "NO",
            "emojis": "NONE",
            "example": "Minimal response, move on. Example: 'Okay.' or 'I see.'"
        },
        "confused": {
            "length": "short",
            "style": "uncertain, seeking clarity",
            "questions": "yes - asking for explanation",
            "emojis": "NONE",
            "example": "Express confusion, ask for clarification. Example: 'Wait, what do you mean?'"
        },
        "irritated": {
            "length": "short",
            "style": "terse, impatient, direct",
            "questions": "NO",
            "emojis": "NONE",
            "example": "Be brief and less warm. Example: 'Fine.' or 'Whatever works.'"
        },
        "skeptical": {
            "length": "short to medium",
            "style": "questioning, doubtful, reserved",
            "questions": "yes - challenging questions",
            "emojis": "NONE",
            "example": "Express doubt politely. Example: 'I'm not sure I agree with that.'"
        },
        "angry": {
            "length": "short to medium",
            "style": "firm, direct, possibly intense",
            "questions": "NO - you're expressing anger",
            "emojis": "NONE",
            "example": "Be very direct, set clear boundaries. Example: 'That's completely unacceptable.'"
        }
    }

    @classmethod
    def get_tone_instruction(cls, emotion: str, fondness_level: int) -> str:
        """
        Generate tone enforcement instruction based on emotion and fondness level
        """
        emotion = emotion.lower()
        rule = cls.TONE_RULES.get(emotion, cls.TONE_RULES["neutral"])

        # Build tone instruction
        instruction = f"""
⚠️ TONE ENFORCEMENT - Your emotion is '{emotion}':
- Message length: {rule['length']}
- Style: {rule['style']}
- Questions: {rule['questions']}
- Emojis: {rule['emojis']}
- Guideline: {rule['example']}
"""

        # Add fondness-based modifier
        if fondness_level < 30:
            instruction += "\n- Your low fondness (< 30) means you should be LESS engaged, shorter responses, pulling back emotionally"
        elif fondness_level < 50:
            instruction += "\n- Your moderate fondness (30-50) means you're uncertain about them - be measured, not too enthusiastic"

        return instruction

    @classmethod
    def get_previous_context(cls, internal_thought: str, fondness_change: int) -> str:
        """
        Generate context from previous interaction
        """
        if not internal_thought:
            return ""

        context = f"""
PREVIOUS INTERACTION CONTEXT:
- Last time you thought: "{internal_thought}"
- Your fondness changed by {fondness_change:+d}
"""

        if fondness_change < -3:
            context += "- You were put off by them. Be more distant this time.\n"
        elif fondness_change < 0:
            context += "- You were slightly disappointed. Be a bit more reserved.\n"
        elif fondness_change > 5:
            context += "- You were impressed! Show more warmth and interest.\n"
        elif fondness_change > 2:
            context += "- You liked that interaction. Be a bit more engaged.\n"

        return context
