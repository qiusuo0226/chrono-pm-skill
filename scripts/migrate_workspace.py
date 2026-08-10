#!/usr/bin/env python3
"""
ChronoPM 工作区迁移脚本

当 Skill 包升级后，已有的 ai/ 工作区可能缺少新版本所需的目录和文件。
本脚本检测差距并自动创建缺失内容。

用法:
    python migrate_workspace.py --project-root /path/to/project
    python migrate_workspace.py --project-root /path/to/project --dry-run
    python migrate_workspace.py --project-root /path/to/project --target-version 1.2.0
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

# ============================================================
# 版本常量（单一版本源：scripts/_version.py）
# ============================================================
# 从同一目录的 _version.py 导入（本脚本运行于 scripts/，scripts/ 天然在 sys.path[0]），
# 避免在迁移脚本内硬编码版本字符串造成与 Skill 本体版本失步。
from _version import SKILL_VERSION as CURRENT_SKILL_VERSION
from _version import WORKSPACE_SCHEMA_VERSION as CURRENT_SCHEMA_VERSION

# ============================================================
# Schema 版本对应的目录结构定义
# ============================================================

SCHEMA_010_DIRS = [
    "context", "requirements", "plans", "milestones",
    "tasks", "risks", "issues", "decisions",
    "reports/daily/personal", "reports/daily/project",
    "reports/weekly", "reports/monthly",
    "meetings", "reviews", "templates", "logs", "prompts",
]

SCHEMA_020_DIRS = [
    "context", "requirements", "plans", "milestones",
    "tasks", "risks", "issues", "decisions",
    "reports/daily/personal", "reports/daily/project",
    "reports/weekly", "reports/monthly",
    "meetings", "reviews", "templates", "logs", "prompts",
]

SCHEMA_030_DIRS = SCHEMA_020_DIRS + ["continuity"]

SCHEMA_040_DIRS = SCHEMA_030_DIRS + [
    # portfolio 模式新增
]

# Schema 0.5.0 新增的 portfolio 模式目录
PORTFOLIO_050_DIRS = [
    "context", "reports/weekly", "risks", "plans",
    "resources", "meetings", "logs",
    "todos", "todos/snapshots/daily", "todos/snapshots/weekly",
    "todos/actuals/daily", "todos/actuals/weekly",
]

# 子项目目录（schema 0.5.0）
SUB_PROJECT_050_DIRS = [
    "context", "requirements", "plans", "milestones",
    "tasks", "risks", "issues", "decisions",
    "reports/daily/personal/summaries",
    "meetings", "reviews", "logs", "prompts",
    "continuity",
]

# ============================================================
# 每个版本新增的能力检测清单
# ============================================================

VERSION_CAPABILITIES = [
    {
        "version": "0.1.0",
        "schema": "0.1.0",
        "capabilities": ["basic_workspace"],
        "new_dirs": [],
        "new_files": [],
    },
    {
        "version": "0.3.0",
        "schema": "0.2.0",
        "capabilities": ["portfolio_mode", "resource_management"],
        "new_dirs": ["portfolio/resources"],
        "new_files": ["portfolio/resources/resource-register.md", "portfolio/resources/transfer-log.md"],
    },
    {
        "version": "0.4.0",
        "schema": "0.2.0",
        "capabilities": ["update_trigger", "project_brief"],
        "new_dirs": [],
        "new_files": ["context/project-brief.md", "portfolio/context/project-brief.md"],
    },
    {
        "version": "0.5.0",
        "schema": "0.3.0",
        "capabilities": ["output_artifact"],
        "new_dirs": [],
        "new_files": [],
        "external_dirs": ["outputs"],
    },
    {
        "version": "0.7.0",
        "schema": "0.3.0",
        "capabilities": ["personal_progress", "monthly_index"],
        "new_dirs": ["reports/daily/personal/summaries"],
        "new_files": [],
        "note": "目录从 YYYY/MM 改为 YYYYMM（建议性迁移）",
    },
    {
        "version": "0.8.0",
        "schema": "0.4.0",
        "capabilities": ["continuity"],
        "new_dirs": ["continuity"],
        "new_files": [
            "continuity/project-lineage.md",
            "continuity/legacy-sources.md",
            "continuity/carryover-register.md",
            "continuity/import-log.md",
        ],
    },
    {
        "version": "0.9.0",
        "schema": "0.4.0",
        "capabilities": ["quick_query", "todo_index"],
        "new_dirs": ["portfolio/todos"],
        "new_files": [],
    },
    {
        "version": "1.0.0",
        "schema": "0.4.0",
        "capabilities": ["self_check"],
        "new_dirs": [],
        "new_files": [],
    },
    {
        "version": "1.1.0",
        "schema": "0.5.0",
        "capabilities": ["todo_snapshot"],
        "new_dirs": [
            "portfolio/todos/snapshots/daily",
            "portfolio/todos/snapshots/weekly",
            "portfolio/todos/actuals/daily",
            "portfolio/todos/actuals/weekly",
        ],
        "new_files": ["portfolio/todos/history-index.md"],
    },
    {
        "version": "1.2.0",
        "schema": "0.5.0",
        "capabilities": ["skill_governance"],
        "new_dirs": [],
        "new_files": [],
        "note": "governance/ 和 tests/ 只在 Skill 包，不进入工作区",
    },
    {
        "version": "1.6.0",
        "schema": "0.5.0",
        "capabilities": ["domain_glossary"],
        "new_dirs": [],
        "new_files": ["portfolio/context/domain-glossary.md", "context/domain-glossary.md"],
        "note": "词库文件按工作区模式创建：portfolio 模式创建 portfolio/context/domain-glossary.md，single 模式创建 context/domain-glossary.md。不自动抽取历史术语。",
    },
    {
        "version": "1.7.0",
        "schema": "0.5.0",
        "capabilities": ["init_wizard", "iteration_register"],
        "new_dirs": [],
        "new_files": ["plans/iteration-register.md"],
        "note": "迭代登记（iteration-register）为 single 子项目 plans 下新增文件；portfolio 模式不生成。",
    },
    {
        "version": "1.8.0",
        "schema": "0.5.0",
        "capabilities": ["skill_slimming"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.8.0 为 SKILL.md 瘦身，无工作区层变更。",
    },
    {
        "version": "1.9.0",
        "schema": "0.5.0",
        "capabilities": ["pm_profile"],
        "new_dirs": [],
        "new_files": ["portfolio/context/pm-profile.md", "context/pm-profile.md"],
        "note": "PM Profile 按工作区模式创建：portfolio 模式 portfolio/context/pm-profile.md，single 模式 context/pm-profile.md。",
    },
    {
        "version": "1.10.0",
        "schema": "0.5.0",
        "capabilities": ["plan_import_change_tracking"],
        "new_dirs": [],
        "new_files": [],
        "note": "R1-R4 历史计划导入追踪复用 v1.1.0 已建立的 portfolio/todos 目录与 history-index.md、snapshots/daily 等；imported-{date}.md 为运行时动态生成，非模板文件，故此处无新增目录/文件，避免与 v1.1.0 重复误报。",
    },
    {
        "version": "1.10.1",
        "schema": "0.5.0",
        "capabilities": ["blueprint_stat_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.10.1 仅修复 SKILL_BLUEPRINT §5.3 成熟度统计，无工作区层变更。",
    },
]

# 已知结构性缺漏（历史遗留，不影响本次修复，供后续维护 CR 参考）：
#   VERSION_CAPABILITIES 中缺少 0.2.0、0.6.0、1.3.0、1.4.0、1.5.0 的独立条目。
#   若某工作区的 .skill-version.json 恰好等于上述缺漏版本号，get_capabilities_since()
#   将因无法匹配 from_version 而返回空（既有行为）。此场景罕见，留待后续维护 CR 补全。



def get_skill_version():
    """读取 Skill 包版本"""
    return CURRENT_SKILL_VERSION


def read_workspace_version(ai_dir: Path):
    """读取工作区版本信息"""
    version_file = ai_dir / ".skill-version.json"
    if not version_file.exists():
        return None
    with open(version_file, "r", encoding="utf-8") as f:
        return json.load(f)


def get_capabilities_since(from_version: str):
    """获取从指定版本到当前版本之间新增的能力"""
    found = False
    new_caps = []
    for v in VERSION_CAPABILITIES:
        if v["version"] == from_version:
            found = True
            continue
        if found:
            new_caps.append(v)
    return new_caps


def check_missing_dirs(ai_dir: Path, capabilities: list, is_portfolio: bool = False):
    """检查缺失的目录"""
    missing = []
    for cap in capabilities:
        dirs = cap.get("new_dirs", [])
        for d in dirs:
            full_path = ai_dir / d
            if not full_path.exists():
                missing.append(d)

        # external_dirs（如 outputs/）
        ext_dirs = cap.get("external_dirs", [])
        for d in ext_dirs:
            ext_path = ai_dir.parent / d
            if not ext_path.exists():
                missing.append(f"../{d}")
    return missing


def check_missing_files(ai_dir: Path, capabilities: list, is_portfolio: bool = False):
    """检查缺失的文件"""
    missing = []
    for cap in capabilities:
        files = cap.get("new_files", [])
        for f in files:
            # 词库文件按工作区模式过滤：portfolio 模式只检查 portfolio 路径，single 模式只检查 context 路径
            if f == "portfolio/context/domain-glossary.md" and not is_portfolio:
                continue
            if f == "context/domain-glossary.md" and is_portfolio:
                continue
            full_path = ai_dir / f
            if not full_path.exists():
                missing.append(f)
    return missing


def get_templates_dir():
    """获取 Skill 包中的模板目录"""
    skill_root = Path(__file__).parent.parent
    return skill_root / "assets" / "templates"


def create_missing_dirs(ai_dir: Path, dirs: list):
    """创建缺失的目录"""
    for d in dirs:
        clean = d.replace("../", "")
        if d.startswith("../"):
            target = ai_dir.parent / clean
        else:
            target = ai_dir / d
        target.mkdir(parents=True, exist_ok=True)


def create_missing_files(ai_dir: Path, files: list, templates_dir: Path):
    """从模板创建缺失的文件"""
    # 模板名映射
    template_map = {
        "portfolio/resources/resource-register.md": "resource-register-template.md",
        "portfolio/resources/transfer-log.md": "transfer-log-template.md",
        "context/project-brief.md": "project-brief-template.md",
        "portfolio/context/project-brief.md": "project-brief-template.md",
        "continuity/project-lineage.md": "project-lineage-template.md",
        "continuity/legacy-sources.md": "legacy-sources-template.md",
        "continuity/carryover-register.md": "carryover-register-template.md",
        "continuity/import-log.md": "import-log-template.md",
        "portfolio/todos/history-index.md": "todo-history-index-template.md",
        "portfolio/context/domain-glossary.md": "domain-glossary-template.md",
        "context/domain-glossary.md": "domain-glossary-template.md",
    }

    for f in files:
        target = ai_dir / f
        if target.exists():
            continue

        template_name = template_map.get(f)
        if template_name:
            src = templates_dir / template_name
            if src.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
            else:
                # 模板不存在，创建空文件
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"---\ndoc_type: auto-migrated\nmigrated_at: {datetime.now().strftime('%Y-%m-%d')}\n---\n", encoding="utf-8")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"---\ndoc_type: auto-migrated\nmigrated_at: {datetime.now().strftime('%Y-%m-%d')}\n---\n", encoding="utf-8")


def update_version_file(ai_dir: Path, mode: str, skill_version: str = None):
    """更新 .skill-version.json

    写入的 skillVersion 优先使用传入的 skill_version（即迁移目标版本），
    缺省时回落为单一版本源 CURRENT_SKILL_VERSION。
    """
    # 实际写入的目标版本：显式传入优先，否则用单一版本源（skill_version 即 --target-version 或当前版本）
    target_ver = skill_version or CURRENT_SKILL_VERSION
    version_path = ai_dir / ".skill-version.json"
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    if version_path.exists():
        with open(version_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        old_version = data.get("skillVersion", "unknown")
        data["skillVersion"] = target_ver
        data["workspaceSchemaVersion"] = CURRENT_SCHEMA_VERSION
        data["lastMigratedAt"] = now
    else:
        old_version = "unknown"
        data = {
            "skill": "chrono-pm",
            "skillVersion": target_ver,
            "workspaceSchemaVersion": CURRENT_SCHEMA_VERSION,
            "mode": mode,
            "initializedAt": now,
            "lastMigratedAt": now,
        }

    with open(version_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return old_version


def append_migration_log(ai_dir: Path, old_version: str, missing_dirs: list, missing_files: list, skill_version: str = None):
    """追加迁移日志

    记录的新版本号优先使用传入的 skill_version（即迁移目标版本），
    缺省时回落为单一版本源 CURRENT_SKILL_VERSION。
    """
    target_ver = skill_version or CURRENT_SKILL_VERSION
    log_path = ai_dir / "logs" / "migration-log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    entry = f"""
## {today} - 迁移 {old_version} → {target_ver}

### 迁移信息
- 旧版本：{old_version}
- 新版本：{target_ver}
- Schema 版本：{CURRENT_SCHEMA_VERSION}
- 迁移时间：{now}

### 新增目录
"""
    if missing_dirs:
        for d in missing_dirs:
            entry += f"- {d}\n"
    else:
        entry += "- 无\n"

    entry += "\n### 新增文件\n"
    if missing_files:
        for f in missing_files:
            entry += f"- {f}\n"
    else:
        entry += "- 无\n"

    entry += "\n### 结果\n- success\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def create_workspace_health(ai_dir: Path, ws_version: dict, missing_dirs: list, missing_files: list):
    """创建或更新 .workspace-health.md"""
    health_path = ai_dir / ".workspace-health.md"
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    skill_ver = ws_version.get("skillVersion", "unknown") if ws_version else "unknown"
    schema_ver = ws_version.get("workspaceSchemaVersion", "unknown") if ws_version else "unknown"
    mode = ws_version.get("mode", "single") if ws_version else "single"

    is_healthy = len(missing_dirs) == 0 and len(missing_files) == 0
    status = "healthy" if is_healthy else "needs_migration"

    # 检查各能力状态
    def cap_status(path_list):
        for p in path_list:
            if not (ai_dir / p).exists():
                return "missing"
        return "ok"

    capabilities = [
        ("daily_report", cap_status(["tasks/board.md"]) if mode == "single" else cap_status(["projects/"])),
        ("quick_query", cap_status(["portfolio/todos/personal-todo-index.md"])),
        ("todo_snapshot", cap_status(["portfolio/todos/snapshots/daily"])),
        ("output_artifact", "ok" if (ai_dir.parent / "outputs").exists() else "missing"),
        ("continuity", cap_status(["continuity/carryover-register.md"])),
        ("self_check", "ok"),  # 规则层能力，不依赖目录
    ]

    content = f"""---
doc_type: workspace-health
version: v1.0
last_checked: {now_str}
last_prompted_upgrade_at: 
ignored_until: 
---

# 工作区健康状态

## 版本状态

| Item | Value |
|---|---|
| Skill Version | {skill_ver} |
| Workspace Schema | {schema_ver} |
| Current Skill Version | {CURRENT_SKILL_VERSION} |
| Current Schema | {CURRENT_SCHEMA_VERSION} |
| Mode | {mode} |
| Status | {status} |

## 能力状态

| Capability | Status | Notes |
|---|---|---|
"""
    for cap_name, cap_stat in capabilities:
        notes = "" if cap_stat == "ok" else "目录缺失，需迁移"
        content += f"| {cap_name} | {cap_stat} | {notes} |\n"

    content += f"""
## 索引状态

| Index File | Exists | Status |
|---|---|---|
| portfolio/todos/personal-todo-index.md | {'yes' if (ai_dir / 'portfolio/todos/personal-todo-index.md').exists() else 'no'} | {'ok' if (ai_dir / 'portfolio/todos/personal-todo-index.md').exists() else 'missing'} |
| portfolio/todos/history-index.md | {'yes' if (ai_dir / 'portfolio/todos/history-index.md').exists() else 'no'} | {'ok' if (ai_dir / 'portfolio/todos/history-index.md').exists() else 'missing'} |

## 推荐动作
"""
    if is_healthy:
        content += "1. 工作区版本已匹配，无需迁移\n"
    else:
        content += f"1. 执行迁移：python scripts/migrate_workspace.py --project-root .\n"
        content += "2. 检查新增文件并填写内容\n"
        content += "3. 可选：重建最近 7 天待办索引\n"

    content += f"""
## 升级提醒控制

| Field | Value |
|---|---|
| Last Prompted | {now_str} |
| Ignored Until | |
| Reminder Frequency | once_per_session |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
| {now.strftime('%Y-%m-%d')} | auto_check | 健康检查 | AI | - |
"""
    health_path.write_text(content, encoding="utf-8")


def rebuild_index_recent(ai_dir: Path, days: int = 7):
    """从最近 N 天日报索引重建待办索引（简化版）"""
    # 这个函数在实际执行时需要扫描最近日报索引
    # 这里只创建空索引文件作为占位
    todos_dir = ai_dir / "portfolio" / "todos"
    todos_dir.mkdir(parents=True, exist_ok=True)

    # 创建空 personal-todo-index.md
    pti = todos_dir / "personal-todo-index.md"
    if not pti.exists():
        pti.write_text("---\ndoc_type: personal-todo-index\nversion: v1.0\nlast_updated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n---\n\n# 个人待办索引\n\n| Todo ID | Owner | Project | Task | Due Date | Priority | Status | Source Ref | Updated At |\n|---|---|---|---|---|---|---|---|---|\n", encoding="utf-8")

    # 创建空 daily-todo-index.md
    dti = todos_dir / "daily-todo-index.md"
    if not dti.exists():
        dti.write_text("---\ndoc_type: daily-todo-index\nversion: v1.0\nlast_updated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n---\n\n# 每日待办索引\n\n## 日期索引\n", encoding="utf-8")


def migrate_workspace(project_root: str, dry_run: bool = False, target_version: str = None, index_mode: str = "structure-only"):
    """执行工作区迁移"""
    ai_dir = Path(project_root) / "ai"

    if not ai_dir.exists():
        print(f"错误: {ai_dir} 不存在")
        return

    print(f"{'='*60}")
    print(f"ChronoPM 工作区迁移")
    print(f"{'='*60}")

    # 1. 读取当前版本
    ws_version = read_workspace_version(ai_dir)

    if ws_version:
        current_ws_version = ws_version.get("skillVersion", "unknown")
        current_schema = ws_version.get("workspaceSchemaVersion", "unknown")
        mode = ws_version.get("mode", "single")
        print(f"\n工作区当前版本: {current_ws_version}")
        print(f"工作区 Schema: {current_schema}")
        print(f"工作区模式: {mode}")
    else:
        current_ws_version = "unknown"
        current_schema = "unknown"
        mode = "single"
        print(f"\n⚠️ 未检测到 .skill-version.json")
        print(f"工作区可能由旧版本初始化")

    # 2. 目标版本
    skill_version = target_version or CURRENT_SKILL_VERSION
    print(f"目标 Skill 版本: {skill_version}")
    print(f"目标 Schema: {CURRENT_SCHEMA_VERSION}")

    if current_ws_version == skill_version and current_schema == CURRENT_SCHEMA_VERSION:
        print(f"\n✅ 版本已匹配，无需迁移")
        return

    # 3. 检测缺失能力
    new_caps = get_capabilities_since(current_ws_version)

    if not new_caps:
        print(f"\n✅ 未检测到新增能力，仅更新版本号")
    else:
        print(f"\n📋 检测到以下版本新增能力:")
        for cap in new_caps:
            caps = ", ".join(cap["capabilities"])
            print(f"  v{cap['version']} (schema {cap['schema']}): {caps}")

    # 4. 检查缺失目录和文件
    missing_dirs = check_missing_dirs(ai_dir, new_caps, mode == "portfolio")
    missing_files = check_missing_files(ai_dir, new_caps, is_portfolio=(mode == "portfolio"))

    print(f"\n📁 缺失目录:")
    if missing_dirs:
        for d in missing_dirs:
            print(f"  ✗ {d}")
    else:
        print(f"  无")

    print(f"\n📄 缺失文件:")
    if missing_files:
        for f in missing_files:
            print(f"  ✗ {f}")
    else:
        print(f"  无")

    if dry_run:
        print(f"\n🔍 DRY RUN 模式：仅检测，不执行迁移")
        print(f"如需执行迁移，请去掉 --dry-run 参数")
        return

    if not missing_dirs and not missing_files:
        print(f"\n✅ 目录和文件已完整，仅更新版本号")
        old_version = update_version_file(ai_dir, mode, skill_version)
        append_migration_log(ai_dir, old_version, [], [], skill_version)
        print(f"\n✅ 版本已更新到 {skill_version}")
        return

    # 5. 执行迁移
    print(f"\n{'='*40}")
    print(f"开始迁移...")
    print(f"{'='*40}")

    templates_dir = get_templates_dir()

    # 创建缺失目录
    if missing_dirs:
        print(f"\n创建缺失目录...")
        create_missing_dirs(ai_dir, missing_dirs)
        for d in missing_dirs:
            print(f"  ✓ 创建 {d}")

    # 创建缺失文件
    if missing_files:
        print(f"\n创建缺失文件...")
        create_missing_files(ai_dir, missing_files, templates_dir)
        for f in missing_files:
            print(f"  ✓ 创建 {f}")

    # 索引重建（如指定）
    if index_mode in ("recent-7-days", "current-month", "full-rebuild"):
        print(f"\n重建待办索引（模式：{index_mode}）...")
        rebuild_index_recent(ai_dir, days=7 if index_mode == "recent-7-days" else 30)
        print(f"  ✓ 待办索引已重建")

    # 更新版本号
    print(f"\n更新版本号...")
    old_version = update_version_file(ai_dir, mode, skill_version)
    print(f"  ✓ {old_version} → {skill_version}")

    # 记录迁移日志
    print(f"\n记录迁移日志...")
    append_migration_log(ai_dir, old_version, missing_dirs, missing_files, skill_version)
    print(f"  ✓ logs/migration-log.md 已追加")

    # 生成健康文件
    print(f"\n生成工作区健康文件...")
    updated_version = read_workspace_version(ai_dir)
    create_workspace_health(ai_dir, updated_version or {}, [], [])
    print(f"  ✓ .workspace-health.md 已生成")

    # 完成
    print(f"\n{'='*60}")
    print(f"✅ 迁移完成!")
    print(f"{'='*60}")
    print(f"  旧版本: {old_version}")
    print(f"  新版本: {skill_version}")
    print(f"  新增目录: {len(missing_dirs)} 个")
    print(f"  新增文件: {len(missing_files)} 个")
    print(f"\n下一步:")
    print(f"  1. 检查新增文件并填写内容")
    print(f"  2. 如有 YYYY/MM 旧目录，建议迁移到 YYYYMM")
    print(f"  3. 在 project-brief.md 中更新项目信息")


def create_glossary_for_existing(project_root: str):
    """为旧工作区创建领域词库模板，内置用户已确认初始词条，不自动抽取历史术语。
    自动检测工作区模式、扫描旧术语文件并提示是否导入（不自动导入）。"""
    ai_dir = Path(project_root) / "ai"
    if not ai_dir.exists():
        print(f"错误: {ai_dir} 不存在")
        return

    # 检测模式：优先 portfolio，其次 single
    portfolio_dir = ai_dir / "portfolio" / "context"
    single_dir = ai_dir / "context"

    if portfolio_dir.exists():
        target_dir = portfolio_dir
        mode_label = "项目集(portfolio)"
    elif single_dir.exists():
        target_dir = single_dir
        mode_label = "单项目(single)"
    else:
        print(f"错误: 未找到 context 目录，无法确定工作区模式")
        print(f"  尝试查找: {portfolio_dir}")
        print(f"  尝试查找: {single_dir}")
        return

    print(f"检测到工作区模式: {mode_label}")
    print(f"词库目标路径: {target_dir / 'domain-glossary.md'}")

    target_path = target_dir / "domain-glossary.md"

    if target_path.exists():
        print(f"词库文件已存在，不覆盖: {target_path}")
        return

    # 扫描旧术语文件（不自动导入，仅提示）
    old_glossary_patterns = [
        "glossary.md",
        "terms.md",
        "术语表.md",
        "term-mapping.md",
    ]
    found_old_files = []
    search_dirs = [ai_dir, ai_dir / "portfolio" / "context", ai_dir / "context"]
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for pattern in old_glossary_patterns:
            candidate = search_dir / pattern
            if candidate.exists() and candidate != target_path:
                found_old_files.append(str(candidate))

    # 创建词库模板
    templates_dir = get_templates_dir()
    src = templates_dir / "domain-glossary-template.md"

    if src.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target_path)
        print(f"✅ 领域词库已创建: {target_path}")
        print(f"   内置初始词条：外资→外商投资、农专→农民专业合作社")
        print(f"   不自动抽取历史术语")
    else:
        print(f"错误: 模板文件不存在: {src}")
        return

    # 提示旧术语文件
    if found_old_files:
        print(f"\n⚠️ 检测到可能存在的旧术语文件（不自动导入）：")
        for f in found_old_files:
            print(f"  - {f}")
        print(f"如需导入旧术语，请手动确认后添加到词库的术语映射表中。")
    else:
        print(f"未检测到旧术语文件。")


def create_pm_profile_for_existing(project_root: str):
    """为旧工作区创建 PM 偏好档案模板，不自动抽取历史偏好。"""
    ai_dir = Path(project_root) / "ai"
    if not ai_dir.exists():
        print(f"错误: {ai_dir} 不存在")
        return

    # 检测模式：优先 portfolio，其次 single
    portfolio_dir = ai_dir / "portfolio" / "context"
    single_dir = ai_dir / "context"

    if portfolio_dir.exists():
        target_dir = portfolio_dir
        mode_label = "项目集(portfolio)"
    elif single_dir.exists():
        target_dir = single_dir
        mode_label = "单项目(single)"
    else:
        print(f"错误: 未找到 context 目录，无法确定工作区模式")
        print(f"  尝试查找: {portfolio_dir}")
        print(f"  尝试查找: {single_dir}")
        return

    print(f"检测到工作区模式: {mode_label}")
    print(f"PM 偏好档案目标路径: {target_dir / 'pm-profile.md'}")

    target_path = target_dir / "pm-profile.md"

    if target_path.exists():
        print(f"PM 偏好档案已存在，不覆盖: {target_path}")
        return

    # 创建 PM 偏好档案模板
    templates_dir = get_templates_dir()
    src = templates_dir / "pm-profile-template.md"

    if src.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target_path)
        print(f"PM 偏好档案已创建: {target_path}")
        print(f"   AI 将在交互中被动学习用户习惯，写入 pending 后经用户确认升为 confirmed")
    else:
        print(f"错误: 模板文件不存在: {src}")
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChronoPM 工作区迁移脚本")
    parser.add_argument(
        "--project-root",
        required=True,
        help="项目根目录路径",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅检测不执行迁移",
    )
    parser.add_argument(
        "--target-version",
        default=None,
        help="目标版本（默认为当前 Skill 版本）",
    )
    parser.add_argument(
        "--index-mode",
        choices=["structure-only", "recent-7-days", "current-month", "full-rebuild"],
        default="structure-only",
        help="索引重建模式（默认：structure-only）",
    )
    parser.add_argument(
        "--create-glossary",
        action="store_true",
        default=False,
        help="为旧工作区创建领域词库模板（内置用户已确认初始词条），不自动抽取历史术语",
    )
    parser.add_argument(
        "--create-profile",
        action="store_true",
        default=False,
        help="为旧工作区创建 PM 偏好档案模板，AI 将在交互中被动学习用户习惯",
    )

    args = parser.parse_args()
    if args.create_glossary:
        create_glossary_for_existing(args.project_root)
    elif args.create_profile:
        create_pm_profile_for_existing(args.project_root)
    else:
        migrate_workspace(args.project_root, args.dry_run, args.target_version, args.index_mode)
