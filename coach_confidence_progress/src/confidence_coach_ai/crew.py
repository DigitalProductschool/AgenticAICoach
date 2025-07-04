from crewai import Agent, Task, Crew, Process
from tools.custom_tool import AudioTranscriberTool
import os
import yaml
import requests
import tempfile
import os.path

# Load config
with open('config/agents.yaml', 'r') as file:
    agent_config = yaml.safe_load(file)

with open('config/tasks.yaml', 'r') as file:
    task_config = yaml.safe_load(file)

# Define agents

analyzer = Agent(
    role=agent_config["analyzer"]["role"],
    goal=agent_config["analyzer"]["goal"],
    backstory=agent_config["analyzer"]["backstory"],
    memory=True,
    cache=False,
)

coach = Agent(
    role=agent_config["coach"]["role"],
    goal=agent_config["coach"]["goal"],
    backstory=agent_config["coach"]["backstory"],
    memory=True,
    cache=False
)


progress_reporter = Agent(
    role="Progress Reporter",
    goal=agent_config["progress_reporter"]["goal"],
    backstory=agent_config["progress_reporter"]["backstory"],
    memory=True,
    cache=False
)

summarizer = Agent(
    role="Summarizer",
    goal=agent_config["summarizer"]["goal"],
    backstory=agent_config["summarizer"]["backstory"],
    memory=True,
    cache=False
)


analyze_communication_task = Task(
    description=task_config["analyze_communication_task"]["description"],
    expected_output=task_config["analyze_communication_task"]["expected_output"],
    agent=analyzer,
    human_input=False  # Change to False since we're passing input via context
)

provide_feedback_task = Task(
    description=task_config["provide_feedback_task"]["description"],
    expected_output=task_config["provide_feedback_task"]["expected_output"],
    agent=coach
)

summarize_analyzer_output_task = Task(
    description=task_config["summarize_analyzer_output_task"]["description"],
    expected_output=task_config["summarize_analyzer_output_task"]["expected_output"],
    agent=summarizer
)

create_progress_report_task = Task(
    description=task_config["create_progress_report_task"]["description"],
    expected_output=task_config["create_progress_report_task"]["expected_output"],
    agent=progress_reporter
)


crew = Crew(
    agents=[analyzer, coach, summarizer],
    tasks=[
        analyze_communication_task,
        provide_feedback_task,
        summarize_analyzer_output_task
    ],
    process=Process.sequential,
    # memory=True,
    # verbose=True,
    cache=False
)

def download_audio_from_url(url):
    """Downloads audio file from URL and saves it to a temporary file"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get the file extension from the URL
        file_extension = os.path.splitext(url)[1]
        if not file_extension:
            file_extension = '.mp3'  # Default to mp3 if no extension found
            
        # Create temporary file with the correct extension
        temp_file = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
        with temp_file as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return temp_file.name
    except Exception as e:
        raise Exception(f"Failed to download audio file: {str(e)}")

def interactive_session():
    progress_report = []  # Keeps track of all user inputs and feedback
    is_first_submission = True  # Track if it's the first submission

    print("Welcome to the Confidence Coach! Let's improve your communication skills.")
    print("Type your message or audio file URL and I'll provide analysis and feedback. Enter 'quit()' to exit.")

    while True:
        user_input = input("\nYour message or audio file path/URL: ").strip()
        
        # Handle audio input
        if user_input.startswith(('http://', 'https://')):
            try:
                temp_file_path = download_audio_from_url(user_input)
                transcriber = AudioTranscriberTool()
                user_input = transcriber.run(temp_file_path)
                os.unlink(temp_file_path)  # Clean up temporary file
            except Exception as e:
                print(f"Error processing audio URL: {e}")
                continue
        elif user_input.lower().endswith((".mp3", ".wav")):
            transcriber = AudioTranscriberTool()
            user_input = transcriber.run(user_input)

        if user_input.lower() == "quit()":
            print("\nThank you for using the Confidence Coach. Keep practicing, and good luck!")
            break

        if not user_input:
            print("Input cannot be empty. Please provide a valid message.")
            continue

        try:
            current_turn = len(progress_report) + 1
            inputs = {"text": user_input, "is_first_submission": is_first_submission}
            
            # Process input through the crew
            result = crew.kickoff(inputs)
            
            # Retrieve outputs for different steps
            analysis = analyze_communication_task.output.raw
            summary = summarize_analyzer_output_task.output.raw
            feedback = provide_feedback_task.output.raw
            
            # Store the results in the progress report
            progress_report.append({
                "turn": current_turn,
                "input": user_input,
                # "analysis": analysis,
                "summary": summary,
                # "feedback": feedback
            })

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        print(f"\n--- Turn {current_turn} ---")
        print(f"Analysis: {analysis}")
        # print(f"Summary: {summary}")
        print(f"Feedback: {feedback}")

        if is_first_submission:
            print("\nGreat start! Let's work on refining this further.")
            is_first_submission = False
        else:
            print("\nKeep it up! You're improving with every attempt.")

        if input("\nWould you like to see your progress report so far? (yes/no): ").strip().lower() == "yes":
            print("\n--- Progress Report ---")
            progress_crew = Crew(
                agents=[progress_reporter],
                tasks=[create_progress_report_task],
                process=Process.sequential,
                memory=True,
                verbose=True,
                cache=False
            )
            progress_report_result = progress_crew.kickoff(inputs={"progress_data": progress_report})
            print(progress_report_result)

