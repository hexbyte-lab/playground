import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';
import {
  Alert,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

type Habit = {
  id: string;
  name: string;
  streak: number;
  completedToday: boolean;
};

const DEFAULT_HABITS: Habit[] = [
  { id: '1', name: 'Exercise', streak: 5, completedToday: false },
  { id: '2', name: 'Read 30 min', streak: 12, completedToday: false },
  { id: '3', name: 'Meditate', streak: 3, completedToday: false },
  { id: '4', name: 'Drink 2L water', streak: 7, completedToday: false },
  { id: '5', name: 'No phone before 9am', streak: 2, completedToday: false },
];

export default function App() {
  const [habits, setHabits] = useState<Habit[]>(DEFAULT_HABITS);
  const [newHabitName, setNewHabitName] = useState('');

  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });

  const completed = habits.filter((h) => h.completedToday).length;
  const progress = habits.length > 0 ? completed / habits.length : 0;

  function toggleHabit(id: string) {
    setHabits((prev) =>
      prev.map((h) => {
        if (h.id !== id) return h;
        const completedToday = !h.completedToday;
        return {
          ...h,
          completedToday,
          streak: completedToday ? h.streak + 1 : Math.max(0, h.streak - 1),
        };
      })
    );
  }

  function addHabit() {
    const name = newHabitName.trim();
    if (!name) return;
    if (habits.some((h) => h.name.toLowerCase() === name.toLowerCase())) {
      Alert.alert('Duplicate', 'A habit with that name already exists.');
      return;
    }
    setHabits((prev) => [
      ...prev,
      { id: Date.now().toString(), name, streak: 0, completedToday: false },
    ]);
    setNewHabitName('');
  }

  function deleteHabit(id: string) {
    Alert.alert('Delete habit?', undefined, [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Delete',
        style: 'destructive',
        onPress: () => setHabits((prev) => prev.filter((h) => h.id !== id)),
      },
    ]);
  }

  return (
    <KeyboardAvoidingView
      style={styles.root}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <StatusBar style="light" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.dateText}>{today}</Text>
        <Text style={styles.title}>Habit Tracker</Text>

        {/* Progress bar */}
        <View style={styles.progressBarBg}>
          <View style={[styles.progressBarFill, { flex: progress }]} />
        </View>
        <Text style={styles.progressLabel}>
          {completed} / {habits.length} done today
        </Text>
      </View>

      {/* Habit list */}
      <FlatList
        data={habits}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <Pressable
            style={[styles.card, item.completedToday && styles.cardDone]}
            onPress={() => toggleHabit(item.id)}
            onLongPress={() => deleteHabit(item.id)}
          >
            <View style={[styles.checkbox, item.completedToday && styles.checkboxDone]}>
              {item.completedToday && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={[styles.habitName, item.completedToday && styles.habitNameDone]}>
              {item.name}
            </Text>
            <View style={styles.streakBadge}>
              <Text style={styles.streakText}>🔥 {item.streak}</Text>
            </View>
          </Pressable>
        )}
      />

      {/* Add habit */}
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="New habit…"
          placeholderTextColor="#888"
          value={newHabitName}
          onChangeText={setNewHabitName}
          onSubmitEditing={addHabit}
          returnKeyType="done"
        />
        <Pressable style={styles.addButton} onPress={addHabit}>
          <Text style={styles.addButtonText}>+</Text>
        </Pressable>
      </View>
    </KeyboardAvoidingView>
  );
}

const PURPLE = '#7C4DFF';
const PURPLE_LIGHT = '#B39DDB';
const BG = '#12121A';
const CARD = '#1E1E2E';
const CARD_DONE = '#1A2A1A';

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: BG,
  },
  header: {
    paddingTop: 60,
    paddingHorizontal: 24,
    paddingBottom: 20,
    backgroundColor: CARD,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  dateText: {
    color: PURPLE_LIGHT,
    fontSize: 13,
    marginBottom: 4,
  },
  title: {
    color: '#fff',
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 16,
  },
  progressBarBg: {
    height: 8,
    backgroundColor: '#333',
    borderRadius: 4,
    flexDirection: 'row',
    overflow: 'hidden',
  },
  progressBarFill: {
    backgroundColor: PURPLE,
    borderRadius: 4,
  },
  progressLabel: {
    color: PURPLE_LIGHT,
    fontSize: 12,
    marginTop: 6,
  },
  listContent: {
    padding: 16,
    gap: 10,
  },
  card: {
    backgroundColor: CARD,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 14,
  },
  cardDone: {
    backgroundColor: CARD_DONE,
  },
  checkbox: {
    width: 26,
    height: 26,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: PURPLE,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkboxDone: {
    backgroundColor: PURPLE,
    borderColor: PURPLE,
  },
  checkmark: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
  },
  habitName: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
  },
  habitNameDone: {
    color: '#666',
    textDecorationLine: 'line-through',
  },
  streakBadge: {
    backgroundColor: '#2A2A3E',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  streakText: {
    color: '#fff',
    fontSize: 13,
  },
  inputRow: {
    flexDirection: 'row',
    gap: 10,
    padding: 16,
    paddingBottom: 32,
    backgroundColor: CARD,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
  },
  input: {
    flex: 1,
    backgroundColor: '#2A2A3E',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    color: '#fff',
    fontSize: 15,
  },
  addButton: {
    backgroundColor: PURPLE,
    borderRadius: 12,
    width: 48,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addButtonText: {
    color: '#fff',
    fontSize: 24,
    lineHeight: 28,
  },
});
