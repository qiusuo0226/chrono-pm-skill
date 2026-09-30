#!/usr/bin/env python3
"""模块 98：父块绑定与待确认包。"""
import io
import sys
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import compile_source_digests as csd  # noqa: E402
from compile_source_digests import backfill_live_wps, compile_workspace  # noqa: E402
from refresh_views import _load_spec, compute_slice_fp, parse_wp, render_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().strftime("%Y%m%d")


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _src(root: Path, sid: str, *, profile: str = "", atoms: str = "ATOM-1 条款\n- source_ref: 第1章\n", title: str = "甲", kind: str = "", extra: str = "") -> Path:
    d = root / "ai" / "requirements" / "sources" / sid
    head = ["---", f"source_id: {sid}"]
    if kind:
        head.append(f"doc_kind: {kind}")
    if profile:
        head.append(f"split_profile: {profile}")
    head.append("---")
    _write(d / "meta.md", "\n".join(head) + f"\n\n# {sid} — {title}\n{extra}")
    _write(d / "ledger.md", "| source_id | source_fingerprint |\n|---|---|\n" + f"| {sid} | abc |\n")
    if atoms is not None:
        _write(d / "atoms.md", atoms)
    return d


def _reg(root: Path, rows: list[tuple[str, str, str, str]]) -> None:
    body = "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n"
    body += "".join(f"| {a} | {b} | {c} | {d} |\n" for a, b, c, d in rows)
    _write(root / "ai" / "requirements" / "requirement-register.md", body)


def _wp(root: Path, wp_id: str, req_ids: list[str], *, effect: str = "正常", status: str = "已规划", name: str = "包", superseded: str = "—") -> Path:
    rows = "".join(f"| {r} | — |\n" for r in req_ids)
    path = root / "ai" / "wps" / f"{wp_id}.md"
    _write(
        path,
        "---\n"
        "doc_type: work-package\n"
        f"wp_id: {wp_id}\n"
        f"status: {status}\n"
        f"effect: {effect}\n"
        f"superseded_by: {superseded}\n"
        "plan_ref:\n"
        "---\n\n"
        f"# {wp_id} - {name}\n\n"
        "## 2. 关联需求\n\n"
        "| 需求编号 | 来源路径 |\n|---|---|\n"
        f"{rows}",
    )
    return path


def _run(root: Path, check_only: bool = False) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = compile_workspace(str(root), check_only=check_only)
    return code, buf.getvalue()


def _backfill(root: Path, only=None) -> tuple[list[str], str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        created = backfill_live_wps(root / "ai", only)
    return created, buf.getvalue()


def _page(root: Path, sid: str) -> str:
    return _read(root / "ai" / "requirements" / "sources" / sid / "_digest.md")


def _section2(text: str) -> str:
    grab = False
    buf = []
    for line in text.splitlines():
        if line.startswith("## 2"):
            grab = True
            continue
        if grab and line.startswith("## "):
            break
        if grab:
            buf.append(line)
    return "\n".join(buf)


def _rules(name: str) -> str:
    return _read(ROOT / name)


def test_sb001_table_stays():
    text = _rules("source-split-skill/references/split-rules.md")
    assert "表头和单元格都留在父块" in text
    assert "不从半张表切开" in text


def test_sb002_figure_path():
    text = _rules("source-split-skill/references/split-rules.md")
    assert "figures/" in text
    assert "文字没读出" in text
    assert "相对路径" in text


def test_sb003_two_children():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        atoms = (
            "ATOM-1 设立\n- source_ref: 第1章\nparent_ref: atoms.md#设立\n"
            "ATOM-2 变更\n- source_ref: 第2章\nparent_ref: atoms.md#变更\n"
        )
        _src(root, "SRC-001", profile="4.1.0", atoms=atoms, title="两块")
        _reg(
            root,
            [
                ("REQ-1", "设立登记", "WP-1", "sources/SRC-001 ATOM-1"),
                ("REQ-2", "变更登记", "WP-2", "sources/SRC-001 ATOM-2"),
            ],
        )
        _wp(root, "WP-1", ["REQ-1"], name="设立登记")
        _wp(root, "WP-2", ["REQ-2"], name="变更登记")
        code, out = _run(root)
        assert code == 0, out
        assert "GAP SRC-001 同时对上好几条需求" not in out
        text = _page(root, "SRC-001")
        assert "ATOM-1" in text and "REQ-1" in text and "WP-1" in text
        assert "ATOM-2" in text and "REQ-2" in text and "WP-2" in text


def test_sb004_create_pending():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _reg(root, [("REQ-8", "设立登记", "WP-OLD", ""), ("REQ-9", "设立登记", "", "")])
        old = _wp(root, "WP-OLD", ["REQ-8"], name="设立登记")
        before = _read(old)
        created, out = _backfill(root)
        assert len(created) == 1, out
        assert "BACKFILL created=1" in out
        assert "哪个包" not in out
        wp_id = created[0]
        assert wp_id.startswith(f"WP-{TODAY}-")
        body = _read(root / "ai" / "wps" / f"{wp_id}.md")
        assert "status: 待确认" in body
        assert "effect: 正常" in body
        assert "superseded_by: —" in body
        assert "plan_ref:" in body
        assert f"# {wp_id} - 设立登记" in body
        assert _section2(body).count("REQ-9") == 1
        assert "REQ-8" not in _section2(body)
        assert _read(old) == before
        reg = _read(root / "ai" / "requirements" / "requirement-register.md")
        assert wp_id in reg
        again, out2 = _backfill(root)
        assert again == [], out2
        assert "BACKFILL created=0" in out2
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-C", profile="4.1.0", atoms="ATOM-1 设立\n- source_ref: 第1章\n", title="设立登记")
        _reg(root, [("REQ-9", "设立登记", "", "sources/SRC-C")])
        code, out3 = _run(root, check_only=True)
        assert code != 0
        assert not (root / "ai" / "wps").exists() or not list((root / "ai" / "wps").glob("WP-*.md")), out3


def test_sb005_live_keeps():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _reg(root, [("REQ-1", "设立登记", "", "sources/SRC-001")])
        path = _wp(root, "WP-1", ["REQ-1"], name="原包")
        before = _read(path)
        created, out = _backfill(root)
        assert created == [], out
        assert _read(path) == before
        assert "REQ-1" in _section2(_read(path))
        reg = _read(root / "ai" / "requirements" / "requirement-register.md")
        assert "WP-1" in reg
        assert len(list((root / "ai" / "wps").glob("WP-*.md"))) == 1


def test_sb006_deprecated_not_successor():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _reg(root, [("REQ-1", "设立登记", "WP-OLD", "")])
        old = _wp(root, "WP-OLD", ["REQ-1"], effect="废弃", name="旧包", superseded="—")
        before = _read(old)
        created, out = _backfill(root)
        assert len(created) == 1, out
        assert _read(old) == before
        assert "superseded_by: —" in _read(old)
        body = _read(root / "ai" / "wps" / f"{created[0]}.md")
        assert "WP-OLD" not in body
        assert "status: 待确认" in body


def test_sb007_named_resplit_sentence():
    rules = _rules("source-split-skill/references/split-rules.md")
    query = _rules("query-skill/references/query-rules.md")
    assert "指纹相同也执行" in rules
    assert "重新拆" in rules
    assert "再拆一下这份" in rules
    assert "split_profile: 4.1.0" in rules
    assert "未点名且指纹未变则跳过；点名强制重拆则执行" in query
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root, "SRC-001", profile="4.1.0")
        _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001")])
        _wp(root, "WP-1", ["REQ-1"], name="甲")
        _write(d / "_digest.md", "---\ndoc_type: source-digest\nsource_id: SRC-001\nslice_fingerprint: " + ("ab" * 32) + "\n---\n\n# 旧\n")
        before = _read(d / "_digest.md")
        code, out = _run(root)
        assert code == 0, out
        assert _read(d / "_digest.md") != before
        assert "split_profile: 4.1.0" in _read(d / "meta.md")


def test_sb008_glossary_unique():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", profile="4.1.0", atoms="ATOM-1 办理外资企业登记\n- source_ref: 第1章\nparent_ref: atoms.md#外资\n")
        _reg(root, [("REQ-1", "别的标题", "", "")])
        _wp(root, "WP-1", ["REQ-1"], name="外商投资企业")
        _write(
            root / "ai" / "context" / "domain-glossary.md",
            "## 1 说法\n\n| 编号 | 说法 | 登记名 | 路径 | 状态 | 来源 | 热度 |\n|---|---|---|---|---|---|---|\n"
            "| G-1 | 外资企业 | 外商投资企业 | — | confirmed | 测试 | 1 |\n",
        )
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "WP-1" in text and "REQ-1" in text
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", profile="4.1.0", atoms="ATOM-1 办理企业登记\n- source_ref: 第1章\n")
        _reg(root, [("REQ-1", "公司设立", "", "")])
        _wp(root, "WP-1", ["REQ-1"], name="公司")
        code, out = _run(root)
        assert code == 0, out
        assert "没有可确定的需求" not in out
        assert "独立" in _page(root, "SRC-001")
        assert _read(root / "ai" / "wps" / "WP-1.md").split("# ", 1)[1].startswith("WP-1 - 公司")
        assert len(list((root / "ai" / "wps").glob("WP-*.md"))) == 1


def test_sb009_ok_frozen():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root, "SRC-001", title="同一标题")
        _write(d / "facts.md", "一条事实\n")
        _write(d / "figures" / "FIG-1.webp", "fig")
        _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001")])
        _wp(root, "WP-1", ["REQ-1"])
        assert _run(root)[0] == 0
        snap = {
            "atoms": _read(d / "atoms.md"),
            "facts": _read(d / "facts.md"),
            "fig": (d / "figures" / "FIG-1.webp").read_bytes(),
            "page": _read(d / "_digest.md"),
        }
        d2 = _src(root, "SRC-002", title="同一标题", kind="reference")
        fp = compute_slice_fp(d2)
        _write(d2 / "_digest.md", f"---\ndoc_type: source-digest\nsource_id: SRC-002\nslice_fingerprint: {fp}\n---\n\n# SRC-002\n")
        code, out = _run(root)
        assert code == 0, out
        assert _read(d / "atoms.md") == snap["atoms"]
        assert _read(d / "facts.md") == snap["facts"]
        assert (d / "figures" / "FIG-1.webp").read_bytes() == snap["fig"]
        page = _read(d / "_digest.md")

        def _bind(text: str) -> str:
            buf: list[str] = []
            grab = False
            for line in text.splitlines():
                if line.startswith("## ") and "已绑" in line:
                    grab = True
                    buf = [line]
                    continue
                if grab and line.startswith("## "):
                    break
                if grab:
                    buf.append(line)
            return "\n".join(buf).rstrip()

        assert _bind(page) == _bind(snap["page"])
        assert "REQ-1" in _bind(page) and "WP-1" in _bind(page)
        assert "SRC-002" in page.split("## 参见", 1)[1]


def test_sb010_old_gap_no_rewrite():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root, "SRC-001")
        _write(d / "_digest.md", "# 保持\n")
        _write(root / "ai" / ".skill-version.json", '{"skillVersion": "3.30.2"}\n')
        atoms = _read(d / "atoms.md")
        code, out = _run(root)
        assert code == 0, out
        assert "没有可确定的需求" not in out
        text = _read(d / "_digest.md")
        assert "# 保持" in text
        assert "独立" in text
        assert "无参见" in text
        assert _read(d / "atoms.md") == atoms
        assert "3.30.2" in _read(root / "ai" / ".skill-version.json")


def test_sb011_reference_multi():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", kind="reference")
        _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001"), ("REQ-2", "乙", "WP-1", "sources/SRC-001")])
        code, out = _run(root)
        assert code == 0, out
        assert "同时对上好几条需求" not in out


def test_sb012_no_id_no_wp():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "ai" / "requirements" / "requirement-register.md", "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n")
        created, out = _backfill(root)
        assert created == [], out
        assert not (root / "ai" / "wps").exists() or not list((root / "ai" / "wps").glob("WP-*.md"))


def test_sb013_only_live():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001")
        _reg(root, [("REQ-1", "甲", "WP-LIVE", "sources/SRC-001")])
        _wp(root, "WP-DEAD", ["REQ-1"], effect="废弃", name="废")
        _wp(root, "WP-LIVE", ["REQ-1"], name="活")
        code, out = _run(root)
        assert code == 0, out
        text = _page(root, "SRC-001")
        assert "WP-LIVE" in text
        assert "WP-DEAD" not in text
        assert "哪个包" not in out


def test_sb014_two_live():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001")
        _reg(root, [("REQ-1", "甲", "", "sources/SRC-001")])
        _wp(root, "WP-A", ["REQ-1"], name="甲一")
        _wp(root, "WP-B", ["REQ-1"], name="甲二")
        created, out = _backfill(root)
        assert created == [], out
        code, out2 = _run(root)
        assert code == 0, out2
        text = _page(root, "SRC-001")
        assert "WP-A" in text and "WP-B" in text
        assert len(list((root / "ai" / "wps").glob("WP-*.md"))) == 2


def test_sb015_unnamed_skip():
    rules = _rules("source-split-skill/references/split-rules.md")
    assert "未点名且指纹相同，仍跳过" in rules
    assert "禁止二次拆解" in rules
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = _src(root, "SRC-001")
        _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001")])
        _wp(root, "WP-1", ["REQ-1"])
        assert _run(root)[0] == 0
        first = _read(d / "_digest.md")
        atoms = _read(d / "atoms.md")
        assert _run(root)[0] == 0
        assert _read(d / "_digest.md") == first
        assert _read(d / "atoms.md") == atoms


def test_sb016_pending_not_auto():
    rules = _rules("references/00-pm-main-rules.md")
    line = next(x for x in rules.splitlines() if "归属判定①" in x)
    assert "待确认" in line and "不进候选" in line
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        path = _wp(Path(tmp), "WP-P", ["REQ-1"], status="待确认", name="像一条待办")
        text = render_index([parse_wp(path)], _load_spec())
        live = text.split("## 2.")[0]
        assert "WP-P" in live
        assert "待确认" in live


def test_sb017_exact_title_only():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-A", kind="reference", title="设立登记业务")
        _src(root, "SRC-B", kind="reference", title="设立变更业务")
        _src(root, "SRC-C", kind="reference", title="完全相同的标题")
        _src(root, "SRC-D", kind="reference", title="完全相同的标题")
        code, out = _run(root)
        assert code == 0, out
        assert "SRC-B" not in _page(root, "SRC-A")
        assert "SRC-A" not in _page(root, "SRC-B")
        assert "SRC-D" in _page(root, "SRC-C")
        assert "SRC-C" in _page(root, "SRC-D")


def test_sb018_parent_in_bind():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(
            root,
            "SRC-001",
            profile="4.1.0",
            atoms="ATOM-1 设立\n- source_ref: 第1章\nparent_ref: atoms.md#设立\n",
        )
        _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001 ATOM-1")])
        _wp(root, "WP-1", ["REQ-1"])
        code, out = _run(root)
        assert code == 0, out
        assert "atoms.md#设立" in _page(root, "SRC-001")


def test_sb019_two_glossary_hits():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _src(root, "SRC-001", profile="4.1.0", atoms="ATOM-1 外资企业登记\n- source_ref: 第1章\n")
        _reg(root, [("REQ-1", "甲", "", ""), ("REQ-2", "乙", "", "")])
        _wp(root, "WP-A", ["REQ-1"], name="外商投资企业")
        _wp(root, "WP-B", ["REQ-2"], name="外商投资企业")
        _write(
            root / "ai" / "context" / "domain-glossary.md",
            "## 1 说法\n\n| 编号 | 说法 | 登记名 | 路径 | 状态 | 来源 | 热度 |\n|---|---|---|---|---|---|---|\n"
            "| G-1 | 外资企业 | 外商投资企业 | — | confirmed | 测试 | 1 |\n",
        )
        code, out = _run(root)
        assert code == 0, out
        assert "对上两个目标" not in out
        text = _page(root, "SRC-001")
        assert "WP-A" not in text and "WP-B" not in text
        assert "外商投资企业" not in text
        assert "独立" in text
        assert len(list((root / "ai" / "wps").glob("WP-*.md"))) == 2


def test_sb020_no_id_no_successor():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "ai" / "requirements" / "requirement-register.md", "| Req ID | 标题 | 工作包 | 来源 |\n|---|---|---|---|\n")
        old = _wp(root, "WP-OLD", [], effect="废弃", name="废", superseded="—")
        before = _read(old)
        created, out = _backfill(root)
        assert created == [], out
        assert _read(old) == before
        assert len(list((root / "ai" / "wps").glob("WP-*.md"))) == 1


def test_sb021_decorative_skip():
    text = _rules("source-split-skill/references/split-rules.md")
    assert "装饰图仍跳过" in text
    assert "不要求产生图文件" in text


def test_sb022_stale_and_old_not_rewritten():
    import tempfile
    calls = []
    orig = csd._build_page

    def wrapped(*args, **kwargs):
        calls.append(args[0].name if args else "")
        return orig(*args, **kwargs)

    csd._build_page = wrapped
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = _src(root, "SRC-001")
            _write(d / "facts.md", "事实\n")
            _write(d / "figures" / "a.webp", "x")
            _reg(root, [("REQ-1", "甲", "WP-1", "sources/SRC-001")])
            _wp(root, "WP-1", ["REQ-1"])
            _write(
                d / "_digest.md",
                "---\ndoc_type: source-digest\nsource_id: SRC-001\nslice_fingerprint: " + ("cd" * 32) + "\n---\n\n# 旧页\n",
            )
            snap_atoms = _read(d / "atoms.md")
            snap_facts = _read(d / "facts.md")
            snap_fig = (d / "figures" / "a.webp").read_bytes()
            calls.clear()
            code, out = _run(root)
            assert code == 0, out
            assert calls == []
            assert _read(d / "atoms.md") == snap_atoms
            assert _read(d / "facts.md") == snap_facts
            assert (d / "figures" / "a.webp").read_bytes() == snap_fig
            text = _read(d / "_digest.md")
            assert "# 旧页" in text
            assert "slice_fingerprint: " + ("cd" * 32) in text
            assert "REQ-1" in text and "WP-1" in text
            assert "## 参见" in text
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = _src(root, "SRC-002")
            _reg(root, [("REQ-2", "乙", "WP-2", "sources/SRC-002")])
            _wp(root, "WP-2", ["REQ-2"])
            _write(d / "_digest.md", "# 不是摘要页\n")
            calls.clear()
            code, out = _run(root)
            assert code == 0, out
            assert "SRC-002" not in calls
            text = _read(d / "_digest.md")
            assert text.startswith("# 不是摘要页")
            assert "REQ-2" in text and "WP-2" in text
            assert "## 已绑" in text and "## 参见" in text
    finally:
        csd._build_page = orig


def main() -> None:
    test_sb001_table_stays()
    test_sb002_figure_path()
    test_sb003_two_children()
    test_sb004_create_pending()
    test_sb005_live_keeps()
    test_sb006_deprecated_not_successor()
    test_sb007_named_resplit_sentence()
    test_sb008_glossary_unique()
    test_sb009_ok_frozen()
    test_sb010_old_gap_no_rewrite()
    test_sb011_reference_multi()
    test_sb012_no_id_no_wp()
    test_sb013_only_live()
    test_sb014_two_live()
    test_sb015_unnamed_skip()
    test_sb016_pending_not_auto()
    test_sb017_exact_title_only()
    test_sb018_parent_in_bind()
    test_sb019_two_glossary_hits()
    test_sb020_no_id_no_successor()
    test_sb021_decorative_skip()
    test_sb022_stale_and_old_not_rewritten()
    print("ok")


if __name__ == "__main__":
    main()
