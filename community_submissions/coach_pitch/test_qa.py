from utils.crew_setup import PitchCoachCrew
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY is not set in .env file")
    exit(1)

# Test sample pitch
sample_pitch = """
We're building an AI-powered resume optimizer to help job seekers improve their job applications.
Our solution analyzes resumes against job descriptions and provides tailored recommendations.
We target recent graduates and career changers who struggle with the job application process.
"""

try:
    print("Initializing Pitch Coach Crew...")
    crew = PitchCoachCrew()
    
    print("Simulating investor Q&A...")
    result = crew.simulate_investor_qa(
        pitch_content=sample_pitch,
        industry="technology",
        funding_stage="seed"
    )
    
    print("\n=== Q&A SIMULATION RESULT ===\n")
    print(result)
    print("\n=== TEST COMPLETED SUCCESSFULLY ===\n")
except Exception as e:
    print(f"ERROR: {str(e)}")