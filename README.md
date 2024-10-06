# Agentic AI Coach

Agentic AI Coach is an open-source project that utilizes CrewAI to enable collaborative AI agents for various coaching tasks. This project aims to foster community involvement by allowing members to submit their own AI agents for integration into our coaching system. 
It is pioneered by the [AI Makerspace](https://github.com/DigitalProductschool/AI-Makerspace) community of DPS with the purpose to provide scalable coaching for entrepreneurial teams. DPS alumni and AI engineers are encouraged to contribute by submitting Agents and Tasks, and Crews.

## Features

- **Modular Architecture**: Built using CrewAI, allowing easy addition of new agents and tasks.
- **Community-driven**: Encourage community members to contribute their own AI agents.
- **Flexible Configuration**: Easily customize agents and tasks through YAML configuration files.
- **Extensible Tools**: Support for custom tools to enhance agent capabilities.

## Getting Started

To get started with Agentic AI Coach, follow these steps:

1. Clone the repository:
   ```sh
   git clone DigitalProductschool/AgenticAICoach
   cd AgenticAICoach

2. Choose your coaching applications. For example, coach_responsible_ai. 

3. Run the project following its README specifications. 

## Project Structure
Our project follows CrewAI's recommended structure:
```bash 
AgenticAICoach/
├── coach_responsible_ai/
│   ├── db/
│   ├── src/
│   │   └── ai_act_compliance_checker/
│   │       ├── config/
│   │       │   ├── agents.yaml
│   │       │   ├── tasks.yaml
│   │       ├── data/
│   │       ├── tools/
│   │       ├── __init__.py
│   │       ├── crew.py
│   │       ├── main.py
│   ├── .env.example
│   ├── .gitignore
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   ├── trained_agents_data.pkl
├── community_submissions/
│   ├── agent_template/
│   │   ├── tests/
│   │   │   └── test_agent.py
│   │   ├── agent.py
│   ├── coaching_application_template/
├── docs/
│   ├── CONTRIBUTING.md
│   ├── PULL_REQUEST_TEMPLATE.md
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the CrewAI team for creating such an excellent framework!
- Thanks to all community members who contribute their agents to this project.


