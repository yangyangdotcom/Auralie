# Auralie - Digital Twin Dating Simulator

AI-powered dating simulator where digital twins interact over 7 days to determine compatibility before you date in real life.

## 🏗️ Monorepo Structure

```
Auralie/
├── backend/          # Python FastAPI backend + simulation engine
├── mobile/           # React Native Expo mobile app
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt  # For API server

# Configure environment
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env

# Run simulation engine (standalone)
python src/main.py

# OR run API server (for mobile app)
python src/api/main.py
```

Backend runs on: **http://localhost:8000**

### 2. Mobile App Setup

```bash
cd mobile

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Update EXPO_PUBLIC_API_URL if needed

# Start development server
npm start

# Then:
# - Scan QR code with Expo Go app (iOS/Android)
# - Press 'i' for iOS simulator
# - Press 'a' for Android emulator
```

## 📱 Mobile App Features

- **Browse Profiles**: View personality profiles with MBTI, interests, and values
- **Create Matches**: Select two profiles to simulate
- **Run Simulations**: 7-day AI-powered interactions
- **View Results**: Compatibility scores, fondness charts, day-by-day conversations
- **Track History**: Access past simulations

## 🧠 How It Works

1. **Profiles**: Define personality using MBTI, interests, values, and traits
2. **Digital Twins**: LLM-powered agents embody each person's personality
3. **7-Day Simulation**: Twins interact via texting and activities
4. **Compatibility Score**: Average of both twins' fondness levels (0-100)
5. **Analysis**: Review conversations, emotions, and compatibility insights

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI**: REST API server
- **OpenRouter**: LLM provider (supports 100+ models)
- **Pydantic**: Data validation

### Mobile
- **React Native** + **Expo**: Cross-platform mobile framework
- **TypeScript**: Type-safe JavaScript
- **React Native Paper**: Material Design UI components
- **React Native Chart Kit**: Data visualization
- **Axios**: HTTP client

## 📊 API Endpoints

```
GET  /api/profiles              # List all profiles
GET  /api/profiles/{id}         # Get profile details
POST /api/profiles              # Create new profile
POST /api/simulations           # Run simulation
GET  /api/simulations           # List simulations
GET  /api/simulations/{id}      # Get simulation results
DELETE /api/simulations/{id}    # Delete simulation
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Run tests
python -m pytest

# Check configuration
python test_setup.py

# Run simulation
python src/main.py
```

### Mobile Development

```bash
cd mobile

# Run on iOS
npm run ios

# Run on Android
npm run android

# Type check
npx tsc --noEmit
```

## 📝 Environment Variables

### Backend (.env)
```
OPENROUTER_API_KEY=your_key_here
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
OPENROUTER_APP_NAME=Auralie
```

### Mobile (.env)
```
EXPO_PUBLIC_API_URL=http://localhost:8000
```

**Note**: For mobile development:
- iOS Simulator: `http://localhost:8000`
- Android Emulator: `http://10.0.2.2:8000`
- Physical Device: `http://YOUR_COMPUTER_IP:8000` (e.g., `192.168.1.100:8000`)

## 🚢 Deployment

### Backend
Deploy to Railway, Render, or Fly.io:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
cd backend
railway up
```

### Mobile
Build with EAS (Expo Application Services):

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS
cd mobile
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android
```

## 📖 Documentation

- **Backend**: See `/backend/README.md` for detailed backend documentation
- **Mobile**: See `/mobile/README.md` for mobile app development guide
- **API**: FastAPI auto-generated docs at `http://localhost:8000/docs`

## 🎯 Key Features

### ✅ Implemented
- Profile creation with MBTI, interests, values
- 7-day simulation with texting and activities
- Emotion tracking and fondness system
- Compatibility scoring
- FastAPI REST API
- Mobile app (iOS + Android)
- Real-time progress tracking
- Beautiful UI with charts

### 🚧 Future Enhancements
- User authentication
- Profile creation via mobile app
- Push notifications for completed simulations
- Social features (share results)
- Advanced matching algorithms
- Video/voice simulation modes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🐛 Issues & Feedback

Report issues at: https://github.com/yourusername/auralie/issues

## 💡 Project Origin

Built as an MVP to test the feasibility of AI-powered compatibility prediction through simulated interactions.

**Development Time**: ~2 weeks from concept to working MVP

---

Made with 💜 by [Your Name]
