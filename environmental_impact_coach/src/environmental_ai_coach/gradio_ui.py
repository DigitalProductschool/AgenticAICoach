import gradio as gr
from crew import crew, implement_gamification, research_task
from crew import Crew, Task, Process
import re
import os
# Function to process user input

os.environ["PORT"] = "8080" 

def process_input(location, user_input, user_points=0):
    if not location or not user_input:
        return "Error: Both fields are required.", "", "", "", user_points, "", ""

    try:
        inputs = {"user_input": user_input, "location": location}
        result = crew.kickoff(inputs)

        # Retrieve outputs for different steps
        research = research_task.output.raw
        gamification = implement_gamification.output.raw

        # Extract PM2.5 and PM10 values
        pm25 = "N/A"
        pm10 = "N/A"
        for line in research.split('\n'):
            if "PM2.5" in line:
                matches = re.findall(r"PM2.5:?\s*([-+]?\d*\.?\d+)", line)
                if matches:
                    pm25 = matches[0]
            if "PM10" in line:
                matches = re.findall(r"PM10:?\s*([-+]?\d*\.?\d+)", line)
                if matches:
                    pm10 = matches[0]

        quiz_question = ""
        options = []
        correct_answer = ""

        if "---QUIZ---" in gamification and "---END---" in gamification:
            quiz_content = gamification.split("---QUIZ---")[1].split("---END---")[0].strip()
            for line in quiz_content.split('\n'):
                line = line.strip()
                if line.startswith('QUESTION:'):
                    quiz_question = line.replace('QUESTION:', '').strip()
                elif line.startswith(('a)', 'b)', 'c)', 'd)')):
                    options.append(line)
                elif line.startswith('ANSWER:'):
                    correct_answer = line.replace('ANSWER:', '').strip().lower()

        return research, quiz_question, options, user_points, correct_answer, pm25, pm10

    except Exception as e:
        return f"Error occurred: {e}", "", "", "", user_points, "", "", ""

# Function to handle quiz answer
def handle_quiz_answer(user_answer, correct_answer, user_points):
    if user_answer.lower() == correct_answer:
        user_points += 1
        feedback = f"Correct! You earned 1 point. Total points: {user_points}"
    else:
        feedback = f"Incorrect. The correct answer was '{correct_answer}'. Total points: {user_points}"
    return feedback, user_points

# Define the Gradio interface
def gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# 🌱 Environmental AI Coach")
        gr.Markdown("Welcome to your personalized environmental coach! Let's get started by entering your location and telling me about your lifestyle and goals.")
        
        # Introduction to User Input
        with gr.Row():
            location = gr.Textbox(label="📍 Location", placeholder="Enter your location, eg: Munich, Germany", interactive=True)
            user_input = gr.Textbox(label="💡 Lifestyle, Goals or any other message", placeholder="Describe your interests, and environmental goals or any other message eg: I am 30, Love to go hiking", interactive=True)
        
        # Submit Button
        submit_button = gr.Button("🚀 Get Personalized Insights")
        user_points = gr.Number(value=0, visible=False)
        correct_answer = gr.Textbox(visible=False)

        # Display Results (initially hidden)
        with gr.Row(visible=False) as result_section:
            gr.Markdown("### 📝 Your Personalized Recommendations")
            research_output = gr.Textbox(label="Personalized Recommendations based on your location", interactive=False)
        
        # Quiz Section (initially hidden)
        with gr.Row(visible=False) as quiz_section:
            gr.Markdown("### 🎯 Quiz Time! Test your knowledge.")
            quiz_question_output = gr.Textbox(label="Quiz Question", interactive=False)
            options_output = gr.Textbox(label="Options", interactive=False)
            quiz_answer = gr.Textbox(label="Your Answer", placeholder="Enter a, b, c, or d", interactive=True)
            quiz_submit_button = gr.Button("Submit Quiz Answer")
            quiz_feedback = gr.Textbox(label="Quiz Feedback", interactive=False)

        # Add Air Quality Section (initially hidden)
        with gr.Row(visible=False) as air_quality_section:
            gr.Markdown("### 🌬️ Current Air Quality")
            with gr.Column():
                pm25_output = gr.Textbox(label="PM2.5", interactive=False)
                pm10_output = gr.Textbox(label="PM10", interactive=False)

        # Click submit to process user input
        submit_button.click(
            process_input,
            inputs=[location, user_input, user_points],
            outputs=[research_output, quiz_question_output, options_output, user_points, correct_answer, pm25_output, pm10_output],
            show_progress=True  # Show a progress bar
        )

        # Once the results are ready, show the results and quiz
        submit_button.click(
            lambda: result_section.update(visible=True),
            outputs=[result_section]
        )

        # Show quiz section after results
        submit_button.click(
            lambda: quiz_section.update(visible=True),
            outputs=[quiz_section]
        )

        # Show air quality section after results
        submit_button.click(
            lambda: air_quality_section.update(visible=True),
            outputs=[air_quality_section]
        )

        # Handle quiz submission
        quiz_submit_button.click(
            handle_quiz_answer,
            inputs=[quiz_answer, correct_answer, user_points],
            outputs=[quiz_feedback, user_points]
        )

    return demo


# Launch the Gradio interface
if __name__ == "__main__":
    ui = gradio_ui()
    ui.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 8080)),
        share=True,
        auth=None  # Set this to None for public access or implement authentication
    )
