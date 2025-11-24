import { Stack } from 'expo-router';
import { PaperProvider } from 'react-native-paper';

export default function RootLayout() {
  return (
    <PaperProvider>
      <Stack>
        <Stack.Screen
          name="(tabs)"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="match"
          options={{
            title: 'Create Match',
            headerBackTitle: 'Back'
          }}
        />
        <Stack.Screen
          name="simulation/[id]"
          options={{
            title: 'Simulation Results',
            headerBackTitle: 'Back'
          }}
        />
      </Stack>
    </PaperProvider>
  );
}
