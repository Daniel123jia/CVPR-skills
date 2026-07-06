import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_ROOT / "skills" / "cvpr-idea-miner"


class CvprIdeaMinerSkillTest(unittest.TestCase):
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
        self.assertIn("title-level preliminary analysis", skill_md)
        self.assertIn("Do not invent methods, experiments, datasets, results, or conclusions", skill_md)

    def test_manifest_declares_idea_workflow_axis_and_core_files(self):
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
            "topic-map": "references/workflows/wf1-topic-map.md",
            "gap-analysis": "references/workflows/wf2-gap-analysis.md",
            "method-recombination": "references/workflows/wf3-method-recombination.md",
            "idea-cards": "references/workflows/wf4-idea-cards.md",
            "experiment-plan": "references/workflows/wf5-experiment-plan.md",
        }
        self.assertIn("axes:", manifest)
        self.assertIn("workflow:", manifest)
        for workflow, path in expected_workflows.items():
            self.assertRegex(manifest, rf"\b{re.escape(workflow)}:\s+{re.escape(path)}")
            self.assertTrue((SKILL_DIR / path).is_file(), path)

        default_pipeline = re.sub(r"\s+", " ", manifest)
        self.assertRegex(
            default_pipeline,
            r"default_full_pipeline:.*topic-map.*gap-analysis.*method-recombination.*idea-cards.*experiment-plan",
        )

    def test_workflow_fragments_define_inputs_steps_outputs_and_anti_hallucination(self):
        workflows_dir = SKILL_DIR / "references" / "workflows"
        for workflow_name in [
            "wf1-topic-map.md",
            "wf2-gap-analysis.md",
            "wf3-method-recombination.md",
            "wf4-idea-cards.md",
            "wf5-experiment-plan.md",
        ]:
            workflow_path = workflows_dir / workflow_name
            self.assertTrue(workflow_path.is_file(), workflow_path)
            content = workflow_path.read_text(encoding="utf-8")
            with self.subTest(workflow=workflow_name):
                for heading in ["## 输入要求", "## 执行步骤", "## 输出格式", "## 反幻觉约束"]:
                    self.assertIn(heading, content)

    def test_core_policy_defines_evidence_levels_and_title_only_limits(self):
        principles = (SKILL_DIR / "static" / "core" / "principles.md").read_text(encoding="utf-8")
        evidence = (SKILL_DIR / "static" / "core" / "evidence-policy.md").read_text(encoding="utf-8")
        output_contract = (SKILL_DIR / "static" / "core" / "output-contract.md").read_text(encoding="utf-8")

        self.assertIn("只做 CVPR 相关研究灵感挖掘", principles)
        self.assertIn("优先使用 cvpr-paper-reader", principles)
        self.assertIn("如果只有 title，只能做粗粒度方向扫描", principles)
        self.assertIn("不能把模型推断当成论文事实", principles)

        for level in ["title_only", "title_abstract", "reader_notes", "fulltext_notes", "user_hypothesis"]:
            self.assertIn(level, evidence)
        for forbidden in ["方法细节", "网络结构", "数据集", "baseline", "实验结果", "ablation", "代码链接", "引用量"]:
            self.assertIn(forbidden, evidence)

        for output_file in [
            "topic_map.md",
            "gap_analysis.md",
            "method_recombination.md",
            "idea_cards.md",
            "experiment_plan.md",
        ]:
            self.assertIn(output_file, output_contract)

    def test_collect_reader_notes_help_runs_without_network(self):
        script = SKILL_DIR / "scripts" / "collect_reader_notes.py"
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--input-dir", result.stdout)
        self.assertIn("--output", result.stdout)
        self.assertIn("reading_note.md", result.stdout)

    def test_collect_reader_notes_indexes_expected_note_files(self):
        script = SKILL_DIR / "scripts" / "collect_reader_notes.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paper_dir = root / "CVPR2026_000001"
            paper_dir.mkdir()
            (paper_dir / "reading_note.md").write_text("# Useful CVPR Paper\n\nnotes", encoding="utf-8")
            (paper_dir / "method.md").write_text("# Method\n\nmethod notes", encoding="utf-8")
            output = root / "reader_notes_index.json"

            result = subprocess.run(
                [sys.executable, str(script), "--input-dir", str(root), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            index = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(index["source_root"], str(root.resolve()))
            self.assertEqual(len(index["papers"]), 1)
            paper = index["papers"][0]
            self.assertEqual(paper["paper_id"], "CVPR2026_000001")
            self.assertEqual(paper["title"], "Useful CVPR Paper")
            self.assertIn("reading_note", paper["files"])
            self.assertIn("method", paper["files"])

    def test_root_docs_metadata_and_evals_include_idea_miner(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        plugin = json.loads((PROJECT_ROOT / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((PROJECT_ROOT / "marketplace.json").read_text(encoding="utf-8"))

        self.assertIn("`cvpr-idea-miner`", readme)
        self.assertIn("多篇论文/阅读笔记的研究灵感挖掘", readme)
        self.assertIn("从这些 CVPR 论文找研究灵感", readme)
        self.assertIn("cvpr-idea-miner", plugin["skills"])
        self.assertIn("idea", marketplace["summary"].lower())
        self.assertIn("research-ideas", marketplace["tags"])

        cases = [
            "idea_from_reader_notes",
            "title_only_idea_warning",
            "method_recombination",
        ]
        for case in cases:
            prompt = PROJECT_ROOT / "evals" / "prompts" / f"{case}.txt"
            expected = PROJECT_ROOT / "evals" / "expected" / f"{case}.md"
            self.assertTrue(prompt.is_file(), prompt)
            self.assertTrue(expected.is_file(), expected)

        reader_notes_expected = (PROJECT_ROOT / "evals" / "expected" / "idea_from_reader_notes.md").read_text(
            encoding="utf-8"
        )
        title_only_expected = (
            PROJECT_ROOT / "evals" / "expected" / "title_only_idea_warning.md"
        ).read_text(encoding="utf-8")
        recombination_expected = (
            PROJECT_ROOT / "evals" / "expected" / "method_recombination.md"
        ).read_text(encoding="utf-8")

        self.assertIn("idea_id", reader_notes_expected)
        self.assertIn("reader_notes", reader_notes_expected)
        self.assertIn("title_only", title_only_expected)
        self.assertIn("不得输出方法细节", title_only_expected)
        self.assertIn("evidence source", recombination_expected)
        self.assertIn("组合想法", recombination_expected)


if __name__ == "__main__":
    unittest.main()
