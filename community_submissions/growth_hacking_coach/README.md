# 🚀 Growth Hacking & Viral Marketing Coach

An AI-powered conversational coach that helps entrepreneurs design and execute low-cost, high-impact growth strategies for acquiring users, generating buzz, and scaling their startups efficiently.

## Features

- 💬 **Conversational Interface**: Engage in a natural dialogue with your AI growth coach
- 🔍 **Channel Assessment**: Identify which marketing channels will be most effective for your startup
- 🔄 **Viral Loop Design**: Create viral growth mechanics and referral strategies
- 🤖 **Content & Automation**: Implement AI-driven content creation and marketing automation
- 📊 **Growth Analytics**: Track key metrics and iterate on strategies
- 🧠 **Contextual Memory**: The coach remembers your previous conversations and company details
- 🔄 **Streamlit Integration**: User-friendly chat interface built with Streamlit

## Installation

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ansuamn-shukla/growth-hacking-coach.git
cd growth-hacking-coach
```

2. Install dependencies:
```bash
# Using Poetry (recommended)
poetry install

# Using pip
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your API keys
cp .env.example .env
# Edit the .env file with your actual API keys
```

**Important**: You must replace the placeholder API keys in the .env file with your actual API keys:
- Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Get a Serper API key from [Serper.dev](https://serper.dev/) (optional, for search functionality)

Example .env file:
```
# Gemini API Key
GEMINI_API_KEY=your_actual_gemini_key_here

# Serper API Key (for search tool)
SERPER_API_KEY=your_actual_serper_key_here
```

## Usage

### Live Demo

You can try the Growth Hacking Coach without any installation:

- **Frontend (Streamlit UI)**: [https://agenticaicoach-growth-hacking-coach.streamlit.app/](https://agenticaicoach-growth-hacking-coach.streamlit.app/)
- **Backend API**: [https://agenticaicoach-atbf.onrender.com](https://agenticaicoach-atbf.onrender.com)

### Quick Start

Start the components separately:

#### API Server

Start the FastAPI server:

```bash
uvicorn src.growth_hacking_coach.api:app --reload
```

The API will be available at http://127.0.0.1:8000

#### Streamlit Chat Interface

Start the Streamlit chat interface:

```bash
streamlit run app.py
```

The chat interface will be available at http://localhost:8501

#### Chat Interface Preview

The Streamlit interface provides a user-friendly chat experience:

- Clean, modern design with message bubbles
- Real-time responses from the Growth Hacking Coach
- Session persistence (chat history is maintained during your session)
- Mobile-friendly responsive layout

### API Endpoint

- **POST /query**: Send a message to the Growth Hacking Coach

#### API Request Format

The API accepts a JSON payload with the following structure:

```json
{
  "message": "Your question or message here",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous user message"
    },
    {
      "role": "assistant",
      "content": "Previous assistant response"
    }
  ]
}
```

The `conversation_history` field is optional and allows you to provide context from previous interactions.

### Example API Request

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi! I'm building an AI tool that helps researchers quickly summarize academic papers. We have a basic version out, but user acquisition is really slow."
  }'
```

### Example API Response

```json
{
  "response": "Hi there! Thanks for sharing about your AI research paper summarizer tool. Slow initial user acquisition is a common challenge, especially for specialized tools like yours.\n\nTo help you better, I'd like to understand a bit more about your current situation:\n\n1. Who is your primary target audience? (PhD students, professors, research institutions, etc.)\n2. How are you currently trying to reach potential users?\n3. What's your budget situation for marketing efforts?\n\nIn the meantime, here are two quick experiments you might consider:\n\n1. **Academic Forum Engagement**: Identify 3-5 subreddits, Discord servers, or other online communities where your target users discuss research challenges. Participate genuinely in conversations and mention your tool when relevant to someone's specific problem.\n\n2. **Professor Outreach Campaign**: Create a personalized email template and reach out to 10-15 professors who teach research methods courses. Offer them and their students free access in exchange for feedback.\n\nLet me know more details about your situation, and I can provide more tailored strategies!"
}
```

The coach will analyze your message and provide guidance. If more information is needed, the coach will ask follow-up questions.

## Architecture

This project uses CrewAI to orchestrate a team of specialized AI agents that work together to provide comprehensive growth hacking guidance through a conversational interface:

- **Lead Growth Coach**: Orchestrates the conversation and synthesizes expert advice
- **Channel Specialist**: Identifies high-impact marketing channels
- **Viral Mechanics Designer**: Creates viral growth mechanics and referral programs
- **Content & Automation Guru**: Develops content strategies and automation approaches
- **Growth Analytics Expert**: Provides guidance on metrics and data-driven iteration

The system follows a conversational flow where:
1. The Lead Coach processes the user's message and determines which specialists to consult
2. Relevant specialists analyze the query and provide their expert input
3. The Lead Coach synthesizes this input into a cohesive, conversational response
4. If more information is needed, the Lead Coach will ask follow-up questions

## Development

### Poetry Lock File

This project includes a `poetry.lock` file that locks all dependencies to specific versions, ensuring consistent installations across different environments. If you make changes to the `pyproject.toml` file, update the lock file by running:

```bash
poetry lock
```

### Testing

The project includes a test suite to ensure functionality works as expected:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_api.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
