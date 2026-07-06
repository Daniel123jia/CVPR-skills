import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_ROOT / "skills" / "conference-cvpr"


class CvprSkillRouterTest(unittest.TestCase):
    def test_manifest_uses_nature_academic_search_router_shape(self):
        manifest = (SKILL_DIR / "manifest.yaml").read_text(encoding="utf-8")

        self.assertIn("always_load:", manifest)
        self.assertIn("static/core/tools.md", manifest)
        self.assertIn("static/core/routing-and-ops.md", manifest)
        self.assertIn("axes:", manifest)
        self.assertIn("workflow:", manifest)

        expected_workflows = {
            "collect-cvf": "references/workflows/wf1-collect-cvf.md",
            "normalize-metadata": "references/workflows/wf2-normalize-metadata.md",
            "export-artifacts": "references/workflows/wf3-export-artifacts.md",
            "completeness-check": "references/workflows/wf4-completeness-check.md",
            "research-analysis": "references/workflows/wf5-research-analysis.md",
        }
        for workflow, path in expected_workflows.items():
            self.assertRegex(manifest, rf"\b{re.escape(workflow)}:\s+{re.escape(path)}")
            self.assertTrue((SKILL_DIR / path).is_file(), path)

    def test_skill_md_is_short_router_not_task_body(self):
        skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Read `manifest.yaml`", skill_md)
        self.assertIn("Read every file listed under `always_load`", skill_md)
        self.assertIn("Detect the workflow", skill_md)
        self.assertIn("Load the matching workflow fragment", skill_md)
        self.assertIn("references/workflows/", skill_md)
        self.assertNotIn("static/tasks/", skill_md)

    def test_static_tasks_directory_is_not_used_by_router(self):
        self.assertFalse((SKILL_DIR / "static" / "tasks").exists())

    def test_research_analysis_workflow_has_grounding_guardrails(self):
        workflow = (SKILL_DIR / "references" / "workflows" / "wf5-research-analysis.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("title + abstract", workflow)
        self.assertIn("Do not claim full-paper findings", workflow)
        self.assertIn("Do not invent code links, citation counts, experimental results", workflow)
        self.assertIn("Mark conclusions as preliminary", workflow)
        self.assertIn("metadata coverage gate", workflow.lower())
        self.assertIn("abstract_coverage < 50%", workflow)
        self.assertIn("abstract_coverage < 5%", workflow)
        self.assertIn("title-based preliminary scan", workflow)
        self.assertIn("当前几乎没有摘要，分析仅基于标题，不适合做细粒度技术结论", workflow)


if __name__ == "__main__":
    unittest.main()
