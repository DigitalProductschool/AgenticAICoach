import os
from dotenv import load_dotenv
import openai

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
        Analyze the following text for low-confidence cues such as hedging, excessive apologizing, passive voice, and minimizing phrases. 
        Highlight the areas of improvement and suggest actionable replacements. Additionally, provide a confidence score (1 to 5) 
        for each section or phrase, and overall feedback to improve confidence in the communication.

        Example input: "I just think that maybe we should try this."
        Example output:
        - Highlight: "I just think that maybe"
        - Suggestion: "I recommend we try this."
        - Confidence Score: 2/5
        - Overall Feedback: Try using more assertive language.

        Input text: {input_text}

        Provide your analysis as a structured JSON object.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI Confidence Coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Return the confident text
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
user_input = "Could you explain this sentence?"
output = generate_confident_text(user_input, max_requests=5)
print(output)
