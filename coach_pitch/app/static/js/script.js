// Global variables
let sessionId = null;
let completePitch = null;

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const pitchPreviewContainer = document.getElementById('pitch-preview-container');
const pitchContent = document.getElementById('pitch-content');
const qaButton = document.getElementById('qa-button');
const feedbackButton = document.getElementById('feedback-button');
const exportButton = document.getElementById('export-button');
const actionResults = document.getElementById('action-results');
const actionTitle = document.getElementById('action-title');
const actionContent = document.getElementById('action-content');

// Initialize the coaching session
async function initializeSession() {
    try {
        const response = await fetch('/start_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 'web_user'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        sessionId = data.session_id;
        
        // Add welcome message to chat
        addMessage('coach', data.welcome_message);
    } catch (error) {
        console.error('Error initializing session:', error);
        addMessage('coach', 'Sorry, there was an error connecting to the AI coach. Please refresh the page and try again.');
    }
}

// Send a message to the coach
async function sendMessage(message) {
    if (!sessionId) {
        console.error('No active session');
        return;
    }
    
    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message,
                user_id: 'web_user'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add coach's response to chat
        addMessage('coach', data.response);
        
        // Check if pitch is complete
        if (data.is_pitch_complete && data.complete_pitch) {
            completePitch = data.complete_pitch;
            pitchContent.textContent = completePitch;
            pitchPreviewContainer.style.display = 'block';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('coach', 'Sorry, there was an error communicating with the AI coach.');
    }
}

// Perform a session action (Q&A or feedback)
async function performAction(action) {
    if (!sessionId) {
        console.error('No active session');
        return;
    }
    
    try {
        const response = await fetch('/session_action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                action: action,
                user_id: 'web_user'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the results
        actionTitle.textContent = action === 'qa' ? 'Investor Q&A Simulation' : 'Pitch Clarity Feedback';
        actionContent.textContent = data.result;
        actionResults.style.display = 'block';
        
        // Scroll to the results
        actionResults.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error(`Error performing ${action} action:`, error);
        addMessage('coach', `Sorry, there was an error generating the ${action === 'qa' ? 'investor questions' : 'pitch feedback'}.`);
    }
}

// Add a message to the chat
function addMessage(sender, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const senderDiv = document.createElement('div');
    senderDiv.className = 'message-sender';
    senderDiv.textContent = sender === 'user' ? 'You' : 'Coach';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(senderDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Auto scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Export pitch to a text file
function exportPitch() {
    if (!completePitch) return;
    
    const blob = new Blob([completePitch], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'startup_pitch.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Event listeners
document.addEventListener('DOMContentLoaded', initializeSession);

sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        addMessage('user', message);
        sendMessage(message);
        userInput.value = '';
    }
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
});

qaButton.addEventListener('click', () => performAction('qa'));
feedbackButton.addEventListener('click', () => performAction('feedback'));
exportButton.addEventListener('click', exportPitch);