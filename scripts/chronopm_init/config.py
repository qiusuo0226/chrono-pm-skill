#!/usr/bin/env python3
"""ChronoPM 工作区初始化配置常量。

本模块集中维护版本常量与目录结构配置。目录结构中的当年当月目录
（如 meetings/202608）在 CR-20260810-001 中由硬编码改为按运行当天
动态生成，替换方式与脚本内既有 datetime.now().strftime 用法一致。
"""

import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# 版本常量（单一版本源：scripts/_version.py）
# ============================================================
# 从 scripts/_version.py 导入，避免在包内硬编码版本字符串造成失步。
# 向上定位 scripts/ 目录后按模块名导入，逻辑与 template_renderer 的目录定位一致。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _version import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION  # noqa: E402

# 当前年月（用于当年当月目录，替代原硬编码 202608）
CURRENT_YM = datetime.now().strftime("%Y%m")

# ============================================================
# 单项目模式目录结构
# ============================================================
SINGLE_PROJECT_DIRS = [
    "context",
    # v2.1.0：continuity/ 合并入 context/（D-9），不再单独建目录
    "requirements",
    "requirements/canonical",
    "requirements/atoms",
    "plans",
    "todos",
    f"meetings/{CURRENT_YM}",
    f"reports/daily/project/{CURRENT_YM}",
    "reports/weekly",
    "reports/monthly",
    "risks",
    "issues",
    "decisions",
    f"reviews/{CURRENT_YM}",
    "templates",
    "logs",
    "prompts",
    # v2.1.0：outputs/ 移入 ai/ 内（D-8），工作区根目录不再有 outputs/
    "outputs",
]

SINGLE_FACT_SOURCE_FILES = {
    "risks/risk-register.md": "risk-register-template.md",
    "issues/issue-register.md": "issue-register-template.md",
    "decisions/decision-log.md": "change-log-template.md",
    "plans/progress-plan.md": "project-status-template.md",
    "plans/budget.md": "project-status-template.md",
    "requirements/requirement-register.md": "requirement-register-template.md",
    "requirements/change-log.md": "change-log-template.md",
    "requirements/source-type-registry.md": "source-type-registry-template.md",
    "requirements/contract-register.md": "contract-register-template.md",
}

# ============================================================
# v3.0.0（P-14）：PORTFOLIO_DIRS / PORTFOLIO_FACT_SOURCE_FILES /
# PORTFOLIO_INDEX_TEMPLATES 集层初始化常量已删除（init 仅 single）。
# 存量 portfolio 工作区的读取/迁移结构常量见 migrate_workspace.py
# （PORTFOLIO_050_DIRS / PORTFOLIO_060_DIRS，存量兼容有意保留）。
# ============================================================

# ============================================================
# v3.0.0（P-14）：SUB_PROJECT_DIRS / SUB_PROJECT_FACT_SOURCE_FILES 项目集
# 子项目结构常量已删除（init 仅单项目；单项目结构用 SINGLE_PROJECT_DIRS /
# SINGLE_FACT_SOURCE_FILES）。存量集工作区迁移结构常量见 migrate_workspace.py
# （PORTFOLIO_050_DIRS / PORTFOLIO_060_DIRS，存量兼容有意保留）。
# ============================================================

# 项目级索引文件（v3.0.0：原 SUB_PROJECT_INDEX_TEMPLATES 改名，项目集命名退役）
SINGLE_PROJECT_INDEX_TEMPLATES = {
    "reports/daily/index.md": """---
doc_type: index
project: "{name}"
---

# 日报索引

| Date | Type | File | Owner | Summary | Task Sync | Risk Sync | Issue Sync | Weekly Sync |
|------|------|------|-------|--------|-----------|-----------|------------|-------------|
""",
    "reports/weekly/index.md": """---
doc_type: index
project: "{name}"
---

# 周报索引

| Week | Date Range | File | Status | Key Highlights |
|------|------------|------|--------|----------------|
""",
    "meetings/index.md": """---
doc_type: index
project: "{name}"
---

# 会议索引

| Date | Meeting ID | Title | Key Decisions | Action Items | File |
|------|------------|-------|---------------|--------------|------|
""",
    "reviews/index.md": """---
doc_type: index
project: "{name}"
---

# 复盘索引

| Date | Event | 关联里程碑（WP-NNN） | File | Key Lessons |
|------|--------|-----------|------|-------------|
""",
    "reports/monthly/index.md": """---
doc_type: index
project: "{name}"
---

# 月报索引

| Month | File | Status | Key Highlights |
|-------|------|--------|----------------|
""",
}

# 所有模板文件列表（复制到 ai/templates/）
# v2.0.0 待办体系重构后：board/迭代登记册/里程碑板/旧待办索引/快照/actuals/
# 个人日报/个人进度/结转/延期统计等模板已删除，新增 PLAN/待办文件/绑定文件模板。
# v2.1.0：项目日报模板已删除（按需生成，无独立模板，见 01 号规则 §2.2）。
# v3.0.0（P-13）：portfolio-weekly-template / 集级 project-index-template 迁
# ChronoPM-Portfolio 包，Project 侧不再 init 复制（模板总数 35→33）。
ALL_TEMPLATE_FILES = [
    "weekly-report-template.md",
    "meeting-template.md",
    "risk-register-template.md",
    "issue-register-template.md",
    "requirement-register-template.md",
    "change-log-template.md",
    "change-log-index-template.md",
    "change-log-archive-template.md",
    "project-status-template.md",
    "resource-register-template.md",
    "transfer-log-template.md",
    "project-context-template.md",
    "lessons-learned-template.md",
    "project-brief-template.md",
    "outputs-index-template.md",
    "output-manifest-template.md",
    "pending-changes-index-template.md",
    "plan-import-template.md",
    "project-lineage-template.md",
    "legacy-sources-template.md",
    "import-log-template.md",
    "domain-glossary-template.md",
    "pm-profile-template.md",
    "contract-register-template.md",
    "entity-registry-template.md",
    "workspace-health-template.md",
    # v2.0.0 新体系核心模板
    "plan-template.md",
    "personal-daily-todo-template.md",
    "daily-todo-binding-template.md",
    # AI 运行时格式参考副本（非 FACT_SOURCE 实例化模板）
    "decision-log-template.md",
    "project-notes-template.md",
    # 已通过 *_FACT_SOURCE_FILES 实例化，按全量副本库口径纳入
    "source-type-registry-template.md",
]
