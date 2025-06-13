// Main JavaScript file for DineDesk application (AJAX version)
class DineDesk {
    constructor() {
        this.isConnected = true;
        this.messageHistory = [];
        this.isTyping = false;
        this.chatManager = null;
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupAutoResize();
        this.loadMessageHistory();
        // Initialize chat manager
        this.chatManager = new ChatManager(this);
        // Initialize chat history manager
        this.chatHistory = new ChatHistoryManager(this);
        // Initialize voice manager
        this.voiceManager = new VoiceManager(this);
        
        // Make DineDesk globally available for voice manager
        window.dineDesk = this;
    }
    
    setupEventListeners() {
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        const voiceBtn = document.getElementById('voice-btn');
        
        // Send button click
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character counter
        messageInput.addEventListener('input', this.updateCharacterCounter);
        
        // Voice button functionality will be handled by VoiceManager
        // Remove placeholder functionality as it's now implemented
        
        // Modal close handlers
        const modal = document.getElementById('restaurant-modal');
        const closeModal = document.getElementById('close-modal');
        
        closeModal.addEventListener('click', () => this.closeModal());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeModal();
        });
        
        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeModal();
        });
        
        // New chat button
        const newChatBtn = document.getElementById('new-chat-btn');
        newChatBtn.addEventListener('click', () => this.startNewChat());
    }
    
    setupAutoResize() {
        const messageInput = document.getElementById('message-input');
        
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
    
    updateCharacterCounter() {
        const messageInput = document.getElementById('message-input');
        const charCounter = document.getElementById('char-counter');
        const currentLength = messageInput.value.length;
        const maxLength = 1000;
        
        charCounter.textContent = `${currentLength}/${maxLength}`;
        
        if (currentLength > maxLength * 0.9) {
            charCounter.classList.add('text-red-500');
            charCounter.classList.remove('text-gray-400');
        } else {
            charCounter.classList.remove('text-red-500');
            charCounter.classList.add('text-gray-400');
        }
    }
    
    async sendMessage() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        this.updateCharacterCounter();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display user message
                this.chatManager.displayMessage(data.user_message);
                
                // Simulate typing delay and display bot response
                setTimeout(() => {
                    this.hideTypingIndicator();
                    this.chatManager.displayBotResponseWithStreaming(data.bot_response);
                }, 500);
            } else {
                this.hideTypingIndicator();
                this.showToast(data.error || 'Error sending message', 'error');
            }
            
        } catch (error) {
            this.hideTypingIndicator();
            this.showToast('Network error. Please try again.', 'error');
            console.error('Error sending message:', error);
        }
    }
    
    async loadMessageHistory() {
        try {
            const response = await fetch('/api/get_history');
            const messages = await response.json();
            
            if (response.ok) {
                this.chatManager.loadMessageHistory(messages);
            }
        } catch (error) {
            console.error('Error loading message history:', error);
        }
    }
    
    showTypingIndicator() {
        if (this.isTyping) return;
        this.isTyping = true;
        const typingIndicator = document.getElementById('typing-indicator');
        typingIndicator.classList.remove('hidden');
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('typing-indicator');
        typingIndicator.classList.add('hidden');
    }
    
    showToast(message, type = 'info', duration = 3000) {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle'
        };
        
        toast.className = `toast ${type} px-4 py-3 rounded-lg shadow-lg flex items-center space-x-2 mb-2`;
        toast.innerHTML = `
            <i class="${icons[type] || icons.info}"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto remove after duration
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, duration);
        
        // Remove on click
        toast.addEventListener('click', () => toast.remove());
    }
    
    closeModal() {
        const modal = document.getElementById('restaurant-modal');
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    
    openModal(content) {
        const modal = document.getElementById('restaurant-modal');
        const modalContent = document.getElementById('modal-content');
        
        modalContent.innerHTML = content;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    clearMessages() {
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = '';
        this.messageHistory = [];
    }
    
    formatTimestamp(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        const diffInHours = (now - date) / (1000 * 60 * 60);
        
        if (diffInHours < 1) {
            return 'Just now';
        } else if (diffInHours < 24) {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else {
            return date.toLocaleDateString();
        }
    }
    
    sanitizeHTML(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
    
    startNewChat() {
        // Clear current messages
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = '';
        
        // Reset message history in memory
        this.messageHistory = [];
        
        // Clear server-side session
        fetch('/new-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show welcome message for new chat
                this.displayWelcomeMessage();
                this.showToast('New chat started', 'success');
            }
        })
        .catch(error => {
            console.error('Error starting new chat:', error);
            this.showToast('Error starting new chat', 'error');
        });
    }
    
    displayWelcomeMessage() {
        const welcomeMessage = {
            type: 'bot',
            content: "Hi! Welcome to DineDesk! I'm here to help you with restaurant reservations and food delivery. Are you looking to:\n\n1. Make a restaurant reservation\n2. Order food for delivery\n3. Browse restaurants in your area",
            timestamp: new Date().toISOString(),
            quickReplies: [
                { text: "Make a Reservation", action: "reservation" },
                { text: "Order Food", action: "delivery" },
                { text: "Browse Restaurants", action: "browse" }
            ]
        };
        
        this.chatManager.displayMessage(welcomeMessage, true);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dineDesk = new DineDesk();
});