"""Validate shared plugin metadata and optionally build its release ZIP."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"


def validate(tag=None):
    manifests = [
        json.loads((ROOT / path).read_text())
        for path in (
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            "package.json",
        )
    ]
    version = manifests[0]["version"]
    if not re.fullmatch(VERSION_PATTERN, version):
        raise ValueError("Plugin version must be stable SemVer X.Y.Z")
    if any(manifest["version"] != version for manifest in manifests):
        raise ValueError("All three manifest versions must match")
    if any(manifest["name"] != "igor-builder" for manifest in manifests[:2]):
        raise ValueError("Codex and Claude plugin names must match")
    if manifests[0]["skills"] != "./skills/":
        raise ValueError("Codex skill directory must be ./skills/")
    skill = ROOT / "skills/igor-builder/SKILL.md"
    text = skill.read_text()
    frontmatter = text.split("---", 2)
    if len(frontmatter) != 3 or frontmatter[0].strip():
        raise ValueError("Skill needs YAML frontmatter")
    if "name: igor-builder" not in frontmatter[1] or "description:" not in frontmatter[1]:
        raise ValueError("Skill name/description missing")
    for reference in re.findall(r"\]\((references/[^)]+)\)", text):
        if not (skill.parent / reference).is_file():
            raise ValueError(f"Missing skill reference: {reference}")
    if f"## {version}\n" not in (ROOT / "release.md").read_text():
        raise ValueError("release.md needs notes for the current version")
    if tag is not None and tag != f"v{version}":
        raise ValueError("Release tag must match manifest version exactly")
    return version


def package(version):
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"igor-builder-{version}.zip"
    files = [ROOT / ".codex-plugin/plugin.json", ROOT / ".claude-plugin/plugin.json"]
    files.extend(path for path in (ROOT / "skills").rglob("*") if path.is_file())
    files.extend(ROOT / name for name in ("README.md", "release.md"))
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for path in sorted(files):
            if path.is_symlink():
                raise ValueError(f"Symlinks are not allowed in plugin package: {path}")
            bundle.write(path, path.relative_to(ROOT))
    with ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("Invalid ZIP")
        for name in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            if json.loads(bundle.read(name))["version"] != version:
                raise ValueError("Packaged manifest version mismatch")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
    print(f"Built {archive.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Require the exact release tag vX.Y.Z")
    parser.add_argument("--package", action="store_true")
    args = parser.parse_args()
    checked_version = validate(args.tag)
    if args.package:
        package(checked_version)
    print(f"Plugin {checked_version} is valid")
