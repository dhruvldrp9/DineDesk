// Chat History Management for DineDesk
class ChatHistoryManager {
    constructor(dineDesk) {
        this.dineDesk = dineDesk;
        this.isHistoryOpen = false;
        this.chatSessions = [];
        this.currentChatId = null;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // User menu dropdown
        document.getElementById('user-menu-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            const dropdown = document.getElementById('user-dropdown');
            dropdown.classList.toggle('hidden');
        });
        
        // Toggle history sidebar
        document.getElementById('toggle-history-btn').addEventListener('click', () => {
            this.toggleHistory();
            // Close dropdown
            document.getElementById('user-dropdown').classList.add('hidden');
        });
        
        // Close history sidebar
        document.getElementById('close-history-btn').addEventListener('click', () => {
            this.closeHistory();
        });
        
        // New chat button
        document.getElementById('new-chat-btn').addEventListener('click', () => {
            this.createNewChat();
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            const sidebar = document.getElementById('chat-history-sidebar');
            const toggleBtn = document.getElementById('toggle-history-btn');
            const userDropdown = document.getElementById('user-dropdown');
            const userMenuBtn = document.getElementById('user-menu-btn');
            
            // Close dropdown if clicking outside
            if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.add('hidden');
            }
            
            // Close sidebar if clicking outside
            if (this.isHistoryOpen && 
                !sidebar.contains(e.target) && 
                !toggleBtn.contains(e.target)) {
                this.closeHistory();
            }
        });
    }
    
    async toggleHistory() {
        if (this.isHistoryOpen) {
            this.closeHistory();
        } else {
            await this.openHistory();
        }
    }
    
    async openHistory() {
        this.isHistoryOpen = true;
        const sidebar = document.getElementById('chat-history-sidebar');
        sidebar.classList.remove('-translate-x-full');
        
        // Load chat history
        await this.loadChatHistory();
    }
    
    closeHistory() {
        this.isHistoryOpen = false;
        const sidebar = document.getElementById('chat-history-sidebar');
        sidebar.classList.add('-translate-x-full');
    }
    
    async loadChatHistory() {
        try {
            const response = await fetch('/api/chat-history', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.chatSessions = data.chat_sessions;
                this.renderChatHistory();
            } else {
                this.showHistoryError('Failed to load chat history');
            }
            
        } catch (error) {
            console.error('Error loading chat history:', error);
            this.showHistoryError('Connection error');
        }
    }
    
    renderChatHistory() {
        const historyList = document.getElementById('chat-history-list');
        
        if (this.chatSessions.length === 0) {
            historyList.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <i class="fas fa-comments text-2xl mb-2"></i>
                    <p>No previous chats</p>
                    <p class="text-sm">Start a conversation to see your history here</p>
                </div>
            `;
            return;
        }
        
        historyList.innerHTML = this.chatSessions.map(chat => this.createChatItem(chat)).join('');
        
        // Add event listeners for chat items
        this.attachChatItemListeners();
    }
    
    createChatItem(chat) {
        const isActive = chat.status === 'active';
        
        return `
            <div class="chat-item group p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer transition-all duration-200 ${isActive ? 'bg-blue-50 border-blue-200' : ''}" 
                 data-chat-id="${chat.id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <h3 class="text-sm font-medium text-gray-900 truncate">
                            ${chat.title || 'New Chat'}
                        </h3>
                        <p class="text-xs text-gray-600 mt-1 font-medium">
                            ${chat.formatted_date}
                        </p>
                        <p class="text-xs text-gray-400 mt-0.5 flex items-center space-x-2">
                            <span>${chat.formatted_time}</span>
                            <span>•</span>
                            <span>${chat.relative_time}</span>
                            <span>•</span>
                            <span>${chat.message_count} messages</span>
                        </p>
                        ${isActive ? '<span class="inline-block w-2 h-2 bg-green-500 rounded-full mt-1"></span>' : ''}
                    </div>
                    <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="delete-chat-btn text-red-500 hover:text-red-700 p-1" 
                                data-chat-id="${chat.id}" 
                                title="Delete chat">
                            <i class="fas fa-trash text-xs"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    attachChatItemListeners() {
        // Load chat on click
        document.querySelectorAll('.chat-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.delete-chat-btn')) {
                    const chatId = item.dataset.chatId;
                    this.loadChat(chatId);
                }
            });
        });
        
        // Delete chat buttons
        document.querySelectorAll('.delete-chat-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const chatId = btn.dataset.chatId;
                this.deleteChat(chatId);
            });
        });
    }
    
    async loadChat(chatId) {
        try {
            const response = await fetch(`/api/load-chat/${chatId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentChatId = chatId;
                
                // Clear current messages and load new ones
                this.dineDesk.clearMessages();
                
                // Load messages with animation
                data.messages.forEach((message, index) => {
                    setTimeout(() => {
                        this.dineDesk.chatManager.displayMessage(message, false);
                    }, index * 100);
                });
                
                this.closeHistory();
                this.dineDesk.showToast('Chat loaded successfully', 'success');
                
                // Scroll to bottom after all messages are loaded
                setTimeout(() => {
                    this.dineDesk.scrollToBottom();
                }, data.messages.length * 100 + 200);
                
            } else {
                this.dineDesk.showToast(data.error || 'Failed to load chat', 'error');
            }
            
        } catch (error) {
            console.error('Error loading chat:', error);
            this.dineDesk.showToast('Failed to load chat', 'error');
        }
    }
    
    async deleteChat(chatId) {
        if (!confirm('Are you sure you want to delete this chat? This action cannot be undone.')) {
            return;
        }
        
        try {
            const response = await fetch(`/api/delete-chat/${chatId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Remove from local list
                this.chatSessions = this.chatSessions.filter(chat => chat.id !== chatId);
                this.renderChatHistory();
                
                // If this was the current chat, start a new one
                if (this.currentChatId === chatId) {
                    this.createNewChat();
                }
                
                this.dineDesk.showToast('Chat deleted successfully', 'success');
            } else {
                this.dineDesk.showToast(data.error || 'Failed to delete chat', 'error');
            }
            
        } catch (error) {
            console.error('Error deleting chat:', error);
            this.dineDesk.showToast('Failed to delete chat', 'error');
        }
    }
    
    async createNewChat() {
        try {
            const response = await fetch('/new-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentChatId = data.chat_id;
                
                // Clear current messages
                this.dineDesk.clearMessages();
                
                // Display welcome message if provided
                if (data.welcome_message) {
                    this.dineDesk.chatManager.displayMessage(data.welcome_message);
                }
                
                // Close history and refresh if open
                if (this.isHistoryOpen) {
                    this.loadChatHistory();
                }
                
                this.dineDesk.showToast('New chat started', 'success');
                
            } else {
                this.dineDesk.showToast(data.error || 'Failed to start new chat', 'error');
            }
            
        } catch (error) {
            console.error('Error creating new chat:', error);
            this.dineDesk.showToast('Failed to start new chat', 'error');
        }
    }
    
    showHistoryError(message) {
        const historyList = document.getElementById('chat-history-list');
        historyList.innerHTML = `
            <div class="text-center text-red-500 py-8">
                <i class="fas fa-exclamation-triangle text-xl mb-2"></i>
                <p>${message}</p>
                <button onclick="window.chatHistory.loadChatHistory()" 
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800">
                    Try again
                </button>
            </div>
        `;
    }
    
    formatTimeAgo(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString();
    }
}

// Export for global access
window.ChatHistoryManager = ChatHistoryManager;