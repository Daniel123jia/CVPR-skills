import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTest(unittest.TestCase):
    def test_root_readme_names_cvpr_skills_and_single_skill_scope(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue(readme.startswith("# CVPR-skills\n"))
        self.assertIn("一个面向 CVPR main conference papers 的 Codex / Claude Code Agent Skill", readme)
        self.assertIn("当前仓库只包含一个 skill：`conference-cvpr`", readme)
        self.assertNotIn("# ai-conference-skills", readme)
        self.assertNotIn("后续计划扩展 ICCV", readme)

    def test_gitignore_excludes_runtime_artifacts_and_common_binary_outputs(self):
        gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

        for pattern in [".venv/", "__pycache__/", "*.pyc", ".DS_Store", "data/", "outputs/", "logs/", "*.sqlite", "*.db", "*.xlsx"]:
            self.assertIn(pattern, gitignore)

    def test_plugin_and_marketplace_metadata_describe_single_cvpr_skill(self):
        plugin = json.loads((PROJECT_ROOT / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((PROJECT_ROOT / "marketplace.json").read_text(encoding="utf-8"))

        self.assertEqual(plugin["name"], "CVPR-skills")
        self.assertIn("conference-cvpr", plugin["skills"])
        self.assertEqual(marketplace["skill_path"], "skills/conference-cvpr")
        for tag in ["cvpr", "computer-vision", "papers", "metadata", "codex", "claude-code"]:
            self.assertIn(tag, marketplace["tags"])

    def test_eval_prompts_and_expected_routes_exist(self):
        evals = PROJECT_ROOT / "evals"
        cases = [
            "collect_cvpr_2026",
            "export_cvpr_excel",
            "analyze_low_abstract_coverage",
            "reject_non_cvpr",
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


if __name__ == "__main__":
    unittest.main()
