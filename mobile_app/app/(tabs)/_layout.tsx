import { Tabs } from 'expo-router';
import { ActivityIndicator, StyleSheet } from 'react-native';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#2563eb', headerShown: true }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Dashboard',
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: 'AI Triage',
        }}
      />
      <Tabs.Screen
        name="telehealth"
        options={{
          title: 'Telehealth',
        }}
      />
    </Tabs>
  );
}
