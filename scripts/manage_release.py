#!/usr/bin/env python3
"""Synchronize the packaged skill and manage repository releases."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_RELATIVE = Path("skills/storyboard-director")
MANAGED_PATHS = (Path("SKILL.md"), Path("VERSION"), Path("agents"), Path("references"))
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def _assert_package_target(root: Path, target: Path) -> None:
    root = root.resolve()
    expected = (root / PACKAGE_RELATIVE).resolve()
    if target.resolve() != expected:
        raise RuntimeError(f"Unexpected package target: {target}")
    target.resolve().relative_to(root)


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    if path.is_file():
        return {path.name: _hash_file(path)}
    return {
        item.relative_to(path).as_posix(): _hash_file(item)
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def sync_package(root: Path = REPO_ROOT) -> None:
    root = root.resolve()
    package = root / PACKAGE_RELATIVE
    _assert_package_target(root, package)
    package.mkdir(parents=True, exist_ok=True)

    for relative in MANAGED_PATHS:
        source = root / relative
        destination = package / relative
        if not source.exists():
            raise FileNotFoundError(f"Canonical source is missing: {source}")

        if source.is_dir():
            if destination.exists():
                _assert_package_target(root, package)
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def sync_issues(root: Path = REPO_ROOT) -> list[str]:
    root = root.resolve()
    package = root / PACKAGE_RELATIVE
    issues: list[str] = []
    for relative in MANAGED_PATHS:
        source = root / relative
        destination = package / relative
        if source.is_file():
            if not destination.is_file():
                issues.append(f"Missing packaged file: {destination.relative_to(root)}")
            elif _hash_file(source) != _hash_file(destination):
                issues.append(f"Packaged file differs: {relative.as_posix()}")
            continue

        source_manifest = _tree_manifest(source)
        destination_manifest = _tree_manifest(destination)
        if source_manifest != destination_manifest:
            missing = sorted(set(source_manifest) - set(destination_manifest))
            extra = sorted(set(destination_manifest) - set(source_manifest))
            changed = sorted(
                key
                for key in set(source_manifest) & set(destination_manifest)
                if source_manifest[key] != destination_manifest[key]
            )
            if missing:
                issues.append(f"Missing from packaged {relative}: {', '.join(missing)}")
            if extra:
                issues.append(f"Extra in packaged {relative}: {', '.join(extra)}")
            if changed:
                issues.append(f"Changed in packaged {relative}: {', '.join(changed)}")
    return issues


def set_version(version: str, root: Path = REPO_ROOT) -> None:
    if not SEMVER_RE.fullmatch(version):
        raise ValueError(f"Version must be semantic x.y.z (optional prerelease): {version}")
    root = root.resolve()
    manifest_path = root / ".codex-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = version
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "VERSION").write_text(version + "\n", encoding="utf-8", newline="\n")


def repository_issues(root: Path = REPO_ROOT) -> list[str]:
    root = root.resolve()
    issues = sync_issues(root)
    version_path = root / "VERSION"
    manifest_path = root / ".codex-plugin/plugin.json"

    if not version_path.is_file():
        issues.append("VERSION file is missing")
    else:
        version = version_path.read_text(encoding="utf-8").strip()
        if not SEMVER_RE.fullmatch(version):
            issues.append(f"VERSION is not valid semantic versioning: {version}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("version") != version:
            issues.append(
                f"plugin.json version {manifest.get('version')!r} does not match VERSION {version!r}"
            )

    skill_path = root / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        issues.append("SKILL.md is missing YAML frontmatter")
    if "\nname: storyboard-director\n" not in skill_text[:1000]:
        issues.append("SKILL.md name must be storyboard-director")
    if "\ndescription:" not in skill_text[:1000]:
        issues.append("SKILL.md is missing its description")

    for reference in sorted(set(re.findall(r"`(references/[^`]+\.md)`", skill_text))):
        if not (root / reference).is_file():
            issues.append(f"Referenced file is missing: {reference}")
    return issues


def check_repository(root: Path = REPO_ROOT) -> None:
    issues = repository_issues(root)
    if issues:
        raise RuntimeError("\n".join(f"- {issue}" for issue in issues))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sync", help="Regenerate the packaged skill from canonical root files")
    subparsers.add_parser("check", help="Verify package synchronization and release metadata")
    release = subparsers.add_parser("release", help="Set a version, sync, and validate")
    release.add_argument("version")
    args = parser.parse_args()

    try:
        if args.command == "sync":
            sync_package()
            print("Packaged skill synchronized from canonical root files.")
        elif args.command == "check":
            check_repository()
            print("Repository version and packaged skill are valid and synchronized.")
        elif args.command == "release":
            set_version(args.version)
            sync_package()
            check_repository()
            print(f"Release {args.version} prepared and packaged skill synchronized.")
    except (FileNotFoundError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
