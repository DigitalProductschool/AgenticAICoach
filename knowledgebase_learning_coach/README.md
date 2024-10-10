# Learning PDF Coach

## Overview
The Learning PDF Coach is an agentic AI coach that helps you search and answer questions based on uploaded PDF documents. Built using Streamlit and CrewAI, it allows users to ask questions and receive answers from multiple uploaded documents.

## Directory Structure

```
learning_pdf_agent/
├── src/
│   ├── learning_pdf_coach_agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── main.py
│   │   ├── crew.py
│   │   ├── tools/
│   │   │   └── pdf_search.py
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   ├── tasks.yaml
│   ├── __init__.py
├── tests/
│   ├── test_agent.py
├── pyproject.toml
├── .env.example
├── README.md
```

### **Summary**
- **Split your code into modular components**: Move each responsibility into separate files (`agent.py`, `crew.py`, etc.) to align with the CrewAI example structure.
- **Logging Improvements**: Ensure logs appear in the terminal using `logging`, and provide user-friendly messages on the Streamlit interface.
- **Update Configuration**: Ensure the YAML configurations (`agents.yaml` and `tasks.yaml`) are kept consistent with the agent's purpose and goals.
- **Refactor for Better Usability**: Refactor `main.py` to handle user interaction cleanly, without exposing technical logs to users.

This restructuring makes your application well-organized, maintainable, and easy for other developers to contribute to, while also providing a better user experience by removing technical details from the user-facing interface.
