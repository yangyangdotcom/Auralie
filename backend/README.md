h# Auralie Backend

Python backend for Auralie digital twin dating simulator.

## Components

1. **Simulation Engine** (`src/`): Core logic for running 7-day simulations
2. **REST API** (`src/api/`): FastAPI server for mobile app
3. **Profiles** (`profiles/`): JSON profile definitions
4. **Output** (`output/`): Simulation results

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt

# Configure
cp .env.example .env
# Add OPENROUTER_API_KEY
```

## Running

### Standalone Simulation
```bash
python src/main.py
```

### API Server
```bash
# Development
python src/api/main.py

# Production (with uvicorn)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# With auto-reload
uvicorn src.api.main:app --reload
```

API will be available at:
- **Endpoint**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   └── main.py           # FastAPI server
│   ├── activities.py         # Activity scenarios
│   ├── config.py             # Configuration
│   ├── llm_client.py         # LLM interface
│   ├── main.py               # CLI entry point
│   ├── models.py             # Data models
│   ├── output_formatter.py   # Result formatting
│   ├── profile.py            # Profile models
│   ├── sample_profiles.py    # Sample data
│   ├── simulator.py          # Simulation engine
│   └── twin.py               # Digital twin agent
├── profiles/                 # Profile JSON files
├── output/                   # Simulation results
├── requirements.txt          # Core dependencies
├── requirements-api.txt      # API dependencies
└── .env                      # Environment config
```

## Creating Profiles

Create JSON files in `profiles/` directory:

```json
{
  "name": "Alex Chen",
  "age": 28,
  "mbti": "INTJ",
  "interests": ["coding", "hiking", "coffee", "books"],
  "values": ["authenticity", "growth", "independence"],
  "spontaneity_level": 5,
  "emotional_expressiveness": 6,
  "bio": "Software engineer who loves the outdoors"
}
```

**Required fields:**
- `name`: Full name (string)
- `age`: Age (number, 18-100)
- `mbti`: Myers-Briggs type (4 letters)
- `interests`: Array of interests
- `values`: Array of core values
- `spontaneity_level`: 1-10 (1=very planned, 10=very spontaneous)
- `emotional_expressiveness`: 1-10 (1=reserved, 10=very expressive)
- `bio`: Optional bio (string)

## API Usage

### Create Profile
```bash
curl -X POST http://localhost:8000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "age": 26,
    "mbti": "ENFP",
    "interests": ["travel", "photography"],
    "values": ["adventure", "creativity"],
    "spontaneity_level": 8,
    "emotional_expressiveness": 9
  }'
```

### Run Simulation
```bash
curl -X POST http://localhost:8000/api/simulations \
  -H "Content-Type: application/json" \
  -d '{
    "profile1_id": "alex_chen",
    "profile2_id": "sarah_johnson"
  }'
```

### Get Results
```bash
curl http://localhost:8000/api/simulations/{simulation_id}
```

## Configuration

### LLM Provider (OpenRouter)

OpenRouter gives you access to 100+ models:
- Default: `meta-llama/llama-3.1-70b-instruct`
- Cost: ~$0.05 per simulation
- No rate limits (with credits)

Alternative models:
- `anthropic/claude-3.5-sonnet` (best quality, higher cost)
- `meta-llama/llama-3.1-8b-instruct` (faster, cheaper)
- `google/gemini-pro-1.5` (good balance)

Update `.env`:
```
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

## Simulation Flow

1. **Load Profiles**: Read two profiles from JSON
2. **Create Twins**: Initialize LLM-powered agents
3. **Day Loop** (7 days):
   - Morning texting (4 exchanges)
   - Physical activity (dinner, hike, etc.)
   - Evening texting (4 exchanges)
4. **Track State**:
   - Fondness level (0-100)
   - Emotions
   - Internal thoughts
5. **Calculate Score**: Average final fondness levels
6. **Save Results**: JSON + human-readable text

## Output Format

### JSON (`output/<id>.json`)
```json
{
  "profile1": {...},
  "profile2": {...},
  "compatibility_score": 75.5,
  "days": [
    {
      "day": 1,
      "interactions": [...],
      "person1_fondness": 58,
      "person2_fondness": 62
    }
  ],
  "completed_days": 7,
  "status": "completed"
}
```

### Text (`output/<id>.txt`)
Human-readable conversation transcript with emotions and thoughts.

## Troubleshooting

### Rate Limit Errors
OpenRouter shouldn't have rate limits with credits. If you see 429 errors:
- Check your OpenRouter account balance
- Switch to a different model
- Add delays between simulations

### Import Errors
Make sure you're in the `backend/` directory when running scripts:
```bash
cd backend
python src/main.py
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn src.api.main:app --port 8001
```

## Testing

```bash
# Test configuration
python test_setup.py

# Test API endpoints
python -m pytest tests/  # (if you have tests)

# Manual test
python src/main.py
```

## Performance

- **Simulation time**: 2-5 minutes per simulation
- **Token usage**: ~50k-100k tokens per simulation
- **Cost**: ~$0.05-0.10 per simulation (with llama-3.1-70b)
- **Concurrent simulations**: Possible, but watch API limits

## Compatibility Insights

Based on testing, compatibility factors:

1. **Shared Foundation (40%)**: Common values and communication styles
2. **Complementary Differences (30%)**: Different MBTI functions, balanced traits
3. **Tension & Challenge (20%)**: Some friction creates growth
4. **Mystery (10%)**: Unpredictability and surprise

**Key Learning**: Being TOO similar = boring. Aim for 70% similar, 30% different.

## Documentation

- `START_HERE.md`: Quick start guide
- `COMPATIBILITY_GUIDE.md`: How compatibility works
- `WHY_ELENA_LEO_FAILED.md`: Case study on "too perfect" matches
- `OPENROUTER_SETUP.md`: LLM configuration
- `QUICKSTART.md`: Step-by-step setup

## Support

For issues, check:
1. Backend logs
2. `.env` configuration
3. OpenRouter API status
4. Profile JSON format
