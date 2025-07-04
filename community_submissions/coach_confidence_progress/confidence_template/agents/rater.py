from crewai import Agent
import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio
import json
from typing import List, Dict, Any

load_dotenv()

class ConfidenceRaterAgent:
    def __init__(self, training_file='../training/rater_examples.json', scoring_table_file='../training/rating_table.txt'):
        self.training_file = training_file
        self.scoring_table_file = scoring_table_file
        
        # Initialize Gemini model
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )

        self.examples_content = self._load_file_content(self.training_file)
        self.scoring_table_content = self._load_file_content(self.scoring_table_file)
        self.instructions = self._create_instructions()

    def _load_file_content(self, filepath):
        """Loads the content of a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return ""

    def _create_instructions(self):
        """Creates the instructions for the agent."""
        return f"""Analyze the text and assess the speaker's confidence level on a scale of 1 to 5. If there are multiple speakers rate each speaker. Focus on the context of every sentence and its intention as well.

Here is a confidence scoring table to guide you:
{self.scoring_table_content}

Here are some examples of text and their corresponding confidence ratings:
{self.examples_content}

Analyze the provided text and provide a confidence rating from 1 to 5:"""

    def create_agent(self):
        return Agent(
            role='Confidence Rater',
            goal='Rate a person\'s confidence level in a given text from 1 to 5.',
            backstory="You are an expert in analyzing text and assessing the speaker's confidence level. You have been trained on various examples of confident and unconfident speech.",
            allow_delegation=False,
            verbose=True,
            instructions=self.instructions,
            tools=[]
        )

    async def rate_confidence_async(self, text):
        """Asynchronous method to rate confidence with timeout handling"""
        full_prompt = f"{self.instructions}\nText: {text}\nRating (1-5):"
        try:
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(
                    full_prompt,
                    request_options={"timeout": 40}  # timeout in seconds
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error during rating: {e}"

    def rate_confidence(self, text):
        """Synchronous wrapper for the async method"""
        return asyncio.run(self.rate_confidence_async(text))
    
    async def analyze_multiple_ratings(self, ratings_data: List[Dict[str, Any]], ratings_data_2: List[Dict[str, Any]], ratings_data_3: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes multiple ratings and provides overall confidence assessment and improvement pointers.
        
        Args:
            ratings_data: List of dictionaries containing:
                - 'text': Original text
                - 'rating': Confidence rating (1-5)
                - 'analysis': Detailed rating analysis
        
        Returns:
            Dictionary containing:
                - 'average_rating': Overall confidence score
                - 'trend_analysis': Confidence trend over time
                - 'improvement_areas': Specific areas for improvement
                - 'confidence_breakdown': Detailed analysis by confidence level
        """
        try:
            # Prepare the analysis prompt
            analysis_prompt = f"""
            This is a history of a user's evolvement over time when it comes to their confidence ratings, do the following:
            1. Average confidence score
            2. Confidence trends (improving/declining/stable)
            3. Key improvement areas
            4. Actionable advice
            5. Patterns in high/low confidence moments
            
            Rating Data:
            First rating:  {json.dumps(ratings_data_3,indent=2)}
            Second rating: {json.dumps(ratings_data_2,indent=2)}
            Third rating: {json.dumps(ratings_data, indent=2)}
            
           
            
            Here is a confidence scoring table to guide you:
            {self.scoring_table_content}

            Here are some examples of text and their corresponding confidence ratings:
            {self.examples_content}

            provide reply in regular text
            Use this regular expression: Confidence Rating:\s*(\d)/5 to display the rating.
            
            """
            
            # Get the analysis from Gemini
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(
                    analysis_prompt,
                    request_options={"timeout": 60}
                )
            )
            
            return response.text.strip()
           
                
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}"
            }

    def analyze_multiple_ratings_sync(self, ratings_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synchronous wrapper for the async method"""
        return asyncio.run(self.analyze_multiple_ratings(ratings_data))