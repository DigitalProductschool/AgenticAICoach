#!/usr/bin/env python
import sys
import warnings

from ai_community_matchmaker.crew import AiCommunityMatchmaker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    path_target_user_file = './src/ai_community_matchmaker/data/target_user.json'
    path_community_file = './src/ai_community_matchmaker/data/community.csv'
    inputs = {
        'target_user': path_target_user_file,
        'community_members': path_community_file,
    }
    AiCommunityMatchmaker().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    path_target_user_file = './src/ai_community_matchmaker/data/target_user.json'
    path_community_file = './src/ai_community_matchmaker/data/community.csv'
    inputs = {
        'target_user': path_target_user_file,
        'community_members': path_community_file,
    }
    try:
        AiCommunityMatchmaker().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiCommunityMatchmaker().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    path_target_user_file = './src/ai_community_matchmaker/data/target_user.json'
    path_community_file = './src/ai_community_matchmaker/data/community.csv'
    inputs = {
        'target_user': path_target_user_file,
        'community_members': path_community_file,
    }
    try:
        AiCommunityMatchmaker().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
