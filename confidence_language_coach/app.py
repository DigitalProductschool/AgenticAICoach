import gradio as gr
import requests
import json

API_URL = "http://localhost:8000/analyze"  # Update if hosted elsewhere

def analyze_text(user_input):
    response = requests.post(API_URL, json={"user_text": user_input})
    if response.status_code == 200:
        result = response.json().get("result", {})
        # Extract all relevant sections from the response
        raw_result = result.get("raw", "")
        tasks_output = result.get("tasks_output", [])
        
        # Organize the results into different sections
        analysis_sections = {
            "Summary": raw_result,
            "Confidence Analysis": "",
            "Assertive Alternatives": "",
            "Confidence Evaluation": ""
        }
        
        # Map each task output to the appropriate section
        for task in tasks_output:
            if task.get("agent") == "Confidence Analyzer":
                analysis_sections["Confidence Analysis"] = task.get("raw", "")
            elif task.get("agent") == "Confidence Rewriter":
                analysis_sections["Assertive Alternatives"] = task.get("raw", "")
            elif task.get("agent") == "Confidence Reviewer":
                analysis_sections["Confidence Evaluation"] = task.get("raw", "")
        
        return [
            analysis_sections["Summary"],
            analysis_sections["Confidence Analysis"],
            analysis_sections["Assertive Alternatives"],
            analysis_sections["Confidence Evaluation"]
        ]
    return [
        f"Error {response.status_code}: {response.text}",
        "",
        "",
        ""
    ]

# Custom CSS for better styling
css = """
.tab-button {
    padding: 0.5em 1em;
    border-radius: 0.5em 0.5em 0 0 !important;
}
.tab-button.selected {
    background: #f0f0f0;
    font-weight: bold;
}
.output-section {
    border: 1px solid #e0e0e0;
    border-radius: 0 0.5em 0.5em 0.5em;
    padding: 1em;
    margin-top: -1px;
    background: #f0f0f0;
}
"""

# Create the interface with tabs
with gr.Blocks(css=css) as app:
    gr.Markdown("## AI Confidence Coach")
    gr.Markdown("This tool analyzes your communication for confidence and assertiveness.")
    
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                lines=5, 
                placeholder="Enter your text here...",
                label="Your Text"
            )
            analyze_btn = gr.Button("Analyze", variant="primary")
        
        with gr.Column():
            with gr.Tabs():
                with gr.TabItem("Summary", elem_classes="tab-button"):
                    summary_output = gr.Markdown(
                        label="Summary",
                        value="The analysis summary will appear here..."
                    )
                
                with gr.TabItem("Confidence Analysis", elem_classes="tab-button"):
                    analysis_output = gr.Markdown(
                        label="Confidence Analysis",
                        value="Detailed confidence analysis will appear here..."
                    )
                
                with gr.TabItem("Assertive Alternatives", elem_classes="tab-button"):
                    alternatives_output = gr.Markdown(
                        label="Assertive Alternatives",
                        value="More assertive alternatives will appear here..."
                    )
                
                with gr.TabItem("Confidence Evaluation", elem_classes="tab-button"):
                    evaluation_output = gr.Markdown(
                        label="Confidence Evaluation",
                        value="Confidence evaluation and suggestions will appear here..."
                    )
    
    # Handle the button click
    analyze_btn.click(
        fn=analyze_text,
        inputs=user_input,
        outputs=[
            summary_output,
            analysis_output,
            alternatives_output,
            evaluation_output
        ]
    )

if __name__ == "__main__":
    app.launch()