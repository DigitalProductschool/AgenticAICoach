import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

# Import the module to be tested
from utils import file_parser

# --- Tests for find_github_urls ---

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

# CORRECTED: The patch target now points to the location where PdfReader is used.
@patch('utils.file_parser.pypdf.PdfReader')
def test_parse_pdf_text(MockPdfReader):
    """
    Tests the PDF parsing function by mocking the PdfReader library.
    """
    # Arrange
    mock_instance = MockPdfReader.return_value
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "This is the first page."
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "This is the second page."
    mock_instance.pages = [mock_page1, mock_page2]
    fake_file_stream = BytesIO(b"fake pdf content")

    # Act
    result = file_parser.parse_pdf_text(fake_file_stream)

    # Assert
    expected = "This is the first page.\nThis is the second page."
    assert result == expected
    MockPdfReader.assert_called_once_with(fake_file_stream)

@patch('utils.file_parser.docx.Document')
def test_parse_docx_text(MockDocxDocument):
    """
    Tests the DOCX parsing function by mocking the python-docx library.
    """
    # Arrange
    mock_instance = MockDocxDocument.return_value
    mock_para1 = MagicMock()
    mock_para1.text = "Hello world."
    mock_para2 = MagicMock()
    mock_para2.text = "This is a test."
    mock_instance.paragraphs = [mock_para1, mock_para2]
    fake_file_stream = BytesIO(b"fake docx content")

    # Act
    result = file_parser.parse_docx_text(fake_file_stream)

    # Assert
    expected = "Hello world.\nThis is a test."
    assert result == expected
    MockDocxDocument.assert_called_once_with(fake_file_stream)