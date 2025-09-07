// Our Books Intelligent Chatbot
class OurBooksChatbot {
    constructor() {
        this.isOpen = false;
        this.conversationHistory = [];
        this.config = window.OurBooksConfig || {};
        this.apiKeys = this.config.apiKeys || [];
        this.currentKeyIndex = 0;
        this.keyUsageCount = new Array(this.apiKeys.length).fill(0);
        this.maxRequestsPerKey = this.config.maxRequestsPerKey || 100;
        
        // Content mapping for all subjects and chapters
        this.contentMap = this.initializeContentMap();
        
        this.init();
    }

    init() {
        this.createChatWidget();
        this.loadConversationHistory();
        this.setupEventListeners();
    }

    // Initialize content mapping for all subjects and chapters
    initializeContentMap() {
        return {
            chemistry: {
                xi: {
                    path: "chemistrybooks",
                    chapters: [
                        { num: 1, name: "Stoichiometry", topics: ["mole concept", "calculations", "limiting reactant", "reaction yield"] },
                        { num: 2, name: "Atomic Structure", topics: ["atomic models", "electron configuration", "quantum numbers", "periodic trends"] },
                        { num: 3, name: "Chemical Bonding", topics: ["ionic bonding", "covalent bonding", "metallic bonding", "lewis structures"] },
                        { num: 4, name: "States of Matter", topics: ["gas laws", "liquid properties", "solid structures", "phase changes"] },
                        { num: 5, name: "Thermodynamics", topics: ["enthalpy", "entropy", "gibbs free energy", "heat capacity"] },
                        { num: 6, name: "Chemical Equilibrium", topics: ["equilibrium constant", "le chatelier principle", "reaction quotient"] },
                        { num: 7, name: "Acids, Bases, and Salts", topics: ["pH scale", "buffer solutions", "acid-base titrations", "salt hydrolysis"] },
                        { num: 8, name: "Chemical Kinetics", topics: ["reaction rate", "rate laws", "activation energy", "catalysis"] },
                        { num: 9, name: "Solutions and Colloids", topics: ["solubility", "colligative properties", "osmosis", "colloids"] },
                        { num: 10, name: "Thermochemistry", topics: ["heat of reaction", "calorimetry", "bond energy", "hess law"] },
                        { num: 11, name: "Electrochemistry", topics: ["galvanic cells", "electrolysis", "nernst equation", "corrosion"] }
                    ]
                },
                xii: {
                    path: "chemistryxiibooks",
                    chapters: [
                        { num: 1, name: "Solid State", topics: ["crystal structures", "defects", "electrical properties", "magnetic properties"] },
                        { num: 2, name: "Solutions", topics: ["raoult law", "ideal solutions", "azeotropes", "osmotic pressure"] },
                        { num: 3, name: "Electrochemistry", topics: ["conductance", "kohlrausch law", "batteries", "fuel cells"] },
                        { num: 4, name: "Chemical Kinetics", topics: ["integrated rate laws", "half-life", "temperature dependence", "mechanism"] },
                        { num: 5, name: "Surface Chemistry", topics: ["adsorption", "catalysis", "colloids", "emulsions"] },
                        { num: 6, name: "General Principles and Processes of Isolation of Elements", topics: ["metallurgy", "ore concentration", "extraction", "refining"] },
                        { num: 7, name: "p-Block Elements", topics: ["group 13-18", "properties", "compounds", "applications"] },
                        { num: 8, name: "d- and f-Block Elements", topics: ["transition metals", "lanthanides", "actinides", "coordination compounds"] },
                        { num: 9, name: "Coordination Compounds", topics: ["werner theory", "nomenclature", "isomerism", "bonding"] },
                        { num: 10, name: "Haloalkanes and Haloarenes", topics: ["nomenclature", "preparation", "reactions", "mechanisms"] },
                        { num: 11, name: "Alcohols, Phenols, and Ethers", topics: ["classification", "preparation", "reactions", "properties"] },
                        { num: 12, name: "Aldehydes, Ketones, and Carboxylic Acids", topics: ["nomenclature", "preparation", "reactions", "mechanisms"] },
                        { num: 13, name: "Amines", topics: ["classification", "preparation", "reactions", "properties"] },
                        { num: 14, name: "Biomolecules", topics: ["carbohydrates", "proteins", "nucleic acids", "vitamins"] }
                    ]
                }
            },
            physics: {
                xi: {
                    path: "physicsbooks",
                    chapters: [
                        { num: 1, name: "Physics and Measurements", topics: ["units", "dimensions", "measurement", "errors"] },
                        { num: 2, name: "Kinematics", topics: ["motion", "velocity", "acceleration", "projectile motion"] },
                        { num: 3, name: "Dynamics", topics: ["newton laws", "friction", "momentum", "impulse"] },
                        { num: 4, name: "Rotational and Circular Motion", topics: ["angular velocity", "centripetal force", "moment of inertia", "torque"] },
                        { num: 5, name: "Work, Energy and Power", topics: ["work", "kinetic energy", "potential energy", "conservation"] },
                        { num: 6, name: "Fluid Statics", topics: ["pressure", "pascal law", "archimedes principle", "surface tension"] },
                        { num: 7, name: "Fluid Dynamics", topics: ["bernoulli equation", "viscosity", "turbulence", "reynolds number"] },
                        { num: 8, name: "Electric Fields", topics: ["coulomb law", "electric field", "gauss law", "potential"] },
                        { num: 9, name: "Capacitors", topics: ["capacitance", "parallel plate", "energy", "dielectrics"] },
                        { num: 10, name: "D.C Circuits", topics: ["ohm law", "kirchhoff laws", "power", "resistance"] },
                        { num: 11, name: "Oscillations", topics: ["simple harmonic motion", "pendulum", "damping", "resonance"] },
                        { num: 12, name: "Acoustics", topics: ["sound waves", "frequency", "amplitude", "doppler effect"] },
                        { num: 13, name: "Physical Optics", topics: ["interference", "diffraction", "polarization", "coherence"] },
                        { num: 14, name: "Communication", topics: ["modulation", "demodulation", "antenna", "propagation"] }
                    ]
                },
                xii: {
                    path: "physicsxiibooks",
                    chapters: [
                        { num: 15, name: "Electric Charges and Fields", topics: ["coulomb law", "electric field", "gauss law", "electric dipole"] },
                        { num: 16, name: "Electrostatic Potential and Capacitance", topics: ["electric potential", "equipotential surfaces", "capacitance", "energy"] },
                        { num: 17, name: "Current Electricity", topics: ["drift velocity", "ohm law", "resistivity", "kirchhoff laws"] },
                        { num: 18, name: "Moving Charges and Magnetism", topics: ["magnetic force", "biot-savart law", "ampere law", "solenoid"] },
                        { num: 19, name: "Magnetism and Matter", topics: ["magnetic dipole", "magnetization", "magnetic materials", "hysteresis"] },
                        { num: 20, name: "Electromagnetic Induction", topics: ["faraday law", "lenz law", "self inductance", "mutual inductance"] },
                        { num: 21, name: "Alternating Current", topics: ["ac circuits", "impedance", "resonance", "power factor"] },
                        { num: 22, name: "Electromagnetic Waves", topics: ["maxwell equations", "wave equation", "spectrum", "properties"] },
                        { num: 23, name: "Ray Optics and Optical Instruments", topics: ["reflection", "refraction", "lenses", "mirrors"] },
                        { num: 24, name: "Wave Optics", topics: ["interference", "diffraction", "polarization", "coherence"] },
                        { num: 25, name: "Dual Nature of Radiation and Matter", topics: ["photoelectric effect", "compton effect", "de broglie waves", "uncertainty principle"] },
                        { num: 26, name: "Atoms", topics: ["bohr model", "energy levels", "spectral lines", "quantum mechanics"] },
                        { num: 27, name: "Nuclei", topics: ["nuclear structure", "radioactivity", "nuclear reactions", "binding energy"] },
                        { num: 28, name: "Semiconductor Electronics", topics: ["p-n junction", "diodes", "transistors", "logic gates"] }
                    ]
                }
            },
            mathematics: {
                xi: {
                    path: "mathbooks",
                    chapters: [
                        { num: 1, name: "Complex Numbers", topics: ["imaginary numbers", "argand plane", "polar form", "de moivre theorem"] },
                        { num: 2, name: "Matrices & Determinants", topics: ["matrix operations", "determinants", "inverse", "rank"] },
                        { num: 3, name: "Vectors", topics: ["vector algebra", "dot product", "cross product", "applications"] },
                        { num: 4, name: "Sequences & Series", topics: ["arithmetic progression", "geometric progression", "summation", "convergence"] },
                        { num: 5, name: "Miscellaneous Series", topics: ["special series", "binomial series", "taylor series", "maclaurin series"] },
                        { num: 6, name: "Permutation, Combination & Probability", topics: ["counting principles", "permutations", "combinations", "probability"] },
                        { num: 7, name: "Mathematical Induction & Binomial Theorem", topics: ["induction", "binomial expansion", "coefficients", "applications"] },
                        { num: 8, name: "Functions & Graphs", topics: ["domain", "range", "graphing", "transformations"] },
                        { num: 9, name: "Linear Inequalities", topics: ["inequality solving", "graphical method", "systems", "applications"] },
                        { num: 10, name: "Trigonometric Identities", topics: ["identities", "sum and difference", "double angle", "half angle"] },
                        { num: 11, name: "Application of Trigonometry", topics: ["law of sines", "law of cosines", "area", "applications"] },
                        { num: 12, name: "Trigonometric Functions", topics: ["graphs", "inverse functions", "equations", "periodicity"] }
                    ]
                },
                xii: {
                    path: "mathsxiibooks",
                    chapters: [
                        { num: 1, name: "Relations and Functions", topics: ["relations", "functions", "composition", "inverse"] },
                        { num: 2, name: "Inverse Trigonometric Functions", topics: ["inverse functions", "domain", "range", "graphs"] },
                        { num: 3, name: "Matrices", topics: ["matrix operations", "types", "properties", "applications"] },
                        { num: 4, name: "Determinants", topics: ["properties", "expansion", "cramer rule", "applications"] },
                        { num: 5, name: "Continuity and Differentiability", topics: ["limits", "continuity", "derivatives", "chain rule"] },
                        { num: 6, name: "Application of Derivatives", topics: ["rate of change", "maxima minima", "tangents", "normals"] },
                        { num: 7, name: "Integrals", topics: ["antiderivatives", "integration techniques", "substitution", "parts"] },
                        { num: 8, name: "Application of Integrals", topics: ["area under curve", "volume", "length", "applications"] },
                        { num: 9, name: "Differential Equations", topics: ["formation", "solution", "homogeneous", "linear"] },
                        { num: 10, name: "Vector Algebra", topics: ["vector operations", "scalar triple product", "vector triple product", "applications"] },
                        { num: 11, name: "Three Dimensional Geometry", topics: ["direction cosines", "plane", "line", "distance"] },
                        { num: 12, name: "Linear Programming", topics: ["objective function", "constraints", "feasible region", "optimization"] },
                        { num: 13, name: "Probability", topics: ["conditional probability", "bayes theorem", "random variables", "distributions"] }
                    ]
                }
            },
            biology: {
                xi: {
                    path: "biologybooks",
                    chapters: [
                        { num: 1, name: "The Living World", topics: ["characteristics", "classification", "taxonomy", "nomenclature"] },
                        { num: 2, name: "Biological Classification", topics: ["five kingdom", "monera", "protista", "fungi"] },
                        { num: 3, name: "Plant Kingdom", topics: ["algae", "bryophytes", "pteridophytes", "gymnosperms"] },
                        { num: 4, name: "Animal Kingdom", topics: ["porifera", "cnidaria", "platyhelminthes", "annelida"] },
                        { num: 5, name: "Morphology of Flowering Plants", topics: ["root", "stem", "leaf", "flower"] },
                        { num: 6, name: "Anatomy of Flowering Plants", topics: ["tissues", "meristem", "permanent tissues", "secondary growth"] },
                        { num: 7, name: "Structural Organisation in Animals", topics: ["epithelial", "connective", "muscular", "nervous tissues"] },
                        { num: 8, name: "Cell: The Unit of Life", topics: ["cell theory", "prokaryotic", "eukaryotic", "organelles"] },
                        { num: 9, name: "Biomolecules", topics: ["carbohydrates", "proteins", "lipids", "nucleic acids"] },
                        { num: 10, name: "Cell Cycle and Cell Division", topics: ["mitosis", "meiosis", "cell cycle", "regulation"] },
                        { num: 11, name: "Transport in Plants", topics: ["transpiration", "translocation", "root pressure", "cohesion tension"] },
                        { num: 12, name: "Mineral Nutrition", topics: ["essential elements", "deficiency symptoms", "nitrogen fixation", "metabolism"] },
                        { num: 13, name: "Photosynthesis in Higher Plants", topics: ["light reaction", "dark reaction", "calvin cycle", "factors"] },
                        { num: 14, name: "Respiration in Plants", topics: ["glycolysis", "krebs cycle", "electron transport", "fermentation"] }
                    ]
                },
                xii: {
                    path: "biologyxiibooks",
                    chapters: [
                        { num: 15, name: "Reproduction in Organisms", topics: ["asexual reproduction", "sexual reproduction", "life cycles", "patterns"] },
                        { num: 16, name: "Sexual Reproduction in Flowering Plants", topics: ["flower structure", "pollination", "fertilization", "embryo development"] },
                        { num: 17, name: "Human Reproduction", topics: ["reproductive system", "gametogenesis", "fertilization", "pregnancy"] },
                        { num: 18, name: "Reproductive Health", topics: ["contraception", "infertility", "sexually transmitted diseases", "population control"] },
                        { num: 19, name: "Principles of Inheritance and Variation", topics: ["mendel laws", "inheritance patterns", "linkage", "recombination"] },
                        { num: 20, name: "Molecular Basis of Inheritance", topics: ["dna structure", "replication", "transcription", "translation"] },
                        { num: 21, name: "Evolution", topics: ["origin of life", "evolutionary theories", "evidence", "human evolution"] },
                        { num: 22, name: "Human Health and Disease", topics: ["immunity", "pathogens", "diseases", "treatment"] },
                        { num: 23, name: "Microbes in Human Welfare", topics: ["microorganisms", "industrial applications", "medicine", "environment"] },
                        { num: 24, name: "Biotechnology - Principles and Processes", topics: ["genetic engineering", "tools", "techniques", "applications"] },
                        { num: 25, name: "Biotechnology and its Applications", topics: ["agriculture", "medicine", "industry", "ethics"] },
                        { num: 26, name: "Organisms and Populations", topics: ["ecology", "population dynamics", "community", "ecosystem"] },
                        { num: 27, name: "Ecosystem", topics: ["energy flow", "nutrient cycling", "succession", "conservation"] }
                    ]
                }
            }
        };
    }

    // Create the floating chat widget
    createChatWidget() {
        const widgetHTML = `
            <div id="chatbot-widget" class="chatbot-widget">
                <div id="chatbot-toggle" class="chatbot-toggle">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                </div>
                <div id="chatbot-container" class="chatbot-container hidden">
                <div class="chatbot-header">
                    <button id="chatbot-back" class="chatbot-back">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M19 12H5M12 19l-7-7 7-7"/>
                        </svg>
                    </button>
                    <h3>Our Books Assistant</h3>
                    <button id="chatbot-close" class="chatbot-close">×</button>
                </div>
                    <div id="chatbot-messages" class="chatbot-messages"></div>
                    <div class="chatbot-input-container">
                        <input type="text" id="chatbot-input" placeholder="Ask me anything about your subjects..." />
                        <button id="chatbot-send">Send</button>
                    </div>
                    <div class="chatbot-status">
                        <span id="chatbot-status-text">Ready to help!</span>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    // Setup event listeners
    setupEventListeners() {
        const toggle = document.getElementById('chatbot-toggle');
        const close = document.getElementById('chatbot-close');
        const back = document.getElementById('chatbot-back');
        const send = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');

        toggle.addEventListener('click', () => this.toggleChat());
        close.addEventListener('click', () => this.closeChat());
        back.addEventListener('click', () => this.closeChat());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Auto-focus input when chat opens
        toggle.addEventListener('click', () => {
            setTimeout(() => input.focus(), 300);
        });
    }

    // Toggle chat visibility
    toggleChat() {
        const container = document.getElementById('chatbot-container');
        const toggle = document.getElementById('chatbot-toggle');
        
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            container.classList.remove('hidden');
            toggle.classList.add('active');
            this.addWelcomeMessage();
        } else {
            container.classList.add('hidden');
            toggle.classList.remove('active');
        }
    }

    // Close chat
    closeChat() {
        this.isOpen = false;
        document.getElementById('chatbot-container').classList.add('hidden');
        document.getElementById('chatbot-toggle').classList.remove('active');
    }

    // Add welcome message
    addWelcomeMessage() {
        const messagesContainer = document.getElementById('chatbot-messages');
        if (messagesContainer.children.length === 0) {
            this.addMessage('bot', `Hello! I'm your study assistant. I can help you with questions about:

📚 **Chemistry** - Stoichiometry, Atomic Structure, Chemical Bonding, and more
🔬 **Physics** - Kinematics, Dynamics, Thermodynamics, and more  
📐 **Mathematics** - Complex Numbers, Calculus, Probability, and more
🧬 **Biology** - Cell Biology, Genetics, Evolution, and more

I can also solve numerical problems and explain concepts with LaTeX equations. What would you like to know?`);
        }
    }

    // Add message to chat
    addMessage(sender, content, isTyping = false) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}-message ${isTyping ? 'typing' : ''}`;
        
        if (isTyping) {
            messageDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        } else {
            messageDiv.innerHTML = `<div class="message-content">${this.formatMessage(content)}</div>`;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Render LaTeX if present
        if (!isTyping && (content.includes('$') || content.includes('\\(') || content.includes('\\['))) {
            // Small delay to ensure DOM is ready
            setTimeout(() => {
                this.renderLatex(messageDiv);
            }, 100);
        }
    }

    // Format message content
    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    // Render LaTeX in message
    renderLatex(element) {
        if (this.config.debug) {
            console.log('Rendering LaTeX for element:', element);
        }
        
        if (window.MathJax) {
            // Wait for MathJax to be ready
            MathJax.startup.promise.then(() => {
                MathJax.typesetPromise([element]).then(() => {
                    if (this.config.debug) {
                        console.log('LaTeX rendered successfully');
                    }
                }).catch((err) => {
                    console.error('MathJax rendering error:', err);
                });
            });
        } else {
            // If MathJax isn't loaded yet, wait for it
            const checkMathJax = setInterval(() => {
                if (window.MathJax) {
                    clearInterval(checkMathJax);
                    MathJax.startup.promise.then(() => {
                        MathJax.typesetPromise([element]).then(() => {
                            if (this.config.debug) {
                                console.log('LaTeX rendered successfully (delayed)');
                            }
                        }).catch((err) => {
                            console.error('MathJax rendering error:', err);
                        });
                    });
                }
            }, 100);
        }
    }

    // Send message
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        
        // Add typing indicator
        this.addMessage('bot', '', true);
        
        try {
            // Analyze question and get context
            const context = this.analyzeQuestion(message);
            
            // Generate response using Gemini API
            const response = await this.generateResponse(message, context);
            
            // Remove typing indicator and add response
            const messagesContainer = document.getElementById('chatbot-messages');
            messagesContainer.removeChild(messagesContainer.lastChild);
            
            this.addMessage('bot', response);
            
            // Save to conversation history
            this.conversationHistory.push({
                user: message,
                bot: response,
                context: context,
                timestamp: new Date().toISOString()
            });
            
            this.saveConversationHistory();
            
        } catch (error) {
            console.error('Error generating response:', error);
            
            // Remove typing indicator
            const messagesContainer = document.getElementById('chatbot-messages');
            messagesContainer.removeChild(messagesContainer.lastChild);
            
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again or check your internet connection.');
        }
    }

    // Analyze question to determine relevant context
    analyzeQuestion(question) {
        const lowerQuestion = question.toLowerCase();
        const context = {
            subject: null,
            class: null,
            chapter: null,
            topics: []
        };

        // Check for subject keywords
        for (const [subject, classes] of Object.entries(this.contentMap)) {
            if (lowerQuestion.includes(subject)) {
                context.subject = subject;
                break;
            }
        }

        // Check for class indicators
        if (lowerQuestion.includes('class xi') || lowerQuestion.includes('class 11')) {
            context.class = 'xi';
        } else if (lowerQuestion.includes('class xii') || lowerQuestion.includes('class 12')) {
            context.class = 'xii';
        }

        // Check for chapter-specific topics
        if (context.subject && context.class) {
            const chapters = this.contentMap[context.subject][context.class].chapters;
            for (const chapter of chapters) {
                for (const topic of chapter.topics) {
                    if (lowerQuestion.includes(topic)) {
                        context.chapter = chapter;
                        context.topics.push(topic);
                    }
                }
            }
        }

        return context;
    }

    // Generate response using Gemini API
    async generateResponse(question, context) {
        const apiKey = this.getNextApiKey();
        if (!apiKey) {
            throw new Error('No available API keys');
        }

        const model = this.config.model || "gemini-2.5-flash-preview-05-20";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

        // Build context-aware prompt
        let prompt = `You are an intelligent study assistant for "Our Books" educational platform. `;
        
        if (context.subject && context.chapter) {
            prompt += `The user is asking about ${context.subject} Chapter ${context.chapter.num}: ${context.chapter.name}. `;
            prompt += `Focus your answer on the topics: ${context.chapter.topics.join(', ')}. `;
            prompt += `Provide detailed explanations with examples and use LaTeX for mathematical expressions. `;
        } else if (context.subject) {
            prompt += `The user is asking about ${context.subject}. Provide comprehensive information about this subject. `;
        } else {
            prompt += `The user is asking a general question. Provide helpful information. `;
        }

        prompt += `IMPORTANT: Use LaTeX for all mathematical expressions. Use $ for inline math and $$ for display math. For example: $E = mc^2$ or $$\\frac{a}{b} = \\frac{c}{d}$$`;
        prompt += `Question: ${question}`;

        const payload = {
            contents: [{
                parts: [{ text: prompt }]
            }],
            generationConfig: {
                temperature: 0.7,
                topK: 40,
                topP: 0.95,
                maxOutputTokens: 1024,
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
        return result?.candidates?.[0]?.content?.parts?.[0]?.text || "I couldn't generate a response. Please try again.";
    }

    // Get next available API key
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

    // Save conversation history to localStorage
    saveConversationHistory() {
        try {
            localStorage.setItem('ourbooks_chat_history', JSON.stringify(this.conversationHistory));
        } catch (error) {
            console.error('Error saving conversation history:', error);
        }
    }

    // Load conversation history from localStorage
    loadConversationHistory() {
        try {
            const saved = localStorage.getItem('ourbooks_chat_history');
            if (saved) {
                this.conversationHistory = JSON.parse(saved);
            }
        } catch (error) {
            console.error('Error loading conversation history:', error);
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ourBooksChatbot = new OurBooksChatbot();
});