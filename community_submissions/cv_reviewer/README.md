# AI CV Review Coach

An intelligent multi-agent system built with **CrewAI** and **FastAPI** that provides comprehensive, structured feedback on professional CVs. Users can upload a PDF or DOCX file and receive a detailed analysis, including an overall score, actionable suggestions, and relevant job role recommendations.

---

## ✨ Features

- **Direct File Upload**: Supports `.pdf` and `.docx` file formats for a seamless user experience.
- **Intelligent Tool Usage**: Automatically detects and analyzes GitHub links found within the CV text.
- **Structured AI Output**: Leverages Pydantic models to ensure the AI's response is always a consistent, structured JSON object.
- **User-Friendly Frontend**: A clean and responsive interface built with HTML and Tailwind CSS to display the analysis in an easy-to-digest format.
- **Robust Backend**: Built on FastAPI with a clean, modular architecture separating concerns (API, AI logic, utilities).
- **Containerized**: Fully containerized with Docker and Docker Compose for easy setup and deployment.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Gunicorn, Uvicorn
- **AI Framework**: CrewAI
- **File Parsing**: `pypdf`, `python-docx`
- **Frontend**: HTML, Tailwind CSS, JavaScript (`marked.js`)
- **Containerization**: Docker, Docker Compose
- **Dependency Management**: Poetry

---

## 📂 Project Structure

The project follows a clean, modular architecture to separate concerns:


.
├── Dockerfile          # Defines the container for the application
├── pyproject.toml      # Manages Python dependencies with Poetry
├── static/
│   └── index.html      # The single-page frontend
└── src/
├── api.py          # FastAPI application, handles HTTP requests
├── cv_reviewer/    # The core CrewAI package
│   ├── config/     # YAML files for agents and tasks
│   ├── crew.py     # Assembles the crew from agents and tasks
│   └── tools/      # Custom tools for agents (e.g., GitHub tool)
├── schemas/
│   └── cv_output.py# Pydantic model for structured AI output
└── utils/
├── agent_helper.py # Bridge between the API and the crew
└── file_parser.py  # Handles parsing of PDF/DOCX files


---

## 🚀 Getting Started (Docker)

Running the application with Docker is the recommended method.

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your system.
- An OpenAI API key.

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd cv_reviewer
    ```

2.  **Create Environment File**
    Create a `.env` file in the project's root directory. Add your OpenAI API key to this file:
    ```
    OPENAI_API_KEY=sk-YourSecretApiKeyGoesHere
    ```

3.  **Build and Run with Docker Compose**
    From the root directory, run the following command. This will build the Docker image and start the application.
    ```bash
    docker-compose up --build
    ```

4.  **Access the Application**
    Once the container is running, open your web browser and navigate to:
    **[http://localhost:8000](http://localhost:8000)**

You can now upload a CV and receive your AI-powered review!

---

### 💻 Local Development (Without Docker)

If you prefer to run the application locally for development:

1.  **Install Poetry**:
    Follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

2.  **Install Dependencies**:
    ```bash
    poetry install --no-dev
    ```

3.  **Create `.env` File**:
    As described in the Docker setup, create a `.env` file in the root directory with your `OPENAI_API_KEY`.

4.  **Run the FastAPI Server**:
    ```bash
    poetry run uvicorn src.api:app --reload
    ```

5.  **Access the Application**:
    The application will be available at **[http://localhost:8000](http://localhost:8000)**.
