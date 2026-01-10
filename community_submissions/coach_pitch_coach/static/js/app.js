// App State
const state = {
  sessionId: null,
  currentMode: 'coach',
  currentStage: 'one_liner',
  audience: 'VC',
  fundingStage: 'pre-seed',
  industry: '',
  isLoading: false,
  stages: ['one_liner', 'problem', 'solution', 'uvp', 'target_customer', 'market', 'business_model', 'traction', 'moat', 'ask']
};

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const sendText = document.getElementById('send-text');
const loadingSpinner = document.getElementById('loading-spinner');
const modeButtons = document.querySelectorAll('.mode-btn');
const audienceSelect = document.getElementById('audience');
const fundingStageSelect = document.getElementById('funding-stage');
const industryInput = document.getElementById('industry');
const industryGroup = document.getElementById('industry-group');
const newSessionBtn = document.getElementById('new-session-btn');
const exportBtn = document.getElementById('export-btn');
const sessionIdDisplay = document.getElementById('session-id-display');
const statusDisplay = document.getElementById('status-display');
const progressContainer = document.getElementById('progress-container');
const progressText = document.getElementById('progress-text');
const progressPercentage = document.getElementById('progress-percentage');
const progressFill = document.getElementById('progress-fill');
const scoreDisplay = document.getElementById('score-display');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadSessionFromStorage();
  attachEventListeners();
  updateUIForMode();
});

// Event Listeners
function attachEventListeners() {
  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  modeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.dataset.mode;
      setMode(mode);
    });
  });

  audienceSelect.addEventListener('change', (e) => {
    state.audience = e.target.value;
  });

  fundingStageSelect.addEventListener('change', (e) => {
    state.fundingStage = e.target.value;
  });

  industryInput.addEventListener('input', (e) => {
    state.industry = e.target.value;
  });

  newSessionBtn.addEventListener('click', startNewSession);
  exportBtn.addEventListener('click', exportPitch);
}

// Mode Management
function setMode(mode) {
  state.currentMode = mode;
  
  modeButtons.forEach(btn => {
    if (btn.dataset.mode === mode) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  updateUIForMode();
  clearWelcomeMessage();
}

function updateUIForMode() {
  // Show/hide progress bar for coach mode
  if (state.currentMode === 'coach') {
    progressContainer.style.display = 'block';
    industryGroup.style.display = 'none';
  } else if (state.currentMode === 'qa') {
    progressContainer.style.display = 'none';
    industryGroup.style.display = 'flex';
  } else {
    progressContainer.style.display = 'none';
    industryGroup.style.display = 'none';
  }

  updateProgressBar();
}

// Message Handling
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message || state.isLoading) return;

  // Add user message to chat
  addMessageToChat('user', message);
  userInput.value = '';
  clearWelcomeMessage();

  // Set loading state
  setLoading(true);

  try {
    const response = await fetch('/coach', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: state.sessionId,
        mode: state.currentMode,
        user_message: message,
        audience: state.audience,
        funding_stage: state.fundingStage,
        industry: state.industry || undefined
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Update state
    state.sessionId = data.session_id;
    if (data.stage) {
      state.currentStage = data.stage;
    }

    // Add assistant response
    addMessageToChat('assistant', data.coach_response, data.next_question);

    // Update scores
    if (data.scores) {
      updateScores(data.scores);
    }

    // Update progress
    updateProgressBar();

    // Save session
    saveSessionToStorage();
    updateSessionDisplay();

  } catch (error) {
    console.error('Error:', error);
    addMessageToChat('assistant', '❌ Sorry, there was an error processing your request. Please try again.');
  } finally {
    setLoading(false);
  }
}

function addMessageToChat(role, content, nextQuestion = null) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = role === 'user' ? '👤' : '🤖';

  const messageContent = document.createElement('div');
  messageContent.className = 'message-content';
  
  // Render markdown for assistant messages
  if (role === 'assistant') {
    try {
      if (typeof marked !== 'undefined' && marked.parse) {
        messageContent.innerHTML = marked.parse(content);
      } else {
        console.warn('Marked library not loaded, falling back to plain text');
        messageContent.textContent = content;
      }
    } catch (error) {
      console.error('Markdown parsing error:', error);
      messageContent.textContent = content;
    }
  } else {
    messageContent.textContent = content;
  }

  if (nextQuestion) {
    const nextQuestionDiv = document.createElement('div');
    nextQuestionDiv.className = 'next-question';
    nextQuestionDiv.textContent = `Next: ${nextQuestion}`;
    messageContent.appendChild(nextQuestionDiv);
  }

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(messageContent);

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function clearWelcomeMessage() {
  const welcomeMsg = chatContainer.querySelector('.welcome-message');
  if (welcomeMsg) {
    welcomeMsg.remove();
  }
}

// UI State Management
function setLoading(loading) {
  state.isLoading = loading;
  sendBtn.disabled = loading;
  userInput.disabled = loading;

  if (loading) {
    sendText.style.display = 'none';
    loadingSpinner.style.display = 'inline';
    statusDisplay.textContent = 'Thinking...';
  } else {
    sendText.style.display = 'inline';
    loadingSpinner.style.display = 'none';
    statusDisplay.textContent = 'Ready';
  }
}

// Progress Bar
function updateProgressBar() {
  if (state.currentMode !== 'coach') return;

  const currentIndex = state.stages.indexOf(state.currentStage);
  const percentage = ((currentIndex + 1) / state.stages.length) * 100;

  progressFill.style.width = `${percentage}%`;
  progressPercentage.textContent = `${Math.round(percentage)}%`;
  progressText.textContent = `Stage: ${formatStageName(state.currentStage)}`;

  // Update stage indicators
  document.querySelectorAll('.stage').forEach((stageEl, index) => {
    stageEl.classList.remove('completed', 'current');
    if (index < currentIndex) {
      stageEl.classList.add('completed');
    } else if (index === currentIndex) {
      stageEl.classList.add('current');
    }
  });
}

function formatStageName(stage) {
  return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

// Scores
function updateScores(scores) {
  scoreDisplay.style.display = 'grid';
  
  updateScore('clarity', scores.clarity);
  updateScore('persuasion', scores.persuasion);
  updateScore('confidence', scores.confidence);
}

function updateScore(type, value) {
  const bar = document.getElementById(`${type}-bar`);
  const scoreEl = document.getElementById(`${type}-score`);
  
  bar.style.width = `${value * 10}%`;
  scoreEl.textContent = value;
}

// Session Management
function startNewSession() {
  if (confirm('Start a new session? Your current session will be saved.')) {
    state.sessionId = null;
    state.currentStage = 'one_liner';
    chatContainer.innerHTML = '<div class="welcome-message"><h2>Welcome! 👋</h2><p>New session started. Ready to build your pitch?</p></div>';
    scoreDisplay.style.display = 'none';
    saveSessionToStorage();
    updateSessionDisplay();
    updateProgressBar();
  }
}

function saveSessionToStorage() {
  localStorage.setItem('pitchCoachSession', JSON.stringify({
    sessionId: state.sessionId,
    currentMode: state.currentMode,
    currentStage: state.currentStage,
    audience: state.audience,
    fundingStage: state.fundingStage,
    industry: state.industry
  }));
}

function loadSessionFromStorage() {
  const saved = localStorage.getItem('pitchCoachSession');
  if (saved) {
    try {
      const data = JSON.parse(saved);
      state.sessionId = data.sessionId;
      state.currentMode = data.currentMode || 'coach';
      state.currentStage = data.currentStage || 'one_liner';
      state.audience = data.audience || 'VC';
      state.fundingStage = data.fundingStage || 'pre-seed';
      state.industry = data.industry || '';

      audienceSelect.value = state.audience;
      fundingStageSelect.value = state.fundingStage;
      industryInput.value = state.industry;

      setMode(state.currentMode);
      updateSessionDisplay();
    } catch (e) {
      console.error('Failed to load session:', e);
    }
  }
}

function updateSessionDisplay() {
  if (state.sessionId) {
    sessionIdDisplay.textContent = `Session: ${state.sessionId.slice(0, 8)}...`;
  } else {
    sessionIdDisplay.textContent = 'Session: New';
  }
}

// Export Functionality
async function exportPitch() {
  if (!state.sessionId) {
    alert('No active session to export!');
    return;
  }

  try {
    const response = await fetch(`/sessions/${state.sessionId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch session data');
    }

    const sessionData = await response.json();
    
    // Create markdown export
    let markdown = '# My Startup Pitch\n\n';
    markdown += `**Generated:** ${new Date().toLocaleDateString()}\n\n`;
    markdown += `**Audience:** ${state.audience}\n`;
    markdown += `**Funding Stage:** ${state.fundingStage}\n\n`;
    markdown += '---\n\n';

    if (sessionData.context) {
      state.stages.forEach(stage => {
        if (sessionData.context[stage]) {
          markdown += `## ${formatStageName(stage)}\n\n`;
          markdown += `${sessionData.context[stage]}\n\n`;
        }
      });
    }

    // Download file
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pitch-${state.sessionId.slice(0, 8)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

  } catch (error) {
    console.error('Export error:', error);
    alert('Failed to export pitch. Make sure you have completed at least one stage.');
  }
}
