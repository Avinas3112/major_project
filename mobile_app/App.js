import React, { useState } from 'react';
import { View, Text, TouchableOpacity, SafeAreaView, StyleSheet } from 'react-native';
import Dashboard from './src/components/Dashboard';
import Chatbot from './src/components/Chatbot';
import TelehealthMockup from './src/components/TelehealthMockup';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>HealthPredict AI</Text>
      </View>
      
      <View style={styles.content}>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'chat' && <Chatbot />}
        {activeTab === 'telehealth' && <TelehealthMockup />}
      </View>

      <View style={styles.tabBar}>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'dashboard' && styles.activeTab]}
          onPress={() => setActiveTab('dashboard')}>
          <Text style={[styles.tabText, activeTab === 'dashboard' && styles.activeTabText]}>Dashboard</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'chat' && styles.activeTab]}
          onPress={() => setActiveTab('chat')}>
          <Text style={[styles.tabText, activeTab === 'chat' && styles.activeTabText]}>Triage AI</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'telehealth' && styles.activeTab]}
          onPress={() => setActiveTab('telehealth')}>
          <Text style={[styles.tabText, activeTab === 'telehealth' && styles.activeTabText]}>Telehealth</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  header: { padding: 20, backgroundColor: '#0f172a', alignItems: 'center' },
  headerTitle: { color: 'white', fontSize: 20, fontWeight: 'bold' },
  content: { flex: 1 },
  tabBar: { flexDirection: 'row', borderTopWidth: 1, borderColor: '#e2e8f0', backgroundColor: 'white' },
  tab: { flex: 1, padding: 15, alignItems: 'center' },
  activeTab: { backgroundColor: '#eff6ff' },
  tabText: { color: '#64748b', fontWeight: '600' },
  activeTabText: { color: '#2563eb' }
});
