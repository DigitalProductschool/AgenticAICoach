from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
import yaml

def has_job_description(inputs) -> bool:
    """Check if a job description is provided"""
    return bool(inputs.get("jd_text", "").strip())

class CVReviewCrew:
    """Crew to review CVs and generate feedback reports"""

    def __init__(self, inputs):
        self.inputs = inputs
        with open('./src/cv_reviewer/config/agents.yaml', 'r') as agents_file:
            self.agents_config = yaml.safe_load(agents_file)
        with open('./src/cv_reviewer/config/tasks.yaml', 'r') as tasks_file:
            self.tasks_config = yaml.safe_load(tasks_file)
        
        self.task_outputs = {}

        """Create agents for the crew"""
        self.cv_analyzer = Agent(
            config=self.agents_config['cv_analyzer'],
            verbose=True,
            allow_delegation=False
        )
            
        self.jd_processor = Agent(
            config=self.agents_config['jd_processor'],
            verbose=True,
            allow_delegation=False
        )
            
        self.report_generator = Agent(
            config=self.agents_config['report_generator'],
            verbose=True,
            allow_delegation=False
        )
    
    def create_tasks(self):
        """Create and organize tasks for the crew."""
        jd_text = self.inputs.get("jd_text", "").strip()

        if jd_text:
            choice = Task(
                config=self.tasks_config['analyze_job_description'],
                agent=self.jd_processor
            )
            relevance = Task(
                config=self.tasks_config['analyze_cv_relevance_w_jd'],
                agent=self.cv_analyzer,
                context=[choice],
                callback=self.task_callback('relevance')
            )
        else:
            choice = Task(
                config=self.tasks_config['infer_industry_from_cv'],
                agent=self.cv_analyzer
            )
            relevance = Task(
                config=self.tasks_config['analyze_cv_relevance_wo_jd'],
                agent=self.cv_analyzer,
                context=[choice],
                callback=self.task_callback('relevance')
            )

        structure = Task(
            config=self.tasks_config['analyze_cv_structure'],
            agent=self.cv_analyzer,
            callback=self.task_callback('structure')
        )

        language = Task(
            config=self.tasks_config['analyze_cv_language'],
            agent=self.cv_analyzer,
            callback=self.task_callback('language')
        )

        power = Task(
            config=self.tasks_config['analyze_cv_power'],
            agent=self.cv_analyzer,
            callback=self.task_callback('power')
        )

        feedback = Task(
            config=self.tasks_config['generate_feedback_report'],
            agent=self.report_generator,
            context=[structure, relevance, language, power],
            callback=self.task_callback('report')
        )

        self.tasks_list = [choice, structure, relevance, language, power, feedback]
    
    def task_callback(self, task_name):
        """
        Creates a callback function that includes the task name.
        :param task_name: The name of the task being executed.
        :return: A callback function.
        """
        def callback(output):
            """
            Callback function to handle task output.
            :param output: The output of the task.
            """
            # Store the output with the task name
            self.task_outputs[task_name] = output.raw_output

        return callback

    @crew
    def crew(self) -> Crew:
        """Creates the CV review crew"""
        self.create_tasks()
        return Crew(
            agents=[self.cv_analyzer, self.jd_processor, self.report_generator],
            tasks=self.tasks_list,
            process=Process.sequential,
            verbose=2
        )
