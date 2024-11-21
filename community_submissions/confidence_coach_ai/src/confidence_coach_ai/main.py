import os
from crew import interactive_session

if __name__ == "__main__":
    # Change working directory to script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    interactive_session()