import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTest(unittest.TestCase):
    def test_root_readme_names_cvpr_skills_and_cvpr_only_scope(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue(readme.startswith("# CVPR-skills\n"))
        self.assertIn("一个面向 CVPR main conference papers 的 Codex / Claude Code Agent Skill", readme)
        self.assertIn("当前仓库只做 CVPR-skills", readme)
        self.assertIn("`conference-cvpr`", readme)
        self.assertIn("`cvpr-paper-reader`", readme)
        self.assertNotIn("# ai-conference-skills", readme)
        self.assertNotIn("后续计划扩展 ICCV", readme)

    def test_gitignore_excludes_runtime_artifacts_and_common_binary_outputs(self):
        gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

        for pattern in [".venv/", "__pycache__/", "*.pyc", ".DS_Store", "data/", "outputs/", "logs/", "*.pdf", "*.sqlite", "*.db", "*.xlsx"]:
            self.assertIn(pattern, gitignore)

    def test_requirements_pin_pypdf_to_python37_compatible_range(self):
        requirements = (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8")

        self.assertIn("pypdf>=3.17.4,<4.0", requirements.splitlines())

    def test_plugin_and_marketplace_metadata_describe_cvpr_skills(self):
        plugin = json.loads((PROJECT_ROOT / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((PROJECT_ROOT / "marketplace.json").read_text(encoding="utf-8"))

        self.assertEqual(plugin["name"], "CVPR-skills")
        self.assertIn("conference-cvpr", plugin["skills"])
        self.assertIn("cvpr-paper-reader", plugin["skills"])
        self.assertEqual(marketplace["skill_path"], "skills/conference-cvpr")
        self.assertIn("paper reading", marketplace["summary"])
        for tag in ["cvpr", "computer-vision", "papers", "metadata", "codex", "claude-code"]:
            self.assertIn(tag, marketplace["tags"])

    def test_eval_prompts_and_expected_routes_exist(self):
        evals = PROJECT_ROOT / "evals"
        cases = [
            "collect_cvpr_2026",
            "export_cvpr_excel",
            "analyze_low_abstract_coverage",
            "reject_non_cvpr",
            "read_single_cvpr_paper",
            "method_extraction",
            "abstract_only_warning",
        ]
        for case in cases:
            self.assertTrue((evals / "prompts" / f"{case}.txt").is_file(), case)
            self.assertTrue((evals / "expected" / f"{case}.md").is_file(), case)

        self.assertIn(
            "collect-cvf -> normalize-metadata -> export-artifacts -> completeness-check",
            (evals / "expected" / "collect_cvpr_2026.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "title-based preliminary scan",
            (evals / "expected" / "analyze_low_abstract_coverage.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "v1 only supports CVPR main conference papers",
            (evals / "expected" / "reject_non_cvpr.md").read_text(encoding="utf-8"),
        )

    def test_v11_usage_docs_and_examples_include_run_pipeline(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        tools = (
            PROJECT_ROOT / "skills" / "conference-cvpr" / "static" / "core" / "tools.md"
        ).read_text(encoding="utf-8")

        self.assertIn("run_pipeline.py", readme)
        self.assertIn("高级用法", readme)
        self.assertIn("run_pipeline.py", tools)
        self.assertIn("普通用户优先使用", tools)

        sample_commands = PROJECT_ROOT / "examples" / "sample_commands.md"
        sample_papers = PROJECT_ROOT / "examples" / "sample_cvpr_2026_5_papers.md"
        self.assertTrue(sample_commands.is_file())
        self.assertTrue(sample_papers.is_file())
        self.assertIn("run_pipeline.py --year 2026", sample_commands.read_text(encoding="utf-8"))
        sample_text = sample_papers.read_text(encoding="utf-8")
        self.assertIn("paper_id", sample_text)
        self.assertIn("CVPR2026_000001", sample_text)
        self.assertNotIn("4068", sample_text)

    def test_root_readme_has_distinct_skill_navigator(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Skill Navigator", readme)
        self.assertIn("conference-cvpr", readme)
        self.assertIn("一键完整流程", readme)
        self.assertIn("采集 → 清洗 → 导出 → 检查", readme)
        self.assertIn("只支持 CVPR main conference papers", readme)
        self.assertIn("run_pipeline.py --year 2026", readme)
        self.assertNotIn("| 技能 | 状态 | 用途 | 触发词 |", readme)

    def test_research_analysis_declares_three_grounding_modes(self):
        workflow = (
            PROJECT_ROOT
            / "skills"
            / "conference-cvpr"
            / "references"
            / "workflows"
            / "wf5-research-analysis.md"
        ).read_text(encoding="utf-8")

        for mode in ["title_only", "title_abstract", "fulltext_assisted"]:
            self.assertIn(mode, workflow)
        self.assertIn("abstract_coverage < 5%", workflow)
        self.assertIn("abstract_coverage >= 50%", workflow)
        self.assertIn("用户提供了全文文本", workflow)

    def test_v143_collect_reader_notes_help_lists_quality_filters(self):
        script = PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "scripts" / "collect_reader_notes.py"
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        for flag in [
            "--paper-id",
            "--evidence-level",
            "--min-evidence-level",
            "--include-unknown-evidence",
            "--dedupe-title",
            "--selected-root",
        ]:
            self.assertIn(flag, result.stdout)
        self.assertIn("required unless --selected-root is provided", result.stdout)

    def test_v143_quality_docs_and_evals_exist(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        paper_reader_contract = (
            PROJECT_ROOT / "skills" / "cvpr-paper-reader" / "static" / "core" / "output-contract.md"
        ).read_text(encoding="utf-8")
        paper_reader_readme = (
            PROJECT_ROOT / "skills" / "cvpr-paper-reader" / "README.md"
        ).read_text(encoding="utf-8")
        idea_contract = (
            PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "static" / "core" / "output-contract.md"
        ).read_text(encoding="utf-8")
        idea_workflow = (
            PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "references" / "workflows" / "wf1-topic-map.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Quality Guards", readme)
        self.assertIn("--selected-root outputs/computer_vision/cvpr/reader/{paper_id}", readme)
        self.assertIn("--input-dir outputs/computer_vision/cvpr/reader", readme)
        self.assertIn("Numeric Extraction Confidence", paper_reader_contract)
        self.assertIn("reproduction_checklist.md", paper_reader_contract)
        self.assertIn("reproduction_checklist.md", paper_reader_readme)
        self.assertIn("feasibility_score", idea_contract)
        self.assertIn("single-paper", idea_workflow)
        self.assertIn("local topic map", idea_workflow)

        for case in [
            "reader_notes_filtering_and_dedupe",
            "numeric_extraction_confidence",
            "single_paper_topic_map_boundary",
            "idea_feasibility_fields",
        ]:
            self.assertTrue((PROJECT_ROOT / "evals" / "prompts" / "{}.txt".format(case)).is_file(), case)
            self.assertTrue((PROJECT_ROOT / "evals" / "expected" / "{}.md".format(case)).is_file(), case)

    def test_v145_reproduction_checklist_integration_contract(self):
        script = (
            PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "scripts" / "collect_reader_notes.py"
        ).read_text(encoding="utf-8")
        reader_contract = (
            PROJECT_ROOT / "skills" / "cvpr-paper-reader" / "static" / "core" / "output-contract.md"
        ).read_text(encoding="utf-8")
        idea_contract = (
            PROJECT_ROOT / "skills" / "cvpr-idea-miner" / "static" / "core" / "output-contract.md"
        ).read_text(encoding="utf-8")
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn('"reproduction_checklist": "reproduction_checklist.md"', script)
        self.assertIn("optional reader artifact", reader_contract)
        self.assertIn("reproduction_checklist", idea_contract)
        self.assertIn("evidence source", idea_contract)
        self.assertIn("`reproduction_checklist.md` is an optional reader artifact", readme)

        case = "reproduction_checklist_integration"
        self.assertTrue((PROJECT_ROOT / "evals" / "prompts" / "{}.txt".format(case)).is_file())
        self.assertTrue((PROJECT_ROOT / "evals" / "expected" / "{}.md".format(case)).is_file())

    def test_v15_optional_cvf_pdf_download_contract(self):
        script = PROJECT_ROOT / "skills" / "conference-cvpr" / "scripts" / "download_cvf_pdf.py"
        workflow = (
            PROJECT_ROOT
            / "skills"
            / "conference-cvpr"
            / "references"
            / "workflows"
            / "wf6-download-cvf-pdf.md"
        )
        manifest = (PROJECT_ROOT / "skills" / "conference-cvpr" / "manifest.yaml").read_text(encoding="utf-8")
        skill = (PROJECT_ROOT / "skills" / "conference-cvpr" / "SKILL.md").read_text(encoding="utf-8")
        conference_readme = (
            PROJECT_ROOT / "skills" / "conference-cvpr" / "README.md"
        ).read_text(encoding="utf-8")
        root_readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        tools = (
            PROJECT_ROOT / "skills" / "conference-cvpr" / "static" / "core" / "tools.md"
        ).read_text(encoding="utf-8")
        routing = (
            PROJECT_ROOT / "skills" / "conference-cvpr" / "static" / "core" / "routing-and-ops.md"
        ).read_text(encoding="utf-8")
        ci = (PROJECT_ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")

        self.assertTrue(script.is_file())
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(workflow.is_file())
        self.assertIn("version: 1.5.0", manifest)
        self.assertIn("download-cvf-pdf", manifest)
        self.assertIn("wf6-download-cvf-pdf.md", manifest)
        self.assertIn("download-cvf-pdf", skill)
        self.assertIn("optional PDF download", root_readme)
        self.assertIn("No automatic full-conference PDF download", root_readme)
        self.assertIn(
            "metadata match -> optional PDF download -> extract text -> paper-reader -> idea-miner",
            root_readme,
        )
        self.assertIn("optional PDF download", conference_readme)
        self.assertIn("download results are runtime artifacts", tools)
        self.assertIn("explicit user request", routing)
        self.assertIn("download_cvf_pdf.py --help", ci)

        case = "optional_pdf_download_workflow"
        prompt = PROJECT_ROOT / "evals" / "prompts" / "{}.txt".format(case)
        expected = PROJECT_ROOT / "evals" / "expected" / "{}.md".format(case)
        self.assertTrue(prompt.is_file())
        self.assertTrue(expected.is_file())
        expected_text = expected.read_text(encoding="utf-8")
        for phrase in [
            "optional and explicit",
            "CVF Open Access URLs",
            "No automatic full-conference PDF download",
            "No code repository download",
            "runtime artifacts",
            "does not replace the evidence policy",
        ]:
            self.assertIn(phrase, expected_text)

    def test_v151_root_readme_documentation_polish_contract(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        required_phrases = [
            "CVPR-skills",
            "conference-cvpr",
            "cvpr-paper-reader",
            "cvpr-idea-miner",
            "optional CVF PDF download",
            "Validated Cases",
            "Evidence Levels",
            "Quality Guards",
            "Scope and Non-goals",
            "outputs/computer_vision/cvpr/2026/cvpr_2026_papers.json",
            "no automatic full-conference PDF download",
            "reproduction_checklist.md",
            "Numeric Extraction Confidence",
            "paper_id",
            "title",
            "pdf_url",
            "local PDF",
            "Runtime artifacts",
            "DirectFisheye-GS",
            "SAM3DBody",
            "91 tests OK",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, readme)

        self.assertNotIn(
            "outputs/computer_vision/cvpr/normalized/cvpr_2026_papers.json",
            readme,
        )

    def test_v151_root_readme_has_bilingual_layout(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        required_phrases = [
            "English | 中文",
            "中文说明",
            "中文快速导航",
            "面向 CVPR 论文采集、全文精读与研究 idea 挖掘的 Agent Skill 工具箱",
            "从 CVPR 年份开始",
            "从 paper_id / 标题 / pdf_url 开始",
            "从本地 PDF 开始",
            "What Is CVPR-skills? / CVPR-skills 是什么？",
            "What Can It Do? / 它能做什么？",
            "End-to-End Workflows / 端到端工作流",
            "Evidence Levels / 证据等级",
            "Quality Guards / 质量护栏",
            "Scope and Non-goals / 项目边界",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, readme)


if __name__ == "__main__":
    unittest.main()
