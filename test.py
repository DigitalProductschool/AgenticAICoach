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
        # Use chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the chat model
            messages=[
                {"role": "system", "content": "You are an assistant that rewrites text to make it more confident."},
                {"role": "user", "content": f"Rewrite the following text to sound more confident:\n\n{input_text}"}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        request_count += 1  # Increment request count

        # Return the confident text
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
user_input = "Sorry, but could please explaint this to me again"
output = generate_confident_text(user_input, max_requests=5)
print(output)
