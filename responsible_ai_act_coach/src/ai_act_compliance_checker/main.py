#!/usr/bin/env python
import sys
from ai_act_compliance_checker.crew import AIComplianceCrew  # Ensure correct import

def run():
    inputs = {
        'path_to_ai_act': './src/ai_act_compliance_checker/data/AIAct.pdf', # https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.pdf
        'path_to_project_description': './src/ai_act_compliance_checker/data/ProjectDescription.pdf'
    }
    AIComplianceCrew().crew().kickoff(inputs=inputs)

