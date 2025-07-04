from datetime import datetime
import json
import os

#This class manages the persistence of pitch feedback history
#Tracks pitch iterations over time, allowing for progress tracking
class FeedbackTracker:
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.feedback_dir = "feedback_data"
        os.makedirs(self.feedback_dir, exist_ok=True)
        self.feedback_file = f"{self.feedback_dir}/{user_id}_feedback.json"
        self.load_feedback_history()
    
    def load_feedback_history(self):
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback_history = json.load(f)
        else:
            self.feedback_history = {
                "user_id": self.user_id,
                "pitches": []
            }
    
    def save_feedback_history(self):
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_history, f, indent=2)
    
    def _serialize_crew_output(self, output):
        """Convert CrewOutput to a serializable format"""
        # If output is already a string, just return it
        if isinstance(output, str):
            return output
        
        # Otherwise convert to string and sanitize
        try:
            if hasattr(output, '__str__'):
                return str(output).replace('\n', ' ').replace('\r', ' ')
            return str(output).replace('\n', ' ').replace('\r', ' ')
        except Exception as e:
            return f"Error serializing output: {str(e)}"
    
    def add_pitch_feedback(self, pitch_content, feedback, pitch_id=None):
        # Create new pitch entry if no ID provided, otherwise update existing
        timestamp = datetime.now().isoformat()
        
        # Ensure feedback is serializable
        serialized_feedback = self._serialize_crew_output(feedback)
        
        if pitch_id is None:
            # New pitch
            pitch_entry = {
                "pitch_id": str(len(self.feedback_history["pitches"]) + 1),
                "created_at": timestamp,
                "iterations": [{
                    "timestamp": timestamp,
                    "pitch_content": pitch_content,
                    "feedback": serialized_feedback
                }]
            }
            self.feedback_history["pitches"].append(pitch_entry)
        else:
            # Update existing pitch
            pitch_found = False
            for pitch in self.feedback_history["pitches"]:
                if pitch["pitch_id"] == pitch_id:
                    pitch["iterations"].append({
                        "timestamp": timestamp,
                        "pitch_content": pitch_content,
                        "feedback": serialized_feedback
                    })
                    pitch_found = True
                    break
            
            # If pitch_id not found, create a new entry
            if not pitch_found:
                pitch_entry = {
                    "pitch_id": pitch_id,
                    "created_at": timestamp,
                    "iterations": [{
                        "timestamp": timestamp,
                        "pitch_content": pitch_content,
                        "feedback": serialized_feedback
                    }]
                }
                self.feedback_history["pitches"].append(pitch_entry)
        
        self.save_feedback_history()
        return pitch_id or pitch_entry["pitch_id"]
    
    def get_pitch_history(self, pitch_id):
        for pitch in self.feedback_history["pitches"]:
            if pitch["pitch_id"] == pitch_id:
                return pitch
        return None
    
    def get_all_pitches(self):
        return self.feedback_history["pitches"]
    
    def get_improvement_metrics(self, pitch_id):
        pitch = self.get_pitch_history(pitch_id)
        if not pitch or len(pitch["iterations"]) < 2:
            return None
        
        # This would be more sophisticated in a real implementation
        # For now, just return the number of iterations as a simple metric
        return {
            "iterations_count": len(pitch["iterations"]),
            "last_updated": pitch["iterations"][-1]["timestamp"]
        }