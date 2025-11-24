# Auralie - Quick Start Guide

Get your first simulation running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- An OpenRouter API key (get at https://openrouter.ai/keys)
- $5 minimum credits ($5 free credits included = $10 total)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - For OpenRouter API (100+ models)
- `python-dotenv` - For environment variables
- `pydantic` - For data validation

### 2. Configure API Key

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-xxxxx
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```

**Get your API key at:** https://openrouter.ai/keys

**Available models:**
- `meta-llama/llama-3.1-70b-instruct` - Best value (recommended)
- `anthropic/claude-3.5-sonnet` - Highest quality
- `mistralai/mixtral-8x7b-instruct` - Budget option

### 3. Verify Setup

```bash
python test_setup.py
```

This checks:
- All dependencies are installed
- Project structure is correct
- Modules import successfully
- API key is configured

### 4. Run Your First Simulation

```bash
cd src
python main.py
```

This will:
1. Create 10 diverse sample profiles
2. Randomly pair them up
3. Run 5 complete 7-day simulations
4. Save results to `simulations/` and `output/`

Expected runtime: 5-10 minutes per simulation (depends on LLM API speed)

## Understanding the Output

Each simulation creates two files:

### 1. JSON Data (`simulations/`)
Raw simulation data with all interactions, emotions, and metadata:
```
simulations/David_Chen_Clare_Martinez_20250120_143022.json
```

### 2. Readable Output (`output/`)
Formatted text showing conversations and outcomes:
```
output/David_Chen_Clare_Martinez_20250120_143022.txt
```

Example output:
```
DAY 1 - Texting each other
[David]: Hi Clare, nice to meet you. Your profile is interesting!
    💭 She seems genuine, excited to learn more — feeling curious

[Clare]: Hi David! What caught your attention?
    💭 He seems thoughtful with his opener — feeling interested

...

VIRTUAL DATING OUTCOME
Overall Compatibility: Highly compatible (82.5/100)

[David]: I feel like Clare really gets me. Can't wait to meet in person!
    Final fondness level: 85/100
```

## Other Commands

**Run specific number of simulations:**
```bash
python main.py batch 10
```

**Choose specific profiles to pair:**
```bash
python main.py interactive
```

**Just create sample profiles:**
```bash
python main.py create-profiles
```

## Customizing Profiles

### Method 1: Edit JSON Files

After creating sample profiles, edit them in `profiles/`:
```bash
cd profiles
# Edit any .json file
```

### Method 2: Python Code

Create `custom_profiles.py`:
```python
from profile import UserProfile, Gender, MBTIType

my_profile = UserProfile(
    name="Your Name",
    age=28,
    gender=Gender.FEMALE,
    mbti=MBTIType.INFJ,
    bio="Your bio here",
    instagram_style="your ig vibe",
    linkedin_summary="your professional summary",
    interests=["interest1", "interest2", "interest3"],
    values=["value1", "value2"],
    love_language="quality time",
    dealbreakers=["dealbreaker1"],
    communication_style="your style",
    spontaneity_level=7,
    emotional_expressiveness=6
)

my_profile.save()
```

Run it:
```bash
python custom_profiles.py
```

## Troubleshooting

**Import errors:**
```bash
pip install -r requirements.txt
```

**API key not working:**
- Check the key is correct in `.env`
- Verify you have credits (check https://openrouter.ai/credits)
- Make sure LLM_PROVIDER is set to `openrouter`
- Ensure your key starts with `sk-or-v1-`

**Simulation takes too long:**
- Each simulation should take 3-7 minutes
- If slower, try a faster model: `mistralai/mixtral-8x7b-instruct`
- Reduce number of simulations for testing: `python main.py batch 1`

**JSON parsing errors:**
- LLM sometimes returns non-JSON
- System has fallback handling
- Try switching to `meta-llama/llama-3.1-70b-instruct`

**Insufficient credits:**
- Add more credits at https://openrouter.ai/credits
- Check usage at https://openrouter.ai/activity
- Minimum purchase: $5 (+ $5 free = $10 total)

## API Costs

OpenRouter offers **pay-as-you-go pricing** with access to 100+ models!

**OpenRouter (Llama 3.1 70B):**
- ~30-40 API calls per simulation
- ~100,000-150,000 tokens total
- Cost: **~$0.05 per simulation**
- $10 credits ($5 purchase + $5 free) = **~200 simulations**

**Why OpenRouter is great for this project:**
- 🌐 Access to 100+ models (Claude, GPT-4, Gemini, Llama, etc.)
- 💰 Pay only for what you use
- 🚫 No rate limits (unlike Groq's 100K tokens/day)
- 🎯 Switch models anytime without code changes
- 📊 Detailed cost tracking per request

**Tip:** Start with Llama 3.1 70B ($0.05/sim), upgrade to Claude 3.5 Sonnet ($0.36/sim) for best quality!

## Next Steps

1. Run your first simulation and review the output
2. Create your own profile
3. Experiment with different personality combinations
4. Adjust activity scenarios in `src/activities.py`
5. Modify simulation logic in `src/simulator.py`
6. Build a web UI (future enhancement!)

## Getting Help

- Check `README.md` for detailed documentation
- Review sample profiles in `src/sample_profiles.py`
- Examine the code - it's well-commented!

Happy simulating! 💕
