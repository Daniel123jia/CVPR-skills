import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "skills" / "conference-cvpr" / "scripts" / "download_cvf_pdf.py"


def load_downloader():
    if not SCRIPT_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("download_cvf_pdf", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, body=b"%PDF-1.7\nmock", url=None, headers=None, status_code=200):
        self.body = body
        self.url = url or "https://openaccess.thecvf.com/content/CVPR2026/papers/mock.pdf"
        self.headers = headers or {}
        self.status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("HTTP {}".format(self.status_code))

    def iter_content(self, chunk_size=65536):
        for index in range(0, len(self.body), chunk_size):
            yield self.body[index : index + chunk_size]


class FakeSession:
    def __init__(self, response=None):
        self.response = response or FakeResponse()
        self.calls = []
        self.closed = False

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response

    def close(self):
        self.closed = True


class DownloadCvfPdfTest(unittest.TestCase):
    def setUp(self):
        self.downloader = load_downloader()
        if self.downloader is None:
            self.fail("download_cvf_pdf.py must exist")
        self.records = [
            {
                "paper_id": "CVPR2026_000001",
                "title": "SAM 3D Body: Robust Full-Body Human Mesh Recovery",
                "pdf_url": "https://openaccess.thecvf.com/content/CVPR2026/papers/body.pdf",
            },
            {
                "paper_id": "CVPR2026_000002",
                "title": "SAM 3D Human: General Human Mesh Recovery",
                "pdf_url": "https://openaccess.thecvf.com/content/CVPR2026/papers/human.pdf",
            },
        ]

    def test_title_exact_normalized_match_finds_one_paper(self):
        selected = self.downloader.select_records(
            self.records,
            title="  sam 3d body: robust full–body human mesh recovery  ",
        )
        self.assertEqual([record["paper_id"] for record in selected], ["CVPR2026_000001"])

    def test_title_fuzzy_multiple_candidates_requires_paper_id(self):
        with self.assertRaisesRegex(self.downloader.SelectionError, "specify --paper-id") as context:
            self.downloader.select_records(self.records, title="SAM 3D mesh recovery")
        self.assertIn("CVPR2026_000001", str(context.exception))
        self.assertIn("CVPR2026_000002", str(context.exception))

    def test_paper_id_match_resolves_pdf_url(self):
        selected = self.downloader.select_records(self.records, paper_ids=["CVPR2026_000002"])
        self.assertEqual(selected[0]["pdf_url"], self.records[1]["pdf_url"])

    def test_url_must_be_exact_cvf_https_pdf(self):
        accepted = "https://openaccess.thecvf.com/content/CVPR2026/papers/test.pdf?download=1"
        self.assertEqual(self.downloader.validate_cvf_pdf_url(accepted), accepted)
        rejected = [
            "http://openaccess.thecvf.com/content/test.pdf",
            "https://evil.example/test.pdf",
            "https://openaccess.thecvf.com.evil.example/test.pdf",
            "https://user@openaccess.thecvf.com/test.pdf",
            "https://openaccess.thecvf.com:444/test.pdf",
            "https://openaccess.thecvf.com/content/test.zip",
            "https://openaccess.thecvf.com/content/test.pdf#fragment",
        ]
        for url in rejected:
            with self.subTest(url=url):
                with self.assertRaises(self.downloader.UrlPolicyError):
                    self.downloader.validate_cvf_pdf_url(url)

    def test_dry_run_does_not_create_directory_or_call_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "pdfs"
            session = FakeSession()
            result = self.downloader.download_record(
                self.records[0], output_dir, session=session, dry_run=True
            )
            self.assertEqual(result["status"], "dry_run")
            self.assertFalse(output_dir.exists())
            self.assertEqual(session.calls, [])

    def test_existing_pdf_skips_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            target = output_dir / "CVPR2026_000001.pdf"
            target.write_bytes(b"existing")
            session = FakeSession()
            result = self.downloader.download_record(self.records[0], output_dir, session=session)
            self.assertEqual(result["status"], "skipped")
            self.assertEqual(target.read_bytes(), b"existing")
            self.assertEqual(session.calls, [])

    def test_force_atomically_overwrites_existing_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            target = output_dir / "CVPR2026_000001.pdf"
            target.write_bytes(b"old")
            response = FakeResponse(body=b"%PDF-new", url=self.records[0]["pdf_url"])
            result = self.downloader.download_record(
                self.records[0], output_dir, session=FakeSession(response), force=True
            )
            self.assertEqual(result["status"], "downloaded")
            self.assertEqual(target.read_bytes(), b"%PDF-new")

    def test_success_writes_pdf_and_complete_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            body = b"%PDF-1.7\ncontent"
            response = FakeResponse(
                body=body,
                url=self.records[0]["pdf_url"],
                headers={"Content-Length": str(len(body))},
            )
            result = self.downloader.download_record(
                self.records[0], output_dir, session=FakeSession(response)
            )
            target = output_dir / "CVPR2026_000001.pdf"
            sidecar = output_dir / "CVPR2026_000001.pdf.json"
            metadata = json.loads(sidecar.read_text(encoding="utf-8"))

            self.assertEqual(target.read_bytes(), body)
            self.assertEqual(result["bytes"], len(body))
            self.assertEqual(metadata["bytes"], len(body))
            self.assertEqual(metadata["sha256"], result["sha256"])
            self.assertEqual(metadata["source_url"], self.records[0]["pdf_url"])
            self.assertEqual(metadata["source"], "cvf_openaccess")
            self.assertEqual(metadata["downloader_version"], "1.5.0")
            self.assertTrue(metadata["downloaded_at"].endswith("Z"))

    def test_download_record_closes_an_internally_created_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = FakeSession(FakeResponse(url=self.records[0]["pdf_url"]))
            with mock.patch.object(self.downloader.requests, "Session", return_value=session):
                self.downloader.download_record(self.records[0], Path(tmp))
            self.assertTrue(session.closed)

    def test_declared_or_streamed_size_over_limit_leaves_no_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            declared = FakeResponse(
                body=b"small",
                url=self.records[0]["pdf_url"],
                headers={"Content-Length": "1000"},
            )
            with self.assertRaises(self.downloader.DownloadError):
                self.downloader.download_record(
                    self.records[0], output_dir, session=FakeSession(declared), max_bytes=10
                )

            streamed = FakeResponse(body=b"x" * 20, url=self.records[0]["pdf_url"])
            with self.assertRaises(self.downloader.DownloadError):
                self.downloader.download_record(
                    self.records[0], output_dir, session=FakeSession(streamed), max_bytes=10
                )

            self.assertFalse((output_dir / "CVPR2026_000001.pdf").exists())
            self.assertFalse((output_dir / "CVPR2026_000001.pdf.part").exists())
            self.assertFalse((output_dir / "CVPR2026_000001.pdf.json").exists())

    def test_cross_domain_redirect_is_rejected_without_partial_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            response = FakeResponse(body=b"bad", url="https://evil.example/redirected.pdf")
            with self.assertRaises(self.downloader.UrlPolicyError):
                self.downloader.download_record(
                    self.records[0], Path(tmp), session=FakeSession(response)
                )
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_output_filename_uses_sanitized_paper_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = dict(self.records[0], paper_id="../../custom paper:id")
            result = self.downloader.download_record(
                record,
                Path(tmp),
                session=FakeSession(FakeResponse(url=record["pdf_url"])),
            )
            self.assertEqual(Path(result["saved_path"]).name, "custom_paper_id.pdf")
            self.assertTrue((Path(tmp) / "custom_paper_id.pdf").is_file())

    def test_batch_requires_allow_limit_and_explicit_sleep(self):
        parser = self.downloader.build_parser()
        base = [
            "--metadata",
            "papers.json",
            "--paper-id",
            "one",
            "--paper-id",
            "two",
            "--output-dir",
            "pdfs",
        ]
        for extra in [[], ["--allow-batch"], ["--allow-batch", "--limit", "2"]]:
            with self.subTest(extra=extra):
                with self.assertRaises(self.downloader.UsageError):
                    self.downloader.validate_cli_args(parser.parse_args(base + extra))

        args = parser.parse_args(base + ["--allow-batch", "--limit", "2", "--sleep", "1.0"])
        self.downloader.validate_cli_args(args)

    def test_direct_url_requires_one_paper_id_and_no_metadata(self):
        parser = self.downloader.build_parser()
        with self.assertRaises(self.downloader.UsageError):
            self.downloader.validate_cli_args(
                parser.parse_args(
                    ["--pdf-url", self.records[0]["pdf_url"], "--output-dir", "pdfs"]
                )
            )
        args = parser.parse_args(
            [
                "--pdf-url",
                self.records[0]["pdf_url"],
                "--paper-id",
                "custom",
                "--output-dir",
                "pdfs",
            ]
        )
        self.downloader.validate_cli_args(args)

    def test_help_runs(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            cwd=str(PROJECT_ROOT),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for flag in [
            "--metadata",
            "--paper-id",
            "--title",
            "--pdf-url",
            "--allow-batch",
            "--limit",
            "--sleep",
            "--force",
            "--dry-run",
        ]:
            self.assertIn(flag, result.stdout)


if __name__ == "__main__":
    unittest.main()
