# Understanding Groq Rate Limits

## Your Current Limit

You're on the **free tier** with these limits:
- **100,000 tokens per day**
- **30 requests per minute**

## How Much Does a Simulation Use?

Each complete 7-day simulation typically uses:
- **~30-40 API requests**
- **~3,000-5,000 tokens** (with llama-3.3-70b-versatile)

This means you can run approximately **20-30 simulations per day** on the free tier.

## Your Error Explained

```
Rate limit reached for model `llama-3.3-70b-versatile`
Limit 100000, Used 99998, Requested 332
```

You've used 99,998 out of 100,000 tokens today! Almost maxed out.

**Solution:** Wait 4-5 minutes (as mentioned in error), or try tomorrow.

## Recommendations for Testing

### Option 1: Use Smaller Model (Recommended for Testing)

Edit your `.env` file:
```bash
GROQ_MODEL=llama-3.1-8b-instant
```

**Benefits:**
- Uses **~50% fewer tokens** per simulation
- **2-3x faster** responses
- Still produces good quality results
- Can run **40-60 simulations/day** instead of 20-30

### Option 2: Run Fewer Simulations

```bash
# Run just 1 simulation (default now)
python main.py

# Or specify:
python main.py batch 1
```

The system now:
- Defaults to **1 simulation** instead of 5
- Adds **10-second delays** between simulations
- **Saves progress** every 2 days
- **Saves partial results** if it fails

### Option 3: Wait and Retry

Your token limit resets every 24 hours. Check when your limit resets at:
https://console.groq.com/usage

## Checking Your Usage

Monitor your usage in real-time:
1. Go to https://console.groq.com/usage
2. See tokens used today
3. Plan your simulations accordingly

## Best Practices

### For Quick Testing
```bash
# .env file
GROQ_MODEL=llama-3.1-8b-instant

# Terminal
python main.py batch 1
```
**Result:** Fast, low-cost testing

### For Quality Results
```bash
# .env file
GROQ_MODEL=llama-3.3-70b-versatile

# Terminal
python main.py batch 1
```
**Result:** Best quality, but uses more tokens

### For Maximum Simulations
```bash
# .env file
GROQ_MODEL=llama-3.1-8b-instant

# Terminal
python main.py batch 10
```
**Result:** Run many simulations quickly (stay under daily limit)

## Token Usage by Model

| Model | Tokens/Simulation | Simulations/Day (100k limit) |
|-------|-------------------|------------------------------|
| llama-3.3-70b-versatile | ~4,000-5,000 | 20-25 |
| llama-3.1-70b-versatile | ~3,500-4,500 | 22-28 |
| llama-3.1-8b-instant | ~2,000-3,000 | 33-50 |
| mixtral-8x7b-32768 | ~3,000-4,000 | 25-33 |

## File Saving Improvements

The system now saves:
1. ✅ **Progress every 2 days** - won't lose all data if it fails
2. ✅ **Partial results** - even failed simulations save what completed
3. ✅ **Both JSON and text** - easier to review results
4. ✅ **Status tracking** - see if simulation completed or failed

Check your saved files:
```bash
ls simulations/    # JSON data
ls output/         # Readable text
```

## Upgrading (If Needed)

If you need more tokens:
- **Dev Tier**: Higher limits, minimal cost
- Go to: https://console.groq.com/settings/billing

But for MVP testing, the **free tier is usually enough!**

## Quick Commands Reference

```bash
# Check what model you're using
cat .env | grep GROQ_MODEL

# Switch to faster model
echo "GROQ_MODEL=llama-3.1-8b-instant" >> .env

# Run single simulation
cd src && python main.py batch 1

# View saved simulations
ls -lh ../simulations/
ls -lh ../output/

# Check file contents
cat ../simulations/*.json | grep "status"
```

## Summary

**What happened:** You hit the daily 100k token limit
**Quick fix:** Use `llama-3.1-8b-instant` model
**Long-term:** System now saves progress and uses fewer tokens by default

**Next steps:**
1. Wait 4-5 minutes (or until tomorrow)
2. OR switch to `llama-3.1-8b-instant` in `.env`
3. Run `python main.py batch 1`
4. Check `simulations/` and `output/` folders for saved files
