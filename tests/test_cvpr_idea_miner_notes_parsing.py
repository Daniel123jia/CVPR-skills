import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "reader_notes"
SCRIPT = PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "scripts" / "collect_reader_notes.py"


class CvprIdeaMinerNotesParsingTest(unittest.TestCase):
    def run_collector(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        output = Path(tmp.name) / "reader_notes_index.json"

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--input-dir", str(FIXTURE_DIR), "--output", str(output)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(output.read_text(encoding="utf-8"))

    def test_collect_reader_notes_cleans_titles_and_records_evidence_levels(self):
        index = self.run_collector()
        papers = {paper["paper_id"]: paper for paper in index["papers"]}

        self.assertEqual(index["paper_count"], 5)
        self.assertEqual(papers["CVPR2026_000001"]["title"], "Generalizable Structure-Aware Keypoint Correspondence")
        self.assertEqual(papers["CVPR2026_TITLE_EN"]["title"], "DirectFisheye-GS")
        self.assertEqual(papers["CVPR2026_ABSTRACT_001"]["title"], "Abstract Fixture Paper")
        self.assertEqual(papers["CVPR2026_FULLTEXT_001"]["title"], "Fulltext Fixture Paper")
        self.assertEqual(papers["CVPR2026_NO_TITLE"]["title"], "CVPR2026_NO_TITLE")

        self.assertEqual(papers["CVPR2026_000001"]["evidence_level"], "title_only")
        self.assertEqual(papers["CVPR2026_TITLE_EN"]["evidence_level"], "title_only")
        self.assertEqual(papers["CVPR2026_NO_TITLE"]["evidence_level"], "title_only")
        self.assertEqual(papers["CVPR2026_ABSTRACT_001"]["evidence_level"], "abstract_only")
        self.assertEqual(papers["CVPR2026_FULLTEXT_001"]["evidence_level"], "fulltext")

        self.assertIn("reading_note", papers["CVPR2026_FULLTEXT_001"]["files"])
        self.assertIn("method", papers["CVPR2026_FULLTEXT_001"]["files"])
        self.assertIn("experiments", papers["CVPR2026_FULLTEXT_001"]["files"])
        self.assertIn("limitations_and_ideas", papers["CVPR2026_FULLTEXT_001"]["files"])

    def test_title_and_abstract_fixtures_are_not_marked_fulltext(self):
        index = self.run_collector()
        papers = {paper["paper_id"]: paper for paper in index["papers"]}

        self.assertNotEqual(papers["CVPR2026_000001"]["evidence_level"], "fulltext")
        self.assertNotEqual(papers["CVPR2026_TITLE_EN"]["evidence_level"], "fulltext")
        self.assertNotEqual(papers["CVPR2026_ABSTRACT_001"]["evidence_level"], "fulltext")
        self.assertIn(papers["CVPR2026_FULLTEXT_001"]["evidence_level"], ["fulltext", "fulltext_notes"])

    def test_cleaned_titles_do_not_contain_note_suffixes(self):
        index = self.run_collector()
        forbidden_suffixes = [
            "中文阅读笔记",
            "阅读笔记",
            "论文阅读笔记",
            "Reading Note",
            "Paper Reading Note",
            "CVPR Paper Reading Note",
        ]

        for paper in index["papers"]:
            for suffix in forbidden_suffixes:
                self.assertNotIn(suffix, paper["title"])


if __name__ == "__main__":
    unittest.main()
