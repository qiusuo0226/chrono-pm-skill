#!/usr/bin/env python3
"""ChronoPM 单一版本源（Single Source of Truth）。

本模块是 Skill 版本与工作区 Schema 版本的【唯一事实源】。
任何脚本需要版本号时必须从此处导入，禁止在脚本内硬编码版本字符串。

职责：
    - 定义 SKILL_VERSION（Skill 本体版本）
    - 定义 WORKSPACE_SCHEMA_VERSION（工作区目录结构 Schema 版本）

如何使用（见 CR-20260810-009-version-sync-fix）：
    - scripts/migrate_workspace.py（位于 scripts/ 下，运行时 scripts/ 在 sys.path[0]）：
          from _version import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION
    - scripts/chronopm_init/config.py（位于包内，向上定位 scripts 后导入）：
          import sys
          from pathlib import Path
          sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
          from _version import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION

升级本 Skill 时只需改此处的版本号，其余触点（VERSION / SKILL.md / skill.json /
CHANGELOG）由发布流程统一同步，禁止遗漏。
"""

# Skill 本体版本（发布时统一 bump）
SKILL_VERSION = "3.25.2"

# 工作区目录结构 Schema 版本（CR-20260811-002 → 0.6.0；CR-20260813-001 → 0.7.0 跨源需求归集；
# CR-20260813-002 → 0.8.0 合同作用域 RI，新增 portfolio/requirements + contract-register；
# v2.1.0 保持 0.8.0 不变：路径整合 continuity/→context/、outputs/→ai/outputs/ 为存量迁移，不引入新 schema；
# 0.9.0 = 联邦挂载 projects/{名}/ai/ + 项目 ai 内禁 portfolio/projects；
# 0.10.0 = 新增 wps/ 独立 WP 目录 + _index.md；
# 0.11.0 = 新增 requirements/sources/ 文档级拆解目录 + _index.md；
# 0.12.0 = parse-log + 可选 atoms/facts 分片；废 entity-registry；风险/问题登记册新结构；
# 0.13.0 = 各项目 ai/backup/ 空目录；人员事实源改待办+_index；
# 0.14.0 = pm-decisions 取代 pending-changes；需求索引；WP 待确认；关联处理记录；
# 0.15.0 = 新增 ai/project-info/；budget/progress-plan 迁出 plans/；
# 0.16.0 = pm-profile current_operator；升级契约含存量受控迁移。
# 3.21.0 百科叠层为懒建派生，不升 schema：新增必填目录/必填文件/迁移义务才升 schema；
# 懒建可选派生物（缺了能降级、不参与 migrate 校验）不升。）
WORKSPACE_SCHEMA_VERSION = "0.16.0"
