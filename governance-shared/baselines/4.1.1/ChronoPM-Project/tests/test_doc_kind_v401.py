#!/usr/bin/env python3
"""模块 97：doc_kind 与参见。"""
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from compile_source_digests import compile_workspace  # noqa: E402
from refresh_views import compute_slice_fp  # noqa: E402


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _src(root: Path, sid: str, *, kind: str = "", note: str = "", atoms: str | None = "ATOM-1 条款\n- source_ref: 第1章\n", facts: str | None = None, title: str = "甲", extra: str = "") -> Path:
    d = root / "ai" / "requirements" / "sources" / sid
    head = ["---", f"source_id: {sid}"]
    if kind:
        head.append(f"doc_kind: {kind}")
    if note:
        head.append(f"doc_kind_note: {note}")
    head.append("---")
    _write(d / "meta.md", "\n".join(head) + f"\n\n# {sid} — {title}\n{extra}")
    _write(d / "ledger.md", "| source_id | source_fingerprint |\n|---|---|\n" + f"| {sid} | abc |\n")
    if atoms is not None:
        _write(d / "atoms.md", atoms)
    if facts is not None:
        _write(d / "facts.md", facts)
    _write(root / "ai" / ".skill-version.json", json.dumps({"skillVersion": "4.0.0", "workspaceSchemaVersion": "0.17.0", "mode": "single"}))
    return d


def _req(root: Path, sid: str, req: str = "REQ-1", wp: str = "WP-1", title: str = "甲", extra_rows: str = "") -> None:
    _write(
        root / "ai" / "requirements" / "requirement-register.md",
        "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n"
        f"| {req} | {title} | {wp} | sources/{sid} |\n{extra_rows}",
    )
    _write(
        root / "ai" / "wps" / f"{wp}.md",
        f"# {wp}\n\n## 2. 关联需求\n\n| 需求编号 | 来源路径 |\n|---|---|\n| {req} | requirements/sources/{sid}/ |\n",
    )


def _digest(root: Path) -> str:
    return (root / "ai/requirements/sources").as_posix()


def _page(root: Path, sid: str) -> str:
    return (root / "ai" / "requirements" / "sources" / sid / "_digest.md").read_text(encoding="utf-8")


def _run(root: Path, check_only: bool = False) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = compile_workspace(str(root), check_only=check_only)
    return code, buf.getvalue()


def test_dk001_reference_exempt():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference", note="**密评**方案")
        before = ""
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "非需求类" in text
        assert "**密评**方案" in text
        assert "没有可确定的需求" not in out
        log = root / "ai" / "logs" / "migration-log.md"
        assert not log.is_file() or "SRC-001" not in log.read_text(encoding="utf-8")
        assert "REFERENCE" not in out


def test_dk002_default_still_gaps():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001")
        code, out = _run(root)
        assert code == 0, out
        assert "没有可确定的需求" not in out
        assert "独立" in _page(root, "SRC-001")


def test_dk003_requirement_binds():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="requirement")
        _req(root, "SRC-001")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "REQ-1" in text and "WP-1" in text


def test_dk004_explicit_requirement_gaps():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="requirement")
        code, out = _run(root)
        assert code == 0, out
        assert "没有可确定的需求" not in out
        assert "独立" in _page(root, "SRC-001")


def test_dk005_reference_ignores_multi_req():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference")
        _write(
            root / "ai" / "requirements" / "requirement-register.md",
            "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n"
            "| REQ-1 | 甲 | WP-1 | sources/SRC-001 |\n"
            "| REQ-2 | 乙 | WP-1 | sources/SRC-001 |\n",
        )
        code, out = _run(root)
        assert code == 0, out
        assert "同时对上好几条需求" not in out


def test_dk006_unknown_kind():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="other")
        code, out = _run(root)
        assert code == 1
        assert "doc_kind 无法识别" in out


def test_dk007_idempotent():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference")
        assert _run(root)[0] == 0
        first = _page(root, "SRC-001")
        log = root / "ai" / "logs" / "migration-log.md"
        log_before = log.read_text(encoding="utf-8") if log.is_file() else ""
        assert _run(root)[0] == 0
        assert _page(root, "SRC-001") == first
        log_after = log.read_text(encoding="utf-8") if log.is_file() else ""
        assert log_after == log_before


def test_dk008_check_prints_reference():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference")
        code, out = _run(root, check_only=True)
        assert "REFERENCE SRC-001（豁免）" in out
        _src(root, "SRC-002", kind="reference", title="乙")
        # 正式跑不打印
        d = root / "ai" / "requirements" / "sources" / "SRC-002"
        code2, out2 = _run(root)
        assert code2 == 0, out2
        assert "REFERENCE" not in out2


def test_dk009_portfolio_refuses():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "ai" / "portfolio").mkdir(parents=True)
        (root / "ai" / "projects").mkdir()
        code, out = _run(root)
        assert code == 1
        assert "REFUSE" in out


def test_dk010_facts_only():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference", atoms=None, facts="硬件一台\n")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "facts.md" in text
        assert "非需求类" in text


def test_dk011_requirement_no_atoms():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="requirement", atoms=None)
        code, out = _run(root)
        assert code == 1
        assert not (root / "ai/requirements/sources/SRC-001/_digest.md").is_file()
        assert "无 atoms" in out


def test_dk012_register_unchanged():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference")
        reg = root / "ai" / "requirements" / "requirement-register.md"
        _write(reg, "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n| REQ-9 | 别的 | WP-9 | sources/SRC-009 |\n")
        before = reg.read_text(encoding="utf-8")
        code, out = _run(root)
        assert code == 0, out
        assert reg.read_text(encoding="utf-8") == before


def _ready_peer(root: Path, sid: str) -> None:
    d = _src(root, sid, kind="reference", title="乙" + sid, atoms="ATOM-X\n- source_ref: 第9章\n")
    fp = compute_slice_fp(d)
    _write(
        d / "_digest.md",
        "---\ndoc_type: source-digest\n"
        f"source_id: {sid}\nsource_fingerprint: abc\nslice_fingerprint: {fp}\n---\n\n# {sid}\n\n## 已绑\n\n非需求类\n",
    )


def test_dk013_see_existing_src():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _ready_peer(root, "SRC-002")
        _src(root, "SRC-001", kind="reference", extra="见 SRC-002\n")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "SRC-002" in text
        assert "非需求类" in text


def test_dk014_missing_id_not_created():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference", extra="见 SRC-999\n")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "SRC-999" not in text
        assert not (root / "ai/requirements/sources/SRC-999").exists()


def test_dk015_same_title():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference", title="同一标题")
        _src(root, "SRC-002", kind="reference", title="同一标题")
        code, out = _run(root)
        assert code == 0, out
        assert "没有可确定的需求" not in out
        assert "SRC-002" in _page(root, "SRC-001")
        assert "SRC-001" in _page(root, "SRC-002")


def test_dk016_see_does_not_replace_bind():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _ready_peer(root, "SRC-002")
        _src(root, "SRC-001", extra="见 SRC-002\n")
        _req(root, "SRC-001")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "REQ-1" in text and "WP-1" in text and "SRC-002" in text


def test_dk017_previous_digest():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _ready_peer(root, "SRC-B")
        _src(root, "SRC-A", kind="reference", extra="引用 SRC-B\n", title="另")
        code, out = _run(root)
        assert code == 0, out
        assert "SRC-B" in _page(root, "SRC-A")


def test_dk018_atoms_and_facts():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference", facts="规格一条\n")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "ATOM-1" in text
        assert "没有可确定的需求" not in out


def main() -> None:
    test_dk001_reference_exempt()
    test_dk002_default_still_gaps()
    test_dk003_requirement_binds()
    test_dk004_explicit_requirement_gaps()
    test_dk005_reference_ignores_multi_req()
    test_dk006_unknown_kind()
    test_dk007_idempotent()
    test_dk008_check_prints_reference()
    test_dk009_portfolio_refuses()
    test_dk010_facts_only()
    test_dk011_requirement_no_atoms()
    test_dk012_register_unchanged()
    test_dk013_see_existing_src()
    test_dk014_missing_id_not_created()
    test_dk015_same_title()
    test_dk016_see_does_not_replace_bind()
    test_dk017_previous_digest()
    test_dk018_atoms_and_facts()
    print("ok")


if __name__ == "__main__":
    main()
