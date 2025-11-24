# Auralie Setup Checklist ✅

## What's Been Done

✅ Project structure created
✅ All core modules implemented
✅ Configured to use Groq (fast + free!)
✅ 10 sample profiles ready
✅ Documentation complete
✅ `.env` file updated for Groq

## What You Need to Do (5 minutes)

### Step 1: Get Groq API Key (2 minutes)

1. Go to **https://console.groq.com/keys**
2. Sign up (free, no credit card)
3. Click "Create API Key"
4. Copy the key (starts with `gsk_`)

### Step 2: Configure API Key (1 minute)

Edit `.env` file and replace:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

With your actual key:
```bash
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup (30 seconds)

```bash
python test_setup.py
```

You should see all green checkmarks ✅

### Step 5: Run First Simulation (1 minute)

```bash
cd src
python main.py
```

This will:
- Create 10 diverse profiles
- Run 5 random simulations
- Save results to `output/` folder
- Take about 15-20 minutes total

## Quick Commands

```bash
# Run 1 simulation (for quick test)
python main.py batch 1

# Run 10 simulations
python main.py batch 10

# Choose specific profiles
python main.py interactive

# Just create profiles
python main.py create-profiles
```

## Expected Output

You'll see:
```
🎭 AURALIE SIMULATION
==========================================
👤 David Chen (ENFP)
💕 Clare Martinez (INFJ)
==========================================

📅 DAY 1
  💬 Morning texting session...
  💬 Evening texting session...

📅 DAY 2
  💬 Morning texting session...
  🎯 Dog walking at the park...
  💬 Evening texting session...
...
```

## Troubleshooting

**"Import error: No module named 'groq'"**
```bash
pip install groq
```

**"GROQ_API_KEY not set"**
- Edit `.env` file
- Add your actual Groq API key

**"Rate limit exceeded"**
- Free tier: 30 requests/minute
- Wait 60 seconds between simulation batches

## Next Steps

1. ✅ Complete setup above
2. 📊 Review simulation outputs in `output/` folder
3. 🎨 Create your own profile
4. 🔧 Customize scenarios in `src/activities.py`
5. 🚀 Build a web UI (future!)

## File Guide

| File | Purpose |
|------|---------|
| `GROQ_SETUP.md` | Detailed Groq setup guide |
| `QUICKSTART.md` | 5-minute quick start |
| `README.md` | Full documentation |
| `CHANGES.md` | What changed (Groq migration) |
| `test_setup.py` | Verify installation |

## Support

Need help?
- **Groq Issues**: https://console.groq.com/docs
- **Project Issues**: Check README.md troubleshooting
- **Questions**: Review QUICKSTART.md

---

**Ready to simulate?** Follow the 5 steps above! 🚀
