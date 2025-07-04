
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from chainlit import AskUserMessage, run_sync

def ask_human(question: str, timeout: int = 300) -> str:
    """Send a question to the human user and return their response as a string."""
    response = run_sync(
        AskUserMessage(content=question, timeout=timeout).send()
    )
    return (response or {}).get("output", "No response received.")

class HumanInputContextToolInput(BaseModel):
    question: str = Field(..., description="Description of the argument.")

class HumanInputContextTool(BaseTool):
    name: str = "ask_user"
    description: str = (
        "Use this tool to ask follow-up questions to the human through the Chainlit UI "
        "if additional context is needed during the task. Maximum 2 uses per run."
    )
    args_schema: Type[BaseModel] = HumanInputContextToolInput

    def _run(self, question: str) -> str:
        if isinstance(question, dict) and 'description' in question:
            return ask_human(question['description'])
        elif isinstance(question, str):
            return ask_human(question)
        else:
            raise ValueError("Invalid input type. Expected a string or a dictionary with 'description' key.")