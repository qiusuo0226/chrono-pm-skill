#!/usr/bin/env python3
"""ChronoPM Skill 发布前自动断言脚本（治理一致性防线）。

落位 governance/scripts/（developer-side，分发包不含）：
    python governance/scripts/audit_release.py

对应 governance/review-checklists/release-checklist.md 中"机器可判"检查项的
自动化兜底。任一断言失败 → 退出码非零 → 禁止发布。

断言清单（12 条）：
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
   12. 汇总：任一失败退出码非零

本脚本只读，不修改任何文件。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

FAILURES = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not ok:
        FAILURES.append(name)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def version_source() -> str:
    """单一版本源：scripts/_version.py 的 SKILL_VERSION。"""
    text = read(ROOT / "scripts" / "_version.py")
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


def is_retained(rel: str, ex: dict) -> bool:
    """复刻 pack.ps1 Test-Excluded 语义，判断文件是否进入分发包。"""
    rel = norm(rel)
    if rel in ex["exceptions"]:
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
        "VERSION": read(ROOT / "VERSION").strip(),
        "skill.json": json.loads(read(ROOT / "skill.json"))["version"],
    }
    skill_md = read(ROOT / "SKILL.md")
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
    skill_json = json.loads(read(ROOT / "skill.json"))
    lv = skill_json.get("blueprint", {}).get("lastVersion", "<缺失>")
    check("2. skill.json blueprint.lastVersion", lv == version, f"lastVersion={lv}")

    # 3. SKILL.md 版本表 + BLUEPRINT 当前版本 + §11.3 含当前版本行
    vt = re.search(r"Skill 包版本号（当前\s*([\d.]+)）", skill_md)
    ok3a = bool(vt) and vt.group(1) == version
    bp = read(ROOT / "SKILL_BLUEPRINT.md")
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
    suite = read(ROOT / "tests" / "regression-suite.md")
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
    ids = re.findall(r"^\|\s*([A-Z]{2,3}-[0-9A-Z]{1,4})\s*\|", suite, re.M)
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
    actual = {p.name for p in (ROOT / "references").glob("*.md")}
    expected = {f for f in actual if is_retained(f"references/{f}", ex)}
    missing = expected - listed
    extra = listed - actual
    check(
        "6. §15 规则索引表覆盖 references/（减分发包排除集）",
        not missing and not extra,
        f"缺失={sorted(missing) or '无'}, 多余={sorted(extra) or '无'}",
    )

    # 7/8. 幽灵引用（仓库内 + 分发包保留集）
    ref_files = sorted((ROOT / "references").glob("*.md"))
    sources = [(ROOT / "SKILL.md", "SKILL.md")] + [(p, f"references/{p.name}") for p in ref_files]
    in_repo_bad, dist_bad = [], []
    for path, label in sources:
        targets = extract_targets(read(path))
        for t in sorted(targets):
            if not (ROOT / t).is_file():
                in_repo_bad.append(f"{label}→{t}")
            elif is_retained(label, ex) and not is_retained(t, ex):
                dist_bad.append(f"{label}→{t}")
    check("7. 仓库内幽灵引用", not in_repo_bad, "; ".join(in_repo_bad) or "无")
    check("8. 分发包保留集幽灵引用", not dist_bad, "; ".join(dist_bad) or "无")

    # 9. 基线存在性
    baseline = ROOT / "governance" / "baselines" / version
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

    # 12. 汇总
    print()
    if FAILURES:
        print(f"== 审计失败：{len(FAILURES)}/11 类断言未通过，禁止发布 ==")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("== 审计通过：全部断言成立，可继续发布流程 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
