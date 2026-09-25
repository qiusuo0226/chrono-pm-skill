#!/usr/bin/env python3
"""说法表：两张各 7 列的表，同在 domain-glossary.md。

第 1 表给查询定位，第 1b 表留类别和备注。单表不超过 7 列。
不把路径写成「对话/文件/系统」。
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

MAIN = ["编号", "说法", "登记名", "路径", "状态", "来源", "热度"]
META = ["编号", "类别", "context_hint", "首次出现", "最近命中", "updated", "备注"]
COLUMNS = MAIN + [c for c in META if c not in MAIN]
OLD_COLUMNS = [
    "编号", "原词", "标准词", "类别", "context_hint", "状态",
    "来源", "首次出现", "最近命中", "命中次数", "备注",
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cells(line: str) -> list[str]:
    raw = line.strip()
    if not raw.startswith("|"):
        return []
    parts = [p.strip() for p in raw.strip("|").split("|")]
    return parts


def _is_sep(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        cells = _cells(line)
        if not cells or _is_sep(cells):
            continue
        rows.append(cells)
    return rows


def section(text: str, title: str) -> str:
    m = re.search(rf"(?m)^##\s+{re.escape(title)}.*$", text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"(?m)^##\s+", rest)
    return rest[: nxt.start()] if nxt else rest


def _blank(row: dict) -> dict:
    return {k: row.get(k, "") or "" for k in COLUMNS}


def row_from_old(cells: list[str], header: list[str]) -> dict:
    src = {header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))}
    heat = src.get("命中次数") or src.get("热度") or "0"
    return _blank({
        "编号": src.get("编号", ""),
        "说法": src.get("原词") or src.get("说法") or "",
        "登记名": src.get("标准词") or src.get("登记名") or "",
        "路径": src.get("路径", ""),
        "类别": src.get("类别") or "—",
        "context_hint": src.get("context_hint", ""),
        "状态": src.get("状态") or "pending",
        "来源": src.get("来源") or "词库",
        "热度": heat or "0",
        "首次出现": src.get("首次出现", ""),
        "最近命中": src.get("最近命中", ""),
        "updated": src.get("updated") or date.today().isoformat(),
        "备注": src.get("备注", ""),
    })


def row_from_header(cells: list[str], header: list[str]) -> dict:
    if header[:3] == ["编号", "说法", "登记名"]:
        src = {header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))}
        return _blank(src)
    return row_from_old(cells, header)


def parse_section_rows(block: str) -> tuple[list[str], list[dict]]:
    rows = table_rows(block)
    if not rows:
        return [], []
    header = rows[0]
    out = []
    for cells in rows[1:]:
        if not any(cells):
            continue
        out.append(row_from_header(cells, header))
    return header, out


def _section_heading(text: str, heading: str) -> str:
    m = re.search(rf"(?m)^##\s+{re.escape(heading)}.*$", text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"(?m)^##\s+", rest)
    return rest[: nxt.start()] if nxt else rest


def load_rows(text: str) -> list[dict]:
    _, rows = parse_section_rows(section(text, "1."))
    _, meta = parse_section_rows(_section_heading(text, "1b."))
    by_id = {r.get("编号"): r for r in meta if r.get("编号")}
    for row in rows:
        extra = by_id.get(row.get("编号"))
        if not extra:
            continue
        for key in META:
            if key != "编号" and extra.get(key):
                row[key] = extra[key]
    return rows


def _one_table(rows: list[dict], cols: list[str]) -> str:
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        lines.append("| " + " | ".join((row.get(c) or "").replace("|", "/") for c in cols) + " |")
    return "\n".join(lines) + "\n"


def render_table(rows: list[dict]) -> str:
    return _one_table(rows, MAIN) + "\n## 1b. 说法附注\n\n" + _one_table(rows, META)


def stamp_glossary_text(text: str) -> str:
    rows = load_rows(text)
    if not rows and "说法" not in text:
        return sha_text(text)
    cloned = []
    for row in rows:
        item = dict(row)
        item["热度"] = ""
        item["最近命中"] = ""
        cloned.append(item)
    return sha_text(render_table(cloned))


def _key(row: dict) -> tuple[str, str]:
    return (row.get("说法") or "").strip(), (row.get("登记名") or "").strip()


def _new_id(existing: set[str]) -> str:
    base = "G-" + date.today().strftime("%Y%m%d") + "-M"
    n = 1
    while True:
        gid = f"{base}{n:04d}"
        if gid not in existing:
            existing.add(gid)
            return gid
        n += 1


def _add(rows: list[dict], seen: set[tuple[str, str]], ids: set[str], row: dict, keys: set[str]) -> None:
    speech = (row.get("说法") or "").strip()
    if speech:
        keys.add(speech)
    k = _key(row)
    if not k[0] and not k[1]:
        return
    if k in seen:
        return
    same_speech = [r for r in rows if (r.get("说法") or "").strip() == k[0] and k[0]]
    if same_speech and any((r.get("登记名") or "").strip() != k[1] for r in same_speech):
        if (row.get("来源") or "") not in ("词库", "manual"):
            row["来源"] = "冲突"
    if not row.get("编号"):
        row["编号"] = _new_id(ids)
    else:
        ids.add(row["编号"])
    rows.append(_blank(row))
    seen.add(k)


def _brain_pairs(text: str) -> list[tuple[str, str]]:
    pairs = []
    for line in text.splitlines():
        if "→" in line:
            left, right = line.split("→", 1)
        elif "->" in line:
            left, right = line.split("->", 1)
        else:
            continue
        speech = re.sub(r"^[\s|\-*]+", "", left).strip()
        target = right.strip().strip("`").split()[0] if right.strip() else ""
        target = target.strip("|").strip()
        if speech and target and speech not in ("说法", "别名"):
            pairs.append((speech, target))
    return pairs


def _wp_inputs(ai: Path):
    import refresh_views as rv
    items = []
    parsed = []
    wps = ai / "wps"
    if not wps.is_dir():
        return items, parsed, rv._successor_id
    for path in sorted(wps.glob("WP-*.md")):
        try:
            rec = rv.parse_wp(path)
        except Exception:
            continue
        parsed.append(rec)
        rel = rec.get("path") or f"wps/{path.name}"
        for alias in rec.get("aliases") or []:
            alias = str(alias).strip()
            if alias and alias not in ("—", "-", "[]"):
                items.append((alias, rec.get("id") or "", rel, rec))
    return items, parsed, rv._successor_id


def _apply_successor(rows: list[dict], parsed: list[dict], successor_id) -> None:
    by_id = {w.get("id"): w for w in parsed if w.get("id")}
    for row in rows:
        rel = row.get("路径") or ""
        wid = ""
        m = re.search(r"(WP-[A-Za-z0-9-]+)", rel) or re.search(r"(WP-[A-Za-z0-9-]+)", row.get("登记名") or "")
        if m:
            wid = m.group(1)
        rec = by_id.get(wid)
        if not rec or rec.get("effect") != "废弃":
            continue
        nxt = successor_id(rec, by_id)
        if nxt and nxt in by_id:
            row["登记名"] = nxt
            row["路径"] = by_id[nxt].get("path") or row["路径"]
            row["updated"] = date.today().isoformat()
        else:
            row["状态"] = "废弃"
            note = row.get("备注") or ""
            if "无后继" not in note:
                row["备注"] = (note + " 无后继").strip()


def input_keys(ai: Path, text: str) -> set[str]:
    keys: set[str] = set()
    for block, speech_i in (("1.", 1),):
        header, rows = parse_section_rows(section(text, "1."))
        if header[:3] == ["编号", "原词", "标准词"]:
            for row in rows:
                if row.get("说法"):
                    keys.add(row["说法"])
        else:
            for row in rows:
                if row.get("说法"):
                    keys.add(row["说法"])
    for row in parse_section_rows(section(text, "2."))[1]:
        speech = row.get("说法") or ""
        # section 2 old layout is remapped poorly; read raw
    raw2 = table_rows(section(text, "2."))
    if raw2 and "错误写法" in raw2[0]:
        for cells in raw2[1:]:
            if len(cells) > 1 and cells[1]:
                keys.add(cells[1])
    raw3 = table_rows(section(text, "3."))
    if raw3 and raw3[0] and raw3[0][0] == "编号" and "术语" in raw3[0]:
        for cells in raw3[1:]:
            if len(cells) > 1 and cells[1]:
                keys.add(cells[1])
    ent = ai / "context" / "active-entities.json"
    if ent.is_file():
        try:
            data = json.loads(ent.read_text(encoding="utf-8"))
            for k in (data.get("alias_index") or {}):
                if str(k).strip():
                    keys.add(str(k).strip())
        except json.JSONDecodeError:
            pass
    brain = ai / "context" / "brain.md"
    if brain.is_file():
        for speech, _target in _brain_pairs(brain.read_text(encoding="utf-8")):
            keys.add(speech)
    try:
        items, _, _ = _wp_inputs(ai)
        for speech, _wid, _rel, _rec in items:
            keys.add(speech)
    except Exception:
        pass
    return {k for k in keys if k and k not in ("—", "-", "[]")}


def merge_glossary(ai: Path) -> tuple[int, str]:
    """返回 (0 成功, 说明)。失败时不替换原文件。"""
    path = ai / "context" / "domain-glossary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    required = input_keys(ai, text)
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()
    ids: set[str] = set()
    produced: set[str] = set()

    header, main = parse_section_rows(section(text, "1."))
    for row in main:
        if header[:3] == ["编号", "原词", "标准词"] and row.get("来源") in ("", "manual"):
            row["来源"] = "词库" if row.get("来源") in ("", "manual") else row["来源"]
        if row.get("来源") == "manual":
            row["来源"] = "词库"
        _add(rows, seen, ids, row, produced)

    raw2 = table_rows(section(text, "2."))
    if raw2 and "错误写法" in "".join(raw2[0]):
        for cells in raw2[1:]:
            if len(cells) < 3:
                continue
            _add(rows, seen, ids, _blank({
                "编号": cells[0],
                "说法": cells[1],
                "登记名": cells[2],
                "类别": cells[3] if len(cells) > 3 else "—",
                "状态": cells[4] if len(cells) > 4 else "pending",
                "来源": "纠错",
                "热度": "0",
                "updated": date.today().isoformat(),
            }), produced)

    raw3 = table_rows(section(text, "3."))
    if raw3 and "术语" in "".join(raw3[0]):
        for cells in raw3[1:]:
            if len(cells) < 2:
                continue
            _add(rows, seen, ids, _blank({
                "编号": cells[0],
                "说法": cells[1],
                "登记名": cells[2] if len(cells) > 2 else "",
                "context_hint": cells[3] if len(cells) > 3 else "",
                "首次出现": cells[4] if len(cells) > 4 else "",
                "状态": "pending",
                "来源": "待确认",
                "热度": "0",
                "updated": date.today().isoformat(),
            }), produced)

    ent = ai / "context" / "active-entities.json"
    if ent.is_file():
        try:
            data = json.loads(ent.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        for speech, rec in (data.get("alias_index") or {}).items():
            speech = str(speech).strip()
            if not speech:
                continue
            if isinstance(rec, dict):
                canon = str(rec.get("canonical") or rec.get("id") or "")
                rel = str(rec.get("path") or "")
            else:
                canon, rel = str(rec), ""
            _add(rows, seen, ids, _blank({
                "说法": speech,
                "登记名": canon,
                "路径": rel,
                "状态": "pending",
                "来源": "别名表",
                "热度": "0",
                "updated": date.today().isoformat(),
            }), produced)

    brain = ai / "context" / "brain.md"
    if brain.is_file():
        for speech, target in _brain_pairs(brain.read_text(encoding="utf-8")):
            rel = ""
            if target.startswith("WP-"):
                rel = ""
            _add(rows, seen, ids, _blank({
                "说法": speech,
                "登记名": target,
                "路径": rel,
                "状态": "pending",
                "来源": "脑图",
                "热度": "0",
                "updated": date.today().isoformat(),
            }), produced)

    parsed = []
    try:
        items, parsed, successor_id = _wp_inputs(ai)
    except Exception as exc:
        return 1, f"工作包解析失败: {exc}"
    for speech, wid, rel, _rec in items:
        _add(rows, seen, ids, _blank({
            "说法": speech,
            "登记名": wid,
            "路径": rel,
            "状态": "pending",
            "来源": "工作包",
            "热度": "0",
            "updated": date.today().isoformat(),
        }), produced)
    if parsed:
        _apply_successor(rows, parsed, successor_id)

    missing = sorted(k for k in required if k not in {r.get("说法") for r in rows})
    if missing:
        return 1, "说法表少键: " + ", ".join(missing[:8])

    body = _rewrite(text, rows)
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.replace(path)
    return 0, f"rows={len(rows)}"


def _rewrite(text: str, rows: list[dict]) -> str:
    table = render_table(rows).rstrip() + "\n"
    sec1 = "## 1. 术语映射表\n\n" + table + "\n"
    text = re.sub(r"(?m)^##\s+1b\..*?(?=^##\s+|\Z)", "", text, count=1, flags=re.S)
    sec2 = "## 2. 纠错映射表\n\n已并入第 1 表，禁止再追加。\n\n"
    sec3 = "## 3. 待确认术语\n\n已并入第 1 表，禁止再追加。\n\n"
    if not text.strip():
        return "---\ndoc_type: domain-glossary\nstatus: 活跃\n---\n\n# 领域术语词库\n\n" + sec1 + sec2 + sec3
    out = text
    for title, repl in (("1. 术语映射表", sec1), ("1.", sec1)):
        pass
    pattern = re.compile(r"(?m)^##\s+1\..*?(?=^##\s+|\Z)", re.S)
    if pattern.search(out):
        out = pattern.sub(sec1, out, count=1)
    else:
        out = out.rstrip() + "\n\n" + sec1
    for num, repl in (("2.", sec2), ("3.", sec3)):
        pat = re.compile(rf"(?m)^##\s+{num}.*?(?=^##\s+|\Z)", re.S)
        if pat.search(out):
            out = pat.sub(repl, out, count=1)
        else:
            out = out.rstrip() + "\n\n" + repl
    return out if out.endswith("\n") else out + "\n"


def is_13col(text: str) -> bool:
    """名字保留给旧调用。合格标准是第 1 表恰好 7 列。"""
    rows = table_rows(section(text, "1."))
    return bool(rows) and rows[0] == MAIN


def authoritative_files(ai: Path) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []

    def add(rel: str, path: Path) -> None:
        if path.is_file():
            found.append((rel.replace("\\", "/"), path))

    todos = ai / "todos"
    if todos.is_dir():
        for p in todos.rglob("*.md"):
            if "inbox" in p.parts:
                continue
            add(str(p.relative_to(ai)), p)
    wps = ai / "wps"
    if wps.is_dir():
        for p in wps.glob("WP-*.md"):
            add(f"wps/{p.name}", p)
    plans = ai / "plans"
    if plans.is_dir():
        for p in plans.glob("PLAN-*.md"):
            add(f"plans/{p.name}", p)
    singles = [
        "project-info/progress-plan.md",
        "project-info/budget.md",
        "requirements/requirement-register.md",
        "requirements/contract-register.md",
        "requirements/change-log.md",
        "requirements/source-type-registry.md",
        "registers/scope-register.md",
        "risks/risk-register.md",
        "issues/issue-register.md",
        "decisions/decision-log.md",
        "pm-decisions.md",
        "context/domain-glossary.md",
        "context/project-brief.md",
        "context/project-context.md",
        "context/pm-profile.md",
    ]
    for rel in singles:
        add(rel, ai / rel)
    can = ai / "requirements" / "canonical"
    if can.is_dir():
        for p in can.glob("CAN-*.md"):
            add(f"requirements/canonical/{p.name}", p)
    atoms = ai / "requirements" / "atoms"
    if atoms.is_dir():
        for p in atoms.glob("*.md"):
            if p.name.endswith("-index.md") or p.name == "atom-index.md":
                continue
            add(f"requirements/atoms/{p.name}", p)
    src = ai / "requirements" / "sources"
    if src.is_dir():
        for d in src.iterdir():
            if not d.is_dir():
                continue
            for name in ("meta.md", "ledger.md", "atoms.md", "rows.md", "_digest.md"):
                add(f"requirements/sources/{d.name}/{name}", d / name)
            atom_dir = d / "atoms"
            if atom_dir.is_dir():
                for p in atom_dir.glob("*.md"):
                    add(f"requirements/sources/{d.name}/atoms/{p.name}", p)
            for p in d.glob("original.*"):
                add(f"requirements/sources/{d.name}/{p.name}", p)
    return found


def glossary_stamp_ok(path: Path) -> str:
    return stamp_glossary_text(path.read_text(encoding="utf-8"))


def write_fact_stamps(ai: Path) -> tuple[int, str]:
    state_path = ai / ".state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
    except json.JSONDecodeError:
        return 1, "state 损坏"
    if not isinstance(state, dict):
        state = {}
    stamps = {}
    for rel, path in authoritative_files(ai):
        try:
            if rel.endswith("context/domain-glossary.md"):
                stamps[rel] = glossary_stamp_ok(path)
            else:
                stamps[rel] = sha_file(path)
        except OSError as exc:
            return 1, f"读失败 {rel}: {exc}"
    state["fact_stamps"] = stamps
    tmp = state_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(state_path)
    return 0, f"stamps={len(stamps)}"


def member_ready(ai: Path) -> bool:
    gloss = ai / "context" / "domain-glossary.md"
    if gloss.is_file() and not is_13col(gloss.read_text(encoding="utf-8")):
        return False
    state_path = ai / ".state.json"
    if not state_path.is_file():
        return False
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    stamps = state.get("fact_stamps")
    if not isinstance(stamps, dict):
        return False
    for rel, _path in authoritative_files(ai):
        if rel not in stamps:
            return False
    return True


def apply_member(ai: Path) -> int:
    code, msg = merge_glossary(ai)
    print(f"  说法表 {msg}")
    if code != 0:
        return code
    code, msg = write_fact_stamps(ai)
    print(f"  版本戳 {msg}")
    return code


def refresh_glossary_index(ai: Path) -> int:
    projects = ai / "projects"
    if not projects.is_dir():
        return 0
    lines = ["| 成员 | 说法表 |", "| --- | --- |"]
    for member in sorted(projects.iterdir()):
        gloss = member / "ai" / "context" / "domain-glossary.md"
        if not member.is_dir():
            continue
        if gloss.is_file() and not is_13col(gloss.read_text(encoding="utf-8")):
            print(f"  成员说法表未合并 {member.name}")
            return 1
        if gloss.is_file():
            lines.append(f"| {member.name} | projects/{member.name}/ai/context/domain-glossary.md |")
    dest = ai / "portfolio" / "context" / "glossary-index.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("# 术语指针\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print("  已重写 glossary-index 指针")
    return 0


def fix_successor_rows(ai: Path) -> None:
    path = ai / "context" / "domain-glossary.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not is_13col(text):
        return
    try:
        _items, parsed, successor_id = _wp_inputs(ai)
    except Exception:
        return
    rows = load_rows(text)
    before = json.dumps(rows, ensure_ascii=False)
    _apply_successor(rows, parsed, successor_id)
    if json.dumps(rows, ensure_ascii=False) == before:
        return
    path.write_text(_rewrite(text, rows), encoding="utf-8")
