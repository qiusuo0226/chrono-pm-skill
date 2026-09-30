#!/usr/bin/env python3
"""升级执行器：把 missing/old/stale 的 _digest.md 编成 source-digest。

日常 refresh_views 不调用本脚本。指纹函数复用 refresh_views，禁止双实现。
集根拒绝（各成员根自行跑）。无 atoms 不空编。ok 页不重写。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from refresh_views import (  # noqa: E402
    collect_source_digest_status,
    compute_slice_fp,
    ledger_source_fingerprint,
)

ATOM_RE = re.compile(r"\bATOM-[A-Za-z0-9._-]+\b")


def _ai(root: Path) -> Path:
    cand = root / "ai"
    return cand if cand.is_dir() else root


def _is_portfolio_root(ai: Path) -> bool:
    return (ai / "portfolio").is_dir() and (ai / "projects").is_dir()


def _front(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _atom_ids(src_dir: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    files = []
    for name in ("atoms.md",):
        p = src_dir / name
        if p.is_file():
            files.append(p)
    ad = src_dir / "atoms"
    if ad.is_dir():
        files.extend(sorted(ad.glob("**/*.md")))
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in ATOM_RE.finditer(text):
            if m.group(0) not in seen:
                seen.add(m.group(0))
                ids.append(m.group(0))
    return ids


def _has_atoms(src_dir: Path) -> bool:
    if (src_dir / "atoms.md").is_file() and (src_dir / "atoms.md").stat().st_size > 0:
        return True
    ad = src_dir / "atoms"
    if ad.is_dir() and any(p.suffix.lower() == ".md" for p in ad.glob("**/*") if p.is_file()):
        return True
    return False


def _meta_type(src_dir: Path) -> tuple[str, str]:
    meta = src_dir / "meta.md"
    st, cat = "generic", "generic"
    if meta.is_file():
        try:
            fm = _front(meta.read_text(encoding="utf-8"))
        except OSError:
            fm = {}
        st = (fm.get("source_type") or st).strip() or st
        cat = (fm.get("source_category") or cat).strip() or cat
    digest = src_dir / "_digest.md"
    if digest.is_file():
        try:
            fm = _front(digest.read_text(encoding="utf-8"))
        except OSError:
            fm = {}
        st = (fm.get("source_type") or st).strip() or st
        cat = (fm.get("source_category") or fm.get("digest_schema") or cat).strip() or cat
    if cat not in (
        "contractual",
        "procurement",
        "approval",
        "compliance",
        "technical",
        "operational",
        "generic",
    ):
        cat = "generic"
    return st, cat


def _columns(cat: str) -> list[str]:
    tables = {
        "contractual": ["这是什么", "当事人", "标的与价款", "工期与质保", "硬约束", "范围依据", "切片索引", "已绑需求与工作包"],
        "procurement": ["这是什么", "采购身份", "门槛与评分", "承诺与偏离", "与合同衔接", "切片索引", "已绑"],
        "approval": ["这是什么", "批复或结论", "建设内容", "投资与工期", "约束", "切片索引", "已绑"],
        "compliance": ["这是什么", "评测对象", "必须满足", "门禁与证据", "切片索引", "已绑"],
        "technical": ["这是什么", "边界", "功能与规则", "接口与数据", "非功能", "切片索引", "已绑"],
        "operational": ["这是什么", "约定事项", "时点", "责任", "切片索引", "已绑"],
        "generic": ["这是什么", "要点", "切片索引", "已绑"],
    }
    return tables.get(cat, tables["generic"])


def _build_page(src_dir: Path, sid: str) -> str:
    st, cat = _meta_type(src_dir)
    fp = compute_slice_fp(src_dir)
    src_fp = ledger_source_fingerprint(src_dir) or "—"
    atoms = _atom_ids(src_dir)
    if atoms:
        rows = "\n".join(f"| {a} | `{a}` |" for a in atoms)
    elif _has_facts(src_dir):
        rows = "| facts.md | 非需求类 |"
    else:
        rows = "| — | 本源未见 |"
    cols = _columns(cat)
    parts = [
        "---",
        "doc_type: source-digest",
        f"source_id: {sid}",
        f"source_type: {st}",
        f"source_category: {cat}",
        "authority: —",
        f"source_fingerprint: {src_fp}",
        f"slice_fingerprint: {fp}",
        f"compiled_at: {date.today().isoformat()}",
        f"digest_schema: {cat}",
        "---",
        "",
        f"# {sid}",
        "",
        "绑定状态以登记册 / 工作包第二节为准，本节可能延迟。升级回填页。",
        "",
    ]
    for col in cols:
        parts.append(f"## {col}")
        parts.append("")
        if "切片" in col:
            parts.append("| 切片 | 指针 |")
            parts.append("|---|---|")
            parts.append(rows)
        elif "已绑" in col:
            parts.append("—")
        elif "硬约束" in col or "必须满足" in col or "约束" == col:
            if atoms:
                parts.append("；".join(f"[{a}]({a})" for a in atoms[:20]))
            else:
                parts.append("本源未见")
        else:
            parts.append("本源未见")
        parts.append("")
    text = "\n".join(parts)
    if "[[wikilink]]" in text:
        raise RuntimeError("page contains wikilink")
    return text


REQ_RE = re.compile(r"\bREQ-[A-Za-z0-9._-]+\b")
WP_RE = re.compile(r"\bWP-[A-Za-z0-9._-]+\b")
_EMPTY = {"", "—", "-", "–", "本源未见"}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _title(src_dir: Path) -> str:
    for name in ("meta.md", "_digest.md"):
        for line in _read(src_dir / name).splitlines():
            if not line.startswith("# "):
                continue
            rest = line[2:].strip()
            if "—" in rest:
                return rest.split("—", 1)[1].strip()
            if " - " in rest:
                return rest.split(" - ", 1)[1].strip()
            return rest
    return ""


def _source_refs(src_dir: Path) -> list[str]:
    refs: list[str] = []
    files = []
    atoms = src_dir / "atoms.md"
    if atoms.is_file():
        files.append(atoms)
    ad = src_dir / "atoms"
    if ad.is_dir():
        files.extend(sorted(p for p in ad.glob("**/*.md") if p.is_file()))
    for p in files:
        for line in _read(p).splitlines():
            if "source_ref" not in line or ":" not in line:
                continue
            val = line.split(":", 1)[1].strip()
            if val not in _EMPTY and val not in refs:
                refs.append(val)
    return refs


def _atom_ids_in(src_dir: Path) -> list[str]:
    return _atom_ids(src_dir)


def _has_facts(src_dir: Path) -> bool:
    facts = src_dir / "facts.md"
    if facts.is_file() and facts.stat().st_size > 0:
        return True
    folder = src_dir / "facts"
    if not folder.is_dir():
        return False
    for p in folder.glob("**/*"):
        if p.is_file() and p.suffix.lower() == ".md" and not p.name.startswith("."):
            rel = p.relative_to(src_dir).as_posix()
            if rel == "facts/local_only.md" or rel.startswith("facts/local_only/"):
                continue
            return True
    return False


def _doc_kind(src_dir: Path) -> tuple[str, str]:
    """返回 (requirement|reference|invalid, note)。缺省是 requirement。"""
    meta = src_dir / "meta.md"
    if not meta.is_file():
        return "requirement", ""
    fm = _front(_read(meta))
    raw = (fm.get("doc_kind") or "").strip()
    note = (fm.get("doc_kind_note") or "").splitlines()
    note_s = note[0].strip() if note else ""
    if raw in ("", "requirement"):
        return "requirement", note_s
    if raw == "reference":
        return "reference", note_s
    return "invalid", note_s


def _split_profile(src_dir: Path) -> str:
    meta = src_dir / "meta.md"
    if not meta.is_file():
        return ""
    return (_front(_read(meta)).get("split_profile") or "").strip()


def _digest_frozen(src_dir: Path) -> bool:
    """已有摘要页、且不是 4.1.0：不调用 _build_page。已绑和参见仍可由 _apply_wiki 更新。"""
    return _split_profile(src_dir) != "4.1.0" and (src_dir / "_digest.md").is_file()


def _wp_effect(ai: Path, wp_id: str) -> str:
    fm = _front(_read(ai / "wps" / f"{wp_id}.md"))
    return (fm.get("effect") or "正常").strip() or "正常"


def _wp_name(ai: Path, wp_id: str) -> str:
    for line in _read(ai / "wps" / f"{wp_id}.md").splitlines():
        if line.startswith("# "):
            rest = line[2:].strip()
            if " - " in rest:
                return rest.split(" - ", 1)[1].strip()
            if "—" in rest:
                return rest.split("—", 1)[1].strip()
            return rest
    return ""


def _req_titles(register_text: str) -> dict[str, str]:
    headers, rows = _table_rows(register_text)
    req_i = _col(headers, "Req", "需求编号")
    title_i = _col(headers, "标题")
    out: dict[str, str] = {}
    if req_i < 0:
        return out
    for row in rows:
        if req_i >= len(row):
            continue
        rid = row[req_i]
        if not (REQ_RE.fullmatch(rid) or rid.startswith("REQ-")):
            continue
        title = row[title_i].strip() if 0 <= title_i < len(row) else ""
        out[rid] = title
    return out


def _register_ids(register_text: str) -> list[str]:
    return list(_req_titles(register_text))


def _confirmed_pairs(ai: Path) -> list[tuple[str, str]]:
    text = _read(ai / "context" / "domain-glossary.md")
    pairs: list[tuple[str, str]] = []
    in_main = False
    for line in text.splitlines():
        if line.startswith("## 1") and not line.startswith("## 1b"):
            in_main = True
            continue
        if in_main and line.startswith("## "):
            break
        if not in_main or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[1] in ("说法", "") or set(cells[1]) <= {"-", ":"}:
            continue
        if cells[4] != "confirmed":
            continue
        if cells[1] and cells[2]:
            pairs.append((cells[1], cells[2]))
    return pairs


def _atom_blobs(src_dir: Path) -> list[tuple[str, str, str]]:
    """(atom_id, text, parent_ref)。parent_ref 来自该 ATOM 文件头或正文行。"""
    files: list[Path] = []
    atoms = src_dir / "atoms.md"
    if atoms.is_file():
        files.append(atoms)
    folder = src_dir / "atoms"
    if folder.is_dir():
        files.extend(sorted(p for p in folder.glob("**/*.md") if p.is_file()))
    out: list[tuple[str, str, str]] = []
    for p in files:
        text = _read(p)
        file_parent = (_front(text).get("parent_ref") or "").strip()
        current = ""
        buf: list[str] = []
        parent = file_parent
        def flush() -> None:
            if current:
                out.append((current, "\n".join(buf), parent))
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("parent_ref:"):
                parent = stripped.split(":", 1)[1].strip().strip('"').strip("'") or parent
                buf.append(line)
                continue
            bare = stripped.lstrip("-").strip()
            if bare.startswith("#"):
                bare = bare.lstrip("#").strip()
            m = ATOM_RE.match(bare)
            if m:
                flush()
                current = m.group(0)
                buf = [line]
                continue
            buf.append(line)
        flush()
    return out


def _live_wp_ids_for_req(ai: Path, register_text: str, req_id: str) -> list[str]:
    found: set[str] = set()
    headers, rows = _table_rows(register_text)
    req_i = _col(headers, "Req", "需求编号")
    wp_i = _col(headers, "工作包")
    if req_i >= 0 and wp_i >= 0:
        for row in rows:
            if req_i < len(row) and row[req_i] == req_id and wp_i < len(row):
                for wp in WP_RE.findall(row[wp_i]):
                    if _wp_effect(ai, wp) != "废弃":
                        found.add(wp)
    wps = ai / "wps"
    if wps.is_dir():
        for wp in sorted(wps.glob("WP-*.md")):
            if _wp_effect(ai, wp.stem) == "废弃":
                continue
            if req_id in _section2(_read(wp)):
                found.add(wp.stem)
    return sorted(found)


def _set_register_wp(register_text: str, req_id: str, wp_ids: list[str]) -> str:
    headers, _rows = _table_rows(register_text)
    req_i = _col(headers, "Req", "需求编号")
    wp_i = _col(headers, "工作包")
    if req_i < 0 or wp_i < 0:
        return register_text
    cell = " / ".join(wp_ids)
    lines = register_text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("|") or req_id not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if req_i >= len(cells) or cells[req_i] != req_id:
            continue
        while len(cells) <= wp_i:
            cells.append("")
        cells[wp_i] = cell
        lines[i] = "| " + " | ".join(cells) + " |"
        break
    text = "\n".join(lines)
    return text if text.endswith("\n") else text + "\n"


def _next_wp_id(ai: Path, day: str) -> str:
    n = 0
    wps = ai / "wps"
    if wps.is_dir():
        for p in wps.glob(f"WP-{day}-*.md"):
            m = re.search(r"-(\d+)$", p.stem)
            if m:
                n = max(n, int(m.group(1)))
    return f"WP-{day}-{n + 1:03d}"


def _write_backfill_wp(path: Path, wp_id: str, title: str, req_id: str, day: str) -> None:
    name = title or req_id
    body = (
        "---\n"
        "doc_type: work-package\n"
        f"wp_id: {wp_id}\n"
        "project: —\n"
        "plan_ref:\n"
        "status: 待确认\n"
        "effect: 正常\n"
        "superseded_by: —\n"
        f"created_at: {day}\n"
        "completed_at: —\n"
        "retired_at: —\n"
        "---\n\n"
        f"# {wp_id} - {name}\n\n"
        "## 1. 基本信息\n"
        "| 字段 | 值 |\n|---|---|\n"
        f"| WP 编号 | {wp_id} |\n"
        f"| WP 名称 | {name} |\n"
        "| 负责人 | — |\n"
        "| 开始时间 | — |\n"
        "| 结束时间 | — |\n"
        "| 生效 | 正常 |\n"
        f"| 关联需求 | {req_id} |\n\n"
        "## 2. 关联需求（强制字段，只留编号）\n"
        "| 需求编号 | 来源路径 |\n|---|---|\n"
        f"| {req_id} | — |\n\n"
        "## 7. 状态历史\n"
        "| 时间 | 从状态 | 到状态 |\n|---|---|---|\n"
        f"| {day} | — | 待确认 |\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.replace(path)


def backfill_live_wps(ai: Path, only_ids: set[str] | None = None) -> list[str]:
    """为登记册上还没有未废弃包的需求编号建待确认包。无编号不建。返回新建编号。"""
    register = ai / "requirements" / "requirement-register.md"
    reg_text = _read(register)
    titles = _req_titles(reg_text)
    ids = [i for i in titles if only_ids is None or i in only_ids]
    created: list[str] = []
    day = date.today().strftime("%Y%m%d")
    for req_id in ids:
        if not req_id:
            continue
        live = _live_wp_ids_for_req(ai, reg_text, req_id)
        if live:
            headers, rows = _table_rows(reg_text)
            wp_i = _col(headers, "工作包")
            req_i = _col(headers, "Req", "需求编号")
            column: list[str] = []
            if req_i >= 0 and wp_i >= 0:
                for row in rows:
                    if req_i < len(row) and row[req_i] == req_id and wp_i < len(row):
                        column = [w for w in WP_RE.findall(row[wp_i]) if _wp_effect(ai, w) != "废弃"]
                        break
            if not column:
                reg_text = _set_register_wp(reg_text, req_id, live)
            continue
        if not register.is_file():
            continue
        wp_id = _next_wp_id(ai, day)
        wp_path = ai / "wps" / f"{wp_id}.md"
        _write_backfill_wp(wp_path, wp_id, titles.get(req_id, ""), req_id, day)
        new_reg = _set_register_wp(reg_text, req_id, [wp_id])
        try:
            register.write_text(new_reg, encoding="utf-8")
        except OSError:
            wp_path.unlink(missing_ok=True)
            continue
        written = _read(register)
        if wp_id not in written or req_id not in written:
            wp_path.unlink(missing_ok=True)
            continue
        reg_text = written
        created.append(wp_id)
    if register.is_file() and reg_text != _read(register):
        try:
            register.write_text(reg_text, encoding="utf-8")
        except OSError:
            pass
    line = f"BACKFILL created={len(created)}"
    if created:
        line += " " + " ".join(created)
    print(line)
    return created


_SEE_RE = re.compile(
    r"\b(SRC-[A-Za-z0-9._-]+|REQ-[A-Za-z0-9._-]+|WP-[A-Za-z0-9._-]+|"
    r"MTG-[A-Za-z0-9._-]+|CON-[A-Za-z0-9._-]+|BID-[A-Za-z0-9._-]+|"
    r"INIT-[A-Za-z0-9._-]+)\b"
)


def _slice_corpus(src_dir: Path) -> str:
    parts: list[str] = []
    for name in ("meta.md", "atoms.md", "facts.md"):
        parts.append(_read(src_dir / name))
    for sub in ("atoms", "facts"):
        folder = src_dir / sub
        if folder.is_dir():
            for p in sorted(folder.glob("**/*.md")):
                if p.is_file():
                    parts.append(_read(p))
    return "\n".join(parts)


def _digested(sources: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    if not sources.is_dir():
        return out
    for d in sources.iterdir():
        if d.is_dir() and (d / "_digest.md").is_file():
            out[d.name] = d
    return out


def _meeting_exists(ai: Path, mid: str) -> bool:
    root = ai / "meetings"
    if not root.is_dir():
        return False
    for p in root.rglob("*"):
        if p.is_file() and p.name.startswith(mid):
            return True
    return False


def _id_exists(ai: Path, token: str, reg_text: str, contract_text: str, digested: dict[str, Path]) -> bool:
    if token.startswith("SRC-"):
        d = digested.get(token)
        return d is not None and (d / "meta.md").is_file()
    if token.startswith("REQ-"):
        return bool(re.search(rf"\b{re.escape(token)}\b", reg_text))
    if token.startswith("WP-"):
        return (ai / "wps" / f"{token}.md").is_file()
    if token.startswith("MTG-"):
        return _meeting_exists(ai, token)
    if token.startswith(("CON-", "BID-", "INIT-")):
        d = digested.get(token)
        if d is not None and (d / "meta.md").is_file():
            return True
        return bool(re.search(rf"\b{re.escape(token)}\b", contract_text))
    return False


def _see_also(ai: Path, sid: str, src_dir: Path, reg_text: str, contract_text: str, digested: dict[str, Path]) -> list[str]:
    found: set[str] = set()
    for token in _SEE_RE.findall(_slice_corpus(src_dir)):
        if token == sid:
            continue
        if _id_exists(ai, token, reg_text, contract_text, digested):
            found.add(token)
    title = _title(src_dir)
    if title:
        for other, folder in digested.items():
            if other != sid and _title(folder) == title:
                found.add(other)
        for rid, req_title in _req_titles(reg_text).items():
            if req_title and req_title == title:
                found.add(rid)
    hits, blocked = _glossary_matches(ai, _slice_corpus(src_dir), reg_text, digested, sid)
    if not blocked:
        for token in hits:
            if token != sid:
                found.add(token)
    return sorted(found)


def _table_rows(text: str) -> tuple[list[str], list[list[str]]]:
    lines = text.splitlines()
    headers: list[str] = []
    start = None
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if any("来源" in c for c in cells) and any("Req" in c or "需求" in c for c in cells):
            headers = cells
            start = i
            break
    if start is None:
        return [], []
    rows = []
    for line in lines[start + 1 :]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set(cells) <= {"---", ":---", "---:", ":---:"} or all(set(c) <= {"-", ":"} for c in cells):
            continue
        rows.append(cells)
    return headers, rows


def _col(headers: list[str], *names: str) -> int:
    for i, h in enumerate(headers):
        if any(n in h for n in names):
            return i
    return -1


def _section2(text: str) -> str:
    grab = False
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## 2"):
            grab = True
            continue
        if grab and line.startswith("## "):
            break
        if grab:
            buf.append(line)
    return "\n".join(buf)


def _wp_ids_for(ai: Path, sid: str, req_ids: set[str], register_text: str) -> list[str]:
    found: set[str] = set()
    headers, rows = _table_rows(register_text)
    req_i = _col(headers, "Req", "需求编号")
    wp_i = _col(headers, "工作包")
    if req_i >= 0 and wp_i >= 0:
        for row in rows:
            if req_i >= len(row):
                continue
            if row[req_i] not in req_ids:
                continue
            cell = row[wp_i] if wp_i < len(row) else ""
            found.update(WP_RE.findall(cell))
    wps = ai / "wps"
    if wps.is_dir():
        for wp in sorted(wps.glob("WP-*.md")):
            body = _section2(_read(wp))
            if f"sources/{sid}" in body or any(r in body for r in req_ids):
                found.add(wp.stem)
    return sorted(wp for wp in found if _wp_effect(ai, wp) != "废弃")


def _direct_reqs(register_text: str, sid: str, atom_ids: list[str]) -> set[str]:
    found: set[str] = set()
    headers, rows = _table_rows(register_text)
    req_i = _col(headers, "Req", "需求编号")
    src_i = _col(headers, "来源")
    if req_i >= 0 and src_i >= 0:
        for row in rows:
            if max(req_i, src_i) >= len(row):
                continue
            src = row[src_i]
            if f"sources/{sid}" in src or f"/{sid}" in src:
                if REQ_RE.fullmatch(row[req_i]) or row[req_i].startswith("REQ-"):
                    found.add(row[req_i])
    if atom_ids:
        lines = register_text.splitlines()
        last_req = ""
        for line in lines:
            ids = REQ_RE.findall(line)
            if ids:
                last_req = ids[-1]
            if last_req and any(a in line for a in atom_ids):
                found.add(last_req)
    return found


def _append_unique(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = _read(path) if path.is_file() else ""
    if line in old:
        return
    text = old
    if text and not text.endswith("\n"):
        text += "\n"
    if path.name == "migration-log.md" and "## wiki 缺口" not in text:
        text += "\n## wiki 缺口\n\n"
    if path.name == "pm-decisions.md" and "## 升级待裁定" not in text:
        text += "\n## 升级待裁定\n\n"
    text += line + "\n"
    path.write_text(text, encoding="utf-8")


def _set_bind(text: str, body: list[str]) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    found = False
    while i < len(lines):
        if lines[i].startswith("## ") and "已绑" in lines[i]:
            found = True
            out.append(lines[i])
            out.append("")
            out.extend(body)
            out.append("")
            i += 1
            while i < len(lines) and not (lines[i].startswith("## ") and "已绑" not in lines[i]):
                if lines[i].startswith("## ") and "已绑" not in lines[i]:
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    if not found:
        if out and out[-1] != "":
            out.append("")
        out.extend(["## 已绑", ""] + body)
    return "\n".join(out).rstrip() + "\n"


def _set_h2(text: str, title: str, body: list[str]) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    found = False
    while i < len(lines):
        if lines[i].startswith("## ") and lines[i].strip() == f"## {title}":
            found = True
            out.append(lines[i])
            out.append("")
            out.extend(body)
            out.append("")
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    if not found:
        if out and out[-1] != "":
            out.append("")
        out.extend([f"## {title}", ""] + body)
    return "\n".join(out).rstrip() + "\n"


def _mark_reference(text: str, note: str) -> str:
    lines = text.splitlines()
    head_end = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            head_end = i
            break
    head = lines[:head_end]
    want = ["非需求类"]
    if note and note != "非需求类":
        want.append(note)
    missing = [w for w in want if not any(ln.strip() == w for ln in head)]
    if not missing:
        return text if text.endswith("\n") else text + "\n"
    out: list[str] = []
    placed = False
    for line in head:
        out.append(line)
        if not placed and line.startswith("# "):
            out.append("")
            out.extend(missing)
            out.append("")
            placed = True
    if not placed:
        out.extend([""] + missing + [""])
    out.extend(lines[head_end:])
    return "\n".join(out).rstrip() + "\n"


def _bind_body(req_ids: list[str], wp_ids: list[str], siblings: list[str]) -> list[str]:
    body = [" / ".join(req_ids + wp_ids)]
    if siblings:
        body.append("同链源 " + " ".join(siblings))
    return body


def _ensure_pointer(text: str, sid: str, ref: str, req_id: str) -> str:
    pointer = f"sources/{sid} {ref}".strip()
    doc = f"requirements/sources/{sid}/"
    headers, _rows = _table_rows(text)
    src_i = _col(headers, "来源")
    lines = text.splitlines()
    if src_i >= 0:
        for i, line in enumerate(lines):
            if not line.startswith("|") or req_id not in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if src_i < len(cells) and f"sources/{sid}" not in cells[src_i]:
                cells[src_i] = (cells[src_i] + "；" + pointer).strip("；")
                lines[i] = "| " + " | ".join(cells) + " |"
                break
    text = "\n".join(lines)
    if doc not in text:
        text = text.rstrip() + (
            f"\n\n### 升级补链 {req_id}\n\n"
            f"- 来源指针：{pointer}\n"
            f"- 原型/文档链接：{doc}\n"
        )
    elif f"sources/{sid}" not in text:
        text = text.rstrip() + f"\n- 来源指针：{pointer}\n"
    return text if text.endswith("\n") else text + "\n"


def _glossary_matches(
    ai: Path, text: str, reg_text: str, digested: dict[str, Path], sid: str
) -> tuple[list[str], bool]:
    """说法出现在 text 里、且登记名恰好对上一个未废弃目标时返回该编号。对上多个则整段不作数。"""
    pairs = _confirmed_pairs(ai)
    if not pairs or not text:
        return [], False
    titles = _req_titles(reg_text)
    collected: list[str] = []
    blocked = False
    wps = ai / "wps"
    for phrase, canonical in pairs:
        if not phrase or phrase not in text:
            continue
        hits: list[str] = []
        if wps.is_dir():
            for wp in sorted(wps.glob("WP-*.md")):
                if _wp_effect(ai, wp.stem) == "废弃":
                    continue
                if _wp_name(ai, wp.stem) == canonical:
                    hits.append(wp.stem)
        for rid, title in titles.items():
            if title and title == canonical:
                hits.append(rid)
        for other, folder in digested.items():
            if other != sid and _title(folder) == canonical:
                hits.append(other)
        uniq = sorted(set(hits))
        if len(uniq) > 1:
            blocked = True
        elif len(uniq) == 1:
            collected.append(uniq[0])
    if blocked or len(set(collected)) > 1:
        return [], True
    return sorted(set(collected)), False


def _req_ids_in_section2(ai: Path, wp_id: str) -> list[str]:
    found: list[str] = []
    for token in REQ_RE.findall(_section2(_read(ai / "wps" / f"{wp_id}.md"))):
        if token not in found:
            found.append(token)
    return found


def _register_atom_map(reg_text: str, sid: str, atom_ids: set[str]) -> tuple[dict[str, set[str]], set[str]]:
    per: dict[str, set[str]] = {}
    source_level: set[str] = set()
    headers, rows = _table_rows(reg_text)
    req_i = _col(headers, "Req", "需求编号")
    src_i = _col(headers, "来源")
    if req_i < 0 or src_i < 0:
        return per, source_level
    for row in rows:
        if max(req_i, src_i) >= len(row):
            continue
        rid = row[req_i]
        if not (REQ_RE.fullmatch(rid) or str(rid).startswith("REQ-")):
            continue
        src = row[src_i]
        if f"sources/{sid}" not in src:
            continue
        mentioned = [a for a in atom_ids if a in src]
        if mentioned:
            for atom in mentioned:
                per.setdefault(atom, set()).add(rid)
        else:
            source_level.add(rid)
    return per, source_level


def _has_bind_section(text: str) -> bool:
    return any(line.startswith("## ") and "已绑" in line for line in text.splitlines())


def _split_enough(src_dir: Path) -> bool:
    kind, _note = _doc_kind(src_dir)
    return _has_atoms(src_dir) or (kind == "reference" and _has_facts(src_dir))


def _profile_choices(
    ai: Path, src_dir: Path, reg_text: str, digested: dict[str, Path]
) -> tuple[list[tuple[str, str, str]], list[tuple[str, str]], set[str]]:
    """按子块定需求。(atom, req, parent)；req 为「独立」表示不挂需求。atom 为 * 表示整源一条。

    对不上恰好一条、词库对上两个目标，都不记缺口。多出来的需求编号放进第三项，供参见使用。
    """
    sid = src_dir.name
    blobs = _atom_blobs(src_dir)
    per, source_level = _register_atom_map(reg_text, sid, {b[0] for b in blobs})
    binds: list[tuple[str, str, str]] = []
    gaps: list[tuple[str, str]] = []
    extra: set[str] = set()

    def gloss_one(atom: str, text: str, parent: str) -> None:
        hits, blocked = _glossary_matches(ai, text, reg_text, digested, sid)
        if blocked:
            binds.append((atom, "独立", parent))
            return
        wps = [h for h in hits if h.startswith("WP-")]
        reqs = [h for h in hits if h.startswith("REQ-")]
        if len(wps) == 1 and len(reqs) == 0:
            owned = _req_ids_in_section2(ai, wps[0])
            if len(owned) == 1:
                binds.append((atom, owned[0], parent))
                return
        elif len(reqs) == 1 and len(wps) == 0:
            binds.append((atom, reqs[0], parent))
            return
        binds.append((atom, "独立", parent))

    if per:
        for atom, text, parent in blobs:
            cands = per.get(atom, set())
            if len(cands) == 1:
                binds.append((atom, next(iter(cands)), parent))
            elif len(cands) > 1:
                extra.update(cands)
                binds.append((atom, "独立", parent))
            else:
                gloss_one(atom, text, parent)
        return binds, gaps, extra
    if len(source_level) > 1:
        extra.update(source_level)
        binds.append(("*", "独立", ""))
        return binds, gaps, extra
    if len(source_level) == 1:
        binds.append(("*", next(iter(source_level)), ""))
        return binds, gaps, extra
    if not blobs:
        binds.append(("*", "独立", ""))
        return binds, gaps, extra
    for atom, text, parent in blobs:
        gloss_one(atom, text, parent)
    return binds, gaps, extra


def _apply_wiki(ai: Path, write: bool = True, audit: bool = False, frozen_ids: set[str] | None = None) -> int:
    """已拆标准文件写入已绑和参见。硬缺口记日志并返回失败数。

    对不上恰好一条已有需求时已绑写「独立」，不计缺口。参见在写盘前算完正向和反向。
    冻结页不整页重写：已有已绑节且仍是唯一绑定时该节保持，其余写入已绑；不是硬缺口的都写参见。
    """
    sources = ai / "requirements" / "sources"
    if not sources.is_dir():
        return 0
    register = ai / "requirements" / "requirement-register.md"
    reg_text = _read(register)
    contract_text = _read(ai / "requirements" / "contract-register.md")
    dirs = [p for p in sorted(sources.iterdir()) if p.is_dir()]
    split = [d for d in dirs if _has_atoms(d)]
    reference: dict[str, str] = {}
    gaps: list[tuple[str, str]] = []
    for d in dirs:
        kind, note = _doc_kind(d)
        if kind == "invalid":
            gaps.append((d.name, "doc_kind 无法识别"))
            continue
        if kind == "reference" and (_has_atoms(d) or _has_facts(d)):
            reference[d.name] = note
    gapped_early = {sid for sid, _reason in gaps}
    req_split = [d for d in split if d.name not in reference and d.name not in gapped_early]
    legacy = [d for d in req_split if _split_profile(d) != "4.1.0"]
    direct: dict[str, set[str]] = {}
    refs: dict[str, list[str]] = {}
    for d in legacy:
        sid = d.name
        refs[sid] = _source_refs(d)
        direct[sid] = _direct_reqs(reg_text, sid, _atom_ids_in(d))
    chosen: dict[str, str] = {}
    independent: set[str] = set()
    extra_reqs: dict[str, set[str]] = {}
    for d in legacy:
        sid = d.name
        if not refs[sid]:
            gaps.append((sid, "切片没有章节或页码"))
            continue
        cands = direct[sid]
        if len(cands) > 1:
            independent.add(sid)
            extra_reqs[sid] = set(cands)
            continue
        if len(cands) == 1:
            chosen[sid] = next(iter(cands))
            continue
        title = _title(d)
        titled = {
            next(iter(direct[other.name]))
            for other in legacy
            if other.name != sid and _title(other) == title and title and len(direct[other.name]) == 1
        }
        if len(titled) == 1:
            chosen[sid] = next(iter(titled))
        elif len(titled) > 1:
            independent.add(sid)
            extra_reqs[sid] = set(titled)
        else:
            independent.add(sid)
    wp_of: dict[str, list[str]] = {}
    for sid, req in list(chosen.items()):
        wps = _wp_ids_for(ai, sid, {req}, reg_text)
        if not wps:
            gaps.append((sid, "没有工作包"))
            del chosen[sid]
            continue
        wp_of[sid] = wps
    by_req: dict[str, list[str]] = {}
    for sid, req in chosen.items():
        by_req.setdefault(req, []).append(sid)
    if write and register.is_file() and chosen:
        text = reg_text
        for sid, req in chosen.items():
            text = _ensure_pointer(text, sid, refs[sid][0], req)
        if text != reg_text:
            register.write_text(text, encoding="utf-8")
            reg_text = text
    profile_dirs = [d for d in req_split if _split_profile(d) == "4.1.0"]
    profile_lines: dict[str, list[str]] = {}
    profile_touched: set[str] = set()
    planned: dict[str, list[tuple[str, str, str]]] = {}
    want_reqs: set[str] = set()
    digested_now = _digested(sources)
    for d in profile_dirs:
        binds, child_gaps, extras = _profile_choices(ai, d, reg_text, digested_now)
        planned[d.name] = binds
        profile_touched.add(d.name)
        gaps.extend(child_gaps)
        extra_reqs.setdefault(d.name, set()).update(extras)
        for _atom, req, _parent in binds:
            if req != "独立":
                want_reqs.add(req)
    if write and want_reqs:
        backfill_live_wps(ai, want_reqs)
        reg_text = _read(register)
    for sid, binds in planned.items():
        lines: list[str] = []
        for atom, req, parent in binds:
            if req == "独立":
                if atom == "*":
                    lines.append("独立")
                else:
                    lines.append(f"{atom} 独立 {parent}".strip())
                continue
            wps = _live_wp_ids_for_req(ai, reg_text, req)
            if not wps:
                gaps.append((sid if atom == "*" else f"{sid}/{atom}", "没有工作包"))
                continue
            wp_s = " ".join(wps)
            if atom == "*":
                lines.append(f"{req} / {wp_s}".strip())
            else:
                lines.append(f"{atom} {req} / {wp_s} {parent}".strip())
        if lines:
            profile_lines[sid] = lines
    gapped = {sid for sid, _reason in gaps}
    frozen = frozen_ids or set()
    if audit:
        for sid in sorted(reference):
            if sid not in gapped:
                print(f"REFERENCE {sid}（豁免）")
    eligible: list[Path] = []
    for d in dirs:
        sid = d.name
        if not (d / "_digest.md").is_file():
            continue
        if sid in gapped:
            continue
        if sid in frozen and not _split_enough(d):
            continue
        if sid in profile_touched and sid not in profile_lines:
            continue
        eligible.append(d)
    digested = _digested(sources)
    see_map: dict[str, set[str]] = {}
    for d in eligible:
        sid = d.name
        found = set(_see_also(ai, sid, d, reg_text, contract_text, digested))
        for token in extra_reqs.get(sid, ()):
            if token != sid and _id_exists(ai, token, reg_text, contract_text, digested):
                found.add(token)
        see_map[sid] = found
    for d in eligible:
        sid = d.name
        for token in _SEE_RE.findall(_slice_corpus(d)):
            if token == sid or token not in see_map or token not in digested:
                continue
            see_map[token].add(sid)
    for d in eligible:
        sid = d.name
        digest = d / "_digest.md"
        old = _read(digest)
        uniquely = sid in chosen or (
            sid in profile_lines
            and bool(profile_lines[sid])
            and all("独立" not in line for line in profile_lines[sid])
        )
        skip_bind = sid in frozen and _has_bind_section(old) and uniquely and sid not in independent
        new = old
        if sid in reference:
            if sid in frozen:
                if not _has_bind_section(old):
                    new = _set_bind(new, ["非需求类"])
            else:
                new = _mark_reference(new, reference[sid])
                new = _set_bind(new, ["非需求类"])
        elif sid in profile_lines:
            if not skip_bind:
                new = _set_bind(new, profile_lines[sid])
        elif sid in chosen:
            if not skip_bind:
                siblings = sorted(s for s in by_req[chosen[sid]] if s != sid)
                new = _set_bind(new, _bind_body([chosen[sid]], wp_of[sid], siblings))
        elif sid in independent:
            new = _set_bind(new, ["独立"])
        elif not skip_bind:
            ids = sorted(set(_direct_reqs(reg_text, sid, [])) | set(_wp_ids_for(ai, sid, set(), reg_text)))
            body = [" / ".join(ids)] if ids else ["无登记边"]
            new = _set_bind(new, body)
        see = sorted(see_map.get(sid, set()))
        newer = _set_h2(new, "参见", see if see else ["无参见"])
        if write and newer != old:
            digest.write_text(newer, encoding="utf-8")
    for sid, reason in gaps:
        line = f"- {sid}：{reason}"
        if write:
            _append_unique(ai / "logs" / "migration-log.md", line)
            _append_unique(ai / "pm-decisions.md", line)
        print(f"GAP {sid} {reason}")
    return len(gaps)


def compile_workspace(root: str, dry_run: bool = False, check_only: bool = False) -> int:
    project = Path(root).resolve()
    ai = _ai(project)
    if _is_portfolio_root(ai):
        print("REFUSE 集根：对各成员根分别跑 compile_source_digests.py")
        return 1
    sources = ai / "requirements" / "sources"
    if not sources.is_dir():
        print("SKIP 无 requirements/sources/")
        return 0
    st = collect_source_digest_status(ai)
    failed = 0
    wrote = 0
    skipped = 0
    seen: set[str] = set()
    frozen_ids: set[str] = set()
    for sid, rec in st.get("sources", {}).items():
        path = rec.get("path") or ""
        src_dir = ai / Path(path).parent if path else sources / sid
        if not src_dir.is_dir():
            src_dir = sources / sid
        key = str(src_dir)
        if key in seen:
            continue
        seen.add(key)
        if _digest_frozen(src_dir):
            print(f"keep {src_dir.name}")
            skipped += 1
            frozen_ids.add(src_dir.name)
            continue
        status = rec.get("status")
        if status == "ok":
            print(f"ok {src_dir.name}")
            skipped += 1
            continue
        kind, _note = _doc_kind(src_dir)
        if not _has_atoms(src_dir) and not (kind == "reference" and _has_facts(src_dir)):
            print(f"FAIL {src_dir.name} 无 atoms，不空编")
            failed += 1
            continue
        if check_only:
            print(f"NEED {status} {src_dir.name}")
            failed += 1
            continue
        if dry_run:
            print(f"DRY would-write {status} {src_dir.name}")
            wrote += 1
            continue
        page = _build_page(src_dir, rec.get("id") or src_dir.name)
        (src_dir / "_digest.md").write_text(page, encoding="utf-8")
        print(f"wrote {src_dir.name} ({status})")
        wrote += 1
    if not check_only and not dry_run and wrote:
        st2 = collect_source_digest_status(ai)
        seen_fail: set[str] = set()
        for sid, rec in st2.get("sources", {}).items():
            if rec.get("status") not in ("missing_page", "old_digest", "stale"):
                continue
            path = rec.get("path") or f"requirements/sources/{sid}/_digest.md"
            src = ai / Path(path).parent
            key = str(src)
            if key in seen_fail:
                continue
            seen_fail.add(key)
            if src.name in frozen_ids:
                continue
            if _has_atoms(src) or (_doc_kind(src)[0] == "reference" and _has_facts(src)):
                print(f"FAIL still {rec.get('status')} {src.name}")
                failed += 1
    failed += _apply_wiki(
        ai,
        write=not dry_run and not check_only,
        audit=check_only,
        frozen_ids=frozen_ids,
    )
    print(f"done wrote={wrote} skip={skipped} fail={failed}")
    return 1 if failed else 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    return compile_workspace(args.root, dry_run=args.dry_run, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
