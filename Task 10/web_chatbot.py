"""
Web-based Hostel Information Chatbot using Flask
"""

from flask import Flask, render_template_string, request, jsonify
import json
from hostel_chatbot import HostelChatbot

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize chatbot
chatbot = HostelChatbot()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Hostel - Chat Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 800px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
            border-bottom: 3px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 25px;
            background-color: #f9f9f9;
        }
        
        .message {
            margin-bottom: 20px;
            display: flex;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 12px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        
        .user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .bot .message-content {
            background: white;
            color: #333;
            border: 2px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        
        .message-content strong {
            display: block;
            margin: 5px 0;
            color: inherit;
        }
        
        .message-content ul, .message-content ol {
            margin-left: 20px;
            margin-top: 8px;
        }
        
        .message-content li {
            margin: 5px 0;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: bounce 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes bounce {
            0%, 80%, 100% {
                opacity: 0.3;
            }
            40% {
                opacity: 1;
            }
        }
        
        .input-area {
            background: white;
            padding: 20px;
            border-top: 2px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        
        .input-container {
            flex: 1;
            display: flex;
            gap: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        #userInput:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .reset-btn {
            background: #ff6b6b;
            padding: 10px 15px;
            font-size: 13px;
        }
        
        .reset-btn:hover {
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .suggestions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }
        
        .suggestion {
            padding: 8px 12px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
        }
        
        .suggestion:hover {
            background: #e0e0e0;
            transform: translateX(2px);
        }
        
        @media (max-width: 600px) {
            .container {
                height: 100vh;
                border-radius: 0;
            }
            
            .message-content {
                max-width: 85%;
            }
            
            .suggestions {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏨 Campus Hostel Assistant</h1>
            <p>Your 24/7 hostel information chatbot</p>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="message bot">
                <div class="message-content">
                    <strong>Welcome to Campus Hostel! 👋</strong><br>
                    I'm here to help answer any questions about our facilities, pricing, booking, rules, and more.<br><br>
                    <strong>What would you like to know?</strong>
                </div>
            </div>
            <div class="suggestions">
                <div class="suggestion" onclick="askQuestion('What are your facilities?')">📍 Facilities</div>
                <div class="suggestion" onclick="askQuestion('What is your pricing?')">💰 Pricing</div>
                <div class="suggestion" onclick="askQuestion('How do I book?')">📅 Booking</div>
                <div class="suggestion" onclick="askQuestion('What are your rules?')">📋 Rules</div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="input-container">
                <input 
                    type="text" 
                    id="userInput" 
                    placeholder="Type your question..." 
                    onkeypress="handleKeyPress(event)"
                >
                <button onclick="sendMessage()">Send</button>
                <button class="reset-btn" onclick="resetChat()">Reset</button>
            </div>
        </div>
    </div>

    <script>
        const chatArea = document.getElementById('chatArea');
        const userInput = document.getElementById('userInput');
        
        function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                removeTypingIndicator();
                addMessage('Sorry, there was an error. Please try again.', 'bot');
                console.error('Error:', error);
            });
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text;
            
            messageDiv.appendChild(contentDiv);
            chatArea.appendChild(messageDiv);
            
            // Scroll to bottom
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function showTypingIndicator() {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot';
            messageDiv.id = 'typingIndicator';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
            
            messageDiv.appendChild(contentDiv);
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function removeTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function resetChat() {
            if (confirm('Are you sure you want to clear the chat?')) {
                chatArea.innerHTML = `
                    <div class="message bot">
                        <div class="message-content">
                            <strong>Chat cleared! 👋</strong><br>
                            Ready for a fresh conversation.
                        </div>
                    </div>
                `;
                userInput.value = '';
                fetch('/reset', { method: 'POST' });
            }
        }
        
        function askQuestion(question) {
            userInput.value = question;
            sendMessage();
        }
        
        // Focus on input field
        userInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main chatbot page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    # Get response from chatbot
    response = chatbot.respond(user_message)
    
    return jsonify({'response': response})

@app.route('/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    chatbot.reset_conversation()
    return jsonify({'status': 'success'})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting Hostel Information Chatbot Web Server")
    print("="*60)
    print("\n🌐 Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
