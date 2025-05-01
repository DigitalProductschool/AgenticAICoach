from crewai import LLM
import os
from dotenv import load_dotenv

def get_gemini_llm():
    load_dotenv()
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    print(llm)
    return llm
