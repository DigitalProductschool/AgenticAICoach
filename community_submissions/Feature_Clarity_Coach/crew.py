from crewai import Agent, Crew, Task, Flow
from crewai.flow.flow import listen, start, router
from pydantic import BaseModel
from utils.llm_assistant import llm
from utils.format import format_chat_history
from utils.enable_logging import logger
import yaml
import json

with open("config/agents.yaml", "r") as f:
    agent_configs = yaml.safe_load(f)

with open("config/tasks.yaml", "r") as f:
    task_configs = yaml.safe_load(f)


class UserState(BaseModel):
    phase: str = "core_problem"
    chat_history: list[dict[str, str]] = []
    user_input: str = ""
    phase_summaries: dict[str, str] = {
        "core_problem": "",
        "core_value": "",
        "brainstorm_solution": "",
        "validate": ""
    }


phase_reasoning = ''


class FeatureClarityCoach(Flow[UserState]):

    @start()
    def conversation_phase(self):
        # Force 'stay' if user expresses uncertainty
        uncertainty_keywords = ["i don't know", "you suggest", "not sure", "help me decide", "what do you think"]
        if any(keyword in self.state.user_input.lower() for keyword in uncertainty_keywords):
            logger.info(f"User expressed uncertainty — forcing stay.")
            return self.state.phase

        formatted_history = format_chat_history(self.state.chat_history)
        agent = Agent(config=agent_configs["routing_agent"], verbose=True)
        task_config = task_configs["routing_task"].copy()
        if 'description' in task_config:
            task_config['description'] = task_config['description'] \
                .replace('{{ chat_history }}', formatted_history) \
                .replace('{user_input}', self.state.user_input) \
                .replace('{phase}', self.state.phase) \
                .replace('{current_phase_summary}', self.state.phase_summaries[self.state.phase])
        task = Task(config=task_config, agent=agent)
        crew_instance = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
            memory=False,
            llm=llm,
        )

        result = crew_instance.kickoff({
            "chat_history": formatted_history,
            "user_input": self.state.user_input,
            "phase": self.state.phase,
            "current_phase_summary": self.state.phase_summaries[self.state.phase]
        })
        logger.info(f"Phase before decision: {self.state.phase}")

        phase_order = ["core_problem", "core_value", "brainstorm_solution", "validate", "complete"]
        current_index = phase_order.index(self.state.phase)

        try:
            raw_output = result.output if hasattr(result, "output") else str(result)
            result_json = json.loads(raw_output)
            logger.info(f"Conversation Coordinator JSON response: {result_json}")

            action = result_json.get("action", "stay")

            # Save phase summary before advancing
            phase_summary = result_json.get("phase_summary", "")

            global phase_reasoning
            phase_reasoning = result_json.get("reason", "")
            self.state.phase_summaries[self.state.phase] = phase_summary

            if action == "advance" and current_index < len(phase_order) - 1:
                new_phase = phase_order[current_index + 1]
                logger.info(f"Phase advanced: {self.state.phase} → {new_phase}")
                self.state.phase = new_phase
        except Exception as e:
            logger.info(f"Error parsing LLM output: {e}")
            logger.info(f"❗Forcing stay due to invalid LLM response.")
        return self.state.phase

    @router(conversation_phase)
    def assign_agent(self):
        logger.info(f"Phase after decision: {self.state.phase}")
        phase_to_agent = {
            "core_problem": "core_problem_agent",
            "core_value": "core_value_agent",
            "brainstorm_solution": "brainstorm_solution_agent",
            "validate": "validate_agent"
        }

        if self.state.phase == "complete":
            logger.info(f"Flow complete! No agent needed.")
            return None

        return phase_to_agent.get(self.state.phase, "core_problem_agent")

    def run_agent(self, agent_key):
        logger.info(f"Conversation handled by agent: {agent_key}")
        formatted_history = format_chat_history(self.state.chat_history)
        agent = Agent(config=agent_configs[agent_key], verbose=True)

        task_config = task_configs["coaching_task"].copy()
        if 'description' in task_config:
            desc = task_config['description']
            task_config['description'] = desc.replace('{{ chat_history }}', formatted_history) \
                                             .replace('{user_input}', self.state.user_input) \
                                             .replace('{phase_summary}', self.state.phase_summaries[self.state.phase])\
                                             .replace('{reason}', phase_reasoning)

        task = Task(config=task_config, agent=agent)
        crew_instance = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
            memory=False,
            llm=llm,
        )
        return crew_instance.kickoff({
            "chat_history": formatted_history,
            "user_input": self.state.user_input,
        })

    @listen("core_problem_agent")
    def run_core_problem_agent(self):
        return self.run_agent("core_problem_agent")

    @listen("core_value_agent")
    def run_core_value_agent(self):
        return self.run_agent("core_value_agent")

    @listen("brainstorm_solution_agent")
    def run_brainstorm_solution_agent(self):
        return self.run_agent("solution_agent")

    @listen("validate_agent")
    def run_validate_agent(self):
        return self.run_agent("validation_agent")


if __name__ == "__main__":
    user = UserState()
    coach = FeatureClarityCoach(initial_state=user)
    print("AI Feature Clarity Coach is ready! Let's help you build something amazing.")
    print("What brings you here today?")

    for _ in range(20):
        user_input = input("\nYou: ")
        user.user_input = user_input

        response = coach.kickoff(user.model_dump())
        # Sync your local `user` object with the updated state
        user.phase = coach.state.phase

        if user.phase == "complete":
            response_text = "You've completed the Feature Clarity Coaching process! You're ready to build!"
        else:
            response_text = getattr(response, "output", str(response))

        print(f"\nCoach: {response_text}")
        user.chat_history.append({"user": user_input, "assistant": response_text})
