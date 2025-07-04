from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ContentCrew():
    """ContentCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'],
            verbose=True
        )

    @task
    def generate_website_copy(self) -> Task:
        return Task(
            config=self.tasks_config['generate_website_copy'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ContentCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
