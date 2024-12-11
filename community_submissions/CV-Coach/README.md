# CV Coach Agent
## Overview
The **CV Coach Agent** is part of the Agentic AI Coach framework, designed to assist users in improving their CVs. It provides actionable feedback based on best practices, enabling users to enhance their CV structure, content, and relevance for job applications.
## Features
- **Upload CVs:** Accepts PDFs and DOCX files for analysis.
- **Content Analysis:** Checks structure, keywords, achievements, and soft skills.
- **Formatting Checks:** Identifies inconsistencies in font, spacing, and layout.
- **Actionable Feedback:** Offers suggestions for improvements, including missing keywords and quantified achievements.
- **Scores:** Rates CV sections and provides an overall score for quality.

## Live Deployment
- **Frontend:** [Streamlit Frontend](https://cv-coach.streamlit.app/)  
- **Backend:** [FastAPI Backend](https://cv-coach-backend.onrender.com/docs#/default/upload_file_upload__post)

## Getting Started
Follow these steps to set up and run the project locally.

### **Backend**
1. Clone the repository:
   git clone https://github.com/PreetiAwate/CV-Coach.git
   cd CV-Coach

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the backend server:
   uvicorn app.main:app --host 0.0.0.0 --port 8000

The backend will be available at `http://127.0.0.1:8000`.

### **Frontend**
1. Navigate to the frontend directory:
   cd frontend

2. Install Streamlit if not already installed:
   pip install streamlit


3. Run the frontend:
   streamlit run cv_ui.py

The frontend will be available at `http://localhost:8501`.

## API Endpoints
### `/upload/`
- **Method:** POST  
- **Description:** Accepts a CV file and returns actionable feedback.  
- **Payload:** `file` (PDF or DOCX)  
- **Response:** JSON feedback including analysis, scores, and suggestions.  

Example Response:
{
  "filename": "SHIVAM_SAHANE_Europass1.pdf",
  "feedback": {
    "structure": [
      "Found section: Work Experience",
      "Found section: Education",
      "Found section: Skills",
      "Missing section: Contact Information",
      "Found section: Projects"
    ],
    "keywords": [
      "Found keywords: Python, JavaScript, React, Angular, Docker, Kubernetes, CI/CD, DevOps, Machine Learning, Deep Learning, AI, Scrum, Microservices",
      "Missing keywords: Cloud Computing, OOP, TensorFlow, Natural Language Processing, PyTorch, System Design, Agile, Data Science"
    ],
    "achievements": [
      "• Designed and developed robust APIs and intuitive frontend interfaces for admin applications, enabling",
      "with improved accuracy.",
      "– Developed the Devices Screen, allowing admins to view and manage information on over 10,000 devices, improving",
      "– Developed a Dynamic Random Assignment API to automate task assignments, enhancing task allocation eﬃciency."
    ],
    "soft_skills": [
      "Soft skills identified: Collaboration, Team Leadership, Problem Solving, Communication, Adaptability"
    ],
    "formatting": [
      "Font inconsistency detected. Consider using uniform fonts and spacing."
    ],
    "overall_feedback": [
      "Your CV is strong and well-structured."
    ],
    "scores": {
      "structure": 16,
      "keywords": 26,
      "achievements": 20,
      "soft_skills": 20,
      "formatting": 10,
      "total": 92
    }
  }
}


## Contributions
We welcome contributions! Follow the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines for details on how to contribute to the project.

## Screenshots
### **Frontend File Upload**
![File Upload](community_submissions/CV-Coach/screenshots/frontend_upload.png)

### **Analysis Results**
![Analysis Results](community_submissions/CV-Coach/screenshots/frontend_results.png)

### **Backend API Response**
![Backend API Response](community_submissions/CV-Coach/screenshots/backend_api_response.png)

### **Testing**
**Unit Tests**
Navigate to the tests directory and run the tests:
pytest

Ensure all tests pass successfully.

## Documentation
Refer to the `/docs` folder for detailed documentation on the architecture, API reference, and contribution guidelines.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to:
- The Agentic AI Coach framework for providing the foundation.
- The AI Makerspace community for fostering collaboration.
