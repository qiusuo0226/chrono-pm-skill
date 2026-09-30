#!/usr/bin/env python3
"""只读：D-TODO-01/02/03 结转连续性。对照日=最新合法日 _index。退出 0/1/2。"""
import argparse
import re
import sys
from pathlib import Path


def _ai(root: Path) -> Path:
    ai = root / "ai"
    return ai if ai.exists() else root


def latest_index(todos: Path):
    dates = []
    for d in todos.iterdir():
        if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name) and (d / "_index.md").exists():
            dates.append(d.name)
    if not dates:
        return None
    dates.sort()
    return todos / dates[-1]


def roster(index_md: Path):
    text = index_md.read_text(encoding="utf-8")
    names = []
    in_s1 = False
    for line in text.splitlines():
        if line.startswith("## 1") or "花名册" in line and line.startswith("##"):
            in_s1 = True
            continue
        if in_s1 and line.startswith("## "):
            break
        if in_s1 and line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0] not in ("姓名", "人员", "Name"):
                st = cells[1] if len(cells) > 1 else ""
                if st != "已出组":
                    names.append(cells[0])
    return names


def open_todos(md: Path):
    if not md.exists():
        return []
    text = md.read_text(encoding="utf-8")
    ids = []
    in_core = False
    for line in text.splitlines():
        if "核心执行表" in line:
            in_core = True
            continue
        if in_core and line.startswith("### ") and "核心" not in line:
            break
        if in_core and line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0].startswith("TD-") and len(cells) > 2:
                if cells[2] not in ("已完成", "已取消", "已转出"):
                    ids.append(cells[0])
    return ids


def has_energy(md: Path) -> bool:
    if not md.exists():
        return False
    return "## 0.6" in md.read_text(encoding="utf-8") or "§0.6" in md.read_text(encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--date", default=None, help="今天 YYYY-MM-DD，默认最新日的下一天不猜，用目录内最大日")
    args = p.parse_args()
    ai = _ai(Path(args.root))
    todos = ai / "todos"
    if not todos.exists():
        print("无 todos/，退出 0")
        return 0
    legal = latest_index(todos)
    if not legal:
        print("无合法 _index，退出 2")
        return 2
    names = roster(legal / "_index.md")
    today = args.date or legal.name
    tdir = todos / today
    diffs = []
    for name in names:
        f = tdir / f"{name}.md"
        if not f.exists():
            diffs.append(f"D-TODO-01 应建档 {name} 今日无文件")
            continue
        prev = legal / f"{name}.md"
        if prev.exists():
            old_ids = open_todos(prev)
            new_ids = open_todos(f)
            missing = [i for i in old_ids if i not in new_ids]
            if missing:
                diffs.append(f"D-TODO-02 {name} 未滚存 {missing}")
            if has_energy(prev) and "## 0.6" not in f.read_text(encoding="utf-8"):
                diffs.append(f"D-TODO-03 {name} 缺 §0.6")
    for d in diffs:
        print("DIFF", d)
    if diffs:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
