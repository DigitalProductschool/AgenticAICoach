from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from tools.dynamic_input_tool import HumanInputContextTool

from pydantic import BaseModel
from typing import List

class BrandNarrativeOutput(BaseModel):
    mission: str
    vision: str
    values: str
    target_audience_pain_points: str
    final_narrative: str
    messaging_pillars: List[str]

@CrewBase
class NarrativeCrew():
    """NarrativeCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    # ollama_llm = LLM(
    #     model='ollama/llama3.2',
    #     base_url='http://localhost:11434'
    # )

    @agent
    def narrative_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["narrative_researcher"],
            verbose=True,
            tools=[
                HumanInputContextTool(max_usage_count=2)
            ],
            # llm=self.ollama_llm,
        )

    @agent
    def story_coach(self) -> Agent:
        return Agent(
            config=self.agents_config["story_coach"],
            verbose=True,
            tools=[
                HumanInputContextTool(max_usage_count=2)
            ],
            # llm=self.ollama_llm,
        )

    @agent
    def archetype_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["archetype_strategist"],
            verbose=True,
            # llm=self.ollama_llm,
        )

    @agent
    def narrative_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["narrative_editor"],
            verbose=True,
            # llm=self.ollama_llm,
        )

    # --------------  TASKS  --------------------------------------------------
    @task
    def research_context(self) -> Task:
        return Task(
            config=self.tasks_config["research_context"]
        )

    @task
    def elicitation_story(self) -> Task:
        return Task(
            config=self.tasks_config["elicitation_story"]
        )

    @task
    def framework_mapping(self) -> Task:
        return Task(
            config=self.tasks_config["framework_mapping"]
        )

    @task
    def editing_polish(self) -> Task:
        return Task(
            config=self.tasks_config["editing_polish"],
            output_pydantic=BrandNarrativeOutput
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NarrativeCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
