from pypdf import PdfReader
from docx import Document
import os

class FileParser:
    def __init__(self, file_path):
        """
        Initializes the FileParser with the path to the file.
        :param file_path: Path to the file to be parsed.
        """
        self.file_path = file_path

    def parse(self):
        """
        Parses the file based on its extension and extracts the content.
        :return: Extracted text content from the file.
        :raises ValueError: If the file format is unsupported.
        :raises Exception: If the file cannot be processed (e.g., corrupted file).
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")
        
        if self.file_path.endswith(".pdf"):
            return self._parse_pdf()
        elif self.file_path.endswith(".docx"):
            return self._parse_docx()
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    def _parse_pdf(self):
        """
        Parses a PDF file and extracts its text.
        :return: Extracted text content from the PDF file.
        :raises Exception: If the PDF file is corrupted or cannot be read.
        """
        text = ""
        try:
            reader = PdfReader(self.file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            raise Exception(f"Failed to parse PDF file: {str(e)}")
        if not text.strip():
            raise Exception("The PDF file is empty or does not contain readable text.")
        return text

    def _parse_docx(self):
        """
        Parses a DOCX file and extracts its text.
        :return: Extracted text content from the DOCX file.
        :raises Exception: If the DOCX file cannot be processed.
        """
        text = ""
        try:
            doc = Document(self.file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Failed to parse DOCX file: {str(e)}")
        if not text.strip():
            raise Exception("The DOCX file is empty or does not contain readable text.")
        return text
