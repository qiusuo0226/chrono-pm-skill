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
    return sorted(found)


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


def _apply_wiki(ai: Path, write: bool = True, audit: bool = False) -> int:
    """已拆标准文件串成链。写不出则记缺口并返回失败数。没拆过的源只把已绑写成无登记边或已有编号。

    doc_kind: reference 不查需求、不查工包、不计缺口。参见只收已存在的编号和完全相同的标题。
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
    direct: dict[str, set[str]] = {}
    refs: dict[str, list[str]] = {}
    for d in req_split:
        sid = d.name
        refs[sid] = _source_refs(d)
        direct[sid] = _direct_reqs(reg_text, sid, _atom_ids_in(d))
    chosen: dict[str, str] = {}
    for d in req_split:
        sid = d.name
        if not refs[sid]:
            gaps.append((sid, "切片没有章节或页码"))
            continue
        cands = direct[sid]
        if len(cands) > 1:
            gaps.append((sid, "同时对上好几条需求"))
            continue
        if len(cands) == 1:
            chosen[sid] = next(iter(cands))
            continue
        title = _title(d)
        titled = {
            next(iter(direct[other.name]))
            for other in req_split
            if other.name != sid and _title(other) == title and title and len(direct[other.name]) == 1
        }
        if len(titled) == 1:
            chosen[sid] = next(iter(titled))
        elif len(titled) > 1:
            gaps.append((sid, "同时对上好几条需求"))
        else:
            gaps.append((sid, "没有可确定的需求"))
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
    gapped = {sid for sid, _reason in gaps}
    if audit:
        for sid in sorted(reference):
            if sid not in gapped:
                print(f"REFERENCE {sid}（豁免）")
    for d in dirs:
        sid = d.name
        digest = d / "_digest.md"
        if not digest.is_file():
            continue
        if sid in gapped:
            continue
        old = _read(digest)
        if sid in reference:
            new = _mark_reference(old, reference[sid])
            new = _set_bind(new, ["非需求类"])
        elif sid in chosen:
            siblings = sorted(s for s in by_req[chosen[sid]] if s != sid)
            body = _bind_body([chosen[sid]], wp_of[sid], siblings)
            new = _set_bind(old, body)
        else:
            ids = sorted(set(_direct_reqs(reg_text, sid, [])) | set(_wp_ids_for(ai, sid, set(), reg_text)))
            body = [" / ".join(ids)] if ids else ["无登记边"]
            new = _set_bind(old, body)
        if write and new != old:
            digest.write_text(new, encoding="utf-8")
            new = _read(digest) if digest.is_file() else new
        digested = _digested(sources)
        see = _see_also(ai, sid, d, reg_text, contract_text, digested)
        see_body = see if see else ["无参见"]
        newer = _set_h2(new, "参见", see_body)
        if write and newer != new:
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
    for sid, rec in st.get("sources", {}).items():
        path = rec.get("path") or ""
        src_dir = ai / Path(path).parent if path else sources / sid
        if not src_dir.is_dir():
            src_dir = sources / sid
        key = str(src_dir)
        if key in seen:
            continue
        seen.add(key)
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
            if _has_atoms(src) or (_doc_kind(src)[0] == "reference" and _has_facts(src)):
                print(f"FAIL still {rec.get('status')} {src.name}")
                failed += 1
    failed += _apply_wiki(ai, write=not dry_run and not check_only, audit=check_only)
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
