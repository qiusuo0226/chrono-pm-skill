#!/usr/bin/env python3
"""查询热路径：说法表 → 一个文件的哈希。不调用 refresh_views。"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import glossary_table as gt  # noqa: E402


def _ai(root: Path) -> Path:
    root = root.resolve()
    if (root / "ai").is_dir():
        return root / "ai"
    return root


def _portfolio(ai: Path) -> bool:
    return (ai / "portfolio").is_dir() and (ai / "projects").is_dir()


def _load_state(ai: Path) -> dict:
    p = ai / ".state.json"
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _save_state(ai: Path, state: dict) -> None:
    p = ai / ".state.json"
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


def _rows(ai: Path) -> tuple[str, list[dict]]:
    path = ai / "context" / "domain-glossary.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return text, gt.load_rows(text)


def _write_rows(ai: Path, text: str, rows: list[dict]) -> None:
    path = ai / "context" / "domain-glossary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(gt._rewrite(text, rows), encoding="utf-8")


def _live(rows: list[dict]) -> list[dict]:
    return [r for r in rows if (r.get("状态") or "") != "废弃" and (r.get("说法") or "").strip()]


def _resolve_empty(ai: Path, canon: str) -> str:
    canon = (canon or "").strip()
    if not canon:
        return ""
    if canon.startswith("WP-"):
        hits = list((ai / "wps").glob(f"{canon}*.md")) if (ai / "wps").is_dir() else []
        return f"wps/{hits[0].name}" if len(hits) == 1 else ""
    if canon.startswith("PLAN-"):
        hits = list((ai / "plans").glob(f"{canon}*.md")) if (ai / "plans").is_dir() else []
        return f"plans/{hits[0].name}" if len(hits) == 1 else ""
    if not (ai / "wps").is_dir():
        return ""
    named = []
    for p in (ai / "wps").glob("WP-*.md"):
        head = p.read_text(encoding="utf-8")[:500]
        if canon == p.stem or f"# {canon}" in head or canon in head.splitlines()[0:8].__repr__():
            if canon in head:
                named.append(p)
    if len(named) == 1:
        return f"wps/{named[0].name}"
    return ""


def _evidence(ai: Path, rel: str) -> dict:
    empty = {
        "file": rel or None,
        "section": None,
        "req_id": None,
        "source_pointer": None,
        "doc_link": None,
        "wp_id": None,
        "changelog_tail": None,
    }
    if not rel:
        return empty
    path = ai / rel
    if not path.is_file():
        return empty
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"来源指针[:：]\s*(.+)", text)
    if m:
        empty["source_pointer"] = m.group(1).strip()
    m = re.search(r"(?:原型/文档链接|文档链接)[:：]\s*(.+)", text)
    if m:
        empty["doc_link"] = m.group(1).strip()
    m = re.search(r"\b(REQ-[A-Za-z0-9-]+)\b", text)
    if m:
        empty["req_id"] = m.group(1)
    m = re.search(r"\b(WP-[A-Za-z0-9-]+)\b", text)
    if m:
        empty["wp_id"] = m.group(1)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|") and "---" not in ln]
    if "Change Log" in text or "变更" in text:
        tails = [ln for ln in lines if not ln.startswith("| Date") and not ln.startswith("| 日期")]
        if tails:
            empty["changelog_tail"] = tails[-1][:200]
    return empty


def _emit(code: int, payload: dict) -> int:
    print(json.dumps(payload, ensure_ascii=False))
    return code


def locate(ai: Path, text: str) -> int:
    _src, rows = _rows(ai)
    matches = []
    for row in _live(rows):
        speech = row["说法"].strip()
        if speech and speech in text:
            matches.append(row)
    if not matches:
        return _emit(2, {"hits": [], "evidence": [], "ambiguous": False, "candidate_count": 0})
    # 长说法优先，短说法被长说法包含且路径不同则仍算多条
    matches.sort(key=lambda r: len(r["说法"]), reverse=True)
    groups: dict[str, dict] = {}
    for row in matches:
        rel = (row.get("路径") or "").strip()
        if not rel:
            rel = _resolve_empty(ai, row.get("登记名") or "")
            if rel:
                row = dict(row)
                row["路径"] = rel
                _fill_path(ai, row["说法"], rel)
        key = rel or ("#" + (row.get("登记名") or row["说法"]))
        groups.setdefault(key, row)
    if len(groups) != 1:
        hits = [{"path": r.get("路径") or None, "id": r.get("编号"), "speech": r.get("说法"), "canonical": r.get("登记名")} for r in groups.values()]
        return _emit(3, {"hits": hits, "evidence": [], "ambiguous": True, "candidate_count": len(groups)})
    row = next(iter(groups.values()))
    rel = (row.get("路径") or "").strip()
    state = _load_state(ai)
    stamps = state.get("fact_stamps") if isinstance(state.get("fact_stamps"), dict) else {}
    prev = stamps.get(rel) if rel else None
    now = None
    changed = True
    path = ai / rel if rel else None
    if path and path.is_file():
        if rel.endswith("context/domain-glossary.md"):
            now = gt.glossary_stamp_ok(path)
        else:
            now = gt.sha_file(path)
        changed = prev != now
        if changed:
            stamps = dict(stamps)
            stamps[rel] = now
            state["fact_stamps"] = stamps
            _save_state(ai, state)
    hit = {
        "path": rel or None,
        "id": row.get("编号"),
        "speech": row.get("说法"),
        "canonical": row.get("登记名"),
        "changed": changed if rel else None,
        "stamp_prev": prev,
        "stamp_now": now,
    }
    return _emit(0, {"hits": [hit], "evidence": [_evidence(ai, rel)], "ambiguous": False, "candidate_count": 1})


def _fill_path(ai: Path, speech: str, rel: str) -> int:
    text, rows = _rows(ai)
    owners = [r for r in rows if (r.get("说法") or "").strip() == speech.strip()]
    empty = [r for r in owners if not (r.get("路径") or "").strip()]
    if not empty:
        return 0
    if len(owners) != 1:
        return 3
    empty[0]["路径"] = rel
    empty[0]["updated"] = date.today().isoformat()
    _write_rows(ai, text, rows)
    return 0


def register(ai: Path, speech: str, canon: str, rel: str) -> int:
    if not rel:
        return _emit(1, {"error": "路径为空"})
    text, rows = _rows(ai)
    for row in rows:
        if (row.get("说法") or "").strip() == speech and (row.get("登记名") or "").strip() == canon:
            return _emit(0, {"written": False})
    ids = {r.get("编号") for r in rows}
    gid = gt._new_id(ids)
    rows.append(gt._blank({
        "编号": gid,
        "说法": speech,
        "登记名": canon,
        "路径": rel,
        "状态": "pending",
        "来源": "对话登记",
        "热度": "1",
        "首次出现": date.today().isoformat(),
        "updated": date.today().isoformat(),
    }))
    _write_rows(ai, text, rows)
    return _emit(0, {"written": True, "id": gid})


def correct(ai: Path, speech: str, canon: str, rel: str) -> int:
    text, rows = _rows(ai)
    hit = [r for r in rows if (r.get("说法") or "").strip() == speech]
    if len(hit) != 1:
        return _emit(3 if len(hit) > 1 else 2, {"error": "说法不唯一"})
    hit[0]["登记名"] = canon
    if rel:
        hit[0]["路径"] = rel
    hit[0]["来源"] = "用户纠正"
    hit[0]["状态"] = "confirmed"
    hit[0]["updated"] = date.today().isoformat()
    _write_rows(ai, text, rows)
    return _emit(0, {"written": True})


def flush_heat(ai: Path, speeches: list[str]) -> int:
    text, rows = _rows(ai)
    today = date.today().isoformat()
    for speech in speeches:
        for row in rows:
            if (row.get("说法") or "").strip() == speech:
                try:
                    n = int(row.get("热度") or "0")
                except ValueError:
                    n = 0
                row["热度"] = str(n + 1)
                row["最近命中"] = today
    _write_rows(ai, text, rows)
    gloss = ai / "context" / "domain-glossary.md"
    state = _load_state(ai)
    stamps = state.get("fact_stamps") if isinstance(state.get("fact_stamps"), dict) else {}
    rel = "context/domain-glossary.md"
    if gloss.is_file():
        stamps = dict(stamps)
        stamps[rel] = gt.glossary_stamp_ok(gloss)
        state["fact_stamps"] = stamps
        _save_state(ai, state)
    return _emit(0, {"written": True})


def fill_path_cmd(ai: Path, speech: str, rel: str) -> int:
    text, rows = _rows(ai)
    owners = [r for r in rows if (r.get("说法") or "").strip() == speech]
    if len(owners) != 1:
        return _emit(3 if len(owners) > 1 else 2, {"error": "说法不唯一"})
    if (owners[0].get("路径") or "").strip():
        return _emit(0, {"written": False})
    owners[0]["路径"] = rel
    owners[0]["updated"] = date.today().isoformat()
    _write_rows(ai, text, rows)
    return _emit(0, {"written": True})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, required=True)
    ap.add_argument("--text", default="")
    ap.add_argument("--register", action="store_true")
    ap.add_argument("--correct", action="store_true")
    ap.add_argument("--flush-heat", action="store_true")
    ap.add_argument("--fill-path", action="store_true")
    ap.add_argument("--speech", action="append", default=[])
    ap.add_argument("--canonical", default="")
    ap.add_argument("--path", default="")
    args = ap.parse_args(argv)
    ai = _ai(args.project_root)
    if _portfolio(ai):
        return _emit(4, {"error": "集根拒绝"})
    if args.register:
        return register(ai, args.speech[0], args.canonical, args.path)
    if args.correct:
        return correct(ai, args.speech[0], args.canonical, args.path)
    if args.flush_heat:
        return flush_heat(ai, args.speech)
    if args.fill_path:
        return fill_path_cmd(ai, args.speech[0], args.path)
    return locate(ai, args.text)


if __name__ == "__main__":
    sys.exit(main())
