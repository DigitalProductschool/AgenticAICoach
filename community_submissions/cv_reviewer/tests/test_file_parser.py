import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from src.utils import file_parser


def test_find_github_urls_with_multiple_links():
    """Tests that multiple unique GitHub URLs are found correctly."""
    text = "My projects are at https://github.com/user/repo1 and also see https://github.com/another-user/project-x."
    expected = ["https://github.com/another-user/project-x", "https://github.com/user/repo1"]
    assert file_parser.find_github_urls(text) == expected

def test_find_github_urls_with_duplicates():
    """Tests that duplicate URLs are handled and only unique ones are returned."""
    text = "Check out my repo: https://github.com/user/repo1. Yes, https://github.com/user/repo1 is the one."
    expected = ["https://github.com/user/repo1"]
    assert file_parser.find_github_urls(text) == expected

def test_find_github_urls_with_no_links():
    """Tests that an empty list is returned when no GitHub URLs are present."""
    text = "This is a CV with no links to any repositories."
    expected = []
    assert file_parser.find_github_urls(text) == expected

def test_find_github_urls_with_complex_text():
    """Tests URL finding amidst complex sentences and punctuation."""
    text = "My main project (https://github.com/user/main.repo) is key. Don't look at https://github.com/user/old-repo."
    expected = ["https://github.com/user/main.repo", "https://github.com/user/old-repo"]
    assert file_parser.find_github_urls(text) == expected


# --- Tests for File Parsers ---
# For these tests, we mock the external libraries (pypdf, python-docx)
# to avoid needing real files. We are testing that our code correctly
# calls these libraries and processes their return values.

@patch('utils.file_parser.PdfReader')
def test_parse_pdf_text(MockPdfReader):
    """
    Tests the PDF parsing function by mocking the PdfReader library.
    """
    # Arrange: Create a mock PDF reader object that simulates a real one.
    mock_instance = MockPdfReader.return_value
    # Simulate a PDF with two pages, each with some text.
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "This is the first page."
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "This is the second page."
    mock_instance.pages = [mock_page1, mock_page2]

    # Create a fake file stream in memory.
    fake_file_stream = BytesIO(b"fake pdf content")

    # Act: Call our function with the fake file stream.
    result = file_parser.parse_pdf_text(fake_file_stream)

    # Assert: Check that our function joined the text from the pages correctly.
    expected = "This is the first page.\nThis is the second page."
    assert result == expected
    # Assert that the PdfReader was called with our fake file stream.
    MockPdfReader.assert_called_once_with(fake_file_stream)


@patch('utils.file_parser.docx.Document')
def test_parse_docx_text(MockDocxDocument):
    """
    Tests the DOCX parsing function by mocking the python-docx library.
    """
    # Arrange: Create a mock Document object.
    mock_instance = MockDocxDocument.return_value
    # Simulate a document with three paragraphs.
    mock_para1 = MagicMock()
    mock_para1.text = "Hello world."
    mock_para2 = MagicMock()
    mock_para2.text = "This is a test."
    mock_para3 = MagicMock()
    mock_para3.text = "" # Simulate an empty paragraph
    mock_instance.paragraphs = [mock_para1, mock_para2, mock_para3]

    # Create a fake file stream.
    fake_file_stream = BytesIO(b"fake docx content")

    # Act: Call our function.
    result = file_parser.parse_docx_text(fake_file_stream)

    # Assert: Check that our function joined the paragraph text correctly.
    expected = "Hello world.\nThis is a test.\n"
    assert result == expected
    # Assert that the Document class was instantiated with our fake stream.
    MockDocxDocument.assert_called_once_with(fake_file_stream)
