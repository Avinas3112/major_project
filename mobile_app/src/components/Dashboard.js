import React, { useState } from 'react';
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
