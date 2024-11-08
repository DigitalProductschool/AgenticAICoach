from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import PDFSearchTool

@CrewBase
class AIComplianceCrew():
    """AI Compliance Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def ai_act_action_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_act_action_extractor'],
            tools=[PDFSearchTool()],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def coaching_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['coaching_auditor'],
            tools=[PDFSearchTool()],
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def ai_compliance_action_planner(self) -> Task:
        task_config = self.tasks_config['ai_compliance_action_planner']
        # Remove 'agent' from task_config if it exists to avoid conflict
        task_config.pop('agent', None)
        return Task(
            **task_config,
            agent=self.ai_act_action_extractor()  # Use self to call the method
        )

    @task
    def ai_compliance_coach(self) -> Task:
        task_config = self.tasks_config['ai_compliance_coach']
        # Remove 'agent' from task_config if it exists to avoid conflict
        task_config.pop('agent', None)
        return Task(
            **task_config,
            agent=self.coaching_auditor()  # Use self to call the method
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AI Compliance Crew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical,  # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )