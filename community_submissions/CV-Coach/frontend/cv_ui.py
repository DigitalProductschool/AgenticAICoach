import streamlit as st
import requests

# Streamlit UI setup
st.set_page_config(page_title="CV Analysis Tool", layout="wide")
st.title("📄 Agentic AI CV Coach")
st.write("🤖 Upload your CV (PDF or DOCX) to receive actionable feedback and improve your chances with recruiters!")

# File upload widget
uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])

if uploaded_file is not None:
    # Display uploaded file name
    st.success(f"📂 File '{uploaded_file.name}' uploaded successfully!")

    # Prepare the file for sending to the backend
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    try:
        # Send the file to the backend API
        # response = requests.post("http://127.0.0.1:8000/upload/", files=files)
        response = requests.post("https://cv-coach-backend.onrender.com/upload/", files=files)
        if response.status_code == 200:
            # Parse the response
            analysis_results = response.json()

            # Display structured feedback
            st.header("Analysis Results")
            
            # Display total score prominently
            total_score = analysis_results["feedback"]["scores"]["total"]
            st.markdown(
                f"""
                <div style='text-align: center; font-size: 36px; font-weight: bold; color: #4CAF50; margin-top: 20px;'>
                    🎯 Total Score: {total_score}/100
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # File information
            st.subheader("📁 File Information")
            st.write(f"**Filename:** {analysis_results['filename']}")

            # Structure analysis
            st.subheader("📚 CV Structure")
            for section in analysis_results["feedback"]["structure"]:
                st.markdown(f"- {section}")

            # Keywords
            st.subheader("🔑 Keywords")
            st.markdown(f"**Found Keywords:** {analysis_results['feedback']['keywords'][0]}")
            st.markdown(f"**Missing Keywords:** {analysis_results['feedback']['keywords'][1]}")

            # Achievements
            st.subheader("🏆 Achievements")
            for achievement in analysis_results["feedback"]["achievements"]:
                st.markdown(f"- {achievement}")

            # Soft skills
            st.subheader("💡 Soft Skills")
            for skill in analysis_results["feedback"]["soft_skills"]:
                st.markdown(f"- {skill}")

            # Formatting issues
            st.subheader("🖋️ Formatting Issues")
            for issue in analysis_results["feedback"]["formatting"]:
                st.markdown(f"- {issue}")

            # Overall feedback
            st.subheader("📋 Overall Feedback")
            for feedback in analysis_results["feedback"]["overall_feedback"]:
                st.markdown(f"- {feedback}")

            # Scores
            st.subheader("📊 Detailed Scores")
            scores = analysis_results["feedback"]["scores"]
            st.write(f"**Structure:** {scores['structure']} / 20")
            st.write(f"**Keywords:** {scores['keywords']} / 30")
            st.write(f"**Achievements:** {scores['achievements']} / 20")
            st.write(f"**Soft Skills:** {scores['soft_skills']} / 20")
            st.write(f"**Formatting:** {scores['formatting']} / 10")

        else:
            st.error(f"❌ Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"❌ Could not connect to the backend. Error: {e}")

# Footer
st.markdown("---")
st.markdown("🚀 Developed by Preeti Awate")
