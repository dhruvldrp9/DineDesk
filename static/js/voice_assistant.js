// Voice Assistant Page JavaScript
class VoiceAssistant {
    constructor() {
        this.isListening = false;
        this.isProcessing = false;
        this.isConversationActive = false;
        this.recognition = null;
        this.synthesis = null;
        this.currentChatId = null;
        
        this.voiceBtn = document.getElementById('voice-assistant-btn');
        this.voiceIcon = document.getElementById('voice-assistant-icon');
        this.voiceStatus = document.getElementById('voice-status');
        this.statusText = document.getElementById('status-text');
        this.transcriptDisplay = document.getElementById('transcript-display');
        this.transcriptText = document.getElementById('transcript-text');
        this.responseDisplay = document.getElementById('response-display');
        this.responseText = document.getElementById('response-text');
        this.wave1 = document.getElementById('wave-1');
        this.wave2 = document.getElementById('wave-2');
        this.wave3 = document.getElementById('wave-3');
        this.wave4 = document.getElementById('wave-4');
        
        this.initializeSpeechRecognition();
        this.initializeSpeechSynthesis();
        this.setupEventListeners();
        this.initializeChatSession();
    }
    
    initializeSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('Speech recognition not supported in this browser');
            this.disableVoiceButton();
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
        };
        
        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            if (interimTranscript) {
                this.updateTranscript(interimTranscript, false);
            }
            
            if (finalTranscript) {
                this.updateTranscript(finalTranscript, true);
                this.processUserInput(finalTranscript.trim());
            }
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            if (!this.isProcessing) {
                this.updateUI('idle');
            }
        };
        
        this.recognition.onerror = (event) => {
            this.isListening = false;
            this.isProcessing = false;
            this.handleSpeechError(event.error);
            this.updateUI('idle');
        };
    }
    
    initializeSpeechSynthesis() {
        if ('speechSynthesis' in window) {
            this.synthesis = window.speechSynthesis;
        } else {
            console.warn('Speech synthesis not supported');
        }
    }
    
    setupEventListeners() {
        if (this.voiceBtn) {
            this.voiceBtn.addEventListener('click', () => {
                this.toggleVoiceRecognition();
            });
        }
        
        // New conversation button
        const newConversationBtn = document.getElementById('new-conversation-btn');
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', () => {
                this.startNewConversation();
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.toggleVoiceRecognition();
            }
        });
    }
    
    async initializeChatSession() {
        try {
            const response = await fetch('/api/new-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            if (data.success) {
                this.currentChatId = data.chat_id;
            }
        } catch (error) {
            console.error('Error initializing chat session:', error);
        }
    }
    
    toggleVoiceRecognition() {
        if (this.isListening) {
            this.stopListening();
            this.isConversationActive = false;
        } else if (!this.isProcessing) {
            this.startListening();
            this.isConversationActive = true;
        }
    }
    
    startListening() {
        if (!this.recognition) {
            this.showError('Voice recognition not available');
            return;
        }
        
        try {
            this.hideDisplays();
            this.recognition.start();
            this.showToast('Voice recognition started', 'info');
        } catch (error) {
            console.error('Error starting voice recognition:', error);
            this.showError('Could not start voice recognition');
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
    
    updateUI(state) {
        this.clearWaves();
        
        switch (state) {
            case 'listening':
                this.voiceBtn.classList.add('active');
                this.voiceIcon.className = 'fas fa-stop text-white text-4xl';
                this.voiceStatus.classList.remove('hidden');
                this.statusText.textContent = 'Listening... Speak now';
                this.startWaves('listening');
                break;
                
            case 'processing':
                this.voiceBtn.classList.remove('active');
                this.voiceBtn.classList.add('opacity-50');
                this.voiceIcon.className = 'fas fa-cog fa-spin text-white text-4xl';
                this.statusText.textContent = 'Processing...';
                break;
                
            case 'speaking':
                this.statusText.textContent = 'Assistant speaking...';
                this.voiceIcon.className = 'fas fa-volume-up text-white text-4xl';
                this.startWaves('speaking');
                break;
                
            case 'idle':
            default:
                this.voiceBtn.classList.remove('active', 'opacity-50');
                this.voiceIcon.className = 'fas fa-microphone text-white text-4xl';
                this.voiceStatus.classList.add('hidden');
                break;
        }
    }
    
    startWaves(type) {
        const waves = [this.wave1, this.wave2, this.wave3, this.wave4];
        waves.forEach(wave => {
            if (wave) {
                wave.classList.remove('listening', 'speaking');
                wave.classList.add(type);
            }
        });
    }
    
    clearWaves() {
        const waves = [this.wave1, this.wave2, this.wave3, this.wave4];
        waves.forEach(wave => {
            if (wave) {
                wave.classList.remove('listening', 'speaking');
            }
        });
    }
    
    updateTranscript(text, isFinal) {
        this.transcriptText.textContent = text;
        this.transcriptDisplay.classList.remove('hidden');
        
        if (isFinal) {
            this.transcriptText.classList.add('font-semibold');
        } else {
            this.transcriptText.classList.remove('font-semibold');
        }
    }
    
    async processUserInput(transcript) {
        if (!transcript.trim()) return;
        
        // Check if user wants to end conversation
        if (this.isConversationEndPhrase(transcript)) {
            this.endConversation();
            return;
        }
        
        this.isProcessing = true;
        this.isConversationActive = true;
        this.updateUI('processing');
        
        try {
            const response = await fetch('/api/send_message', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: transcript
                })
            });
            
            const data = await response.json();
            
            if (data.bot_response) {
                this.showResponse(data.bot_response.content);
                this.speakResponse(data.bot_response.content);
            } else {
                this.showError('No response received');
            }
        } catch (error) {
            console.error('Error processing message:', error);
            this.showError('Failed to process your message');
        } finally {
            this.isProcessing = false;
        }
    }
    
    isConversationEndPhrase(text) {
        const endPhrases = [
            'thank you', 'thanks', 'bye', 'goodbye', 'see you later',
            'that\'s all', 'i\'m done', 'end conversation', 'stop',
            'exit', 'quit', 'finished', 'done', 'good bye'
        ];
        
        const lowerText = text.toLowerCase().trim();
        return endPhrases.some(phrase => lowerText.includes(phrase));
    }
    
    endConversation() {
        this.isConversationActive = false;
        this.updateUI('idle');
        this.showResponse('Thank you for using DineDesk! Have a great day!');
        this.speakResponse('Thank you for using DineDesk! Have a great day!');
    }
    
    showResponse(text) {
        this.responseText.textContent = text;
        this.responseDisplay.classList.remove('hidden');
    }
    
    speakResponse(text) {
        if (!this.synthesis) return;
        
        this.updateUI('speaking');
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        
        utterance.onend = () => {
            // If conversation is active, continue listening for next input
            if (this.isConversationActive) {
                setTimeout(() => {
                    this.startListening();
                }, 1000); // Brief pause before listening again
            } else {
                this.updateUI('idle');
            }
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.updateUI('idle');
        };
        
        this.synthesis.speak(utterance);
    }
    
    async startNewConversation() {
        try {
            this.hideDisplays();
            await this.initializeChatSession();
            this.showToast('New conversation started', 'success');
        } catch (error) {
            console.error('Error starting new conversation:', error);
            this.showError('Failed to start new conversation');
        }
    }
    
    hideDisplays() {
        this.transcriptDisplay.classList.add('hidden');
        this.responseDisplay.classList.add('hidden');
    }
    
    disableVoiceButton() {
        if (this.voiceBtn) {
            this.voiceBtn.disabled = true;
            this.voiceBtn.classList.add('opacity-50', 'cursor-not-allowed');
            this.voiceBtn.title = 'Voice recognition not supported';
        }
    }
    
    handleSpeechError(error) {
        let errorMessage = 'Voice recognition error';
        
        switch (error) {
            case 'not-allowed':
                errorMessage = 'Microphone access denied. Please allow microphone access.';
                break;
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone not found. Please check your microphone.';
                break;
            case 'network':
                errorMessage = 'Network error. Please check your connection.';
                break;
            case 'aborted':
                return; // Don't show error for intentional stops
        }
        
        this.showError(errorMessage);
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-notification px-4 py-3 rounded-lg shadow-lg text-white mb-2 transform transition-all duration-300 translate-x-full`;
        
        switch (type) {
            case 'success':
                toast.classList.add('bg-green-500');
                break;
            case 'error':
                toast.classList.add('bg-red-500');
                break;
            case 'warning':
                toast.classList.add('bg-yellow-500');
                break;
            default:
                toast.classList.add('bg-blue-500');
        }
        
        toast.textContent = message;
        
        const container = document.getElementById('toast-container');
        container.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);
        
        // Remove toast after 4 seconds
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }
    
    showError(message) {
        this.showToast(message, 'error');
    }
}

// Initialize Voice Assistant
document.addEventListener('DOMContentLoaded', () => {
    window.voiceAssistant = new VoiceAssistant();
});