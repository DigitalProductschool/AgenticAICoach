import os
from cv_reviewer.crew import CVReviewCrew
from cv_reviewer.tools.file_parser import FileParser

def get_test_file(file_name):
    """
    Retrieves the absolute path of a test file located in the 'data' directory.
    :param file_name: Name of the test file.
    :return: Absolute path of the test file.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, "data", file_name)

def get_output_folder(folder_name):
    """
    Retrieves the absolute path of an output folder.
    :param folder_name: Name of the folder.
    :return: Absolute path of the output folder.
    """
    current_dir = os.path.dirname(__file__)
    output_folder = os.path.join(current_dir, "output", folder_name)
    os.makedirs(output_folder, exist_ok=True)  # Ensure folder exists
    return output_folder

def write_task_outputs(output_folder, task_outputs):
    """
    Writes the outputs of tasks into separate markdown files.
    :param output_folder: Path to the output folder.
    :param task_outputs: Dictionary of task names and their outputs.
    """
    for task_name, output in task_outputs.items():
        file_name = f"{task_name}.md"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)

def test_crew_with_jd():
    """
    Tests the execution of CVReviewCrew with a provided Job Description.
    """
    # Parse the sample CV file
    cv_file_path = get_test_file("sample_cv.docx")
    parser = FileParser(cv_file_path)
    cv_text = parser.parse()

    # Load the sample Job Description
    jd_file_path = get_test_file("sample_jd.txt")
    with open(jd_file_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # Create inputs for the crew
    inputs = {
        "jd_text": jd_text,
        "cv_text": cv_text
    }

    # Initialize the crew and execute
    cv_crew = CVReviewCrew(inputs=inputs)
    crew_instance = cv_crew.crew()
    result = crew_instance.kickoff(inputs=inputs)

    # Write individual task outputs
    output_folder = get_output_folder("test_w_jd")
    write_task_outputs(output_folder, cv_crew.task_outputs)

    # Ensure result is not empty
    assert result, "Crew execution with JD did not produce any results."

def test_crew_without_jd():
    """
    Tests the execution of CVReviewCrew without a provided Job Description.
    """
    # Parse the sample CV file
    cv_file_path = get_test_file("sample_cv.docx")
    parser = FileParser(cv_file_path)
    cv_text = parser.parse()

    # Create inputs for the crew
    inputs = {
        "jd_text": "",  # No job description provided
        "cv_text": cv_text
    }

    # Initialize the crew and execute
    cv_crew = CVReviewCrew(inputs=inputs)
    crew_instance = cv_crew.crew()
    result = crew_instance.kickoff(inputs=inputs)

    # Write individual task outputs
    output_folder = get_output_folder("test_wo_jd")
    write_task_outputs(output_folder, cv_crew.task_outputs)

    # Ensure result is not empty
    assert result, "Crew execution without JD did not produce any results."
