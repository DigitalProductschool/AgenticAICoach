from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.cv_reviewer.tools.github_tool import GithubRepoTool
from src.schemas.cv_output import CVReview

@CrewBase
class CvReviewAiCrew():
	"""CvReviewAi crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def cv_analyst(self) -> Agent:
		"""
		Loads the CV Analyst agent from the YAML config.
		"""
		return Agent(
			config=self.agents_config['cv_analyst'],
			verbose=True
		)

	@agent
	def tech_talent_assessor(self) -> Agent:
		"""
		Loads the Tech Talent Assessor agent from the YAML config
		and equips it with the GitHub analysis tool.
		"""
		return Agent(
			config=self.agents_config['tech_talent_assessor'],
			tools=[GithubRepoTool()],  # Assign the custom tool here
			verbose=True
		)

	@agent
	def career_strategist(self) -> Agent:
		"""
		Loads the Career Strategist agent from the YAML config.
		"""
		return Agent(
			config=self.agents_config['career_strategist'],
			verbose=True
		)

	# Define the tasks that the crew will perform
	@task
	def cv_analysis_task(self) -> Task:
		"""
		Loads the CV analysis task from the YAML config.
		This task will be performed by the cv_analyst agent.
		"""
		return Task(
			config=self.tasks_config['cv_analysis_task'],
		)

	@task
	def repo_review_task(self) -> Task:
		"""
		Loads the repository review task from the YAML config.
		This task will be performed by the tech_talent_assessor agent.
		"""
		return Task(
			config=self.tasks_config['repo_review_task'],
		)

	@task
	def career_strategy_task(self) -> Task:
		"""
		Loads the final career strategy task from the YAML config.
		This task uses the outputs of the previous two tasks as its context.
		"""
		return Task(
			config=self.tasks_config['career_strategy_task'],
			context=[self.cv_analysis_task(), self.repo_review_task()],
			output_pydantic=CVReview
		)

	# Define the crew that will orchestrate the agents and tasks
	@crew
	def crew(self) -> Crew:
		"""Creates and configures the CV Review AI crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=2,
		)