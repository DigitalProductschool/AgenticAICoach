# AI MVP Coach 🎯

An AI-powered coach that helps entrepreneurs validate their MVP ideas through structured self-reflection using CrewAI. ([DPS](https://digitalproductschool.io) AI track assessment.)

## Core Features

- **Guided Self-Reflection**: One question at a time approach
- **Risk Assessment**: Identify the riskiest assumptions in your MVP
- **Quick Validation**: Design experiments testable within 24 hours
- **Actionable Insights**: Get clear next steps for your MVP

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the coach
python -m ai_mvp_coach.main
```

## How It Works

The AI MVP Coach guides you through 4 key stages:

1. **Identify Riskiest Assumption** - Define your core AI feature and uncertainty
2. **Design Validation Experiment** - Break down assumptions into testable hypotheses
3. **Fast Prototyping** - Create the simplest testable version
4. **Define Success Metrics** - Set clear validation criteria

## Project Structure

```
ai_mvp_coach/
├── src/ai_mvp_coach/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── crew.py           # CrewAI setup
│   ├── agents/           # AI agents
│   └── tools/            # Custom tools
├── tests/
└── README.md
```

## License

MIT License
