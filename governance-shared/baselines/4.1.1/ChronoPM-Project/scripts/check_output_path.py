#!/usr/bin/env python3
"""出文件路径裁决。只判断，不建目录。

名单读 references/11-output-artifact-rules.md 的标记块，不在本文件写死路径。
退出码：0 ALLOW，2 REMAP，3 DENY。
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
POLICY = HERE.parent / "references" / "11-output-artifact-rules.md"
START = "<!-- output-path-policy:start -->"
END = "<!-- output-path-policy:end -->"


def _policy_rows(text: str) -> list[tuple[str, str]] | None:
    if START not in text or END not in text:
        return None
    block = text.split(START, 1)[1].split(END, 1)[0]
    rows: list[tuple[str, str]] = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[0]) <= {"-", ":"} or cells[0] in ("裁决",):
            continue
        if all(set(c) <= {"-", ":"} for c in cells):
            continue
        verdict = cells[0].upper()
        if verdict not in ("ALLOW", "REMAP", "DENY"):
            continue
        rows.append((verdict, cells[1].strip().strip("`")))
    return rows


def _rel(root: Path, path: Path) -> str | None:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    return rel.as_posix()


def judge(root: Path, path: Path, rows: list[tuple[str, str]], batch: str | None) -> tuple[int, str]:
    if not rows:
        return 3, "DENY 名单没有可用裁决行"
    rel = _rel(root, path)
    if rel is None or rel.startswith("../") or rel == "..":
        return 3, "DENY 工作区以外"
    allow_prefixes = [target.rstrip("/") + "/" for verdict, target in rows if verdict == "ALLOW" and target.endswith("/")]
    allow_exact = [target for verdict, target in rows if verdict == "ALLOW" and not target.endswith("/")]
    if rel in allow_exact or any(rel.startswith(prefix) for prefix in allow_prefixes):
        return 0, f"ALLOW {rel}"
    deny_tokens = {target for verdict, target in rows if verdict == "DENY"}
    remap_tokens = {target for verdict, target in rows if verdict == "REMAP"}
    parent = path.resolve().parent
    at_root = parent == root.resolve()
    under_ai = rel == "ai" or rel.startswith("ai/")
    if under_ai and "ai-fact-source" in deny_tokens:
        return 3, "DENY ai 下除允许路径以外"
    if rel.startswith("ai/") and not any(rel.startswith(p) for p in allow_prefixes) and rel not in allow_exact:
        if "ai-fact-source" in deny_tokens:
            return 3, "DENY ai 下除允许路径以外"
    if at_root and ({"workspace-root-file", "beside-ai"} & remap_tokens):
        stamp = batch or datetime.now().strftime("%Y%m%d%H%M%S")
        return 2, f"ai/outputs/{stamp}/{path.name}"
    if "outside-workspace" in deny_tokens and rel is None:
        return 3, "DENY 工作区以外"
    return 3, "DENY 不在允许路径"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--batch", default=None)
    p.add_argument("--policy", default=None)
    args = p.parse_args()
    policy_path = Path(args.policy) if args.policy else POLICY
    if not policy_path.is_file():
        print("DENY 找不到路径名单")
        return 3
    rows = _policy_rows(policy_path.read_text(encoding="utf-8"))
    if rows is None:
        print("DENY 名单标记缺失")
        return 3
    root = Path(args.root)
    target = Path(args.path)
    if not target.is_absolute():
        target = root / target
    code, line = judge(root, target, rows, args.batch)
    print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
