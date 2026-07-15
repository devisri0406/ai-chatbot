import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'hospital_chatbot')
    
    # AI Model Configuration
    MODEL_NAME = os.getenv('MODEL_NAME', 'distilbert-base-uncased-finetuned-sst-2-english')
    
    # Hospital Configuration
    HOSPITAL_NAME = "City Hospital"
    DOCTORS = {
        'cardiologist': ['Dr. Smith', 'Dr. Johnson'],
        'dermatologist': ['Dr. Williams', 'Dr. Brown'],
        'pediatrician': ['Dr. Davis', 'Dr. Miller'],
        'orthopedic': ['Dr. Wilson', 'Dr. Moore'],
        'general': ['Dr. Taylor', 'Dr. Anderson']
    }
    
    AVAILABLE_SLOTS = {
        'morning': ['09:00', '09:30', '10:00', '10:30', '11:00'],
        'afternoon': ['14:00', '14:30', '15:00', '15:30', '16:00'],
        'evening': ['17:00', '17:30', '18:00']
    }
