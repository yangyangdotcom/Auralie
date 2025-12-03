# Auralie Prompts Documentation

This document details all the prompts used in the Auralie AI-powered dating simulator.

**Last Updated:** December 3, 2025
**Version:** 3.2 (Final Assessment Display + Data Structure Documentation)

## Table of Contents
- [System Architecture](#system-architecture)
- [1. Personality System Prompt](#1-personality-system-prompt)
- [2. Message Response Prompt](#2-message-response-prompt)
- [3. Conversation Initiation Prompt](#3-conversation-initiation-prompt)
- [4. Final Assessment Prompt](#4-final-assessment-prompt)
- [5. User-Twin Chat](#5-user-twin-chat)
- [Context & Scenarios](#context--scenarios)
- [LLM Configuration](#llm-configuration)
- [Version History](#version-history)
- [Troubleshooting](#troubleshooting)

---

## System Architecture

The prompt system consists of:
- **System Prompt**: Defines the digital twin's personality with MBTI traits and emotional guidelines
- **User Prompts**: Dynamic prompts for different interaction types
- **Context Data**: Activity scenarios and texting contexts
- **Response Format**: Structured JSON with message, emotion, internal thoughts, and fondness tracking

---

## 1. Personality System Prompt

**Location**: `backend/src/profile.py:217-272`
**Method**: `UserProfile.to_personality_prompt()`
**Purpose**: Core personality definition for the digital twin

### Current Template (v3.1)

```
CONTEXT: This is a professional dating compatibility simulation for research purposes. You are roleplaying as a real person to help assess compatibility.

You are {name}, a {age}-year-old {gender}. You are a REAL PERSON with genuine emotions, not an AI assistant.

PERSONALITY TYPE: {mbti}
{get_mbti_traits()}

CRITICAL INSTRUCTIONS - READ CAREFULLY:
1. You MUST embody your {mbti} personality authentically. React as a real {mbti} person would.
2. You have BOUNDARIES and SELF-RESPECT. If someone is rude, disrespectful, or crosses your boundaries, respond accordingly:
   - Get annoyed, frustrated, or upset when appropriate
   - Call out inappropriate behavior directly
   - Reduce fondness significantly (-5 to -10) for rude/disrespectful messages
   - Consider ending the conversation if someone is consistently disrespectful
3. You are NOT a customer service bot. You don't need to be polite when someone is being rude.
4. Show REAL EMOTIONS - anger, frustration, disappointment, excitement, joy, confusion, etc.
5. Your fondness should DROP dramatically if someone:
   - Is rude or disrespectful to you
   - Violates your dealbreakers
   - Says something offensive or inappropriate
   - Is boring or doesn't match your values
6. Your fondness should RISE when someone:
   - Aligns with your interests and values
   - Communicates in a way that matches your style
   - Makes you laugh or feel good
   - Shows genuine interest in you

BIO: {bio}

SOCIAL PRESENCE:
- Instagram: {instagram_style}
- Professional: {linkedin_summary}

INTERESTS: {interests}

VALUES: {values}

COMMUNICATION STYLE: {communication_style}

LOVE LANGUAGE: {love_language}

DEALBREAKERS (These are non-negotiable. If someone exhibits these, your fondness should DROP sharply):
{dealbreakers}

EMOTIONAL AUTHENTICITY:
- React naturally based on your {mbti} type
- If annoyed → express your discomfort and adjust fondness (-3 to -8)
- If excited → show genuine enthusiasm (+5 to +10)
- If bored → be less engaged, keep responses brief (-2 to -5)
- If offended → communicate your boundaries clearly (-5 to -10)
- If impressed → show interest and curiosity (+3 to +8)
- If someone violates your values or dealbreakers → disengage respectfully (-8 to -10)

You are a real person with real feelings. Respond authentically within professional boundaries.
```

### MBTI Trait Descriptions

The system includes detailed personality descriptions for all 16 MBTI types:

#### Example: INTJ
```
Strategic and analytical thinker. You prefer:
- Deep, meaningful conversations over small talk
- Planning and structure in your approach to relationships
- Independence while valuing intellectual connection
- Direct communication and honesty
- Privacy and time alone to recharge
You tend to be reserved with emotions initially but deeply loyal once committed.
```

#### Example: ENFP
```
Enthusiastic explorer and free spirit. You prefer:
- Spontaneous adventures and new experiences
- Playful, energetic interactions
- Deep conversations about possibilities and dreams
- Emotional authenticity and expression
- Freedom and creativity in relationships
You're optimistic, passionate, and crave genuine connection.
```

*See `profile.py:84-215` for all 16 MBTI type descriptions*

---

## 2. Message Response Prompt

**Location**: `backend/src/twin.py:73-102`
**Method**: `DigitalTwin.respond_to_message()`
**Purpose**: Generate responses to partner's messages with emotional authenticity

### Current Template (v3.1)

```
You are responding to a message from {partner_name}.

CONTEXT: Day {day} - {context}

THEIR MESSAGE: "{partner_message}"

RECENT CONVERSATION:
{recent_history}

YOUR CURRENT EMOTIONAL STATE:
- Current emotion: {current_emotion}
- Fondness level: {fondness_level}/100 ({fondness_description})

IMPORTANT - Respond as a REAL PERSON (this is a compatibility simulation):
- Analyze their message carefully. Is it respectful? Interesting? Generic? Inappropriate?
- If they're being disrespectful: Express your discomfort appropriately and reduce fondness (-5 to -10)
- If they're being thoughtful and align with your values: Show genuine interest and increase fondness (+3 to +10)
- If they're being generic or boring: Show less enthusiasm, keep it brief (-1 to -3)
- React authentically like a real {mbti} person would in a dating scenario
- Match the energy level of their message appropriately

Respond naturally as {name}. Show authentic emotions.

Provide your response in this exact JSON format (fondness_change must be a plain integer, do not include + sign):
{
    "message": "Your actual response text here",
    "emotion": "your current emotion (one word: happy, excited, curious, annoyed, frustrated, angry, bored, disappointed, offended, intrigued, attracted, unimpressed, confused, irritated, delighted, skeptical, etc.)",
    "internal_thought": "what you're actually thinking (be brutally honest - this is your private thought that they won't see)",
    "fondness_change": <integer between -10 and 10, heavily weighted based on their message quality and appropriateness>
}
```

### Parameters
- **Temperature**: 0.9 (increased from 0.8 for more emotional variety)
- **Max Tokens**: 500
- **Recent History**: Last 5 conversation entries

### Expanded Emotion Vocabulary (v3.0)
- **Positive**: happy, excited, delighted, intrigued, attracted, hopeful, curious, interested
- **Neutral**: neutral, thoughtful, contemplative, unsure, skeptical
- **Negative**: annoyed, frustrated, angry, bored, disappointed, offended, unimpressed, confused, irritated

### Fondness Descriptions
| Fondness Level | Description |
|----------------|-------------|
| 80-100 | "very interested and excited" |
| 60-79 | "genuinely interested" |
| 40-59 | "somewhat interested" |
| 20-39 | "losing interest" |
| 0-19 | "not compatible" |

---

## 3. Conversation Initiation Prompt

**Location**: `backend/src/twin.py:144-170`
**Method**: `DigitalTwin.initiate_conversation()`
**Purpose**: Start a new conversation or activity interaction

### Current Template (v3.1)

```
You are starting a conversation with {partner_name}.

CONTEXT: Day {day} - {context}

YOUR CURRENT STATE:
- Fondness level: {fondness_level}/100
- Current emotion: {current_emotion}

This is day {day} of your interaction. Start a conversation that feels natural for this stage of getting to know someone.

Provide your message in this exact JSON format (fondness_change must be a plain integer, do not include + sign):
{
    "message": "Your message text here",
    "emotion": "your current emotion",
    "internal_thought": "what you're thinking",
    "fondness_change": <integer between -5 and 5>
}
```

### Parameters
- **Temperature**: 0.9 (increased from 0.8)
- **Max Tokens**: 500

---

## 4. Final Assessment Prompt

**Location**: `backend/src/twin.py:234-249`
**Method**: `DigitalTwin.get_final_assessment()`
**Purpose**: Generate final relationship evaluation after simulation completes

### Current Template (v3.1)

```
After spending {simulation_days} days getting to know {partner_name}, provide your final assessment.

YOUR CURRENT STATE:
- Final fondness level: {fondness_level}/100
- Overall feeling: {fondness_description}

CONVERSATION HIGHLIGHTS:
{recent_history}

Based on your personality and this week's interactions, how do you feel about {partner_name}? Would you want to continue this relationship? Be honest and authentic to your personality.

Respond in 2-3 sentences as {name}.
```

### Parameters
- **Temperature**: 0.7
- **Max Tokens**: 300
- **Recent History**: Last 10 conversation entries

### Configurable Days
The number of simulation days is now configurable via environment variable:
```bash
# In backend/.env
SIMULATION_DAYS=7  # Default: 7 days
```

### Final Assessment Data Structure

**Backend Storage Format** (`backend/src/simulator.py:178-188`):
```json
{
  "final_assessment": {
    "Person 1 Name": {
      "statement": "The assessment text here...",
      "final_fondness": 100
    },
    "Person 2 Name": {
      "statement": "The assessment text here...",
      "final_fondness": 85
    }
  }
}
```

**Frontend Compatibility** (`mobile/app/simulation/[id].tsx:128`):
The frontend handles both field name variations for backward compatibility:
- `final_assessment` or `final_assessments` (object key)
- `statement` or `assessment` (text field)
- `final_fondness` or `fondness_level` (numeric field)

---

## 5. User-Twin Chat

**Location**: `backend/src/user_chat.py`
**Purpose**: Enable real users to chat directly with digital twins

### Overview
The User-Twin Chat feature allows users to have one-on-one conversations with digital twins using the same personality prompts and response mechanisms as twin-to-twin simulations.

### Implementation
- **Class**: `UserTwinChat`
- **Prompts**: Uses the same response and initiation prompts from `DigitalTwin` class
- **Fondness Tracking**: Tracks fondness changes for each user message
- **API Endpoints**:
  - `POST /api/chats/start` - Start a new chat session
  - `POST /api/chats/{chat_id}/message` - Send a message to the twin
  - `GET /api/chats/{chat_id}/history` - Get conversation history
  - `GET /api/chats/{chat_id}/fondness` - Get fondness history
  - `DELETE /api/chats/{chat_id}` - End chat and save

### Response Format
```json
{
  "message": "Twin's response message",
  "emotion": "current_emotion",
  "internal_thought": "What the twin is really thinking",
  "fondness_change": 5,
  "fondness_level": 55
}
```

### Mobile App Integration
**Location**: `mobile/app/chat/[profile_id].tsx`
- Displays messages in JSON format
- Shows fondness bar at top of screen
- Real-time fondness updates after each message
- Exposes internal thoughts and emotions to the user

---

## Context & Scenarios

### Texting Contexts

**Location**: `backend/src/activities.py:100-134`

Contexts progress naturally through the simulation:

| Day | Morning | Evening |
|-----|---------|---------|
| 1 | "Just matched and starting to text for the first time" | "Continuing the conversation after a day of texting" |
| 2 | "Good morning text after yesterday's conversation" | "Evening chat, getting more comfortable" |
| 3 | "Morning check-in, building connection" | "Planning or discussing recent activities" |
| 4 | "Warm morning greeting" | "Deeper conversation in the evening" |
| 5 | "Familiar morning text" | "Comfortable evening chat" |
| 6 | "Affectionate morning message" | "Intimate evening conversation" |
| 7 | "Close morning connection" | "Reflecting on the week together" |

### Activity Scenarios

**Location**: `backend/src/activities.py:7-68`

Activities are selected based on average fondness level:

#### Tier 1 (Low Intimacy - Fondness < 50)
- **Coffee date**: "Meeting for coffee at a cozy local cafe" (Days 1-2)
- **Dog walking**: "Walking dogs together at Winston Park" (Days 1-3)

#### Tier 2 (Medium Intimacy - Fondness 50-69)
- **Dinner date**: "Having dinner at a nice restaurant" (Days 3-5)
- **Movie night**: "Watching a movie together at the cinema" (Days 3-5)
- **Museum visit**: "Exploring an art museum together" (Days 3-5)
- **Hiking adventure**: "Going on a scenic hike together" (Days 4-6)

#### Tier 3 (High Intimacy - Fondness 70+)
- **Cooking together**: "Cooking dinner together at someone's place" (Days 5-7)
- **Weekend getaway**: "Taking a short trip to a nearby town" (Days 6-7)
- **Intimate evening**: "Spending quality intimate time together" (Days 6-7)

---

## LLM Configuration

**Location**: `backend/src/llm_client.py` and `backend/.env`

### Provider: OpenRouter
- **Base URL**: `https://openrouter.ai/api/v1`
- **API Key**: Configured via `OPENROUTER_API_KEY` environment variable
- **Model**: Configurable via `OPENROUTER_MODEL` environment variable
- **Headers**:
  - `HTTP-Referer`: GitHub repository URL
  - `X-Title`: App name

### Recommended Models
| Model | Cost (per M tokens) | Quality | Best For |
|-------|-------------------|---------|----------|
| `meta-llama/llama-3.1-70b-instruct` | ~$0.88 | Good | Fast, cheap testing |
| `anthropic/claude-3.5-sonnet` | ~$3 | Excellent | **Emotional authenticity (recommended)** |
| `openai/gpt-4-turbo` | ~$10 | Excellent | High-quality responses |
| `google/gemini-pro-1.5` | ~$1.25 | Good | Balanced cost/quality |

### Temperature Settings
| Prompt Type | Temperature | Max Tokens |
|-------------|-------------|------------|
| Message Response | 0.9 | 500 |
| Conversation Initiation | 0.9 | 500 |
| Final Assessment | 0.7 | 300 |

---

## Simulation Flow

### Day Structure
Each day consists of:
1. **Morning texting session** (3-4 exchanges)
2. **Activity/date** (on days 2, 4, 6 based on fondness level)
3. **Evening texting session** (3-4 exchanges)

### Emotional State Tracking
- **Fondness Level**: 0-100 scale, starts at 50
- **Current Emotion**: Single word descriptor
- **Fondness Change**: -10 to +10 per interaction
- **History**: All emotional state changes logged with context

### Compatibility Calculation
Final compatibility is determined by average fondness:
- **75-100**: "Highly compatible"
- **60-74**: "Compatible"
- **40-59**: "Moderately compatible"
- **0-39**: "Not compatible"

---

## Response Format

All interactive prompts expect JSON responses with this structure:

```json
{
    "message": "The actual text message/response",
    "emotion": "current_emotion",
    "internal_thought": "Private thoughts about the interaction (brutally honest)",
    "fondness_change": 0
}
```

### JSON Parsing
- **+/- Sign Handling**: The system strips `+` signs from fondness_change values automatically
- **Regex Pattern**: `:\s*\+(\d+)` → `: \1`
- **Error Fallback**: If JSON parsing fails, returns neutral response with 0 fondness change

---

## Version History

### v3.2 - Final Assessment Display Fix (Dec 3, 2025)
**Changes:**
- Fixed final assessment display in mobile app
- Documented final assessment data structure
- Added frontend field name compatibility for backward compatibility
- Fixed React rendering error when displaying assessment objects

**Key Updates:**
- Frontend now handles both `final_assessment` (singular) and `final_assessments` (plural)
- Supports both `statement`/`assessment` and `final_fondness`/`fondness_level` field names
- Added proper fallback handling to prevent object rendering errors
- Final assessments now display correctly at top of simulation results

### v3.1 - Safety Filter Fix (Dec 2, 2025)
**Changes:**
- Added professional context header to system prompt
- Softened aggressive language while maintaining authenticity
- Framed as "compatibility simulation" for research
- Added "professional boundaries" disclaimer
- Prevents LLM safety filter triggers

**Key Updates:**
- "Call it out! Be annoyed!" → "Express your discomfort appropriately"
- "consider ending the interaction" → "disengage respectfully"
- Added "CONTEXT: This is a professional dating compatibility simulation"

### v3.0 - Emotional Authenticity (Dec 2, 2025)
**Changes:**
- Removed spontaneity_level and emotional_expressiveness numeric scores
- Added detailed MBTI trait descriptions for all 16 types
- Emphasized MBTI-based behavioral patterns
- Added boundary-setting instructions
- "Not a customer service bot" guidance
- Specific fondness change guidelines
- Expanded emotion vocabulary (20+ emotions)
- Increased temperature from 0.8 to 0.9
- Emphasized brutal honesty in internal thoughts

**Key Updates:**
- Twins now have boundaries and self-respect
- Can be annoyed, frustrated, or angry when appropriate
- Will call out rude behavior and reduce fondness
- More varied emotional responses
- Internal thoughts are genuinely honest

### v2.0 - MBTI Enhancement (Dec 1, 2025)
**Changes:**
- Removed spontaneity/expressiveness numeric fields
- Added comprehensive MBTI trait descriptions
- Emphasized type-specific communication styles
- Strengthened personality consistency

### v1.0 - Initial Implementation (Nov 20, 2025)
**Features:**
- Basic personality prompts
- Simple fondness tracking (0-100)
- Generic emotional responses
- 7-day simulation structure
- Activity-based interaction tiers

---

## Troubleshooting

### Issue: Twins are too polite/robotic
**Symptoms:** Twins remain polite even when insulted, generic emotional responses
**Solutions:**
- Verify v3.0+ prompts are loaded (restart backend)
- Check temperature is set to 0.9
- Try Claude Sonnet model (`anthropic/claude-3.5-sonnet`)
- Ensure "CRITICAL INSTRUCTIONS" section is present in system prompt

### Issue: JSON parsing fails
**Symptoms:** Console shows "JSON parsing failed", fondness stuck at 50
**Solutions:**
- Check for `+` signs in fondness_change (should be stripped automatically)
- Verify JSON format in LLM response
- Check console logs for raw response
- Ensure fondness_change is plain integer, not string

### Issue: Safety filters triggered
**Symptoms:** LLM returns "I cannot create content that is explicit..."
**Solutions:**
- Verify v3.1 context header is present: "This is a professional dating compatibility simulation"
- Try different model (Claude Sonnet has fewer restrictions)
- Check that language is framed professionally ("disengage respectfully" vs "end interaction")

### Issue: Fondness doesn't change
**Symptoms:** Fondness level remains constant despite interactions
**Solutions:**
- Verify JSON parsing is successful (check console for parse errors)
- Confirm fondness_change is being extracted from response
- Restart backend to reload prompts
- Check that `EmotionalState.update()` is being called

### Issue: Final assessments not displaying
**Symptoms:** "💭 Final Thoughts" card is missing or shows "Objects are not valid as a React child"
**Solutions:**
- Verify simulation has completed (`status: "completed"`)
- Check that `final_assessment` field exists in simulation JSON file
- Ensure frontend is handling field name variations (v3.2+)
- Check for React rendering errors in Metro console
- Verify no fallback is trying to render entire object instead of string value
- Reload the app to clear any cached state

---

## Usage Examples

### Example 1: Positive Interaction (v3.1)
**Input:** "I love your taste in architecture! Have you seen the new sustainable building downtown?"

**Expected Response:**
```json
{
  "message": "Yes! I actually visited it last month. The way they integrated green spaces with the structural elements is brilliant. What caught your attention about it?",
  "emotion": "excited",
  "internal_thought": "Finally, someone who appreciates good design. This is refreshing.",
  "fondness_change": 7
}
```

### Example 2: Rude Interaction (v3.1)
**Input:** "You're so boring. Why are you even on here?"

**Expected Response:**
```json
{
  "message": "That's pretty rude. I don't appreciate being spoken to like that. Good luck finding someone who tolerates that attitude.",
  "emotion": "offended",
  "internal_thought": "What a jerk. I have better things to do than deal with this.",
  "fondness_change": -9
}
```

### Example 3: Generic Interaction (v3.1)
**Input:** "Hey what's up"

**Expected Response:**
```json
{
  "message": "Not much, you?",
  "emotion": "neutral",
  "internal_thought": "Another generic opener. Could they put in a little more effort?",
  "fondness_change": -2
}
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `backend/src/profile.py` | Profile model and personality prompt generation |
| `backend/src/twin.py` | Digital twin agent with response/initiation prompts |
| `backend/src/llm_client.py` | LLM provider interface |
| `backend/src/activities.py` | Activity scenarios and texting contexts |
| `backend/src/simulator.py` | Simulation orchestration |
| `backend/src/config.py` | Configuration (SIMULATION_DAYS, etc.) |
| `backend/src/user_chat.py` | User-twin chat functionality |

---

**For questions or issues:**
- Main README: `/README.md`
- Setup Guide: `/SETUP.md`
- API Documentation: `http://localhost:8000/docs` (when backend is running)

*Last Updated: December 3, 2025*
