/**
 * LLM Chat Interface
 * Handles communication with LLM backend API for intelligent assistance
 */

class LLMChat {
    constructor() {
        this.messages = [];
        this.sessionId = null;
        this.inputPath = null;
        this.outputPath = null;
        this.isTyping = false;
        
        this.messagesContainer = null;
        this.inputField = null;
        this.sendButton = null;
        this.statusDot = null;
        this.statusText = null;
        
        this.init();
    }
    
    /**
     * Initialize chat interface
     */
    init() {
        console.log('[LLM Chat] Initializing...');
        
        // Get DOM elements
        this.messagesContainer = document.getElementById('llm-messages');
        this.inputField = document.getElementById('llm-input');
        this.sendButton = document.getElementById('send-message');
        this.statusDot = document.getElementById('llm-status-dot');
        this.statusText = document.getElementById('llm-status-text');
        
        if (!this.messagesContainer || !this.inputField || !this.sendButton) {
            console.error('[LLM Chat] Required DOM elements not found');
            return;
        }
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Check LLM service status
        this.checkServiceStatus();
    }
    
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Send button
        this.sendButton.addEventListener('click', () => this.handleSendMessage());
        
        // Enter key in input
        this.inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });
        
        // Auto-resize textarea
        this.inputField.addEventListener('input', () => {
            this.inputField.style.height = 'auto';
            this.inputField.style.height = this.inputField.scrollHeight + 'px';
        });
        
        // Clear history button
        const clearBtn = document.getElementById('clear-history');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearHistory());
        }
        
        // Auto-explain button
        const explainBtn = document.getElementById('auto-explain');
        if (explainBtn) {
            explainBtn.addEventListener('click', () => this.requestAutoExplanation());
        }
        
        // Summary button
        const summaryBtn = document.getElementById('auto-summary');
        if (summaryBtn) {
            summaryBtn.addEventListener('click', () => this.requestSummary());
        }
        
        // Quick action buttons
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.currentTarget.dataset.question;
                if (question) {
                    this.inputField.value = question;
                    this.handleSendMessage();
                }
            });
        });
        
        // Suggestion cards
        document.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const question = e.currentTarget.dataset.question;
                if (question) {
                    this.inputField.value = question;
                    this.handleSendMessage();
                }
            });
        });
    }
    
    /**
     * Check LLM service status
     */
    async checkServiceStatus() {
        try {
            const response = await fetch('/api/llm/status');
            const data = await response.json();
            
            if (data.success && data.status.available) {
                this.updateStatus('online', 'LLM Service Online');
            } else {
                this.updateStatus('offline', 'LLM Service Offline');
                this.showAlert('warning', 'LLM service is not available. Please ensure LM Studio is running.');
            }
        } catch (error) {
            console.error('[LLM Chat] Error checking service status:', error);
            this.updateStatus('offline', 'Connection Error');
            this.showAlert('error', 'Cannot connect to LLM service.');
        }
    }
    
    /**
     * Update status indicator
     */
    updateStatus(status, text) {
        if (this.statusDot) {
            this.statusDot.className = 'status-dot ' + status;
        }
        if (this.statusText) {
            this.statusText.textContent = text;
        }
    }
    
    /**
     * Show welcome message
     */
    showWelcomeMessage() {
        this.addSystemMessage('Welcome! I can help you understand the MARK analysis results. Ask me anything about the analyzed project.');
    }
    
    /**
     * Set project paths for context
     */
    setProjectPaths(inputPath, outputPath) {
        this.inputPath = inputPath;
        this.outputPath = outputPath;
        console.log('[LLM Chat] Project paths set:', { inputPath, outputPath });
    }
    
    /**
     * Handle send message
     */
    async handleSendMessage() {
        const message = this.inputField.value.trim();
        
        if (!message || this.isTyping) {
            return;
        }
        
        if (!this.inputPath || !this.outputPath) {
            this.showAlert('warning', 'Please run an analysis first from the Input tab.');
            return;
        }
        
        // Clear input
        this.inputField.value = '';
        this.inputField.style.height = 'auto';
        
        // Add user message
        this.addMessage('user', message);
        
        // Show typing indicator (after a small delay to ensure message is rendered)
        setTimeout(() => {
            this.setTyping(true);
        }, 50);
        
        try {
            // Send to backend
            const response = await fetch('/api/llm/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    input_path: this.inputPath,
                    output_path: this.outputPath,
                    question: message,
                    session_id: this.sessionId,
                    history: this.messages.filter(m => m.role !== 'system').map(m => ({
                        role: m.role,
                        content: m.content
                    }))
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update session ID
                this.sessionId = data.session_id;
                
                // Add assistant response
                this.addMessage('assistant', data.answer);
            } else {
                this.showAlert('error', data.message || 'Error getting response from LLM');
            }
            
        } catch (error) {
            console.error('[LLM Chat] Error sending message:', error);
            this.showAlert('error', 'Failed to communicate with LLM service.');
        } finally {
            this.setTyping(false);
        }
    }
    
    /**
     * Request automatic explanation
     */
    async requestAutoExplanation() {
        if (!this.inputPath || !this.outputPath) {
            this.showAlert('warning', 'Please run an analysis first from the Input tab.');
            return;
        }
        
        this.setTyping(true);
        this.addSystemMessage('Generating automatic explanation...');
        
        try {
            const response = await fetch('/api/llm/explain', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    input_path: this.inputPath,
                    output_path: this.outputPath
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('assistant', data.explanation);
            } else {
                this.showAlert('error', data.message || 'Error generating explanation');
            }
            
        } catch (error) {
            console.error('[LLM Chat] Error requesting explanation:', error);
            this.showAlert('error', 'Failed to generate explanation.');
        } finally {
            this.setTyping(false);
        }
    }
    
    /**
     * Request project summary
     */
    async requestSummary() {
        if (!this.inputPath || !this.outputPath) {
            this.showAlert('warning', 'Please run an analysis first from the Input tab.');
            return;
        }
        
        this.setTyping(true);
        this.addSystemMessage('Generating project summary...');
        
        try {
            const response = await fetch('/api/llm/summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    input_path: this.inputPath,
                    output_path: this.outputPath
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('assistant', data.summary);
            } else {
                this.showAlert('error', data.message || 'Error generating summary');
            }
            
        } catch (error) {
            console.error('[LLM Chat] Error requesting summary:', error);
            this.showAlert('error', 'Failed to generate summary.');
        } finally {
            this.setTyping(false);
        }
    }
    
    /**
     * Add message to chat
     */
    addMessage(role, content) {
        // Store message
        this.messages.push({ role, content, timestamp: new Date() });
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `llm-message ${role}`;
        
        let avatarHtml = '';
        if (role === 'user') {
            avatarHtml = '<div class="message-avatar user-avatar"><i class="bi bi-person-fill"></i></div>';
        } else if (role === 'assistant') {
            avatarHtml = '<div class="message-avatar assistant-avatar"><i class="bi bi-robot"></i></div>';
        }
        
        const contentHtml = `
            ${role === 'user' ? '' : avatarHtml}
            <div class="message-content">
                ${this.formatMessage(content)}
                <span class="message-timestamp">${this.formatTime(new Date())}</span>
            </div>
            ${role === 'user' ? avatarHtml : ''}
        `;
        
        messageDiv.innerHTML = contentHtml;
        
        // Remove empty state if present
        const emptyState = this.messagesContainer.querySelector('.llm-empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        // Insert message before typing indicator (so typing indicator stays at bottom)
        const typingIndicatorContainer = this.messagesContainer.querySelector('.llm-message.assistant:has(#typing-indicator)');
        if (typingIndicatorContainer) {
            this.messagesContainer.insertBefore(messageDiv, typingIndicatorContainer);
        } else {
            this.messagesContainer.appendChild(messageDiv);
        }
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    /**
     * Add system message
     */
    addSystemMessage(content) {
        // Remove empty state if present
        const emptyState = this.messagesContainer.querySelector('.llm-empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'llm-message system';
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="bi bi-info-circle"></i> ${content}
            </div>
        `;
        
        // Insert message before typing indicator (so typing indicator stays at bottom)
        const typingIndicatorContainer = this.messagesContainer.querySelector('.llm-message.assistant:has(#typing-indicator)');
        if (typingIndicatorContainer) {
            this.messagesContainer.insertBefore(messageDiv, typingIndicatorContainer);
        } else {
            this.messagesContainer.appendChild(messageDiv);
        }
        this.scrollToBottom();
    }
    
    /**
     * Show alert message
     */
    showAlert(type, message) {
        // Remove empty state if present
        const emptyState = this.messagesContainer.querySelector('.llm-empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `llm-alert ${type}`;
        
        const icon = type === 'error' ? 'exclamation-triangle-fill' : 
                     type === 'warning' ? 'exclamation-circle-fill' : 
                     'info-circle-fill';
        
        alertDiv.innerHTML = `
            <i class="bi bi-${icon}"></i>
            <span>${message}</span>
        `;
        
        // Insert alert before typing indicator (so typing indicator stays at bottom)
        const typingIndicatorContainer = this.messagesContainer.querySelector('.llm-message.assistant:has(#typing-indicator)');
        if (typingIndicatorContainer) {
            this.messagesContainer.insertBefore(alertDiv, typingIndicatorContainer);
        } else {
            this.messagesContainer.appendChild(alertDiv);
        }
        this.scrollToBottom();
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    /**
     * Set typing indicator
     */
    setTyping(typing) {
        this.isTyping = typing;
        this.inputField.disabled = typing;
        this.sendButton.disabled = typing;
        
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            if (typing) {
                typingIndicator.classList.add('active');
                this.scrollToBottom();
            } else {
                typingIndicator.classList.remove('active');
            }
        }
    }
    
    /**
     * Clear conversation history
     */
    async clearHistory() {
        if (!confirm('Are you sure you want to clear the conversation history?')) {
            return;
        }
        
        // Clear session on server if exists
        if (this.sessionId) {
            try {
                await fetch(`/api/llm/session/${this.sessionId}`, {
                    method: 'DELETE'
                });
            } catch (error) {
                console.error('[LLM Chat] Error clearing session:', error);
            }
        }
        
        // Clear local state
        this.messages = [];
        this.sessionId = null;
        
        // Clear UI and restore empty state
        this.messagesContainer.innerHTML = `
            <!-- Empty State -->
            <div class="llm-empty-state">
                <i class="bi bi-chat-dots"></i>
                <h3>Welcome to LLM Assistant</h3>
                <p>I can help you understand your MARK analysis results. Start by asking a question or try one of these:</p>
                
                <div class="llm-suggestions">
                    <div class="suggestion-card" data-question="Why is this project classified as a Producer?">
                        <i class="bi bi-question-circle-fill"></i>
                        <strong>Classification</strong>
                        <small>Understand the classification reasoning</small>
                    </div>
                    
                    <div class="suggestion-card" data-question="What ML libraries are being used?">
                        <i class="bi bi-stack"></i>
                        <strong>Libraries</strong>
                        <small>Learn about detected ML libraries</small>
                    </div>
                    
                    <div class="suggestion-card" data-question="What is the application domain of this project?">
                        <i class="bi bi-globe"></i>
                        <strong>Domain</strong>
                        <small>Infer the project's purpose</small>
                    </div>
                    
                    <div class="suggestion-card" data-question="What keywords were detected and what do they mean?">
                        <i class="bi bi-tags"></i>
                        <strong>Keywords</strong>
                        <small>Explore detected API keywords</small>
                    </div>
                </div>
            </div>
            
            <!-- Typing Indicator -->
            <div class="llm-message assistant">
                <div class="message-avatar assistant-avatar">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="typing-indicator" id="typing-indicator">
                    <div class="typing-dots">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
            </div>
        `;
        
        // Re-attach event listeners for suggestion cards
        document.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const question = e.currentTarget.dataset.question;
                if (question) {
                    this.inputField.value = question;
                    this.handleSendMessage();
                }
            });
        });
    }
    
    /**
     * Format message content (basic markdown-like)
     */
    formatMessage(content) {
        // Escape HTML
        let formatted = content
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
        
        // Bold
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Inline code
        formatted = formatted.replace(/`(.+?)`/g, '<code>$1</code>');
        
        // Code blocks
        formatted = formatted.replace(/```([\s\S]+?)```/g, '<pre><code>$1</code></pre>');
        
        // Line breaks
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }
    
    /**
     * Format timestamp
     */
    formatTime(date) {
        return date.toLocaleTimeString('it-IT', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    /**
     * Scroll to bottom of messages
     */
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
}

// Global instance
window.llmChat = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit to ensure all elements are loaded
    setTimeout(() => {
        window.llmChat = new LLMChat();
    }, 500);
});

// Listen for tab changes to refresh paths
document.addEventListener('tabChanged', (e) => {
    if (e.detail.tab === 'LLM Assistant' && window.llmChat) {
        // Get paths from session storage
        const inputPath = sessionStorage.getItem('lastInputPath');
        const outputPath = sessionStorage.getItem('lastOutputPath');
        
        if (inputPath && outputPath) {
            window.llmChat.setProjectPaths(inputPath, outputPath);
        }
    }
});
