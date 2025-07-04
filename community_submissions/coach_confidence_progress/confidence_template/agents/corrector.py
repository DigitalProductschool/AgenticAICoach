from crewai import Agent
import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

class ConfidenceCorrectorAgent:
    def __init__(self, training_file='../training/corrector_examples.json'):
        self.training_file = training_file
        self.examples = self._load_and_format_examples()
        
        # Initialize Gemini model
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 8192,
            }
        )

        self.prompt = f"""Identify the following text and help me phrase it in a better way so I sound more confident.
Also identify which parts of the text falls under which categories: Hedging, Minimizing Language, Passive Voice, Discouraging Language and Excessive Apologizing.
I want the response in markdown format.

Use these examples as reference to know how to rephrase sentences:
{self.examples}.


"""

    def _load_and_format_examples(self):
        """Loads examples from the JSON file and formats them for the prompt."""
        try:
            with open(self.training_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {self.training_file}")
            return ""
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.training_file}")
            return ""

        formatted_examples = ""
        for category, examples in data.items():
            formatted_examples += f"Category: {category}\n"
            for example in examples:
                formatted_examples += (
                    f"  Input: {example['input']}\n"
                    f"  Recommendation: {example['output']['recommendation']}\n"
                    f"  Context: {example['output']['context']}\n\n"
                )
        return formatted_examples

    def create_agent(self):
        return Agent(
            role='Confidence Corrector',
            goal='Give recommendations on how to phrase things differently so the person sounds more confident.',
            backstory="You are a skilled editor with a keen ear for language and a focus on enhancing confidence in communication.",
            allow_delegation=False,
            verbose=True,
            instructions=self.prompt,
            tools=[]
        )

    async def correct_text_async(self, text):
        """Asynchronous method to correct text with timeout handling"""
        full_prompt = f"{self.prompt}\nText: {text}\nConfident Alternative:"
        try:
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(
                    full_prompt,
                    request_options={"timeout": 40}  # timeout in seconds
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error during correction: {e}"

    def correct_text(self, text):
        """Synchronous wrapper for the async method"""
        return asyncio.run(self.correct_text_async(text))