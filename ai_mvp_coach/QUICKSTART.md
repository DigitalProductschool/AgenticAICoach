# MVP Validation Coach

Enterprise-grade coaching application implementing structured lean startup methodology for rapid MVP validation.

## Architecture Overview

The application implements a multi-phase coaching workflow using CrewAI framework integration:

1. **Risk Assessment** - Systematic identification of critical business assumptions
2. **Experiment Design** - Rapid validation experiment planning
3. **Resource Assessment** - Implementation capacity evaluation
4. **Success Criteria** - Measurable outcome definition

## Technical Implementation

### Core Components

- **`agents/mvp_coach.py`** - Coaching agent factory with behavioral constraints
- **`tasks/coaching_tasks.py`** - Structured task definitions for each validation phase
- **`crew.py`** - Workflow orchestration and session management
- **`main.py`** - Command-line interface and application entry point
- **`simple_coach.py`** - Standalone implementation for deployment flexibility

### Dependencies

- **CrewAI Framework** - Multi-agent workflow orchestration
- **Groq LLM Integration** - High-performance language model backend
- **Python-dotenv** - Environment configuration management

## Execution Options

### Production Deployment (Recommended)
```bash
cd /path/to/ai_mvp_coach
source venv/bin/activate
python -m src.ai_mvp_coach.main
```

### Standalone Deployment
```bash
cd /path/to/ai_mvp_coach
source venv/bin/activate
python -m src.ai_mvp_coach.simple_coach
```

## Configuration

Required environment variables:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

## Methodology

Implements proven lean startup validation principles:

- **Single-question interaction patterns** for conversation depth
- **24-hour execution constraints** for rapid learning cycles
- **Evidence-based decision frameworks** over intuition-driven development
- **Assumption falsification focus** rather than confirmation bias

## Development Standards

- **PEP 8 compliant** code formatting
- **Type hints** for API clarity
- **Comprehensive error handling** with graceful degradation
- **Modular architecture** supporting independent component testing
- **Professional documentation** standards throughout codebase

## Session Termination

Use `exit`, `quit`, `done`, or `stop` to end coaching sessions gracefully.
