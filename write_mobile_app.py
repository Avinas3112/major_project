import os

base_dir = "mobile_app/src/components"
os.makedirs(base_dir, exist_ok=True)

app_js = '''import React, { useState } from 'react';
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
'''

dashboard_js = '''import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

const API_URL = 'http://192.168.29.23:5000'; // Make sure this matches backend accessible IP

export default function Dashboard() {
  const [formData, setFormData] = useState({
    age: '45', gender: '1', bmi: '26.5', systolic_bp: '130', diastolic_bp: '85', blood_sugar: '105'
  });
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async () => {
    try {
      const payload = {
        age: parseFloat(formData.age), gender: parseInt(formData.gender), bmi: parseFloat(formData.bmi),
        systolic_bp: parseFloat(formData.systolic_bp), diastolic_bp: parseFloat(formData.diastolic_bp),
        blood_sugar: parseFloat(formData.blood_sugar), symptoms: "mild headache and slight fever"
      };

      const response = await axios.post(`${API_URL}/predict_disease`, payload);
      
      const predictionData = response.data;
      if (predictionData.success && predictionData.prediction_id) {
        try {
          const docResponse = await axios.post(`${API_URL}/recommend_doctor`, { prediction_id: predictionData.prediction_id });
          predictionData.recommended_doctors = docResponse.data.recommendations.map(r => ({
            name: r.specialist, match_score: r.relevance_score
          }));
        } catch (e) { console.log(e); }
      }
      setPrediction(predictionData);
    } catch (error) {
      console.error(error);
      Alert.alert('Error', 'Failed to fetch prediction');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Patient Health Data</Text>
      <View style={styles.formContainer}>
        {['age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'blood_sugar'].map(key => (
          <View key={key} style={styles.inputGroup}>
            <Text style={styles.label}>{key}</Text>
            <TextInput 
              style={styles.input} 
              value={formData[key]} 
              onChangeText={t => setFormData({...formData, [key]: t})}
              keyboardType="numeric"
            />
          </View>
        ))}
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Run AI Analysis</Text>
        </TouchableOpacity>
      </View>

      {prediction && (
        <View style={styles.resultContainer}>
          <Text style={styles.title}>Prediction Results</Text>
          <View style={[styles.card, prediction?.severity?.level === 'high' ? styles.cardRed : styles.cardGreen]}>
            <Text style={styles.resultText}>Severity: {prediction?.severity?.level}</Text>
            <Text style={styles.resultText}>Fusion Risk: {prediction?.fusion_score ? (prediction.fusion_score * 100).toFixed(1) : 0}%</Text>
            
            <Text style={styles.subTitle}>Top Diseases:</Text>
            {prediction.top_diseases?.map((d, i) => (
              <Text key={i} style={styles.itemText}>• {d.disease} ({(d.probability * 100).toFixed(1)}%)</Text>
            ))}

            <Text style={styles.subTitle}>Recommended Specialists:</Text>
            {prediction.recommended_doctors?.map((doc, idx) => (
              <Text key={idx} style={styles.itemText}>• {doc.name} ({(doc.match_score * 100).toFixed(0)}% match)</Text>
            ))}
          </View>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  title: { fontSize: 18, fontWeight: 'bold', marginBottom: 10, color: '#334155' },
  formContainer: { backgroundColor: 'white', padding: 15, borderRadius: 10, elevation: 2, marginBottom: 20 },
  inputGroup: { marginBottom: 10 },
  label: { fontSize: 14, color: '#64748b', marginBottom: 5, textTransform: 'capitalize' },
  input: { borderWidth: 1, borderColor: '#cbd5e1', padding: 10, borderRadius: 5 },
  button: { backgroundColor: '#2563eb', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 10 },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
  resultContainer: { backgroundColor: 'white', padding: 15, borderRadius: 10, elevation: 2, marginBottom: 40 },
  card: { padding: 15, borderRadius: 8 },
  cardRed: { backgroundColor: '#fef2f2', borderColor: '#fca5a5', borderWidth: 1 },
  cardGreen: { backgroundColor: '#f0fdf4', borderColor: '#86efac', borderWidth: 1 },
  resultText: { fontSize: 16, fontWeight: 'bold', marginBottom: 5 },
  subTitle: { fontSize: 15, fontWeight: '600', marginTop: 10, marginBottom: 5 },
  itemText: { fontSize: 14, color: '#334' }
});
'''

chatbot_js = '''import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I am your AI Triage Nurse. Describe your symptoms.' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text: input }]);
    const currentInput = input;
    setInput('');
    
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'bot', 
        text: `Extracted Symptoms from "${currentInput}". We recommend running a full analysis on the Dashboard or booking a Telehealth appointment.`
      }]);
    }, 1500);
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.chatArea}>
        {messages.map((msg, idx) => (
          <View key={idx} style={[styles.messageBubble, msg.role === 'user' ? styles.userBubble : styles.botBubble]}>
            <Text style={[styles.messageText, msg.role === 'user' && styles.userText]}>{msg.text}</Text>
          </View>
        ))}
      </ScrollView>
      <View style={styles.inputArea}>
        <TextInput 
          style={styles.input} 
          value={input} 
          onChangeText={setInput} 
          placeholder="Type symptoms..." 
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
          <Text style={styles.sendText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: 'white', padding: 10 },
  chatArea: { flex: 1, marginBottom: 10 },
  messageBubble: { padding: 12, borderRadius: 8, maxWidth: '80%', marginBottom: 10 },
  botBubble: { backgroundColor: '#f1f5f9', alignSelf: 'flex-start' },
  userBubble: { backgroundColor: '#2563eb', alignSelf: 'flex-end' },
  messageText: { fontSize: 15, color: '#1e293b' },
  userText: { color: 'white' },
  inputArea: { flexDirection: 'row', alignItems: 'center' },
  input: { flex: 1, borderWidth: 1, borderColor: '#cbd5e1', padding: 10, borderRadius: 20, marginRight: 10 },
  sendButton: { backgroundColor: '#2563eb', paddingVertical: 10, paddingHorizontal: 15, borderRadius: 20 },
  sendText: { color: 'white', fontWeight: 'bold' }
});
'''

telehealth_js = '''import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';

const slots = [
  { time: '09:00 AM', doctor: 'Dr. Sarah Jenkins', spec: 'Cardiologist' },
  { time: '11:30 AM', doctor: 'Dr. Michael Chen', spec: 'General Physician' },
  { time: '02:00 PM', doctor: 'Dr. Emily Rodriguez', spec: 'Neurologist' },
];

export default function TelehealthMockup() {
  const [booked, setBooked] = useState(false);

  if (booked) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.successTitle}>Appointment Confirmed!</Text>
        <Text style={styles.successText}>You will receive an email shortly.</Text>
        <TouchableOpacity style={styles.button} onPress={() => setBooked(false)}>
          <Text style={styles.buttonText}>Back to Schedule</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.alertBox}>
        <Text style={styles.alertText}>Virtual Care - Book an instant consultation</Text>
      </View>
      
      {slots.map((s, idx) => (
        <View key={idx} style={styles.card}>
          <Text style={styles.docName}>{s.doctor}</Text>
          <Text style={styles.docSpec}>{s.spec}</Text>
          <Text style={styles.timeText}>{s.time}</Text>
          <TouchableOpacity style={styles.bookBtn} onPress={() => setBooked(true)}>
            <Text style={styles.bookBtnText}>Book Appointment</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  centerContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  alertBox: { backgroundColor: '#eff6ff', padding: 15, borderRadius: 8, marginBottom: 20 },
  alertText: { color: '#1e40af', fontWeight: '600', fontSize: 16 },
  card: { backgroundColor: 'white', padding: 15, borderRadius: 8, elevation: 2, marginBottom: 15 },
  docName: { fontSize: 18, fontWeight: 'bold', color: '#1e293b' },
  docSpec: { fontSize: 14, color: '#2563eb', marginBottom: 5 },
  timeText: { fontSize: 14, color: '#64748b', marginBottom: 10 },
  bookBtn: { borderWidth: 1, borderColor: '#2563eb', padding: 10, borderRadius: 5, alignItems: 'center' },
  bookBtnText: { color: '#2563eb', fontWeight: 'bold' },
  successTitle: { fontSize: 24, fontWeight: 'bold', color: '#16a34a', marginBottom: 10 },
  successText: { fontSize: 16, color: '#4b5563', marginBottom: 20 },
  button: { backgroundColor: '#16a34a', padding: 15, borderRadius: 8 },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});
'''

with open('mobile_app/App.js', 'w') as f:
    f.write(app_js)
with open('mobile_app/src/components/Dashboard.js', 'w') as f:
    f.write(dashboard_js)
with open('mobile_app/src/components/Chatbot.js', 'w') as f:
    f.write(chatbot_js)
with open('mobile_app/src/components/TelehealthMockup.js', 'w') as f:
    f.write(telehealth_js)
print("Mobile app files generated successfully.")
