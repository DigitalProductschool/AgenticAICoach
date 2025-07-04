from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import yaml

from pydantic import BaseModel
from typing import List

class Suggestion(BaseModel):
    from_: str  # use 'from_' because 'from' is a reserved keyword
    to: str

class SuggestionOutput(BaseModel):
    original_text: str
    revised_text: str
    suggestions: List[Suggestion]
    feedback: str
    
@CrewBase
class ConfidenceCoachCrew():
    """Confidence Coach Crew for analyzing and improving communication"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def ConfidenceAnalysisAgent(self) -> Agent:
        """Agent responsible for analyzing low-confidence markers in the user's text"""
        return Agent(
            config=self.agents_config['ConfidenceAnalysisAgent'],  
            verbose=True
        )

    @agent
    def SuggestionAgent(self) -> Agent:
        """Agent responsible for suggesting confident language alternatives"""
        return Agent(
            config=self.agents_config['SuggestionAgent'],  
            verbose=True
        )

    @task
    def Analyze_task(self) -> Task:
        """Task to analyze the user's text for low-confidence markers"""
        return Task(
            config=self.tasks_config['Analyze_task'],  # Type from config
        )

    @task
    def Suggestion_task(self) -> Task:
        """Task to suggest improvements to the user's text for more assertive language"""
        return Task(
            config=self.tasks_config['Suggestion_task'],  # Type from config
            output_json=SuggestionOutput 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the confidence coach crew that orchestrates the agents and tasks"""
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # Orchestrates tasks sequentially
            verbose=True,
        )
