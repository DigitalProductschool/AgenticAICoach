# Contributing to Our Open Source Project

We welcome contributions! Whether you're an experienced developer or just starting out, we appreciate any help you can give us. Here's how you can get involved:

## Submission Guidelines

### Agent Structure

You can submit your completele coaching application crew using our template proposal. 

Alternatively, you can submit an Agent to be integrated in our coaching examples, please follow this structure:

1. **Agent Definition (`agent.py`)**:
   - Create a file named `agent.py` in the `community_submissions/[agent_name]/` directory. 
   - Define your Agent class using CrewAI's `@Agent` decorator.
   - Include any necessary imports and helper functions.

2. **Unit Tests (`tests/` directory)**:
   - Create a `tests/` directory inside your Agent's directory.
   - Write unit tests for your Agent using Python's built-in `unittest` module or a testing framework of your choice.
   - Include at least one test case that covers the main functionality of your Agent.

3. **Additional Configuration Files**:
   - If your Agent requires any additional configuration, create a `config/` directory in your Agent's folder.
   - Place any necessary configuration files (e.g., YAML, JSON) in this directory.

### Example Structure

```bash
community_submissions/
└── my_agent/
    ├── coaching_application_template
    ├── agent_template
         └── agent.py
         └── tests/
            └── test_agent.py
```

### Submission Process

1. Fork the repository on GitHub.
2. Clone your fork to your local machine.
3. Navigate to the `community_submissions/` directory.
4. Create a new directory for your Agent and add the required files.
5. Commit and push your changes to your fork.
6. Open a Pull Request against the main repository.

### Code Style

- We follow CrewAI's style guide. Please refer to the [CrewAI Documentation](https://docs.crew.ai/) for details.
- Use consistent indentation (PEP 8 recommends 4 spaces).

### Testing

- All submissions must include unit tests.
- Tests should cover critical paths through your Agent's functionality.
- Include a test that verifies the Agent's output matches expectations.

### Documentation

- Add comments to your code explaining complex logic or decisions.
- Include a brief description of your Agent's purpose and how it fits into the overall project.

### License

- Make sure your submission complies with the project's license (MIT).
- Include a copy of the MIT license in your submission if it's not already present.

### Review Process

- We aim to review submissions within 3 business days.
- Be prepared to address feedback and make necessary changes.

### Additional Notes

- If your Agent depends on external libraries, please specify them in your pyproject.toml file under [tool.poetry.dependencies].
- If your Agent interacts with external services, please document any API endpoints or authentication methods used.

Thank you for your contribution! We look forward to reviewing your submission.

## Citations:
2. [GitHub Guidelines for Contributors](https://docs.github.com/articles/setting-guidelines-for-repository-contributors)
3. [freeCodeCamp Contributing Guide](https://github.com/freeCodeCamp/how-to-contribute-to-open-source/blob/main/CONTRIBUTING.md)
4. [How to Build a Contributing.md](https://contributing.md/how-to-build-contributing-md/)
5. [CNCF Maintainers Templates](https://contribute.cncf.io/maintainers/templates/contributing/)
6. [Open Source Contributor Guidelines](https://opensource.com/life/16/3/contributor-guidelines-template-and-tips)
7. [Best Practices for Managing an Open Source Project](https://blog.codacy.com/best-practices-to-manage-an-open-source-project)
8. [freeCodeCamp Guide on Contributing to Open Source](https://www.freecodecamp.org/news/how-to-contribute-to-open-source/)
9. [Open Source Guide: How to Contribute](https://opensource.guide/how-to-contribute/)
```
