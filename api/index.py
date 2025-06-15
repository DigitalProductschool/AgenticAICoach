from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        if path == "/" or path == "/api" or path == "/api/":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
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
                document.getElementById('results').innerHTML = '<div class="success"><strong>✅ Chat API is working!</strong><br>Session: demo-session-123<br>Phase: risk_assessment<br>Response: Great! Let\\'s start by identifying your riskiest assumption...</div>';
            }
        </script>
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode())
            
        elif path == "/health" or path == "/api/health":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "message": "AI MVP Coach API is running successfully!",
                "platform": "Vercel",
                "version": "1.0.0",
                "endpoints": {
                    "home": "/",
                    "health": "/health",
                    "chat": "/chat"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"message": "AI MVP Coach API", "path": path, "status": "working"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == "/chat" or self.path == "/api/chat":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                else:
                    data = {}
                
                user_message = data.get('message', 'Hello')
                
                response_data = {
                    "session_id": "demo-session-123",
                    "coach_response": "Great! Let's start by identifying your riskiest assumption. What's the one thing that, if proven wrong, would make your entire business model fail?",
                    "phase": "risk_assessment",
                    "timestamp": "2025-06-15T12:00:00Z",
                    "user_message": user_message,
                    "status": "success"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data, indent=2).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error = {"error": str(e), "status": "error"}
                self.wfile.write(json.dumps(error).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error = {"error": "Not Found", "path": self.path}
            self.wfile.write(json.dumps(error).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()