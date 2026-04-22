import React, { useState } from 'react';
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
