# AiCommunityMatchmaker Crew

Welcome to the AiCommunityMatchmaker Crew project, powered by [crewAI](https://crewai.com). This coach help community members connect with others who can help them achieve their entrepreneurship goals. The AI Community Matchmaker Coach take the profile data of the user and the community members then suggest cofounder and mentor matches based on skills, interests, goals, and potential collaborations.

**Input:**
- A CSV file contains the profiles of the community members 
- A JSON file contains the profile of the target user looking for matches

**Output:**
- A Markdown file contains the list of suggested cofounder matches and mentor matches ranked by relevance to the user's goals, with their corresponding social media URL (if included in the inputs), and breif description why the matches are suitable.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```
pip install -r requirements.txt
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

```
OPENAI_API_KEY=<your-openai-api-key>
```

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes your AI crew, activates their assigned tasks, and begins the collaborative execution process. By default, the project generates a report.md file in the root directory containing a summary of community match recommendations based on the input CSV and JSON files.

## Understanding The Crew

The ai-community-matchmaker Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in the crew.

## API Deployment
If deploying as an API, use FastAPI. To run the API locally:

```bash
uvicorn src.ai_community_matchmaker.api:app --reload
```

Access the interactive documentation at http://127.0.0.1:8000/docs.

Endpoint: POST /run-matchmaker/

## Run unit test

```bash
python -m unittest discover -s tests
```