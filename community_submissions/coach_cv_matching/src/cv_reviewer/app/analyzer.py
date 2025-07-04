import os
from io import BytesIO
from cv_reviewer.tools.file_parser import FileParser
from cv_reviewer.crew import CVReviewCrew

def analyze_cv(cv_filename: str, job_description: str):
    """
    Parse and analyze a CV file using FileParser and CVReviewCrew.
    Automatically save analysis outputs to files.

    :param cv_filename: The original filename of the uploaded CV.
    :param job_description: The job description provided by the user (optional).
    :return: A dictionary containing task outputs.
    """
    # Parse the CV using FileParser
    file_parser = FileParser(cv_filename)
    cv_text = file_parser.parse()

    # Initialize Crew inputs
    inputs = {
        "jd_text": job_description or "",  # Allow job_description to be empty
        "cv_text": cv_text,
    }
    cv_crew = CVReviewCrew(inputs=inputs)
    result = cv_crew.crew().kickoff(inputs=inputs)

    # Ensure the output directory exists
    output_dir = "./cache/output"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over Crew task outputs and save them as individual files
    for task_name, task_output in cv_crew.task_outputs.items():
        # Create a safe filename for each task output
        file_name = f"{task_name}.md"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(task_output)

    return result
