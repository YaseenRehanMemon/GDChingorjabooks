// Urdu Translation System
class UrduTranslator {
    constructor() {
        this.config = window.OurBooksConfig || {};
        this.apiKeys = this.config.apiKeys || [];
        this.currentKeyIndex = 0;
        this.keyUsageCount = new Array(this.apiKeys.length).fill(0);
        this.maxRequestsPerKey = this.config.maxRequestsPerKey || 100;
        this.translationCache = new Map();
        this.isTranslating = false;
        this.init();
    }

    init() {
        this.createLanguageToggle();
        this.loadTranslationCache();
        this.setupEventListeners();
    }

    createLanguageToggle() {
        const toggleHTML = `
            <div id="language-toggle" class="language-toggle">
                <button id="lang-en-btn" class="lang-btn active" data-lang="en">
                    <span>English</span>
                </button>
                <button id="lang-ur-btn" class="lang-btn" data-lang="ur">
                    <span>اردو</span>
                </button>
            </div>
        `;

        // Insert after the header
        const header = document.querySelector('header');
        if (header) {
            header.insertAdjacentHTML('afterend', toggleHTML);
        }
    }

    setupEventListeners() {
        const enBtn = document.getElementById('lang-en-btn');
        const urBtn = document.getElementById('lang-ur-btn');

        if (enBtn && urBtn) {
            enBtn.addEventListener('click', () => this.switchLanguage('en'));
            urBtn.addEventListener('click', () => this.switchLanguage('ur'));
        }
    }

    async switchLanguage(lang) {
        if (this.isTranslating) {
            this.showNotification('Translation in progress, please wait...', 'info');
            return;
        }

        const currentLang = this.getCurrentLanguage();
        if (currentLang === lang) return;

        // Update button states
        this.updateButtonStates(lang);

        if (lang === 'ur') {
            await this.translateToUrdu();
        } else {
            this.showOriginalContent();
        }
    }

    getCurrentLanguage() {
        const urBtn = document.getElementById('lang-ur-btn');
        return urBtn && urBtn.classList.contains('active') ? 'ur' : 'en';
    }

    updateButtonStates(lang) {
        const enBtn = document.getElementById('lang-en-btn');
        const urBtn = document.getElementById('lang-ur-btn');

        if (enBtn && urBtn) {
            enBtn.classList.toggle('active', lang === 'en');
            urBtn.classList.toggle('active', lang === 'ur');
        }
    }

    async translateToUrdu() {
        this.isTranslating = true;
        this.showNotification('Translating to Urdu...', 'info');

        try {
            // Get the main content
            const contentElement = document.querySelector('.content');
            if (!contentElement) {
                throw new Error('Content element not found');
            }

            // Check if we have cached translation
            const pageKey = this.getPageKey();
            if (this.translationCache.has(pageKey)) {
                this.applyTranslation(this.translationCache.get(pageKey));
                this.showNotification('Translation loaded from cache', 'success');
                return;
            }

            // Extract text content
            const textContent = this.extractTextContent(contentElement);
            
            // Translate using Gemini API
            const translation = await this.translateWithGemini(textContent);
            
            // Cache the translation
            this.translationCache.set(pageKey, translation);
            this.saveTranslationCache();

            // Apply translation
            this.applyTranslation(translation);
            this.showNotification('Translation completed!', 'success');

        } catch (error) {
            console.error('Translation error:', error);
            this.showNotification('Translation failed. Please try again.', 'error');
        } finally {
            this.isTranslating = false;
        }
    }

    extractTextContent(element) {
        // Clone the element to avoid modifying the original
        const clone = element.cloneNode(true);
        
        // Remove script tags and other non-content elements
        const scripts = clone.querySelectorAll('script, style, .theme-toggle-checkbox, .theme-toggle-label');
        scripts.forEach(el => el.remove());

        // Extract text content
        return clone.textContent.trim();
    }

    async translateWithGemini(text) {
        const apiKey = this.getNextApiKey();
        if (!apiKey) {
            throw new Error('No available API keys');
        }

        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${apiKey}`;

        const prompt = `Translate the following educational content from English to Urdu. This is a textbook chapter about science subjects (Chemistry, Physics, Mathematics, Biology). 

IMPORTANT INSTRUCTIONS:
1. Translate ALL text content to Urdu
2. Keep mathematical formulas and equations in LaTeX format unchanged
3. Keep chemical formulas unchanged (like H2O, CO2, etc.)
4. Keep scientific symbols and units unchanged
5. Maintain the educational tone and structure
6. Use proper Urdu scientific terminology
7. Preserve HTML structure and formatting
8. Return ONLY the translated content, no explanations

Content to translate:
${text}`;

        const payload = {
            contents: [{
                parts: [{ text: prompt }]
            }],
            generationConfig: {
                temperature: 0.3,
                topK: 40,
                topP: 0.95,
                maxOutputTokens: 4096,
            }
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }

        const result = await response.json();
        return result?.candidates?.[0]?.content?.parts?.[0]?.text || '';
    }

    applyTranslation(translation) {
        const contentElement = document.querySelector('.content');
        if (!contentElement) return;

        // Store original content if not already stored
        if (!contentElement.dataset.originalContent) {
            contentElement.dataset.originalContent = contentElement.innerHTML;
        }

        // Apply translation
        contentElement.innerHTML = translation;

        // Re-render MathJax if present
        if (window.MathJax) {
            MathJax.typesetPromise([contentElement]).catch(err => {
                console.error('MathJax rendering error:', err);
            });
        }
    }

    showOriginalContent() {
        const contentElement = document.querySelector('.content');
        if (!contentElement || !contentElement.dataset.originalContent) return;

        contentElement.innerHTML = contentElement.dataset.originalContent;

        // Re-render MathJax if present
        if (window.MathJax) {
            MathJax.typesetPromise([contentElement]).catch(err => {
                console.error('MathJax rendering error:', err);
            });
        }
    }

    getPageKey() {
        return window.location.pathname;
    }

    getNextApiKey() {
        // Find a key that hasn't exceeded its limit
        for (let i = 0; i < this.apiKeys.length; i++) {
            const keyIndex = (this.currentKeyIndex + i) % this.apiKeys.length;
            if (this.keyUsageCount[keyIndex] < this.maxRequestsPerKey) {
                this.currentKeyIndex = keyIndex;
                this.keyUsageCount[keyIndex]++;
                return this.apiKeys[keyIndex];
            }
        }
        return null; // All keys exhausted
    }

    showNotification(message, type = 'info') {
        // Remove existing notification
        const existing = document.getElementById('translation-notification');
        if (existing) {
            existing.remove();
        }

        const notification = document.createElement('div');
        notification.id = 'translation-notification';
        notification.textContent = message;
        
        const colors = {
            info: '#3b82f6',
            success: '#10b981',
            error: '#ef4444'
        };

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type]};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 10000;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 3000);
    }

    saveTranslationCache() {
        try {
            const cacheData = Array.from(this.translationCache.entries());
            localStorage.setItem('urdu_translation_cache', JSON.stringify(cacheData));
        } catch (error) {
            console.error('Error saving translation cache:', error);
        }
    }

    loadTranslationCache() {
        try {
            const saved = localStorage.getItem('urdu_translation_cache');
            if (saved) {
                const cacheData = JSON.parse(saved);
                this.translationCache = new Map(cacheData);
            }
        } catch (error) {
            console.error('Error loading translation cache:', error);
        }
    }
}

// Initialize translator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on chapter pages
    if (window.location.pathname.includes('ch') && window.location.pathname.includes('.html')) {
        window.urduTranslator = new UrduTranslator();
    }
});