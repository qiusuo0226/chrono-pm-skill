#!/usr/bin/env python3
"""ChronoPM Skill 发布前自动断言脚本（治理一致性防线）。

落位 governance-shared/scripts/（developer-side，分发包不含）：
    python governance-shared/scripts/audit_release.py

对应 governance/review-checklists/release-checklist.md 中"机器可判"检查项的
自动化兜底。任一断言失败 → 退出码非零 → 禁止发布。

断言清单：
    1. 版本六触点一致：_version.py / VERSION / skill.json version /
       SKILL.md frontmatter / README.md 标题+版本表 / README.en.md 标题+版本表
    2. skill.json blueprint.lastVersion == VERSION
    3. SKILL.md 版本控制表“当前版本” + SKILL_BLUEPRINT.md §1 当前版本 == VERSION，
       且 BLUEPRINT §11.3 演进表含当前版本行
    4. README.md + README.en.md 回归用例数（共 6 处）== regression-suite 统计表合计
    5. regression-suite 模块数 == 统计表行数，Case ID 去重数 == 合计
    6. SKILL.md §15 规则索引表覆盖 references/ 全部文件减去分发包排除集
    7. 仓库内幽灵引用：SKILL.md 与 references/ 引用的 references/templates 文件均存在
    8. 分发包幽灵引用：分发包保留集内文件引用的目标必须仍在保留集内
       （排除模型实读自 tools/pack-skill/scripts/pack.ps1，复刻其四类机制：
        目录排除 excludeDirs + 文件排除 excludeFiles + 路径排除 excludeFilePaths
        + 例外放行 includeExceptions。与 pack.ps1 保持一致，改动须同步）
    9. 基线存在性：governance/baselines/<VERSION>/ 目录存在
   10. README 目录树不标注仓库中不存在的顶层目录（workspace-template 类问题）
   11. 命名漂移守门：仓库根目录无 chrono-pm-*.zip 类漂移命名产物
   12. 统计类断言（v2.1.0 需求十一/D-20）：规则文件数/模板数自动统计，
       比对 README×2 与 BLUEPRINT §1 中标注的数字
   13. 双包一致性（v3.0.0 G-2）：ChronoPM-Portfolio 伴生包版本/命名/模式
       与主包一致 + 基线含双包快照
   14. 升级残留（阻断）：baselines/{v} 仍留 upgrade-plan-v{v}.md → FAIL；
       高于当前 VERSION 且无基线的在研 AP 至多 1；更低版本无基线 FAIL
   15. 模拟 pack：不得含 tests/**、SKILL_BLUEPRINT.md、16-skill-governance、
       SKILL_MODULE_MAP.md；必须含 source-split 规则+四模板；
       除包根外禁止 SKILL.md
   16. 有 references 无 SKILL.md：仅当主 SKILL 未路由到该子树才 FAIL
   17. ops / parse-log 模板单表 ≤7 列
   18. 汇总：失败退出码非零；警告仍允许发布

本脚本只读，不修改任何文件。
"""

import json
import re
import sys
from pathlib import Path

# __file__ = <repo>/governance-shared/scripts/audit_release.py → repo root
ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT = ROOT / "ChronoPM-Project"
PORTFOLIO = ROOT / "ChronoPM-Portfolio"
SHARED = ROOT / "governance-shared"

FAILURES = []
WARNINGS = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not ok:
        FAILURES.append(name)


def warn_check(name: str, ok: bool, detail: str = "") -> None:
    """警告级：打印 WARN 但不计入失败、不阻断发布。"""
    if ok:
        line = f"[PASS] {name}"
        if detail:
            line += f" — {detail}"
        print(line)
        return
    line = f"[WARN] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    WARNINGS.append(name)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def version_source() -> str:
    """单一版本源：ChronoPM-Project/scripts/_version.py 的 SKILL_VERSION。"""
    text = read(PROJECT / "scripts" / "_version.py")
    m = re.search(r'SKILL_VERSION\s*=\s*"([^"]+)"', text)
    if not m:
        raise RuntimeError("无法从 _version.py 解析 SKILL_VERSION")
    return m.group(1)


# ── pack.ps1 排除模型实读（四类机制，与 pack.ps1 保持一致，改动须同步） ──

def pack_exclusions() -> dict:
    text = read(ROOT / "tools" / "pack-skill" / "scripts" / "pack.ps1")

    def arr(var: str):
        m = re.search(re.escape(var) + r"\s*=\s*@\((.*?)\)", text, re.S)
        return re.findall(r'"([^"]+)"', m.group(1)) if m else []

    return {
        "dirs": arr("$excludeDirs"),
        "files": arr("$excludeFiles"),
        "paths": arr("$excludeFilePaths"),
        "exceptions": arr("$includeExceptions"),
    }


def norm(rel: str) -> str:
    return rel.replace("\\", "/")


def _ver_tuple(v: str):
    parts = []
    for x in re.split(r"[^\d]+", v or ""):
        if x:
            parts.append(int(x))
    return tuple(parts)


def _ver_cmp(a: str, b: str) -> int:
    ta, tb = _ver_tuple(a), _ver_tuple(b)
    n = max(len(ta), len(tb))
    ta = ta + (0,) * (n - len(ta))
    tb = tb + (0,) * (n - len(tb))
    return (ta > tb) - (ta < tb)


def simulated_pack_rels(skill_root: Path, ex: dict):
    """Yield pack-relative paths as if packing skill_root with pack.ps1 rules."""
    skip_dirs = {".git", "__pycache__", ".idea", ".qoder", "node_modules"}
    for p in skill_root.rglob("*"):
        if not p.is_file():
            continue
        rel = norm(str(p.relative_to(skill_root)))
        if any(part in skip_dirs for part in rel.split("/")):
            continue
        if is_retained(rel, ex):
            yield rel


def table_separator_col_counts(text: str):
    """Count columns from markdown table separator rows (|---|---|)."""
    counts = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = s.strip("|").split("|")
        if cells and all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in cells):
            counts.append(len(cells))
    return counts


def is_retained(rel: str, ex: dict) -> bool:
    """复刻 pack.ps1 Test-Excluded 语义，判断文件是否进入分发包。"""
    rel = norm(rel)
    if rel in ex["exceptions"]:
        return True
    for exc in ex["exceptions"]:
        if exc.endswith("/"):
            prefix = exc.rstrip("/")
            if rel == prefix or rel.startswith(prefix + "/"):
                return True
    parts = rel.split("/")
    if any(p in ex["dirs"] for p in parts):
        return False
    if parts[-1] in ex["files"]:
        return False
    if rel in ex["paths"]:
        return False
    return True


def all_repo_files():
    skip_dirs = {".git", "__pycache__", ".idea", ".qoder", "node_modules"}
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = norm(str(p.relative_to(ROOT)))
        if any(part in skip_dirs for part in rel.split("/")):
            continue
        yield rel


# ── 断言实现 ──

REF_PATTERNS = [
    re.compile(r"references/(\d{2}-[\w-]+\.md)"),
    re.compile(r"assets/templates/([\w.-]+\.md)"),
    re.compile(r"(?<![\w/.])(templates/([\w.-]+\.md))"),
]


def extract_targets(text: str):
    """提取文本中引用的 references/ 与 templates/ 目标（相对仓库根）。"""
    targets = set()
    for m in REF_PATTERNS[0].finditer(text):
        targets.add(f"references/{m.group(1)}")
    for m in REF_PATTERNS[1].finditer(text):
        targets.add(f"assets/templates/{m.group(1)}")
    for m in REF_PATTERNS[2].finditer(text):
        targets.add(f"assets/{m.group(1)}")
    return targets


def main() -> int:
    version = version_source()
    print(f"== ChronoPM release audit @ {ROOT} (版本源 {version}) ==\n")

    # 1. 版本六触点一致
    touches = {
        "_version.py": version,
        "VERSION": read(PROJECT / "VERSION").strip(),
        "skill.json": json.loads(read(PROJECT / "skill.json"))["version"],
    }
    skill_md = read(PROJECT / "SKILL.md")
    fm = re.search(r"^version:\s*([\d.]+)\s*$", skill_md, re.M)
    touches["SKILL.md frontmatter"] = fm.group(1) if fm else "<缺失>"
    for readme in ("README.md", "README.en.md"):
        rt = read(ROOT / readme)
        t = re.search(r"^#\s*ChronoPM\s+v([\d.]+)", rt, re.M)
        touches[f"{readme} 标题"] = t.group(1) if t else "<缺失>"
        v = re.search(r"Skill (?:版本|version)\s*\|\s*([\d.]+)", rt)
        touches[f"{readme} 版本表"] = v.group(1) if v else "<缺失>"
    bad = [f"{k}={v}" for k, v in touches.items() if v != version]
    check("1. 版本六触点一致", not bad, "; ".join(bad) or f"全部 == {version}")

    # 2. blueprint.lastVersion == VERSION
    skill_json = json.loads(read(PROJECT / "skill.json"))
    lv = skill_json.get("blueprint", {}).get("lastVersion", "<缺失>")
    check("2. skill.json blueprint.lastVersion", lv == version, f"lastVersion={lv}")

    # 3. SKILL.md 版本表 + BLUEPRINT 当前版本 + §11.3 含当前版本行
    vt = re.search(r"Skill 包版本号（当前\s*([\d.]+)）", skill_md)
    ok3a = bool(vt) and vt.group(1) == version
    bp = read(PROJECT / "SKILL_BLUEPRINT.md")
    bv = re.search(r"当前版本\s*\|\s*([\d.]+)", bp)
    ok3b = bool(bv) and bv.group(1) == version
    ok3c = f"| {version} |" in bp
    check(
        "3. SKILL.md 版本表 + BLUEPRINT 当前版本 + §11.3 演进表",
        ok3a and ok3b and ok3c,
        f"SKILL.md表={vt.group(1) if vt else '<缺失>'}, BLUEPRINT="
        f"{bv.group(1) if bv else '<缺失>'}, §11.3行={'有' if ok3c else '无'}",
    )

    # 4. README×2 回归用例数（6 处）== 回归套件统计表合计
    suite = read(PROJECT / "tests" / "regression-suite.md")
    total_m = re.search(r"\|\s*\*\*合计\*\*\s*\|\s*\*\*(\d+)\*\*", suite)
    suite_total = int(total_m.group(1)) if total_m else -1
    zh_patterns = [
        r"回归测试\s*\|\s*(\d+)\s*个用例",
        r"回归测试套件（(\d+)\s*个用例）",
        r"回归用例\s*\|\s*(\d+)\s*个",
    ]
    en_patterns = [
        r"Regression tests\s*\|\s*(\d+)\s*cases",
        r"Regression test suite\s*\((\d+)\s*cases\)",
        r"Regression cases\s*\|\s*(\d+)",
    ]
    mismatches = []
    for readme, pats in (("README.md", zh_patterns), ("README.en.md", en_patterns)):
        rt = read(ROOT / readme)
        for pat in pats:
            m = re.search(pat, rt)
            val = int(m.group(1)) if m else -1
            if val != suite_total:
                mismatches.append(f"{readme}:{pat[:18]}..={val}")
    check(
        "4. README×2 用例数（6 处）== 统计表合计",
        not mismatches and suite_total > 0,
        "; ".join(mismatches) or f"全部 == {suite_total}",
    )

    # 5. 模块数 == 统计表行数；Case ID 去重数 == 合计
    modules = len(re.findall(r"^## \d+\.", suite, re.M))
    stats_sec = suite.split("## 回归用例统计", 1)[-1]
    stat_rows = [
        ln for ln in stats_sec.strip().splitlines()
        if ln.startswith("|") and not ln.startswith("|---")
        and "模块" not in ln and "合计" not in ln
    ]
    ids = re.findall(r"^\|\s*([A-Z][A-Z0-9]{1,2}(?:-[A-Z]{1,4})?-[0-9A-Z]{1,4})\s*\|", suite, re.M)
    uniq = len(set(ids))
    ok5 = modules == len(stat_rows) and uniq == suite_total
    check(
        "5. 回归套件自洽（模块数/统计表/Case ID）",
        ok5,
        f"模块={modules}, 统计表行={len(stat_rows)}, 唯一Case ID={uniq}, 合计={suite_total}",
    )

    # 6. SKILL.md §15 索引表覆盖 references/（减分发包排除集）
    ex = pack_exclusions()
    sec15 = skill_md.split("## 15.", 1)[-1].split("\n## ", 1)[0]
    listed = set(re.findall(r"`(\d{2}-[\w-]+\.md)`", sec15))
    actual = {p.name for p in (PROJECT / "references").glob("*.md")}
    expected = {f for f in actual if is_retained(f"references/{f}", ex)}
    missing = expected - listed
    extra = listed - actual
    check(
        "6. §15 规则索引表覆盖 references/（减分发包排除集）",
        not missing and not extra,
        f"缺失={sorted(missing) or '无'}, 多余={sorted(extra) or '无'}",
    )

    # 7/8. 幽灵引用（仓库内 + 分发包保留集）
    ref_files = sorted((PROJECT / "references").glob("*.md"))
    sources = [(PROJECT / "SKILL.md", "SKILL.md")] + [(p, f"references/{p.name}") for p in ref_files]
    in_repo_bad, dist_bad = [], []
    for path, label in sources:
        targets = extract_targets(read(path))
        for t in sorted(targets):
            if not (PROJECT / t).is_file():
                in_repo_bad.append(f"{label}→{t}")
            elif is_retained(label, ex) and not is_retained(t, ex):
                dist_bad.append(f"{label}→{t}")
    check("7. 仓库内幽灵引用", not in_repo_bad, "; ".join(in_repo_bad) or "无")
    check("8. 分发包保留集幽灵引用", not dist_bad, "; ".join(dist_bad) or "无")

    # 9. 基线存在性
    baseline = SHARED / "baselines" / version
    check("9. 基线存在性 baselines/<VERSION>/", baseline.is_dir(), str(baseline))

    # 10. README 目录树不标注不存在的顶层目录
    tree_bad = []
    for readme in ("README.md", "README.en.md"):
        rt = read(ROOT / readme)
        for m in re.finditer(r"^[├└]──\s+([A-Za-z0-9_.-]+)/", rt, re.M):
            if not (ROOT / m.group(1)).is_dir():
                tree_bad.append(f"{readme}:{m.group(1)}/")
    check("10. README 目录树顶层目录真实存在", not tree_bad, "; ".join(tree_bad) or "无")

    # 11. 命名漂移守门：仓库根无 chrono-pm-*.zip 类漂移命名产物
    drift_zips = sorted(ROOT.glob("chrono-pm-*.zip"))
    drift_names = [z.name for z in drift_zips]
    check(
        "11. 命名漂移守门（无 chrono-pm-*.zip）",
        not drift_names,
        "; ".join(drift_names) if drift_names else "无漂移产物",
    )

    # 12. 统计类断言（v2.1.0 需求十一/D-20）：规则数/模板数自动统计比对
    n_rules = len(list((PROJECT / "references").glob("*.md")))
    n_templates = len(list((PROJECT / "assets" / "templates").glob("*.md")))
    stat_bad = []
    for readme in ("README.md", "README.en.md"):
        rt = read(ROOT / readme)
        zh = readme == "README.md"
        m_r = re.search(r"规则文件\s*\|\s*(\d+)\s*份" if zh else r"Rule files\s*\|\s*(\d+)", rt)
        m_t = re.search(r"文档模板\s*\|\s*(\d+)\s*个" if zh else r"Document templates\s*\|\s*(\d+)", rt)
        if not m_r or int(m_r.group(1)) != n_rules:
            stat_bad.append(f"{readme} 规则数={m_r.group(1) if m_r else '<缺失>'}")
        if not m_t or int(m_t.group(1)) != n_templates:
            stat_bad.append(f"{readme} 模板数={m_t.group(1) if m_t else '<缺失>'}")
    m_bp = re.search(r"(\d+) 份规则 \+ (\d+) 个模板", bp)
    if not m_bp or int(m_bp.group(1)) != n_rules or int(m_bp.group(2)) != n_templates:
        stat_bad.append(
            f"BLUEPRINT §1=({m_bp.group(1)},{m_bp.group(2)})" if m_bp else "BLUEPRINT §1=<缺失>"
        )
    check(
        "12. 统计类断言（规则数/模板数 vs README×2 + BLUEPRINT）",
        not stat_bad,
        "; ".join(stat_bad) or f"规则={n_rules}, 模板={n_templates} 全部一致",
    )

    # 13. 双包一致性（v3.0.0 G-2：双包版本一致 + 双基线 + 双包命名）
    pkg = PORTFOLIO
    dual_bad = []
    if not pkg.is_dir():
        dual_bad.append("ChronoPM-Portfolio/ 目录缺失")
    else:
        pv_file = pkg / "VERSION"
        pv = pv_file.read_text(encoding="utf-8").strip() if pv_file.is_file() else "<缺失>"
        if pv != version:
            dual_bad.append(f"Portfolio VERSION={pv}")
        pj_file = pkg / "skill.json"
        if pj_file.is_file():
            pj = json.loads(read(pj_file))
            if pj.get("name") != "chrono-pm-portfolio":
                dual_bad.append(f"Portfolio name={pj.get('name')}")
            if str(pj.get("version")) != version:
                dual_bad.append(f"Portfolio skill.json version={pj.get('version')}")
            if pj.get("modes") != ["viewer"]:
                dual_bad.append(f"Portfolio modes={pj.get('modes')}")
        else:
            dual_bad.append("Portfolio skill.json 缺失")
        if not (pkg / "SKILL.md").is_file():
            dual_bad.append("Portfolio SKILL.md 缺失")
    dual_baseline = SHARED / "baselines" / version / "ChronoPM-Portfolio"
    if not dual_baseline.is_dir():
        dual_bad.append(f"baselines/{version}/ChronoPM-Portfolio/ 双基线缺失")
    # 3.1.1+ 双子树：baselines/{v}/ChronoPM-Project/（3.1.0 及更早冻结快照不要求）
    proj_baseline = SHARED / "baselines" / version / "ChronoPM-Project"
    parts = [int(x) for x in version.split(".")[:3]]
    if parts >= [3, 1, 1] and not proj_baseline.is_dir():
        dual_bad.append(f"baselines/{version}/ChronoPM-Project/ 双子树缺失")
    check(
        "13. 双包一致性（版本/命名/viewer/双基线）",
        not dual_bad,
        "; ".join(dual_bad) or f"双包均 {version}，命名/模式/双基线齐备",
    )

    # 14. 升级残留（阻断）：有基线仍留该版 AP → FAIL；在研 AP 至多 1
    ap_fail = []
    in_progress = []
    for p in sorted(SHARED.glob("upgrade-plan-v*.md")):
        m = re.search(r"upgrade-plan-v(.+)\.md$", p.name)
        ver = m.group(1) if m else ""
        if not ver:
            ap_fail.append(p.name)
            continue
        has_baseline = (SHARED / "baselines" / ver).is_dir()
        if has_baseline:
            ap_fail.append(f"baselines/{ver} 仍留 {p.name}")
        elif _ver_cmp(ver, version) >= 0:
            in_progress.append(p.name)
        else:
            ap_fail.append(f"更低版本无基线 {p.name}")
    if len(in_progress) > 1:
        ap_fail.append("在研 AP 超过 1 份: " + ",".join(in_progress))
    check(
        "14. 升级残留 AP（有基线仍留 / 在研至多 1 / 低版本无基线）",
        not ap_fail,
        "; ".join(ap_fail) or (
            f"在研 AP={in_progress[0]}" if in_progress else "无残留 AP"
        ),
    )

    # 15. 模拟 pack：排除集 + 必含 source-split + 除根外禁止 SKILL.md
    packed = list(simulated_pack_rels(PROJECT, ex))
    packed_set = set(packed)
    pack_fail = []
    forbidden = []
    for rel in packed:
        if rel == "SKILL_BLUEPRINT.md" or rel.endswith("/SKILL_BLUEPRINT.md"):
            forbidden.append(rel)
        elif rel == "SKILL_MODULE_MAP.md" or rel.endswith("/SKILL_MODULE_MAP.md"):
            forbidden.append(rel)
        elif rel == "references/16-skill-governance-rules.md":
            forbidden.append(rel)
        elif rel.startswith("tests/") or rel == "tests":
            forbidden.append(rel)
    if forbidden:
        pack_fail.append("不得含=" + ",".join(forbidden[:8]))
    required = [
        "source-split-skill/references/split-rules.md",
        "source-split-skill/assets/templates/source-doc-meta-template.md",
        "source-split-skill/assets/templates/source-index-template.md",
        "source-split-skill/assets/templates/source-parse-log-template.md",
        "source-split-skill/assets/templates/source-atoms-index-template.md",
        "skill-gap-skill/references/gap-capture-rules.md",
        "skill-gap-skill/assets/templates/skill-gap-demand-template.md",
        "reply-norm-skill/references/reply-rules.md",
        "reply-norm-skill/CAPABILITY.md",
    ]
    missing_req = [r for r in required if r not in packed_set]
    if missing_req:
        pack_fail.append("缺=" + ",".join(missing_req))
    nested_skill = [r for r in packed if r.endswith("SKILL.md") and r != "SKILL.md"]
    if nested_skill:
        pack_fail.append("嵌套SKILL.md=" + ",".join(nested_skill))
    check(
        "15. 模拟 pack（排除 tests/BLUEPRINT/16/MODULE_MAP；含 source-split、skill-gap、reply-norm；无嵌套 SKILL.md）",
        not pack_fail,
        "; ".join(pack_fail) or f"保留 {len(packed)} 个文件",
    )

    # 16. 有 references 无 SKILL.md：仅当主 SKILL 未路由到该子树才 FAIL
    skill_md_text = skill_md
    orphan_fail = []
    for refs_dir in PROJECT.rglob("references"):
        if not refs_dir.is_dir():
            continue
        subtree = refs_dir.parent
        if subtree == PROJECT:
            continue
        rel_sub = norm(str(subtree.relative_to(PROJECT)))
        has_skill = (subtree / "SKILL.md").is_file()
        if has_skill:
            continue
        if rel_sub not in skill_md_text and f"{rel_sub}/" not in skill_md_text:
            orphan_fail.append(rel_sub)
    check(
        "16. 有 references 无 SKILL.md（主 SKILL 未路由才 FAIL）",
        not orphan_fail,
        "; ".join(orphan_fail) or "无未路由孤儿子树",
    )

    # 17. ops / parse-log 模板单表 ≤7 列
    col_fail = []
    col_targets = [
        PROJECT / "assets" / "templates" / "ops-log-template.md",
        PROJECT / "assets" / "templates" / "ops-log-index-template.md",
        PROJECT / "assets" / "templates" / "source-parse-log-template.md",
        PROJECT / "source-split-skill" / "assets" / "templates" / "source-parse-log-template.md",
        PROJECT / "assets" / "templates" / "pm-decisions-template.md",
        PROJECT / "assets" / "templates" / "requirement-index-template.md",
    ]
    seen = set()
    for path in col_targets:
        if not path.is_file():
            continue
        key = path.resolve()
        if key in seen:
            continue
        seen.add(key)
        counts = table_separator_col_counts(read(path))
        over = [c for c in counts if c > 7]
        if over:
            col_fail.append(f"{path.relative_to(PROJECT).as_posix()} 列={over}")
    parse_log_exists = (
        (PROJECT / "assets" / "templates" / "source-parse-log-template.md").is_file()
        or (PROJECT / "source-split-skill" / "assets" / "templates" / "source-parse-log-template.md").is_file()
    )
    ops_exists = (PROJECT / "assets" / "templates" / "ops-log-template.md").is_file()
    if not parse_log_exists:
        col_fail.append("缺 source-parse-log-template.md")
    if not ops_exists:
        col_fail.append("缺 ops-log-template.md")
    check(
        "17. ops/parse-log 模板单表 ≤7 列",
        not col_fail,
        "; ".join(col_fail) or "全部 ≤7",
    )

    # 18. 汇总
    print()
    if FAILURES:
        print(f"== 审计失败：{len(FAILURES)} 类断言未通过，禁止发布 ==")
        for f in FAILURES:
            print(f"  - {f}")
        if WARNINGS:
            print(f"另有 {len(WARNINGS)} 条警告（未计入失败）")
        return 1
    if WARNINGS:
        print(f"== 审计通过：阻断项全部成立；{len(WARNINGS)} 条警告不阻断发布 ==")
        for w in WARNINGS:
            print(f"  WARN - {w}")
        return 0
    print("== 审计通过：全部断言成立，可继续发布流程 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
