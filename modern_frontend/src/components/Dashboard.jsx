import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { name: 'Jan', risk: 10 },
  { name: 'Feb', risk: 15 },
  { name: 'Mar', risk: 12 },
  { name: 'Apr', risk: 25 },
  { name: 'May', risk: 40 },
  { name: 'Jun', risk: 35 },
];

export default function Dashboard() {
  const [formData, setFormData] = useState({
    age: 45, gender: 1, bmi: 26.5, systolic_bp: 130, diastolic_bp: 85, blood_sugar: 105
  });
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict_disease', {
        ...formData,
        symptoms: "mild headache and slight fever" // Placeholder for fusion
      });
      
      // Get doctor recommendation based on prediction_id
      const predictionData = response.data;
      if (predictionData.success && predictionData.prediction_id) {
        try {
          const docResponse = await axios.post('http://localhost:5000/recommend_doctor', {
            prediction_id: predictionData.prediction_id
          });
          predictionData.recommended_doctors = docResponse.data.recommendations.map(r => ({
            name: r.specialist,
            specialty: r.specialist,
            match_score: r.relevance_score
          }));
        } catch (docErr) {
          console.error("Could not fetch doctors", docErr);
        }
      }
      setPrediction(predictionData);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Input Form */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">Patient Health Data</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {Object.keys(formData).map(key => (
              <div key={key}>
                <label className="block text-sm font-medium text-slate-600 capitalize mb-1">
                  {key.replace('_', ' ')}
                </label>
                <input 
                  type="number" 
                  step="0.1"
                  value={formData[key]} 
                  onChange={e => setFormData({...formData, [key]: parseFloat(e.target.value)})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            ))}
          </div>
          <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
            Run AI Analysis
          </button>
        </form>
      </div>

      {/* Results Panel */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">AI Prediction Results</h3>
        {prediction ? (
          <div className="space-y-6">
            <div className={`p-4 rounded-lg flex items-center justify-between ${prediction?.severity?.level === 'high' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'}`}>
              <div>
                <p className="text-sm font-medium uppercase tracking-wider">Severity Level</p>
                <p className="text-2xl font-bold">{prediction?.severity?.level || 'N/A'}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium uppercase tracking-wider">Fusion Risk</p>
                <p className="text-2xl font-bold">{prediction.fusion_score != null ? (prediction.fusion_score * 100).toFixed(1) : 0}%</p>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-slate-700 mb-2">Recommended Specialists</h4>
              <div className="space-y-2">
                {prediction?.recommended_doctors?.map((doc, idx) => (
                  <div key={idx} className="flex justify-between items-center p-3 bg-slate-50 border border-slate-100 rounded-lg">
                    <div>
                      <p className="font-medium text-slate-800">{doc.name}</p>
                      <p className="text-sm text-slate-500">{doc.specialty}</p>
                    </div>
                    <p className="text-sm font-medium text-blue-600">{doc.match_score ? (doc.match_score * 100).toFixed(0) : 0}% Match</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="h-48 flex items-center justify-center text-slate-400">
            <p>Enter patient data and run analysis to see results.</p>
          </div>
        )}
      </div>

      {/* Time-Series Chart */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 lg:col-span-2">
         <h3 className="text-lg font-semibold text-slate-800 mb-4">Historical Risk Trajectory</h3>
         <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                <Line type="monotone" dataKey="risk" stroke="#3b82f6" strokeWidth={3} dot={{r: 4, strokeWidth: 2}} activeDot={{r: 6}} />
              </LineChart>
            </ResponsiveContainer>
         </div>
      </div>
    </div>
  );
}
