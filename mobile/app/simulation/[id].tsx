import { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Modal, Pressable, Animated } from 'react-native';
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
  const [selectedThought, setSelectedThought] = useState<{
    name: string;
    thought: string;
  } | null>(null);
  const [highlightedMessage, setHighlightedMessage] = useState<string | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);
  const messageRefs = useRef<{ [key: string]: View | null }>({});

  useEffect(() => {
    loadSimulation();

    // Poll for updates if simulation is still running
    const pollInterval = setInterval(() => {
      if (simulation?.status === 'running' || simulation?.status === 'pending') {
        loadSimulation();
      }
    }, 5000); // Check every 5 seconds

    return () => clearInterval(pollInterval);
  }, [id, simulation?.status]);

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

  const handleDataPointClick = (data: any) => {
    const { index } = data;
    if (index >= 0 && index < fondnessData.length) {
      const messageId = fondnessData[index].messageId;
      setHighlightedMessage(messageId);

      // Scroll to the message
      setTimeout(() => {
        const messageView = messageRefs.current[messageId];
        if (messageView && scrollViewRef.current) {
          messageView.measureLayout(
            scrollViewRef.current as any,
            (x, y) => {
              scrollViewRef.current?.scrollTo({ y: y - 100, animated: true });
            },
            () => {}
          );
        }
      }, 100);

      // Clear highlight after 3 seconds
      setTimeout(() => {
        setHighlightedMessage(null);
      }, 3000);
    }
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

  // Extract days from result if nested
  const days = simulation.result?.days || simulation.days || [];
  const profile1 = simulation.result?.participants?.person1 || simulation.profile1;
  const profile2 = simulation.result?.participants?.person2 || simulation.profile2;
  const compatibilityScore = simulation.result?.compatibility?.score || simulation.compatibility_score;
  // Backend uses "final_assessment" (singular), try both singular and plural
  const finalAssessments = simulation.result?.final_assessment || simulation.result?.final_assessments || simulation.final_assessment || simulation.final_assessments || {};

  // Show loading/pending state if simulation is still running
  if (days.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#8b5cf6" />
        <Text style={styles.statusText}>
          {simulation.status === 'running'
            ? 'Simulation in progress...'
            : simulation.status === 'pending'
            ? 'Simulation starting...'
            : 'Processing simulation...'}
        </Text>
        <Text style={styles.statusSubtext}>
          This may take 2-5 minutes
        </Text>
      </View>
    );
  }

  // Calculate fondness data from every message
  const fondnessData: Array<{
    person1_fondness: number;
    person2_fondness: number;
    label: string;
    day: number;
    messageId: string;
  }> = [];

  days.forEach((d: any) => {
    // Process morning and evening texting sessions
    d.texting_sessions?.forEach((session: any, sessionIdx: number) => {
      session.exchanges?.forEach((exchange: any, exchIdx: number) => {
        const isProfile1 = exchange.sender === profile1;
        const currentP1Fondness = fondnessData.length > 0
          ? fondnessData[fondnessData.length - 1].person1_fondness
          : 50;
        const currentP2Fondness = fondnessData.length > 0
          ? fondnessData[fondnessData.length - 1].person2_fondness
          : 50;

        const messageId = `day${d.day}-session${sessionIdx}-exchange${exchIdx}`;
        fondnessData.push({
          person1_fondness: isProfile1
            ? (exchange.fondness_level ?? currentP1Fondness)
            : currentP1Fondness,
          person2_fondness: !isProfile1
            ? (exchange.fondness_level ?? currentP2Fondness)
            : currentP2Fondness,
          label: `D${d.day}`,
          day: d.day,
          messageId,
        });
      });
    });

    // Process activities
    d.activities?.forEach((act: any, actIdx: number) => {
      act.interactions?.forEach((interaction: any, intIdx: number) => {
        const isProfile1 = interaction.sender === profile1;
        const currentP1Fondness = fondnessData.length > 0
          ? fondnessData[fondnessData.length - 1].person1_fondness
          : 50;
        const currentP2Fondness = fondnessData.length > 0
          ? fondnessData[fondnessData.length - 1].person2_fondness
          : 50;

        const messageId = `day${d.day}-activity${actIdx}-interaction${intIdx}`;
        fondnessData.push({
          person1_fondness: isProfile1
            ? (interaction.fondness_level ?? currentP1Fondness)
            : currentP1Fondness,
          person2_fondness: !isProfile1
            ? (interaction.fondness_level ?? currentP2Fondness)
            : currentP2Fondness,
          label: `D${d.day}`,
          day: d.day,
          messageId,
        });
      });
    });
  });

  // Prepare chart data with labels showing day markers
  const chartData = {
    labels: fondnessData.map((d, idx) => {
      // Show day label at start of each day, otherwise empty
      const prevDay = idx > 0 ? fondnessData[idx - 1].day : 0;
      return d.day !== prevDay ? `D${d.day}` : '';
    }),
    datasets: [
      {
        data: fondnessData.map(d => d.person1_fondness),
        color: () => '#8b5cf6',
        strokeWidth: 2,
      },
      {
        data: fondnessData.map(d => d.person2_fondness),
        color: () => '#ec4899',
        strokeWidth: 2,
      },
    ],
    legend: [profile1, profile2],
  };

  return (
    <ScrollView style={styles.container} ref={scrollViewRef}>
      {/* Compatibility Score */}
      <Card style={styles.scoreCard}>
        <Card.Content>
          <Text style={styles.names}>
            {profile1} ♥ {profile2}
          </Text>
          <View style={styles.scoreContainer}>
            <Text
              style={[
                styles.score,
                { color: getScoreColor(compatibilityScore) },
              ]}
            >
              {compatibilityScore || '--'}
            </Text>
            <Text style={styles.scoreLabel}>
              {getScoreLabel(compatibilityScore)}
            </Text>
          </View>

          {days.length > 0 && fondnessData.length > 0 && (
            <View style={styles.fondnessRow}>
              <View style={styles.fondnessItem}>
                <Text style={styles.fondnessLabel}>{profile1}</Text>
                <View style={styles.fondnessBar}>
                  <View
                    style={[
                      styles.fondnessFill,
                      {
                        width: `${
                          fondnessData[fondnessData.length - 1].person1_fondness
                        }%`,
                        backgroundColor: '#8b5cf6',
                      },
                    ]}
                  />
                </View>
                <Text style={styles.fondnessValue}>
                  {fondnessData[fondnessData.length - 1].person1_fondness}
                  /100
                </Text>
              </View>

              <View style={styles.fondnessItem}>
                <Text style={styles.fondnessLabel}>{profile2}</Text>
                <View style={styles.fondnessBar}>
                  <View
                    style={[
                      styles.fondnessFill,
                      {
                        width: `${
                          fondnessData[fondnessData.length - 1].person2_fondness
                        }%`,
                        backgroundColor: '#ec4899',
                      },
                    ]}
                  />
                </View>
                <Text style={styles.fondnessValue}>
                  {fondnessData[fondnessData.length - 1].person2_fondness}
                  /100
                </Text>
              </View>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Final Assessments */}
      {Object.keys(finalAssessments).length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.cardTitle}>💭 Final Thoughts</Text>

            {finalAssessments[profile1] && (
              <View style={styles.assessmentContainer}>
                <Text style={styles.assessmentName}>{profile1}</Text>
                <Text style={styles.assessmentText}>
                  "{finalAssessments[profile1].statement || finalAssessments[profile1].assessment || 'No assessment available'}"
                </Text>
                {(finalAssessments[profile1].final_fondness !== undefined || finalAssessments[profile1].fondness_level !== undefined) && (
                  <View style={styles.assessmentFondness}>
                    <Text style={styles.assessmentFondnessLabel}>Final Fondness:</Text>
                    <Text style={[styles.assessmentFondnessValue, { color: '#8b5cf6' }]}>
                      {finalAssessments[profile1].final_fondness ?? finalAssessments[profile1].fondness_level}/100
                    </Text>
                  </View>
                )}
              </View>
            )}

            {finalAssessments[profile2] && (
              <View style={[styles.assessmentContainer, styles.assessmentContainerLast]}>
                <Text style={styles.assessmentName}>{profile2}</Text>
                <Text style={styles.assessmentText}>
                  "{finalAssessments[profile2].statement || finalAssessments[profile2].assessment || 'No assessment available'}"
                </Text>
                {(finalAssessments[profile2].final_fondness !== undefined || finalAssessments[profile2].fondness_level !== undefined) && (
                  <View style={styles.assessmentFondness}>
                    <Text style={styles.assessmentFondnessLabel}>Final Fondness:</Text>
                    <Text style={[styles.assessmentFondnessValue, { color: '#ec4899' }]}>
                      {finalAssessments[profile2].final_fondness ?? finalAssessments[profile2].fondness_level}/100
                    </Text>
                  </View>
                )}
              </View>
            )}
          </Card.Content>
        </Card>
      )}

      {/* Date Suggestions */}
      {(simulation.result?.date_suggestions || simulation.date_suggestions)?.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.cardTitle}>💡 Conversation Starters for Your Date</Text>
            <Text style={styles.suggestionsSubtitle}>
              Based on your simulation, here are specific topics to discuss:
            </Text>
            <View style={styles.suggestionsContainer}>
              {(simulation.result?.date_suggestions || simulation.date_suggestions).map((suggestion, index) => (
                <View key={index} style={styles.suggestionItem}>
                  <View style={styles.suggestionNumber}>
                    <Text style={styles.suggestionNumberText}>{index + 1}</Text>
                  </View>
                  <Text style={styles.suggestionText}>{suggestion}</Text>
                </View>
              ))}
            </View>
          </Card.Content>
        </Card>
      )}

      {/* Fondness Chart */}
      {days.length > 0 && fondnessData.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.cardTitle}>Fondness Over Time (Every Message)</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={true}>
              <LineChart
                data={chartData}
                width={Math.max(screenWidth - 64, fondnessData.length * 15)}
                height={220}
                chartConfig={{
                  backgroundColor: '#ffffff',
                  backgroundGradientFrom: '#ffffff',
                  backgroundGradientTo: '#ffffff',
                  decimalPlaces: 0,
                  color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                  labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                  propsForDots: {
                    r: '3',
                  },
                }}
                bezier
                style={styles.chart}
                onDataPointClick={handleDataPointClick}
              />
            </ScrollView>
          </Card.Content>
        </Card>
      )}

      {/* Day-by-Day Interactions */}
      {days.map((day: any) => {
        return (
        <View key={day.day}>
          <Text style={styles.dayHeader}>Day {day.day}</Text>

          {/* Morning Texting */}
          {day.texting_sessions?.map((session: any, sessionIdx: number) => (
            <View key={`session-${sessionIdx}`}>
              <Text style={styles.timeLabel}>
                {session.time === 'morning' ? '🌅 Morning' : '🌙 Evening'}
              </Text>
              {session.exchanges?.map((exchange: any, exchIdx: number) => {
                const isProfile1 = exchange.sender === profile1;
                const messageId = `day${day.day}-session${sessionIdx}-exchange${exchIdx}`;
                const isHighlighted = highlightedMessage === messageId;
                return (
                  <TouchableOpacity
                    key={`exchange-${exchIdx}`}
                    onLongPress={() => setSelectedThought({
                      name: exchange.sender,
                      thought: exchange.internal_thought
                    })}
                    activeOpacity={0.8}
                    style={isProfile1 ? styles.chatContainer1 : styles.chatContainer2}
                  >
                    <View
                      ref={(ref) => { messageRefs.current[messageId] = ref; }}
                      style={[
                        styles.chatBubble,
                        isProfile1 ? styles.chatBubble1 : styles.chatBubble2,
                        isHighlighted && styles.chatBubbleHighlighted
                      ]}>
                      <Text style={styles.chatName}>{exchange.sender}</Text>
                      <View style={styles.jsonContainer}>
                        <Text style={styles.jsonKey}>message: <Text style={styles.jsonValue}>"{exchange.message}"</Text></Text>
                        <Text style={styles.jsonKey}>emotion: <Text style={styles.jsonValue}>"{exchange.emotion}"</Text></Text>
                        <Text style={styles.jsonKey}>internal_thought: <Text style={styles.jsonValue}>"{exchange.internal_thought}"</Text></Text>
                        <View style={styles.jsonFooter}>
                          <Text style={styles.jsonKey}>fondness_level: <Text style={styles.jsonValueNumber}>{exchange.fondness_level || 50}</Text></Text>
                          <Text style={styles.chatEmotion}>
                            {getEmotionEmoji(exchange.emotion)}
                          </Text>
                        </View>
                        {exchange.fondness_breakdown && (
                          <View style={styles.breakdownContainer}>
                            <Text style={styles.breakdownTitle}>Fondness Change Breakdown:</Text>
                            <Text style={styles.breakdownItem}>
                              • Total: <Text style={[styles.breakdownValue, { color: exchange.fondness_breakdown.total >= 0 ? '#10b981' : '#ef4444' }]}>{exchange.fondness_breakdown.total >= 0 ? '+' : ''}{exchange.fondness_breakdown.total}</Text>
                            </Text>
                            <Text style={styles.breakdownItem}>
                              • LLM Decision: <Text style={[styles.breakdownValue, { color: exchange.fondness_breakdown.llm_decision >= 0 ? '#10b981' : '#ef4444' }]}>{exchange.fondness_breakdown.llm_decision >= 0 ? '+' : ''}{exchange.fondness_breakdown.llm_decision}</Text>
                            </Text>
                            {exchange.fondness_breakdown.value_penalty !== 0 && (
                              <Text style={styles.breakdownItem}>
                                • Value Mismatch: <Text style={styles.breakdownValue}>{exchange.fondness_breakdown.value_penalty}</Text>
                              </Text>
                            )}
                            {exchange.fondness_breakdown.dealbreaker_penalty !== 0 && (
                              <Text style={styles.breakdownItem}>
                                • Dealbreaker: <Text style={styles.breakdownValue}>{exchange.fondness_breakdown.dealbreaker_penalty}</Text>
                              </Text>
                            )}
                          </View>
                        )}
                      </View>
                    </View>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}

          {/* Activities */}
          {day.activities?.map((act: any, actIdx: number) => (
            <View key={`activity-${actIdx}`}>
              <View style={styles.activityHeader}>
                <Text style={styles.activityLabel}>
                  🎯 {act.activity?.name || 'Activity'}
                </Text>
              </View>
              {act.interactions?.map((interaction: any, intIdx: number) => {
                const isProfile1 = interaction.sender === profile1;
                const messageId = `day${day.day}-activity${actIdx}-interaction${intIdx}`;
                const isHighlighted = highlightedMessage === messageId;
                return (
                  <TouchableOpacity
                    key={`interaction-${intIdx}`}
                    onLongPress={() => setSelectedThought({
                      name: interaction.sender,
                      thought: interaction.internal_thought
                    })}
                    activeOpacity={0.8}
                    style={isProfile1 ? styles.chatContainer1 : styles.chatContainer2}
                  >
                    <View
                      ref={(ref) => { messageRefs.current[messageId] = ref; }}
                      style={[
                        styles.chatBubble,
                        isProfile1 ? styles.chatBubble1 : styles.chatBubble2,
                        isHighlighted && styles.chatBubbleHighlighted
                      ]}>
                      <Text style={styles.chatName}>{interaction.sender}</Text>
                      <View style={styles.jsonContainer}>
                        <Text style={styles.jsonKey}>message: <Text style={styles.jsonValue}>"{interaction.message}"</Text></Text>
                        <Text style={styles.jsonKey}>emotion: <Text style={styles.jsonValue}>"{interaction.emotion}"</Text></Text>
                        <Text style={styles.jsonKey}>internal_thought: <Text style={styles.jsonValue}>"{interaction.internal_thought}"</Text></Text>
                        <View style={styles.jsonFooter}>
                          <Text style={styles.jsonKey}>fondness_level: <Text style={styles.jsonValueNumber}>{interaction.fondness_level || 50}</Text></Text>
                          <Text style={styles.chatEmotion}>
                            {getEmotionEmoji(interaction.emotion)}
                          </Text>
                        </View>
                        {interaction.fondness_breakdown && (
                          <View style={styles.breakdownContainer}>
                            <Text style={styles.breakdownTitle}>Fondness Change Breakdown:</Text>
                            <Text style={styles.breakdownItem}>
                              • Total: <Text style={[styles.breakdownValue, { color: interaction.fondness_breakdown.total >= 0 ? '#10b981' : '#ef4444' }]}>{interaction.fondness_breakdown.total >= 0 ? '+' : ''}{interaction.fondness_breakdown.total}</Text>
                            </Text>
                            <Text style={styles.breakdownItem}>
                              • LLM Decision: <Text style={[styles.breakdownValue, { color: interaction.fondness_breakdown.llm_decision >= 0 ? '#10b981' : '#ef4444' }]}>{interaction.fondness_breakdown.llm_decision >= 0 ? '+' : ''}{interaction.fondness_breakdown.llm_decision}</Text>
                            </Text>
                            {interaction.fondness_breakdown.value_penalty !== 0 && (
                              <Text style={styles.breakdownItem}>
                                • Value Mismatch: <Text style={styles.breakdownValue}>{interaction.fondness_breakdown.value_penalty}</Text>
                              </Text>
                            )}
                            {interaction.fondness_breakdown.dealbreaker_penalty !== 0 && (
                              <Text style={styles.breakdownItem}>
                                • Dealbreaker: <Text style={styles.breakdownValue}>{interaction.fondness_breakdown.dealbreaker_penalty}</Text>
                              </Text>
                            )}
                          </View>
                        )}
                      </View>
                    </View>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}
        </View>
        );
      })}

      {/* Internal Thought Modal */}
      <Modal
        visible={selectedThought !== null}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setSelectedThought(null)}
      >
        <Pressable
          style={styles.modalOverlay}
          onPress={() => setSelectedThought(null)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>
              💭 {selectedThought?.name}'s Thoughts
            </Text>
            <Text style={styles.modalThought}>
              "{selectedThought?.thought}"
            </Text>
            <Text style={styles.modalHint}>Tap anywhere to close</Text>
          </View>
        </Pressable>
      </Modal>
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
  statusText: {
    fontSize: 18,
    color: '#6b7280',
    marginTop: 16,
    textAlign: 'center',
  },
  statusSubtext: {
    fontSize: 14,
    color: '#9ca3af',
    marginTop: 8,
    textAlign: 'center',
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
  dayHeader: {
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 24,
    marginBottom: 16,
    color: '#374151',
  },
  timeLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#9ca3af',
    textAlign: 'center',
    marginVertical: 12,
    textTransform: 'uppercase',
  },
  activityHeader: {
    alignItems: 'center',
    marginVertical: 16,
  },
  activityLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
  },
  chatContainer1: {
    width: '100%',
    alignItems: 'flex-start',
  },
  chatContainer2: {
    width: '100%',
    alignItems: 'flex-end',
  },
  chatBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
    marginVertical: 4,
    marginHorizontal: 16,
  },
  chatBubble1: {
    backgroundColor: '#ddd6fe',
    borderBottomLeftRadius: 4,
  },
  chatBubble2: {
    backgroundColor: '#fce7f3',
    borderBottomRightRadius: 4,
  },
  chatBubbleHighlighted: {
    borderWidth: 3,
    borderColor: '#fbbf24',
    shadowColor: '#fbbf24',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.6,
    shadowRadius: 8,
    elevation: 8,
  },
  chatName: {
    fontSize: 11,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 8,
  },
  jsonContainer: {
    gap: 4,
  },
  jsonKey: {
    fontSize: 12,
    color: '#374151',
    fontFamily: 'monospace',
  },
  jsonValue: {
    fontSize: 12,
    color: '#059669',
    fontFamily: 'monospace',
  },
  jsonValueNumber: {
    fontSize: 12,
    color: '#8b5cf6',
    fontWeight: '600',
    fontFamily: 'monospace',
  },
  jsonFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  chatEmotion: {
    fontSize: 14,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 24,
    maxWidth: '90%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#374151',
  },
  modalThought: {
    fontSize: 16,
    fontStyle: 'italic',
    color: '#4b5563',
    lineHeight: 24,
    marginBottom: 16,
  },
  modalHint: {
    fontSize: 12,
    color: '#9ca3af',
    textAlign: 'center',
  },
  assessmentContainer: {
    marginBottom: 20,
  },
  assessmentContainerLast: {
    marginBottom: 0,
  },
  assessmentName: {
    fontSize: 16,
    fontWeight: '700',
    color: '#374151',
    marginBottom: 8,
  },
  assessmentText: {
    fontSize: 15,
    fontStyle: 'italic',
    color: '#4b5563',
    lineHeight: 22,
    marginBottom: 12,
    paddingLeft: 12,
    borderLeftWidth: 3,
    borderLeftColor: '#e5e7eb',
  },
  assessmentFondness: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  assessmentFondnessLabel: {
    fontSize: 13,
    color: '#6b7280',
  },
  assessmentFondnessValue: {
    fontSize: 15,
    fontWeight: '700',
  },
  suggestionsSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 16,
    lineHeight: 20,
  },
  suggestionsContainer: {
    gap: 12,
  },
  suggestionItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#f9fafb',
    padding: 12,
    borderRadius: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#8b5cf6',
  },
  suggestionNumber: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#8b5cf6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
    marginTop: 2,
  },
  suggestionNumberText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '700',
  },
  suggestionText: {
    flex: 1,
    fontSize: 14,
    color: '#374151',
    lineHeight: 20,
  },
  breakdownContainer: {
    marginTop: 8,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: 'rgba(0, 0, 0, 0.1)',
  },
  breakdownTitle: {
    fontSize: 11,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 4,
  },
  breakdownItem: {
    fontSize: 11,
    color: '#374151',
    fontFamily: 'monospace',
    marginBottom: 2,
  },
  breakdownValue: {
    fontSize: 11,
    fontWeight: '700',
    fontFamily: 'monospace',
  },
});
