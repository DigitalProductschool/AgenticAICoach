from crewai import Crew
from agents.pitch_coach import PitchCoachAgents
from utils.tasks import PitchCoachTasks

#This class ties together the agent definitions and task definitions using CrewAI
class PitchCoachCrew:
    def __init__(self):
        self.agents = PitchCoachAgents()
    
    def analyze_initial_pitch(self, pitch_content):
        # Create agents
        structure_coach = self.agents.create_structure_coach()
        messaging_coach = self.agents.create_messaging_coach()
        
        # Create tasks
        structure_task = PitchCoachTasks.create_structure_analysis_task(
            structure_coach, pitch_content
        )
        messaging_task = PitchCoachTasks.create_messaging_analysis_task(
            messaging_coach, pitch_content
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[structure_coach, messaging_coach],
            tasks=[structure_task, messaging_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def simulate_investor_qa(self, pitch_content, industry, funding_stage):
        # Create agent
        qa_coach = self.agents.create_qa_simulation_coach()
        
        # Create task
        qa_task = PitchCoachTasks.create_qa_simulation_task(
            qa_coach, pitch_content, industry, funding_stage
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[qa_coach],
            tasks=[qa_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result