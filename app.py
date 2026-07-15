from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from chatbot import HospitalChatbot
from database import db
from config import Config

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize chatbot
chatbot = HospitalChatbot()

# Store user sessions
user_sessions = {}

@app.before_request
def before_request():
    """Initialize user session if not exists"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        user_id = str(uuid.uuid4())
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'created_at': str(uuid.uuid4()),
            'conversation_history': []
        }

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Hospital Chatbot API',
        'version': '1.0.0'
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = request.headers.get('X-User-ID', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Generate response from chatbot
        result = chatbot.generate_response(user_id, user_message)
        bot_response = result['response']
        
        # Save conversation to database
        db.save_conversation(user_id, user_message, bot_response)
        
        # Save appointment if confirmed
        if result.get('state') == 'appointment_confirmed':
            appointment_id = db.save_appointment(result.get('appointment_data'))
            result['appointment_id'] = appointment_id
        
        # Add to conversation history
        if user_id in user_sessions:
            user_sessions[user_id]['conversation_history'].append({
                'user_message': user_message,
                'bot_response': bot_response,
                'intent': result.get('intent')
            })
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'user_message': user_message,
            'bot_response': bot_response,
            'intent': result.get('intent'),
            'state': result.get('state'),
            'appointment_data': result.get('appointment_data'),
            'appointment_id': result.get('appointment_id')
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversation/<user_id>', methods=['GET'])
def get_conversation(user_id):
    """Get conversation history for a user"""
    try:
        history = db.get_conversation_history(user_id)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'conversation_history': [
                {
                    'user_message': h.get('user_message'),
                    'bot_response': h.get('bot_response'),
                    'timestamp': str(h.get('timestamp'))
                }
                for h in history
            ]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/appointments/<user_id>', methods=['GET'])
def get_appointments(user_id):
    """Get appointments for a user"""
    try:
        appointments = db.get_appointments(user_id)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'appointments': [
                {
                    'id': str(a.get('_id')),
                    'name': a.get('name'),
                    'doctor': a.get('doctor'),
                    'department': a.get('department'),
                    'date': a.get('date'),
                    'time': a.get('time'),
                    'status': a.get('status'),
                    'created_at': str(a.get('created_at'))
                }
                for a in appointments
            ]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get available departments and doctors"""
    try:
        departments_info = {}
        for dept, doctors in Config.DOCTORS.items():
            departments_info[dept] = doctors
        
        return jsonify({
            'success': True,
            'departments': departments_info,
            'available_slots': Config.AVAILABLE_SLOTS
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hospital-info', methods=['GET'])
def hospital_info():
    """Get hospital information"""
    return jsonify({
        'success': True,
        'hospital_name': Config.HOSPITAL_NAME,
        'phone': '+1-800-HOSPITAL',
        'email': 'info@cityhospital.com',
        'address': '123 Medical Plaza, Healthcare City',
        'hours': {
            'weekday': '8:00 AM - 8:00 PM',
            'saturday': '9:00 AM - 5:00 PM',
            'sunday': 'Closed'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🏥 Hospital Chatbot API Starting...")
    print(f"🔧 Environment: {Config.FLASK_ENV}")
    print(f"🤖 Model: {Config.MODEL_NAME}")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
