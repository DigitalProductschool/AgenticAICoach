#!/usr/bin/env python
import os
import sys
from cv_reviewer.crew import CVReviewCrew
from cv_reviewer.tools.file_parser import FileParser

def run():
    # Extract text from the job description and CV
    with open('./test/data/sample_jd.txt', 'r', encoding='utf-8') as jd_file:
        jd_text = jd_file.read()

    cv_parser = FileParser('./test/data/sample_cv.pdf')
    cv_text = cv_parser.parse()

    # Pass extracted text as inputs to the crew
    inputs = {
        'jd_text': jd_text,
        'cv_text': cv_text
    }
    cv_crew = CVReviewCrew(inputs=inputs)
    cv_crew.crew().kickoff(inputs=inputs)
