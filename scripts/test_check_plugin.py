"""Exercise release gates and archive contents without changing the project."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

import check_plugin


class ReleaseChecks(unittest.TestCase):
    def test_rejects_wrong_tag_and_mismatched_manifests(self):
        with self.assertRaises(ValueError):
            check_plugin.validate("v99.0.0")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (".codex-plugin", ".claude-plugin", "skills"):
                shutil.copytree(check_plugin.ROOT / name, root / name)
            for name in ("package.json", "release.md"):
                shutil.copy(check_plugin.ROOT / name, root / name)
            manifest = root / ".claude-plugin/plugin.json"
            data = json.loads(manifest.read_text())
            data["version"] = "99.0.0"
            manifest.write_text(json.dumps(data))
            with patch.object(check_plugin, "ROOT", root):
                with self.assertRaises(ValueError):
                    check_plugin.validate()

    def test_package_contains_plugin_not_development_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (".codex-plugin", ".claude-plugin", "skills"):
                shutil.copytree(check_plugin.ROOT / name, root / name)
            for name in ("README.md", "release.md", "package.json"):
                shutil.copy(check_plugin.ROOT / name, root / name)
            (root / "private.env").write_text("must stay outside the ZIP")
            with patch.object(check_plugin, "ROOT", root):
                version = check_plugin.validate()
                check_plugin.package(version)
            with ZipFile(root / f"dist/igor-builder-{version}.zip") as archive:
                self.assertIn("skills/igor-builder/SKILL.md", archive.namelist())
                self.assertIn(".claude-plugin/plugin.json", archive.namelist())
                self.assertNotIn("private.env", archive.namelist())
                self.assertNotIn("package.json", archive.namelist())


if __name__ == "__main__":
    unittest.main()
