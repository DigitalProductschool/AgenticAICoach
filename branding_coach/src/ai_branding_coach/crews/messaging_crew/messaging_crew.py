from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from pydantic import BaseModel
from typing import List

class MessagingCrewOutput(BaseModel):
    refined_message: str
    taglines: List[str]
    slogans: List[str]

@CrewBase
class MessagingCrew():
    """MessagingCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def messaging_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['messaging_researcher'],
            verbose=True,
            max_iter=3,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_pydantic=MessagingCrewOutput,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MessagingCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
