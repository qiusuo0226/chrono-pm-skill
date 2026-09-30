#!/usr/bin/env python3
"""模块 99：独立材料与参见。"""
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from compile_source_digests import compile_workspace  # noqa: E402
from enforce_workspace_upgrade import enforce  # noqa: E402
from _version import SKILL_VERSION  # noqa: E402


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _src(root: Path, sid: str, *, atoms: str, title: str, profile: str = "", kind: str = "") -> Path:
    d = root / "ai" / "requirements" / "sources" / sid
    head = ["---", f"source_id: {sid}"]
    if kind:
        head.append(f"doc_kind: {kind}")
    if profile:
        head.append(f"split_profile: {profile}")
    head.append("---")
    _write(d / "meta.md", "\n".join(head) + f"\n\n# {sid} — {title}\n")
    _write(d / "ledger.md", "| source_id | source_fingerprint |\n|---|---|\n" + f"| {sid} | abc |\n")
    _write(d / "atoms.md", atoms)
    return d


def _run(root: Path) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = compile_workspace(str(root))
    return code, buf.getvalue()


def _page(root: Path, sid: str) -> str:
    return (root / "ai" / "requirements" / "sources" / sid / "_digest.md").read_text(encoding="utf-8")


def _see(text: str) -> str:
    return text.split("## 参见", 1)[1] if "## 参见" in text else ""


def test_wl011_reverse_one_hop():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        a = _src(root, "SRC-A", title="甲", atoms="ATOM-1 条款\n- source_ref: 第1章\n见 SRC-B 已拆\n")
        b = _src(root, "SRC-B", title="乙", atoms="ATOM-1 条款\n- source_ref: 第2章\n见 SRC-C 已拆\n")
        c = _src(root, "SRC-C", title="丙", atoms="ATOM-1 条款\n- source_ref: 第3章\n")
        atoms = {p: p.read_text(encoding="utf-8") for p in (a / "atoms.md", b / "atoms.md", c / "atoms.md")}
        code, out = _run(root)
        assert code == 0, out
        see_a = _see(_page(root, "SRC-A"))
        see_b = _see(_page(root, "SRC-B"))
        see_c = _see(_page(root, "SRC-C"))
        assert "SRC-B" in see_a
        assert "SRC-A" in see_b
        assert "SRC-C" not in see_a
        assert "SRC-A" not in see_c
        for path, before in atoms.items():
            assert path.read_text(encoding="utf-8") == before


def test_wl012_existing_contract():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", title="招标", atoms="ATOM-1 条款\n- source_ref: 第1章\n合同 CON-1 在正文。不见 CON-999 。\n")
        _write(root / "ai" / "requirements" / "contract-register.md", "| 合同 | 名称 |\n|---|---|\n| CON-1 | 已有合同 |\n")
        code, out = _run(root)
        assert code == 0, out
        see = _see(_page(root, "SRC-001"))
        assert "CON-1" in see
        assert "CON-999" not in see
        assert not (root / "ai" / "requirements" / "sources" / "CON-999").exists()
        assert "没有可确定的需求" not in out


def test_wl005_mixed_children():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        atoms = (
            "ATOM-1 设立\n- source_ref: 第1章\nparent_ref: atoms.md#设立\n"
            "ATOM-2 其他\n- source_ref: 第2章\nparent_ref: atoms.md#其他\n"
        )
        _src(root, "SRC-001", title="两块", profile="4.1.0", atoms=atoms)
        _write(
            root / "ai" / "requirements" / "requirement-register.md",
            "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n"
            "| REQ-1 | 设立登记 | WP-1 | sources/SRC-001 ATOM-1 |\n",
        )
        _write(
            root / "ai" / "wps" / "WP-1.md",
            "# WP-1\n\n## 2. 关联需求\n\n| 需求编号 | 来源路径 |\n|---|---|\n| REQ-1 | — |\n",
        )
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "ATOM-1" in text and "REQ-1" in text and "WP-1" in text
        assert "ATOM-2 独立 atoms.md#其他" in text


def test_wl006_idempotent():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", title="独立材料", atoms="ATOM-1 条款\n- source_ref: 第1章\n")
        assert _run(root)[0] == 0
        first = _page(root, "SRC-001")
        log = root / "ai" / "logs" / "migration-log.md"
        decisions = root / "ai" / "pm-decisions.md"
        log_before = log.read_text(encoding="utf-8") if log.is_file() else ""
        dec_before = decisions.read_text(encoding="utf-8") if decisions.is_file() else ""
        assert _run(root)[0] == 0
        assert _page(root, "SRC-001") == first
        log_after = log.read_text(encoding="utf-8") if log.is_file() else ""
        dec_after = decisions.read_text(encoding="utf-8") if decisions.is_file() else ""
        assert log_after == log_before
        assert dec_after == dec_before
        assert "SRC-001" not in log_after


def test_wl007_stamp_when_independent():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / "ai" / "requirements" / "sources" / "SRC-001"
        _write(d / "meta.md", "---\nsource_id: SRC-001\n---\n\n# SRC-001 — 招标文件\n")
        _write(d / "ledger.md", "| source_id | source_fingerprint |\n|---|---|\n| SRC-001 | abc |\n")
        _write(d / "atoms.md", "ATOM-1 条款\n- source_ref: 第1章\n合同 CON-9 已写在材料里\n")
        _write(root / "ai" / "requirements" / "contract-register.md", "| 合同 | 名称 |\n|---|---|\n| CON-9 | 企业通 |\n")
        _write(d / "_digest.md", "# 旧页\n")
        _write(
            root / "ai" / ".skill-version.json",
            json.dumps({"skillVersion": "3.30.2", "workspaceSchemaVersion": "0.17.0", "mode": "single"}),
        )
        assert enforce(root) == 0
        text = _page(root, "SRC-001")
        assert "独立" in text
        assert "CON-9" in _see(text)
        assert "没有可确定的需求" not in text
        assert "[[" not in text
        assert not (root / "ai" / "wiki").exists()
        assert json.loads((root / "ai/.skill-version.json").read_text(encoding="utf-8"))["skillVersion"] == SKILL_VERSION


def main() -> None:
    test_wl011_reverse_one_hop()
    test_wl012_existing_contract()
    test_wl005_mixed_children()
    test_wl006_idempotent()
    test_wl007_stamp_when_independent()
    print("ok")


if __name__ == "__main__":
    main()
