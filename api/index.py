from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import json

app = FastAPI(
    title="AI MVP Coach",
    description="AI-powered MVP validation coaching",
    version="1.0.0"
)

@app.get("/")
async def home():
    """Landing page"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI MVP Coach</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                text-align: center; 
                padding: 0; 
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                min-height: 100vh; 
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 40px 20px;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            .btn { 
                background: rgba(255,255,255,0.9); 
                color: #667eea; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 25px; 
                font-weight: bold; 
                display: inline-block; 
                margin: 10px; 
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            .btn:hover { 
                transform: translateY(-3px); 
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                background: white;
            }
            .feature { 
                background: rgba(255,255,255,0.1); 
                padding: 25px; 
                margin: 20px 0; 
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            h1 { 
                font-size: 3.5em; 
                margin-bottom: 0.3em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle { 
                font-size: 1.4em; 
                margin-bottom: 2em; 
                opacity: 0.9;
            }
            .success { background: rgba(0,255,0,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; }
            .error { background: rgba(255,0,0,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI MVP Coach</h1>
            <p class="subtitle">AI-powered startup validation coaching platform</p>
            
            <div class="feature">
                <h3>🎯 Validate Your Startup Ideas</h3>
                <p>Get structured guidance through lean startup methodology with AI-powered coaching sessions</p>
            </div>
            
            <div class="feature">
                <h3>📊 Four Validation Phases</h3>
                <p><strong>Risk Assessment</strong> → <strong>Customer Discovery</strong> → <strong>Problem Validation</strong> → <strong>Solution Validation</strong></p>
            </div>
            
            <div class="feature">
                <h3>⚡ Production-Ready API</h3>
                <p>FastAPI backend with working endpoints</p>
            </div>
            
            <div style="margin: 30px 0;">
                <button class="btn" onclick="testHealth()">🔍 Test Health Check</button>
                <button class="btn" onclick="testChat()">💬 Test Chat API</button>
                <a href="/docs" class="btn">📚 API Documentation</a>
            </div>

            <div id="test-results" style="margin-top: 20px;"></div>
            
            <div style="margin-top: 40px; opacity: 0.8;">
                <p>🏆 Built for the Agentic AI Challenge</p>
                <p>✅ WORKING DEPLOYMENT!</p>
            </div>
        </div>

        <script>
            async function testHealth() {
                const resultsDiv = document.getElementById('test-results');
                resultsDiv.innerHTML = '<p>Testing health endpoint...</p>';
                
                try {
                    const response = await fetch('/health');
                    const data = await response.json();
                    resultsDiv.innerHTML = `
                        <div class="success">
                            <strong>✅ Health Check Success!</strong><br>
                            Status: ${data.status}<br>
                            Message: ${data.message}
                        </div>
                    `;
                } catch (error) {
                    resultsDiv.innerHTML = `
                        <div class="error">
                            <strong>❌ Health Check Failed:</strong><br>
                            ${error.message}
                        </div>
                    `;
                }
            }

            async function testChat() {
                const resultsDiv = document.getElementById('test-results');
                resultsDiv.innerHTML = '<p>Testing chat endpoint...</p>';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: 'I have a startup idea about AI coaching' })
                    });
                    const data = await response.json();
                    resultsDiv.innerHTML = `
                        <div class="success">
                            <strong>✅ Chat API Success!</strong><br>
                            <strong>Session:</strong> ${data.session_id}<br>
                            <strong>Phase:</strong> ${data.phase}<br>
                            <strong>Response:</strong> ${data.coach_response.substring(0, 100)}...
                        </div>
                    `;
                } catch (error) {
                    resultsDiv.innerHTML = `
                        <div class="error">
                            <strong>❌ Chat API Failed:</strong><br>
                            ${error.message}
                        </div>
                    `;
                }
            }
        </script>
    </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI MVP Coach API is running",
        "platform": "Vercel",
        "version": "1.0.0",
        "timestamp": "2025-06-15T12:00:00Z"
    }

@app.post("/chat")
async def chat_endpoint(request: dict):
    """Chat endpoint for AI coaching"""
    user_message = request.get("message", "").lower()
    
    # Simple AI coaching logic
    if "idea" in user_message or "startup" in user_message:
        response = "Great! Let's start by identifying your riskiest assumption. What's the one thing that, if proven wrong, would make your entire business model fail?"
        phase = "risk_assessment"
    elif "customer" in user_message:
        response = "Excellent! Understanding your customers is crucial. Can you describe your ideal customer in detail?"
        phase = "customer_discovery"
    elif "problem" in user_message:
        response = "Good! Now let's validate the problem. How painful is this problem for your customers?"
        phase = "problem_validation"
    elif "solution" in user_message:
        response = "Perfect! Let's validate your solution. What's the simplest version that could test your core hypothesis?"
        phase = "solution_validation"
    else:
        response = f"I understand you said: '{request.get('message', '')}'. Let's focus on validating your MVP. What's the biggest assumption in your business model?"
        phase = "risk_assessment"
    
    session_id = f"demo-session-{hash(request.get('message', '')) % 10000}"
    
    return {
        "session_id": session_id,
        "coach_response": response,
        "phase": phase,
        "timestamp": "2025-06-15T12:00:00Z",
        "suggestions": [
            "What's your biggest assumption?",
            "Who is your target customer?",
            "What problem are you solving?",
            "How will you test this?"
        ]
    }

@app.get("/stats")
async def get_stats():
    """Demo stats endpoint"""
    return {
        "total_sessions": 42,
        "active_sessions": 3,
        "total_messages": 128,
        "avg_messages_per_session": 3.0,
        "platform": "Vercel"
    }

# For Vercel compatibility
handler = app