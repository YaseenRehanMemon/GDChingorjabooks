// Text Selection with AI Explanation
class TextSelectionAI {
    constructor() {
        this.selectedText = '';
        this.selectionContext = null;
        this.selectionPopup = null;
        this.isPopupVisible = false;
        this.init();
    }

    init() {
        this.createSelectionPopup();
        this.setupEventListeners();
    }

    createSelectionPopup() {
        const popupHTML = `
            <div id="text-selection-popup" class="text-selection-popup hidden">
                <div class="selection-popup-content">
                    <div class="selection-text">
                        <span id="selected-text-preview"></span>
                    </div>
                    <div class="selection-actions">
                        <button id="ask-ai-btn" class="selection-btn ask-ai-btn">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                            </svg>
                            Ask AI
                        </button>
                        <button id="copy-text-btn" class="selection-btn copy-btn">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
                            </svg>
                            Copy
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', popupHTML);
        this.selectionPopup = document.getElementById('text-selection-popup');
    }

    setupEventListeners() {
        // Listen for text selection
        document.addEventListener('mouseup', (e) => this.handleTextSelection(e));
        document.addEventListener('keyup', (e) => this.handleTextSelection(e));
        
        // Listen for clicks outside popup
        document.addEventListener('click', (e) => {
            if (!this.selectionPopup.contains(e.target) && this.isPopupVisible) {
                this.hidePopup();
            }
        });

        // Setup popup button events
        document.getElementById('ask-ai-btn').addEventListener('click', () => this.askAI());
        document.getElementById('copy-text-btn').addEventListener('click', () => this.copyText());
    }

    handleTextSelection(e) {
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();

        if (selectedText.length > 0 && selectedText.length < 500) {
            this.selectedText = selectedText;
            this.selectionContext = this.getSelectionContext();
            this.showPopup(e);
        } else {
            this.hidePopup();
        }
    }

    getSelectionContext() {
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const container = range.commonAncestorContainer;
        
        // Try to find the chapter context
        let chapterElement = container;
        while (chapterElement && chapterElement.nodeType !== Node.ELEMENT_NODE) {
            chapterElement = chapterElement.parentNode;
        }
        
        while (chapterElement && !chapterElement.classList.contains('content')) {
            chapterElement = chapterElement.parentNode;
        }

        if (chapterElement) {
            const chapterTitle = document.querySelector('h1');
            const subjectInfo = this.extractSubjectFromURL();
            return {
                chapterTitle: chapterTitle ? chapterTitle.textContent : 'Unknown Chapter',
                subject: subjectInfo.subject,
                class: subjectInfo.class,
                chapter: subjectInfo.chapter
            };
        }

        return null;
    }

    extractSubjectFromURL() {
        const path = window.location.pathname;
        const pathParts = path.split('/');
        
        // Extract subject and class from URL
        let subject = 'general';
        let classLevel = 'general';
        let chapter = 'general';

        if (pathParts.includes('chemistrybooks')) {
            subject = 'chemistry';
            classLevel = 'xi';
        } else if (pathParts.includes('chemistryxiibooks')) {
            subject = 'chemistry';
            classLevel = 'xii';
        } else if (pathParts.includes('physicsbooks')) {
            subject = 'physics';
            classLevel = 'xi';
        } else if (pathParts.includes('physicsxiibooks')) {
            subject = 'physics';
            classLevel = 'xii';
        } else if (pathParts.includes('mathbooks')) {
            subject = 'mathematics';
            classLevel = 'xi';
        } else if (pathParts.includes('mathsxiibooks')) {
            subject = 'mathematics';
            classLevel = 'xii';
        } else if (pathParts.includes('biologybooks')) {
            subject = 'biology';
            classLevel = 'xi';
        } else if (pathParts.includes('biologyxiibooks')) {
            subject = 'biology';
            classLevel = 'xii';
        }

        // Extract chapter number from filename
        const filename = pathParts[pathParts.length - 1];
        const chapterMatch = filename.match(/ch(\d+)\.html/);
        if (chapterMatch) {
            chapter = chapterMatch[1];
        }

        return { subject, class: classLevel, chapter };
    }

    showPopup(e) {
        if (!this.selectionPopup) return;

        const popup = this.selectionPopup;
        const preview = document.getElementById('selected-text-preview');
        
        // Update preview text (truncate if too long)
        const displayText = this.selectedText.length > 100 
            ? this.selectedText.substring(0, 100) + '...' 
            : this.selectedText;
        preview.textContent = displayText;

        // Position popup near selection
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Calculate position
        const popupRect = popup.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        let left = rect.left + (rect.width / 2) - (popupRect.width / 2);
        let top = rect.bottom + 10;

        // Adjust if popup goes off screen
        if (left < 10) left = 10;
        if (left + popupRect.width > viewportWidth - 10) {
            left = viewportWidth - popupRect.width - 10;
        }
        if (top + popupRect.height > viewportHeight - 10) {
            top = rect.top - popupRect.height - 10;
        }

        popup.style.left = left + 'px';
        popup.style.top = top + 'px';
        popup.classList.remove('hidden');
        this.isPopupVisible = true;
    }

    hidePopup() {
        if (this.selectionPopup) {
            this.selectionPopup.classList.add('hidden');
            this.isPopupVisible = false;
        }
    }

    async askAI() {
        if (!this.selectedText || !this.selectionContext) return;

        // Hide popup
        this.hidePopup();

        // Open chatbot if not already open
        if (window.ourBooksChatbot && !window.ourBooksChatbot.isOpen) {
            window.ourBooksChatbot.toggleChat();
        }

        // Wait for chatbot to open
        setTimeout(() => {
            // Send the selected text to chatbot with context
            const contextPrompt = this.buildContextPrompt();
            this.sendToChatbot(contextPrompt);
        }, 500);
    }

    buildContextPrompt() {
        const { subject, class: classLevel, chapter, chapterTitle } = this.selectionContext;
        
        let prompt = `I've selected this text from ${subject} ${classLevel === 'xi' ? 'Class XI' : 'Class XII'} Chapter ${chapter}: "${chapterTitle}". `;
        prompt += `Please explain this selected text in detail: "${this.selectedText}"`;
        
        return prompt;
    }

    sendToChatbot(prompt) {
        if (window.ourBooksChatbot) {
            // Set the input value and trigger send
            const input = document.getElementById('chatbot-input');
            if (input) {
                input.value = prompt;
                window.ourBooksChatbot.sendMessage();
            }
        }
    }

    copyText() {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(this.selectedText).then(() => {
                this.showCopyFeedback();
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = this.selectedText;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showCopyFeedback();
        }
        this.hidePopup();
    }

    showCopyFeedback() {
        // Create temporary feedback
        const feedback = document.createElement('div');
        feedback.textContent = 'Copied!';
        feedback.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            z-index: 10002;
            font-size: 14px;
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            document.body.removeChild(feedback);
        }, 2000);
    }
}

// Initialize text selection when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on chapter pages
    if (window.location.pathname.includes('ch') && window.location.pathname.includes('.html')) {
        window.textSelectionAI = new TextSelectionAI();
    }
});