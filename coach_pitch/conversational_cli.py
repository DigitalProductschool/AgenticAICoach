import requests
import json
import os
from pprint import pprint
import uuid

# CLI colors for better readability
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER} {text.center(58)} {Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}\n")

def print_coach(text):
    """Print a message from the coach"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Coach: {Colors.ENDC}")
    print(f"{text.strip()}")

def print_user(text):
    """Print a message from the user"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}You: {Colors.ENDC}")
    print(f"{text.strip()}")

def print_section(text):
    """Print a formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}--- {text} ---{Colors.ENDC}\n")

def print_error(text):
    """Print an error message"""
    print(f"\n{Colors.RED}{text}{Colors.ENDC}")

def check_api_running():
    """Check if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def start_coaching_session():
    """Start a new coaching session"""
    try:
        response = requests.post(
            f"{BASE_URL}/start_session",
            json={"user_id": "cli_user"}
        )
        
        if response.status_code == 200:
            result = response.json()
            session_id = result["session_id"]
            welcome_message = result["welcome_message"]
            
            print_coach(welcome_message)
            return session_id
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def send_message(session_id, message):
    """Send a message to the coach"""
    try:
        response = requests.post(
            f"{BASE_URL}/send_message",
            json={
                "session_id": session_id,
                "message": message,
                "user_id": "cli_user"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            coach_response = result["response"]
            is_complete = result["is_pitch_complete"]
            complete_pitch = result["complete_pitch"]
            
            print_coach(coach_response)
            
            return {
                "response": coach_response,
                "is_complete": is_complete,
                "complete_pitch": complete_pitch
            }
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def perform_action(session_id, action):
    """Perform a session action"""
    try:
        response = requests.post(
            f"{BASE_URL}/session_action",
            json={
                "session_id": session_id,
                "action": action,
                "user_id": "cli_user"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            action_result = result["result"]
            
            if action == "qa":
                print_section("Investor Q&A Simulation")
            else:
                print_section("Pitch Clarity Feedback")
                
            print(action_result)
            return action_result
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def interactive_session():
    """Run an interactive coaching session"""
    print_header("AI Pitch Coach - Guided Coaching Session")
    
    print("I'll guide you step-by-step through creating a compelling startup pitch.")
    print("Let's work together to craft each element of your pitch in a conversational way.\n")
    
    session_id = start_coaching_session()
    if not session_id:
        print_error("Failed to start coaching session. Please check if the API is running.")
        return
    
    # Main conversation loop
    pitch_complete = False
    while True:
        # Get user input
        user_input = input(f"\n{Colors.BOLD}Your response (or type 'exit' to quit): {Colors.ENDC}")
        
        if user_input.lower() == 'exit':
            print("\nThank you for using AI Pitch Coach! Goodbye!")
            break
            
        # Echo the user's input
        print_user(user_input)
        
        # Send message to coach
        result = send_message(session_id, user_input)
        if not result:
            continue
            
        # Check if pitch is complete
        if result["is_complete"] and not pitch_complete:
            pitch_complete = True
            
            # Show the complete pitch
            if result["complete_pitch"]:
                print_section("Your Complete Pitch")
                print(result["complete_pitch"])
            
            # After pitch is complete, offer additional actions
            print_section("Additional Coaching")
            print("Now that we've completed your pitch, you can:")
            print("1. Generate investor Q&A simulation")
            print("2. Get feedback on pitch clarity and persuasiveness")
            print("3. Continue the conversation")
            print("4. Exit")
            
            action_choice = input(f"\n{Colors.BOLD}Choose an option (1-4): {Colors.ENDC}")
            
            if action_choice == "1":
                perform_action(session_id, "qa")
            elif action_choice == "2":
                perform_action(session_id, "feedback")
            elif action_choice == "4":
                print("\nThank you for using AI Pitch Coach! Goodbye!")
                break

def main():
    """Main function"""
    # Check if the API is running
    if not check_api_running():
        print_error("ERROR: The API is not running. Please start it with 'python run_api.py' in another terminal.")
        return
    
    interactive_session()

if __name__ == "__main__":
    main()