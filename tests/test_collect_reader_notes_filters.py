import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "scripts" / "collect_reader_notes.py"


class CollectReaderNotesFiltersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.reader_root = Path(self.tmp.name) / "reader"
        self.reader_root.mkdir()

        self.write_note_dir("P_TITLE", "Shared Paper", "title_only", ["reading_note"])
        self.write_note_dir(
            "P_FULL",
            "Shared Paper",
            "fulltext",
            ["reading_note", "method", "experiments", "limitations_and_ideas"],
        )
        self.write_note_dir("P_ABSTRACT", "Abstract Paper", "abstract_only", ["reading_note"])
        self.write_note_dir("P_READER", "Reader Notes Paper", "reader_notes", ["reading_note"])
        self.write_note_dir("P_UNKNOWN", "Unknown Evidence Paper", None, ["reading_note"])
        self.write_note_dir("P_SAME_SHORT", "Equal Evidence Paper", "fulltext", ["reading_note"])
        self.write_note_dir(
            "P_SAME_COMPLETE",
            "Equal Evidence Paper",
            "fulltext",
            ["reading_note", "method", "experiments"],
        )

    def write_note_dir(self, paper_id, title, evidence_level, files):
        note_dir = self.reader_root / paper_id
        note_dir.mkdir()
        for key in files:
            filename = {
                "reading_note": "reading_note.md",
                "method": "method.md",
                "experiments": "experiments.md",
                "limitations_and_ideas": "limitations_and_ideas.md",
            }[key]
            lines = ["---", "title: {}".format(title)]
            if evidence_level:
                lines.append("evidence_level: {}".format(evidence_level))
            lines.extend(["---", "", "# {} 中文阅读笔记".format(title), ""])
            (note_dir / filename).write_text("\n".join(lines), encoding="utf-8")

    def run_collector(self, *extra_args):
        output = Path(self.tmp.name) / "reader_notes_index.json"
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(self.reader_root),
            "--output",
            str(output),
        ]
        cmd.extend(extra_args)
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(output.read_text(encoding="utf-8"))

    def paper_ids(self, index):
        return [paper["paper_id"] for paper in index["papers"]]

    def test_without_new_filters_keeps_original_full_collection_behavior(self):
        index = self.run_collector()

        self.assertEqual(index["paper_count"], 7)
        self.assertEqual(
            self.paper_ids(index),
            [
                "P_ABSTRACT",
                "P_FULL",
                "P_READER",
                "P_SAME_COMPLETE",
                "P_SAME_SHORT",
                "P_TITLE",
                "P_UNKNOWN",
            ],
        )
        self.assertEqual(index["filters"]["dedupe_title"], "none")

    def test_paper_id_filter_keeps_only_selected_papers(self):
        index = self.run_collector("--paper-id", "P_FULL", "--paper-id", "P_ABSTRACT")

        self.assertEqual(self.paper_ids(index), ["P_ABSTRACT", "P_FULL"])
        self.assertEqual(index["filters"]["paper_ids"], ["P_FULL", "P_ABSTRACT"])

    def test_evidence_level_filter_keeps_only_fulltext(self):
        index = self.run_collector("--evidence-level", "fulltext")

        self.assertEqual(self.paper_ids(index), ["P_FULL", "P_SAME_COMPLETE", "P_SAME_SHORT"])

    def test_min_evidence_level_fulltext_filters_title_and_abstract(self):
        index = self.run_collector("--min-evidence-level", "fulltext")

        self.assertEqual(
            self.paper_ids(index),
            ["P_FULL", "P_READER", "P_SAME_COMPLETE", "P_SAME_SHORT"],
        )

    def test_dedupe_title_prefers_highest_evidence(self):
        index = self.run_collector("--dedupe-title", "prefer_highest_evidence")
        papers_by_title = {paper["title"]: paper for paper in index["papers"]}

        self.assertEqual(papers_by_title["Shared Paper"]["paper_id"], "P_FULL")
        self.assertEqual(papers_by_title["Shared Paper"]["evidence_level"], "fulltext")

    def test_dedupe_title_prefers_more_complete_record_when_evidence_ties(self):
        index = self.run_collector("--dedupe-title", "prefer_highest_evidence")
        papers_by_title = {paper["title"]: paper for paper in index["papers"]}

        self.assertEqual(papers_by_title["Equal Evidence Paper"]["paper_id"], "P_SAME_COMPLETE")
        self.assertIn("experiments", papers_by_title["Equal Evidence Paper"]["files"])

    def test_unknown_evidence_is_excluded_by_min_evidence_level_by_default(self):
        index = self.run_collector("--min-evidence-level", "title_only")

        self.assertNotIn("P_UNKNOWN", self.paper_ids(index))

    def test_include_unknown_evidence_allows_unknown_with_min_evidence_level(self):
        index = self.run_collector("--min-evidence-level", "title_only", "--include-unknown-evidence")

        self.assertIn("P_UNKNOWN", self.paper_ids(index))

    def test_output_json_includes_filters_field(self):
        index = self.run_collector(
            "--paper-id",
            "P_FULL",
            "--evidence-level",
            "fulltext",
            "--min-evidence-level",
            "fulltext",
            "--include-unknown-evidence",
            "--dedupe-title",
            "prefer_highest_evidence",
        )

        self.assertEqual(
            index["filters"],
            {
                "paper_ids": ["P_FULL"],
                "evidence_levels": ["fulltext"],
                "min_evidence_level": "fulltext",
                "include_unknown_evidence": True,
                "dedupe_title": "prefer_highest_evidence",
                "selected_root": None,
            },
        )

    def test_selected_root_scans_only_that_reader_subdirectory(self):
        selected_root = self.reader_root / "P_FULL"
        index = self.run_collector("--selected-root", str(selected_root))

        self.assertEqual(self.paper_ids(index), ["P_FULL"])
        self.assertEqual(index["filters"]["selected_root"], str(selected_root))


if __name__ == "__main__":
    unittest.main()
