# Auralie Mobile App

React Native mobile app for Auralie digital twin dating simulator.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API endpoint:**
   Create `.env` file:
   ```
   EXPO_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Run on device:**
   - Download "Expo Go" app on your phone
   - Scan QR code from terminal

   OR

   - Press `i` for iOS simulator
   - Press `a` for Android emulator

## Project Structure

```
mobile/
├── app/                    # Expo Router pages
│   ├── (tabs)/            # Tab navigation
│   │   ├── index.tsx      # Home
│   │   ├── profiles.tsx   # Profiles list
│   │   └── simulations.tsx # Simulations list
│   ├── match.tsx          # Match selection
│   └── simulation/[id].tsx # Simulation detail
├── src/
│   ├── components/        # Reusable components
│   ├── services/          # API client
│   └── types/             # TypeScript types
└── assets/                # Images, fonts, etc.
```

## Development

- Backend must be running on port 8000
- For iOS simulator: `http://localhost:8000`
- For Android emulator: `http://10.0.2.2:8000`
- For physical device: Use your computer's local IP

## Building for Production

```bash
# iOS
eas build --platform ios

# Android
eas build --platform android
```
