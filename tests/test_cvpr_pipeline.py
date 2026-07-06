import json
import importlib
import subprocess
import sqlite3
import sys
import time
import unittest
from unittest.mock import patch
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "skills" / "conference-cvpr" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_completeness
import collect_cvpr
import export_cvpr
import normalize_cvpr


CVF_LISTING_HTML = """
<html>
  <body>
    <dl>
      <dt class="ptitle"><a href="/content/CVPR2026/html/Smith_Testing_Vision_CVPR_2026_paper.html">Testing Vision Systems</a></dt>
      <dd>Jane Smith, John Doe</dd>
      <dd>
        <a href="/content/CVPR2026/papers/Smith_Testing_Vision_CVPR_2026_paper.pdf">pdf</a>
        <a href="/content/CVPR2026/supplemental/Smith_Testing_Vision_CVPR_2026_supplemental.zip">supp</a>
      </dd>
      <div id="Smith_Testing_Vision_CVPR_2026_paper">
        <div id="abstract">  This paper tests vision systems.  </div>
      </div>
      <dt class="ptitle"><a href="html/Lee_Another_Paper_CVPR_2026_paper.html">Another Paper</a></dt>
      <dd>Alice Lee</dd>
      <dd><a href="papers/Lee_Another_Paper_CVPR_2026_paper.pdf">PDF</a></dd>
      <div id="Lee_Another_Paper_CVPR_2026_paper">
        <div id="abstract">A second abstract.</div>
      </div>
    </dl>
  </body>
</html>
"""


class CvprPipelineTest(unittest.TestCase):
    def test_parse_listing_page_extracts_cvf_fields_with_absolute_urls(self):
        papers = collect_cvpr.parse_listing_page(
            CVF_LISTING_HTML,
            "https://openaccess.thecvf.com/CVPR2026?day=all",
        )

        self.assertEqual(
            papers,
            [
                {
                    "title": "Testing Vision Systems",
                    "authors": ["Jane Smith", "John Doe"],
                    "paper_page_url": "https://openaccess.thecvf.com/content/CVPR2026/html/Smith_Testing_Vision_CVPR_2026_paper.html",
                    "pdf_url": "https://openaccess.thecvf.com/content/CVPR2026/papers/Smith_Testing_Vision_CVPR_2026_paper.pdf",
                    "abstract": "This paper tests vision systems.",
                    "supplementary_url": "https://openaccess.thecvf.com/content/CVPR2026/supplemental/Smith_Testing_Vision_CVPR_2026_supplemental.zip",
                },
                {
                    "title": "Another Paper",
                    "authors": ["Alice Lee"],
                    "paper_page_url": "https://openaccess.thecvf.com/CVPR2026/html/Lee_Another_Paper_CVPR_2026_paper.html",
                    "pdf_url": "https://openaccess.thecvf.com/CVPR2026/papers/Lee_Another_Paper_CVPR_2026_paper.pdf",
                    "abstract": "A second abstract.",
                    "supplementary_url": None,
                },
            ],
        )

    def test_parse_listing_page_scales_to_large_cvf_pages(self):
        parts = ["<html><body><dl>"]
        for index in range(2500):
            identifier = f"Paper_{index}_CVPR_2026_paper"
            parts.append(f'<dt class="ptitle"><a href="html/{identifier}.html">Title {index}</a></dt>')
            parts.append(f"<dd>Author {index}</dd>")
            parts.append(f'<dd><a href="papers/{identifier}.pdf">pdf</a></dd>')
            parts.append(f'<div id="{identifier}"><div id="abstract">Abstract {index}</div></div>')
        parts.append("</dl></body></html>")

        start = time.perf_counter()
        papers = collect_cvpr.parse_listing_page(
            "".join(parts),
            "https://openaccess.thecvf.com/CVPR2026?day=all",
        )
        elapsed = time.perf_counter() - start

        self.assertEqual(len(papers), 2500)
        self.assertLess(elapsed, 6.0)

    def test_normalize_adds_contract_fields_and_stable_ids(self):
        raw = [
            {
                "title": "  Testing   Vision Systems  ",
                "authors": "Jane Smith, John Doe",
                "paper_page_url": "/content/CVPR2026/html/test.html",
                "pdf_url": "/content/CVPR2026/papers/test.pdf",
                "abstract": "  Abstract text. ",
                "supplementary_url": "",
            }
        ]

        normalized = normalize_cvpr.normalize_records(
            raw,
            year=2026,
            base_url="https://openaccess.thecvf.com/CVPR2026",
        )

        paper = normalized[0]
        self.assertEqual(paper["paper_id"], "CVPR2026_000001")
        self.assertEqual(paper["title"], "Testing Vision Systems")
        self.assertEqual(paper["authors"], ["Jane Smith", "John Doe"])
        self.assertEqual(paper["authors_text"], "Jane Smith; John Doe")
        self.assertEqual(paper["conference"], "CVPR")
        self.assertEqual(paper["year"], 2026)
        self.assertEqual(paper["field"], "computer_vision")
        self.assertEqual(paper["source"], "cvf_openaccess")
        self.assertIsNone(paper["doi"])
        self.assertIsNone(paper["citation_count"])
        self.assertIsNone(paper["code_url"])
        self.assertIsNone(paper["project_url"])
        self.assertIsNone(paper["openalex_id"])
        self.assertIsNone(paper["semantic_scholar_id"])
        self.assertIsNone(paper["dblp_key"])
        self.assertEqual(
            paper["paper_page_url"],
            "https://openaccess.thecvf.com/content/CVPR2026/html/test.html",
        )

    def test_collect_does_not_enrich_paper_pages_by_default(self):
        listing_html = """
        <html><body><dl>
          <dt class="ptitle"><a href="/content/CVPR2026/html/test.html">Title</a></dt>
          <dd>Jane Smith</dd>
          <dd><a href="/content/CVPR2026/papers/test.pdf">pdf</a></dd>
        </dl></body></html>
        """

        with patch.object(collect_cvpr, "fetch_url", return_value=listing_html), patch.object(
            collect_cvpr, "enrich_missing_from_paper_pages"
        ) as enrich:
            papers = collect_cvpr.collect_cvpr(2026)

        self.assertEqual(len(papers), 1)
        enrich.assert_not_called()

    def test_collect_can_enrich_paper_pages_when_explicitly_requested(self):
        listing_html = """
        <html><body><dl>
          <dt class="ptitle"><a href="/content/CVPR2026/html/test.html">Title</a></dt>
          <dd>Jane Smith</dd>
          <dd><a href="/content/CVPR2026/papers/test.pdf">pdf</a></dd>
        </dl></body></html>
        """

        with patch.object(collect_cvpr, "fetch_url", return_value=listing_html), patch.object(
            collect_cvpr, "enrich_missing_from_paper_pages"
        ) as enrich:
            papers = collect_cvpr.collect_cvpr(2026, enrich_pages=True)

        self.assertEqual(len(papers), 1)
        enrich.assert_called_once()

    def test_collect_limit_bounds_records_before_enrichment(self):
        listing_html = """
        <html><body><dl>
          <dt class="ptitle"><a href="/content/CVPR2026/html/test1.html">Title 1</a></dt>
          <dd>Jane Smith</dd>
          <dd><a href="/content/CVPR2026/papers/test1.pdf">pdf</a></dd>
          <dt class="ptitle"><a href="/content/CVPR2026/html/test2.html">Title 2</a></dt>
          <dd>John Doe</dd>
          <dd><a href="/content/CVPR2026/papers/test2.pdf">pdf</a></dd>
        </dl></body></html>
        """

        with patch.object(collect_cvpr, "fetch_url", return_value=listing_html), patch.object(
            collect_cvpr, "enrich_missing_from_paper_pages"
        ) as enrich:
            papers = collect_cvpr.collect_cvpr(2026, enrich_pages=True, limit=1, sleep_seconds=0.5)

        self.assertEqual(len(papers), 1)
        enrich.assert_called_once()
        call_args, _ = enrich.call_args
        self.assertEqual(call_args[4], 1)
        self.assertEqual(call_args[5], 0.5)

    def test_export_writes_sqlite_excel_markdown_and_json(self):
        with self.subTest("export files"):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                records = [
                    {
                        "paper_id": "CVPR2026_000001",
                        "title": "Testing Vision Systems",
                        "authors": ["Jane Smith", "John Doe"],
                        "authors_text": "Jane Smith; John Doe",
                        "year": 2026,
                        "conference": "CVPR",
                        "field": "computer_vision",
                        "source": "cvf_openaccess",
                        "abstract": "Abstract text.",
                        "pdf_url": "https://example.com/paper.pdf",
                        "paper_page_url": "https://example.com/paper.html",
                        "supplementary_url": None,
                        "code_url": None,
                        "project_url": None,
                        "doi": None,
                        "citation_count": None,
                        "openalex_id": None,
                        "semantic_scholar_id": None,
                        "dblp_key": None,
                    }
                ]
                normalized_path = tmp_path / "normalized.json"
                normalized_path.write_text(json.dumps(records), encoding="utf-8")
                output_dir = tmp_path / "exports"

                written = export_cvpr.export_records(normalized_path, output_dir, year=2026)

                self.assertTrue(written["sqlite"].exists())
                self.assertTrue(written["excel"].exists())
                self.assertTrue(written["markdown"].exists())
                self.assertTrue(written["json"].exists())

                with sqlite3.connect(written["sqlite"]) as conn:
                    count = conn.execute("select count(*) from papers").fetchone()[0]
                self.assertEqual(count, 1)

                markdown = written["markdown"].read_text(encoding="utf-8")
                self.assertIn("Testing Vision Systems", markdown)
                self.assertIn("Jane Smith; John Doe", markdown)

    def test_completeness_reports_errors_and_warnings(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            records = [
                {
                    "paper_id": "CVPR2026_000001",
                    "title": "Duplicate",
                    "authors": ["Jane Smith"],
                    "paper_page_url": "https://example.com/1",
                    "abstract": "",
                    "pdf_url": "",
                    "supplementary_url": None,
                },
                {
                    "paper_id": "CVPR2026_000002",
                    "title": "Duplicate",
                    "authors": [],
                    "paper_page_url": "",
                    "abstract": "Abstract",
                    "pdf_url": "https://example.com/2.pdf",
                    "supplementary_url": "https://example.com/2.zip",
                },
            ]
            normalized_path = tmp_path / "normalized.json"
            normalized_path.write_text(json.dumps(records), encoding="utf-8")

            report = check_completeness.check_records(normalized_path, tmp_path, year=2026)

            self.assertEqual(report["summary"]["total_papers"], 2)
            self.assertEqual(report["summary"]["error_count"], 3)
            self.assertEqual(report["summary"]["warning_count"], 3)
            self.assertEqual(report["summary"]["coverage"]["abstract_coverage"], 0.5)
            self.assertEqual(report["summary"]["coverage"]["pdf_url_coverage"], 0.5)
            self.assertEqual(report["summary"]["coverage"]["supplementary_url_coverage"], 0.5)
            self.assertEqual(report["summary"]["coverage"]["paper_page_url_coverage"], 0.5)
            self.assertTrue((tmp_path / "completeness_report.md").exists())
            report_text = (tmp_path / "completeness_report.md").read_text(encoding="utf-8")
            self.assertIn("## Coverage Summary", report_text)
            self.assertIn("- abstract_coverage: 50.00%", report_text)
            failed_items = json.loads((tmp_path / "failed_items.json").read_text(encoding="utf-8"))
            self.assertEqual({item["severity"] for item in failed_items}, {"error", "warning"})

    def test_run_pipeline_invokes_default_steps_without_network_in_unit_test(self):
        run_pipeline = importlib.import_module("run_pipeline")

        completed = subprocess.CompletedProcess(args=[], returncode=0)
        with patch.object(run_pipeline.subprocess, "run", return_value=completed) as run, patch("builtins.print"):
            exit_code = run_pipeline.run_pipeline(year=2026)

        self.assertEqual(exit_code, 0)
        command_names = [Path(call_args[0][0][1]).name for call_args in run.call_args_list]
        self.assertEqual(
            command_names,
            ["collect_cvpr.py", "normalize_cvpr.py", "export_cvpr.py", "check_completeness.py"],
        )
        for call_args in run.call_args_list:
            self.assertIn("--year", call_args[0][0])
            self.assertIn("2026", call_args[0][0])

    def test_run_pipeline_passes_enrichment_options_only_to_collect(self):
        run_pipeline = importlib.import_module("run_pipeline")

        completed = subprocess.CompletedProcess(args=[], returncode=0)
        with patch.object(run_pipeline.subprocess, "run", return_value=completed) as run, patch("builtins.print"):
            exit_code = run_pipeline.run_pipeline(
                year=2026,
                enrich_pages=True,
                limit=100,
                sleep_seconds=0.5,
                resume=True,
            )

        self.assertEqual(exit_code, 0)
        collect_command = run.call_args_list[0][0][0]
        self.assertIn("--enrich-pages", collect_command)
        self.assertIn("--limit", collect_command)
        self.assertIn("100", collect_command)
        self.assertIn("--sleep", collect_command)
        self.assertIn("0.5", collect_command)
        self.assertIn("--resume", collect_command)

        for call_args in run.call_args_list[1:]:
            command = call_args[0][0]
            self.assertNotIn("--enrich-pages", command)
            self.assertNotIn("--limit", command)
            self.assertNotIn("--sleep", command)
            self.assertNotIn("--resume", command)

    def test_run_pipeline_stops_on_failed_step(self):
        run_pipeline = importlib.import_module("run_pipeline")

        success = subprocess.CompletedProcess(args=[], returncode=0)
        failure = subprocess.CompletedProcess(args=[], returncode=2)
        with patch.object(run_pipeline.subprocess, "run", side_effect=[success, failure]) as run, patch("builtins.print"):
            exit_code = run_pipeline.run_pipeline(year=2026)

        self.assertEqual(exit_code, 2)
        self.assertEqual(run.call_count, 2)

    def test_run_pipeline_help_works_without_network(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "run_pipeline.py"), "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("--year", result.stdout)
        self.assertIn("--enrich-pages", result.stdout)


if __name__ == "__main__":
    unittest.main()
