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
                context=[choice]
            )
        else:
            choice = Task(
                config=self.tasks_config['infer_industry_from_cv'],
                agent=self.cv_analyzer
            )
            relevance = Task(
                config=self.tasks_config['analyze_cv_relevance_wo_jd'],
                agent=self.cv_analyzer,
                context=[choice]
            )

        structure = Task(
            config=self.tasks_config['analyze_cv_structure'],
            agent=self.cv_analyzer
        )

        language = Task(
            config=self.tasks_config['analyze_cv_language'],
            agent=self.cv_analyzer
        )

        power = Task(
            config=self.tasks_config['analyze_cv_power'],
            agent=self.cv_analyzer
        )

        feedback = Task(
            config=self.tasks_config['generate_feedback_report'],
            agent=self.report_generator,
            context=[structure, relevance, language, power]
        )

        self.tasks_list = [choice, structure, relevance, language, power, feedback]

    @crew
    def crew(self) -> Crew:
        """Creates the CV review crew"""
        return Crew(
            agents=[self.cv_analyzer, self.jd_processor, self.report_generator],
            tasks=self.tasks_list,
            process=Process.sequential,
            verbose=2
        )
