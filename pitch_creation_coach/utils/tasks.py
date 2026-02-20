from crewai import Task

#This class defines the specific tasks that the agents will perform
class PitchCoachTasks:

    #Method performs Structure Analysis: Evaluates if the pitch has all essential components
    @staticmethod
    def create_structure_analysis_task(agent, pitch_content):
        return Task(
            description=f"""
            Analyze the following pitch structure and provide guidance:
            
            PITCH: {pitch_content}
            
            1. Identify if the pitch clearly articulates: problem, solution, market, business model, and unique value proposition
            2. Suggest improvements to the structure following startup storytelling best practices
            3. Provide a step-by-step guide to enhance the pitch structure
            """,
            agent=agent,
            expected_output="A detailed analysis of the pitch structure with specific recommendations for improvement"
        )
    
    #Method performs Messaging Analysis: Focuses on clarity and impact
    @staticmethod
    def create_messaging_analysis_task(agent, pitch_content):
        return Task(
            description=f"""
            Analyze the clarity and persuasiveness of the following pitch:
            
            PITCH: {pitch_content}
            
            1. Evaluate how clearly complex concepts are explained
            2. Assess the persuasiveness and emotional appeal 
            3. Suggest specific wording improvements to make the pitch more impactful
            """,
            agent=agent,
            expected_output="An analysis of pitch clarity and persuasiveness with specific wording improvement suggestions"
        )
    #Method performs Q&A Simulation: Creates realistic investor questions based on industry and funding stage
    @staticmethod
    def create_qa_simulation_task(agent, pitch_content, industry, funding_stage):
        return Task(
            description=f"""
            Generate potential investor questions for the following pitch:
            
            PITCH: {pitch_content}
            INDUSTRY: {industry}
            FUNDING STAGE: {funding_stage}
            
            1. Generate 5 realistic questions investors might ask about this pitch
            2. For each question, provide guidance on how to answer effectively
            3. Focus on questions that address potential concerns or weaknesses in the pitch
            """,
            agent=agent,
            expected_output="A list of 5 realistic investor questions with guidance on how to answer each effectively"
        )