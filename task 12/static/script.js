const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const helpBtn = document.getElementById('helpBtn');
const collectionsBtn = document.getElementById('collectionsBtn');
const clearBtn = document.getElementById('clearBtn');

// Send message when button is clicked
sendBtn.addEventListener('click', sendMessage);

// Send message when Enter is pressed
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && userInput.value.trim()) {
        sendMessage();
    }
});

// Help button
helpBtn.addEventListener('click', () => {
    userInput.value = 'help';
    sendMessage();
});

// Collections button
collectionsBtn.addEventListener('click', () => {
    userInput.value = 'collections';
    sendMessage();
});

// Clear button
clearBtn.addEventListener('click', () => {
    chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                Chat cleared! How can I help you find hadiths today? 🕌
            </div>
        </div>
    `;
});

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    userInput.value = '';
    
    // Show loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.innerHTML = '<div class="message-content"><div class="loading"></div><div class="loading"></div><div class="loading"></div></div>';
    chatMessages.appendChild(loadingDiv);
    scrollToBottom();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        // Remove loading indicator
        loadingDiv.remove();
        
        if (response.ok) {
            const data = await response.json();
            addMessageToChat(data.message, 'bot');
        } else {
            addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        loadingDiv.remove();
        console.error('Error:', error);
        addMessageToChat('Sorry, I couldn\'t process your request. Please check your connection.', 'bot');
    }
    
    scrollToBottom();
}

function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Convert text to HTML with proper formatting
    contentDiv.innerHTML = formatMessage(message);
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
}

function formatMessage(message) {
    // Escape HTML
    let formatted = escapeHtml(message);
    
    // Convert newlines to <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Add styling for sections starting with "📖", "👤", "✓", etc.
    formatted = formatted.replace(/^(📖.*?)(?=<br>|$)/gm, '<strong>$1</strong>');
    formatted = formatted.replace(/^(👤.*?)(?=<br>|$)/gm, '<strong>$1</strong>');
    formatted = formatted.replace(/^(✓.*?)(?=<br>|$)/gm, '<strong>$1</strong>');
    formatted = formatted.replace(/^(\d+\..*?)(?=<br>|$)/gm, '<strong>$1</strong>');
    
    return formatted;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});
