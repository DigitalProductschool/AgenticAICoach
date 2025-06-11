import re
from typing import List, IO
from io import BytesIO

# File parsing libraries
import docx
import pypdf 

def parse_docx_text(file_stream: IO[bytes]) -> str:
    """
    Parses text content from a .docx file stream.
    """
    document = docx.Document(file_stream)
    return "\n".join([para.text for para in document.paragraphs])

def parse_pdf_text(file_stream: IO[bytes]) -> str:
    """
    Parses text content from a .pdf file stream.
    """
    # Use the full namespace for the class
    pdf_reader = pypdf.PdfReader(file_stream)
    return "\n".join([page.extract_text() for page in pdf_reader.pages])

def find_github_urls(text: str) -> List[str]:
    """
    Finds all unique GitHub repository URLs in a given text string.
    """
    # This regex finds potential URLs.
    github_regex = r"https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+"
    matches = re.findall(github_regex, text)
    
    # Post-process the matches to remove common trailing punctuation.
    cleaned_matches = []
    for match in matches:
        # Repeatedly strip trailing characters that are not part of a valid URL
        cleaned_match = match
        while cleaned_match and cleaned_match[-1] in '.,)]':
            cleaned_match = cleaned_match[:-1]
        cleaned_matches.append(cleaned_match)
            
    # Use set for uniqueness and then sort the final list.
    return sorted(list(set(cleaned_matches)))
