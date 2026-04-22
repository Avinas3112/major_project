import os

file_path = os.path.join("backend", "app", "main.py")

with open(file_path, "r", encoding="utf-8") as f:
    orig = f.read()

# Assuming the file ends with:
# if __name__ == '__main__':
#     # Train mock models to ensure they exist
#     os.makedirs('backend/models_saved', exist_ok=True)
#     ...
#     # Run Flask app
#     print("Starting Flask API server...")
#     app.run(host=API_HOST, port=API_PORT, debug=API_DEBUG)

insertion = """

@app.route('/chatbot_extract', methods=['POST'])
def chatbot_extract():
    \"\"\"Mock endpoint to extract symptoms from text using basic NLP pattern.\"\"\"
    try:
        data = request.json
        text = data.get('text', '').lower()
        
        keywords = {
            'headache': 'Headache', 'fever': 'Fever', 'nausea': 'Nausea',
            'cough': 'Cough', 'fatigue': 'Fatigue', 'dizzy': 'Dizziness',
            'pain': 'Pain', 'breath': 'Shortness of Breath'
        }
        
        extracted = [v for k, v in keywords.items() if k in text]
        if not extracted: extracted.append('Unspecified Symptom')
            
        return jsonify({'extracted_symptoms': extracted, 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/book_telehealth', methods=['POST'])
def book_telehealth():
    \"\"\"Mock endpoint to process telehealth appointments.\"\"\"
    try:
        data = request.json
        doc_id = data.get('doctor_id', 'unknown')
        return jsonify({
            'status': 'confirmed',
            'message': 'Appointment booked successfully.',
            'meeting_link': f'https://meet.healthapp.ai/mock-{doc_id}',
            'success': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""

# Insert before if __name__
if "if __name__ == '__main__':" in orig:
    new_content = orig.replace("if __name__ == '__main__':", insertion + "if __name__ == '__main__':")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Injected successfully.")
else:
    print("Could not find __main__")
