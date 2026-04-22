import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import axios from 'axios';

// Replace string with your local IP like localhost! 
const API_URL = 'http://192.168.29.23:5000'; 

export default function Dashboard() {
  const [formData, setFormData] = useState({
    symptoms: '', age: '30', gender: '1'
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!formData.symptoms.trim()) {
      Alert.alert('Missing Info', 'Please describe your symptoms.');
      return;
    }
    
    setLoading(true);
    try {
      const payload = {
        age: parseFloat(formData.age), 
        gender: parseInt(formData.gender),
        symptoms: formData.symptoms,
        // Using medical averages for unrequired fields
        systolic_bp: 120, 
        diastolic_bp: 80,
        blood_sugar: 100,
        height: 170,
        weight: 70
      };

      const response = await axios.post(`${API_URL}/predict_disease`, payload);
      
      const predictionData = response.data;
      if (predictionData.success && predictionData.prediction_id) {
        try {
          const docResponse = await axios.post(`${API_URL}/recommend_doctor`, { prediction_id: predictionData.prediction_id });
          predictionData.recommended_doctors = docResponse.data.recommendations.map((r: any) => ({
            name: r.specialist, match_score: r.relevance_score
          }));
          
          const explainResponse = await axios.post(`${API_URL}/explain_prediction`, { prediction_id: predictionData.prediction_id });
          if (explainResponse.data.success) {
            predictionData.explanation = explainResponse.data.explanation;
          }
        } catch (e) { console.log(e); }
      }
      setPrediction(predictionData);
    } catch (error) {
      console.error(error);
      Alert.alert('Network Error', 'Could not connect to backend server. Make sure API_URL matches your laptop IP.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Patient Health Data</Text>
      <View style={styles.formContainer}>
        {['symptoms', 'age', 'gender'].map(key => (
          <View key={key} style={styles.inputGroup}>
            <Text style={styles.label}>{key}</Text>
            {key === 'gender' ? (
              <View style={styles.dropdownContainer}>
                <TouchableOpacity 
                  style={[styles.dropdownOption, formData.gender === '1' && styles.dropdownOptionSelected]}
                  onPress={() => setFormData({...formData, gender: '1'})}
                >
                  <Text style={[styles.dropdownText, formData.gender === '1' && styles.dropdownTextSelected]}>Male</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                  style={[styles.dropdownOption, formData.gender === '0' && styles.dropdownOptionSelected]}
                  onPress={() => setFormData({...formData, gender: '0'})}
                >
                  <Text style={[styles.dropdownText, formData.gender === '0' && styles.dropdownTextSelected]}>Female</Text>
                </TouchableOpacity>
              </View>
            ) : key === 'symptoms' ? (
              <TextInput 
                style={[styles.input, { minHeight: 80, textAlignVertical: 'top' }]} 
                value={(formData as any)[key]} 
                onChangeText={t => setFormData({...formData, [key]: t})}
                placeholder="E.g., mild headache, fever, cough..."
                multiline
              />
            ) : (
              <TextInput 
                style={styles.input} 
                value={(formData as any)[key]} 
                onChangeText={t => setFormData({...formData, [key]: t})}
                keyboardType="numeric"
              />
            )}
          </View>
        ))}
        <TouchableOpacity style={styles.button} onPress={handleSubmit} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Run AI Analysis</Text>}
        </TouchableOpacity>
      </View>

      {prediction && (
        <View style={styles.resultContainer}>
          <Text style={styles.title}>Prediction Results</Text>
          <View style={[styles.card, (prediction as any).severity?.level === 'high' ? styles.cardRed : styles.cardGreen]}>
            <Text style={styles.resultText}>Severity: {(prediction as any).severity?.level}</Text>
            <Text style={styles.resultText}>Fusion Risk: {(prediction as any).fusion_score ? ((prediction as any).fusion_score * 100).toFixed(1) : 0}%</Text>
            
            <Text style={styles.subTitle}>Top Diseases:</Text>
            {(prediction as any).top_diseases?.map((d: any, i: number) => (
              <Text key={`disease-${i}`} style={styles.itemText}>• {d.disease} ({(d.probability * 100).toFixed(1)}%)</Text>
            ))}

            {(prediction as any).explanation && (
              <>
                <Text style={styles.subTitle}>AI Explanation:</Text>
                <Text style={styles.explanationText}>{(prediction as any).explanation}</Text>
              </>
            )}

            <Text style={styles.subTitle}>Recommended Specialists:</Text>
            {(prediction as any).recommended_doctors?.map((doc: any, idx: number) => (
              <Text key={`doc-${idx}`} style={styles.itemText}>• {doc.name} ({(doc.match_score * 100).toFixed(0)}% match)</Text>
            ))}
          </View>
        </View>
      )}
      <View style={{height: 100}} />
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
  dropdownContainer: { flexDirection: 'row', justifyContent: 'space-between', gap: 10 },
  dropdownOption: { flex: 1, padding: 10, borderWidth: 1, borderColor: '#cbd5e1', borderRadius: 5, alignItems: 'center' },
  dropdownOptionSelected: { backgroundColor: '#2563eb', borderColor: '#2563eb' },
  dropdownText: { color: '#64748b' },
  dropdownTextSelected: { color: 'white', fontWeight: 'bold' },
  button: { backgroundColor: '#2563eb', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 10 },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
  resultContainer: { backgroundColor: 'white', padding: 15, borderRadius: 10, elevation: 2, marginBottom: 40 },
  card: { padding: 15, borderRadius: 8 },
  cardRed: { backgroundColor: '#fef2f2', borderColor: '#fca5a5', borderWidth: 1 },
  cardGreen: { backgroundColor: '#f0fdf4', borderColor: '#86efac', borderWidth: 1 },
  resultText: { fontSize: 16, fontWeight: 'bold', marginBottom: 5 },
  subTitle: { fontSize: 15, fontWeight: '600', marginTop: 10, marginBottom: 5 },
  itemText: { fontSize: 14, color: '#334', paddingVertical: 2 },
  explanationText: { fontSize: 14, color: '#475569', fontStyle: 'italic', backgroundColor: '#f8fafc', padding: 10, borderRadius: 5, marginTop: 5 }
});
