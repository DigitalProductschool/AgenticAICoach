import subprocess
import sys
import time
from pathlib import Path

def install_requirements():
    """Install all packages from requirements.txt"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("Error: requirements.txt not found!", file=sys.stderr)
        sys.exit(1)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Successfully installed all requirements")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

def run_api():
    """Run the API server"""
    try:
        # Using Popen so we can terminate it later
        return subprocess.Popen(
            [sys.executable, "crewapi.py"],
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
            [sys.executable, "-m", "streamlit", "run", "crew_app.py"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Streamlit app failed: {str(e)}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nStreamlit app closed by user")

def main():
    # 1. Install requirements
    install_requirements()
    
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