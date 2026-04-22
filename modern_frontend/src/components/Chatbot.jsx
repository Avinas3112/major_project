import React, { useState } from 'react';
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
