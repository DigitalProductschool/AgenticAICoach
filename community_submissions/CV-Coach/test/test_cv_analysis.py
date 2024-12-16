import unittest
from app.services.cv_analysis import analyze_cv

class TestCVAnalysis(unittest.TestCase):

    def test_analyze_cv_with_complete_cv(self):
        text = """
        Work Experience
        Education
        Skills
        Contact Information
        Projects
        Python, JavaScript, Agile, Collaboration, Problem Solving
        Achieved 50% increase in efficiency.
        """
        result = analyze_cv(text)
        self.assertEqual(result["scores"]["total"], 100)
        self.assertIn("Your CV is strong and well-structured.", result["overall_feedback"])

    def test_analyze_cv_with_missing_sections(self):
        text = """
        Work Experience
        Skills
        Problem Solving
        """
        result = analyze_cv(text)
        self.assertIn("Missing section: Education", result["structure"])
        self.assertIn("Missing section: Contact Information", result["structure"])
        self.assertLess(result["scores"]["total"], 100)

    def test_analyze_cv_with_no_keywords(self):
        text = "Random Text with no relevant keywords."
        result = analyze_cv(text)
        self.assertIn("Missing keywords", result["keywords"][1])
        self.assertEqual(result["scores"]["keywords"], 0)

if __name__ == "__main__":
    unittest.main()
