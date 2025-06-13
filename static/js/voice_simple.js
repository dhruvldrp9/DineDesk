// Voice input functionality for DineDesk (simplified version)
class VoiceManager {
    constructor(dineDesk) {
        this.dineDesk = dineDesk;
        this.isRecording = false;
        this.recognition = null;
        this.voiceBtn = document.getElementById('voice-btn');
        
        this.initializeVoiceRecognition();
        this.setupEventListeners();
    }
    
    initializeVoiceRecognition() {
        // Check for browser support
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
        } else {
            console.log('Speech recognition not supported');
            this.voiceBtn.style.display = 'none';
            return;
        }
        
        // Configure speech recognition
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        
        // Event handlers
        this.recognition.onstart = () => {
            console.log('Voice recognition started');
            this.startRecording();
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
            
            this.updateTranscription(finalTranscript, interimTranscript);
        };
        
        this.recognition.onend = () => {
            console.log('Voice recognition ended');
            this.stopRecording();
        };
        
        this.recognition.onerror = (event) => {
            console.error('Voice recognition error:', event.error);
            this.handleVoiceError(event.error);
            this.stopRecording();
        };
    }
    
    setupEventListeners() {
        if (!this.voiceBtn) return;
        
        this.voiceBtn.addEventListener('click', () => {
            if (this.isRecording) {
                this.stopVoiceRecognition();
            } else {
                this.startVoiceRecognition();
            }
        });
        
        // Keyboard shortcut (Ctrl/Cmd + Shift + V)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'V') {
                e.preventDefault();
                if (this.isRecording) {
                    this.stopVoiceRecognition();
                } else {
                    this.startVoiceRecognition();
                }
            }
        });
    }
    
    startVoiceRecognition() {
        if (!this.recognition) {
            this.dineDesk.showToast('Voice recognition not supported in this browser', 'error');
            return;
        }
        
        if (this.isRecording) return;
        
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting voice recognition:', error);
            this.dineDesk.showToast('Error starting voice recognition', 'error');
        }
    }
    
    stopVoiceRecognition() {
        if (!this.recognition || !this.isRecording) return;
        
        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Error stopping voice recognition:', error);
        }
    }
    
    startRecording() {
        this.isRecording = true;
        this.updateVoiceButton();
        this.showVoiceStatus('Listening... Speak now');
        
        // Update voice icon and button appearance
        const voiceIcon = document.getElementById('voice-icon');
        if (voiceIcon) {
            voiceIcon.className = 'fas fa-stop text-white text-lg';
        }
        
        this.voiceBtn.classList.remove('bg-gray-100', 'hover:bg-gray-200');
        this.voiceBtn.classList.add('bg-red-500', 'hover:bg-red-600');
    }
    
    stopRecording() {
        this.isRecording = false;
        this.updateVoiceButton();
        this.hideVoiceStatus();
        
        // Reset voice icon and button appearance
        const voiceIcon = document.getElementById('voice-icon');
        if (voiceIcon) {
            voiceIcon.className = 'fas fa-microphone text-gray-600 text-lg';
        }
        
        this.voiceBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
        this.voiceBtn.classList.add('bg-gray-100', 'hover:bg-gray-200');
    }
    
    updateVoiceButton() {
        if (!this.voiceBtn) return;
        
        if (this.isRecording) {
            this.voiceBtn.classList.add('bg-red-100', 'hover:bg-red-200');
            this.voiceBtn.classList.remove('bg-gray-100', 'hover:bg-gray-200');
            this.voiceBtn.title = 'Stop recording (Ctrl+Shift+V)';
        } else {
            this.voiceBtn.classList.remove('bg-red-100', 'hover:bg-red-200');
            this.voiceBtn.classList.add('bg-gray-100', 'hover:bg-gray-200');
            this.voiceBtn.title = 'Start voice input (Ctrl+Shift+V)';
        }
    }
    
    updateTranscription(finalTranscript, interimTranscript) {
        const messageInput = document.getElementById('message-input');
        
        if (finalTranscript) {
            // Add final transcript to input
            const currentValue = messageInput.value;
            messageInput.value = currentValue + finalTranscript;
            
            // Trigger input event for character counter
            messageInput.dispatchEvent(new Event('input'));
            
            // Auto-send if transcript seems complete
            if (finalTranscript.trim().endsWith('.') || 
                finalTranscript.trim().endsWith('?') || 
                finalTranscript.trim().endsWith('!')) {
                setTimeout(() => {
                    if (messageInput.value.trim()) {
                        this.dineDesk.sendMessage();
                    }
                }, 500);
            }
        }
        
        // Show interim results in voice status
        if (interimTranscript) {
            this.showVoiceStatus(`Listening: "${interimTranscript}"`);
        }
    }
    
    showVoiceStatus(message) {
        const statusElement = document.getElementById('voice-status');
        
        if (statusElement) {
            const statusText = statusElement.querySelector('span');
            if (statusText) {
                statusText.textContent = message;
            }
            statusElement.classList.remove('hidden');
        }
    }
    
    hideVoiceStatus() {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.classList.add('hidden');
        }
    }
    
    handleVoiceError(error) {
        let errorMessage = 'Voice recognition error';
        
        switch (error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone not accessible. Please check permissions.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please enable microphone access.';
                break;
            case 'network':
                errorMessage = 'Network error during voice recognition.';
                break;
            case 'service-not-allowed':
                errorMessage = 'Voice recognition service not allowed.';
                break;
            default:
                errorMessage = `Voice recognition error: ${error}`;
        }
        
        this.dineDesk.showToast(errorMessage, 'error');
    }
}

// Voice manager is now initialized directly in main_simple.js