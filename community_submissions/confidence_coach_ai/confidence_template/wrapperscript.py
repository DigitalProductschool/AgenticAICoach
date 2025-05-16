import subprocess
import sys
import time
from pathlib import Path
import toml 
import os



def run_api():
    """Run the API server"""
    try:
        # Using Popen so we can terminate it later
        return subprocess.Popen(
            [sys.executable, "community_submissions/confidence_coach_ai/confidence_template/crewapi.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(f"Failed to start API: {str(e)}", file=sys.stderr)
        sys.exit(1)

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "community_submissions/confidence_coach_ai/confidence_template/crew_app.py"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Streamlit app failed: {str(e)}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nStreamlit app closed by user")

def main():

    # 2. Start API
    print("Starting API server...")
    api_process = run_api()
    
    # Wait for API to be ready
    time.sleep(5)
    
    # 3. Run Streamlit app
    print("Launching Streamlit app...")
    try:
        run_streamlit_app()
    finally:
        # Cleanup: terminate API process when Streamlit closes
        api_process.terminate()
        print("API server terminated")

if __name__ == "__main__":
    main()