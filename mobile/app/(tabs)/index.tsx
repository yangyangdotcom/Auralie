import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Button, Card, Title, Paragraph } from 'react-native-paper';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>💘 Auralie</Text>
        <Text style={styles.tagline}>Digital Twin Dating Simulator</Text>
      </View>

      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Title>How It Works</Title>
            <Paragraph style={styles.paragraph}>
              1. Create or browse personality profiles
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              2. Select two profiles to match
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              3. Watch AI twins interact over 7 days
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              4. Get compatibility score & insights
            </Paragraph>
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={() => router.push('/match')}
          style={styles.button}
          buttonColor="#8b5cf6"
        >
          Create New Match
        </Button>

        <Button
          mode="outlined"
          onPress={() => router.push('/profiles')}
          style={styles.button}
        >
          Browse Profiles
        </Button>

        <Button
          mode="outlined"
          onPress={() => router.push('/simulations')}
          style={styles.button}
        >
          View Past Simulations
        </Button>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  header: {
    alignItems: 'center',
    paddingTop: 60,
    paddingBottom: 30,
    backgroundColor: '#fff',
  },
  logo: {
    fontSize: 48,
    marginBottom: 8,
  },
  tagline: {
    fontSize: 16,
    color: '#6b7280',
  },
  content: {
    padding: 20,
  },
  card: {
    marginBottom: 24,
  },
  paragraph: {
    marginVertical: 4,
  },
  button: {
    marginBottom: 12,
  },
});
