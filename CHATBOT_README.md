# Our Books Intelligent Chatbot

## Overview

The Our Books Intelligent Chatbot is an AI-powered study assistant that provides context-aware responses based on your educational content. It uses Google's Gemini 2.5 Flash model to answer questions about Chemistry, Physics, Mathematics, and Biology.

## Features

### 🧠 **Intelligent Context Matching**
- Automatically detects which subject/chapter your question relates to
- Provides detailed explanations based on your textbook content
- Falls back to general responses for non-educational questions

### 🔄 **API Key Rotation**
- Supports multiple Gemini API keys for better rate limiting
- Automatic key rotation to distribute usage
- Usage tracking to prevent exceeding limits

### 📐 **LaTeX Math Rendering**
- Renders mathematical equations beautifully
- Supports inline and display math
- Perfect for numerical problems and formulas

### 💬 **Conversation Memory**
- Remembers your conversation history
- Maintains context across multiple questions
- Saves conversations locally in your browser

### 🎨 **Modern UI**
- Floating chat widget with smooth animations
- Responsive design for mobile and desktop
- Dark theme that matches your website

## Setup Instructions

### 1. Get Gemini API Keys

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Repeat to create multiple keys (recommended: 3-5 keys)

### 2. Configure API Keys

Edit `assets/js/config.js` and replace the placeholder keys:

```javascript
window.OurBooksConfig = {
    apiKeys: [
        "your-actual-api-key-1",
        "your-actual-api-key-2", 
        "your-actual-api-key-3",
        "your-actual-api-key-4",
        "your-actual-api-key-5"
    ],
    // ... other settings
};
```

### 3. Adjust Settings (Optional)

```javascript
window.OurBooksConfig = {
    // API Configuration
    maxRequestsPerKey: 100,        // Requests per key per day
    model: "gemini-2.5-flash-preview-05-20",
    
    // Chatbot Settings
    maxConversationHistory: 50,    // Max messages to remember
    enableTypingIndicator: true,   // Show typing animation
    enableLaTeX: true,            // Render math equations
    
    // Content Settings
    enableContextMatching: true,   // Match questions to content
    contextThreshold: 0.7,        // Confidence threshold
    
    // UI Settings
    theme: "dark",                // dark, light, auto
    position: "bottom-right",     // Widget position
    
    // Debug Settings
    debug: false,                 // Console logging
    logApiRequests: false         // Log API calls
};
```

## Usage Examples

### Subject-Specific Questions
```
User: "Explain stoichiometry"
Bot: "Stoichiometry is the study of quantitative relationships in chemical reactions..."

User: "What is Newton's second law?"
Bot: "Newton's second law states that F = ma, where F is force, m is mass..."

User: "How do I solve quadratic equations?"
Bot: "A quadratic equation has the form ax² + bx + c = 0. You can solve it using..."
```

### Chapter-Specific Questions
```
User: "In Chemistry Chapter 1, what is the mole concept?"
Bot: "According to Chemistry Chapter 1: Stoichiometry, the mole concept is..."

User: "Explain atomic structure from Class XI"
Bot: "In Physics Class XI Chapter 2: Atomic Structure, we learn that..."
```

### Mathematical Problems
```
User: "Solve: 2x + 5 = 13"
Bot: "To solve 2x + 5 = 13:
      Step 1: Subtract 5 from both sides
      2x = 13 - 5 = 8
      Step 2: Divide by 2
      x = 8/2 = 4
      
      Therefore, x = 4"
```

### LaTeX Examples
```
User: "What is the quadratic formula?"
Bot: "The quadratic formula is:
      $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
      
      Where a, b, and c are coefficients of the quadratic equation ax² + bx + c = 0"
```

## File Structure

```
assets/
├── css/
│   └── chatbot.css          # Chatbot styling
├── js/
│   ├── config.js            # Configuration file
│   └── chatbot.js           # Main chatbot logic
└── ...

add_chatbot_to_chapters.py   # Script to add chatbot to all chapters
CHATBOT_README.md            # This file
```

## Technical Details

### Content Mapping
The chatbot maintains a comprehensive map of all subjects and chapters:

- **Chemistry**: 11 chapters (XI) + 14 chapters (XII)
- **Physics**: 14 chapters (XI) + 14 chapters (XII)  
- **Mathematics**: 12 chapters (XI) + 13 chapters (XII)
- **Biology**: 14 chapters (XI) + 13 chapters (XII)

### API Integration
- Uses Gemini 2.5 Flash model for fast responses
- Implements automatic retry logic for failed requests
- Tracks usage per API key to prevent rate limiting

### Browser Compatibility
- Works on all modern browsers
- Responsive design for mobile devices
- Uses localStorage for conversation persistence

## Troubleshooting

### Common Issues

1. **Chatbot not appearing**
   - Check if `config.js` and `chatbot.js` are loaded
   - Verify API keys are correctly set
   - Check browser console for errors

2. **API errors**
   - Verify API keys are valid and have quota
   - Check if you've exceeded rate limits
   - Ensure internet connection is stable

3. **LaTeX not rendering**
   - Check if MathJax is loaded
   - Verify LaTeX syntax in responses
   - Try refreshing the page

4. **Context not matching**
   - Questions need to contain subject/chapter keywords
   - Try being more specific: "Chemistry Chapter 1"
   - Check if content mapping is correct

### Debug Mode
Enable debug mode in `config.js`:

```javascript
window.OurBooksConfig = {
    debug: true,
    logApiRequests: true
};
```

This will log detailed information to the browser console.

## Customization

### Adding New Subjects
Edit the `initializeContentMap()` function in `chatbot.js`:

```javascript
newSubject: {
    xi: {
        path: "newsubjectbooks",
        chapters: [
            { num: 1, name: "Chapter Name", topics: ["topic1", "topic2"] }
        ]
    }
}
```

### Modifying UI
Edit `assets/css/chatbot.css` to customize:
- Colors and themes
- Widget position
- Animation effects
- Responsive breakpoints

### Changing Behavior
Modify `assets/js/chatbot.js` to:
- Add new features
- Change response patterns
- Implement custom logic

## Security Notes

- API keys are stored in client-side JavaScript
- Consider using environment variables for production
- Monitor API usage to prevent abuse
- Implement rate limiting on your server if needed

## Support

For issues or questions:
1. Check the browser console for errors
2. Verify your API key configuration
3. Test with simple questions first
4. Check the troubleshooting section above

## License

This chatbot is part of the Our Books project and follows the same licensing terms.