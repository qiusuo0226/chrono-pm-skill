#!/usr/bin/env python3
"""会话钩子入口：比版本，把已拆标准文件串成链，闸过才改版本号。

超时秒数与 references/20-workspace-version-rules.md 相同：120。
不识别具体项目名称。不是 ChronoPM 目录则立刻退出且不改文件。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _version import SKILL_VERSION  # noqa: E402
from compile_source_digests import compile_workspace  # noqa: E402
from migrate_workspace import _vcmp, stamp_skill_version  # noqa: E402

HOOK_TIMEOUT = 120  # 与 20 号同一数字


def _hook_doc(script: Path) -> dict:
    cmd = f'python "{script}"'
    guard = f'python "{script}" --guard'
    return {
        "SessionStart": [
            {"hooks": [{"type": "command", "command": cmd, "timeout": HOOK_TIMEOUT}]}
        ],
        "PreToolUse": [
            {
                "matcher": "write|search_replace|strreplace|edit|bash|shell|run_terminal_command",
                "hooks": [{"type": "command", "command": guard, "timeout": 10}],
            }
        ],
    }


def install_project_hook(project_root: Path) -> None:
    dest = Path(project_root) / ".grok" / "hooks"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "chronopm-upgrade.json").write_text(
        json.dumps(_hook_doc(Path(__file__).resolve()), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def install_user_hook() -> None:
    if os.environ.get("CHRONOPM_SKIP_USER_HOOK") == "1":
        return
    dest = Path.home() / ".grok" / "hooks"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "chronopm-upgrade.json").write_text(
        json.dumps(_hook_doc(Path(__file__).resolve()), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_version(ai: Path) -> str:
    p = ai / ".skill-version.json"
    if not p.is_file():
        return "unknown"
    try:
        return str(json.loads(p.read_text(encoding="utf-8")).get("skillVersion") or "unknown")
    except (OSError, json.JSONDecodeError):
        return "unknown"


def _is_portfolio(ai: Path) -> bool:
    return (ai / "portfolio").is_dir() and (ai / "projects").is_dir()


def _is_project(ai: Path) -> bool:
    if _is_portfolio(ai):
        return False
    return (ai / ".skill-version.json").is_file() or (ai / "todos").is_dir() or (ai / "wps").is_dir() or (ai / "requirements").is_dir()


def _mode(ai: Path) -> str:
    p = ai / ".skill-version.json"
    if not p.is_file():
        return "single"
    try:
        return str(json.loads(p.read_text(encoding="utf-8")).get("mode") or "single")
    except (OSError, json.JSONDecodeError):
        return "single"


def guard() -> int:
    raw = sys.stdin.read()
    try:
        ev = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0
    blob = json.dumps(ev, ensure_ascii=False)
    if ".skill-version.json" not in blob:
        return 0
    tool = str(ev.get("tool_name") or ev.get("tool") or "").lower()
    write_tool = any(name in tool for name in ("write", "search_replace", "strreplace", "edit"))
    shell_tool = any(name in tool for name in ("bash", "shell", "terminal", "command"))
    shell_write = any(mark in blob for mark in (">", "Set-Content", "Out-File", "write_text"))
    if write_tool or (shell_tool and shell_write):
        print(json.dumps({"decision": "deny", "reason": "版本号只能由升级程序写入"}, ensure_ascii=False))
    return 0


def enforce(root: Path) -> int:
    root = Path(root).resolve()
    ai = root / "ai" if (root / "ai").is_dir() else root
    project = ai.parent if ai.name == "ai" else root
    if not (project / "ai").is_dir():
        print("SKIP 不是 ChronoPM 工作区")
        return 0
    ai = project / "ai"
    if _is_portfolio(ai):
        print("集根不编页")
        worst = 0
        blocked = False
        saw = False
        for member in sorted((ai / "projects").iterdir()):
            if not member.is_dir():
                continue
            mai = member / "ai"
            if not (mai / ".skill-version.json").is_file():
                continue
            saw = True
            if _vcmp(SKILL_VERSION, _read_version(mai)) < 0:
                print(f"SKIP 成员技能版本低于工作区 {member.name}")
                blocked = True
                continue
            if enforce(member) != 0:
                worst = 1
        if not saw:
            return 0
        if worst or blocked:
            return worst
        ws = _read_version(ai)
        if _vcmp(SKILL_VERSION, ws) > 0:
            stamp_skill_version(ai, "portfolio", SKILL_VERSION, gates_passed=True)
        return 0
    if not _is_project(ai):
        print("SKIP 不是 ChronoPM 工作区")
        return 0
    ws = _read_version(ai)
    if ws != "unknown" and _vcmp(SKILL_VERSION, ws) < 0:
        print("SKIP 技能版本低于工作区")
        return 0
    install_project_hook(project)
    install_user_hook()
    code = compile_workspace(str(project))
    if code != 0:
        print("存量或 wiki 未完成，不改版本号")
        return code
    if ws == "unknown" or _vcmp(SKILL_VERSION, ws) > 0:
        stamp_skill_version(ai, _mode(ai), SKILL_VERSION, gates_passed=True)
    return 0


def main() -> int:
    if "--guard" in sys.argv:
        return guard()
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    args = p.parse_args()
    return enforce(Path(args.root))


if __name__ == "__main__":
    sys.exit(main())
