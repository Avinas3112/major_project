import React, { useState } from 'react';
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