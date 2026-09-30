#!/usr/bin/env python3
"""v4.0.0 查询定位与说法表合并。对应回归 QL-001～QL-013。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QS = ROOT / "query-skill" / "scripts"
sys.path.insert(0, str(QS))
sys.path.insert(0, str(ROOT / "scripts"))

import glossary_table as gt  # noqa: E402
import query_locate as ql  # noqa: E402


def _gloss(rows: str) -> str:
    return (
        "---\ndoc_type: domain-glossary\n---\n\n# 领域术语词库\n\n"
        "## 1. 术语映射表\n\n"
        "| 编号 | 原词 | 标准词 | 类别 | context_hint | 状态 | 来源 | 首次出现 | 最近命中 | 命中次数 | 备注 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + rows
        + "\n## 2. 纠错映射表\n\n| 编号 | 错误写法 | 正确写法 | 类别 | 状态 | 来源 |\n| --- | --- | --- | --- | --- | --- |\n"
        "\n## 3. 待确认术语\n\n| 编号 | 术语 | 可能的标准名称 | 上下文 | 首次出现时间 | 状态 |\n| --- | --- | --- | --- | --- | --- |\n"
    )


def _ai(tmp: Path) -> Path:
    ai = tmp / "ai"
    (ai / "context").mkdir(parents=True)
    (ai / "wps").mkdir()
    (ai / "todos" / "2026-09-23").mkdir(parents=True)
    return ai


def test_ql001_unchanged(tmp: Path) -> None:
    ai = _ai(tmp / "a")
    wp = ai / "wps" / "WP-20260923-001.md"
    wp.write_text("# 办理\n\n来源指针：无\n", encoding="utf-8")
    (ai / "context" / "domain-glossary.md").write_text(
        _gloss("| G1 | 办理进度 | WP-20260923-001 | 业务 | — | confirmed | manual | 2026-09-23 | — | 0 | — |\n"),
        encoding="utf-8",
    )
    assert gt.apply_member(ai) == 0
    text = (ai / "context" / "domain-glossary.md").read_text(encoding="utf-8")
    assert gt.is_13col(text)
    # 合并后路径可能来自工作包解析；定位前确保有路径
    rows = gt.load_rows(text)
    for row in rows:
        if row["说法"] == "办理进度":
            row["路径"] = "wps/WP-20260923-001.md"
    (ai / "context" / "domain-glossary.md").write_text(gt._rewrite(text, rows), encoding="utf-8")
    gt.write_fact_stamps(ai)
    code = ql.locate(ai, "办理进度谁做后端")
    assert code == 0


def test_ql003_miss(tmp: Path) -> None:
    ai = _ai(tmp / "b")
    (ai / "context" / "domain-glossary.md").write_text(_gloss(""), encoding="utf-8")
    before = (ai / "context" / "domain-glossary.md").read_text(encoding="utf-8")
    assert ql.locate(ai, "完全无关的一句话xyz") == 2
    assert (ai / "context" / "domain-glossary.md").read_text(encoding="utf-8") == before


def test_ql004_ambiguous(tmp: Path) -> None:
    ai = _ai(tmp / "c")
    (ai / "wps" / "WP-20260923-001.md").write_text("a", encoding="utf-8")
    (ai / "wps" / "WP-20260923-002.md").write_text("b", encoding="utf-8")
    body = (
        "---\n---\n\n## 1. 术语映射表\n\n"
        "| 编号 | 说法 | 登记名 | 路径 | 状态 | 来源 | 热度 |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "| G1 | 进度 | A | wps/WP-20260923-001.md | pending | 词库 | 0 |\n"
        "| G2 | 进度 | B | wps/WP-20260923-002.md | pending | 别名表 | 0 |\n"
    )
    (ai / "context" / "domain-glossary.md").write_text(body, encoding="utf-8")
    assert ql.locate(ai, "进度") == 3


def test_ql005_portfolio(tmp: Path) -> None:
    root = tmp / "port"
    ai = root / "ai"
    (ai / "portfolio").mkdir(parents=True)
    (ai / "projects").mkdir()
    assert ql.main(["--project-root", str(root), "--text", "进度"]) == 4


def test_ql006_merge_idempotent(tmp: Path) -> None:
    ai = _ai(tmp / "m")
    (ai / "context" / "domain-glossary.md").write_text(
        _gloss("| G9 | 农专 | 农民专业合作社 | 主体 | — | confirmed | manual | 2026-09-23 | — | 1 | — |\n"),
        encoding="utf-8",
    )
    (ai / "context" / "active-entities.json").write_text(
        json.dumps({"alias_index": {"办件进度": {"id": "WP-1", "type": "wp", "path": "wps/WP-1.md"}}}),
        encoding="utf-8",
    )
    assert gt.merge_glossary(ai)[0] == 0
    n1 = len(gt.load_rows((ai / "context" / "domain-glossary.md").read_text(encoding="utf-8")))
    assert gt.merge_glossary(ai)[0] == 0
    n2 = len(gt.load_rows((ai / "context" / "domain-glossary.md").read_text(encoding="utf-8")))
    assert n1 == n2
    speeches = {r["说法"] for r in gt.load_rows((ai / "context" / "domain-glossary.md").read_text(encoding="utf-8"))}
    assert "农专" in speeches and "办件进度" in speeches


def test_ql011_register(tmp: Path) -> None:
    ai = _ai(tmp / "r")
    (ai / "context" / "domain-glossary.md").write_text(_gloss(""), encoding="utf-8")
    gt.merge_glossary(ai)
    assert ql.register(ai, "新说法", "WP-9", "wps/WP-9.md") == 0
    rows = gt.load_rows((ai / "context" / "domain-glossary.md").read_text(encoding="utf-8"))
    hit = [r for r in rows if r["说法"] == "新说法"]
    assert len(hit) == 1 and hit[0]["来源"] == "对话登记" and hit[0]["状态"] == "pending"


def test_ql013_heat_stamp(tmp: Path) -> None:
    ai = _ai(tmp / "h")
    (ai / "context" / "domain-glossary.md").write_text(
        _gloss("| G1 | 办理进度 | 办件 | 业务 | — | confirmed | manual | 2026-09-23 | — | 0 | — |\n"),
        encoding="utf-8",
    )
    assert gt.apply_member(ai) == 0
    state = json.loads((ai / ".state.json").read_text(encoding="utf-8"))
    before = state["fact_stamps"]["context/domain-glossary.md"]
    assert ql.flush_heat(ai, ["办理进度"]) == 0
    state = json.loads((ai / ".state.json").read_text(encoding="utf-8"))
    after = state["fact_stamps"]["context/domain-glossary.md"]
    assert before == after
    rows = gt.load_rows((ai / "context" / "domain-glossary.md").read_text(encoding="utf-8"))
    heat = [r["热度"] for r in rows if r["说法"] == "办理进度"][0]
    assert int(heat) >= 1


def test_query_rules_no_all() -> None:
    text = (ROOT / "query-skill" / "references" / "query-rules.md").read_text(encoding="utf-8")
    assert "refresh_views.py\" --project-root" not in text
    assert "--flush-heat" in text and "--register" in text


def main() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        test_ql001_unchanged(tmp)
        test_ql003_miss(tmp)
        test_ql004_ambiguous(tmp)
        test_ql005_portfolio(tmp)
        test_ql006_merge_idempotent(tmp)
        test_ql011_register(tmp)
        test_ql013_heat_stamp(tmp)
        test_query_rules_no_all()
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
