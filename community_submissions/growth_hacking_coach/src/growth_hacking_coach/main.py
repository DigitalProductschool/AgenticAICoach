#!/usr/bin/env python
import os
from dotenv import load_dotenv
from crew import GrowthHackingCrew

# Load environment variables
load_dotenv()

def run():
    """Run the Growth Hacking Coach with sample inputs"""
    print("Starting Growth Hacking Coach...")


    serper_key = os.getenv("SERPER_API_KEY")

    inputs = {
        'user_message': "I want to grow my startup's user it is fintech satrtup focused in crypto ?"
    }

    print("Initializing Growth Hacking Crew...")
    try:
        # Initialize and run the crew
        crew = GrowthHackingCrew()
        print("Crew initialized successfully.")

        print("Starting crew execution...")
        try:
            result = crew.crew().kickoff(inputs=inputs)
            print("Crew execution completed.")

            print("Result:")
            print(result)
        except AttributeError as ae:
            print(f"AttributeError: {str(ae)}")
            print("This might be due to missing tasks or agents.")
            print("Available attributes:", dir(crew))
            if hasattr(crew, 'agents'):
                print("Agents:", crew.agents)
            if hasattr(crew, 'tasks'):
                print("Tasks:", crew.tasks)
    except Exception as e:
        import traceback
        print(f"Error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    run()
