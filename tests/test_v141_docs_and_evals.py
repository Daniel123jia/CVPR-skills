import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WALKTHROUGH = PROJECT_ROOT / "examples" / "clean_clone_walkthrough.md"
FULLTEXT_TEMPLATE = (
    PROJECT_ROOT / "examples" / "end_to_end_demo" / "fulltext_validation_report_template.md"
)


class V141DocsAndEvalsTest(unittest.TestCase):
    def test_clean_clone_walkthrough_exists_and_covers_first_run(self):
        self.assertTrue(WALKTHROUGH.is_file(), WALKTHROUGH)
        content = WALKTHROUGH.read_text(encoding="utf-8")

        required = [
            "git clone",
            "python3.11 -m venv .venv",
            "pip install -r requirements.txt",
            "python -m unittest discover -s tests",
            "python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --limit 5",
            "data/",
            "outputs/",
            "logs/",
            "optional PDF download",
            "download_cvf_pdf.py",
            "cvpr-paper-reader",
            "cvpr-idea-miner",
        ]
        for phrase in required:
            self.assertIn(phrase, content)

    def test_fulltext_validation_report_template_exists_and_has_manual_checks(self):
        self.assertTrue(FULLTEXT_TEMPLATE.is_file(), FULLTEXT_TEMPLATE)
        content = FULLTEXT_TEMPLATE.read_text(encoding="utf-8")

        required = [
            "用户本地已有 PDF",
            "paper_id",
            "title",
            "evidence_level: fulltext",
            "extracted_text_path",
            "generated_reader_files",
            "generated_idea_files",
            "是否编造代码链接",
            "是否编造引用量",
            "是否编造 leaderboard",
            "是否编造未出现的数据集",
            "是否编造实验结果",
            "method / experiments 是否有文本证据",
            "idea 是否标记为 agent hypothesis",
            "first runnable experiment 是否具体",
            "pass / needs revision / fail",
        ]
        for phrase in required:
            self.assertIn(phrase, content)

    def test_boundary_eval_prompts_and_expected_outputs_exist(self):
        cases = [
            "fulltext_no_hallucination",
            "abstract_only_no_experiment_claims",
            "title_only_no_method_details",
        ]

        for case in cases:
            prompt = PROJECT_ROOT / "evals" / "prompts" / f"{case}.txt"
            expected = PROJECT_ROOT / "evals" / "expected" / f"{case}.md"
            with self.subTest(case=case):
                self.assertTrue(prompt.is_file(), prompt)
                self.assertTrue(expected.is_file(), expected)

        title_expected = (
            PROJECT_ROOT / "evals" / "expected" / "title_only_no_method_details.md"
        ).read_text(encoding="utf-8")
        abstract_expected = (
            PROJECT_ROOT / "evals" / "expected" / "abstract_only_no_experiment_claims.md"
        ).read_text(encoding="utf-8")
        fulltext_expected = (
            PROJECT_ROOT / "evals" / "expected" / "fulltext_no_hallucination.md"
        ).read_text(encoding="utf-8")

        for phrase in ["title_only", "不得输出方法细节", "实验结果", "数据集", "代码链接"]:
            self.assertIn(phrase, title_expected)
        for phrase in ["abstract_only", "preliminary summary", "不能输出实验细节"]:
            self.assertIn(phrase, abstract_expected)
        for phrase in ["fulltext", "evidence source", "agent hypothesis", "论文已有结论"]:
            self.assertIn(phrase, fulltext_expected)

    def test_readme_links_walkthrough_and_fulltext_validation_template(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Clean clone walkthrough", readme)
        self.assertIn("Real fulltext validation", readme)
        self.assertIn("examples/clean_clone_walkthrough.md", readme)
        self.assertIn("examples/end_to_end_demo/fulltext_validation_report_template.md", readme)


if __name__ == "__main__":
    unittest.main()
