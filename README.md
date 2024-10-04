# Agentic AI Coach

Agentic AI Coach is an open-source project that utilizes CrewAI to enable collaborative AI agents for various coaching tasks. This project aims to foster community involvement by allowing members to submit their own AI agents for integration into our coaching system.

## Features

- **Modular Architecture**: Built using CrewAI, allowing easy addition of new agents and tasks.
- **Community-driven**: Encourage community members to contribute their own AI agents.
- **Flexible Configuration**: Easily customize agents and tasks through YAML configuration files.
- **Extensible Tools**: Support for custom tools to enhance agent capabilities.

## Getting Started

To get started with Agentic AI Coach, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/agentic-ai-coach.git
   cd agentic-ai-coach

2. Install dependencies:
    ```sh
    poetry install

3. Run the project:
    ```sh 
    poetry run python src/agentic-ai-coach/main.py


## Project Structure
Our project follows CrewAI's recommended structure:
```bash 
agentic-ai-coach/
├── .gitignore
├── README.md
├── pyproject.toml
├── src/
│   └── agentic-ai-coach/
│       ├── __init__.py
│       ├── main.py
│       ├── crew.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           ├── custom_tool.py
│           └── __init__.py
└── docs/
    ├── CONTRIBUTING.md
    └── PULL_REQUEST_TEMPLATE.md
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the CrewAI team for creating such an excellent framework!
- Thanks to all community members who contribute their agents to this project.

## Citations:

1. [CrewAI Example](https://github.com/indexnetwork/examples/blob/main/crewai/README.md?ref=blog.ceramic.network)
2. [CrewAI Getting Started](https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/)
3. [CrewAI Quickstart](https://github.com/alexfazio/crewAI-quickstart/blob/main/README.md)
4. [Developing with CrewAI](https://patford12.medium.com/developing-with-crewai-086d3aafe9de)
5. [Perfect README Guide](https://www.reddit.com/r/opensource/comments/txl9zq/next_level_readme/)
6. [CrewAI Marketing Agents](https://gitlab.leadingbit.com/externaldev/ai_marketing_agents_crewai/-/blob/main/README.md)
7. [How to Make a README](https://www.makeareadme.com/)
8. [Video on Creating a README](https://www.youtube.com/watch?v=sPzc6hMg7So)
9. [CrewAI Open Source](https://www.crewai.com/open-source)
10. [Guide to the Perfect README](https://dev.to/github/how-to-create-the-perfect-readme-for-your-open-source-project-1k69)
