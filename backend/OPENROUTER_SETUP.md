# OpenRouter Setup Guide for Auralie

This project uses **OpenRouter** to access multiple LLM providers through one unified API!

## Why OpenRouter?

- 🌐 **Access to 100+ models** - Llama, Claude, GPT, Gemini, and more
- 💰 **Pay-as-you-go** - No subscriptions, only pay for what you use
- 🔑 **One API key** - Access all models with a single key
- 💳 **$5 free credits** - Great for testing
- 📊 **Usage tracking** - See detailed costs per model
- 🚀 **No rate limits** - (or very generous limits)

## Quick Setup (3 minutes)

### 1. Get Your API Key

1. Go to **https://openrouter.ai**
2. Sign in with Google/GitHub
3. Add credits ($5 minimum, includes $5 free credits)
4. Go to **https://openrouter.ai/keys**
5. Click "Create Key"
6. Copy your key (starts with `sk-or-v1-`)

### 2. Configure Auralie

```bash
# Your .env file is already set up!
# Just add your API key:

OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run!

```bash
cd src
python3 main.py
```

## Available Models

OpenRouter gives you access to ALL major AI models. Here are the best for Auralie:

### Recommended Models (Good Balance)

| Model | Cost/1M tokens | Quality | Speed | Best For |
|-------|----------------|---------|-------|----------|
| `meta-llama/llama-3.1-70b-instruct` | $0.40 | Very Good | Fast | **Default - Best value** |
| `mistralai/mixtral-8x7b-instruct` | $0.24 | Good | Very Fast | Testing/Development |
| `google/gemini-pro-1.5` | $1.25 | Excellent | Fast | Production |

### Premium Models (Highest Quality)

| Model | Cost/1M tokens | Quality | Speed | Best For |
|-------|----------------|---------|-------|----------|
| `anthropic/claude-3.5-sonnet` | $3.00 | Excellent | Medium | Best personality simulation |
| `openai/gpt-4-turbo` | $10.00 | Excellent | Medium | Highest quality output |
| `openai/gpt-4o` | $5.00 | Excellent | Fast | Best GPT-4 value |

### Budget Models (Development)

| Model | Cost/1M tokens | Quality | Speed | Best For |
|-------|----------------|---------|-------|----------|
| `meta-llama/llama-3.1-8b-instruct` | $0.06 | Good | Very Fast | Quick testing |
| `mistralai/mistral-7b-instruct` | $0.06 | Good | Very Fast | Bulk simulations |

## Cost Estimates

Each 7-day simulation uses approximately **3,000-5,000 tokens** per model call, with **30-40 calls total**.

### Per Simulation Cost

| Model | Tokens/Sim | Cost/Sim | Sims/$5 |
|-------|-----------|----------|---------|
| Llama 3.1 70B | ~120K | **$0.05** | **100** |
| Mixtral 8x7B | ~120K | **$0.03** | **166** |
| Claude 3.5 Sonnet | ~120K | **$0.36** | **14** |
| GPT-4 Turbo | ~120K | **$1.20** | **4** |

**Example:** With $5 credits + $5 free = $10 total
- **Llama 3.1 70B**: ~200 simulations
- **Claude 3.5 Sonnet**: ~28 simulations
- **GPT-4 Turbo**: ~8 simulations

## Switching Models

Just change the model in your `.env` file:

```bash
# Budget testing
OPENROUTER_MODEL=mistralai/mixtral-8x7b-instruct

# Balanced (default)
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct

# High quality
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Maximum quality
OPENROUTER_MODEL=openai/gpt-4-turbo
```

No code changes needed!

## Features & Benefits

### No Rate Limits
Unlike Groq (100K tokens/day), OpenRouter has generous limits:
- Most models: **Unlimited** with credits
- Some premium models: 200+ requests/minute

### Access to Premium Models
Want to try Claude 3.5 Sonnet or GPT-4? Just change the model name:
```bash
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### Detailed Cost Tracking
View usage at: **https://openrouter.ai/activity**
- See cost per request
- Track which models you use most
- Monitor remaining credits

### Fallback Models
If one model is down, easily switch to another:
```bash
# Primary model down? Switch instantly
OPENROUTER_MODEL=google/gemini-pro-1.5
```

## Best Practices

### For Development/Testing
```env
OPENROUTER_MODEL=mistralai/mixtral-8x7b-instruct
```
- Fast iterations
- Low cost ($0.03/simulation)
- Test 100+ times on $5

### For Quality Results
```env
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```
- Great personality accuracy
- Good value ($0.05/simulation)
- Production-ready quality

### For Best Quality
```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```
- Most realistic conversations
- Best emotional nuance
- Worth it for final demos

## Troubleshooting

### "Invalid API key"
- Make sure key starts with `sk-or-v1-`
- Check for extra spaces in `.env`
- Regenerate key at https://openrouter.ai/keys

### "Insufficient credits"
- Check balance: https://openrouter.ai/credits
- Add more credits (minimum $5)
- Free credits are automatically applied

### "Model not found"
- Check model name at: https://openrouter.ai/models
- Ensure exact spelling (case-sensitive)
- Some models require special access

### Slow responses
- Some models are slower than others
- Try switching to faster model:
  ```bash
  OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
  ```

## Comparing to Groq

| Feature | Groq | OpenRouter |
|---------|------|------------|
| **Models** | Llama, Mixtral only | 100+ models (all providers) |
| **Cost** | Free (with limits) | Pay-as-you-go ($0.03-$10/M tokens) |
| **Rate Limits** | 100K tokens/day | Unlimited (with credits) |
| **Quality** | Good | Good to Excellent (model dependent) |
| **Speed** | Ultra-fast | Fast to medium |
| **Best For** | Testing, prototypes | Production, flexibility |

## Migration from Groq

Already have Groq experience? Here's the mapping:

| Groq Model | OpenRouter Equivalent |
|------------|-----------------------|
| `llama-3.1-70b-versatile` | `meta-llama/llama-3.1-70b-instruct` |
| `llama-3.1-8b-instant` | `meta-llama/llama-3.1-8b-instruct` |
| `mixtral-8x7b-32768` | `mistralai/mixtral-8x7b-instruct` |

## Example .env File

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-1234567890abcdefghijklmnopqrstuv
LLM_PROVIDER=openrouter

# Choose your model (change anytime!)
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct

# Optional: Your app name (for stats)
OPENROUTER_APP_NAME=Auralie
```

## Resources

- **Get API Key**: https://openrouter.ai/keys
- **Browse Models**: https://openrouter.ai/models
- **View Usage**: https://openrouter.ai/activity
- **Add Credits**: https://openrouter.ai/credits
- **Documentation**: https://openrouter.ai/docs
- **Pricing**: https://openrouter.ai/models (click any model)

## Summary

✅ **Switched from Groq to OpenRouter**
- More models available
- Pay-as-you-go (no daily limits)
- Access to Claude, GPT-4, Gemini, and more
- Only pay for what you use

🎯 **Recommended Settings:**
```env
OPENROUTER_API_KEY=your_actual_key
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```

💰 **Cost:** ~$0.05 per simulation (with Llama 3.1 70B)
🚀 **Get Started:** https://openrouter.ai

---

**Ready to simulate?** Add your API key to `.env` and run `python3 src/main.py`!
