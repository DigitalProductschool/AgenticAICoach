import os
import unittest
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from agents.rater import ConfidenceRaterAgent
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class TestConfidenceRaterAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.training_file = os.path.join(
            project_root,
            'training',
            'rater_examples.json'
        )
        self.scoring_table_file = os.path.join(
            project_root,
            'training',
            'rating_table.txt'
        )
        self.rater_agent = ConfidenceRaterAgent(self.training_file, self.scoring_table_file)
        self.rater = self.rater_agent.create_agent()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)

        self.generation_config = {
            "temperature": 0.5,
            "max_output_tokens": 8192, #Increased max output tokens
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=self.generation_config,
        )

    def test_load_examples(self):
        """Test that the examples are loaded correctly."""
        self.assertIsNotNone(self.rater_agent.examples_content, "Examples content should not be None")
        self.assertNotEqual(self.rater_agent.examples_content, "", "Examples content should not be empty")
        print("Loaded Examples Content:\n", self.rater_agent.examples_content)

    def test_load_scoring_table(self):
        """Test that the scoring table is loaded correctly."""
        self.assertIsNotNone(self.rater_agent.scoring_table_content, "Scoring table content should not be None")
        self.assertNotEqual(self.rater_agent.scoring_table_content, "", "Scoring table content should not be empty")
        print("Loaded Scoring Table Content:\n", self.rater_agent.scoring_table_content)

    def test_rate_confidence(self):
        """Test that the agent provides a confidence rating and a non-empty analysis."""
        test_text = '''Alice: Hey Bob and Carol, good morning! I wanted to quickly touch base on the Q3 marketing campaign tasks. Bob, how's the social media content calendar coming along?

Bob: Good morning, Alice! It's progressing, but I'm a little behind schedule. I think I might need a few more days to finalize it.

Carol: Morning, you two. Bob, is there anything blocking you? Perhaps I could lend a hand with some of the graphics?

Bob: Thanks, Carol, I appreciate the offer. It's mostly just been a time crunch. I've been juggling a few other projects as well. I could probably use an extension, maybe until Wednesday?

Alice: Wednesday might be pushing it a bit, Bob. We need to have the calendar approved by the team lead by Thursday morning. How about Tuesday evening? Can you commit to having it done by then?

Bob: I'm not entirely sure, but I'll try my best. It depends on how quickly I can get the competitor analysis done.

Alice: Okay, let's make this a priority. Carol, could you check in with Bob on Monday afternoon to see how he's doing with the competitor analysis? And Bob, please keep Carol in the loop so she can assist if needed.

Carol: Sure, Alice. I'll reach out to Bob on Monday afternoon. Bob, please share the competitor analysis with me as soon as you have a draft.

Bob: Sounds good. I’ll probably have a draft by Monday morning. Maybe.

Alice: Great. Now, Carol, how's the email marketing campaign coming along?

Carol: It's progressing well, Alice. I've finished the draft of the email sequence, and I'm just waiting for feedback from the product team.

Alice: Have you sent it to them already? It's important to get their input as soon as possible.

Carol: Yes, I sent it to them yesterday. It can't be helped, I have to wait.

Alice: Okay. If you don't hear back from them by Monday morning, please follow up. We need to finalize the email sequence by Tuesday. Also, let's schedule a quick meeting on Wednesday to review all the marketing materials before we send them to the team lead.

Bob: Wednesday might not work for me, I may be busy with the social media calendar.

Alice: Bob, it's important that you attend the meeting. Can you please check your calendar and confirm your availability? Carol, are you available on Wednesday afternoon?

Carol: Yes, I'm available on Wednesday afternoon. But I might have to move my doctor appointment.

Alice: Carol, please don't reschedule important appointments. Let's aim for Wednesday at 2 PM. Bob, can you make that work?

Bob: I know this sounds silly but I think I have something at that day and time.

Alice: Bob, it’s really important you attend. It sounds like you're being really held up.

Carol: How about we push the meeting up and do it tomorrow morning?

Alice: Bob, please tell me if there's something wrong with this that's happening.

Bob: I just don’t want to make the wrong decision, maybe there's a better outcome to this…

Alice: Bob, it might help if you think of the situation…'''
        analysis = self.rater_agent.rate_confidence(test_text)

        try:
            print("LLM Analysis:\n", analysis)
            self.assertIsNotNone(analysis, "LLM analysis should not be None")
            self.assertNotEqual(analysis, "", "LLM analysis should not be empty")
            #Just need to verify that some text is returned and no exception

        except Exception as e:
            self.fail(f"LLM call failed: {e}")



if __name__ == '__main__':
    unittest.main()