// Main JavaScript file for DineDesk application
class DineDesk {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.messageHistory = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.initializeSocketIO();
        this.setupEventListeners();
        this.setupAutoResize();
        this.requestMessageHistory();
    }
    
    initializeSocketIO() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.isConnected = true;
            this.updateConnectionStatus(true);
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.isConnected = false;
            this.updateConnectionStatus(false);
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
            this.showToast('Connection error. Please refresh the page.', 'error');
        });
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
        
        // Voice button (placeholder for future implementation)
        voiceBtn.addEventListener('click', () => {
            this.showToast('Voice input feature coming soon!', 'info');
        });
        
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
    
    sendMessage() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();
        
        if (!message || !this.isConnected) return;
        
        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        this.updateCharacterCounter();
        
        // Send message via Socket.IO
        this.socket.emit('send_message', { message: message });
    }
    
    requestMessageHistory() {
        if (this.isConnected) {
            this.socket.emit('get_message_history');
        }
    }
    
    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        const statusDot = statusElement.querySelector('.w-2');
        const statusText = statusElement.querySelector('span');
        
        if (connected) {
            statusDot.classList.remove('bg-red-500');
            statusDot.classList.add('bg-green-500', 'animate-pulse');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.remove('bg-green-500', 'animate-pulse');
            statusDot.classList.add('bg-red-500');
            statusText.textContent = 'Disconnected';
        }
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
    
    // Utility method to format timestamps
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
    
    // Utility method to sanitize HTML content
    sanitizeHTML(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dineDesk = new DineDesk();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DineDesk;
}
