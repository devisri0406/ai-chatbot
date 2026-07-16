# 🏥 Hospital Appointment Chatbot

An intelligent AI-powered chatbot for booking hospital appointments. This project combines Flask backend with Hugging Face NLP models and a modern web interface.

## 🌟 Features

- **AI-Powered Conversations**: Uses Hugging Face transformers for sentiment analysis and intent detection
- **Appointment Booking**: Multi-step form to collect patient information and preferences
- **Hospital Information**: Quick access to hospital details, doctors, and departments
- **Conversation History**: MongoDB database to store and retrieve conversation logs
- **Appointment Management**: Save and retrieve booked appointments
- **Real-time Chat Interface**: Modern, responsive web UI with typing indicators
- **User Sessions**: Track conversations per user with unique IDs
- **RESTful API**: Clean Flask API endpoints for all chatbot operations

## 📋 Project Structure

```
ai-chatbot/
├── app.py                 # Flask application and routes
├── chatbot.py            # Chatbot logic and NLP processing
├── database.py           # MongoDB database operations
├── config.py             # Configuration settings
├── index.html            # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devisri0406/ai-chatbot.git
   cd ai-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🔧 Configuration

Edit `.env` file to customize:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=hospital_chatbot
MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
```

### Doctors and Departments

Modify `config.py` to add/change doctors and departments:

```python
DOCTORS = {
    'cardiologist': ['Dr. Smith', 'Dr. Johnson'],
    'dermatologist': ['Dr. Williams', 'Dr. Brown'],
    # Add more as needed
}
```

## 📚 API Endpoints

### Health Check
```
GET /api/health
```

### Chat
```
POST /api/chat
Headers: X-User-ID: <user-id>
Body: { "message": "Your message" }
```

### Get Conversation History
```
GET /api/conversation/<user-id>
```

### Get Appointments
```
GET /api/appointments/<user-id>
```

### Get Departments
```
GET /api/departments
```

### Get Hospital Info
```
GET /api/hospital-info
```

## 🤖 Chatbot Features

### Intent Detection

The chatbot can understand user intent:
- `book_appointment` - User wants to book an appointment
- `check_appointment` - Check appointment status
- `hospital_info` - Get hospital information
- `doctor_info` - Get information about doctors
- `greeting` - General greeting
- `goodbye` - Say goodbye
- `general_query` - General questions

### Appointment Booking Flow

1. User initiates booking
2. Chatbot asks for:
   - Patient name
   - Phone number
   - Email address
   - Preferred department
   - Preferred doctor
   - Preferred date
   - Preferred time
   - Reason for visit
3. Chatbot confirms details
4. Appointment saved to database

### Sentiment Analysis

The chatbot uses Hugging Face's distilBERT model to analyze user sentiment (positive/negative/neutral).

## 💾 Database Schema

### Conversations Collection
```javascript
{
  user_id: String,
  user_message: String,
  bot_response: String,
  timestamp: Date
}
```

### Appointments Collection
```javascript
{
  user_id: String,
  name: String,
  phone: String,
  email: String,
  department: String,
  doctor: String,
  date: String,
  time: String,
  reason: String,
  status: String,
  created_at: Date
}
```

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Clean, intuitive interface
- **Real-time Chat**: Instant message display with animations
- **Quick Actions**: Buttons for common operations
- **Sidebar**: Hospital information and session details
- **Typing Indicator**: Shows when bot is "thinking"
- **Scroll Auto-scroll**: Automatically scrolls to latest messages

## 🔐 Security Considerations

- CORS enabled for local development
- Input validation on both client and server
- XSS prevention with HTML escaping
- User sessions tracked with unique IDs
- Environment variables for sensitive data

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Make sure MongoDB is running
mongod  # On Windows: mongod.exe
```

### Model Download Error
```bash
# The first run will download the model (~250MB)
# Ensure you have good internet connection
# Subsequent runs will use cached model
```

### CORS Error
```bash
# Make sure frontend is accessing correct API URL
# Check API_URL in static/js/script.js
```

### Port Already in Use
```bash
# Change port in app.py or kill process using port 5000
# Find process: lsof -i :5000
# Kill process: kill -9 <PID>
```

## 📈 Performance Tips

- Use MongoDB Atlas for cloud database
- Deploy on cloud platforms (Heroku, AWS, GCP)
- Enable caching for frequently accessed data
- Use CDN for static files
- Optimize model loading with caching

## 🚀 Deployment

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👥 Author

**Devi Sri** - [@devisri0406](https://github.com/devisri0406)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: surisettydevi24@gmail.com

## 🎯 Future Enhancements

- [ ] Payment integration
- [ ] SMS/Email notifications
- [ ] Multi-language support
- [ ] Video consultation booking
- [ ] Medical records integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Voice interaction
- [ ] Advanced NLP with GPT models
- [ ] Integration with hospital management systems

---

**Made with ❤️ for healthcare**
