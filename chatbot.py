import random
from datetime import datetime, timedelta
from transformers import pipeline
from config import Config

class HospitalChatbot:
    """Hospital appointment booking chatbot"""
    
    def __init__(self):
        # Initialize sentiment analysis model from Hugging Face
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=Config.MODEL_NAME
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            self.sentiment_pipeline = None
        
        # Conversation state
        self.user_state = {}
        self.appointment_data = {}
    
    def get_user_state(self, user_id):
        """Get or initialize user state"""
        if user_id not in self.user_state:
            self.user_state[user_id] = {
                'step': 'greeting',
                'appointment_data': {}
            }
        return self.user_state[user_id]
    
    def detect_intent(self, user_message):
        """Detect user intent from message"""
        message_lower = user_message.lower()
        
        # Intent mapping
        intents = {
            'book_appointment': ['book', 'appointment', 'schedule', 'reserve', 'consultation'],
            'check_appointment': ['check', 'my appointment', 'status', 'confirm'],
            'cancel_appointment': ['cancel', 'remove', 'delete appointment'],
            'hospital_info': ['hospital', 'address', 'phone', 'hours', 'location'],
            'doctor_info': ['doctor', 'specialist', 'cardiologist', 'dermatologist', 'pediatrician'],
            'greeting': ['hi', 'hello', 'hey', 'greetings'],
            'goodbye': ['bye', 'goodbye', 'see you', 'exit', 'quit'],
        }
        
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return 'general_query'
    
    def get_sentiment(self, text):
        """Get sentiment of user message"""
        if not self.sentiment_pipeline:
            return 'neutral'
        
        try:
            result = self.sentiment_pipeline(text[:512])[0]
            return result['label'].lower()
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return 'neutral'
    
    def handle_booking_appointment(self, user_id, user_message):
        """Handle appointment booking flow"""
        state = self.get_user_state(user_id)
        step = state['step']
        
        if step == 'greeting':
            state['step'] = 'get_name'
            return {
                'response': "Great! I'd be happy to help you book an appointment. What's your name?",
                'state': 'awaiting_name'
            }
        
        elif step == 'get_name':
            state['appointment_data']['name'] = user_message.strip()
            state['step'] = 'get_phone'
            return {
                'response': f"Nice to meet you, {user_message}! What's your phone number?",
                'state': 'awaiting_phone'
            }
        
        elif step == 'get_phone':
            state['appointment_data']['phone'] = user_message.strip()
            state['step'] = 'get_email'
            return {
                'response': "Thank you! What's your email address?",
                'state': 'awaiting_email'
            }
        
        elif step == 'get_email':
            state['appointment_data']['email'] = user_message.strip()
            state['step'] = 'get_department'
            departments = ', '.join(Config.DOCTORS.keys())
            return {
                'response': f"Which department do you need? Available: {departments}",
                'state': 'awaiting_department'
            }
        
        elif step == 'get_department':
            department = user_message.lower().strip()
            if department in Config.DOCTORS:
                state['appointment_data']['department'] = department
                doctors = ', '.join(Config.DOCTORS[department])
                state['step'] = 'get_doctor'
                return {
                    'response': f"Doctors in {department}: {doctors}. Who would you prefer?",
                    'state': 'awaiting_doctor'
                }
            else:
                return {
                    'response': "Sorry, that department is not available. Please choose from: " + ', '.join(Config.DOCTORS.keys()),
                    'state': 'awaiting_department'
                }
        
        elif step == 'get_doctor':
            state['appointment_data']['doctor'] = user_message.strip()
            state['step'] = 'get_date'
            return {
                'response': "What date would you prefer? (Please use YYYY-MM-DD format)",
                'state': 'awaiting_date'
            }
        
        elif step == 'get_date':
            state['appointment_data']['date'] = user_message.strip()
            state['step'] = 'get_time'
            times = ', '.join(Config.AVAILABLE_SLOTS['morning'][:3])
            return {
                'response': f"What time would you prefer? Available slots: {times} (and more)",
                'state': 'awaiting_time'
            }
        
        elif step == 'get_time':
            state['appointment_data']['time'] = user_message.strip()
            state['step'] = 'get_reason'
            return {
                'response': "What's the reason for your visit?",
                'state': 'awaiting_reason'
            }
        
        elif step == 'get_reason':
            state['appointment_data']['reason'] = user_message.strip()
            state['appointment_data']['user_id'] = user_id
            
            # Prepare confirmation message
            data = state['appointment_data']
            confirmation = f"""
Please confirm your appointment details:
- Name: {data.get('name')}
- Phone: {data.get('phone')}
- Email: {data.get('email')}
- Department: {data.get('department')}
- Doctor: {data.get('doctor')}
- Date: {data.get('date')}
- Time: {data.get('time')}
- Reason: {data.get('reason')}

Please reply "yes" to confirm or "no" to cancel.
            """
            state['step'] = 'confirm_appointment'
            return {
                'response': confirmation,
                'state': 'awaiting_confirmation',
                'appointment_data': data
            }
        
        elif step == 'confirm_appointment':
            if user_message.lower() in ['yes', 'confirm', 'ok', 'sure']:
                state['step'] = 'greeting'
                return {
                    'response': "✅ Your appointment has been confirmed! You'll receive a confirmation email shortly. Appointment ID: APT-" + str(datetime.now().timestamp())[:10],
                    'state': 'appointment_confirmed',
                    'appointment_data': state['appointment_data']
                }
            else:
                state['step'] = 'greeting'
                state['appointment_data'] = {}
                return {
                    'response': "Appointment booking cancelled. How can I help you?",
                    'state': 'cancelled'
                }
    
    def generate_response(self, user_id, user_message):
        """Generate chatbot response"""
        intent = self.detect_intent(user_message)
        sentiment = self.get_sentiment(user_message)
        
        if intent == 'greeting':
            return {
                'response': f"👋 Hello! Welcome to {Config.HOSPITAL_NAME}. How can I help you today? You can book an appointment, check information, or ask any questions.",
                'intent': intent
            }
        
        elif intent == 'goodbye':
            return {
                'response': "👋 Thank you for visiting! Have a great day and take care!",
                'intent': intent
            }
        
        elif intent == 'book_appointment':
            result = self.handle_booking_appointment(user_id, user_message)
            result['intent'] = intent
            return result
        
        elif intent == 'hospital_info':
            hospital_info = f"""
📍 {Config.HOSPITAL_NAME}
📞 Phone: +1-800-HOSPITAL
📧 Email: info@cityhospital.com
🏥 Address: 123 Medical Plaza, Healthcare City
⏰ Hours: 
   - Monday to Friday: 8:00 AM - 8:00 PM
   - Saturday: 9:00 AM - 5:00 PM
   - Sunday: Closed
            """
            return {
                'response': hospital_info,
                'intent': intent
            }
        
        elif intent == 'doctor_info':
            doctors_info = "👨‍⚕️ Our Specialist Doctors:\n\n"
            for dept, doctors in Config.DOCTORS.items():
                doctors_info += f"🏥 {dept.capitalize()}: {', '.join(doctors)}\n"
            return {
                'response': doctors_info,
                'intent': intent
            }
        
        elif intent == 'check_appointment':
            return {
                'response': "To check your appointment status, please provide your appointment ID or phone number.",
                'intent': intent
            }
        
        else:
            responses = [
                "That's interesting! Can I help you with booking an appointment or getting hospital information?",
                "I'm here to help with hospital appointments and information. Would you like to book an appointment?",
                "Thanks for your message! Is there anything else I can help you with regarding hospital services?"
            ]
            return {
                'response': random.choice(responses),
                'intent': intent
            }
