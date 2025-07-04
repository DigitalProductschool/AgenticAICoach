from crewai import Agent
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

#This class defines the three specialized AI agents that power the coaching system
class PitchCoachAgents:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))
    
    def create_structure_coach(self):
        return Agent(
            role="Pitch Structure Coach",
            goal="Help founders structure compelling startup pitches",
            backstory="Expert in startup storytelling and pitch deck structure",
            verbose=True,
            llm=self.llm
        )
    
    def create_messaging_coach(self):
        return Agent(
            role="Pitch Messaging Coach",
            goal="Analyze and improve pitch clarity and persuasiveness",
            backstory="Communication expert specializing in simplifying complex concepts and crafting compelling narratives for startups",
            verbose=True,
            llm=self.llm
        )
        
    def create_qa_simulation_coach(self):
        return Agent(
            role="Investor Q&A Coach",
            goal="Prepare founders for tough investor questions",
            backstory="Former VC with experience evaluating thousands of startups across various funding stages",
            verbose=True,
            llm=self.llm
        )