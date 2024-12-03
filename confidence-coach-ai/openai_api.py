import os
from dotenv import load_dotenv
import openai
import json
from fastapi import HTTPException

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def generate_confident_text(input_text, max_requests=100, request_count=0):
    """
    Generates confident text from user input using OpenAI chat completion.
    """
    if request_count >= max_requests:
        return "Request limit reached. Please try again later."

    try:
        prompt = f"""
        Analyze the following text and determine whether it exhibits low-confidence communication. If so, identify specific phrases or patterns and suggest how they can be improved to sound more assertive. If the text is already confident, acknowledge that and provide positive reinforcement. 
        Highlight the areas of improvement and suggest actionable replacements. Additionally, provide a confidence score (1 to 5) for each section or phrase, and overall feedback to improve confidence in the communication.

        Example input: "I just think that maybe we should try this."
        Example output:
        - Highlight: "I just think that maybe"
        - Suggestion: "I recommend we try this."
        - Confidence Score: 2
        - Overall Feedback: Try using more assertive language.

        Input text: {input_text}

        Respond ONLY with valid JSON format:
        {{
            "highlights": [
                {{"low_confidence_phrase": "<phrase>", "suggestion": "<suggestion>"}}
            ],
            "confidence_score": <score>,
            "overall_feedback": "<feedback>"
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI Confidence Coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Return the confident text
        # Extract the model's response content
        raw_response = response['choices'][0]['message']['content']
        print(raw_response)

        # Parse the response content as JSON
        analysis = json.loads(raw_response)
        return analysis

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing OpenAI response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {e}")

# Example usage
# user_input = "Why don't you just do it?"
# output = generate_confident_text(user_input, max_requests=5)
# print(output)
