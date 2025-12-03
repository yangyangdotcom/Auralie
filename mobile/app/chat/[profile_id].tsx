import { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { useLocalSearchParams, Stack } from 'expo-router';
import { startChat, sendChatMessage } from '../../src/services/api';

interface Message {
  id: string;
  isUser: boolean;
  message: string;
  emotion?: string;
  internal_thought?: string;
  fondness_level?: number;
  fondness_change?: number;
}

export default function ChatScreen() {
  const { profile_id } = useLocalSearchParams<{ profile_id: string }>();
  const [chatId, setChatId] = useState<string | null>(null);
  const [profileName, setProfileName] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [currentFondness, setCurrentFondness] = useState(50);
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      const response = await startChat(profile_id);
      setChatId(response.data.chat_id);
      setProfileName(response.data.profile_name);
      setCurrentFondness(response.data.initial_fondness);
    } catch (error) {
      console.error('Failed to start chat:', error);
    } finally {
      setInitializing(false);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim() || !chatId || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      isUser: true,
      message: inputText.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    // Scroll to bottom
    setTimeout(() => flatListRef.current?.scrollToEnd(), 100);

    try {
      const response = await sendChatMessage(chatId, userMessage.message);
      const twinMessage: Message = {
        id: (Date.now() + 1).toString(),
        isUser: false,
        message: response.data.message,
        emotion: response.data.emotion,
        internal_thought: response.data.internal_thought,
        fondness_level: response.data.fondness_level,
        fondness_change: response.data.fondness_change,
      };

      setMessages((prev) => [...prev, twinMessage]);
      setCurrentFondness(response.data.fondness_level);

      // Scroll to bottom after twin responds
      setTimeout(() => flatListRef.current?.scrollToEnd(), 100);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEmotionEmoji = (emotion?: string) => {
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
    return emotion ? emotions[emotion.toLowerCase()] || '😐' : '😐';
  };

  const getFondnessColor = (fondness: number) => {
    if (fondness >= 80) return '#10b981';
    if (fondness >= 60) return '#3b82f6';
    if (fondness >= 40) return '#f59e0b';
    return '#ef4444';
  };

  const renderMessage = ({ item }: { item: Message }) => {
    if (item.isUser) {
      return (
        <View style={styles.userMessageContainer}>
          <View style={styles.userBubble}>
            <Text style={styles.userName}>You</Text>
            <Text style={styles.messageText}>{item.message}</Text>
          </View>
        </View>
      );
    }

    return (
      <View style={styles.twinMessageContainer}>
        <View style={styles.twinBubble}>
          <Text style={styles.twinName}>{profileName}</Text>
          <View style={styles.jsonContainer}>
            <Text style={styles.jsonKey}>
              message: <Text style={styles.jsonValue}>"{item.message}"</Text>
            </Text>
            <Text style={styles.jsonKey}>
              emotion: <Text style={styles.jsonValue}>"{item.emotion}"</Text>
            </Text>
            <Text style={styles.jsonKey}>
              internal_thought:{' '}
              <Text style={styles.jsonValue}>"{item.internal_thought}"</Text>
            </Text>
            <View style={styles.fondnessRow}>
              <Text style={styles.jsonKey}>
                fondness_level:{' '}
                <Text
                  style={[
                    styles.jsonValueNumber,
                    { color: getFondnessColor(item.fondness_level || 50) },
                  ]}
                >
                  {item.fondness_level}
                </Text>
              </Text>
              <Text style={styles.emotionEmoji}>
                {getEmotionEmoji(item.emotion)}
              </Text>
            </View>
            {item.fondness_change !== 0 && (
              <Text style={styles.fondnessChange}>
                {item.fondness_change > 0 ? '+' : ''}
                {item.fondness_change} fondness
              </Text>
            )}
          </View>
        </View>
      </View>
    );
  };

  if (initializing) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#8b5cf6" />
        <Text style={styles.loadingText}>Starting chat...</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: `Chat with ${profileName}`,
          headerStyle: { backgroundColor: '#8b5cf6' },
          headerTintColor: '#fff',
        }}
      />
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={100}
      >
        {/* Fondness Bar */}
        <View style={styles.fondnessBar}>
          <Text style={styles.fondnessLabel}>Fondness:</Text>
          <View style={styles.fondnessBarContainer}>
            <View
              style={[
                styles.fondnessBarFill,
                {
                  width: `${currentFondness}%`,
                  backgroundColor: getFondnessColor(currentFondness),
                },
              ]}
            />
          </View>
          <Text style={[styles.fondnessValue, { color: getFondnessColor(currentFondness) }]}>
            {currentFondness}
          </Text>
        </View>

        {/* Messages */}
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.messagesList}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
        />

        {/* Input */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Type your message..."
            value={inputText}
            onChangeText={setInputText}
            multiline
            editable={!loading}
          />
          <TouchableOpacity
            style={[styles.sendButton, (loading || !inputText.trim()) && styles.sendButtonDisabled]}
            onPress={handleSend}
            disabled={loading || !inputText.trim()}
          >
            {loading ? (
              <ActivityIndicator color="#fff" size="small" />
            ) : (
              <Text style={styles.sendButtonText}>Send</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </>
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
  loadingText: {
    marginTop: 12,
    color: '#6b7280',
  },
  fondnessBar: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
    gap: 8,
  },
  fondnessLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
  },
  fondnessBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
  },
  fondnessBarFill: {
    height: '100%',
  },
  fondnessValue: {
    fontSize: 14,
    fontWeight: '700',
    minWidth: 30,
  },
  messagesList: {
    padding: 16,
    gap: 12,
  },
  userMessageContainer: {
    alignItems: 'flex-end',
  },
  userBubble: {
    backgroundColor: '#8b5cf6',
    borderRadius: 16,
    borderBottomRightRadius: 4,
    padding: 12,
    maxWidth: '80%',
  },
  userName: {
    fontSize: 11,
    fontWeight: '600',
    color: '#fff',
    opacity: 0.8,
    marginBottom: 4,
  },
  messageText: {
    fontSize: 15,
    color: '#fff',
  },
  twinMessageContainer: {
    alignItems: 'flex-start',
  },
  twinBubble: {
    backgroundColor: '#fff',
    borderRadius: 16,
    borderBottomLeftRadius: 4,
    padding: 12,
    maxWidth: '80%',
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  twinName: {
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
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  jsonValue: {
    fontSize: 12,
    color: '#059669',
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  jsonValueNumber: {
    fontSize: 12,
    fontWeight: '600',
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  fondnessRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  emotionEmoji: {
    fontSize: 16,
  },
  fondnessChange: {
    fontSize: 10,
    color: '#8b5cf6',
    fontWeight: '600',
    marginTop: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#f3f4f6',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    fontSize: 15,
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#8b5cf6',
    borderRadius: 20,
    paddingHorizontal: 20,
    paddingVertical: 10,
    justifyContent: 'center',
    alignItems: 'center',
    minWidth: 60,
  },
  sendButtonDisabled: {
    backgroundColor: '#d1d5db',
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 15,
  },
});
