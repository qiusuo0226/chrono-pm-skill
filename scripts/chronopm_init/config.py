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
    "continuity",
    "requirements",
    "requirements/canonical",
    "requirements/atoms",
    "plans",
    "milestones",
    "tasks",
    f"meetings/{CURRENT_YM}",
    f"reports/daily/personal/{CURRENT_YM}",
    "reports/daily/personal/summaries",
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
]

SINGLE_FACT_SOURCE_FILES = {
    "tasks/board.md": "task-board-template.md",
    "tasks/backlog.md": "task-board-template.md",
    "risks/risk-register.md": "risk-register-template.md",
    "issues/issue-register.md": "issue-register-template.md",
    "decisions/decision-log.md": "change-log-template.md",
    "milestones/milestone-board.md": "milestone-board-template.md",
    "plans/progress-plan.md": "project-status-template.md",
    "plans/budget.md": "project-status-template.md",
    "requirements/requirement-register.md": "requirement-register-template.md",
    "requirements/change-log.md": "change-log-template.md",
    "requirements/source-type-registry.md": "source-type-registry-template.md",
    "requirements/contract-register.md": "contract-register-template.md",
}

# ============================================================
# 项目集模式 - portfolio 目录结构
# ============================================================
PORTFOLIO_DIRS = [
    "context",
    "todos",
    "todos/snapshots/daily",
    "todos/snapshots/weekly",
    "todos/actuals/daily",
    "todos/actuals/weekly",
    "reports/weekly",
    "risks",
    "plans",
    "resources",
    "requirements",
    "requirements/canonical",
    "requirements/atoms",
    f"meetings/{CURRENT_YM}",
    "logs",
]

PORTFOLIO_FACT_SOURCE_FILES = {
    "context/project-index.md": "project-index-template.md",
    "context/project-context.md": "project-context-template.md",
    "risks/board.md": "risk-register-template.md",
    "plans/budget-summary.md": "project-status-template.md",
    "resources/resource-register.md": "resource-register-template.md",
    "resources/transfer-log.md": "transfer-log-template.md",
    "requirements/contract-register.md": "contract-register-template.md",
    "requirements/source-type-registry.md": "source-type-registry-template.md",
}

# 项目集级索引文件
PORTFOLIO_INDEX_TEMPLATES = {
    "reports/weekly/index.md": """---
doc_type: index
portfolio: "{name}"
---

# 项目集周报索引

| Week | Date Range | File | Status | Key Highlights |
|------|------------|------|--------|----------------|
""",
    "meetings/index.md": """---
doc_type: index
portfolio: "{name}"
---

# 项目集会议索引

| Date | Meeting ID | Title | Key Decisions | Action Items | File |
|------|------------|-------|---------------|--------------|------|
""",
}

# ============================================================
# 项目集模式 - 子项目目录结构（每个子项目）
# ============================================================
SUB_PROJECT_DIRS = [
    "context",
    "continuity",
    "requirements",
    "requirements/canonical",
    "requirements/atoms",
    "plans",
    "milestones",
    "tasks",
    f"meetings/{CURRENT_YM}",
    f"reports/daily/personal/{CURRENT_YM}",
    "reports/daily/personal/summaries",
    f"reports/daily/project/{CURRENT_YM}",
    "reports/weekly",
    "reports/monthly",
    "risks",
    "issues",
    "decisions",
    f"reviews/{CURRENT_YM}",
    "logs",
    "prompts",
]

SUB_PROJECT_FACT_SOURCE_FILES = {
    "tasks/board.md": "task-board-template.md",
    "tasks/backlog.md": "task-board-template.md",
    "risks/risk-register.md": "risk-register-template.md",
    "issues/issue-register.md": "issue-register-template.md",
    "decisions/decision-log.md": "change-log-template.md",
    "milestones/milestone-board.md": "milestone-board-template.md",
    "plans/progress-plan.md": "project-status-template.md",
    "plans/budget.md": "project-status-template.md",
    "requirements/requirement-register.md": "requirement-register-template.md",
    "requirements/change-log.md": "change-log-template.md",
    "requirements/source-type-registry.md": "source-type-registry-template.md",
}

# 子项目级索引文件
SUB_PROJECT_INDEX_TEMPLATES = {
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

| Date | Event | Milestone | File | Key Lessons |
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
ALL_TEMPLATE_FILES = [
    "personal-daily-template.md",
    "project-daily-template.md",
    "weekly-report-template.md",
    "meeting-template.md",
    "task-board-template.md",
    "risk-register-template.md",
    "issue-register-template.md",
    "milestone-board-template.md",
    "requirement-register-template.md",
    "change-log-template.md",
    "project-status-template.md",
    "portfolio-weekly-template.md",
    "resource-register-template.md",
    "transfer-log-template.md",
    "project-index-template.md",
    "project-context-template.md",
    "lessons-learned-template.md",
    "project-brief-template.md",
    "outputs-index-template.md",
    "output-manifest-template.md",
    "personal-progress-template.md",
    "carryover-register-template.md",
    "project-lineage-template.md",
    "legacy-sources-template.md",
    "import-log-template.md",
    "pm-daily-todo-template.md",
    "personal-todo-index-template.md",
    "daily-todo-index-template.md",
    "weekly-todo-index-template.md",
    "daily-todo-snapshot-template.md",
    "daily-todo-actuals-template.md",
    "weekly-todo-snapshot-template.md",
    "weekly-todo-actuals-template.md",
    "todo-history-index-template.md",
    "domain-glossary-template.md",
    "iteration-register-template.md",
    "pm-profile-template.md",
    "contract-register-template.md",
    "entity-registry-template.md",
]
