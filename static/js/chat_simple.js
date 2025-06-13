// Chat-specific functionality for DineDesk (AJAX version)
class ChatManager {
    constructor(dineDesk) {
        this.dineDesk = dineDesk;
        this.streamingMessages = new Map();
    }
    
    loadMessageHistory(messages) {
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = '';
        
        messages.forEach(message => {
            this.displayMessage(message, false);
        });
        
        this.dineDesk.scrollToBottom();
    }
    
    displayMessage(message, animate = true) {
        const messagesContainer = document.getElementById('messages-container');
        const messageElement = this.createMessageElement(message, animate);
        
        messagesContainer.appendChild(messageElement);
        this.dineDesk.scrollToBottom();
        
        return messageElement;
    }
    
    displayBotResponseWithStreaming(message) {
        if (message.message_type === 'card') {
            // Display card messages immediately
            this.displayMessage(message);
        } else {
            // Simulate streaming for text messages
            this.simulateStreamingResponse(message);
        }
    }
    
    simulateStreamingResponse(message) {
        const messagesContainer = document.getElementById('messages-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex justify-start animate-fade-in';
        messageDiv.dataset.messageId = message.id;
        
        const avatar = `
            <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0 mr-3">
                <i class="fas fa-robot text-gray-600 text-xs"></i>
            </div>
        `;
        
        messageDiv.innerHTML = avatar + `
            <div class="flex-1">
                <div class="message-bubble bot-message px-4 py-3 text-sm">
                    <div class="streaming-content whitespace-pre-wrap"></div>
                    <span class="typing-cursor animate-pulse">|</span>
                    <div class="text-xs mt-2 text-gray-500">${this.dineDesk.formatTimestamp(message.timestamp)}</div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.dineDesk.scrollToBottom();
        
        // Stream the content
        const contentElement = messageDiv.querySelector('.streaming-content');
        const cursorElement = messageDiv.querySelector('.typing-cursor');
        const content = message.content;
        let currentIndex = 0;
        
        const streamInterval = setInterval(() => {
            if (currentIndex <= content.length) {
                contentElement.textContent = content.substring(0, currentIndex);
                currentIndex++;
                this.dineDesk.scrollToBottom();
            } else {
                clearInterval(streamInterval);
                cursorElement.style.display = 'none';
                
                // Replace with complete message
                const completeMessage = this.createMessageElement(message, false);
                messageDiv.parentNode.replaceChild(completeMessage, messageDiv);
                this.dineDesk.scrollToBottom();
            }
        }, 50);
    }
    
    createMessageElement(message, animate = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} ${animate ? 'animate-fade-in' : ''}`;
        messageDiv.dataset.messageId = message.id;
        
        if (message.type === 'user') {
            messageDiv.innerHTML = this.createUserMessage(message);
        } else {
            messageDiv.innerHTML = this.createBotMessage(message);
        }
        
        return messageDiv;
    }
    
    createUserMessage(message) {
        const timestamp = this.dineDesk.formatTimestamp(message.timestamp);
        const content = this.dineDesk.sanitizeHTML(message.content);
        
        return `
            <div class="message-bubble user-message px-4 py-3 text-sm">
                <div class="whitespace-pre-wrap">${content}</div>
                <div class="text-xs mt-1 opacity-75">${timestamp}</div>
            </div>
        `;
    }
    
    createBotMessage(message) {
        const timestamp = this.dineDesk.formatTimestamp(message.timestamp);
        let content = '';
        
        // Bot avatar
        const avatar = `
            <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0 mr-3">
                <i class="fas fa-robot text-gray-600 text-xs"></i>
            </div>
        `;
        
        if (message.message_type === 'card' && message.cards) {
            content = this.createCardMessage(message);
        } else {
            const textContent = this.dineDesk.sanitizeHTML(message.content);
            content = `
                <div class="message-bubble bot-message px-4 py-3 text-sm">
                    <div class="whitespace-pre-wrap">${textContent}</div>
                    <div class="text-xs mt-2 text-gray-500">${timestamp}</div>
                </div>
            `;
        }
        
        // Add quick replies if present
        if (message.quick_replies && message.quick_replies.length > 0) {
            content += this.createQuickReplies(message.quick_replies);
        }
        
        return avatar + '<div class="flex-1">' + content + '</div>';
    }
    
    createCardMessage(message) {
        const timestamp = this.dineDesk.formatTimestamp(message.timestamp);
        let cardsHTML = `
            <div class="message-bubble bot-message px-4 py-3 text-sm">
                <div class="whitespace-pre-wrap mb-3">${this.dineDesk.sanitizeHTML(message.content)}</div>
                <div class="space-y-4">
        `;
        
        message.cards.forEach(card => {
            cardsHTML += this.createRestaurantCard(card);
        });
        
        cardsHTML += `
                </div>
                <div class="text-xs mt-3 text-gray-500">${timestamp}</div>
            </div>
        `;
        
        return cardsHTML;
    }
    
    createRestaurantCard(card) {
        const rating = '★'.repeat(Math.floor(card.rating)) + '☆'.repeat(5 - Math.floor(card.rating));
        let actionsHTML = '';
        
        if (card.actions) {
            actionsHTML = '<div class="flex flex-wrap gap-2 mt-3">';
            card.actions.forEach(action => {
                actionsHTML += `
                    <button onclick="window.chatManager.handleCardAction('${action.action}')" 
                            class="action-btn px-3 py-1 text-xs rounded-full transition-all duration-200">
                        ${action.text}
                    </button>
                `;
            });
            actionsHTML += '</div>';
        }
        
        let dishesHTML = '';
        if (card.popular_dishes && card.popular_dishes.length > 0) {
            dishesHTML = '<div class="mt-3"><div class="text-xs text-gray-500 mb-2">Popular dishes:</div><div class="flex gap-2 overflow-x-auto">';
            card.popular_dishes.forEach(dish => {
                dishesHTML += `
                    <div class="flex-shrink-0 bg-gray-50 rounded-lg p-2 text-xs">
                        <img src="${dish.image}" alt="${dish.name}" class="w-12 h-12 object-cover rounded mb-1" onerror="this.style.display='none'">
                        <div class="font-medium">${dish.name}</div>
                        <div class="text-primary font-semibold">${dish.price}</div>
                    </div>
                `;
            });
            dishesHTML += '</div></div>';
        }
        
        let availabilityHTML = '';
        if (card.availability && card.availability.length > 0) {
            availabilityHTML = '<div class="mt-3"><div class="text-xs text-gray-500 mb-2">Available times:</div><div class="flex flex-wrap gap-1">';
            card.availability.forEach(slot => {
                if (slot.available) {
                    availabilityHTML += `
                        <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                            ${slot.time}
                        </span>
                    `;
                }
            });
            availabilityHTML += '</div></div>';
        }
        
        return `
            <div class="restaurant-card bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-all duration-300">
                <div class="flex items-start space-x-3">
                    <img src="${card.image}" alt="${card.name}" class="w-16 h-16 object-cover rounded-lg flex-shrink-0" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yNCAzMkMzMCAzMiAzMiAyNiAzMiAyNkMzMiAyNiAzNCAzMiA0MCAzMkM0NiAzMiA0MCAzOCA0MCAzOEMzNCAzOCAzMiA0NCAzMiA0NEMzMiA0NCAzMCAzOCAyNCAzOEMxOCAzOCAyNCAzMiAyNCAzMloiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+Cg=='">
                    <div class="flex-1 min-w-0">
                        <h4 class="font-semibold text-gray-800 truncate">${card.name}</h4>
                        <div class="flex items-center space-x-2 mt-1">
                            <span class="rating-stars text-sm">${rating}</span>
                            <span class="text-gray-500 text-xs">${card.rating}</span>
                            <span class="text-gray-400">•</span>
                            <span class="text-gray-500 text-xs">${card.price_level}</span>
                            <span class="text-gray-400">•</span>
                            <span class="text-gray-500 text-xs">${card.distance}</span>
                        </div>
                        <p class="text-gray-600 text-xs mt-1 line-clamp-2">${card.description}</p>
                    </div>
                </div>
                ${dishesHTML}
                ${availabilityHTML}
                ${actionsHTML}
            </div>
        `;
    }
    
    createQuickReplies(quickReplies) {
        let html = '<div class="flex flex-wrap gap-2 mt-3">';
        
        quickReplies.forEach(reply => {
            html += `
                <button onclick="window.chatManager.handleQuickReply('${reply.text}')" 
                        class="quick-reply-btn px-3 py-2 text-xs rounded-full transition-all duration-200">
                    ${reply.text}
                </button>
            `;
        });
        
        html += '</div>';
        return html;
    }
    
    async handleQuickReply(text) {
        try {
            const response = await fetch('/api/quick_reply', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display user message
                this.displayMessage(data.user_message);
                
                // Show typing indicator
                this.dineDesk.showTypingIndicator();
                
                // Display bot response with delay
                setTimeout(() => {
                    this.dineDesk.hideTypingIndicator();
                    this.displayBotResponseWithStreaming(data.bot_response);
                }, 500);
            } else {
                this.dineDesk.showToast(data.error || 'Error processing quick reply', 'error');
            }
            
        } catch (error) {
            this.dineDesk.showToast('Network error. Please try again.', 'error');
            console.error('Error handling quick reply:', error);
        }
    }
    
    handleCardAction(action) {
        console.log('Card action triggered:', action);
        
        if (action.startsWith('book_')) {
            this.dineDesk.showToast('Booking feature will be implemented soon!', 'info');
        } else if (action.startsWith('menu_')) {
            this.dineDesk.showToast('Menu viewing feature coming soon!', 'info');
        } else if (action.startsWith('order_')) {
            this.dineDesk.showToast('Online ordering feature in development!', 'info');
        } else if (action.startsWith('reviews_')) {
            this.dineDesk.showToast('Reviews feature coming soon!', 'info');
        } else {
            // Treat as a message
            this.handleQuickReply(action);
        }
    }
}

// Initialize chat manager when DineDesk is ready
document.addEventListener('DOMContentLoaded', () => {
    const initChatManager = () => {
        if (window.dineDesk) {
            window.chatManager = new ChatManager(window.dineDesk);
            window.dineDesk.chatManager = window.chatManager;
        } else {
            setTimeout(initChatManager, 100);
        }
    };
    
    initChatManager();
});