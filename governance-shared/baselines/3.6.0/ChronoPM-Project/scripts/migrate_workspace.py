#!/usr/bin/env python3
"""
ChronoPM 工作区迁移脚本

当 Skill 包升级后，已有的 ai/ 工作区可能缺少新版本所需的目录和文件。
本脚本检测差距并自动创建缺失内容。

用法:
    python migrate_workspace.py --project-root /path/to/project
    python migrate_workspace.py --project-root /path/to/project --dry-run
    python migrate_workspace.py --project-root /path/to/project --target-version 1.2.0

v3.0.0 存量兼容声明（P-14/P-30 配套）：init 侧 portfolio 分支已删除，
但本脚本内的 is_portfolio 分支与 PORTFOLIO_050_DIRS / PORTFOLIO_060_DIRS
等旧结构常量为**有意保留**——存量 portfolio 工作区（如市监重构项目管理，
用户已定界本次不迁移）日后按 upgrade-to-3.0.0.md 原地升级（D-13/D-21）时，
依赖本脚本读取旧结构并下沉/补建。删除将导致存量工作区无法迁移。
"""

import argparse
import json
import os
import re
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
from chronopm_init.config import ALL_TEMPLATE_FILES
from chronopm_init.file_registry import create_outputs_dir

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

# Schema 0.6.0 新增的 change-log 分层归档目录（single 模式在 ai/ 下）
SCHEMA_060_DIRS = [
    "change-log/archive",
]

# Schema 0.6.0 项目集模式新增目录（portfolio 模式下，change-log 在 portfolio 层）
PORTFOLIO_060_DIRS = [
    "change-log/archive",
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
        "version": "0.2.0",
        "schema": "0.1.0",
        "capabilities": ["template_rewrite"],
        "new_dirs": [],
        "new_files": [],
        "note": "v0.2.0 根据实际云文档结构重写 8 个模板，新增 lessons-learned 与 project-context 模板；无目录结构变更。",
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
        # v2.1.0（D-8）：outputs/ 已移入 ai/ 内，由 2.1.0 条目 new_dirs 承载；
        # 原 external_dirs: ["outputs"]（工作区根目录）不再检测，避免误建根级旧路径。
    },
    {
        "version": "0.6.0",
        "schema": "0.3.0",
        "capabilities": ["excel_generation"],
        "new_dirs": [],
        "new_files": [],
        "note": "v0.6.0 Excel 生成规范（12 号规则）；无工作区结构变更。",
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
        "version": "0.7.1",
        "schema": "0.3.0",
        "capabilities": ["daily_merge_idempotency"],
        "new_dirs": [],
        "new_files": [],
        "note": "v0.7.1 日报合并幂等性约束（同人同日多提交合并追加不覆盖）；规则层变更，无工作区结构变更。",
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
        "version": "1.0.1",
        "schema": "0.4.0",
        "capabilities": ["pm_todo_output_spec"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.0.1 PM 待办查询输出规范（全景视图，禁止只列 PM 个人任务）；规则层变更，无工作区结构变更。",
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
        "version": "1.3.0",
        "schema": "0.4.0",
        "capabilities": ["workspace_upgrade_awareness"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.3.0 工作区升级感知（20 号规则：健康检查+功能触发检查+兼容模式+迁移模式）；.workspace-health.md 等由运行时按需生成，不预建。",
    },
    {
        "version": "1.3.1",
        "schema": "0.4.0",
        "capabilities": ["upgrade_review_constraint"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.3.1 升级方案审查约束（16 号规则 AP 审查文档）；治理层变更，无工作区结构变更。",
    },
    {
        "version": "1.4.0",
        "schema": "0.4.0",
        "capabilities": ["blueprint_external_review"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.4.0 SKILL_BLUEPRINT 架构蓝图 + 发布检查清单；仅 Skill 包层，无工作区结构变更。",
    },
    {
        "version": "1.5.0",
        "schema": "0.5.0",
        "capabilities": ["qoder_entry"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.5.0 QODER_RULES 轻量入口 + 最小读取原则；规则层变更，无工作区结构变更。",
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
        "version": "1.6.1",
        "schema": "0.5.0",
        "capabilities": ["resource_source_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.6.1 资源事实源一致性修复（05 号 §5.4a、01 号、09 号 §5.6 等规则修正）；规则层修复，无工作区结构变更。",
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
        "version": "1.7.1",
        "schema": "0.5.0",
        "capabilities": ["script_refactor"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.7.1 init_workspace.py 拆分为 chronopm_init 包（config/file_registry/template_renderer/workspace_builder/validators）；Skill 包层重构，无工作区结构变更。",
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
        "version": "1.8.1",
        "schema": "0.5.0",
        "capabilities": ["rule_slimming_06"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.8.1 06 号文件规则瘦身（587→299 行），§0 外移为 20 号规则（工作区版本规则）；规则层瘦身，无工作区结构变更。",
    },
    {
        "version": "1.8.2",
        "schema": "0.5.0",
        "capabilities": ["rule_slimming_01"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.8.2 01 号日报规则瘦身（594→221 行）；规则层瘦身，无工作区结构变更。",
    },
    {
        "version": "1.8.3",
        "schema": "0.5.0",
        "capabilities": ["rule_tabular"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.8.3 05/11/07 号规则表格化重构；规则层重构，无工作区结构变更。",
    },
    {
        "version": "1.8.4",
        "schema": "0.5.0",
        "capabilities": ["upgrade_route_closeout"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.8.4 升级路线收尾与全量回归验证；治理层变更，无工作区结构变更。",
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
    {
        "version": "1.10.2",
        "schema": "0.5.0",
        "capabilities": ["single_version_source"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.10.2 建立 scripts/_version.py 单一版本源，sync_version.py 同步全部版本触点；Skill 包层治理，无工作区结构变更。",
    },
    {
        "version": "1.11.0",
        "schema": "0.6.0",
        "capabilities": ["proactive_change", "pending_index", "change_log_archive"],
        "new_dirs": ["change-log/archive"],
        "portfolio_dirs": ["change-log/archive"],
        "new_files": [
            "pending-changes.md",
            "change-log/index.md",
            "portfolio/pending-changes.md",
            "portfolio/change-log/index.md",
        ],
        "note": "v1.11.0 主动变更+人工确认（CR-20260811-002）：pending-changes.md 为 Change Log '待确认' 条目的子集视图索引（single 在 ai/pending-changes.md，portfolio 在 ai/portfolio/pending-changes.md）；change-log 分层归档（活跃区 50 行/30 天 → change-log/archive/YYYYMM-change-log.md + change-log/index.md 导航）。",
    },
    {
        "version": "1.12.0",
        "schema": "0.6.0",
        "capabilities": ["workspace_cleanliness"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.12.0 工作空间清洁度治理（CR-20260811-003）：新增§18根目录白名单、§19交付物类型控制、§20引用完整性约束；§2流程10步→12步；release-checklist新增清洁度检查组；修复F-01~F-11历史污染；回归新增CL-001~CL-004。无工作区结构变更。",
    },
    {
        "version": "1.13.0",
        "schema": "0.6.0",
        "capabilities": ["architecture_slimming"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.13.0 架构精简（级联嵌入 + 归档表 + sync_version.py）；新增 decision-log-template 为 Skill 包模板，无工作区预建文件。",
    },
    {
        "version": "1.13.1",
        "schema": "0.6.0",
        "capabilities": ["version_history_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.13.1 skill.json versionHistory 排序修复并同步 updated_at；治理层修复，无工作区结构变更。",
    },
    {
        "version": "1.14.0",
        "schema": "0.6.0",
        "capabilities": ["standard_workflows"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.14.0 定义 WF-1~WF-6 标准工作流及其数据路径；规则层定义，复用既有目录，无工作区结构变更。",
    },
    {
        "version": "1.15.0",
        "schema": "0.7.0",
        "capabilities": ["requirement_intelligence", "project_notes"],
        "new_dirs": [
            "requirements/canonical",
            "requirements/atoms",
        ],
        "new_files": [
            "requirements/source-type-registry.md",
            "requirements/canonical/canonical-index.md",
            "requirements/atoms/atom-index.md",
            "requirements/atoms/contractual-index.md",
            "requirements/atoms/contractual.md",
            "requirements/atoms/procurement-index.md",
            "requirements/atoms/procurement.md",
            "requirements/atoms/approval-index.md",
            "requirements/atoms/approval.md",
            "requirements/atoms/compliance-index.md",
            "requirements/atoms/compliance.md",
            "requirements/atoms/technical-index.md",
            "requirements/atoms/technical.md",
            "requirements/atoms/operational-index.md",
            "requirements/atoms/operational.md",
        ],
        "note": "v1.15.0 跨源需求归集 RI（CR-20260813-001，schema 0.6.0→0.7.0）：在单一项目工作区 ai/requirements/ 下新增 canonical/ 与 atoms/（L1 主索引 atom-index + 6 类 L2 倒排索引 + 6 类 L3 全文 + source-type-registry.md）。project-notes 为 context 下追加式文件（项目集模式在 ai/portfolio/context/），新增目录由 0.7.0 初始化脚本创建。",
    },
    {
        "version": "1.16.0",
        "schema": "0.8.0",
        "capabilities": ["contract_scope_ri"],
        "new_dirs": [
            "portfolio/requirements/canonical",
            "portfolio/requirements/atoms",
        ],
        "new_files": [
            "portfolio/requirements/contract-register.md",
            "portfolio/requirements/source-type-registry.md",
            "requirements/contract-register.md",
            "portfolio/requirements/canonical/canonical-index.md",
            "portfolio/requirements/atoms/atom-index.md",
            "portfolio/requirements/atoms/contractual-index.md",
            "portfolio/requirements/atoms/contractual.md",
            "portfolio/requirements/atoms/procurement-index.md",
            "portfolio/requirements/atoms/procurement.md",
            "portfolio/requirements/atoms/approval-index.md",
            "portfolio/requirements/atoms/approval.md",
            "portfolio/requirements/atoms/compliance-index.md",
            "portfolio/requirements/atoms/compliance.md",
            "portfolio/requirements/atoms/technical-index.md",
            "portfolio/requirements/atoms/technical.md",
            "portfolio/requirements/atoms/operational-index.md",
            "portfolio/requirements/atoms/operational.md",
        ],
        "sub_project_dirs": [
            "requirements/canonical",
            "requirements/atoms",
        ],
        "sub_project_files": [
            "requirements/source-type-registry.md",
        ],
        "note": "v1.16.0 合同作用域（CR-20260813-002，schema 0.7.0→0.8.0）：项目集模式在 portfolio/requirements/ 新增 canonical/、atoms/、contract-register.md、source-type-registry.md（合同登记册为 RI 检索入口）；单项目模式在 ai/requirements/ 新增 contract-register.md。子项目级 on portfolio 模式补齐 RI 目录（requirements/canonical、requirements/atoms）与 source-type-registry.md（修复 CR-20260813-001 遗留缺口），仅对已含 requirements/ 的子项目执行（D10 守卫）。",
    },
    {
        "version": "1.16.1",
        "schema": "0.8.0",
        "capabilities": ["pack_standardization"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.16.1 打包标准化（tools/pack-skill）；Skill 包层变更，无工作区结构变更。",
    },
    {
        "version": "1.16.2",
        "schema": "0.8.0",
        "capabilities": ["ghost_reference_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.16.2 幽灵引用修复；规则层修复，无工作区结构变更。",
    },
    {
        "version": "1.16.3",
        "schema": "0.8.0",
        "capabilities": ["cascade_enforcement_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.16.3 级联强制执行规则修复；规则层修复，无工作区结构变更。",
    },
    {
        "version": "1.17.0",
        "schema": "0.8.0",
        "capabilities": ["pm_preference_generalization"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.17.0 PM 偏好通用化（01 号 §6/§7 等）；规则层变更，无工作区结构变更（pm-profile.md 已于 v1.9.0 建立）。",
    },
    {
        "version": "1.17.1",
        "schema": "0.8.0",
        "capabilities": ["governance_consistency_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.17.1 治理一致性修复；治理层修复，无工作区结构变更。",
    },
    {
        "version": "1.18.0",
        "schema": "0.8.0",
        "capabilities": ["derived_baseline"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.18.0 推导基线（00 号 §10）；规则层变更，无工作区结构变更。",
    },
    {
        "version": "1.18.1",
        "schema": "0.8.0",
        "capabilities": ["pack_naming"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.18.1 pack.py 命名标准化；Skill 包层变更，无工作区结构变更。",
    },
    {
        "version": "1.19.0",
        "schema": "0.8.0",
        "capabilities": ["wf7_wf8"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.19.0 WF-7 倒排计划编排 + WF-8 待办归属；规则层变更，复用 todos/ 体系，无工作区结构变更。",
    },
    {
        "version": "1.19.1",
        "schema": "0.8.0",
        "capabilities": ["migrate_template_sync_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.19.1 修复 migrate_workspace.py 模板同步缺口；脚本层修复，无工作区结构变更。",
    },
    {
        "version": "1.20.0",
        "schema": "0.8.0",
        "capabilities": ["requirement_dual_view"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.20.0 需求双视图（requirement-register 23→25 列）；模板列扩展，无工作区结构变更，无文件迁移。",
    },
    {
        "version": "1.21.0",
        "schema": "0.8.0",
        "capabilities": ["reverse_daily_matrix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v1.21.0 倒排每日矩阵；零新增文件，无工作区结构变更。",
    },
    {
        "version": "2.0.0",
        "schema": "0.8.0",
        "capabilities": ["todo_workspace_v2"],
        "new_dirs": ["todos"],
        "new_files": [],
        "sub_project_dirs": ["todos"],
        "note": "v2.0.0 待办查询体系重构（schema 保持 0.8.0）：执行状态唯一事实源切换到 todos/{date}/{owner}.md 每人每日待办文件 + todos/{date}/_index.md 绑定文件；PLAN 计划文件替代迭代登记册（AI 按需创建，不预建）；board/backlog/里程碑板/旧待办索引/快照/actuals/个人日报等旧体系文件不再创建，存量旧文件按升级方案归档保留只读；子项目级 on portfolio 模式补齐 todos/ 目录（D10 守卫）。",
    },
    {
        "version": "2.1.0",
        "schema": "0.8.0",
        "capabilities": ["workspace_path_consolidation", "report_migration", "personal_todo_rules"],
        "new_dirs": ["outputs"],
        "new_files": [],
        "note": "v2.1.0（schema 保持 0.8.0）：路径整合 continuity/*→context/（4 文件含 carryover-register，D-9）、工作区根 outputs/→ai/outputs/（D-8），由 migrate_v210_paths() 执行搬移（不覆盖合并）；旧报告结构迁移按 §7.3.2b 由 migrate_v210_reports() 执行（检测→迁移→验证→删除，空源登记跳过）；新增 22 号个人待办规则（规则层，无预建文件）。",
    },
    {
        "version": "3.0.0",
        "schema": "0.9.0",
        "capabilities": ["federal_mount", "single_project_only", "energy_ledger"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.0.0：Skill 双包；工作区 schema 0.9.0 联邦挂载。脚本默认只更新 .skill-version.json 元数据（skillName=chrono-pm-project）。结构下沉/补建见 upgrade-to-3.0.0.md 节 B，不自动拆业务工作区。",
    },
    {
        "version": "3.1.0",
        "schema": "0.9.0",
        "capabilities": ["daily_report_routing", "monthly_residual_cleanup"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.1.0（schema 保持 0.9.0）：路径残留纠偏 + 日报查询/更新路由补全 + 月报残留清理。无结构变更，存量工作区零迁移，重装载规则即生效。",
    },
    {
        "version": "3.1.1",
        "schema": "0.9.0",
        "capabilities": ["dev_repo_layout"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.1.1（schema 保持 0.9.0）：开发仓三目录重组（ChronoPM-Project/ + ChronoPM-Portfolio/ + governance-shared/）。业务工作区零迁移。",
    },
    {
        "version": "3.2.0",
        "schema": "0.9.0",
        "capabilities": ["df017_provenance", "load_scene_tags", "df018_habit_detect"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.2.0（schema 保持 0.9.0）：DF-017/018 + 加载场景分类。存量 pm-profile 零强制迁移。",
    },
    {
        "version": "3.3.0",
        "schema": "0.9.0",
        "capabilities": ["linked_todos", "worklog_td_ref", "td_abbrev_registry"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.3.0（schema 保持 0.9.0）：关联待办 + 工作日志 TD Ref + 缩写治理小表。存量零强制迁移。",
    },
    {
        "version": "3.4.0",
        "schema": "0.9.0",
        "capabilities": ["report_stub", "timeline_report"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.4.0（schema 保持 0.9.0）：报告存根范式 + 时间线报懒建。不预建 timeline/。",
    },
    {
        "version": "3.5.0",
        "schema": "0.10.0",
        "capabilities": ["wp_independent_files", "wp_index_accelerator", "wp_bind_detect"],
        "new_dirs": ["wps"],
        "new_files": ["wps/_index.md"],
        "note": "v3.5.0（schema 0.9.0→0.10.0）：wps/ 独立 WP 文件 + _index.md 查找加速器。脚本只建空目录和索引；计划内嵌 WP 一次性抽取由 AI 输出清单→PM 确认→先迁后验，脚本不自动删内嵌表。编号短号不变。",
    },
    {
        "version": "3.5.1",
        "schema": "0.10.0",
        "capabilities": ["residual_path_fix"],
        "new_dirs": [],
        "new_files": [],
        "note": "v3.5.1（schema 保持 0.10.0）：project-brief §4 / 14 号月度索引停维等措辞残留修复。零迁移。",
    },
    {
        "version": "3.6.0",
        "schema": "0.11.0",
        "capabilities": ["source_doc_dirs", "source_index_accelerator", "atom_kind_ext"],
        "new_dirs": ["requirements/sources"],
        "new_files": ["requirements/sources/_index.md"],
        "note": "v3.6.0（schema 0.10.0→0.11.0）：requirements/sources/{编号}/ 文档级拆解。脚本只建空目录和索引；存量 {type}-source/ 一次性迁移由 AI 输出清单→PM 确认→先迁后验，脚本不自动删旧目录。",
    },
]

# v2.1.0 已将 VERSION_CAPABILITIES 补齐至全部 50 个历史版本（0.1.0 ~ 2.1.0），
# 任意工作区版本均可被 get_capabilities_since() 精确匹配，不再存在 from_version
# 无法命中导致返回空的结构性缺漏（原缺漏 29 个版本已按 skill.json versionHistory
# 与 CHANGELOG 回填，见升级方案 v2.1 §7.3.1）。



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


def _sub_projects(ai_dir: Path):
    """遍历项目集模式下 ai/projects/*/，仅返回含 requirements/ 的子项目（D10 守卫，CR-20260813-002）。"""
    projects_dir = ai_dir / "projects"
    if not projects_dir.exists():
        return []
    return [
        d for d in projects_dir.iterdir()
        if d.is_dir() and (d / "requirements").is_dir()
    ]


def check_missing_dirs(ai_dir: Path, capabilities: list, is_portfolio: bool = False):
    """检查缺失的目录"""
    missing = []
    for cap in capabilities:
        dirs = cap.get("new_dirs", [])
        for d in dirs:
            full_path = ai_dir / d
            if not full_path.exists():
                missing.append(d)

        # 0.6.0 portfolio 模式 change-log 归档目录位于 portfolio 层
        p_dirs = cap.get("portfolio_dirs", [])
        if is_portfolio:
            for d in p_dirs:
                fp = (ai_dir / "portfolio" / d)
                if not fp.exists():
                    missing.append(f"portfolio/{d}")

        # 0.8.0 子项目级 RI 目录（遍历 projects/*/，含 guard D10）
        sub_dirs = cap.get("sub_project_dirs", [])
        if is_portfolio:
            for sub in _sub_projects(ai_dir):
                for d in sub_dirs:
                    fp = sub / d
                    if not fp.exists():
                        missing.append(f"projects/{sub.name}/{d}")

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
            # 0.6.0 pending/change-log 索引按工作区模式过滤
            if f == "portfolio/pending-changes.md" and not is_portfolio:
                continue
            if f == "pending-changes.md" and is_portfolio:
                continue
            if f == "portfolio/change-log/index.md" and not is_portfolio:
                continue
            if f == "change-log/index.md" and is_portfolio:
                continue
            full_path = ai_dir / f
            if not full_path.exists():
                missing.append(f)

        # 0.8.0 子项目级 RI 文件（遍历 projects/*/，仅 source-type-registry 需要模板，D10 守卫）
        sub_files = cap.get("sub_project_files", [])
        if is_portfolio:
            for sub in _sub_projects(ai_dir):
                for rel in sub_files:
                    fp = sub / rel
                    if not fp.exists():
                        missing.append(f"projects/{sub.name}/{rel}")
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
        # v2.0.0 零数据源：人员资源事实源下放子项目（projects/{子项目}/resources/），
        # portfolio 级 resource-register/transfer-log 不再预建模板；存量旧文件保留只读，
        # 数据迁移由 AI/PM 按 09 号 §5 完成，项目集层只维护 shared-resource-index/transfer-index 索引。
        "context/project-brief.md": "project-brief-template.md",
        "portfolio/context/project-brief.md": "project-brief-template.md",
        "continuity/project-lineage.md": "project-lineage-template.md",
        "continuity/legacy-sources.md": "legacy-sources-template.md",
        # v2.0.0：carryover-register / todo-history-index 模板已删除（结转字段化、历史索引砍掉），
        # 旧版本迁移条目若命中将走 auto-migrated 空文件兜底，不影响迁移流程。
        "continuity/import-log.md": "import-log-template.md",
        "portfolio/context/domain-glossary.md": "domain-glossary-template.md",
        "context/domain-glossary.md": "domain-glossary-template.md",
        "requirements/source-type-registry.md": "source-type-registry-template.md",
        "portfolio/requirements/contract-register.md": "contract-register-template.md",
        "portfolio/requirements/source-type-registry.md": "source-type-registry-template.md",
        "context/entity-registry.md": "entity-registry-template.md",
        "portfolio/context/entity-registry.md": "entity-registry-template.md",
        "wps/_index.md": "wp-index-template.md",
        "requirements/sources/_index.md": "source-index-template.md",
    }

    for f in files:
        target = ai_dir / f
        if target.exists():
            continue

        # H1：子项目文件路径剥前缀后查 template_map（CR-20260813-002）
        #   projects/{sub}/requirements/source-type-registry.md → requirements/source-type-registry.md
        template_key = f
        m = re.match(r"^projects/[^/]+/(.+)$", f)
        if m:
            template_key = m.group(1)

        template_name = template_map.get(template_key)
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
        # v2.0.0：旧体系探针（tasks/board.md、旧待办索引、快照目录、carryover-register）已删除，
        # 改为新体系探针（todos/ 目录 + ai/outputs/，v2.1.0 起 outputs 位于 ai/ 内）
        ("todo_workspace_v2", cap_status(["todos"])),
        ("output_artifact", "ok" if (ai_dir / "outputs").exists() else "missing"),
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

> v2.0.0 起旧待办索引（personal-todo-index/history-index）已删除，
> 待办事实源为 todos/{{YYYY-MM-DD}}/{{执行人}}.md，绑定文件为 todos/{{YYYY-MM-DD}}/_index.md。

## 推荐动作
"""
    if is_healthy:
        content += "1. 工作区版本已匹配，无需迁移\n"
    else:
        content += f"1. 执行迁移：python scripts/migrate_workspace.py --project-root .\n"
        content += "2. 检查新增文件并填写内容\n"
        content += "3. 可选：对 AI 说“初始化今天的待办”创建当日待办文件与绑定文件\n"

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
    """索引重建占位（v2.0.0 起已废弃）。

    旧实现会创建 portfolio/todos/personal-todo-index.md 等旧体系索引文件，
    这些文件在 v2.0.0 待办体系重构中已全部删除；待办事实源改为
    todos/{date}/{owner}.md，绑定文件 _index.md 由 AI 按日按需创建，
    无需脚本预建。此函数保留仅为兼容 --index-mode 参数，不再创建任何文件。
    """
    print(f"  ℹ️ v2.0.0 起待办索引由 AI 按需创建，脚本不再预建旧索引文件")


def _vcmp(a: str, b: str) -> int:
    """比较版本号（仅数字段），返回 -1/0/1；无法解析时返回 0。"""
    try:
        pa = [int(x) for x in a.split(".")]
        pb = [int(x) for x in b.split(".")]
    except (ValueError, AttributeError):
        return 0
    return (pa > pb) - (pa < pb)


def _extract_date(path: Path):
    """从文件名提取 YYYY-MM-DD；回退文件名 MMDD/YYYYMMDD 段；再回退父目录名（旧 YYYY/MM 结构）。"""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.stem)
    if m:
        return m.group(1)
    # 文件名中的 YYYYMMDD 段
    m = re.search(r"(?<!\d)(\d{4})(\d{2})(\d{2})(?!\d)", path.stem)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    # 文件名中的 MMDD 段（如 daily-0105.md，年份取目录层级）
    year = None
    for part in path.parts[::-1]:
        if re.fullmatch(r"\d{4}", part):
            year = part
            break
    m = re.search(r"(?<!\d)(\d{2})(\d{2})(?!\d)", path.stem)
    if m and year and 1 <= int(m.group(1)) <= 12 and 1 <= int(m.group(2)) <= 31:
        return f"{year}-{m.group(1)}-{m.group(2)}"
    # 回退：YYYY/MM 两级目录，日期取当月首日（仅无法解析时的兜底）
    if re.fullmatch(r"\d{4}", path.parent.parent.name) and re.fullmatch(r"\d{1,2}", path.parent.name):
        return f"{path.parent.parent.name}-{int(path.parent.name):02d}-01"
    return None


def _scope_project_name(scope_dir: Path) -> str:
    """读取作用域内 context/project-brief.md frontmatter 项目名；回退目录名。"""
    brief = scope_dir / "context" / "project-brief.md"
    if brief.exists():
        try:
            for line in brief.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                for key in ("project:", "portfolio:"):
                    if stripped.startswith(key):
                        name = stripped[len(key):].strip().strip('"')
                        if name:
                            return name
        except OSError:
            pass
    return scope_dir.name


def _append_import_log(log_path: Path, rows: list):
    """向 import-log.md 追加迁移登记记录（文件不存在时先建表头）。"""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text(
            "---\ndoc_type: import-log\n---\n\n# 导入/迁移日志\n\n"
            "| Date | Type | Source | Target | Verify | Result |\n"
            "|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    today = datetime.now().strftime("%Y-%m-%d")
    with open(log_path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(f"| {today} | {r['type']} | {r['source']} | {r['target']} | {r['verify']} | {r['result']} |\n")


def _remove_empty_subdirs(root: Path):
    """自底向上删除 root 下的空子目录（保留 root 本身，v2 活跃路径）。"""
    if not root.exists():
        return
    for d in sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda x: len(x.parts), reverse=True):
        try:
            d.rmdir()
        except OSError:
            pass


def migrate_v210_paths(ai_dir: Path, dry_run: bool = False) -> list:
    """v2.1.0 路径整合（方案 §7.1，D-8/D-9）：
    1. continuity/*.md → context/*.md（搬移，同名已存在则保留源文件并提示人工处理）
    2. 工作区根 outputs/* → ai/outputs/*（同上）
    不覆盖合并；搬空后删除空目录。
    """
    actions = []

    # --- continuity/ → context/ ---
    cont_dir = ai_dir / "continuity"
    ctx_dir = ai_dir / "context"
    if cont_dir.exists():
        files = [f for f in cont_dir.iterdir() if f.is_file()]
        if not files:
            actions.append("continuity/ 为空目录，无数据，跳过")
            if not dry_run:
                try:
                    cont_dir.rmdir()
                except OSError:
                    pass
        for f in files:
            dst = ctx_dir / f.name
            if dst.exists():
                actions.append(f"⚠️ context/{f.name} 已存在，continuity/{f.name} 保留原位，需人工合并")
                continue
            if dry_run:
                actions.append(f"[dry-run] continuity/{f.name} → context/{f.name}")
            else:
                ctx_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dst))
                actions.append(f"✓ continuity/{f.name} → context/{f.name}")
        if not dry_run and cont_dir.exists() and not any(cont_dir.iterdir()):
            try:
                cont_dir.rmdir()
                actions.append("✓ continuity/ 空目录已删除")
            except OSError:
                pass

    # --- 工作区根 outputs/ → ai/outputs/ ---
    root_outputs = ai_dir.parent / "outputs"
    ai_outputs = ai_dir / "outputs"
    if root_outputs.exists():
        items = list(root_outputs.iterdir())
        if not items:
            actions.append("工作区根 outputs/ 为空目录，无数据，跳过")
            if not dry_run:
                try:
                    root_outputs.rmdir()
                except OSError:
                    pass
        for item in items:
            dst = ai_outputs / item.name
            if dst.exists():
                actions.append(f"⚠️ ai/outputs/{item.name} 已存在，根级 outputs/{item.name} 保留原位，需人工合并")
                continue
            if dry_run:
                actions.append(f"[dry-run] outputs/{item.name} → ai/outputs/{item.name}")
            else:
                ai_outputs.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dst))
                actions.append(f"✓ outputs/{item.name} → ai/outputs/{item.name}")
        if not dry_run and root_outputs.exists() and not any(root_outputs.iterdir()):
            try:
                root_outputs.rmdir()
                actions.append("✓ 根级 outputs/ 空目录已删除")
            except OSError:
                pass

    return actions


def migrate_v210_reports(ai_dir: Path, dry_run: bool = False, is_portfolio: bool = False) -> list:
    """v2.1.0 历史报告数据迁移（方案 §7.3.2b，需求十二）。

    严格执行“检测 → 迁移 → 验证 → 删除”：
    - 个人日报：内容级迁移，由 AI 按 §7.3.2b 执行（合并进 todos/{date}/{owner}.md §3 工作日志段）；
      脚本只负责检测与提示，不搬移、不删除源文件（验证通过前禁止删除，数据安全）；
    - 项目日报：文件级规范化迁移 → reports/daily/project/YYYYMM/；
    - 周报：文件级规范化迁移 → reports/weekly/YYYY/YYYY-Wxx.md；
    空源登记“无数据，跳过”，不阻断其余迁移项；验证结果登记 context/import-log.md；
    报告不进 archive；验证通过后才清理旧结构（不留任何历史缓存）。
    """
    if is_portfolio:
        projects_dir = ai_dir / "projects"
        scopes = sorted([d for d in projects_dir.iterdir() if d.is_dir()]) if projects_dir.exists() else []
    else:
        scopes = [ai_dir]

    actions = []
    for scope in scopes:
        prefix = "ai/" if scope == ai_dir else f"projects/{scope.name}/"
        import_log = scope / "context" / "import-log.md"
        proj_name = _scope_project_name(scope)
        rows = []

        personal_dir = scope / "reports" / "daily" / "personal"
        daily_dir = scope / "reports" / "daily" / "project"
        weekly_dir = scope / "reports" / "weekly"

        personal_files = [p for p in personal_dir.rglob("*") if p.is_file()] if personal_dir.exists() else []
        daily_files = [p for p in daily_dir.rglob("*") if p.is_file()] if daily_dir.exists() else []
        weekly_files = [p for p in weekly_dir.rglob("*") if p.is_file()] if weekly_dir.exists() else []

        # --- 1. 个人日报：内容级迁移（AI 执行，脚本仅检测登记） ---
        if not personal_files:
            actions.append(f"  [{prefix}] 个人日报：源为空（无数据，跳过）")
            rows.append({"type": "个人日报内容迁移", "source": f"{prefix}reports/daily/personal/",
                         "target": f"{prefix}todos/{{date}}/{{owner}}.md §3", "verify": "-", "result": "无数据，跳过"})
        else:
            actions.append(f"  [{prefix}] ⚠️ 检测到个人日报 {len(personal_files)} 个：内容级迁移需 AI 按 §7.3.2b 执行")
            for p in personal_files[:5]:
                actions.append(f"      - {p.relative_to(ai_dir)}")
            if len(personal_files) > 5:
                actions.append(f"      - …其余 {len(personal_files) - 5} 个（清单见 governance/migrations/upgrade-to-2.1.0.md）")
            actions.append("      AI 完成内容迁移并验证（日期×人员覆盖核对）后删除源文件；脚本不搬移、不删除个人日报源")

        # --- 2. 项目日报：文件级规范化迁移 ---
        if not daily_files:
            actions.append(f"  [{prefix}] 项目日报：源为空（无数据，跳过）")
            rows.append({"type": "项目日报文件迁移", "source": f"{prefix}reports/daily/project/",
                         "target": f"{prefix}reports/daily/project/YYYYMM/", "verify": "-", "result": "无数据，跳过"})
        else:
            moved, conflicts = 0, []
            for src in daily_files:
                date = _extract_date(src)
                if date:
                    ym = date[:7].replace("-", "")
                    name = src.name if re.match(r"^\d{4}-\d{2}-\d{2}-", src.name) else f"{date}-{proj_name}-项目日报{src.suffix}"
                else:
                    ym, name = "unknown", src.name
                    actions.append(f"      ⚠️ 无法解析日期，保留原名: {src.relative_to(ai_dir)}")
                dst = daily_dir / ym / name
                if src == dst:
                    moved += 1  # 已是 v2 标准结构与命名，计为已迁移
                    continue
                if dst.exists():
                    conflicts.append(src)
                    continue
                if not dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                moved += 1
            ok = moved == len(daily_files) and not conflicts
            verify_msg = f"文件数核对 {moved}/{len(daily_files)}"
            if conflicts:
                verify_msg += f"，冲突 {len(conflicts)} 个"
                for c in conflicts:
                    actions.append(f"      ⚠️ 冲突（目标已存在）: {c.relative_to(ai_dir)}")
            rows.append({"type": "项目日报文件迁移", "source": f"{prefix}reports/daily/project/（{len(daily_files)} 个）",
                         "target": f"{prefix}reports/daily/project/YYYYMM/", "verify": verify_msg,
                         "result": "成功" if ok else "验证失败（保留旧结构，人工介入）"})
            actions.append(f"  [{prefix}] 项目日报：迁移 {moved}/{len(daily_files)}，验证{'通过' if ok else '失败（保留旧结构，人工介入）'}")
            if ok and not dry_run:
                _remove_empty_subdirs(daily_dir)

        # --- 3. 周报：文件级规范化迁移 ---
        if not weekly_files:
            actions.append(f"  [{prefix}] 周报：源为空（无数据，跳过）")
            rows.append({"type": "周报文件迁移", "source": f"{prefix}reports/weekly/",
                         "target": f"{prefix}reports/weekly/YYYY/YYYY-Wxx.md", "verify": "-", "result": "无数据，跳过"})
        else:
            moved, conflicts = 0, []
            for src in weekly_files:
                m = re.search(r"(\d{4})-W(\d{1,2})", src.stem)
                if m:
                    year, week = m.group(1), int(m.group(2))
                    name = f"{year}-W{week:02d}{src.suffix}"
                else:
                    date = _extract_date(src)
                    if date:
                        iso = datetime.strptime(date, "%Y-%m-%d").isocalendar()
                        year, week = iso[0], iso[1]
                        name = f"{year}-W{week:02d}{src.suffix}"
                    else:
                        year = src.parent.name if re.fullmatch(r"\d{4}", src.parent.name) else "unknown"
                        name = src.name
                        actions.append(f"      ⚠️ 无法解析周号，保留原名: {src.relative_to(ai_dir)}")
                dst = weekly_dir / year / name
                if src == dst:
                    moved += 1
                    continue
                if dst.exists():
                    conflicts.append(src)
                    continue
                if not dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                moved += 1
            ok = moved == len(weekly_files) and not conflicts
            verify_msg = f"文件数核对 {moved}/{len(weekly_files)}"
            if conflicts:
                verify_msg += f"，冲突 {len(conflicts)} 个"
                for c in conflicts:
                    actions.append(f"      ⚠️ 冲突（目标已存在）: {c.relative_to(ai_dir)}")
            rows.append({"type": "周报文件迁移", "source": f"{prefix}reports/weekly/（{len(weekly_files)} 个）",
                         "target": f"{prefix}reports/weekly/YYYY/YYYY-Wxx.md", "verify": verify_msg,
                         "result": "成功" if ok else "验证失败（保留旧结构，人工介入）"})
            actions.append(f"  [{prefix}] 周报：迁移 {moved}/{len(weekly_files)}，验证{'通过' if ok else '失败（保留旧结构，人工介入）'}")
            if ok and not dry_run:
                _remove_empty_subdirs(weekly_dir)

        # --- 验证结果登记（N-3）：登记到 context/import-log.md ---
        if rows:
            if dry_run:
                actions.append(f"  [{prefix}] [dry-run] 验证结果将登记: {import_log.relative_to(ai_dir)}")
            else:
                _append_import_log(import_log, rows)
                actions.append(f"  [{prefix}] ✓ 验证结果已登记: {import_log.relative_to(ai_dir)}")

    if not scopes:
        actions.append("  未检测到子项目目录，跳过报告迁移")
    return actions

def detect_project_name(workspace_root: Path) -> str:
    """从工作区读取项目名称。

    优先解析 ai/context/project-brief.md 前置元数据中的
    project / portfolio 字段；读取失败时回退为工作区目录名。
    """
    brief = workspace_root / "ai" / "context" / "project-brief.md"
    if brief.exists():
        try:
            for line in brief.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                for key in ("project:", "portfolio:"):
                    if stripped.startswith(key):
                        name = stripped[len(key):].strip().strip('"')
                        if name:
                            return name
        except OSError:
            pass
    return workspace_root.name


def sync_templates(ai_dir: Path, dry_run: bool = False):
    """同步 Skill 包模板到工作区（只补不覆盖）。

    与 init 的差异：init 面对全新目录（无需 dst 存在性守卫），
    migrate 面对已有工作区，使用 if not dst.exists() 守卫保护用户自定义内容。
    复用 ALL_TEMPLATE_FILES 单一事实源（chronopm_init/config.py），
    未来新增模板只需更新 config.py，migrate 自动覆盖，无需双重维护。
    """
    templates_dir = get_templates_dir()
    missing = []
    synced = 0

    # --- 1. 同步 ai/templates/ 参考模板库 ---
    target_dir = ai_dir / "templates"
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for name in ALL_TEMPLATE_FILES:
        src = templates_dir / name
        dst = target_dir / name
        if not dst.exists():
            if src.exists():
                if dry_run:
                    missing.append(f"templates/{name}")
                else:
                    shutil.copy2(src, dst)
                    synced += 1
            else:
                print(f"  ⚠️ Skill 包模板不存在，跳过: {name}")

    # --- 2. 补齐 ai/outputs/.templates/manifest-template.md ---
    # 与 init 的 create_outputs_dir 行为一致（写死内容生成，非复制模板文件）
    # v2.1.0（D-8）：outputs/ 移入 ai/ 内
    outputs_dir = ai_dir / "outputs"
    manifest_path = outputs_dir / ".templates" / "manifest-template.md"
    if not manifest_path.exists():
        if dry_run:
            missing.append("ai/outputs/.templates/manifest-template.md")
        else:
            create_outputs_dir(str(ai_dir.parent), detect_project_name(ai_dir.parent))
            synced += 1

    return missing, synced


def migrate_workspace(project_root: str, dry_run: bool = False, target_version: str = None, index_mode: str = "structure-only"):
    """执行工作区迁移"""
    ai_dir = Path(project_root) / "ai"

    if not ai_dir.exists():
        print(f"错误: {ai_dir} 不存在")
        return

    print(f"{'='*60}")
    print(f"ChronoPM 工作区迁移")
    print(f"{'='*60}")

    # ★ 无条件模板同步（置于版本检查之前，确保版本已匹配但模板缺失的场景也能触发）
    print(f"\n📋 检查模板完整性...")
    missing_templates, synced_templates = sync_templates(ai_dir, dry_run)
    if missing_templates:
        print(f"  缺失模板 ({len(missing_templates)} 个):")
        for t in missing_templates:
            print(f"    ✗ {t}")
        if not dry_run:
            print(f"  ⚠️ 上述模板将在正式迁移时补齐")
    elif synced_templates > 0:
        print(f"  ✓ 已补齐 {synced_templates} 个模板")
    else:
        print(f"  ✓ 模板完整")

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

    # 4b. v2.1.0 专项迁移（§7.1 路径整合 + §7.3.2b 报告迁移，仅当跨 2.1.0 边界时执行）
    needs_v210 = _vcmp(skill_version, "2.1.0") >= 0 and (
        current_ws_version == "unknown" or _vcmp(current_ws_version, "2.1.0") < 0
    )
    if needs_v210:
        print(f"\n{'='*40}")
        print("v2.1.0 专项迁移（路径整合 + 历史报告迁移）")
        print(f"{'='*40}")
        for line in migrate_v210_paths(ai_dir, dry_run):
            print(f"  {line}")
        for line in migrate_v210_reports(ai_dir, dry_run, mode == "portfolio"):
            print(line)

    # 4c. v3.0.0：默认只升元数据，不自动拆/下沉业务目录（upgrade-to-3.0.0.md 节 B）
    needs_v300 = _vcmp(skill_version, "3.0.0") >= 0 and (
        current_ws_version == "unknown" or _vcmp(current_ws_version, "3.0.0") < 0
    )
    if needs_v300:
        print(f"\n{'='*40}")
        print("v3.0.0：工作区结构迁移见 governance/migrations/upgrade-to-3.0.0.md 节 B")
        print("本次脚本不自动拆工作区、不下沉子项目。仅更新 .skill-version.json 元数据。")
        print(f"{'='*40}")
        sv = ai_dir / ".skill-version.json"
        if sv.exists() and not dry_run:
            try:
                data = json.loads(sv.read_text(encoding="utf-8"))
                data["skillVersion"] = CURRENT_SKILL_VERSION
                data["schemaVersion"] = CURRENT_SCHEMA_VERSION
                if data.get("skillName") in (None, "", "chrono-pm"):
                    data["skillName"] = "chrono-pm-project"
                sv.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print("  已更新 .skill-version.json（skillName=chrono-pm-project, 3.0.0 / schema 0.9.0）")
            except Exception as e:
                print(f"  ⚠️ 未能改写 .skill-version.json: {e}")
        elif dry_run:
            print("  [dry-run] 将更新 .skill-version.json skillVersion/schemaVersion/skillName")

    # 4d. v3.5.0：建 wps/ + 打印一次性抽取入口（不自动删计划内嵌表）
    needs_v350 = _vcmp(skill_version, "3.5.0") >= 0 and (
        current_ws_version == "unknown" or _vcmp(current_ws_version, "3.5.0") < 0
    )
    if needs_v350:
        print(f"\n{'='*40}")
        print("v3.5.0：将创建 wps/ 与 wps/_index.md（schema 0.10.0）")
        print("一次性抽取入口（脚本不自动执行）：")
        print("  1. 扫描 plans/PLAN-*.md 内嵌 WP 表 → 输出抽取清单（含关联需求候选）")
        print("  2. PM 确认 → 建 wps/WP-NNN.md + 更新 _index.md")
        print("  3. 先迁后验（数量核对+抽样）→ 通过后才删计划内嵌表")
        print("  截止条件：首次生成周报或新建待办前必须完成抽取")
        print("  抽取完成前 fallback：查询仍可读 plans 嵌入清单")
        print(f"{'='*40}")

    # 4e. v3.6.0：建 requirements/sources/ + 打印一次性迁移入口
    needs_v360 = _vcmp(skill_version, "3.6.0") >= 0 and (
        current_ws_version == "unknown" or _vcmp(current_ws_version, "3.6.0") < 0
    )
    if needs_v360:
        print(f"\n{'='*40}")
        print("v3.6.0：将创建 requirements/sources/ 与 _index.md（schema 0.11.0）")
        print("一次性迁移入口（脚本不自动删旧 {type}-source/）：")
        print("  1. 扫描 requirements/*-source/ → 按 source_doc 聚合输出映射清单（簇 ID 冻结）")
        print("  2. PM 确认 → 建 sources/{编号}/ + 搬移 + 补 meta/_digest")
        print("  3. 先迁后验（数量核对+抽样）→ 通过后才删旧目录")
        print("  截止条件：首次新拆解或首次 RI 范围判定前必须完成")
        print("  抽取完成前 fallback：查询仍可读 {type}-source/")
        print("  基线包新 source_type 按需启用，不预灌")
        print(f"{'='*40}")

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
