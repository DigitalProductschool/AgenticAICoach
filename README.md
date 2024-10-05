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

2. Choose your agentic coaching applications. 

3. Run the project following its README specifications. 

## Project Structure
Our project follows CrewAI's recommended structure:
```bash 
AgenticAICoach/
├── .gitignore                # Git ignore file for excluding unnecessary files
├── README.md                 # Main project documentation
├── agentic_coaching_applications/
│   └── template_application/   # Template for creating new agentic applications
│       ├── __init__.py         # Initializes the template application
│       ├── main.py             # Main entry point for the template application
│       ├── crew.py             # Handles CrewAI agents and tasks orchestration
│       ├── app.py              # Streamlit app or main interface for this application
│       ├── config/             # Configuration folder for agents and tasks
│       │   ├── agents.yaml     # YAML file defining agents' roles and settings
│       │   └── tasks.yaml      # YAML file defining tasks and their workflow
│       └── tools/              # Custom tools that the agent may utilize
│           ├── custom_tool.py  # Example of a custom tool integrated with the agent
│           └── __init__.py     # Initializes the tools package
└── docs/                       # Documentation files
    ├── CONTRIBUTING.md         # Guidelines for contributing to the project
    └── PULL_REQUEST_TEMPLATE.md  # Template for submitting pull requests
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the CrewAI team for creating such an excellent framework!
- Thanks to all community members who contribute their agents to this project.


