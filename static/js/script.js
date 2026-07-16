// Configuration
const API_URL = 'http://localhost:5000/api';
let userId = localStorage.getItem('userId') || generateUserId();
let isWaitingForResponse = false;

// Generate unique user ID
function generateUserId() {
    const id = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('userId', id);
    return id;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    displaySessionId();
    displayWelcomeMessage();
});

// Display session ID
function displaySessionId() {
    const sessionSpan = document.querySelector('#sessionId .highlight');
    if (sessionSpan) {
        sessionSpan.textContent = userId.substring(0, 16) + '...';
    }
}

// Display welcome message
function displayWelcomeMessage() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    addBotMessage('👋 Welcome to City Hospital! I\'m here to help you book an appointment. How can I assist you today?');
}

// Send message function
async function sendMessage(event) {
    event.preventDefault();
    
    if (isWaitingForResponse) return;
    
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Display user message
    addUserMessage(message);
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    isWaitingForResponse = true;
    
    try {
        // Send message to backend
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-ID': userId
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            // Add bot response
            addBotMessage(data.bot_response);
            
            // Handle appointment confirmation
            if (data.state === 'appointment_confirmed') {
                console.log('Appointment confirmed:', data.appointment_id);
                addBotMessage('✅ Your appointment has been saved! Appointment ID: ' + data.appointment_id);
            }
        } else {
            addBotMessage('❌ Error: ' + (data.error || 'Unknown error occurred'));
        }
    } catch (error) {
        removeTypingIndicator();
        console.error('Error:', error);
        addBotMessage('❌ Error connecting to server. Please try again.');
    } finally {
        isWaitingForResponse = false;
        userInput.focus();
    }
}

// Add user message to chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parse message for better formatting
    const formattedMessage = formatBotMessage(message);
    contentDiv.innerHTML = formattedMessage;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format bot message with line breaks
function formatBotMessage(message) {
    let formatted = escapeHtml(message);
    // Replace newlines with <br> tags
    formatted = formatted.replace(/\n/g, '<br>');
    // Wrap text in paragraph tags
    formatted = formatted.split('<br>').map(line => {
        if (line.trim()) {
            return `<p>${line}</p>`;
        }
        return '';
    }).join('');
    return formatted || '<p>...</p>';
}

// Show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'typing-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'typing-indicator';
    contentDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 0);
}

// Quick action handlers
function quickAction(action) {
    const userInput = document.getElementById('userInput');
    
    const actions = {
        'book': 'I want to book an appointment',
        'info': 'Tell me about the hospital',
        'doctors': 'Show me the doctors',
        'check': 'Check my appointment'
    };
    
    if (actions[action]) {
        userInput.value = actions[action];
        userInput.focus();
        // Optionally auto-send after a short delay
        setTimeout(() => {
            document.getElementById('chatForm').dispatchEvent(new Event('submit'));
        }, 300);
    }
}

// Clear chat history
function clearChat() {
    if (confirm('Are you sure you want to clear the chat? This action cannot be undone.')) {
        displayWelcomeMessage();
        document.getElementById('userInput').focus();
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Fetch and display conversation history
async function fetchConversationHistory() {
    try {
        const response = await fetch(`${API_URL}/conversation/${userId}`, {
            headers: {
                'X-User-ID': userId
            }
        });
        
        const data = await response.json();
        if (data.success) {
            console.log('Conversation history:', data.conversation_history);
        }
    } catch (error) {
        console.error('Error fetching conversation history:', error);
    }
}

// Fetch appointments
async function fetchAppointments() {
    try {
        const response = await fetch(`${API_URL}/appointments/${userId}`, {
            headers: {
                'X-User-ID': userId
            }
        });
        
        const data = await response.json();
        if (data.success) {
            console.log('Appointments:', data.appointments);
            return data.appointments;
        }
    } catch (error) {
        console.error('Error fetching appointments:', error);
    }
}

// Fetch hospital information
async function fetchHospitalInfo() {
    try {
        const response = await fetch(`${API_URL}/hospital-info`);
        const data = await response.json();
        if (data.success) {
            console.log('Hospital info:', data);
            return data;
        }
    } catch (error) {
        console.error('Error fetching hospital info:', error);
    }
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                document.getElementById('chatForm').dispatchEvent(new Event('submit'));
            }
        });
    }
});
