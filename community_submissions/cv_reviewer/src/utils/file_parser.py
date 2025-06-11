import re
from typing import List, IO
from io import BytesIO

import docx
from pypdf import PdfReader

def parse_docx_text(file_stream: IO[bytes]) -> str:
    """
    Parses text content from a .docx file stream.
    
    Args:
        file_stream: The byte stream of the .docx file.
        
    Returns:
        The extracted text content as a string.
    """
    document = docx.Document(file_stream)
    return "\n".join([para.text for para in document.paragraphs])

def parse_pdf_text(file_stream: IO[bytes]) -> str:
    """
    Parses text content from a .pdf file stream.
    
    Args:
        file_stream: The byte stream of the .pdf file.
        
    Returns:
        The extracted text content as a string.
    """
    pdf_reader = PdfReader(file_stream)
    return "\n".join([page.extract_text() for page in pdf_reader.pages])

def find_github_urls(text: str) -> List[str]:
    """
    Finds all unique GitHub repository URLs in a given text string.
    
    Args:
        text: The text to search for GitHub URLs.
        
    Returns:
        A list of unique GitHub repository URLs found in the text.
    """
    github_regex = r"https://github\.com/[\w\-]+/[\w\-\.]+"
    return sorted(list(set(re.findall(github_regex, text))))
