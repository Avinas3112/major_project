import React, { useState } from 'react';
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
