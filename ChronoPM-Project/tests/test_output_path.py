#!/usr/bin/env python3
"""模块 97：出文件路径与路由句。"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_output_path.py"
PKG = ROOT
_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def _run(root: Path, path: Path, batch: str | None = None, policy: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT), "--root", str(root), "--path", str(path)]
    if batch:
        cmd.extend(["--batch", batch])
    if policy:
        cmd.extend(["--policy", str(policy)])
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=_ENV)


def test_pv001_allow_outputs():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "ai" / "outputs" / "a.md"
        target.parent.mkdir(parents=True)
        target.write_text("x", encoding="utf-8")
        r = _run(root, target)
        assert r.returncode == 0, r.stdout + r.stderr
        assert r.stdout.startswith("ALLOW ")


def test_pv002_remap_root_file():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "报告.md"
        r = _run(root, target, batch="20260928120000")
        assert r.returncode == 2, r.stdout
        assert "ai/outputs/20260928120000/报告.md" in r.stdout


def test_pv003_outside():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        outside = Path(tmp).parent / "outside.md"
        r = _run(root, outside)
        assert r.returncode == 3, r.stdout


def test_pv004_fact_source():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "ai" / "requirements" / "foo.md"
        r = _run(root, target)
        assert r.returncode == 3, r.stdout


def test_pv005_chart():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "ai" / "wps" / "_wp-chart.md"
        r = _run(root, target)
        assert r.returncode == 0, r.stdout


def test_pv006_beside_ai():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "说明.md"
        r = _run(root, target, batch="20260928120001")
        assert r.returncode == 2, r.stdout
        assert r.stdout.strip().startswith("ai/outputs/")


def test_pv007_missing_marker():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        policy = Path(tmp) / "policy.md"
        policy.write_text("没有标记\n", encoding="utf-8")
        r = _run(root, root / "a.md", policy=policy)
        assert r.returncode == 3, r.stdout


def test_pv008_empty_rows():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        policy = Path(tmp) / "policy.md"
        policy.write_text(
            "<!-- output-path-policy:start -->\n| 裁决 | 落点 |\n|---|---|\n<!-- output-path-policy:end -->\n",
            encoding="utf-8",
        )
        r = _run(root, root / "ai" / "outputs" / "a.md", policy=policy)
        assert r.returncode == 3, r.stdout
        assert "没有可用裁决行" in r.stdout


def test_rt_dr_mt_sentences():
    skill = (PKG / "SKILL.md").read_text(encoding="utf-8")
    gap = (PKG / "skill-gap-skill" / "references" / "gap-capture-rules.md").read_text(encoding="utf-8")
    daily = (PKG / "references" / "01-daily-report-rules.md").read_text(encoding="utf-8")
    meeting = (PKG / "references" / "02-meeting-rules.md").read_text(encoding="utf-8")
    assert "生成报告/导出" in skill and "技能缺口" in skill
    assert "底线 13 优先" in skill
    assert "生成报告/导出" in gap
    assert "不建 `requirements/sources/`" in daily
    assert "doc_kind: reference" in daily and "日报文件" in daily
    assert "doc_kind: reference" in meeting and "开会文件" in meeting
    assert "没有独立文件" in meeting and "不建 `sources/`" in meeting
    assert "除非用户明示拆进 `sources/`" in meeting


def main() -> None:
    test_pv001_allow_outputs()
    test_pv002_remap_root_file()
    test_pv003_outside()
    test_pv004_fact_source()
    test_pv005_chart()
    test_pv006_beside_ai()
    test_pv007_missing_marker()
    test_pv008_empty_rows()
    test_rt_dr_mt_sentences()
    print("ok")


if __name__ == "__main__":
    main()
