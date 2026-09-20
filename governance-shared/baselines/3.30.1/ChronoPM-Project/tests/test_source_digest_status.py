#!/usr/bin/env python3
"""SW-003 / SW-017：切片与原件指纹过期检测。"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from refresh_views import (  # noqa: E402
    collect_source_digest_status,
    compute_slice_fp,
    digest_status_cmp,
)


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _src(root: Path) -> Path:
    d = root / "ai" / "requirements" / "sources" / "SRC-001"
    d.mkdir(parents=True)
    atoms = "ATOM-1 条款甲\n"
    _write(d / "atoms.md", atoms)
    _write(
        d / "ledger.md",
        "| source_id | file | file_type | size_kb | source_fingerprint | file_created | source_version | description | parse_history |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| SRC-001 | original.pdf | pdf | 10 | abc123deadbeef | — | v1.0 | — | 1 |\n",
    )
    sl = compute_slice_fp(d)
    _write(
        d / "_digest.md",
        "---\n"
        "doc_type: source-digest\n"
        "source_id: SRC-001\n"
        "source_fingerprint: abc123deadbeef\n"
        f"slice_fingerprint: {sl}\n"
        "---\n\n# 页\n",
    )
    return d


def test_ok_when_both_match():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root)
        st = collect_source_digest_status(root / "ai")
        rec = st["sources"]["SRC-001"]
        assert rec["status"] == "ok", rec


def test_sw003_slice_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root)
        (d / "atoms.md").write_text("ATOM-1 条款甲\n改了\n", encoding="utf-8")
        rec = collect_source_digest_status(root / "ai")["sources"]["SRC-001"]
        assert rec["status"] == "stale" and rec.get("reason") == "slice", rec


def test_sw017_source_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root)
        text = (d / "_digest.md").read_text(encoding="utf-8")
        (d / "_digest.md").write_text(text.replace("abc123deadbeef", "ffffwrong"), encoding="utf-8")
        rec = collect_source_digest_status(root / "ai")["sources"]["SRC-001"]
        assert rec["status"] == "stale" and rec.get("reason") == "source", rec


def test_as_of_stripped_from_cmp():
    a = {"as_of": "2026-09-20", "algo": "sha256-aggregate_fp", "sources": {"X": {"status": "ok"}}}
    b = {"as_of": "2026-09-21", "algo": "sha256-aggregate_fp", "sources": {"X": {"status": "ok"}}}
    assert digest_status_cmp(a) == digest_status_cmp(b)


if __name__ == "__main__":
    test_ok_when_both_match()
    test_sw003_slice_mismatch()
    test_sw017_source_mismatch()
    test_as_of_stripped_from_cmp()
    print("ok")
