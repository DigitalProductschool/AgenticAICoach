from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class VisualCrew():
    """VisualCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def visual_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_designer'],
            verbose=True
        )

    @task
    def create_visual_guidelines(self) -> Task:
        return Task(
            config=self.tasks_config['create_visual_guidelines'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VisualCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
