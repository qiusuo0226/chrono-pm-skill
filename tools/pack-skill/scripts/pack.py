#!/usr/bin/env python3
"""Generic Qoder Skill distribution packer (Python implementation).

Packages any Qoder Skill project into a distribution zip.
Includes ALL project files, excludes only known dev/build artifacts.

Exclusion model: reads pack.ps1 arrays at runtime (single source of truth).
  - $excludeDirs / $excludeFiles / $excludeFilePaths / $includeExceptions
  - Same parsing logic as audit_release.py pack_exclusions()

Naming convention: {BrandName}-Skill-v{version}.zip
  - BrandName: extracted from skill.json displayName (text before first — or ()
  - version: from VERSION file or skill.json version field

Usage:
    python pack.py --skill-root <path>
    python pack.py --skill-root <path> --dry-run
    python pack.py --skill-root <path> --output-dir <path> --exclude docs examples
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Package a Qoder Skill into a distribution zip.")
    p.add_argument("--skill-root", required=True, help="Path to the Skill project root (where SKILL.md lives)")
    p.add_argument("--output-dir", default=None, help="Output directory for the zip (default: skill-root)")
    p.add_argument("--dry-run", action="store_true", help="Preview only, do not create zip")
    p.add_argument("--exclude", nargs="*", default=[], help="Additional directory names to exclude")
    return p.parse_args()


# ── Read version ──────────────────────────────────────────

def read_version(root: Path) -> str:
    version_file = root / "VERSION"
    if version_file.is_file():
        v = version_file.read_text(encoding="utf-8").strip()
        if v:
            return v
    skill_json_path = root / "skill.json"
    if skill_json_path.is_file():
        data = json.loads(skill_json_path.read_text(encoding="utf-8"))
        if data.get("version"):
            return data["version"]
    print("ERROR: Cannot determine version: no VERSION file or skill.json version field", file=sys.stderr)
    sys.exit(1)


# ── Read brand name ───────────────────────────────────────

def read_brand_name(root: Path) -> str:
    """Extract brand name from skill.json displayName.

    Splits on '—' (em-dash) and '(' to get the brand prefix.
    Exits with error if displayName is missing (no guessing).
    """
    skill_json_path = root / "skill.json"
    if not skill_json_path.is_file():
        print("ERROR: skill.json not found", file=sys.stderr)
        sys.exit(1)
    data = json.loads(skill_json_path.read_text(encoding="utf-8"))
    display_name = data.get("displayName")
    if not display_name:
        print("ERROR: skill.json missing 'displayName' field. "
              "Cannot determine brand name — refusing to guess.", file=sys.stderr)
        sys.exit(1)
    # Split on em-dash (—) and open-paren (() — NOT hyphen (-)
    brand = re.split(r'[—\(]', display_name)[0].strip()
    if not brand:
        print(f"ERROR: displayName '{display_name}' yielded empty brand name", file=sys.stderr)
        sys.exit(1)
    return brand


# ── Exclusion model (read from pack.ps1 — single source of truth) ──

def pack_exclusions(root: Path) -> dict:
    """Read exclusion arrays from pack.ps1 at runtime.

    Parses $excludeDirs, $excludeFiles, $excludeFilePaths, $includeExceptions.
    Same approach as audit_release.py pack_exclusions() — single source of truth.
    """
    ps1_path = root / "tools" / "pack-skill" / "scripts" / "pack.ps1"
    if not ps1_path.is_file():
        print(f"ERROR: pack.ps1 not found at {ps1_path}", file=sys.stderr)
        sys.exit(1)
    text = ps1_path.read_text(encoding="utf-8")

    def extract_array(var_name: str) -> list:
        pattern = re.escape(var_name) + r"\s*=\s*@\((.*?)\)"
        m = re.search(pattern, text, re.S)
        return re.findall(r'"([^"]+)"', m.group(1)) if m else []

    return {
        "dirs": extract_array("$excludeDirs"),
        "files": extract_array("$excludeFiles"),
        "paths": extract_array("$excludeFilePaths"),
        "exceptions": extract_array("$includeExceptions"),
    }


def is_excluded_file(rel_path: str, exclusions: dict, extra_exclude_dirs: list) -> bool:
    """Determine if a file should be excluded from the distribution package."""
    rel = rel_path.replace("\\", "/")

    # Exceptions first
    if rel in exclusions["exceptions"]:
        return False

    parts = rel.split("/")

    # Directory segments
    for part in parts[:-1]:
        if part in exclusions["dirs"] or part in extra_exclude_dirs:
            return True

    # File extension
    ext = Path(rel).suffix.lower()
    if ext in (".pyc", ".pyo"):
        return True

    # File name
    if parts[-1] in exclusions["files"]:
        return True

    # Specific file paths
    if rel in exclusions["paths"]:
        return True

    # Archive extensions
    if ext == ".zip" or re.search(r'\.tar\.\w+$', rel):
        return True

    return False


# ── Main ──────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    skill_root = Path(args.skill_root).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else skill_root
    extra_excludes = args.exclude or []

    # Validate
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        print(f"ERROR: Not a Qoder Skill project: SKILL.md not found in {skill_root}", file=sys.stderr)
        return 1

    # Read metadata
    brand = read_brand_name(skill_root)
    version = read_version(skill_root)
    skill_name = "skill"
    skill_json_path = skill_root / "skill.json"
    if skill_json_path.is_file():
        data = json.loads(skill_json_path.read_text(encoding="utf-8"))
        skill_name = data.get("name", "skill")

    # Read exclusions from pack.ps1 (single source of truth)
    exclusions = pack_exclusions(skill_root)

    # Package name
    package_name = f"{brand}-Skill-v{version}"
    zip_name = f"{package_name}.zip"
    zip_path = output_dir / zip_name

    print(f"Detected: {skill_name} ({brand}) v{version} at {skill_root}")

    # Collect files
    skip_dirs = {".git", "__pycache__", ".idea", ".qoder", "node_modules"}
    included_files = []

    for f in sorted(skill_root.rglob("*")):
        if not f.is_file():
            continue
        # Quick skip for common dirs not in exclusion model
        rel = f.relative_to(skill_root)
        parts = rel.parts
        if any(p in skip_dirs for p in parts):
            continue
        rel_str = str(rel).replace("\\", "/")
        if not is_excluded_file(rel_str, exclusions, extra_excludes):
            included_files.append((f, rel_str))

    file_count = len(included_files)
    total_size = sum(f.stat().st_size for f, _ in included_files)

    if args.dry_run:
        print()
        print("=== DRY RUN ===")
        print(f"Skill   : {skill_name} ({brand})")
        print(f"Version : {version}")
        print(f"Files   : {file_count}")
        print(f"Size    : {total_size / 1024:.1f} KB (uncompressed)")
        print(f"Output  : {zip_path}")
        print()
        for _, rel in included_files:
            print(f"  + {rel}")
        return 0

    # Create zip
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fpath, rel in included_files:
            # Put files inside a top-level directory named {package_name}/
            arcname = f"{package_name}/{rel}"
            zf.write(fpath, arcname)

    zip_size = zip_path.stat().st_size
    zip_size_kb = round(zip_size / 1024, 1)

    print()
    print("============================================")
    print("  Skill Distribution Package")
    print("============================================")
    print(f"  Name    : {brand}")
    print(f"  Version : {version}")
    print(f"  Files   : {file_count}")
    print(f"  Zip size: {zip_size_kb} KB")
    print(f"  Output  : {zip_path}")
    print("============================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())
