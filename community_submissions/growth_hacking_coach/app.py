import streamlit as st
import requests
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Growth Hacking Coach",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Flag to use mock responses when API is not available
if "use_mock_responses" not in st.session_state:
    st.session_state.use_mock_responses = False  # Default to API mode

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #FF5733, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .chat-container {
        border-radius: 10px;
        background-color: #f9f9f9;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .sidebar-content {
        padding: 15px;
        background-color: #f5f5f5;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF8C00;
    }
    div[data-testid="stChatMessage"] {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Create sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)
    st.markdown("<h1 class='main-header'>Growth Hacking Coach</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Your AI guide to growth & viral marketing</p>", unsafe_allow_html=True)

    # Add sidebar content
    with st.container(border=True):
        st.markdown("### 🔍 What I can help with:")
        st.markdown("- Growth strategy development")
        st.markdown("- Viral marketing techniques")
        st.markdown("- User acquisition channels")
        st.markdown("- Content optimization")
        st.markdown("- Conversion rate optimization")
        st.markdown("- Analytics and metrics")

    # Add buttons for chat management
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    with col_btn2:
        if st.button("📋 Examples"):
            st.session_state.show_examples = not st.session_state.get("show_examples", False)
            st.rerun()


    # Show example questions if toggled
    if st.session_state.get("show_examples", False):
        with st.container(border=True):
            st.markdown("### 💡 Example Questions")
            example_questions = [
                "How can I increase user engagement for my mobile app?",
                "What are the best viral marketing techniques for a SaaS product?",
                "How do I optimize my content for better conversion rates?",
                "What growth metrics should I track for my e-commerce business?",
                "How can I leverage social media for rapid growth?"
            ]

            for i, question in enumerate(example_questions):
                if st.button(f"{i+1}. {question}", key=f"example_{i}"):
                    # Use this example as the user input
                    st.session_state.example_question = question
                    st.rerun()

# Main content area
st.markdown("<h1 class='main-header'>🚀 Growth Hacking Coach</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your AI-powered guide to growth hacking and viral marketing strategies</p>", unsafe_allow_html=True)

# Main chat container
st.markdown("### 💬 Chat with your Growth Hacking Coach")
chat_container = st.container(height=500)

# Function to generate mock responses when API is not available
def get_mock_response(message: str, conversation_history=None) -> str:
    """Generate a mock response for testing when the API is not available"""
    # Simulate thinking time
    time.sleep(1)

    # Common growth hacking terms to include in responses
    growth_terms = [
        "user acquisition", "viral coefficient", "retention rate", "conversion funnel",
        "A/B testing", "customer lifetime value (CLV)", "churn rate", "growth loops",
        "network effects", "referral programs", "content marketing", "SEO optimization",
        "social media engagement", "email marketing", "product-market fit"
    ]

    # Default response if no keywords match
    default_responses = [
        f"That's an interesting growth question. To develop an effective strategy, I'd recommend focusing on {random.choice(growth_terms)} and {random.choice(growth_terms)}. Start by analyzing your current metrics to identify the biggest opportunities for improvement.",
        f"From a growth hacking perspective, you should consider implementing {random.choice(growth_terms)} to address this challenge. I'd also recommend experimenting with {random.choice(growth_terms)} and measuring the results to find what works best for your specific situation.",
        f"Great question about growth! The most effective approach would be to combine {random.choice(growth_terms)} with targeted {random.choice(growth_terms)}. Remember that growth hacking is about rapid experimentation, so set up proper tracking to quickly identify what's working."
    ]

    # Check if we have conversation history and this is a follow-up question
    if conversation_history and len(conversation_history) > 2:
        # Get the last assistant response
        last_assistant_msg = next((msg for msg in reversed(conversation_history)
                                if msg["role"] == "assistant"), None)

        # Get the previous user message
        prev_user_msgs = [msg for msg in conversation_history if msg["role"] == "user"]

        # If this appears to be a follow-up question, acknowledge it
        if last_assistant_msg and len(prev_user_msgs) > 1:
            follow_up_responses = [
                f"Building on our previous discussion about {random.choice(growth_terms)}, I'd recommend focusing on {random.choice(growth_terms)} for your specific question. {random.choice(default_responses)}",
                f"To follow up on our conversation, let's dive deeper into {random.choice(growth_terms)}. For your current question about {message[:20]}..., I suggest exploring {random.choice(growth_terms)} as a strategy.",
                f"Thanks for the follow-up question. Based on what we've discussed about {random.choice(growth_terms)}, I think the next step would be to implement {random.choice(growth_terms)} to address your current challenge."
            ]
            return random.choice(follow_up_responses)

    # Sample responses based on keywords in the message
    responses = {
        "user engagement": [
            f"To increase user engagement, focus on these key strategies: 1) Improve your onboarding experience to show value quickly, 2) Implement {random.choice(growth_terms)} to keep users coming back, 3) Use gamification elements to make the experience more enjoyable, and 4) Regularly collect and act on user feedback.",
            f"User engagement can be significantly improved by understanding your users' core needs. I recommend starting with user interviews and {random.choice(growth_terms)} analysis to identify pain points. Then, create engagement loops that deliver value and encourage return visits."
        ],
        "viral": [
            f"Viral marketing success depends on creating content that people naturally want to share. The key elements are: emotional appeal, practical value, and frictionless sharing mechanisms. I'd recommend focusing on {random.choice(growth_terms)} and {random.choice(growth_terms)} to maximize your viral potential.",
            f"For viral growth, you need a K-factor greater than 1. This means each user brings in more than one new user. Implement strong {random.choice(growth_terms)} and incentivize sharing through {random.choice(growth_terms)}. Make sharing a natural part of the user experience."
        ],
        "conversion": [
            f"To optimize conversion rates, start by analyzing your current funnel to identify drop-off points. Then implement targeted improvements like simplified forms, stronger calls-to-action, and trust signals. Regular {random.choice(growth_terms)} will help you continuously improve.",
            f"Conversion optimization requires a systematic approach. Start with user session recordings to identify friction points, then use {random.choice(growth_terms)} to test improvements. Focus on reducing steps in your funnel and creating a sense of urgency."
        ],
        "metrics": [
            f"The key growth metrics to track include: acquisition cost (CAC), {random.choice(growth_terms)}, {random.choice(growth_terms)}, and activation rate. These will give you a complete picture of your growth funnel and help identify optimization opportunities.",
            f"For e-commerce specifically, focus on tracking average order value, repeat purchase rate, {random.choice(growth_terms)}, and cart abandonment rate. These metrics will help you identify where to focus your growth efforts."
        ],
        "social media": [
            f"To leverage social media for growth, focus on platform-specific content strategies rather than cross-posting the same content. Identify where your audience spends time and double down there. Use {random.choice(growth_terms)} to amplify your reach and {random.choice(growth_terms)} to measure effectiveness.",
            f"Social media growth requires consistency and community building. Create a content calendar, engage authentically with your audience, and use {random.choice(growth_terms)} to expand your reach. Consider partnering with micro-influencers for greater authenticity."
        ]
    }



    # Check for keywords in the message and return appropriate response
    for keyword, keyword_responses in responses.items():
        if keyword.lower() in message.lower():
            return random.choice(keyword_responses)

    # If no keywords match, return a default response
    return random.choice(default_responses)

# Function to send message to API and get response
def query_growth_coach(message: str) -> str:
    # Get conversation history from session state
    conversation_history = st.session_state.messages

    # Try to connect to the API
    try:
        # Send the request to the API with conversation history
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={
                "message": message,
                "conversation_history": conversation_history  # Include full conversation history
            },
            headers={"Content-Type": "application/json"}
        )

        # Check if the request was successful
        if response.status_code == 200:
            response_json = response.json()
            if response_json and "response" in response_json:
                return response_json["response"]
            else:
                return "I received an empty response from the API. Please try again later."
        else:
            # If there was an error, return the error message
            error_text = response.text
            return f"Error: {response.status_code} - {error_text}"
    except requests.exceptions.ConnectionError:
        # If we can't connect to the API, suggest using mock mode
        st.warning("Unable to connect to the API. Switching to mock mode.")
        st.session_state.use_mock_responses = True
        return get_mock_response(message, conversation_history)
    except Exception as e:
        # For any other error, return an error message
        error_msg = f"Error connecting to the Growth Hacking Coach API: {str(e)}"
        st.error(error_msg)
        return error_msg

# Display chat messages in the chat container
with chat_container:
    if not st.session_state.messages:
        st.info("👋 Hello! I'm your Growth Hacking Coach. Ask me anything about growth strategies, viral marketing, user acquisition, or content optimization!")
    else:
        for message in st.session_state.messages:
            avatar = "🧑‍💻" if message["role"] == "user" else "🚀"
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])

# Chat input below the container
# Check if we have an example question to use
if hasattr(st.session_state, 'example_question') and st.session_state.example_question:
    prompt = st.session_state.example_question
    # Clear the example question so it doesn't get reused
    st.session_state.example_question = None
else:
    prompt = st.chat_input("Ask your growth hacking question...", key="chat_input")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with chat_container:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

    # Get response from API
    with chat_container:
        with st.chat_message("assistant", avatar="🚀"):
            with st.spinner("Generating growth hacking insights..."):
                try:
                    response = query_growth_coach(prompt)
                    st.markdown(response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    # Add error message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Rerun to update the UI
    st.rerun()