# Confidence Coach AI

**Confidence Coach AI** is a tool designed to help users refine their communication by analyzing text inputs for confidence levels and providing actionable suggestions for improvement. Whether you're preparing for an interview, crafting an email, or building your public speaking skills, Confidence Coach AI can help you identify and address low-confidence cues.

## Key Features

- **Confidence Analysis**: Analyzes user-provided text and identifies areas where confidence might appear low.  
- **Actionable Feedback**: Responds with tailored suggestions to improve communication.  
- **User-Friendly Interface**: Simple HTML form-based frontend for seamless interaction.  
- **API Documentation**: Endpoints are testable via FastAPI's `/docs` endpoint (requires OpenAI API keys).  

## Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Frontend**: Basic HTML form for user interaction  
- **AI Integration**: [OpenAI API](https://platform.openai.com/)  
- **Deployment**: Hosted on [Render](https://render.com/)  
- **Containerization**: Docker support for easy setup and deployment  

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo/confidence-coach-ai.git
   cd confidence-coach-ai

2. **Set Up API Keys**  
   - Obtain an API key from OpenAI.  
   - Add your key to the environment variables or a `.env` file as `OPENAI_API_KEY`.

3. **Run Locally Using Docker**  
   - Build the Docker image:  
     ```bash
     docker build -t confidence-coach-ai .
     ```  
   - Run the container:  
     ```bash
     docker run -e OPENAI_API_KEY=your_api_key -p 8000:8000 confidence-coach-ai
     ```

4. **Access the App**  
   - Open your browser and go to `http://localhost:8000`.  
   - Test the API via the `/docs` endpoint.  

## Usage

1. Navigate to the app's user interface.  
2. Input text into the provided form.  
3. Receive confidence analysis and actionable suggestions.