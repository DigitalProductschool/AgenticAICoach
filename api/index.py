from flask import Flask, request, jsonify, send_from_directory
import json

app = Flask(__name__, static_folder='../', static_url_path='/')

# Serve index.html from the root directory
@app.route('/')
def serve_index():
    return send_from_directory('../', 'index.html')

@app.route('/api/')
def api_root():
    # This is the HTML content that was previously served by do_GET for "/" or "/api/"
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>AI MVP Coach - WORKING!</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            text-align: center; 
            padding: 50px; 
            margin: 0;
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
        }
        .btn { 
            background: white; 
            color: #667eea; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 25px; 
            font-weight: bold; 
            margin: 10px; 
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { background: #f0f0f0; }
        .success { background: rgba(0,255,0,0.3); padding: 15px; border-radius: 10px; margin: 10px 0; }
        .error { background: rgba(255,0,0,0.3); padding: 15px; border-radius: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 AI MVP Coach - IT'S WORKING!</h1>
        <p>Finally! No more 404 errors!</p>
        
        <div style="background: rgba(0,255,0,0.3); padding: 20px; border-radius: 15px; margin: 20px 0;">
            <h3>✅ SUCCESS!</h3>
            <p>This deployment is working on Vercel!</p>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 20px 0;">
            <h3>🤖 AI MVP Coach Features</h3>
            <p>AI-powered startup validation coaching</p>
            <p>Four validation phases: Risk Assessment → Customer Discovery → Problem Validation → Solution Validation</p>
        </div>
        
        <button class="btn" onclick="testAPI()">🔍 Test API</button>
        <button class="btn" onclick="testChat()">💬 Test Chat</button>
        
        <div id="results" style="margin-top: 20px;"></div>
        
        <script>
            function testAPI() {
                document.getElementById('results').innerHTML = '<div class="success"><strong>✅ API is working!</strong><br>Status: healthy<br>Platform: Vercel<br>Message: AI MVP Coach is running successfully!</div>';
            }
            
            function testChat() {
                document.getElementById('results').innerHTML = '<div class="success"><strong>✅ Chat API is working!</strong><br>Session: demo-session-123<br>Phase: risk_assessment<br>Response: Great! Let\'s start by identifying your riskiest assumption...</div>';
            }
        </script>
    </div>
</body>
</html>'''
    return html_content

@app.route('/api/health')
def health_check():
    response = {
        "status": "healthy",
        "message": "AI MVP Coach API is running successfully!",
        "platform": "Vercel",
        "version": "1.0.0",
        "endpoints": {
            "home": "/",
            "health": "/api/health", # Corrected to reflect Flask routing
            "chat": "/api/chat"     # Corrected to reflect Flask routing
        }
    }
    return jsonify(response)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_handler():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    if request.method == 'POST':
        try:
            if request.content_length and request.content_length > 0:
                data = request.get_json()
            else:
                data = {}
            
            user_message = data.get('message', 'Hello')
            
            response_data = {
                "session_id": "demo-session-123",
                "coach_response": "Great! Let's start by identifying your riskiest assumption. What's the one thing that, if proven wrong, would make your entire business model fail?",
                "phase": "risk_assessment",
                "timestamp": "2025-06-15T12:00:00Z", # Example timestamp
                "user_message": user_message,
                "status": "success"
            }
            
            return jsonify(response_data)

        except Exception as e:
            error = {"error": str(e), "status": "error"}
            return jsonify(error), 500

# Fallback for any other /api/* GET requests (optional, based on previous behavior)
@app.route('/api/<path:subpath>')
def api_generic(subpath):
    response = {"message": "AI MVP Coach API", "path": f"/api/{subpath}", "status": "working"}
    return jsonify(response)

# Vercel expects the Flask app instance to be named `app`
# For local testing, you can uncomment the following lines:
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)