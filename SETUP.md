# Auralie Setup Guide

Complete setup instructions for the monorepo structure.

## 📁 Project Structure

```
Auralie/
├── backend/              # Python backend
│   ├── src/
│   │   ├── api/         # FastAPI server
│   │   └── ...          # Simulation engine
│   ├── profiles/        # JSON profiles
│   ├── output/          # Results
│   └── requirements.txt
├── mobile/              # React Native app
│   ├── app/            # Expo Router pages
│   ├── src/            # Components & services
│   └── package.json
└── README.md
```

## 🚀 Quick Setup

### 1. Backend Setup (5 minutes)

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt

# Configure
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

**Get OpenRouter API key**: https://openrouter.ai/keys
- $5 minimum deposit + $5 free credits

### 2. Mobile Setup (5 minutes)

```bash
cd mobile

# Install Node.js dependencies
npm install

# Configure API URL
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

### 3. Install Expo Go App

- **iOS**: Download from App Store
- **Android**: Download from Google Play

## 🎯 Running the Project

### Start Backend API

```bash
cd backend
python src/api/main.py
```

Backend will run on: **http://localhost:8000**

API docs: **http://localhost:8000/docs**

### Start Mobile App

In a **new terminal**:

```bash
cd mobile
npm start
```

Then:
1. Scan QR code with Expo Go app on your phone
2. **OR** press `i` for iOS simulator
3. **OR** press `a` for Android emulator

## 📱 Using the Mobile App

### First Time Setup

1. **Make sure backend is running** on port 8000
2. **Create some profiles** (if you haven't already):

```bash
cd backend
# Create sample profiles
python src/main.py create-profiles
```

3. **Open mobile app** and navigate to "Profiles" tab
4. **Pull to refresh** to see profiles from backend

### Running a Simulation

1. Tap **"Create New Match"** on home screen
2. Select two different profiles
3. Tap **"Run 7-Day Simulation"**
4. Wait 2-5 minutes (simulation runs on backend)
5. View results with compatibility score, charts, and conversations

## 🔧 Troubleshooting

### Mobile Can't Connect to Backend

**Problem**: "Network Error" or "Failed to load profiles"

**Solutions**:

1. **Check backend is running**:
   - Visit http://localhost:8000 in your browser
   - You should see: `{"message": "Auralie API"}`

2. **iOS Simulator**: Use `http://localhost:8000` ✅

3. **Android Emulator**: Update mobile/.env:
   ```
   EXPO_PUBLIC_API_URL=http://10.0.2.2:8000
   ```

4. **Physical Device**:
   - Your computer and phone must be on the **same WiFi**
   - Find your computer's IP address:
     ```bash
     # Mac/Linux
     ifconfig | grep "inet " | grep -v 127.0.0.1

     # Windows
     ipconfig
     ```
   - Update mobile/.env:
     ```
     EXPO_PUBLIC_API_URL=http://192.168.1.XXX:8000
     ```
   - Restart Expo: `npm start`

### Backend Import Errors

**Problem**: `ModuleNotFoundError: No module named 'profile'`

**Solution**: Make sure you're running from the `backend/` directory:
```bash
cd backend
python src/api/main.py
```

### Port 8000 Already in Use

**Solution**:
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
python src/api/main.py --port 8001
```

Then update mobile/.env:
```
EXPO_PUBLIC_API_URL=http://localhost:8001
```

### Simulation Takes Forever

**Problem**: Simulation running for 10+ minutes

**Possible causes**:
- OpenRouter rate limits (check account balance)
- Network issues
- Model overloaded

**Solutions**:
1. Check backend terminal for errors
2. Try a faster model in backend/.env:
   ```
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
   ```
3. Restart backend

### No Profiles Showing

**Problem**: Mobile app shows "No profiles found"

**Solution**:
```bash
cd backend
python src/main.py create-profiles
```

Then pull to refresh in mobile app.

## 🎨 Development Tips

### Hot Reload

- **Backend**: Changes require restart
- **Mobile**: Auto-reloads on save (may need to shake device and press "Reload")

### Viewing API Docs

Visit http://localhost:8000/docs for interactive API documentation.

### Checking Logs

**Backend**: Terminal shows API requests and simulation progress

**Mobile**:
- Shake device → "Debug Remote JS"
- OR check Expo Dev Tools in browser

### Testing API Manually

```bash
# List profiles
curl http://localhost:8000/api/profiles

# Run simulation
curl -X POST http://localhost:8000/api/simulations \
  -H "Content-Type: application/json" \
  -d '{"profile1_id": "elena_rodriguez", "profile2_id": "leo_martinez"}'
```

## 📚 Next Steps

1. **Create your own profiles** in `backend/profiles/`
2. **Run simulations** via mobile app
3. **Analyze results** - look for patterns
4. **Customize**: Modify profiles, activities, or prompts

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React Native**: https://reactnative.dev/
- **Expo**: https://docs.expo.dev/
- **OpenRouter**: https://openrouter.ai/docs

## 💡 Pro Tips

1. **Keep backend running**: Don't restart unless needed
2. **Use sample profiles first**: Test before creating custom profiles
3. **Monitor costs**: Check OpenRouter usage regularly
4. **Save good simulations**: Results stored in `backend/output/`
5. **Experiment with models**: Try different LLMs for varied personalities

## 🆘 Still Having Issues?

1. Check backend logs for errors
2. Verify `.env` files in both backend/ and mobile/
3. Ensure OpenRouter API key is valid
4. Check your WiFi connection
5. Try restarting both backend and mobile app

## 🎉 Success!

Once everything works, you should see:
- ✅ Backend API responding at localhost:8000
- ✅ Mobile app showing profiles
- ✅ Simulations completing successfully
- ✅ Results displaying with charts and conversations

Enjoy exploring digital twin compatibility! 💘
