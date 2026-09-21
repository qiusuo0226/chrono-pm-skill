#!/usr/bin/env python3
"""UG-S03/04/05：存量编译。"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from compile_source_digests import compile_workspace  # noqa: E402
from refresh_views import collect_source_digest_status  # noqa: E402


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _src(root: Path, sid: str = "SRC-001", digest="old") -> Path:
    d = root / "ai" / "requirements" / "sources" / sid
    d.mkdir(parents=True, exist_ok=True)
    _write(d / "atoms.md", "ATOM-1 必须满足条款甲\n")
    _write(
        d / "ledger.md",
        "| source_id | file | file_type | size_kb | source_fingerprint | file_created | source_version | description | parse_history |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        f"| {sid} | original.pdf | pdf | 10 | abc123deadbeef | — | v1.0 | — | 1 |\n",
    )
    if digest == "old":
        _write(d / "_digest.md", f"# 旧摘要 {sid}\n")
    elif digest == "missing":
        pass
    return d


def test_compile_old_digest():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, digest="old")
        assert compile_workspace(str(root)) == 0
        rec = collect_source_digest_status(root / "ai")["sources"]["SRC-001"]
        assert rec["status"] == "ok", rec
        text = (root / "ai/requirements/sources/SRC-001/_digest.md").read_text(encoding="utf-8")
        assert "doc_type: source-digest" in text
        assert "ATOM-1" in text
        assert "[[wikilink]]" not in text


def test_no_atoms_fail():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / "ai" / "requirements" / "sources" / "SRC-EMPTY"
        d.mkdir(parents=True)
        _write(d / "ledger.md", "# l\n")
        assert compile_workspace(str(root)) == 1


def test_ok_not_rewritten():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root, digest="old")
        assert compile_workspace(str(root)) == 0
        first = (d / "_digest.md").read_text(encoding="utf-8")
        assert compile_workspace(str(root)) == 0
        second = (d / "_digest.md").read_text(encoding="utf-8")
        assert first == second


def test_refuse_portfolio_root():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "ai" / "portfolio").mkdir(parents=True)
        (root / "ai" / "projects").mkdir(parents=True)
        assert compile_workspace(str(root)) == 1


if __name__ == "__main__":
    test_compile_old_digest()
    test_no_atoms_fail()
    test_ok_not_rewritten()
    test_refuse_portfolio_root()
    print("ok")
