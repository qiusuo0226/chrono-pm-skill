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
    rows = "\n".join(f"| {a} | `{a}` |" for a in atoms) or "| — | 本源未见 |"
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
        if not _has_atoms(src_dir):
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
            if _has_atoms(src):
                print(f"FAIL still {rec.get('status')} {src.name}")
                failed += 1
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
