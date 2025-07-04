# AI Pitch Coach

An AI-powered coach that helps founders structure, refine, and practice their startup pitches.



## Overview

AI Pitch Coach is a comprehensive tool designed to assist startup founders in developing compelling pitches. Using advanced AI agents, the application provides step-by-step guidance through a conversational interface, helping users articulate their value proposition, refine their messaging, and prepare for investor questions.

### Features

- **Guided Pitch Development**: Interactive, conversational coaching to build your pitch from scratch
- **Pitch Analysis**: Detailed feedback on clarity, persuasiveness, and structure
- **Investor Q&A Simulation**: Practice answering tough investor questions specific to your industry and funding stage
- **Iterative Refinement**: Track improvements across multiple versions of your pitch
- **Multiple Interfaces**: Web UI, command-line interface, and API access options

## Installation

### Prerequisites

- Python 3.11
- Git
- An OpenAI API key (required for all AI functionality)

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ai-pitch-coach.git
cd ai-pitch-coach
```

2. **Create and activate a virtual environment**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory with the following contents:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Running the Application

AI Pitch Coach offers three ways to interact with the system:

### Option 1: Web Interface

1. **Start the FastAPI server**

```bash
python run_api.py
```

2. **Access the web interface**

Open your browser and navigate to:
```
http://localhost:8000/ui
```

This provides a chat-like interface where you can interact with the AI coach step-by-step, see your complete pitch, and get additional Q&A simulation and feedback.

### Option 2: Command-Line Interface

#### Conversational CLI (Guided Coaching)

For a guided coaching session through the command line:

```bash
python conversational_cli.py
```

This will start an interactive session where the AI coach will guide you step by step through creating your pitch.

#### Standard CLI (Direct Analysis)

For working with specific pitch elements through a menu-driven interface:

```bash
python coach_cli.py
```

This launches a menu with options to:
- Create a new pitch
- Refine your current pitch
- Simulate investor Q&A
- View pitch history
- List all your saved pitches

You can also use direct commands:

```bash
# Analyze a pitch
python coach_cli.py --analyze "Your pitch text here"

# Simulate Q&A for a pitch
python coach_cli.py --qa "Your pitch text here"

# View history for a specific pitch ID
python coach_cli.py --history <pitch_id>

# List all your pitches
python coach_cli.py --list
```

### Option 3: Direct API Access

You can directly call the API endpoints from any HTTP client:

1. **Start the FastAPI server**

```bash
python run_api.py
```

2. **Access the API endpoints**

Here are examples using curl:

```bash
# Get welcome message
curl http://localhost:8000/

# Analyze a pitch
curl -X POST http://localhost:8000/analyze_pitch \
  -H "Content-Type: application/json" \
  -d '{"pitch_content": "We are building an AI-powered resume optimizer.", "user_id": "api_user"}'

# Simulate investor Q&A
curl -X POST http://localhost:8000/simulate_qa \
  -H "Content-Type: application/json" \
  -d '{"pitch_content": "We are building an AI-powered resume optimizer.", "industry": "technology", "funding_stage": "seed", "user_id": "api_user"}'

# Start a coaching session
curl -X POST http://localhost:8000/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "api_user"}'
```

## API Endpoints

The FastAPI backend provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/analyze_pitch` | POST | Submit a pitch for analysis |
| `/simulate_qa` | POST | Simulate investor Q&A |
| `/pitch_history` | POST | Retrieve pitch history |
| `/all_pitches/{user_id}` | GET | List all pitches for a user |
| `/start_session` | POST | Start a new coaching session |
| `/send_message` | POST | Send a message during a coaching session |
| `/session_action` | POST | Perform an action in a session |

## Project Structure

```
/
├── app/                 # Main application code
│   ├── main.py          # FastAPI application
│   └── static/          # Web interface files
│       ├── index.html   # Web UI HTML
│       ├── css/         # Stylesheets
│       │   └── styles.css # Main CSS
│       └── js/          # JavaScript
│           └── script.js # Client-side logic
├── agents/              # AI agent definitions
│   └── pitch_coach.py   # Pitch coach agents
├── utils/               # Utility modules
│   ├── crew_setup.py    # CrewAI configuration
│   ├── coaching_flow.py # Manages conversation flow and pitch development
│   ├── feedback_tracker.py # Stores and analyzes pitch feedback history
│   └── tasks.py         # Defines tasks for different coaching scenarios
├── requirements.txt     # Project dependencies
├── run_api.py           # Script to run the API server
├── coach_cli.py         # Command-line interface for the coach
└── conversational_cli.py # Conversational CLI interface
```

## Core Components

The application is built around several key modules that work together:

### Coaching Flow (utils/coaching_flow.py)
- Manages the step-by-step guidance through pitch development
- Tracks the current stage of pitch creation (one-liner, problem, solution, etc.)
- Provides tailored prompts and feedback for each pitch component
- Generates a complete pitch from individual components
- Creates simulated investor Q&A scenarios based on the pitch content

### Feedback Tracker (utils/feedback_tracker.py)
- Stores pitch history and feedback across multiple iterations
- Tracks improvement metrics over time
- Saves pitch data persistently in JSON format
- Provides access to historical pitch versions and feedback

### Tasks (utils/tasks.py)
- Defines specific tasks for the CrewAI agents
- Creates structured analysis tasks for pitch evaluation
- Establishes messaging analysis for clarity and persuasiveness
- Sets up Q&A simulation tasks with industry-specific context

## How It Works

The AI Pitch Coach uses a multi-agent approach powered by CrewAI and OpenAI's language models to provide specialized coaching:

1. **Conversational Guidance**: The `PitchCoachFlow` class manages a step-by-step conversation, guiding users through each pitch component (problem, solution, market, etc.)

2. **Specialized Agents**: Three distinct AI agents handle different aspects of coaching:
   - **Structure Coach**: Analyzes pitch organization and narrative flow
   - **Messaging Coach**: Evaluates clarity and persuasiveness
   - **Q&A Coach**: Simulates investor questions based on industry and funding stage

3. **Feedback & Iteration**: The system tracks pitch versions over time, allowing users to see their progress and improvement metrics

4. **Task-based Analysis**: Each coaching interaction is broken down into specific tasks (structural analysis, messaging enhancement, Q&A simulation) for focused feedback

The application provides both a conversational interface (for guided coaching) and a more direct analysis interface (for immediate feedback on existing pitches).

## Troubleshooting

- **API not running**: Make sure to start the API with `python run_api.py` before using the CLI or web interface
- **Authentication errors**: Check that your OpenAI API key is correctly set in the `.env` file
- **Import errors**: Verify that your virtual environment is activated and all dependencies are installed
- **Connection refused errors**: Ensure the API server is running on port 8000 and not blocked by a firewall

## Best Practices

1. **Start Simple**: Begin with a concise one-sentence description of your startup
2. **Iterate Gradually**: Make incremental improvements based on feedback
3. **Practice Q&A Regularly**: Investor questions often reveal weak points in your pitch
4. **Focus on Clarity**: Ensure non-technical investors can understand your value proposition
5. **Track Progress**: Review your pitch history to see how far you've come

## Deployment

The application can be deployed on cloud platforms like Render:

1. Push your code to GitHub
2. Connect your repository to Render
3. Configure your web service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables, especially `OPENAI_API_KEY`

## License

This project is open source.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
