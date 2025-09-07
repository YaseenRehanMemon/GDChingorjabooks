// Our Books Chatbot Configuration
window.OurBooksConfig = {
    // Add your Gemini API keys here
    // Get them from: https://makersuite.google.com/app/apikey
    apiKeys: [
        "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw",
        "AIzaSyC12_noKxy5jJJfGoLUWpAiWPXHnBxD1-Q", 
        "AIzaSyD19bjFIt1fNXI0RQy-3BHtZasX-rdZDqo",
        "AIzaSyBaJWfsgTaXwkNy711OXHIcBNe8dV7fF_8 ",
        "AIzaSyCJAus6nrOanNRhWu0rkJJ6Z4CecouJE1E"
    ],
    
    // API Configuration
    maxRequestsPerKey: 100, // Adjust based on your API limits
    model: "gemini-2.5-flash-preview-05-20",
    
    // Chatbot Settings
    maxConversationHistory: 50, // Maximum messages to keep in history
    enableTypingIndicator: true,
    enableLaTeX: true,
    
    // Content Settings
    enableContextMatching: true,
    contextThreshold: 0.7, // Minimum confidence for context matching
    
    // UI Settings
    theme: "dark", // dark, light, auto
    position: "bottom-right", // bottom-right, bottom-left, top-right, top-left
    
    // Debug Settings
    debug: true, // Set to true for console logging
    logApiRequests: true // Set to true to log API requests
};