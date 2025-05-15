import subprocess
import streamlit as st

subprocess.run(["python", "community_submissions\confidence_coach_ai\confidence_template\crewapi.py"],check=True)

subprocess.run(["streamlit", "run", "community_submissions\confidence_coach_ai\confidence_template\crew_app.py"], check=True)