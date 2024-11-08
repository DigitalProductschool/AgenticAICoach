from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class YourCrew():
    """Your Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def agent1(self) -> Agent:
        return Agent(
            config=self.agents_config['agent1'],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def agent2(self) -> Agent:
        return Agent(
            config=self.agents_config['agent2'],
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def task1(self) -> Task:
        return Task(
            config=self.tasks_config['task1'],
            agent=self.agent1()
        )

    @task
    def task2(self) -> Task:
        return Task(
            config=self.tasks_config['task2'],
            agent=self.agent2()
        )


    @crew
    def crew(self) -> Crew:
        """Creates Your Crew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical,  # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    
