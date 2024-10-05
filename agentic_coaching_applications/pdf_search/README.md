# Agentic PDF Search

## Architecture Overview

The **Agentic AI Coach** is structured using a microservice architecture, interacting with external services like GPT-4 and document processing tools. It enables users to upload documents and receive AI-powered insights in real time. For a detailed breakdown of the system, including architecture diagrams, check the full architecture documentation [here](docs/architecture.md).

![System Context Diagram](docs/system-context-diagram-agentic-pdf-search.png)

---

## Breakdown of Crews, Agents, and Tasks

### **Crews**
- **Crew 1**: Created in the `agentic_AI_coach()` function, responsible for orchestrating the agent's task.
  - **Process**: The crew executes tasks sequentially using `Process.sequential`, ensuring that tasks are carried out one after another in a structured manner.

### **Agents**
- **Agent 1**: 
  - **Role**: "Document Search Agent"
  - **Goal**: To search through uploaded documents and extract relevant answers.
  - **Backstory**: The agent is designed to be highly efficient at scanning and retrieving data from multiple PDF documents.
  - **Tools**: The agent utilizes the `PDFSearchTool` for document processing and interacts with the GPT-4 language model (`llm_gpt4`) to generate answers.

### **Tasks**
- **Task 1**: Created dynamically based on user input.
  - **Description**: "Use the available tools to find relevant information in the documents. Based on this information, answer the following question: [user's question]."
  - **Expected Output**: A clear and concise response to the user’s question.
  - **Agent**: The document search agent handles the task using the provided tools.
  - **Crew**: The crew is responsible for managing and executing the task in collaboration with the agent.

---

## Summary:
- **Crew**: Manages the sequential execution of tasks by the agent.
- **Agent**: Scans documents and answers user queries using available tools like `PDFSearchTool` and GPT-4.
- **Task**: The task is dynamically created based on user questions and involves retrieving relevant information from uploaded PDFs.

---

## Usage

1. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. Run the Streamlit application:
   ```sh
   streamlit run app.py
   ```

5. Upload PDF documents using the sidebar, and ask questions to get insights from your documents.