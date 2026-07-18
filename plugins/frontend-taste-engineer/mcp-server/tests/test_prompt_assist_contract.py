import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PLUGIN_ROOT.parents[1]


class PromptAssistContractTests(unittest.TestCase):
    def test_manifest_exposes_prompt_assist_in_the_composer(self) -> None:
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        interface = manifest["interface"]
        icon = PLUGIN_ROOT / interface["composerIcon"]

        self.assertTrue(icon.is_file())
        self.assertIn("rough frontend", interface["shortDescription"].lower())
        self.assertTrue(
            any("polish" in prompt.lower() and "run" in prompt.lower() for prompt in interface["defaultPrompt"])
        )
        self.assertTrue(
            any("rewrite" in prompt.lower() and "do not run" in prompt.lower() for prompt in interface["defaultPrompt"])
        )

    def test_skill_defaults_to_polish_and_run_without_claiming_setting_changes(self) -> None:
        skill = (
            PLUGIN_ROOT / "skills" / "frontend-taste-engineer" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Prompt assist and execution routing", skill)
        self.assertIn("default to **polish and run**", skill)
        self.assertIn("If the user explicitly asks to **rewrite only**", skill)
        self.assertIn("leave them unpinned so Codex can choose automatically", skill)
        self.assertIn("Never silently enable Fast mode", skill)
        self.assertIn("Treat Plan mode as a caller-owned UI mode", skill)
        self.assertIn("persisted goal only when the user explicitly requests", skill)

    def test_prompt_routing_reference_preserves_privacy_and_user_control(self) -> None:
        routing = (
            PLUGIN_ROOT
            / "skills"
            / "frontend-taste-engineer"
            / "references"
            / "prompt-intake-and-routing.md"
        ).read_text(encoding="utf-8")
        agent = (
            PLUGIN_ROOT
            / "skills"
            / "frontend-taste-engineer"
            / "agents"
            / "openai.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("Keep both the raw and normalized prompt request-local", routing)
        self.assertIn("do not receive a supported action for mutating unsent composer text", routing)
        self.assertIn("allow_implicit_invocation: true", agent)
        self.assertNotIn("model:", agent)
        self.assertNotIn("model_reasoning_effort:", agent)

    def test_readme_keeps_install_to_one_copy_paste_command(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        command = (
            "codex plugin marketplace add arnavsri993/frontend-taste-engineer --ref main "
            "&& codex plugin add frontend-taste-engineer@personal"
        )

        self.assertIn(command, readme)


if __name__ == "__main__":
    unittest.main()
