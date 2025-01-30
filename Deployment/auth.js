const themeToggle = document.querySelector('.theme-toggle');
const body = document.body;
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.querySelector('.message-input');
const sendButton = document.querySelector('.send-button');
const typingIndicator = document.querySelector('.typing-indicator');

// Theme toggling
let isDarkTheme = false;
themeToggle.addEventListener('click', () => {
    isDarkTheme = !isDarkTheme;
    body.setAttribute('data-theme', isDarkTheme ? 'dark' : 'light');
    themeToggle.innerHTML = isDarkTheme ?
        '<i class="fas fa-sun"></i>' :
        '<i class="fas fa-moon"></i>';
});

// Chat functionality
function createMessageElement(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    messageDiv.innerHTML = `
        <div class="avatar">${isUser ? 'U' : 'AI'}</div>
        <div class="message-bubble">${content}</div>
    `;

    return messageDiv;
}

function addMessage(content, isUser = false) {
    const messageElement = createMessageElement(content, isUser);
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function simulateBotResponse(userMessage) {
    showTypingIndicator();

    // Simulate varying response times
    setTimeout(() => {
        hideTypingIndicator();
        const responses = [
            "I understand you're asking about " + userMessage + ". Could you elaborate?",
            "That's an interesting point about " + userMessage + ". Let me help you with that.",
            "I've analyzed your message about " + userMessage + ". Here's what I think..."
        ];
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        addMessage(randomResponse);
    }, Math.random() * 1000 + 1500);
}

function handleSendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message, true);
        messageInput.value = '';
        simulateBotResponse(message);
    }
}

sendButton.addEventListener('click', handleSendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSendMessage();
    }
});

setTimeout(() => {
    addMessage("Hello! I'm your AI assistant. How can I help you today?");
}, 500);
