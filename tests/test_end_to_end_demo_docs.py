import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = PROJECT_ROOT / "examples" / "end_to_end_demo"
SKILL_NAMES = ["conference-cvpr", "cvpr-paper-reader", "cvpr-idea-miner"]


class EndToEndDemoDocsTest(unittest.TestCase):
    def read_demo_file(self, filename):
        path = DEMO_DIR / filename
        self.assertTrue(path.is_file(), path)
        return path.read_text(encoding="utf-8")

    def test_demo_readme_and_acceptance_checklist_exist(self):
        self.assertTrue((DEMO_DIR / "README.md").is_file())
        self.assertTrue((DEMO_DIR / "acceptance_checklist.md").is_file())

    def test_demo_readme_documents_full_local_loop(self):
        readme = self.read_demo_file("README.md")

        required_phrases = [
            "conference-cvpr",
            "CVPR 2026 小样本",
            "raw",
            "normalized",
            "exports",
            "completeness report",
            "cvpr-paper-reader",
            "fulltext",
            "abstract_only",
            "reading_note.md",
            "cvpr-idea-miner",
            "collect_reader_notes.py",
            "idea_cards.md",
            "人工检查",
            "反幻觉",
            "evidence level",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, readme)

    def test_acceptance_checklist_covers_anti_hallucination_gates(self):
        checklist = self.read_demo_file("acceptance_checklist.md")

        required_phrases = [
            "raw / normalized / exports / completeness report",
            "fulltext",
            "摘要",
            "evidence level",
            "没有编造实验结果",
            "数据集",
            "ablation",
            "代码链接",
            "正确读取 reader notes",
            "区分论文事实和新 idea",
            "evidence source",
            "risk",
            "first runnable experiment",
            "title_only",
            "没有输出细节结论",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, checklist)

    def test_three_skills_exist_with_required_entry_files(self):
        skill_root = PROJECT_ROOT / "skills"
        actual_skill_dirs = sorted(
            path.name for path in skill_root.iterdir() if path.is_dir() and not path.name.startswith("_")
        )
        self.assertEqual(sorted(SKILL_NAMES), actual_skill_dirs)

        for skill_name in SKILL_NAMES:
            with self.subTest(skill=skill_name):
                skill_dir = skill_root / skill_name
                self.assertTrue(skill_dir.is_dir())
                self.assertTrue((skill_dir / "README.md").is_file())
                self.assertTrue((skill_dir / "SKILL.md").is_file())
                self.assertTrue((skill_dir / "manifest.yaml").is_file())

    def test_demo_directory_contains_docs_only(self):
        forbidden_dirs = {"data", "outputs", "logs"}
        forbidden_suffixes = {".pdf", ".xlsx", ".xls", ".sqlite", ".db"}

        for path in DEMO_DIR.rglob("*"):
            relative_parts = set(path.relative_to(DEMO_DIR).parts)
            self.assertTrue(forbidden_dirs.isdisjoint(relative_parts), path)
            if path.is_file():
                self.assertEqual(".md", path.suffix, path)
                self.assertNotIn(path.suffix.lower(), forbidden_suffixes, path)


if __name__ == "__main__":
    unittest.main()
