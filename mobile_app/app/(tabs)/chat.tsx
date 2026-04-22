import React, { useState } from 'react';
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
  inputArea: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  input: { flex: 1, borderWidth: 1, borderColor: '#cbd5e1', padding: 10, borderRadius: 20, marginRight: 10 },
  sendButton: { backgroundColor: '#2563eb', paddingVertical: 10, paddingHorizontal: 15, borderRadius: 20 },
  sendText: { color: 'white', fontWeight: 'bold' }
});