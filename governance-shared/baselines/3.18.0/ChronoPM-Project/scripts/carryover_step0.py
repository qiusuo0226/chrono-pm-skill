#!/usr/bin/env python3
"""结转 Step 0 机械段：拷贝后裁剪。日常默认写盘。exit 0 完成；1 写失败；2 不可判仍建档。"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

CLOSED = {"已完成", "已取消", "已转出"}
HDR_NAMES = {"姓名", "人员", "Name"}


def _ai(root: Path) -> Path:
    ai = root / "ai"
    return ai if ai.exists() else root


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _blank(today: str, name: str) -> str:
    return (
        f"---\ndoc_type: personal-daily-todo\nowner: {name}\ndate: {today}\n---\n\n"
        f"# 待办 - {today} - {name}\n\n## 1. 待办清单\n\n### 1.1 核心执行表（8 列）\n\n"
        "| 待办编号 | 标题 | 状态 | 进度 | WP Ref | 计划 Ref | 开始时间 | 结束时间 |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )


H2 = r"^## "
H23 = r"^#{2,3} "


def _span(text: str, start_re: str, end_re: str = H23) -> tuple[int, int, int] | None:
    m = re.search(start_re, text, flags=re.M)
    if not m:
        return None
    rest = text[m.end() :]
    nxt = re.search(end_re, rest, flags=re.M)
    end = m.end() + (nxt.start() if nxt else len(rest))
    return m.start(), m.end(), end


def _replace_body(text: str, start_re: str, new_body: str, end_re: str = H23) -> str:
    sp = _span(text, start_re, end_re)
    if not sp:
        return text
    _s, body0, body1 = sp
    body = new_body if new_body.endswith("\n") else new_body + "\n"
    return text[:body0] + body + text[body1:]


def _body(text: str, start_re: str, end_re: str = H23) -> str:
    sp = _span(text, start_re, end_re)
    return text[sp[1] : sp[2]] if sp else ""


def _open_tds(block: str) -> set[str]:
    keep: set[str] = set()
    for line in block.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = _cells(line)
        if cells and cells[0].startswith("TD-"):
            st = cells[2] if len(cells) > 2 else ""
            if st not in CLOSED:
                keep.add(cells[0])
    return keep


def _filter_table(block: str, keep: set[str], col: int = 0) -> str:
    out = []
    for line in block.splitlines():
        if line.startswith("|") and "---" not in line:
            cells = _cells(line)
            if len(cells) > col and cells[col].startswith("TD-") and cells[col] not in keep:
                continue
        out.append(line)
    return "\n".join(out)


def _filter_notes(block: str, keep: set[str], src_date: str) -> str:
    out = []
    for line in block.splitlines():
        m = re.match(r"^- (TD-\S+)[：:]", line)
        if m:
            if m.group(1) not in keep:
                continue
            if "结转自" not in line:
                line = line.rstrip() + f" | 结转自 {src_date}"
        out.append(line)
    return "\n".join(out)


def _trim_energy(block: str, today: str) -> str:
    cum = re.search(r"累计总能耗：[^\n]+", block)
    line = cum.group(0) if cum else f"累计总能耗：— [能耗单位]（截至 {today}）"
    line = re.sub(r"截至 \d{4}-\d{2}-\d{2}", f"截至 {today}", line)
    return (
        f"\n{line}\n\n"
        "| 日期 | 当日能耗 | 来源 | 备注 | 异常 |\n"
        "|---|---|---|---|---|\n"
        f"| {today} | — | — | — | — |\n"
    )


def _has_daily(text: str) -> bool:
    b = _body(text, r"^## 2\. 日报存档.*$", H2)
    stripped = re.sub(r"^>.*$", "", b, flags=re.M).strip()
    return bool(re.search(r"^### \d{4}-\d{2}-\d{2}", b, flags=re.M)) and len(stripped) > 40


def _asks(text: str, name: str, keep: set[str], src_text: str | None) -> str:
    rows = []
    if re.search(r"同时参与", text) or (src_text and re.search(r"同时参与", src_text)):
        rows.append(f"ASK:SHARE {name}")
    if not keep and (src_text is None or not _has_daily(src_text)):
        rows.append(f"ASK:IDLE {name}")
    return "\n".join(rows)


def _apply_trim(text: str, today: str, src_date: str) -> tuple[str, set[str]]:
    text = re.sub(r"^(date:\s*)\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", text, count=1, flags=re.M)
    text = re.sub(r"(# 待办 - )\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", text, count=1)
    keep = _open_tds(_body(text, r"^### 1\.1.+$"))
    text = _replace_body(text, r"^### 1\.1.+$", "\n" + _filter_table(_body(text, r"^### 1\.1.+$"), keep) + "\n")
    text = _replace_body(text, r"^### 1\.2.+$", "\n" + _filter_table(_body(text, r"^### 1\.2.+$"), keep) + "\n")
    text = _replace_body(text, r"^### 1\.3.+$", "\n" + _filter_table(_body(text, r"^### 1\.3.+$"), keep) + "\n")
    text = _replace_body(text, r"^### 1\.4.+$", "\n" + _filter_notes(_body(text, r"^### 1\.4.+$"), keep, src_date) + "\n")
    text = _replace_body(text, r"^### 1\.5.+$", "\n" + _filter_table(_body(text, r"^### 1\.5.+$"), keep, 0) + "\n")
    text = _replace_body(text, r"^## 0\.6.+$", _trim_energy(_body(text, r"^## 0\.6.+$", H2), today), H2)
    text = _replace_body(text, r"^## 2\. 日报存档.*$", "\n", H2)
    text = _replace_body(text, r"^## 3\. 工作日志.*$", "\n", H2)
    text = _replace_body(text, r"^## 6\. 变更日志.*$", "\n| 时间 | 变更内容 | 原因 |\n|---|---|---|\n", H2)
    text = _replace_body(text, r"^## Revision Log.*$", "\n| Time | Change | Reason | Operator |\n|---|---|---|---|\n", H2)
    return text, keep


def _row_map(block: str, col: int = 0) -> dict[str, str]:
    rows = {}
    for line in block.splitlines():
        if line.startswith("|") and "---" not in line:
            cells = _cells(line)
            if len(cells) > col and cells[col].startswith("TD-"):
                rows[cells[col]] = line
    return rows


def parse_index(index_md: Path) -> tuple[list[str], dict]:
    """§1 花名册：返回应建档姓名（非已出组）与标记字典。"""
    text = index_md.read_text(encoding="utf-8") if index_md.exists() else ""
    names: list[str] = []
    in_s1 = False
    for line in text.splitlines():
        if line.startswith("## 1") or ("花名册" in line and line.startswith("##")):
            in_s1 = True
            continue
        if in_s1 and line.startswith("## "):
            break
        if in_s1 and line.startswith("|") and "---" not in line:
            cells = _cells(line)
            if cells and cells[0] not in HDR_NAMES:
                st = cells[3] if len(cells) > 3 else (cells[1] if len(cells) > 1 else "")
                if "已出组" not in st:
                    names.append(cells[0])
    flags = {"done": bool(re.search(r"carryover_done_for_today.*true", text, re.I))}
    return names, flags


def find_source_file(todos: Path, name: str, today: str) -> Path | None:
    """该人 date≤today 的最新个人 md。"""
    dates = []
    if not todos.exists():
        return None
    for d in todos.iterdir():
        if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name) and d.name <= today:
            f = d / f"{name}.md"
            if f.exists():
                dates.append(d.name)
    if not dates:
        return None
    dates.sort()
    return todos / dates[-1] / f"{name}.md"


def copy_and_trim(src: Path | None, dest: Path, today: str, name: str) -> str:
    """源文件裁剪写入 dest。已有 dest 不覆盖 §2，只补缺失未办结。返回 ASK 片段。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest_text = dest.read_text(encoding="utf-8")
        have = _open_tds(_body(dest_text, r"^### 1\.1.+$")) | set(_row_map(_body(dest_text, r"^### 1\.1.+$")))
        if src is None or not src.exists():
            return _asks(dest_text, name, have, None)
        src_text = src.read_text(encoding="utf-8")
        src_open = _open_tds(_body(src_text, r"^### 1\.1.+$"))
        missing = [td for td in src_open if td not in have]
        if missing:
            add11 = "\n".join(x for t in missing if (x := _row_map(_body(src_text, r"^### 1\.1.+$")).get(t)))
            dest_text = _replace_body(
                dest_text, r"^### 1\.1.+$", _body(dest_text, r"^### 1\.1.+$").rstrip() + "\n" + add11 + "\n"
            )
            add15_map = _row_map(_body(src_text, r"^### 1\.5.+$"))
            add15 = "\n".join(add15_map[t] for t in missing if t in add15_map)
            if add15:
                dest_text = _replace_body(
                    dest_text, r"^### 1\.5.+$", _body(dest_text, r"^### 1\.5.+$").rstrip() + "\n" + add15 + "\n"
                )
            dest.write_text(dest_text, encoding="utf-8")
            have |= set(missing)
        return _asks(dest_text, name, have | src_open, src_text)
    if src is None or not src.exists():
        dest.write_text(_blank(today, name), encoding="utf-8")
        return _asks("", name, set(), None)
    src_text = src.read_text(encoding="utf-8")
    m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", src_text, flags=re.M)
    src_date = m.group(1) if m else today
    text, keep = _apply_trim(src_text, today, src_date)
    dest.write_text(text, encoding="utf-8")
    return _asks(text, name, keep, src_text)


def update_markers(index_md: Path, today: str, names: list[str], ok: list[str], failed: list[str]) -> None:
    text = index_md.read_text(encoding="utf-8") if index_md.exists() else (
        f"---\ndoc_type: daily-todo-binding\ndate: {today}\n---\n\n# 当日待办绑定 - {today}\n"
    )
    if "carryover_done_for_today" in text:
        text = re.sub(r"(carryover_done_for_today[:\s*]*)[^\n]+", r"\1true", text, count=1)
    else:
        text += "\n\n> **carryover_done_for_today**: true\n"
    index_md.parent.mkdir(parents=True, exist_ok=True)
    index_md.write_text(text, encoding="utf-8")


def emit_report(today: str, ok: list[str], failed: list[str], asks: list[str]) -> None:
    print(f"CARRYOVER {today} ok={len(ok)} fail={len(failed)}")
    for n in ok:
        print(f"OK {n}")
    for n in failed:
        print(f"FAIL {n}")
    for a in asks:
        print(a)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--date", default=None)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    today = args.date or dt.date.today().isoformat()
    if args.date and args.date > dt.date.today().isoformat():
        print("REFUSE future date (N-37)")
        return 1
    ai = _ai(Path(args.root))
    todos = ai / "todos"
    if not todos.exists():
        print("无 todos/")
        return 2
    dates = sorted(
        d.name
        for d in todos.iterdir()
        if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name) and d.name <= today
    )
    legal = todos / dates[-1] / "_index.md" if dates else None
    if legal is None or not legal.exists():
        print("无合法 _index")
        return 2
    names, flags = parse_index(legal)
    today_dir = todos / today
    today_idx = today_dir / "_index.md"
    if flags.get("done") and today_idx.exists() and all((today_dir / f"{n}.md").exists() for n in names):
        print("SKIP already done")
        return 0
    if args.dry_run:
        print(f"DRY names={len(names)}")
        return 0
    if legal != today_idx:
        today_dir.mkdir(parents=True, exist_ok=True)
        if not today_idx.exists():
            today_idx.write_text(legal.read_text(encoding="utf-8"), encoding="utf-8")
    ok, failed, asks = [], [], []
    for name in names:
        dest = today_dir / f"{name}.md"
        try:
            src = find_source_file(todos, name, today)
            if src == dest:
                src = None
            a = copy_and_trim(src, dest, today, name)
            if a:
                asks.extend(x for x in a.splitlines() if x)
            ok.append(name)
        except OSError as e:
            failed.append(name)
            print(f"E5 {name} {e}")
    update_markers(today_idx, today, names, ok, failed)
    emit_report(today, ok, failed, asks)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
