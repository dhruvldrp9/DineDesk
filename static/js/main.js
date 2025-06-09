document.addEventListener('DOMContentLoaded', () => {
    const chatArea = document.getElementById('chatArea');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const micButton = document.getElementById('micButton');
    const attachButton = document.getElementById('attachButton');
    const charCount = document.getElementById('charCount');
    const toastContainer = document.getElementById('toastContainer');

    // Initialize Socket.IO
    const socket = io();

    // Character count limit
    const MAX_CHARS = 500;

    // Function to show toast notification
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <p>${message}</p>
            </div>
        `;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        // Create message content with proper formatting
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestamp);
        chatArea.appendChild(messageDiv);
        
        // Scroll to bottom with smooth animation
        chatArea.scrollTo({
            top: chatArea.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.innerHTML = `
            <span class="typing"></span>
            <span class="typing"></span>
            <span class="typing"></span>
        `;
        chatArea.appendChild(typingDiv);
        chatArea.scrollTo({
            top: chatArea.scrollHeight,
            behavior: 'smooth'
        });
        return typingDiv;
    }

    // Function to handle sending messages
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Disable input while processing
        userInput.disabled = true;
        sendButton.disabled = true;

        // Add user message
        addMessage(message, true);
        userInput.value = '';
        charCount.textContent = '0/500';

        // Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            // Emit message through Socket.IO
            socket.emit('message', { message });

            // Listen for response
            socket.on('response', (data) => {
                typingIndicator.remove();
                addMessage(data.message);
            });

        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            showToast('Sorry, something went wrong. Please try again.', 'error');
        } finally {
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // Character count handler
    userInput.addEventListener('input', () => {
        const count = userInput.value.length;
        charCount.textContent = `${count}/${MAX_CHARS}`;
        
        if (count > MAX_CHARS) {
            charCount.style.color = '#F56565';
            sendButton.disabled = true;
        } else {
            charCount.style.color = '';
            sendButton.disabled = false;
        }
    });

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    micButton.addEventListener('click', () => {
        showToast('Voice input coming soon!', 'info');
    });

    attachButton.addEventListener('click', () => {
        showToast('File attachment coming soon!', 'info');
    });

    // Socket.IO event handlers
    socket.on('connect', () => {
        showToast('Connected to server', 'success');
    });

    socket.on('disconnect', () => {
        showToast('Disconnected from server', 'error');
    });

    socket.on('error', (error) => {
        showToast(error.message, 'error');
    });

    // Focus input on load
    userInput.focus();
}); 