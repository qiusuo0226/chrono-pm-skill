#!/usr/bin/env python3
"""VW-001/002: parse_todos 只读 §1.1、去重、WP 列正则。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from refresh_views import parse_todos, parse_scope_register, build_entities, parse_wp, parse_plans  # noqa: E402

AI = Path(__file__).resolve().parent / "fixtures" / "derive-scope"


def test_vw001_dedup_and_wp():
    tds = parse_todos(AI, "2026-09-10")
    ids = [t["id"] for t in tds]
    assert ids.count("TD-OWN-20260910-001") == 1, ids
    row = next(t for t in tds if t["id"] == "TD-OWN-20260910-001")
    assert row["wp"] == "WP-20260910-001", row
    assert row["wp"] not in ("0", "是", "—") or row["wp"].startswith("WP-")


def test_vw002_no_timesheet_col():
    tds = parse_todos(AI, "2026-09-10")
    assert all(t["wp"] != "0" for t in tds)
    assert all(t["wp"] != "是" for t in tds)


def test_reg101_filter():
    rows = parse_scope_register(AI)
    no = [r for r in rows if r["include"] == "否"]
    assert len(no) == 1 and no[0]["object_type"] == "对象乙"


def test_edg001_explicit_edges():
    wps = [parse_wp(AI / "wps" / "WP-20260910-001.md")]
    tds = parse_todos(AI, "2026-09-10")
    plans = parse_plans(AI)
    scopes = parse_scope_register(AI)
    ent = build_entities(wps, tds, [], [], {}, {}, [], "fp", "2026-09-10", [], plans=plans, scopes=scopes, req_pairs=[("功能甲", "REQ-001")])
    rel = {(r["from"], r["to"], r["type"]) for r in ent["relations"]}
    assert ("PLAN-20260910-001", "WP-20260910-001", "contains") in rel
    assert ("WP-20260910-001", "REQ-001", "implements") in rel
    assert ("TD-OWN-20260910-001", "WP-20260910-001", "binds") in rel
    assert ("SR-20260910-002", "WP-20260910-001", "scoped_to") in rel


if __name__ == "__main__":
    test_vw001_dedup_and_wp()
    test_vw002_no_timesheet_col()
    test_reg101_filter()
    test_edg001_explicit_edges()
    print("OK")
