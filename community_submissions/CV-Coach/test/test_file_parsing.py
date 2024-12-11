import unittest
from app.services.file_parsing import extract_text

class TestFileParsing(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
        result = extract_text(pdf_content, "application/pdf")
        self.assertIn("No text found", result)

    def test_extract_text_from_docx(self):
        docx_content = b"Word.Document\nContent here"
        result = extract_text(docx_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.assertIn("No text found", result)

    def test_extract_text_with_invalid_file_type(self):
        result = extract_text(b"Some content", "application/unknown")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
