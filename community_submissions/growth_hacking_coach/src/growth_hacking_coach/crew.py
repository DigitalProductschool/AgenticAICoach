from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai import LLM


@CrewBase
class GrowthHackingCrew():
    """Growth Hacking & Viral Marketing Coach Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Initialize tools
    search_tool = SerperDevTool(
        n_results=3,
    )

    @agent
    def lead_growth_coach(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_growth_coach'],
            verbose=True,
            memory=True,
            llm=LLM(
                model="gemini/gemini-2.5-flash-preview-04-17",
                temperature=0.5,
            ),
            allow_delegation=True
        )

    @agent
    def channel_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['channel_specialist'],
            tools=[self.search_tool],
            verbose=True,
            max_iter= 1,
            memory=True,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.2,
            ),
            allow_delegation=False
        )

    @agent
    def viral_mechanics_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['viral_mechanics_designer'],
            tools=[self.search_tool],
            max_iter= 1,
            verbose=True,
            memory=True,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.2,
            ),
            allow_delegation=False
        )

    @agent
    def content_automation_guru(self) -> Agent:
        return Agent(
            config=self.agents_config['content_automation_guru'],
            tools=[self.search_tool],
            verbose=True,
            max_iter= 1,
            memory=True,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.2,
            ),
            allow_delegation=False
        )

    @agent
    def growth_analytics_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['growth_analytics_expert'],
            tools=[self.search_tool],
            max_iter= 1,
            verbose=True,
            memory=True,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.2,
            ),
            allow_delegation=False
        )

    @task
    def synthesize_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesize_response_task'],
            agent=self.lead_growth_coach()
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the Growth Hacking Crew"""
        return Crew(
            agents=[
                self.content_automation_guru(),
                self.channel_specialist(),
                self.viral_mechanics_designer(),
                self.growth_analytics_expert(),
            ],
            tasks=[
                self.tasks_config['synthesize_response_task']
            ],
            manager_agent=self.lead_growth_coach(),      
            process=Process.sequential,
            verbose=True,
        )
