from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/manage_release.py"
SPEC = importlib.util.spec_from_file_location("manage_release", SCRIPT_PATH)
assert SPEC and SPEC.loader
manage_release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manage_release)


class ManageReleaseTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / ".codex-plugin").mkdir()
        (root / "agents").mkdir()
        (root / "references").mkdir()
        (root / "skills/storyboard-director").mkdir(parents=True)
        (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
        (root / ".codex-plugin/plugin.json").write_text(
            json.dumps({"name": "storyboard-director", "version": "1.0.0"}),
            encoding="utf-8",
        )
        (root / "SKILL.md").write_text(
            "---\nname: storyboard-director\ndescription: test\n---\n"
            "Read `references/director-rules.md`.\n",
            encoding="utf-8",
        )
        (root / "agents/openai.yaml").write_text("interface: {}\n", encoding="utf-8")
        (root / "references/director-rules.md").write_text("rules\n", encoding="utf-8")
        return root

    def test_sync_and_detect_drift(self) -> None:
        root = self.make_repo()
        manage_release.sync_package(root)
        self.assertEqual([], manage_release.sync_issues(root))
        packaged = root / "skills/storyboard-director/SKILL.md"
        packaged.write_text("drift\n", encoding="utf-8")
        self.assertTrue(manage_release.sync_issues(root))

    def test_release_updates_manifest_and_version(self) -> None:
        root = self.make_repo()
        manage_release.set_version("1.1.0", root)
        manage_release.sync_package(root)
        self.assertEqual("1.1.0", (root / "VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(
            "1.1.0",
            (root / "skills/storyboard-director/VERSION").read_text(encoding="utf-8").strip(),
        )
        manifest = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("1.1.0", manifest["version"])

    def test_rejects_invalid_version(self) -> None:
        root = self.make_repo()
        with self.assertRaises(ValueError):
            manage_release.set_version("latest", root)


if __name__ == "__main__":
    unittest.main()
