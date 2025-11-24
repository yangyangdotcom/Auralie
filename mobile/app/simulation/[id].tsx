import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { ActivityIndicator, Card, Chip } from 'react-native-paper';
import { useLocalSearchParams } from 'expo-router';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import { getSimulation } from '../../src/services/api';
import { SimulationResult } from '../../src/types';

const screenWidth = Dimensions.get('window').width;

export default function SimulationDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [simulation, setSimulation] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSimulation();
  }, [id]);

  const loadSimulation = async () => {
    try {
      const response = await getSimulation(id);
      setSimulation(response.data);
    } catch (error) {
      console.error('Failed to load simulation:', error);
    } finally {
      setLoading(false);
    }
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

  const getEmotionEmoji = (emotion: string) => {
    const emotions: Record<string, string> = {
      happy: '😊',
      excited: '🤩',
      curious: '🤔',
      nervous: '😰',
      disappointed: '😞',
      interested: '😌',
      content: '😊',
      hopeful: '🥰',
      neutral: '😐',
    };
    return emotions[emotion.toLowerCase()] || '😐';
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#8b5cf6" />
      </View>
    );
  }

  if (!simulation) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>Simulation not found</Text>
      </View>
    );
  }

  // Prepare chart data
  const chartData = {
    labels: simulation.days.map((d) => `D${d.day}`),
    datasets: [
      {
        data: simulation.days.map((d) => d.person1_fondness),
        color: () => '#8b5cf6',
        strokeWidth: 2,
      },
      {
        data: simulation.days.map((d) => d.person2_fondness),
        color: () => '#ec4899',
        strokeWidth: 2,
      },
    ],
    legend: [simulation.profile1, simulation.profile2],
  };

  return (
    <ScrollView style={styles.container}>
      {/* Compatibility Score */}
      <Card style={styles.scoreCard}>
        <Card.Content>
          <Text style={styles.names}>
            {simulation.profile1} ♥ {simulation.profile2}
          </Text>
          <View style={styles.scoreContainer}>
            <Text
              style={[
                styles.score,
                { color: getScoreColor(simulation.compatibility_score) },
              ]}
            >
              {simulation.compatibility_score || '--'}
            </Text>
            <Text style={styles.scoreLabel}>
              {getScoreLabel(simulation.compatibility_score)}
            </Text>
          </View>

          {simulation.days.length > 0 && (
            <View style={styles.fondnessRow}>
              <View style={styles.fondnessItem}>
                <Text style={styles.fondnessLabel}>{simulation.profile1}</Text>
                <View style={styles.fondnessBar}>
                  <View
                    style={[
                      styles.fondnessFill,
                      {
                        width: `${
                          simulation.days[simulation.days.length - 1]
                            .person1_fondness
                        }%`,
                        backgroundColor: '#8b5cf6',
                      },
                    ]}
                  />
                </View>
                <Text style={styles.fondnessValue}>
                  {simulation.days[simulation.days.length - 1].person1_fondness}
                  /100
                </Text>
              </View>

              <View style={styles.fondnessItem}>
                <Text style={styles.fondnessLabel}>{simulation.profile2}</Text>
                <View style={styles.fondnessBar}>
                  <View
                    style={[
                      styles.fondnessFill,
                      {
                        width: `${
                          simulation.days[simulation.days.length - 1]
                            .person2_fondness
                        }%`,
                        backgroundColor: '#ec4899',
                      },
                    ]}
                  />
                </View>
                <Text style={styles.fondnessValue}>
                  {simulation.days[simulation.days.length - 1].person2_fondness}
                  /100
                </Text>
              </View>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Fondness Chart */}
      {simulation.days.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.cardTitle}>Fondness Over Time</Text>
            <LineChart
              data={chartData}
              width={screenWidth - 64}
              height={220}
              chartConfig={{
                backgroundColor: '#ffffff',
                backgroundGradientFrom: '#ffffff',
                backgroundGradientTo: '#ffffff',
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                propsForDots: {
                  r: '4',
                },
              }}
              bezier
              style={styles.chart}
            />
          </Card.Content>
        </Card>
      )}

      {/* Day-by-Day Interactions */}
      {simulation.days.map((day) => (
        <Card key={day.day} style={styles.card}>
          <Card.Content>
            <Text style={styles.dayTitle}>Day {day.day}</Text>

            {day.interactions.map((interaction, idx) => (
              <View key={idx} style={styles.interaction}>
                <Chip style={styles.activityChip} compact>
                  {interaction.activity_type}
                </Chip>

                {/* Person 1 Message */}
                <View style={[styles.messageBubble, styles.messageBubble1]}>
                  <Text style={styles.messageName}>
                    {interaction.person1_name}
                  </Text>
                  <Text style={styles.messageText}>
                    {interaction.person1_message}
                  </Text>
                  <View style={styles.messageFooter}>
                    <Text style={styles.emotion}>
                      {getEmotionEmoji(interaction.person1_emotion)}{' '}
                      {interaction.person1_emotion}
                    </Text>
                    <Text
                      style={[
                        styles.fondnessChange,
                        interaction.person1_fondness_change > 0
                          ? styles.fondnessPositive
                          : interaction.person1_fondness_change < 0
                          ? styles.fondnessNegative
                          : styles.fondnessNeutral,
                      ]}
                    >
                      {interaction.person1_fondness_change > 0 ? '+' : ''}
                      {interaction.person1_fondness_change}
                    </Text>
                  </View>
                  <Text style={styles.thought}>
                    💭 "{interaction.person1_internal_thought}"
                  </Text>
                </View>

                {/* Person 2 Message */}
                <View style={[styles.messageBubble, styles.messageBubble2]}>
                  <Text style={styles.messageName}>
                    {interaction.person2_name}
                  </Text>
                  <Text style={styles.messageText}>
                    {interaction.person2_message}
                  </Text>
                  <View style={styles.messageFooter}>
                    <Text style={styles.emotion}>
                      {getEmotionEmoji(interaction.person2_emotion)}{' '}
                      {interaction.person2_emotion}
                    </Text>
                    <Text
                      style={[
                        styles.fondnessChange,
                        interaction.person2_fondness_change > 0
                          ? styles.fondnessPositive
                          : interaction.person2_fondness_change < 0
                          ? styles.fondnessNegative
                          : styles.fondnessNeutral,
                      ]}
                    >
                      {interaction.person2_fondness_change > 0 ? '+' : ''}
                      {interaction.person2_fondness_change}
                    </Text>
                  </View>
                  <Text style={styles.thought}>
                    💭 "{interaction.person2_internal_thought}"
                  </Text>
                </View>
              </View>
            ))}
          </Card.Content>
        </Card>
      ))}
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
  errorText: {
    fontSize: 18,
    color: '#6b7280',
  },
  scoreCard: {
    margin: 16,
    marginBottom: 8,
  },
  card: {
    margin: 16,
    marginTop: 8,
    marginBottom: 8,
  },
  names: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 16,
  },
  scoreContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  score: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 16,
    color: '#6b7280',
    marginTop: 4,
  },
  fondnessRow: {
    gap: 16,
  },
  fondnessItem: {
    marginBottom: 8,
  },
  fondnessLabel: {
    fontSize: 14,
    fontWeight: '500',
    marginBottom: 4,
  },
  fondnessBar: {
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
  },
  fondnessFill: {
    height: '100%',
  },
  fondnessValue: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 8,
  },
  dayTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
  },
  interaction: {
    marginBottom: 16,
  },
  activityChip: {
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  messageBubble: {
    padding: 12,
    borderRadius: 12,
    marginBottom: 8,
  },
  messageBubble1: {
    backgroundColor: '#ddd6fe',
  },
  messageBubble2: {
    backgroundColor: '#fce7f3',
  },
  messageName: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 4,
  },
  messageText: {
    fontSize: 14,
    marginBottom: 8,
  },
  messageFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  emotion: {
    fontSize: 12,
    color: '#4b5563',
  },
  fondnessChange: {
    fontSize: 12,
    fontWeight: '600',
  },
  fondnessPositive: {
    color: '#10b981',
  },
  fondnessNegative: {
    color: '#ef4444',
  },
  fondnessNeutral: {
    color: '#6b7280',
  },
  thought: {
    fontSize: 12,
    fontStyle: 'italic',
    color: '#6b7280',
  },
});
