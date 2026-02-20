import os
import pytest
from cv_reviewer.tools.file_parser import FileParser

# Helper function to construct file paths
def get_test_file(file_name):
    """
    Retrieves the absolute path of a test file located in the 'data' directory.
    :param file_name: Name of the test file.
    :return: Absolute path of the test file.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, "data", file_name)

# Test parsing a valid PDF file
def test_parse_valid_pdf():
    """
    Tests if a valid PDF file can be parsed successfully.
    """
    file_path = get_test_file("sample_cv.pdf")
    parser = FileParser(file_path)
    content = parser.parse()
    assert len(content) > 0, "Failed to parse valid PDF file"

# Test parsing a valid DOCX file
def test_parse_valid_docx():
    """
    Tests if a valid DOCX file can be parsed successfully.
    """
    file_path = get_test_file("sample_cv.docx")
    parser = FileParser(file_path)
    content = parser.parse()
    assert len(content) > 0, "Failed to parse valid DOCX file"

# Test handling an invalid file format
def test_parse_invalid_format():
    """
    Tests if an unsupported file format raises a ValueError.
    """
    file_path = get_test_file("invalid_format.txt")
    parser = FileParser(file_path)
    with pytest.raises(ValueError, match="Unsupported file format"):
        parser.parse()

# Test handling a non existent file
def test_non_existent_file():
    """
    Tests if a non existent file raises a FileNotFoundError.
    """
    file_path = get_test_file("non_existent.pdf")
    parser = FileParser(file_path)
    with pytest.raises(FileNotFoundError, match="The file '.*' does not exist."):
        parser.parse()

# Test handling a corrupted PDF file
def test_parse_corrupted_pdf():
    """
    Tests if a corrupted PDF file raises an exception during parsing.
    """
    file_path = get_test_file("corrupted_file.pdf")
    parser = FileParser(file_path)
    with pytest.raises(Exception, match="Failed to parse PDF file"):
        parser.parse()

# Test handling a corrupted DOCX file
def test_parse_corrupted_docx():
    """
    Tests if a corrupted DOCX file raises an exception during parsing.
    """
    file_path = get_test_file("corrupted_file.docx")
    parser = FileParser(file_path)
    with pytest.raises(Exception, match="Failed to parse DOCX file"):
        parser.parse()

# Test handling an empty PDF file
def test_parse_empty_pdf():
    """
    Tests if an empty PDF file raises an exception.
    """
    file_path = get_test_file("empty_cv.pdf")
    parser = FileParser(file_path)
    with pytest.raises(Exception, match="The PDF file is empty or does not contain readable text."):
        parser.parse()

# Test handling an empty DOCX file
def test_parse_empty_docx():
    """
    Tests if an empty DOCX file raises an exception.
    """
    file_path = get_test_file("empty_cv.docx")
    parser = FileParser(file_path)
    with pytest.raises(Exception, match="The DOCX file is empty or does not contain readable text."):
        parser.parse()
