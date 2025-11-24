import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert } from 'react-native';
import { Button, Card, Chip, ActivityIndicator, RadioButton } from 'react-native-paper';
import { useRouter } from 'expo-router';
import { getProfiles, runSimulation } from '../src/services/api';
import { Profile } from '../src/types';

export default function MatchScreen() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [selected1, setSelected1] = useState<string>('');
  const [selected2, setSelected2] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      const response = await getProfiles();
      setProfiles(response.data);
    } catch (error) {
      console.error('Failed to load profiles:', error);
      Alert.alert('Error', 'Failed to load profiles. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleRunSimulation = async () => {
    if (!selected1 || !selected2) {
      Alert.alert('Error', 'Please select two profiles');
      return;
    }

    if (selected1 === selected2) {
      Alert.alert('Error', 'Please select two different profiles');
      return;
    }

    setRunning(true);
    try {
      const response = await runSimulation(selected1, selected2);
      Alert.alert(
        'Success',
        'Simulation started! This may take a few minutes.',
        [
          {
            text: 'OK',
            onPress: () => router.replace(`/simulation/${response.data.simulation_id}`),
          },
        ]
      );
    } catch (error: any) {
      console.error('Failed to run simulation:', error);
      Alert.alert(
        'Error',
        error.response?.data?.detail || 'Failed to run simulation'
      );
    } finally {
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#8b5cf6" />
      </View>
    );
  }

  if (profiles.length < 2) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyText}>Not enough profiles</Text>
        <Text style={styles.emptySubtext}>
          You need at least 2 profiles to create a match
        </Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.sectionTitle}>Select First Profile</Text>
        <RadioButton.Group onValueChange={setSelected1} value={selected1}>
          {profiles.map((profile) => (
            <Card
              key={profile.id}
              style={[
                styles.card,
                selected1 === profile.id && styles.selectedCard,
                selected2 === profile.id && styles.disabledCard,
              ]}
            >
              <Card.Content>
                <View style={styles.cardHeader}>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.name}>{profile.name}</Text>
                    <Text style={styles.age}>{profile.age} • {profile.mbti}</Text>
                  </View>
                  <RadioButton
                    value={profile.id}
                    disabled={selected2 === profile.id}
                  />
                </View>
                <View style={styles.chips}>
                  {profile.interests.slice(0, 3).map((interest) => (
                    <Chip key={interest} style={styles.chip} compact>
                      {interest}
                    </Chip>
                  ))}
                </View>
              </Card.Content>
            </Card>
          ))}
        </RadioButton.Group>

        <Text style={[styles.sectionTitle, { marginTop: 24 }]}>
          Select Second Profile
        </Text>
        <RadioButton.Group onValueChange={setSelected2} value={selected2}>
          {profiles.map((profile) => (
            <Card
              key={profile.id}
              style={[
                styles.card,
                selected2 === profile.id && styles.selectedCard,
                selected1 === profile.id && styles.disabledCard,
              ]}
            >
              <Card.Content>
                <View style={styles.cardHeader}>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.name}>{profile.name}</Text>
                    <Text style={styles.age}>{profile.age} • {profile.mbti}</Text>
                  </View>
                  <RadioButton
                    value={profile.id}
                    disabled={selected1 === profile.id}
                  />
                </View>
                <View style={styles.chips}>
                  {profile.interests.slice(0, 3).map((interest) => (
                    <Chip key={interest} style={styles.chip} compact>
                      {interest}
                    </Chip>
                  ))}
                </View>
              </Card.Content>
            </Card>
          ))}
        </RadioButton.Group>

        <Button
          mode="contained"
          onPress={handleRunSimulation}
          disabled={!selected1 || !selected2 || running}
          loading={running}
          style={styles.button}
          buttonColor="#8b5cf6"
        >
          {running ? 'Running Simulation...' : 'Run 7-Day Simulation'}
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
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  content: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#374151',
  },
  emptyText: {
    fontSize: 18,
    color: '#6b7280',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
  },
  card: {
    marginBottom: 12,
  },
  selectedCard: {
    borderColor: '#8b5cf6',
    borderWidth: 2,
  },
  disabledCard: {
    opacity: 0.5,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
  },
  age: {
    fontSize: 14,
    color: '#6b7280',
  },
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  chip: {
    marginRight: 4,
  },
  button: {
    marginTop: 24,
    marginBottom: 40,
  },
});
