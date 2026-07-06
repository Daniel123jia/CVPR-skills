import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "test.yml"
FULLTEXT_GUIDE = PROJECT_ROOT / "examples" / "end_to_end_demo" / "fulltext_case_guide.md"


class CiAndFulltextGuideTest(unittest.TestCase):
    def test_github_actions_workflow_runs_local_validation_only(self):
        self.assertTrue(WORKFLOW.is_file(), WORKFLOW)
        workflow = WORKFLOW.read_text(encoding="utf-8")

        for required in [
            "push:",
            "pull_request:",
            "python-version: '3.11'",
            "pip install -r requirements.txt",
            "python -m unittest discover -s tests",
            "python skills/conference-cvpr/scripts/run_pipeline.py --help",
            "python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --help",
            "python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --help",
        ]:
            self.assertIn(required, workflow)

        forbidden = [
            "run_pipeline.py --year",
            "collect_cvpr.py --year",
            "curl ",
            "wget ",
            "gh release",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, workflow)

    def test_fulltext_case_guide_documents_local_pdf_acceptance_without_artifacts(self):
        self.assertTrue(FULLTEXT_GUIDE.is_file(), FULLTEXT_GUIDE)
        guide = FULLTEXT_GUIDE.read_text(encoding="utf-8")

        required_phrases = [
            "local CVPR PDF",
            "PDF 不提交仓库",
            "extract_pdf_text.py",
            "paper_text.md",
            "reading_note.md",
            "method.md",
            "experiments.md",
            "limitations_and_ideas.md",
            "collect_reader_notes.py",
            "idea_cards.md",
            "evidence level",
            "evidence source",
            "risk",
            "first runnable experiment",
            "代码链接",
            "引用量",
            "leaderboard",
            "未出现的数据集",
            "未出现的实验结果",
            "outputs/",
            "PDF",
            "Excel",
            "SQLite",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, guide)

        self.assertNotIn("download PDF", guide.lower())
        self.assertNotIn("external API", guide)

    def test_demo_readme_links_fulltext_case_guide(self):
        readme = (PROJECT_ROOT / "examples" / "end_to_end_demo" / "README.md").read_text(encoding="utf-8")

        self.assertIn("fulltext_case_guide.md", readme)

    def test_root_readme_mentions_clean_clone_fulltext_and_ci(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        for heading in ["Clean clone validation", "Fulltext local validation", "CI status / testing"]:
            self.assertIn(heading, readme)


if __name__ == "__main__":
    unittest.main()
