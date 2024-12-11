from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO

def extract_text(file_content: bytes, file_type: str) -> str:
    try:
        if file_type == "application/pdf":
            # Extract text from PDF
            reader = PdfReader(BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text if text.strip() else "No text found in the PDF file."
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Extract text from DOCX
            doc = Document(BytesIO(file_content))
            text = "\n".join([p.text for p in doc.paragraphs])
            return text if text.strip() else "No text found in the DOCX file."
        else:
            return None
    except Exception as e:
        # Log error (optional) and return a user-friendly message
        print(f"Error during file parsing: {e}")
        return "Error extracting text from the uploaded file."
