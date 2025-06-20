from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crew import FeatureClarityCoach, UserState
from utils.enable_logging import logger

app = FastAPI()

# CORS setup for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize user state and the Feature Clarity Coach
user_state = UserState()
coach = FeatureClarityCoach(initial_state=user_state)


# Endpoint to handle user input and return a coach response
@app.post("/chat")
def chat(user_input: str):
    user_state.user_input = user_input
    logger.info(f"User input: {user_input}")
    response = coach.kickoff(user_state.model_dump())

    # Sync the state (including phase and phase_summaries)
    user_state.phase = coach.state.phase
    user_state.phase_summaries = coach.state.phase_summaries

    # If all coaching phases are complete, return a structured summary
    if user_state.phase == "complete":
        summaries = user_state.phase_summaries
        response_text = f"""🎉 **Congratulations! You've successfully clarified your AI feature:**

        ✅ **Your Core Problem:** {summaries.get('core_problem', 'Not captured')}
    
        ✅ **Your Value Proposition:** {summaries.get('core_value', 'Not captured')}
    
        ✅ **Your AI Solution:** {summaries.get('brainstorm_solution', 'Not captured')}
    
        ✅ **Validation Results:** {summaries.get('validate', 'Not captured')}
    
        ---
    
        🚀 **You're now ready to move forward with confidence!** 
    
        **Recommended next steps:**
        • Create detailed technical specifications
        • Build a prototype or MVP  
        • Gather user feedback from your target audience
        • Iterate based on real-world testing
    
        Good luck building something amazing! 🌟
    
        *Feel free to start a new coaching session anytime by clicking Reset.*"""
    else:
        # Assistant reply from the current phase
        response_text = getattr(response, "output", str(response))

    # Save this round of conversation to chat history
    user_state.chat_history.append({"user": user_input, "assistant": response_text})
    logger.info(f"Coach output: {response_text}")

    return {
        "response": response_text,
        "chat_history": user_state.chat_history,
        "phase": user_state.phase,
        "phase_summaries": user_state.phase_summaries
    }


# Endpoint to reset the coaching session completely
@app.post("/reset")
def reset():
    global user_state, coach

    # Re-initialize user state and coach flow
    user_state = UserState()
    coach = FeatureClarityCoach(initial_state=user_state)
    logger.info(f"Reset triggered: All user state and chat history cleared.")
    return {
        "message": "Chat history cleared",
        "chat_history": user_state.chat_history
    }
