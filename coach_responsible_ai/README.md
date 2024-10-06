# AI Act Compliance Coach

## Introduction

This project leverages the CrewAI framework to automate the process of evaluating project descriptions for compliance with the **AI Act**. The system orchestrates autonomous AI agents to analyze project descriptions and assess their alignment with the principles and regulations outlined in the AI Act, such as fairness, transparency, accountability, safety, and data privacy.

## CrewAI Framework

**CrewAI** is a framework designed to facilitate collaboration among role-playing AI agents. In this project, AI agents work together to evaluate project descriptions against the AI Act, ensuring compliance with key regulations and producing a detailed compliance report.

## Running the Script

This project uses GPT-4 by default, so you will need access to GPT-4 to run it.

**Disclaimer:** The script uses GPT-4 unless otherwise configured. Please note that different AI models may incur varying costs.

### Steps to Run:

1. **Configure the Environment**:
   - Copy `.env.example` to `.env` and configure your OpenAI API keys and other necessary environment variables.

2. **Install Dependencies**:
   - Run the following commands to lock and install dependencies using Poetry (you need to install Poetry first):
     ```bash
     poetry lock 
     poetry install
     ```

3. **Customize**:
   - Modify `src/ai_act_compliance_checker/main.py` to add your custom inputs (e.g., paths to project descriptions and AI Act documents).
   - Update agent configurations in `src/ai_act_compliance_checker/config/agents.yaml`.
   - Modify task configurations in `src/ai_act_compliance_checker/config/tasks.yaml`.

4. **Execute the Script**:
   - Run the following command to execute the compliance check:
     ```bash
     poetry run ai_act_compliance_checker
     ```
   - Provide paths to the AI Act document and project description when prompted.

## Details & Explanation

**Running the Script:**  
When you execute the script using `poetry run ai_act_compliance_checker`, the system will utilize the **CrewAI** framework to run agents that analyze the project description against the AI Act requirements. A detailed compliance assessemnt along with suggesttions for some improvement ideas will be generated.

**Key Components:**
- **`src/ai_act_compliance_checker/main.py`:** Main script where inputs are provided and the analysis is initiated.
- **`src/ai_act_compliance_checker/crew.py`:** Defines the AI Compliance Crew, linking agents and tasks together.
- **`src/ai_act_compliance_checker/config/agents.yaml`:** Configuration file for defining agents, such as the PDF search tool and document analysis tool.
- **`src/ai_act_compliance_checker/config/tasks.yaml`:** Configuration file for defining tasks, including the AI Act compliance check.
- **`src/ai_act_compliance_checker/tools`:** Directory containing tools used by the agents to perform tasks, such as document analysis.

## Contributing

Contributions are welcome! Feel free to submit pull requests for improvements, new agents, or tasks that enhance the AI Act Compliance Coach’s functionality.


## Appreciation to Contributors

We would like to express our sincere appreciation to the contributors of the [CrewAI Examples Repository](https://github.com/crewAIInc/crewAI-examples/tree/main) for the inspiring examples. 

## License

This project is released under the **MIT License**.
