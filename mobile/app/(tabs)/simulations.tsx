import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { Card, ActivityIndicator, Chip } from 'react-native-paper';
import { useRouter } from 'expo-router';
import { getSimulations } from '../../src/services/api';
import { SimulationSummary } from '../../src/types';

export default function SimulationsScreen() {
  const [simulations, setSimulations] = useState<SimulationSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const router = useRouter();

  const loadSimulations = async () => {
    try {
      const response = await getSimulations();
      setSimulations(response.data);
    } catch (error) {
      console.error('Failed to load simulations:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadSimulations();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadSimulations();
  };

  const getScoreColor = (score?: number) => {
    if (!score) return '#9ca3af';
    if (score >= 85) return '#10b981';
    if (score >= 70) return '#3b82f6';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getScoreLabel = (score?: number) => {
    if (!score) return 'Incomplete';
    if (score >= 85) return 'Highly Compatible';
    if (score >= 70) return 'Compatible';
    if (score >= 50) return 'Moderately Compatible';
    return 'Not Compatible';
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
        {simulations.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No simulations yet</Text>
            <Text style={styles.emptySubtext}>
              Create a match to run your first simulation
            </Text>
          </View>
        ) : (
          simulations.map((sim) => (
            <TouchableOpacity
              key={sim.simulation_id}
              onPress={() => router.push(`/simulation/${sim.simulation_id}`)}
            >
              <Card style={styles.card}>
                <Card.Content>
                  <View style={styles.cardHeader}>
                    <Text style={styles.names}>
                      {sim.profile1} ♥ {sim.profile2}
                    </Text>
                    {sim.compatibility_score !== undefined && (
                      <View style={styles.scoreContainer}>
                        <Text
                          style={[
                            styles.score,
                            { color: getScoreColor(sim.compatibility_score) },
                          ]}
                        >
                          {sim.compatibility_score}
                        </Text>
                      </View>
                    )}
                  </View>

                  <Chip
                    style={[
                      styles.statusChip,
                      { backgroundColor: getScoreColor(sim.compatibility_score) },
                    ]}
                    textStyle={{ color: '#fff' }}
                  >
                    {getScoreLabel(sim.compatibility_score)}
                  </Chip>

                  <Text style={styles.progress}>
                    {sim.completed_days}/7 days completed
                  </Text>
                </Card.Content>
              </Card>
            </TouchableOpacity>
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
    marginBottom: 12,
  },
  names: {
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1,
  },
  scoreContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  score: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  statusChip: {
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  progress: {
    fontSize: 12,
    color: '#6b7280',
  },
});
