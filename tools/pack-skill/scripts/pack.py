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

v3.0.0 (G-3) dual-pack: when skill-root contains a ChronoPM-Portfolio/
companion package (has its own SKILL.md), pack.py emits a second zip for it
(ChronoPM-Portfolio-Skill-v{version}.zip). The main package excludes the
companion directory (exclusion model in pack.ps1, single source of truth).

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
from typing import Optional


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

def find_repo_root(skill_root: Path) -> Path:
    """Locate the git/dev repo root that holds tools/pack-skill/scripts/pack.ps1.

    CR-G: skill-root is ChronoPM-Project/ or ChronoPM-Portfolio/; pack.ps1 stays at repo root.
    """
    cur = skill_root.resolve()
    for _ in range(5):
        if (cur / "tools" / "pack-skill" / "scripts" / "pack.ps1").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return skill_root.resolve()


def find_companion(skill_root: Path) -> Optional[Path]:
    """Companion ChronoPM-Portfolio next to ChronoPM-Project, or nested (pre-CR-G)."""
    skill_root = skill_root.resolve()
    sibling = skill_root.parent / "ChronoPM-Portfolio"
    if skill_root.name == "ChronoPM-Project" and (sibling / "SKILL.md").is_file():
        return sibling
    nested = skill_root / "ChronoPM-Portfolio"
    if (nested / "SKILL.md").is_file():
        return nested
    return None


def parse_intentional_exclusions(ps1_text: str) -> list:
    """Parse the 有意排除清单 comment block from pack.ps1 (single source of truth)."""
    m = re.search(
        r"有意排除清单 BEGIN ===\s*(.*?)\s*# === 有意排除清单 END",
        ps1_text,
        re.S,
    )
    rows = []
    if not m:
        return rows
    for line in m.group(1).splitlines():
        line = line.strip().lstrip("#").strip()
        if not line or "|" not in line:
            continue
        path, reason = line.split("|", 1)
        rows.append((path.strip(), reason.strip()))
    return rows


def print_intentional_exclusions(rows: list) -> None:
    """Print 有意排除 table on dry-run and real pack. Missing these files is not a bug."""
    print()
    print("有意排除（产品化裁剪，不是 bug）")
    print("| 路径 | 理由 |")
    print("|---|---|")
    for path, reason in rows:
        print(f"| {path} | {reason} |")
    print("不排除：source-split-skill/（能力目录，必须进包；目录内禁止 SKILL.md）")


def pack_exclusions(ps1_root: Path) -> dict:
    """Read exclusion arrays from pack.ps1 at runtime.

    Parses $excludeDirs, $excludeFiles, $excludeFilePaths, $includeExceptions.
    Same approach as audit_release.py pack_exclusions() — single source of truth.
    ps1_root is the repo root holding tools/pack-skill/scripts/pack.ps1
    (for the companion package this is the parent repo root, not the package dir).
    """
    ps1_path = ps1_root / "tools" / "pack-skill" / "scripts" / "pack.ps1"
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
        "intentional": parse_intentional_exclusions(text),
    }


def is_excluded_file(rel_path: str, exclusions: dict, extra_exclude_dirs: list) -> bool:
    """Determine if a file should be excluded from the distribution package."""
    rel = rel_path.replace("\\", "/")

    # Exceptions first (exact path, or directory prefix ending with "/")
    for exc in exclusions["exceptions"]:
        if rel == exc:
            return False
        if exc.endswith("/"):
            prefix = exc.rstrip("/")
            if rel == prefix or rel.startswith(prefix + "/"):
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

def pack_one(skill_root: Path, ps1_root: Path, output_dir: Path,
             extra_excludes: list, dry_run: bool) -> int:
    """Pack a single Skill project into its distribution zip.

    ps1_root is the repo root holding tools/pack-skill/scripts/pack.ps1;
    for the companion package it is the parent repo root.
    """
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
    exclusions = pack_exclusions(ps1_root)

    # Package name
    package_name = f"{brand}-Skill-v{version}"
    zip_name = f"{package_name}.zip"
    zip_path = output_dir / zip_name

    print(f"Detected: {skill_name} ({brand}) v{version} at {skill_root}")
    print_intentional_exclusions(exclusions.get("intentional") or [])

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

    if dry_run:
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


def main() -> int:
    args = parse_args()

    skill_root = Path(args.skill_root).resolve()
    repo_root = find_repo_root(skill_root)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else repo_root
    extra_excludes = args.exclude or []

    rc = pack_one(skill_root, repo_root, output_dir, extra_excludes, args.dry_run)
    if rc != 0:
        return rc

    # v3.0.0 (G-3) / v3.1.1 (CR-G): auto-detect ChronoPM-Portfolio companion
    companion = find_companion(skill_root)
    if companion is not None:
        print()
        print(">> Companion package detected: ChronoPM-Portfolio — packing second zip")
        rc = pack_one(companion, repo_root, output_dir, extra_excludes, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
