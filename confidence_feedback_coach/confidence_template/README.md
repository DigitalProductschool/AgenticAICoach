# Agentic AI Confidence Coach

This project provides an AI-powered confidence coach designed to help users improve their communication skills and emotional well-being in the workplace. It utilizes a multi-agent system with each agent specializing in a specific aspect of confidence coaching.

## Agent Overview

The system consists of four distinct agents:

1.  **Rater Agent:**
    *   **Purpose:** Evaluates a user's confidence level on a scale of 1 to 5, providing a detailed analysis and justification for the assigned rating.
    *   **Training:** Employs few-shot learning, referencing `rating_examples.json` for various phrasing scenarios and `rating_table.txt` for a structured point system based on sentence categories.

2.  **Confident Alternatives Agent:**
    *   **Purpose:** Suggests alternative phrasing options to enhance confidence in conversations.
    *   **Training:** Leverages `corrector_examples.json` to identify sentences indicative of low or high self-confidence and learn appropriate replacements.

3.  **Advice Agent:**
    *   **Purpose:** Focuses on the user's emotional well-being, interpreting underlying feelings and providing tailored advice. It can also ask probing questions to help users navigate challenging situations. A dedicated function allows users to express their current feelings, enabling the agent to adapt its advice accordingly.
    *   **Training:** Uses `advice_examples.json` to learn associations between internal feelings, workplace contexts (e.g., lack of recognition, criticism, bullying), and effective advice strategies. The goal is to guide the LLM in providing emotionally intelligent and contextually relevant responses.
    *   **Note:** All training data (feelings, contexts, and advice) are specifically tailored to the workplace environment.

4.  **Transcriber Agent:**
    *   **Purpose:** Converts audio files into text for analysis by the other agents.
    *   **Functionality:** Transcribes audio input into text format.

## Training Methodology

All agents are trained using the **few-shot learning** method. This approach involves providing the LLM with a limited number of examples to guide its learning process and shape its responses in different scenarios.

## Running the Application

To run the Agentic AI Confidence Coach, follow these steps:

1.  **Start the API Server:**

    ```bash
    python crewapi.py
    ```

2.  **Launch the Streamlit App:**

    ```bash
    streamlit run crew_app.py
    ```

Once the application is running, you can access it through your web browser. The user interface features three tabs:

*   **Text Analysis:** Analyzez the confidence of written text.
*   **Audio Analysis:** Analyzez the confidence of spoken language from audio files.
*   **Emotional Advice:** Gives personalized emotional support and guidance.