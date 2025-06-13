// Voice input functionality for DineDesk
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
        
        // Add visual feedback
        this.voiceBtn.classList.add('voice-recording');
        this.voiceBtn.innerHTML = '<i class="fas fa-stop text-red-600"></i>';
    }
    
    stopRecording() {
        this.isRecording = false;
        this.updateVoiceButton();
        this.hideVoiceStatus();
        
        // Remove visual feedback
        this.voiceBtn.classList.remove('voice-recording');
        this.voiceBtn.innerHTML = '<i class="fas fa-microphone text-gray-600"></i>';
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
        // Create or update voice status indicator
        let statusElement = document.getElementById('voice-status');
        
        if (!statusElement) {
            statusElement = document.createElement('div');
            statusElement.id = 'voice-status';
            statusElement.className = 'fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-75 text-white px-4 py-2 rounded-lg text-sm z-50';
            document.body.appendChild(statusElement);
        }
        
        statusElement.textContent = message;
        statusElement.style.display = 'block';
    }
    
    hideVoiceStatus() {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.style.display = 'none';
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
    
    // Check microphone permissions
    async checkMicrophonePermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (error) {
            console.error('Microphone permission error:', error);
            return false;
        }
    }
    
    // Request microphone permissions
    async requestMicrophonePermission() {
        const hasPermission = await this.checkMicrophonePermission();
        
        if (!hasPermission) {
            this.dineDesk.showToast(
                'Microphone access is required for voice input. Please enable it in your browser settings.',
                'error',
                5000
            );
        }
        
        return hasPermission;
    }
}

// Initialize voice manager when DineDesk is ready
document.addEventListener('DOMContentLoaded', () => {
    const initVoiceManager = () => {
        if (window.dineDesk) {
            window.voiceManager = new VoiceManager(window.dineDesk);
        } else {
            setTimeout(initVoiceManager, 100);
        }
    };
    
    initVoiceManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceManager;
}
