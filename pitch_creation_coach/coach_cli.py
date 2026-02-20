import argparse
import requests
import json
from pprint import pprint
import time
import os

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

def print_section(text):
    """Print a formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- {text} ---{Colors.ENDC}\n")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}{text}{Colors.ENDC}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}{text}{Colors.ENDC}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}{text}{Colors.ENDC}")

def check_api_running():
    """Check if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def analyze_pitch(pitch_content, stage="initial", pitch_id=None, user_id="cli_user"):
    """Submit a pitch for analysis"""
    print_section("Analyzing Pitch")
    print("This may take a moment as the AI processes your pitch...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_pitch",
            json={
                "pitch_content": pitch_content,
                "stage": stage,
                "pitch_id": pitch_id,
                "user_id": user_id
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            pitch_id = result["pitch_id"]
            
            print_success(f"Analysis completed! Pitch ID: {pitch_id}\n")
            print_section("Analysis Results")
            print(result["analysis"])
            
            return pitch_id
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def simulate_qa(pitch_content, industry="technology", funding_stage="seed", user_id="cli_user"):
    """Simulate investor Q&A for a pitch"""
    print_section("Simulating Investor Q&A")
    print("This may take a moment as the AI generates investor questions...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/simulate_qa",
            json={
                "pitch_content": pitch_content,
                "industry": industry,
                "funding_stage": funding_stage,
                "user_id": user_id
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print_success("Q&A simulation completed!\n")
            print_section("Investor Questions")
            print(result["qa_simulation"])
            
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def get_pitch_history(pitch_id, user_id="cli_user"):
    """Retrieve the history of a pitch"""
    print_section(f"Retrieving History for Pitch {pitch_id}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/pitch_history",
            json={
                "pitch_id": pitch_id,
                "user_id": user_id
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print_success("History retrieved successfully!\n")
            
            iterations = result["history"]["iterations"]
            metrics = result["metrics"]
            
            print_section("Pitch Iterations")
            for i, iteration in enumerate(iterations):
                print(f"Iteration {i+1} ({iteration['timestamp']})")
                print(f"Content: {iteration['pitch_content'][:100]}...")
                print("-" * 40)
            
            if metrics:
                print_section("Improvement Metrics")
                print(f"Total Iterations: {metrics['iterations_count']}")
                print(f"Last Updated: {metrics['last_updated']}")
            
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def list_all_pitches(user_id="cli_user"):
    """List all pitches for a user"""
    print_section(f"Listing All Pitches for User {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/all_pitches/{user_id}")
        
        if response.status_code == 200:
            result = response.json()
            
            print_success(f"Found {result['count']} pitches\n")
            
            if result['count'] > 0:
                for pitch in result['pitches']:
                    print(f"Pitch ID: {pitch['pitch_id']}")
                    print(f"Created: {pitch['created_at']}")
                    print(f"Iterations: {len(pitch['iterations'])}")
                    print(f"Latest Content: {pitch['iterations'][-1]['pitch_content'][:100]}...")
                    print("-" * 40)
            else:
                print_warning("No pitches found for this user.")
            
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def interactive_mode():
    """Run the CLI in interactive mode"""
    user_id = "cli_user"
    current_pitch_id = None
    current_pitch_content = None
    
    print_header("AI Pitch Coach CLI")
    
    while True:
        print("\n")
        print("1. Create New Pitch")
        print("2. Refine Current Pitch")
        print("3. Simulate Investor Q&A")
        print("4. View Pitch History")
        print("5. List All Pitches")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            print_section("Create New Pitch")
            pitch_content = input("Enter your pitch:\n")
            current_pitch_content = pitch_content
            current_pitch_id = analyze_pitch(pitch_content, user_id=user_id)
            
        elif choice == "2":
            if not current_pitch_id or not current_pitch_content:
                print_warning("No active pitch. Please create a new pitch first.")
                continue
                
            print_section("Refine Current Pitch")
            print(f"Current pitch:\n{current_pitch_content}\n")
            
            new_content = input("Enter your refined pitch (or press Enter to keep current):\n")
            if not new_content:
                new_content = current_pitch_content
                
            current_pitch_content = new_content
            analyze_pitch(new_content, stage="refinement", pitch_id=current_pitch_id, user_id=user_id)
            
        elif choice == "3":
            if not current_pitch_content:
                print_warning("No active pitch. Please create a new pitch first.")
                continue
                
            print_section("Simulate Investor Q&A")
            industry = input("Enter industry (default: technology): ") or "technology"
            funding_stage = input("Enter funding stage (default: seed): ") or "seed"
            
            simulate_qa(current_pitch_content, industry, funding_stage, user_id)
            
        elif choice == "4":
            if not current_pitch_id:
                print_warning("No active pitch. Please create a new pitch first.")
                continue
                
            get_pitch_history(current_pitch_id, user_id)
            
        elif choice == "5":
            list_all_pitches(user_id)
            
            # Optionally load a different pitch
            load_id = input("\nEnter a Pitch ID to load (or press Enter to skip): ")
            if load_id:
                try:
                    response = requests.post(
                        f"{BASE_URL}/pitch_history",
                        json={"pitch_id": load_id, "user_id": user_id}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        current_pitch_id = load_id
                        current_pitch_content = result["history"]["iterations"][-1]["pitch_content"]
                        print_success(f"Loaded pitch {load_id}")
                    else:
                        print_error("Could not load that pitch")
                except Exception as e:
                    print_error(f"Error: {str(e)}")
            
        elif choice == "0":
            print("Exiting. Thank you for using AI Pitch Coach!")
            break
            
        else:
            print_warning("Invalid choice. Please try again.")

def main():
    """Main CLI function"""
    # Check if API is running
    if not check_api_running():
        print_error("ERROR: The API is not running. Please start it with 'python run_api.py' in another terminal.")
        return
    
    parser = argparse.ArgumentParser(description="AI Pitch Coach CLI")
    parser.add_argument("--analyze", type=str, help="Analyze a pitch")
    parser.add_argument("--qa", type=str, help="Simulate Q&A for a pitch")
    parser.add_argument("--history", type=str, help="Get history for a pitch ID")
    parser.add_argument("--list", action="store_true", help="List all pitches")
    parser.add_argument("--user", type=str, default="cli_user", help="User ID")
    
    args = parser.parse_args()
    
    # If no arguments, run in interactive mode
    if not args.analyze and not args.qa and not args.history and not args.list:
        interactive_mode()
        return
    
    # Process command line arguments
    if args.analyze:
        analyze_pitch(args.analyze, user_id=args.user)
        
    if args.qa:
        simulate_qa(args.qa, user_id=args.user)
        
    if args.history:
        get_pitch_history(args.history, user_id=args.user)
        
    if args.list:
        list_all_pitches(args.user)

if __name__ == "__main__":
    main()