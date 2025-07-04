from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class GithubRepoToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    repo_url: str = Field(..., description="The Github Repository URL to analyze.")

class GithubRepoTool(BaseTool):
    name: str = "GitHub Repository Analysis Tool"
    description: str = "Analyzes a single GitHub repository URL to assess code quality, documentation, and developer skills. Returns a brief summary."

    args_schema: Type[BaseModel] = GithubRepoToolInput

    def _run(self, repo_url: str) -> str:
        if not repo_url or "github.com" not in repo_url:
            return "Invalid or missing GitHub URL provided."
        return (f"Mock analysis for the repository at {repo_url}: "
                "The project appears to be well-structured with a clear README file. "
                "Contributions seem consistent, suggesting good developer habits.")