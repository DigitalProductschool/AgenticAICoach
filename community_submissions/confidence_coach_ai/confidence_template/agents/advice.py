from crewai import Agent
import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

load_dotenv()

class ConfidenceAdviceAgent:
    def __init__(self, training_file='../training/advice_examples.json'):
        self.training_file = training_file
        self.examples_content = self._load_examples() # load examples content

        # Initialize the Gemini model
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)
        
        self.model = genai.GenerativeModel(         # Call for model
            model_name="gemini-2.0-flash",  
            generation_config={
                "temperature": 1,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )

        self.instructions = self._create_instructions()

    def _load_examples(self):
        """Loads examples from the JSON file."""
        try:
            with open(self.training_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.training_file}")
            return ""

    def _create_instructions(self):     # Creates instrcutions / original prompt for the agent
        """Creates the instructions for the agent with examples."""
        return f"""You are a seasoned confidence coach with a proven track record of helping people build self-assurance. Based on the following examples, provide specific advice on how to change one's mentality/attitude to be more confident. Ask questions if you need to, and always validate the user's feelings.
        The examples are provided from the AI Engineer. While the text is from the customer. So use the examples but don't mention that the examples exist to the customer. Also if you'll use any of the examples word for word then make sure you eliminate any grammatical mistakes.

Examples:
{self.examples_content}

Recognize whether the text is part of a conversation or they're just telling you what they feel, usually if they're telling you what they feel the text will start with "I feel". Now, provide advice for the following text:"""

    def create_agent(self):
        prompt = self.instructions
        return Agent(
            role='Confidence Advisor',
            goal='Give specific advice on how to change one\'s mentality/attitude to be more confident.',
            backstory="You are a seasoned confidence coach with a proven track record of helping people build self-assurance.",
            allow_delegation=False,
            verbose=True,
            instructions=prompt,
            tools=[]
        )

    async def give_advice_async(self, text):        # Main Method
        """Asynchronous method to give advice with timeout handling"""
        prompt = f"{self.instructions}\nText: {text}\nAdvice:"
        try:
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(
                    prompt, 
                    request_options={"timeout": 40}  # timeout in seconds
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error during advice generation: {e}"

    def give_advice(self, text):
        """Synchronous wrapper for the async method"""
        return asyncio.run(self.give_advice_async(text))