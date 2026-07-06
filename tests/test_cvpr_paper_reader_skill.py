import re
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_ROOT / "skills" / "cvpr-paper-reader"


class CvprPaperReaderSkillTest(unittest.TestCase):
    def test_skill_md_is_router_with_evidence_guardrails(self):
        skill_md_path = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md_path.is_file())

        skill_md = skill_md_path.read_text(encoding="utf-8")
        self.assertIn("Router", skill_md)
        self.assertIn("Read `manifest.yaml`", skill_md)
        self.assertIn("Read every file listed under `always_load`", skill_md)
        self.assertIn("Detect one or more workflow values", skill_md)
        self.assertIn("Do not read every workflow by default", skill_md)
        self.assertIn("directly usable Markdown file", skill_md)
        self.assertIn("Do not invent methods, experiments, datasets, results, or conclusions", skill_md)

    def test_manifest_declares_reader_workflow_axis_and_core_files(self):
        manifest_path = SKILL_DIR / "manifest.yaml"
        self.assertTrue(manifest_path.is_file())
        manifest = manifest_path.read_text(encoding="utf-8")

        for core in [
            "static/core/principles.md",
            "static/core/evidence-policy.md",
            "static/core/workflow.md",
            "static/core/output-contract.md",
        ]:
            self.assertIn(core, manifest)
            self.assertTrue((SKILL_DIR / core).is_file(), core)

        expected_workflows = {
            "paper-summary": "references/workflows/wf1-paper-summary.md",
            "method-extraction": "references/workflows/wf2-method-extraction.md",
            "experiment-table": "references/workflows/wf3-experiment-table.md",
            "limitations-and-ideas": "references/workflows/wf4-limitations-and-ideas.md",
            "reading-note": "references/workflows/wf5-reading-note.md",
        }
        self.assertIn("axes:", manifest)
        self.assertIn("workflow:", manifest)
        for workflow, path in expected_workflows.items():
            self.assertRegex(manifest, rf"\b{re.escape(workflow)}:\s+{re.escape(path)}")
            self.assertTrue((SKILL_DIR / path).is_file(), path)

        default_pipeline = re.sub(r"\s+", " ", manifest)
        self.assertRegex(
            default_pipeline,
            r"default_full_pipeline:.*paper-summary.*method-extraction.*experiment-table.*limitations-and-ideas.*reading-note",
        )

    def test_workflow_fragments_define_inputs_steps_outputs_and_anti_hallucination(self):
        workflows_dir = SKILL_DIR / "references" / "workflows"
        for workflow_path in sorted(workflows_dir.glob("wf*.md")):
            content = workflow_path.read_text(encoding="utf-8")
            with self.subTest(workflow=workflow_path.name):
                for heading in ["## 输入要求", "## 执行步骤", "## 输出格式", "## 反幻觉约束"]:
                    self.assertIn(heading, content)

    def test_core_policy_defines_evidence_levels_and_title_only_limits(self):
        principles = (SKILL_DIR / "static" / "core" / "principles.md").read_text(encoding="utf-8")
        evidence = (SKILL_DIR / "static" / "core" / "evidence-policy.md").read_text(encoding="utf-8")

        self.assertIn("只做 CVPR 论文精读", principles)
        self.assertIn("如果只有 title，不做细节分析", principles)
        self.assertIn("如果只有 title + abstract，只能做 preliminary summary", principles)
        self.assertIn("如果有全文文本，才可以做方法、实验、局限性和灵感分析", principles)

        for level in ["title_only", "abstract_only", "fulltext", "user_provided_notes"]:
            self.assertIn(level, evidence)
        for forbidden in ["方法细节", "网络结构", "数据集", "baseline", "实验结果", "ablation", "引用量"]:
            self.assertIn(forbidden, evidence)

    def test_pdf_text_extractor_help_runs_without_network(self):
        script = SKILL_DIR / "scripts" / "extract_pdf_text.py"
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--pdf", result.stdout)
        self.assertIn("--output", result.stdout)
        self.assertIn("OCR", result.stdout)

    def test_reader_eval_prompts_and_expected_outputs_exist(self):
        cases = [
            "read_single_cvpr_paper",
            "method_extraction",
            "abstract_only_warning",
        ]
        for case in cases:
            prompt = PROJECT_ROOT / "evals" / "prompts" / f"{case}.txt"
            expected = PROJECT_ROOT / "evals" / "expected" / f"{case}.md"
            self.assertTrue(prompt.is_file(), prompt)
            self.assertTrue(expected.is_file(), expected)

        fulltext_expected = (PROJECT_ROOT / "evals" / "expected" / "read_single_cvpr_paper.md").read_text(
            encoding="utf-8"
        )
        abstract_expected = (PROJECT_ROOT / "evals" / "expected" / "abstract_only_warning.md").read_text(
            encoding="utf-8"
        )
        method_expected = (PROJECT_ROOT / "evals" / "expected" / "method_extraction.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("fulltext", fulltext_expected)
        self.assertIn("preliminary", abstract_expected)
        self.assertIn("不能输出方法和实验细节", abstract_expected)
        self.assertIn("title_only", method_expected)
        self.assertIn("不得生成方法、网络结构、实验或结果细节", method_expected)


if __name__ == "__main__":
    unittest.main()
