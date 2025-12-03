import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { Card, Chip, ActivityIndicator, Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import { getProfiles } from '../../src/services/api';
import { Profile } from '../../src/types';

export default function ProfilesScreen() {
  const router = useRouter();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadProfiles = async () => {
    try {
      const response = await getProfiles();
      setProfiles(response.data);
    } catch (error) {
      console.error('Failed to load profiles:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadProfiles();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadProfiles();
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#8b5cf6" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.content}>
        {profiles.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No profiles found</Text>
            <Text style={styles.emptySubtext}>
              Add profiles in the backend or create them via API
            </Text>
          </View>
        ) : (
          profiles.map((profile) => (
            <Card key={profile.id} style={styles.card}>
              <Card.Content>
                <View style={styles.cardHeader}>
                  <Text style={styles.name}>{profile.name}</Text>
                  <Text style={styles.age}>{profile.age}</Text>
                </View>

                <Chip style={styles.mbtiChip} mode="outlined">
                  {profile.mbti}
                </Chip>

                {profile.bio && (
                  <Text style={styles.bio}>{profile.bio}</Text>
                )}

                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Interests</Text>
                  <View style={styles.chips}>
                    {profile.interests.slice(0, 3).map((interest) => (
                      <Chip key={interest} style={styles.chip} compact>
                        {interest}
                      </Chip>
                    ))}
                    {profile.interests.length > 3 && (
                      <Chip style={styles.chip} compact>
                        +{profile.interests.length - 3} more
                      </Chip>
                    )}
                  </View>
                </View>

                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Values</Text>
                  <View style={styles.chips}>
                    {profile.values.slice(0, 3).map((value) => (
                      <Chip key={value} style={styles.chip} compact>
                        {value}
                      </Chip>
                    ))}
                  </View>
                </View>

                <View style={styles.traits}>
                  <Text style={styles.trait}>
                    Spontaneity: {profile.spontaneity_level}/10
                  </Text>
                  <Text style={styles.trait}>
                    Expressiveness: {profile.emotional_expressiveness}/10
                  </Text>
                </View>

                <Button
                  mode="contained"
                  onPress={() => router.push(`/chat/${profile.id}`)}
                  style={styles.chatButton}
                  buttonColor="#8b5cf6"
                  icon="chat"
                >
                  Start Chat
                </Button>
              </Card.Content>
            </Card>
          ))
        )}
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
  },
  content: {
    padding: 16,
  },
  emptyState: {
    alignItems: 'center',
    marginTop: 100,
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
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  name: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  age: {
    fontSize: 16,
    color: '#6b7280',
  },
  mbtiChip: {
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  bio: {
    fontSize: 14,
    color: '#4b5563',
    marginBottom: 12,
    fontStyle: 'italic',
  },
  section: {
    marginTop: 12,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 6,
    textTransform: 'uppercase',
  },
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  chip: {
    marginRight: 4,
    marginBottom: 4,
  },
  traits: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  trait: {
    fontSize: 12,
    color: '#6b7280',
  },
  chatButton: {
    marginTop: 16,
  },
});
