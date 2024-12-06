from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import CSVSearchTool, FileReadTool

import tempfile
from chromadb import Client
from chromadb.config import Settings
# Uncomment the following line to use an example of a custom tool
# from ai_community_matchmaker.tools.custom_tool import MyCustomTool
# Uncomment the following line to use an example of a knowledge source
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

_chroma_client = None  # Global variable for Chroma client

def reset_chroma_client():
    """
    Resets the shared Chroma client to ensure no residual state.
    """
    global _chroma_client
    _chroma_client = None

def get_in_memory_chroma_client():
    """
    Creates or reuses a singleton Chroma client.
    """
    global _chroma_client
    if _chroma_client is None:
        temp_dir = tempfile.mkdtemp()
        _chroma_client = Client(Settings(persist_directory=temp_dir))
    return _chroma_client

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AiCommunityMatchmaker():
	"""AiCommunityMatchmaker crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	# Initialize tools
	chroma_client = get_in_memory_chroma_client()

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def cofounder_search_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['cofounder_search_agent'],
			tools=[CSVSearchTool(db_client=self.chroma_client),FileReadTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation=False
		)

	@agent
	def mentor_search_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['mentor_search_agent'],
			tools=[CSVSearchTool(db_client=self.chroma_client),FileReadTool()],
			verbose=True,
			allow_delegation=False
		)
	
	@agent
	def community_matching_coach(self) -> Agent:
		return Agent(
			config=self.agents_config['community_matching_coach'],
			tools=[CSVSearchTool(db_client=self.chroma_client),FileReadTool()],
			verbose=True,
			allow_delegation=False
		)

	@task
	def cofounder_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['cofounder_search_task'],
			agent=self.cofounder_search_agent()
		)
	
	@task
	def mentor_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['mentor_search_task'],
			agent=self.mentor_search_agent()
		)

	@task
	def report_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['report_generation_task'],
			agent=self.community_matching_coach(),
			context=[self.cofounder_search_task(),self.mentor_search_task()],
			output_file='output/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiCommunityMatchmaker crew"""
		# You can add knowledge sources here
		# knowledge_path = "user_preference.txt"
		# sources = [
		# 	TextFileKnowledgeSource(
		# 		file_path="knowledge/user_preference.txt",
		# 		metadata={"preference": "personal"}
		# 	),
		# ]

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			# knowledge_sources=sources, # In the case you want to add knowledge sources
		)
