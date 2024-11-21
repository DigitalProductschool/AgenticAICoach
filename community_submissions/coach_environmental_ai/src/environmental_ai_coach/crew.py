import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools.custom_tool import AirQualityTool
import os


#uncomment
# os.environ["OPENAI_API_KEY"] = ""
# os.environ["SERPER_API_KEY"] = ""
# Define agents

search_tool = SerperDevTool()
air_quality_tool = AirQualityTool()

with open('config/agents.yaml', 'r') as file:
    agent_config = yaml.safe_load(file)

with open('config/tasks.yaml', 'r') as file:
    task_config = yaml.safe_load(file)



location_researcher = Agent(
    role=agent_config['location_researcher']['role'],
    goal=agent_config['location_researcher']['goal'],
    backstory=agent_config['location_researcher']['backstory'],
    tools=[search_tool, air_quality_tool],
)


# action_planner = Agent(
#     role=agent_config['action_planner']['role'],
#     goal=agent_config['action_planner']['goal'],
#     backstory=agent_config['action_planner']['backstory'],
#     memory=True,
#     cache=True
# )

progress_tracker = Agent(
    role=agent_config['progress_tracker']['role'],
    goal=agent_config['progress_tracker']['goal'],
    backstory=agent_config['progress_tracker']['backstory'],
    # memory=True,
    cache=True
)


research_task = Task(
    description=task_config['research_task']['description'],
    expected_output=task_config['research_task']['expected_output'],    
    agent=location_researcher,
)


# create_action_plan = Task(
#     description=task_config['create_action_plan']['description'],
#     expected_output=task_config['create_action_plan']['expected_output'],
#     agent=action_planner
# )

implement_gamification = Task(
    description=task_config['implement_gamification']['description'],
    expected_output=task_config['implement_gamification']['expected_output'],
    agent=progress_tracker
)



crew = Crew(
    agents=[location_researcher,
            # environmental_expert,
            # action_planner,
            progress_tracker],
    tasks=[
        research_task,
        # analyze_user_input,
        # create_action_plan,
        implement_gamification
    ],
    process=Process.sequential,
    # memory=True,
    # verbose=True,
    cache=True
)


def interactive_session():
    progress_report = []
    is_first_submission = True
    user_points = 0

    print("Welcome to the Environmental AI Coach! Let's improve your environmental impact.")
    print("Type your message and I'll provide analysis and feedback. Enter 'quit()' to exit.")

    location = input("Kindly provide your location for personalized suggestions: ").strip()

    while True:
        user_input = input("Please tell me your lifestyle, interests, and environmental goals: ").strip()
        
            
        if user_input.lower() == "quit()" or location.lower() == "quit()":
            print("\nThank you for using the Environmental AI Coach. Good luck!")
            break
        

        if not user_input or not location:
            print("Input cannot be empty. Please provide the required information to proceed.")
            continue

        try:
            current_turn = len(progress_report) + 1
            inputs = {"user_input": user_input, "location": location}
            
            # Process input through the crew
            result = crew.kickoff(inputs)
            
            # Retrieve outputs for different steps
            research = research_task.output.raw
            gamification = implement_gamification.output.raw

            print(f"Personalized Environmental Contribution: {research}")
            
            # Handle quiz responses and update points
            if "---QUIZ---" in gamification and "---END---" in gamification:
                print("\n=== Environmental Quiz Challenge ===")
                
                # Extract quiz content
                quiz_content = gamification.split("---QUIZ---")[1].split("---END---")[0].strip()
                
                # Parse question, options, and answer
                question = ""
                options = []
                correct_answer = ""
                
                for line in quiz_content.split('\n'):
                    line = line.strip()
                    if line.startswith('QUESTION:'):
                        question = line.replace('QUESTION:', '').strip()
                    elif line.startswith('a)') or line.startswith('b)') or line.startswith('c)') or line.startswith('d)'):
                        options.append(line)
                    elif line.startswith('ANSWER:'):
                        correct_answer = line.replace('ANSWER:', '').strip().lower()

                # Present question to user
                print(f"\n{question}")
                for option in options:
                    print(option)
                
                user_answer = input("Your answer: ").lower().strip()
                if user_answer == correct_answer:
                    user_points += 1
                    print(f"Correct! You earned 1 point. Total points: {user_points}")
                else:
                    print(f"Not quite. The correct answer was: {correct_answer}")
                    print(f"Current points: {user_points}")

            # Update progress report
            progress_report.append({
                'current_turn': current_turn,
                'user_input': user_input,
                'analysis': research_task,
                'points': user_points
            })

        except Exception as e:
            print(f"An error occurred: {e}")
            continue
