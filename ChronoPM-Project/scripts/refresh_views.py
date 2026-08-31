#!/usr/bin/env python3
"""派生视图生成器。列与指纹只读 view-spec.json。失败不留半文件。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC_PATH = HERE / "view-spec.json"
TPL = HERE.parent / "assets" / "templates"
LIVE_STATUS = {"待确认", "已规划", "进行中", "已完成"}


def _load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def _ai(root: Path) -> Path:
    cand = root / "ai"
    return cand if cand.is_dir() else root


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("." + path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _front(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+\S", line) and key:
            out[key] = str(out.get(key, "")) + "\n" + line
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            key = k.strip()
            out[key] = v.strip().strip('"').strip("'")
    return out


def _heading_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if not m:
        return ""
    t = m.group(1).strip()
    t = re.sub(r"^WP-\S+\s*[-—]\s*", "", t)
    return t


def _section(text: str, title: str) -> str:
    heads = list(re.finditer(r"^##\s+(.+)$", text, re.M))
    for i, h in enumerate(heads):
        if h.group(1).strip().startswith(title):
            start = h.end()
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            return text[start:end]
    return ""


def _table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells:
            rows.append(cells)
    return rows


def _table_header_from_template(path: Path, after: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if after:
        idx = text.find(after)
        text = text[idx:] if idx >= 0 else text
    for line in text.splitlines():
        if line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and not cells[0].startswith("---"):
                return cells
    return []


def check_spec(spec: dict) -> int:
    idx = _table_header_from_template(TPL / "wp-index-template.md", "## 1. 进行中")
    s3 = _table_header_from_template(TPL / "plan-template.md", "## 3. WP 引用简表")
    ok = True
    if idx != spec["wp_index_columns"]:
        print("SPEC-001 FAIL index header", idx, "!=", spec["wp_index_columns"], file=sys.stderr)
        ok = False
    if s3 != spec["plan_s3_columns"]:
        print("SPEC-001 FAIL plan §3 header", s3, "!=", spec["plan_s3_columns"], file=sys.stderr)
        ok = False
    if spec["wp_chart_fingerprint"] != [
        "编号", "名称", "plan_ref", "开始日", "结束日", "当前阶段名", "upstream", "downstream", "effect"
    ]:
        print("SPEC-001 FAIL chart fingerprint keys", file=sys.stderr)
        ok = False
    if ok:
        print("SPEC-001 OK")
        return 0
    return 2


def _latest_legal_day(ai: Path, today: str) -> str | None:
    todos = ai / "todos"
    if not todos.is_dir():
        return None
    days = []
    for p in todos.iterdir():
        if p.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}$", p.name) and p.name <= today and (p / "_index.md").is_file():
            days.append(p.name)
    return max(days) if days else None


def _cell(fm: dict, *keys: str) -> str:
    for k in keys:
        v = fm.get(k, "")
        if v and v not in ("[]", "—"):
            return v
    return "—"


def _listish(val: str) -> list[str]:
    if not val or val in ("—", "[]"):
        return []
    raw = re.findall(r"[A-Za-z0-9\u4e00-\u9fff\-]+", val)
    return [x for x in raw if x not in ("upstream", "downstream")]


def parse_wp(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = _front(text)
    wp_id = fm.get("wp_id") or path.stem.split(".")[0]
    name = _heading_title(text) or fm.get("name") or wp_id
    effect = fm.get("effect") or "正常"
    status = fm.get("status") or "待确认"
    plan_ref = fm.get("plan_ref") or "—"
    s1 = _section(text, "1.")
    start = end = owner = req = stage = "—"
    for row in _table_rows(s1):
        if len(row) >= 2:
            k, v = row[0], row[1]
            if "开始" in k:
                start = v or "—"
            elif "结束" in k:
                end = v or "—"
            elif k == "负责人":
                owner = v or "—"
            elif "关联需求" in k:
                req = v or "—"
            elif "所属阶段" in k or "关键阶段" in k:
                stage = v or "—"
    fps = []
    s3 = _section(text, "3.")
    rows = _table_rows(s3)
    if rows:
        hdr = rows[0]
        for row in rows[1:]:
            if row and row[0] and row[0] not in ("实体或功能点", "功能点"):
                fps.append(row[0])
    up = _listish(str(fm.get("related_wps", "")))
    # yaml nested related_wps: try section 2b
    s2b = _section(text, "2b")
    down: list[str] = []
    for row in _table_rows(s2b):
        if len(row) >= 2 and "后继" in row[0]:
            down = _listish(row[1])
        if len(row) >= 2 and "前置" in row[0]:
            up = _listish(row[1]) or up
    aliases = [name, wp_id] + fps
    supersedes = _listish(fm.get("supersedes", ""))
    for m in re.finditer(r"(?m)^\s+supersedes:\s*\n((?:\s+-\s+\S+[^\n]*\n)+)", text):
        supersedes += re.findall(r"-\s+(\S+)", m.group(1))
    aliases += supersedes
    sb = (fm.get("superseded_by") or "").strip()
    if sb in ("—", "-", "[]", "none"):
        sb = ""
    return {
        "id": wp_id,
        "name": name,
        "status": status,
        "effect": effect,
        "plan_ref": plan_ref if plan_ref else "—",
        "owner": owner,
        "start": start,
        "end": end,
        "stage": stage,
        "req": req,
        "path": f"wps/{path.name}",
        "upstream": up,
        "downstream": down,
        "fps": fps,
        "aliases": aliases,
        "supersedes": supersedes,
        "superseded_by": sb,
        "completed": fm.get("completed_at") or "—",
        "retired": fm.get("retired_at") or "—",
        "file": path,
    }


def _md_row(cols: list[str]) -> str:
    return "| " + " | ".join(cols) + " |"


def render_index(wps: list[dict], spec: dict) -> str:
    cols = spec["wp_index_columns"]
    hdr = _md_row(cols)
    sep = "|" + "|".join(["---"] * len(cols)) + "|"

    def rows(pred):
        out = []
        for w in wps:
            if not pred(w):
                continue
            out.append(_md_row([
                w["id"], w["name"], "废弃" if w["effect"] == "废弃" else w["status"],
                w["plan_ref"], w["owner"], w["stage"], w["req"], w["path"],
                " / ".join(w["upstream"]) or "—", " / ".join(w["downstream"]) or "—",
                w["completed"], w["retired"] if w["effect"] == "废弃" else "—",
            ]))
        return out or []

    live = rows(lambda w: w["effect"] != "废弃" and w["status"] != "已完成")
    done = rows(lambda w: w["effect"] != "废弃" and w["status"] == "已完成")
    dead = rows(lambda w: w["effect"] == "废弃")
    parts = [
        "---",
        "doc_type: wp-index",
        "derived: true",
        "---",
        "",
        "# WP 索引",
        "",
        "> 查找加速器。存在性以 WP 文件为准。由 refresh_views.py 覆盖生成。",
        "",
        "## 1. 进行中",
        "",
        hdr,
        sep,
        *live,
        "",
        "## 2. 已完成归档",
        "",
        hdr,
        sep,
        *done,
        "",
        "## 3. 废弃归档",
        "",
        hdr,
        sep,
        *dead,
        "",
    ]
    return "\n".join(parts) + "\n"


def _nid(wp_id: str) -> str:
    return "N_" + re.sub(r"[^A-Za-z0-9]", "_", wp_id)


def render_chart(wps: list[dict]) -> str:
    live = [w for w in wps if w["effect"] != "废弃" and w["status"] != "已完成"]
    by_plan: dict[str, list] = {}
    for w in live:
        by_plan.setdefault(w["plan_ref"] or "—", []).append(w)
    chunks = [
        "---",
        "doc_type: wp-chart",
        "derived: true",
        "---",
        "",
        "# 工作包总览图（派生视图）",
        "",
        "> 非事实源。由 refresh_views.py 覆盖生成。",
        "",
    ]
    for plan, group in by_plan.items():
        title = plan if plan != "—" else "未纳入计划"
        chunks.append(f"### {title}")
        chunks.append("")
        chunks.append("```mermaid")
        chunks.append("graph TD")
        linked = set()
        for w in group:
            for other in w["downstream"] + w["upstream"]:
                if any(x["id"] == other for x in group):
                    linked.add(w["id"])
                    linked.add(other)
        chained = [w for w in group if w["id"] in linked]
        independent = [w for w in group if w["id"] not in linked]
        if chained:
            chunks.append("  subgraph chain1 [\"有关联\"]")
            chunks.append("    direction LR")
            for w in chained:
                lab = f'{w["id"]}<br/>{w["name"]}<br/>{w["start"]} ~ {w["end"]}'
                chunks.append(f'    {_nid(w["id"])}["{lab}"]')
            for w in chained:
                for d in w["downstream"]:
                    if any(x["id"] == d for x in chained):
                        chunks.append(f'    {_nid(w["id"])} --> {_nid(d)}')
            chunks.append("  end")
        if independent:
            chunks.append("  subgraph indep [\"独立（无关联绑定）\"]")
            chunks.append("    direction TB")
            for w in independent:
                lab = f'{w["id"]}<br/>{w["name"]}'
                chunks.append(f'    {_nid(w["id"])}["{lab}"]')
            chunks.append("  end")
        chunks.append("```")
        chunks.append("")
    return "\n".join(chunks) + "\n"


def chart_fp(wps: list[dict], spec: dict) -> str:
    keys = spec["wp_chart_fingerprint"]
    live = [w for w in wps if w["effect"] != "废弃" and w["status"] != "已完成"]
    rows = []
    for w in sorted(live, key=lambda x: x["id"]):
        rec = {
            "编号": w["id"],
            "名称": w["name"],
            "plan_ref": w["plan_ref"],
            "开始日": w["start"],
            "结束日": w["end"],
            "当前阶段名": w["stage"],
            "upstream": ",".join(sorted(w["upstream"])),
            "downstream": ",".join(sorted(w["downstream"])),
            "effect": w["effect"],
        }
        rows.append("|".join(rec[k] for k in keys))
    return _sha("\n".join(rows))


def parse_ops_index(ai: Path) -> list[tuple[str, str]]:
    p = ai / "logs" / "ops" / "_index.md"
    if not p.is_file():
        return []
    rows = []
    for row in _table_rows(p.read_text(encoding="utf-8")):
        if len(row) < 2 or row[0] in ("日期", "date"):
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}", row[0]):
            continue
        rows.append((row[0][:10], (row[1] or "").strip()[:80]))
    return rows[-2:]


def parse_decision_titles(ai: Path) -> list[tuple[str, str]]:
    p = ai / "decisions" / "decision-log.md"
    if not p.is_file():
        return []
    out = []
    block = _section(p.read_text(encoding="utf-8"), "活跃决策") or p.read_text(encoding="utf-8")
    for row in _table_rows(block):
        if len(row) < 3 or row[0] in ("决策ID", "决策编号"):
            continue
        did = row[0].strip()
        if not did.startswith("D-"):
            continue
        title = row[2].strip()[:40]
        if title and title not in ("—", "-"):
            out.append((title, did))
    return out


def parse_req_titles(ai: Path) -> list[tuple[str, str]]:
    p = ai / "requirements" / "requirement-register.md"
    if not p.is_file():
        return []
    out = []
    for row in _table_rows(_section(p.read_text(encoding="utf-8"), "需求总览") or p.read_text(encoding="utf-8")):
        if len(row) < 2 or row[0] in ("Req ID", "需求编号"):
            continue
        rid = row[0].strip()
        if not rid.startswith("REQ"):
            continue
        title = row[1].strip()[:40]
        if title and title not in ("—", "-"):
            out.append((title, rid))
    return out


def render_brain(wps: list[dict], entities: dict, as_of: str, facts_fp: str, ops_rows: list[tuple[str, str]] | None = None) -> str:
    live = [w for w in wps if w["effect"] != "废弃" and w["status"] != "已完成"]
    lines = [
        "---",
        "doc_type: brain",
        f"as_of: {as_of}",
        f"facts_fingerprint: {facts_fp}",
        "generated_by: refresh_views.py",
        "---",
        "",
        "# 项目大脑",
        "",
        "> 派生快照。禁止手改。确认面只读 pm-decisions.md，本文件不复制。",
        "",
        "## 进行中 WP",
        "",
        "| WP 编号 | WP 名称 | 状态 | 负责人 | 计划 | 卡点 |",
        "|---|---|---|---|---|---|",
    ]
    for w in live:
        lines.append(_md_row([w["id"], w["name"], w["status"], w["owner"], w["plan_ref"], w["stage"]]))
    tds = sorted((e for e in entities["entities"] if e["type"] == "td"), key=lambda x: x["id"])
    lines += ["", "## 未办结待办", "", "| 编号 | 名称 | 状态 | Owner | WP |", "|---|---|---|---|---|"]
    for e in tds[:80]:
        lines.append(_md_row([e["id"], e["name"], e.get("status", "—"), e.get("owner", "—"), e.get("wp", "—")]))
    risks = [e for e in entities["entities"] if e["type"] in ("risk", "issue")]
    lines += ["", "## 开放风险/问题", ""]
    if not risks:
        lines.append("（无）")
    for e in risks:
        lines.append(f"- {e['id']} {e['name']}（{e.get('status','—')}）")
    lines += ["", "## 最近过程", ""]
    if ops_rows:
        for d, s in ops_rows:
            lines.append(f"- {d}：{s or '（无摘要）'}")
    else:
        lines.append("（无过程日志）")
    lines += ["", "## 别名跳转", "", "| 别名 | 指向 | 类型 |", "|---|---|---|"]
    n = 0
    seen: set[str] = set()
    people = [e for e in entities.get("entities") or [] if e.get("type") == "person"]
    srcs = [e for e in entities.get("entities") or [] if e.get("type") == "src"]
    alias_index = entities.get("alias_index") or {}
    ordered: list[tuple[str, str, str]] = []
    for w in live:
        for k in (w.get("name"), w.get("id")):
            if k:
                ordered.append((str(k), w["id"], "wp"))
    for e in people:
        if e.get("name"):
            ordered.append((e["name"], e["id"], "person"))
        for a in e.get("aliases") or []:
            ordered.append((str(a), e["id"], "person"))
    live_names = {w.get("name") for w in live}
    for k, v in alias_index.items():
        if (v or {}).get("type") != "term":
            continue
        dest = (v or {}).get("id") or ""
        if k in live_names:
            ordered.insert(0, (str(k), dest, "term"))
        else:
            ordered.append((str(k), dest, "term"))
    for e in srcs:
        for k in (e.get("name"), e.get("id")):
            if k:
                ordered.append((str(k), e.get("id") or "", "src"))
    for k, dest, typ in ordered:
        if n >= 80 or not k or k in ("—", "-") or k in seen:
            continue
        seen.add(k)
        lines.append(_md_row([str(k)[:40], dest, typ]))
        n += 1
    if n == 0:
        lines.append("（无）")
    lines += ["", "全文见 `context/active-entities.json` 的 alias_index。", ""]
    return "\n".join(lines) + "\n"


def parse_sources(ai: Path) -> list[dict]:
    """SRC meta 标题/编号进 alias。不读 atoms。"""
    root = ai / "requirements" / "sources"
    out: list[dict] = []
    if not root.is_dir():
        return out
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        meta = d / "meta.md"
        if not meta.is_file():
            continue
        try:
            text = meta.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = _front(text)
        sid = (fm.get("source_id") or d.name).strip()
        title = (fm.get("title") or "").strip()
        if not title:
            h = _heading_title(text)
            if "—" in h:
                title = h.split("—", 1)[-1].strip()
            elif "-" in h and h.startswith("SRC"):
                title = h.split("-", 1)[-1].strip()
            else:
                title = h
        for row in _table_rows(_section(text, "meta")):
            if len(row) >= 2 and row[0] in ("源文档名称", "名称"):
                title = title or row[1]
            if len(row) >= 2 and row[0] == "编号":
                sid = sid or row[1]
        aliases = [sid, d.name]
        if title and title not in aliases:
            aliases.append(title[:40])
        rel = f"requirements/sources/{d.name}/meta.md"
        out.append(
            {
                "id": sid,
                "type": "src",
                "name": title or sid,
                "status": "源",
                "path": rel,
                "aliases": [a for a in aliases if a and a not in ("—", "-")],
            }
        )
    return out


def parse_todos(ai: Path, day: str | None) -> list[dict]:
    if not day:
        return []
    out = []
    d = ai / "todos" / day
    if not d.is_dir():
        return out
    closed = {"已完成", "已取消", "已转出"}
    for p in d.glob("*.md"):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8")
        owner = _front(text).get("owner") or p.stem
        for row in _table_rows(_section(text, "1.")):
            if len(row) < 3 or row[0] in ("待办编号", "编号"):
                continue
            tid, title, st = row[0], row[1], row[2]
            if not tid.startswith("TD-"):
                continue
            if st in closed:
                continue
            wp = row[4] if len(row) > 4 else "—"
            out.append({"id": tid, "type": "td", "name": title, "status": st, "path": f"todos/{day}/{p.name}", "owner": owner, "wp": wp, "aliases": [title]})
    return out


def parse_register(path: Path, typ: str) -> list[dict]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    out = []
    open_st = {"开放", "监控中", "处理中", "未关闭"}
    for row in _table_rows(text):
        if len(row) < 3:
            continue
        rid = row[0]
        if not re.match(r"^[RI]-", rid):
            continue
        st = row[2] if len(row) > 2 else ""
        if st and st not in open_st and "开放" not in st and "监控" not in st and "处理" not in st:
            continue
        out.append({"id": rid, "type": typ, "name": row[1] if len(row) > 1 else rid, "status": st or "开放", "path": str(path.relative_to(path.parents[1] if path.parents[1].name != "ai" else path.parent.parent)), "aliases": [row[1]] if len(row) > 1 else []})
    return out


def parse_glossary(path: Path) -> tuple[dict, list]:
    alias = {}
    corrections = []
    if not path.is_file():
        return alias, corrections
    text = path.read_text(encoding="utf-8")
    s1 = _section(text, "1.")
    for row in _table_rows(s1):
        if len(row) < 6 or row[0] in ("编号",):
            continue
        gid, orig, canon, status = row[0], row[1], row[2], row[5] if len(row) > 5 else ""
        if status != "confirmed":
            continue
        rec = {"id": gid, "type": "term", "canonical": canon}
        alias[orig] = rec
        if canon and canon not in alias:
            alias[canon] = rec
    s2 = _section(text, "2.")
    for row in _table_rows(s2):
        if len(row) < 3 or row[0] in ("编号",):
            continue
        corrections.append({"wrong": row[1], "right": row[2], "src": "context/domain-glossary.md#纠错映射表"})
        alias[row[1]] = {"id": row[0], "type": "term", "canonical": row[2]}
    return alias, corrections


def parse_people(ai: Path, day: str | None) -> list[dict]:
    if not day:
        return []
    p = ai / "todos" / day / "_index.md"
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8")
    out = []
    alias_extra = {}
    s1 = _section(text, "1.")
    for row in _table_rows(s1):
        if len(row) < 1 or row[0] in ("姓名", "人员", "Name"):
            continue
        name = row[0]
        if not name or name in ("—",):
            continue
        out.append({"id": name, "type": "person", "name": name, "status": row[1] if len(row) > 1 else "在册", "path": f"todos/{day}/_index.md", "aliases": [name]})
    s6 = _section(text, "6.")
    for row in _table_rows(s6):
        if len(row) >= 2 and row[0] not in ("缩写", "现行缩写"):
            alias_extra[row[0]] = row[1]
    return out, alias_extra


def collect_facts(ai: Path, today: str) -> dict[str, str]:
    facts = {}
    wps = ai / "wps"
    if wps.is_dir():
        for p in wps.glob("WP-*.md"):
            facts[f"wps/{p.name}"] = _file_sha(p)
    day = _latest_legal_day(ai, today)
    if day:
        d = ai / "todos" / day
        for p in d.glob("*.md"):
            facts[f"todos/{day}/{p.name}"] = _file_sha(p)
    for rel in (
        "risks/risk-register.md",
        "issues/issue-register.md",
        "decisions/decision-log.md",
        "requirements/requirement-register.md",
        "requirements/_index.md",
        "requirements/sources/_index.md",
        "context/domain-glossary.md",
        "logs/ops/_index.md",
    ):
        p = ai / rel
        if p.is_file():
            facts[rel] = _file_sha(p)
    plans = ai / "plans"
    if plans.is_dir():
        for p in plans.glob("PLAN-*.md"):
            txt = p.read_text(encoding="utf-8")
            fm = _front(txt)
            if fm.get("status") == "废弃":
                continue
            facts[f"plans/{p.name}"] = _file_sha(p)
    src_root = ai / "requirements" / "sources"
    if src_root.is_dir():
        for d in src_root.iterdir():
            meta = d / "meta.md"
            if d.is_dir() and meta.is_file():
                facts[f"requirements/sources/{d.name}/meta.md"] = _file_sha(meta)
    return facts


def collect_journal(ai: Path) -> dict[str, str]:
    d = ai / "logs" / "journal"
    if not d.is_dir():
        return {}
    out = {}
    for p in d.glob("J-*.md"):
        out[f"logs/journal/{p.name}"] = _file_sha(p)
    return out


def aggregate_fp(m: dict[str, str]) -> str:
    blob = "\n".join(f"{k}={v}" for k, v in sorted(m.items()))
    return _sha(blob)


def load_state(ai: Path) -> dict:
    p = ai / ".state.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _put_alias(idx: dict, key: str, val: dict) -> None:
    if not key or key in ("—", "-", "[]"):
        return
    cur = idx.get(key)
    if cur and cur.get("type") == "term":
        return
    idx[key] = val


def _successor_id(w: dict, by_id: dict, seen: set | None = None) -> str:
    seen = seen or set()
    sid = (w.get("superseded_by") or "").strip()
    if not sid or sid in seen:
        return ""
    seen.add(sid)
    nxt = by_id.get(sid)
    if not nxt:
        return sid
    if nxt.get("effect") == "废弃":
        return _successor_id(nxt, by_id, seen) or sid
    return nxt["id"]


def build_entities(wps: list[dict], tds: list[dict], risks: list[dict], people: list[dict], people_abbr: dict, gloss_alias: dict, corrections: list, facts_fp: str, as_of: str, srcs: list[dict] | None = None) -> dict:
    entities = []
    alias_index = dict(gloss_alias)
    by_id = {w["id"]: w for w in wps}
    for w in wps:
        live = w["effect"] != "废弃"
        rec = {
            "id": w["id"],
            "type": "wp",
            "name": w["name"],
            "status": "废弃" if not live else w["status"],
            "path": w["path"],
            "aliases": w["aliases"],
            "supersedes": w.get("supersedes") or [],
            "superseded_by": w.get("superseded_by") or "",
        }
        if live and w["status"] != "已完成":
            entities.append(rec)
        dest = _successor_id(w, by_id) if not live else w["id"]
        if not dest:
            dest = w["id"]
        ptr = {"id": dest, "type": "wp"}
        for a in [w["id"], w["name"], *w["aliases"]]:
            _put_alias(alias_index, a, ptr)
    for e in tds + risks + people + (srcs or []):
        entities.append(e)
        ptr = {"id": e["id"], "type": e["type"]}
        _put_alias(alias_index, e["id"], ptr)
        for a in e.get("aliases", []):
            _put_alias(alias_index, a, ptr)
    for abbr, name in people_abbr.items():
        _put_alias(alias_index, abbr, {"id": name, "type": "person"})
    return {
        "as_of": as_of,
        "facts_fingerprint": facts_fp,
        "generated_by": "refresh_views.py",
        "entity_count": len(entities),
        "alias_count": len(alias_index),
        "entities": entities,
        "alias_index": alias_index,
        "term_corrections": corrections,
    }


def put_title_aliases(alias_index: dict, pairs: list[tuple[str, str]], typ: str, path: str) -> None:
    for title, eid in pairs:
        _put_alias(alias_index, title, {"id": eid, "type": typ, "path": path})
        _put_alias(alias_index, eid, {"id": eid, "type": typ, "path": path})


def patch_plan(ai: Path, wps: list[dict], spec: dict) -> bool:
    plans = ai / "plans"
    if not plans.is_dir():
        return False
    by_id = {w["id"]: w for w in wps if w["effect"] != "废弃"}
    changed = False
    for p in plans.glob("PLAN-*.md"):
        text = p.read_text(encoding="utf-8")
        fm = _front(text)
        if fm.get("status") == "废弃":
            continue
        s3 = _section(text, "3.")
        rows = _table_rows(s3)
        if not rows:
            continue
        hdr = rows[0]
        if hdr != spec["plan_s3_columns"]:
            continue
        new_rows = [hdr]
        for row in rows[1:]:
            if not row or not row[0].startswith("WP"):
                continue
            w = by_id.get(row[0])
            if not w:
                new_rows.append(row)
                continue
            window = f'{w["start"]}~{w["end"]}' if w["start"] != "—" else "—"
            new_rows.append([w["id"], w["name"], w["status"] if w["status"] != "进行中" else w["stage"], w["owner"], window, w["stage"]])
        body = [_md_row(r) if isinstance(r, list) else r for r in new_rows]
        sep = "|" + "|".join(["---"] * 6) + "|"
        table = "\n".join([_md_row(spec["plan_s3_columns"]), sep] + [_md_row(r) for r in new_rows[1:]])
        # replace first table in section 3
        new_text, n = re.subn(
            r"(## 3\. WP 引用简表[\s\S]*?)(\n\| WP 编号 \|[\s\S]*?\n)(?=\n## |\Z)",
            lambda m: m.group(1) + "\n" + table + "\n",
            text,
            count=1,
        )
        if n and new_text != text:
            _atomic_write(p, new_text)
            changed = True
    return changed


def run(root: Path, flags: argparse.Namespace) -> int:
    spec = _load_spec()
    rc = check_spec(spec)
    if rc != 0:
        return rc
    if flags.check_spec_only:
        return 0
    ai = _ai(root)
    today = date.today().isoformat()
    as_of = today
    facts = collect_facts(ai, today)
    journal = collect_journal(ai)
    facts_fp = aggregate_fp(facts)
    journal_fp = aggregate_fp(journal)
    prev = load_state(ai)
    if (
        not flags.force
        and prev.get("facts_fingerprint") == facts_fp
        and prev.get("journal_fingerprint") == journal_fp
        and flags.all
    ):
        print("fingerprints unchanged; skip write")
        return 0

    wps_dir = ai / "wps"
    wps = []
    if wps_dir.is_dir():
        for p in sorted(wps_dir.glob("WP-*.md")):
            try:
                wps.append(parse_wp(p))
            except Exception as e:
                print(f"skip {p.name}: {e}", file=sys.stderr)

    day = _latest_legal_day(ai, today)
    tds = parse_todos(ai, day)
    people_pair = parse_people(ai, day)
    people, abbr = people_pair if isinstance(people_pair, tuple) else ([], {})
    risks = parse_register(ai / "risks" / "risk-register.md", "risk")
    issues = parse_register(ai / "issues" / "issue-register.md", "issue")
    gloss_alias, corrections = parse_glossary(ai / "context" / "domain-glossary.md")
    srcs = parse_sources(ai)
    entities = build_entities(wps, tds, risks + issues, people, abbr, gloss_alias, corrections, facts_fp, as_of, srcs)
    put_title_aliases(entities["alias_index"], parse_decision_titles(ai), "decision", "decisions/decision-log.md")
    put_title_aliases(entities["alias_index"], parse_req_titles(ai), "req", "requirements/requirement-register.md")
    entities["alias_count"] = len(entities["alias_index"])
    ops_rows = parse_ops_index(ai)

    views = prev.get("views") or {}
    want_index = flags.all or flags.index
    want_chart = flags.all or flags.chart
    want_plan = flags.all or flags.plan
    want_brain = flags.all or flags.brain

    try:
        if want_index:
            _atomic_write(ai / "wps" / "_index.md", render_index(wps, spec))
            views["wp_index"] = {"as_of": as_of, "view_fingerprint": _sha(render_index(wps, spec)), "status": "ok"}
        if want_chart:
            body = render_chart(wps)
            _atomic_write(ai / "wps" / "_wp-chart.md", body)
            views["wp_chart"] = {"as_of": as_of, "view_fingerprint": chart_fp(wps, spec), "status": "ok"}
        if want_plan:
            ok = patch_plan(ai, wps, spec)
            views["plan_proj"] = {"as_of": as_of, "view_fingerprint": _sha("plan"), "status": "ok" if ok or True else "stale"}
        if want_brain:
            dumped = json.dumps(entities, ensure_ascii=False, separators=(",", ":"))
            _atomic_write(ai / "context" / "active-entities.json", dumped + "\n")
            views["active_entities"] = {"as_of": as_of, "view_fingerprint": _sha(json.dumps(entities, ensure_ascii=False, sort_keys=True)), "status": "ok"}
            brain = render_brain(wps, entities, as_of, facts_fp, ops_rows)
            if "## 待拍板" in brain or "## 等你裁定" in brain:
                print("brain must not contain pending section", file=sys.stderr)
                return 1
            _atomic_write(ai / "context" / "brain.md", brain)
            views["brain"] = {"as_of": as_of, "view_fingerprint": _sha(brain), "status": "ok"}
    except Exception as e:
        print(f"write failed: {e}", file=sys.stderr)
        return 1

    state = {
        "facts_fingerprint": facts_fp,
        "journal_fingerprint": journal_fp,
        "facts": facts,
        "journal": journal,
        "views": views,
    }
    _atomic_write(ai / ".state.json", json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    print("refresh_views ok", ai)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path("."))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--brain", action="store_true")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--chart", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--check-spec-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    flags = ap.parse_args(argv)
    if flags.check_spec or flags.check_spec_only:
        flags.check_spec_only = True
        return check_spec(_load_spec())
    if not (flags.all or flags.brain or flags.index or flags.chart or flags.plan):
        flags.all = True
    return run(flags.project_root, flags)


if __name__ == "__main__":
    sys.exit(main())
