# Groq Setup Guide for Auralie

This project uses **Groq** for ultra-fast, cost-effective LLM inference!

## Why Groq?

- ⚡ **Blazing fast** - Responses in seconds, not minutes
- 💰 **Free tier** - 14,400 requests/day, 30/minute
- 🎯 **Great quality** - Llama 3.1 70B is comparable to GPT-4
- 🚀 **Perfect for testing** - Iterate quickly without cost concerns

## Quick Setup (3 minutes)

### 1. Get Your API Key

1. Go to https://console.groq.com/keys
2. Sign up (free, no credit card required)
3. Click "Create API Key"
4. Copy your key (starts with `gsk_`)

### 2. Configure Auralie

```bash
# Copy example config
cp .env.example .env

# Edit .env and paste your key
GROQ_API_KEY=gsk_your_actual_key_here
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.1-70b-versatile
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run!

```bash
cd src
python main.py
```

## Available Models

Choose the best model for your needs by setting `GROQ_MODEL` in `.env`:

| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `llama-3.1-70b-versatile` | Production | Fast | Excellent |
| `llama-3.1-8b-instant` | Testing | Very Fast | Good |
| `mixtral-8x7b-32768` | Long context | Fast | Very Good |

**Recommendation:** Start with `llama-3.1-70b-versatile` for best results.

## Rate Limits (Free Tier)

- **Daily**: 14,400 requests
- **Per minute**: 30 requests
- **Tokens per minute**: 30,000

For Auralie:
- Each simulation = ~30-40 requests
- Takes ~3-5 minutes per simulation
- You can run **~350 simulations/day** on free tier! 🎉

## Troubleshooting

**Error: "Invalid API key"**
- Make sure key starts with `gsk_`
- Check for extra spaces in `.env`
- Regenerate key at https://console.groq.com/keys

**Error: "Rate limit exceeded"**
- Free tier: 30 requests/minute
- Wait 60 seconds or reduce simulation count
- Run fewer parallel simulations

**Slow responses**
- Check Groq status: https://status.groq.com
- Try `llama-3.1-8b-instant` for faster (but slightly lower quality) results

**JSON parsing errors**
- Llama sometimes doesn't return perfect JSON
- System has fallback handling built-in
- Usually self-corrects after a few retries

## Cost Comparison

| Provider | Model | Cost/Simulation | Speed |
|----------|-------|-----------------|-------|
| **Groq** | Llama 3.1 70B | **FREE** (or $0.01) | 3-5 min |
| Anthropic | Claude Sonnet | $0.40 | 8-12 min |
| OpenAI | GPT-4 Turbo | $0.50 | 10-15 min |

**Winner:** Groq for MVP testing and development! 🏆

## Advanced: Optimizing for Groq

### Increase Speed
```env
GROQ_MODEL=llama-3.1-8b-instant  # 2x faster
```

### Better Quality
```env
GROQ_MODEL=llama-3.1-70b-versatile  # More nuanced responses
```

### Longer Context
```env
GROQ_MODEL=mixtral-8x7b-32768  # 32k context window
```

## API Usage Tips

1. **Monitor usage**: https://console.groq.com/usage
2. **Check quotas**: https://console.groq.com/settings/limits
3. **Rate limits**: Add delays if hitting 30 req/min limit
4. **Upgrade**: Paid plans available for higher limits

## Example .env File

```bash
# Groq Configuration
GROQ_API_KEY=gsk_1234567890abcdefghijklmnopqrstuv
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.1-70b-versatile
```

## Support

- **Groq Docs**: https://console.groq.com/docs
- **Status Page**: https://status.groq.com
- **Community**: https://groq.com/community

---

**Ready to simulate?** Run `python src/main.py` and watch the magic happen! ✨
