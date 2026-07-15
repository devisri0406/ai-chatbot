from pymongo import MongoClient
from config import Config
from datetime import datetime

class Database:
    """Database manager for MongoDB"""
    
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.conversations = self.db['conversations']
            self.appointments = self.db['appointments']
            self.users = self.db['users']
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
    
    def save_conversation(self, user_id, user_message, bot_response):
        """Save conversation to database"""
        if not self.db:
            return False
        
        try:
            self.conversations.insert_one({
                'user_id': user_id,
                'user_message': user_message,
                'bot_response': bot_response,
                'timestamp': datetime.utcnow()
            })
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def save_appointment(self, appointment_data):
        """Save appointment to database"""
        if not self.db:
            return False
        
        try:
            result = self.appointments.insert_one({
                'user_id': appointment_data.get('user_id'),
                'name': appointment_data.get('name'),
                'phone': appointment_data.get('phone'),
                'email': appointment_data.get('email'),
                'department': appointment_data.get('department'),
                'doctor': appointment_data.get('doctor'),
                'date': appointment_data.get('date'),
                'time': appointment_data.get('time'),
                'reason': appointment_data.get('reason'),
                'status': 'confirmed',
                'created_at': datetime.utcnow()
            })
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return None
    
    def get_conversation_history(self, user_id, limit=10):
        """Get conversation history for a user"""
        if not self.db:
            return []
        
        try:
            conversations = list(self.conversations.find(
                {'user_id': user_id}
            ).sort('timestamp', -1).limit(limit))
            return conversations
        except Exception as e:
            print(f"Error fetching conversation history: {e}")
            return []
    
    def get_appointments(self, user_id):
        """Get appointments for a user"""
        if not self.db:
            return []
        
        try:
            appointments = list(self.appointments.find(
                {'user_id': user_id}
            ).sort('created_at', -1))
            return appointments
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            return []

# Initialize database
db = Database()
