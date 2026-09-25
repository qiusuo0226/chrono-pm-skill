#!/usr/bin/env python3
"""模块 95：升级程序强制与已拆标准文件串联。"""
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ["CHRONOPM_SKIP_USER_HOOK"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from compile_source_digests import compile_workspace  # noqa: E402
from enforce_workspace_upgrade import enforce, guard  # noqa: E402
from migrate_workspace import stamp_skill_version  # noqa: E402


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _project(root: Path, sid: str = "SRC-001", atoms: bool = True, req: bool = True, wp: bool = True, title: str = "甲") -> None:
    d = root / "ai" / "requirements" / "sources" / sid
    _write(d / "meta.md", f"---\nsource_id: {sid}\n---\n\n# {sid} — {title}\n")
    _write(
        d / "ledger.md",
        "| source_id | source_fingerprint |\n|---|---|\n"
        f"| {sid} | abc |\n",
    )
    if atoms:
        _write(d / "atoms.md", f"ATOM-1 条款\n- source_ref: 第1章\n")
    _write(d / "_digest.md", f"---\ndoc_type: source-digest\nsource_id: {sid}\nslice_fingerprint: abc\n---\n\n# {sid}\n\n## 已绑\n\n—\n")
    _write(root / "ai" / ".skill-version.json", json.dumps({"skillVersion": "3.30.2", "workspaceSchemaVersion": "0.17.0", "mode": "single"}))
    if req:
        _write(
            root / "ai" / "requirements" / "requirement-register.md",
            "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n"
            f"| REQ-1 | {title} | WP-1 | sources/{sid} |\n",
        )
    if wp:
        _write(
            root / "ai" / "wps" / "WP-1.md",
            f"# WP-1\n\n## 2. 关联需求\n\n| 需求编号 | 来源路径 |\n|---|---|\n| REQ-1 | requirements/sources/{sid}/ |\n",
        )


def test_ue001_copy_ids():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root)
        assert enforce(root) == 0
        text = (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8")
        assert "REQ-1" in text and "WP-1" in text
        assert "[[ " not in text and "[[" not in text


def test_ue002_unsplit_marker():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root, atoms=False, req=False, wp=False)
        from refresh_views import compute_slice_fp

        d = root / "ai/requirements/sources/SRC-001"
        fp = compute_slice_fp(d)
        digest = d / "_digest.md"
        digest.write_text(digest.read_text(encoding="utf-8").replace("slice_fingerprint: abc", f"slice_fingerprint: {fp}"), encoding="utf-8")
        assert compile_workspace(str(root)) == 0
        text = (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8")
        assert "无登记边" in text
        assert "REQ-" not in text


def test_ue004_placeholder_not_success_when_split_without_chain():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root, req=False, wp=False)
        before = (root / "ai/.skill-version.json").read_text(encoding="utf-8")
        assert enforce(root) == 1
        assert (root / "ai/.skill-version.json").read_text(encoding="utf-8") == before


def test_ue007_lower_skill_noop(monkeypatch=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root)
        data = json.loads((root / "ai/.skill-version.json").read_text(encoding="utf-8"))
        data["skillVersion"] = "9.9.9"
        (root / "ai/.skill-version.json").write_text(json.dumps(data), encoding="utf-8")
        digest = (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8")
        assert enforce(root) == 0
        assert (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8") == digest
        assert json.loads((root / "ai/.skill-version.json").read_text(encoding="utf-8"))["skillVersion"] == "9.9.9"


def test_ue010_stamp_blocked():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root, req=False, wp=False)
        assert stamp_skill_version(root / "ai", "single", gates_passed=False) is None
        assert json.loads((root / "ai/.skill-version.json").read_text(encoding="utf-8"))["skillVersion"] == "3.30.2"


def test_ue012_no_sources():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "ai").mkdir()
        (root / "ai/.skill-version.json").write_text(json.dumps({"skillVersion": "3.30.2"}), encoding="utf-8")
        assert compile_workspace(str(root)) == 0


def test_ue013_not_project():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        assert enforce(root) == 0
        assert not any(root.rglob("*"))


def test_ue015_same_title():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root, sid="SRC-001", title="新设名称")
        d2 = root / "ai" / "requirements" / "sources" / "SRC-002"
        _write(d2 / "meta.md", "---\nsource_id: SRC-002\n---\n\n# SRC-002 — 新设名称\n")
        _write(d2 / "atoms.md", "ATOM-2 条款\n- source_ref: 第2章\n")
        _write(d2 / "_digest.md", "---\ndoc_type: source-digest\nsource_id: SRC-002\n---\n\n# SRC-002\n\n## 已绑\n\n—\n")
        assert enforce(root) == 0
        reg = (root / "ai/requirements/requirement-register.md").read_text(encoding="utf-8")
        assert "sources/SRC-002" in reg
        page = (d2 / "_digest.md").read_text(encoding="utf-8")
        assert "REQ-1" in page and "WP-1" in page and "SRC-001" in page


def test_ue016_gap_exit():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root, req=False, wp=False)
        assert enforce(root) == 1
        log = (root / "ai/logs/migration-log.md").read_text(encoding="utf-8")
        assert "没有可确定的需求" in log
        assert (root / "ai/pm-decisions.md").is_file()


def test_ue017_no_wiki_dir():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _project(root)
        assert enforce(root) == 0
        assert not (root / "ai" / "wiki").exists()
        assert "[[" not in (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8")


def test_guard_allows_other_files():
    sys.stdin = __import__("io").StringIO(json.dumps({"tool_name": "write", "path": "readme.md"}))
    assert guard() == 0


if __name__ == "__main__":
    test_ue001_copy_ids()
    test_ue002_unsplit_marker()
    test_ue004_placeholder_not_success_when_split_without_chain()
    test_ue007_lower_skill_noop()
    test_ue010_stamp_blocked()
    test_ue012_no_sources()
    test_ue013_not_project()
    test_ue015_same_title()
    test_ue016_gap_exit()
    test_ue017_no_wiki_dir()
    test_guard_allows_other_files()
    print("ok")
