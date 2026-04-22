import os

app_content = """import React, { useState } from 'react';
import { Activity, MessageSquare, Calendar, User, ChevronRight, FileText } from 'lucide-react';
import Dashboard from './components/Dashboard';
import Chatbot from './components/Chatbot';
import TelehealthMockup from './components/TelehealthMockup';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-slate-300 flex flex-col">
        <div className="p-6 flex items-center gap-3 text-white border-b border-slate-800">
          <Activity className="w-8 h-8 text-blue-500" />
          <h1 className="text-xl font-bold">HealthPredict AI</h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setActiveTab('dashboard')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800'}`}
          >
            <Activity className="w-5 h-5" /> Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('chat')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'chat' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800'}`}
          >
            <MessageSquare className="w-5 h-5" /> AI Triage Nurse
          </button>
          <button 
            onClick={() => setActiveTab('telehealth')} 
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'telehealth' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800'}`}
          >
            <Calendar className="w-5 h-5" /> Telehealth & Booking
          </button>
        </nav>
        <div className="p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 px-4 py-3">
            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
              <User className="w-5 h-5 text-slate-400" />
            </div>
            <div>
              <p className="text-sm font-medium text-white">Patient View</p>
              <p className="text-xs text-slate-500">John Doe</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-semibold text-slate-800 capitalize">
            {activeTab === 'chat' ? 'AI Triage Setup' : activeTab}
          </h2>
          <div className="flex items-center gap-4 text-sm text-slate-500">
            <span>Powered by Advanced XAI Models</span>
          </div>
        </header>
        <main className="p-8">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'chat' && <Chatbot />}
          {activeTab === 'telehealth' && <TelehealthMockup />}
        </main>
      </div>
    </div>
  );
}
"""

dashboard_content = """import React, { useState } from 'react';
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
      const response = await axios.post('http://localhost:5000/predict', {
        features: formData,
        symptoms: "mild headache and slight fever" // Placeholder for fusion
      });
      setPrediction(response.data);
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
            <div className={`p-4 rounded-lg flex items-center justify-between ${prediction.severity.level === 'high' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'}`}>
              <div>
                <p className="text-sm font-medium uppercase tracking-wider">Severity Level</p>
                <p className="text-2xl font-bold">{prediction.severity.level}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium uppercase tracking-wider">Fusion Risk</p>
                <p className="text-2xl font-bold">{(prediction.fusion_score * 100).toFixed(1)}%</p>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-slate-700 mb-2">Recommended Specialists</h4>
              <div className="space-y-2">
                {prediction.recommended_doctors.map((doc, idx) => (
                  <div key={idx} className="flex justify-between items-center p-3 bg-slate-50 border border-slate-100 rounded-lg">
                    <div>
                      <p className="font-medium text-slate-800">{doc.name}</p>
                      <p className="text-sm text-slate-500">{doc.specialty}</p>
                    </div>
                    <p className="text-sm font-medium text-blue-600">{doc.match_score * 100}% Match</p>
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
"""

chatbot_content = """import React, { useState } from 'react';
import axios from 'axios';
import { Send, Bot, User } from 'lucide-react';

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I am your AI Triage Nurse. Please describe your symptoms in detail, and I will extract the medical features for prediction.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Mocking the endpoint until backend is fully hooked up for LLM parsing
      const response = await axios.post('http://localhost:5000/chatbot_extract', { text: input });
      setMessages(prev => [...prev, { role: 'bot', text: `Extracted Symptoms: ${response.data.extracted_symptoms.join(', ')}. We recommend running a full analysis on the Dashboard.` }]);
    } catch (error) {
      setTimeout(() => {
        setMessages(prev => [...prev, { role: 'bot', text: "I've analyzed your input. These sound like symptoms of concern. I've noted them for the doctor. We recommend booking a Telehealth appointment immediately." }]);
      }, 1000);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto bg-white border border-slate-200 rounded-xl shadow-sm h-[600px] flex flex-col">
      <div className="p-4 border-b border-slate-200 bg-slate-50 rounded-t-xl flex items-center gap-3">
        <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
          <Bot size={24} />
        </div>
        <div>
          <h3 className="font-semibold text-slate-800">AI Triage Assistant</h3>
          <p className="text-xs text-green-600 font-medium">Online - Powered by Advanced NLP</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'bot' && <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0"><Bot size={16} className="text-blue-600"/></div>}
            <div className={`p-3 rounded-lg max-w-[75%] ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-slate-100 text-slate-800 rounded-tl-none'}`}>
              <p className="text-sm">{msg.text}</p>
            </div>
            {msg.role === 'user' && <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0"><User size={16} className="text-white"/></div>}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0"><Bot size={16} className="text-blue-600"/></div>
            <div className="p-3 rounded-lg bg-slate-100 text-slate-800 rounded-tl-none flex items-center gap-2">
              <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-slate-200">
        <form onSubmit={handleSend} className="flex gap-2">
          <input 
            type="text" 
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your symptoms here... (e.g., I have a strong headache and nausea)"
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button type="submit" disabled={!input.trim() || isLoading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-lg transition-colors flex items-center justify-center">
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}
"""

telehealth_content = """import React, { useState } from 'react';
import { Calendar as CalendarIcon, Video, Clock, CheckCircle } from 'lucide-react';

export default function TelehealthMockup() {
  const [booked, setBooked] = useState(false);

  const availableSlots = [
    { time: '09:00 AM', doctor: 'Dr. Sarah Jenkins', specialty: 'Cardiologist' },
    { time: '11:30 AM', doctor: 'Dr. Michael Chen', specialty: 'General Physician' },
    { time: '02:00 PM', doctor: 'Dr. Emily Rodriguez', specialty: 'Neurologist' },
    { time: '04:15 PM', doctor: 'Dr. James Smith', specialty: 'Endocrinologist' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold text-slate-800 flex items-center gap-2">
            <Video className="text-blue-600" /> Virtual Care
          </h3>
          <p className="text-slate-500 mt-1">Book an instant telehealth consultation based on your AI risk score.</p>
        </div>
        <div className="bg-red-50 text-red-700 px-4 py-2 rounded-lg border border-red-200 flex items-center gap-2">
           <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </span>
          High Risk Detected - Priority Booking Unlocked
        </div>
      </div>

      {!booked ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {availableSlots.map((slot, idx) => (
            <div key={idx} className="bg-white border border-slate-200 rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="font-semibold text-lg text-slate-800">{slot.doctor}</h4>
                  <p className="text-blue-600 text-sm font-medium">{slot.specialty}</p>
                </div>
                <div className="bg-slate-100 text-slate-700 px-3 py-1 rounded-md text-sm font-medium flex items-center gap-2">
                  <Clock size={16}/> {slot.time}
                </div>
              </div>
              <button 
                onClick={() => setBooked(true)}
                className="w-full mt-4 py-2 border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-medium rounded-lg transition-colors"
              >
                Book Appointment
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-green-50 border border-green-200 rounded-xl p-12 text-center flex flex-col items-center">
          <CheckCircle size={64} className="text-green-500 mb-4" />
          <h3 className="text-2xl font-bold text-green-800 mb-2">Appointment Confirmed!</h3>
          <p className="text-green-700">You will receive an email with the video link shortly.</p>
          <button 
            onClick={() => setBooked(false)}
            className="mt-6 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
          >
            View My Schedule
          </button>
        </div>
      )}
    </div>
  );
}
"""

base = "modern_frontend/src"
with open(f"{base}/App.jsx", "w") as f:
    f.write(app_content)
with open(f"{base}/components/Dashboard.jsx", "w") as f:
    f.write(dashboard_content)
with open(f"{base}/components/Chatbot.jsx", "w") as f:
    f.write(chatbot_content)
with open(f"{base}/components/TelehealthMockup.jsx", "w") as f:
    f.write(telehealth_content)

print("Modern React UI files created successfully.")
