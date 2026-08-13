#!/usr/bin/env python3
"""ChronoPM 项目文件生成注册。

职责：生成工作区内各类标准文件（版本文件、迁移日志、项目简报、
上下文、迭代登记册、AI 日志、经验库、项目级规则、输出物目录、
领域词库、README）。函数体在 CR-20260810-001 中由
scripts/init_workspace.py 原样迁移，保证行为零变化。
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

from .config import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION
from .template_renderer import copy_template, get_templates_dir


def create_outputs_dir(project_root: str, project_name: str):
    """在项目根目录下创建 outputs/ 目录和索引文件"""
    outputs_dir = Path(project_root) / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # 创建 outputs/index.md
    index_path = outputs_dir / "index.md"
    if not index_path.exists():
        index_content = f"""---
doc_type: outputs-index
project: "{project_name}"
version: v1.0
date: "{datetime.now().strftime("%Y-%m-%d")}"
status: 草稿
---

# 生成物索引

本文件记录所有 AI 生成物输出批次，按创建时间排列。

## 输出批次记录

| Batch ID | Created At | Request | Type | Status | Main File | Related AI File |
|---|---|---|---|---|---|---|

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
"""
        index_path.write_text(index_content, encoding="utf-8")

    # 创建 manifest 模板参考文件
    manifest_ref_dir = outputs_dir / ".templates"
    manifest_ref_dir.mkdir(parents=True, exist_ok=True)
    manifest_ref_path = manifest_ref_dir / "manifest-template.md"
    if not manifest_ref_path.exists():
        manifest_ref_content = """---
doc_type: output-manifest
batch_id: YYYYMMDDHHMMSS
---

# 输出批次清单

## 基本信息
| Field | Value |
|---|---|
| Batch ID | YYYYMMDDHHMMSS |
| Created At | YYYY-MM-DD HH:MM:SS |
| Status | draft |
| Request Type | [类型] |
| User Request | [请求] |
| Skill Version | chrono-pm 0.5.0 |

## 来源文件
| Source File | Purpose |
|---|---|

## 生成文件
| File | Type | Status |
|---|---|---|

## 修订历史
| Revision | Time | Summary |
|---|---|---|

## 归档信息
| Field | Value |
|---|---|
| Archived To | pending |
| Archived At | - |
| Confirmed By | - |
"""
        manifest_ref_path.write_text(manifest_ref_content, encoding="utf-8")


def create_skill_version(ai_dir: Path, mode: str):
    """在工作区根目录生成 .skill-version.json"""
    version_path = ai_dir / ".skill-version.json"
    if version_path.exists():
        return

    metadata = {
        "skill": "chrono-pm",
        "skillVersion": SKILL_VERSION,
        "workspaceSchemaVersion": WORKSPACE_SCHEMA_VERSION,
        "mode": mode,
        "initializedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "lastMigratedAt": None
    }
    version_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def create_migration_log(ai_dir: Path):
    """在工作区 logs/ 下生成 migration-log.md"""
    log_path = ai_dir / "logs" / "migration-log.md"
    if log_path.exists():
        return

    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
doc_type: migration-log
skill_version: "{SKILL_VERSION}"
schema_version: "{WORKSPACE_SCHEMA_VERSION}"
---

# 迁移历史记录

本文件记录工作区的结构迁移历史，每次 schema 版本变更时追加记录。

---

## {today} - 初始化 (schema {WORKSPACE_SCHEMA_VERSION})

### 初始化信息
- Skill 版本：{SKILL_VERSION}
- Workspace Schema 版本：{WORKSPACE_SCHEMA_VERSION}
- 操作：初始化
- 结果：success

"""
    log_path.write_text(content, encoding="utf-8")


def create_brief_file(base_dir: Path, project_name: str, is_portfolio: bool = False, sub_projects: list = None):
    """创建项目简报文件（AI 首读入口文件）"""
    brief_path = base_dir / "context" / "project-brief.md"
    if brief_path.exists():
        return

    scope = "portfolio" if is_portfolio else "project"
    scope_label = "项目集" if is_portfolio else "项目"
    mode = "项目集" if is_portfolio else "单项目"

    # 构建子项目清单表格
    sub_table_lines = []
    if is_portfolio and sub_projects:
        for idx, sub_name in enumerate(sub_projects, 1):
            sub_table_lines.append(f"| PRJ-{idx:03d} | {sub_name} | | M0x | | 进行中 |")
        sub_table = "\n".join(sub_table_lines)
    else:
        sub_table = "| （单项目模式，无子项目） |"

    brief_content = f"""---
doc_type: project-brief
{scope}: "{project_name}"
version: v1.0
date: "{datetime.now().strftime("%Y-%m-%d")}"
status: 草稿
author: AI辅助生成
---

# {scope_label}简报 — AI 快速入口

> 本文件是 AI 处理任何用户输入前的**必读文件**。AI 在解析日报、会议纪要、需求文件、评审材料等内容前，必须先读取本文件，以此判断输入内容与当前项目的关联度，确定项目归属和作用范围。
>
> 本文件应保持精炼（建议 ≤ 100 行），只放 AI 快速判断所需的关键信息。详细背景见 `project-context.md`。

## 1. 项目基本信息

- **{scope_label}名称**：{project_name}
- **项目类型**：{mode}
- **当前阶段**：M0x [里程碑名称]
- **立项时间**：YYYY-MM-DD
- **启动日期**：YYYY-MM-DD
- **计划完成**：YYYY-MM-DD

## 2. 子项目清单（项目集模式填写）

| 项目ID | 子项目名称 | 一句话描述 | 当前里程碑 | PM | 状态 |
|---|---|---|---|---|---|
{sub_table}

## 3. 迭代概览

> 仅放一行摘要，明细见各子项目 `plans/iteration-register.md`。

{sub_table if is_portfolio else "- [项目名称]：0 个迭代 / 0 个需求 / 0 名资源"}

## 4. 团队核心成员

| 姓名 | 角色 | 所属子项目 | 分配方式 | 备注 |
|---|---|---|---|---|
| | | | | |

## 5. 技术栈与关键约束

- **后端**：
- **前端**：
- **数据库**：
- **信创要求**：
- **关键约束**：

## 6. 管理约定

- **日报截止时间**：每天 18:00 前
- **周报频率**：每周五汇总
- **评审要求**：
- **风险升级阈值**：

## 7. 文件路由速查

| 内容类型 | 目标文件 |
|---|---|
| 人员变动 / 请假 / 借调 | `portfolio/resources/transfer-log.md` + `resource-register.md` |
| 新需求 / 需求变更 | `projects/{{子项目}}/requirements/requirement-register.md` 或 `change-log.md` |
| 任务进展 / 任务完成 | `projects/{{子项目}}/tasks/board.md` |
| 风险识别 | `projects/{{子项目}}/risks/risk-register.md`（项目集级 → `portfolio/risks/`）|
| 问题 / 阻塞 | `projects/{{子项目}}/issues/issue-register.md` |
| 决策 / 结论 | `projects/{{子项目}}/decisions/decision-log.md` |
| 里程碑变更 | `projects/{{子项目}}/milestones/milestone-board.md` |
| 成本 / 预算变动 | `projects/{{子项目}}/plans/budget.md`（项目集级 → `portfolio/plans/budget.md`）|
| 日报归档 | `projects/{{子项目}}/reports/daily/` |
| 会议纪要 | `projects/{{子项目}}/meetings/`（跨项目 → `portfolio/meetings/`）|

## 8. AI 处理前必读声明

AI 在处理以下任何类型输入前，**必须先读取本文件**：

- 用户粘贴的文本内容
- 用户上传的文件（评审材料、会议纪要、日报、需求文档等）
- 用户口述的项目信息
- 用户要求"记录一下""更新一下""整理到项目里"时

**判断流程：**

1. 读取本文件，获取项目基本信息、子项目清单、团队成员
2. 扫描输入内容，提取关键词（人名、子项目名、需求编号、任务编号等）
3. 与本文件中的信息进行匹配，判断关联度和项目归属
4. 关联度高 → 按 `10-update-trigger-rules.md` 进入更新流程
5. 关联度低 → 提示用户"该内容似乎与当前项目不匹配，请确认是否需要纳入管理"

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
"""
    brief_path.write_text(brief_content, encoding="utf-8")


def create_context_file(base_dir: Path, project_name: str, is_portfolio: bool = False):
    """创建项目上下文文件"""
    context_path = base_dir / "context" / "project-context.md"
    if context_path.exists():
        return

    doc_type = "portfolio-context" if is_portfolio else "project-context"
    scope_label = "项目集" if is_portfolio else "项目"

    context_content = f"""---
doc_type: {doc_type}
{"portfolio" if is_portfolio else "project"}: "{project_name}"
version: v1.0
date: "{datetime.now().strftime("%Y-%m-%d")}"
status: 草稿
---

# {scope_label}背景

## 合同信息

| 项目 | 内容 |
|------|------|
| 合同名称 | |
| 合同总额 | XX万元 |
| 合同类型 | 固定总价含税合同 / 其他 |
| 合同范围摘要 | 一段话概括合同覆盖的业务范围 |
| 立项时间 | YYYY-MM-DD |
| 启动时间 | YYYY-MM-DD |
| 计划完工时间 | YYYY-MM-DD |
| 测算周期 | 如：12个月开发 + 12个月质保 |

## {scope_label}名称
{project_name}

## {scope_label}背景

（描述{scope_label}背景、来源、业务需求）

## {scope_label}目标

（描述{scope_label}要达成的目标）

## {scope_label}范围

### 包含范围
- 

### 排除范围
- 

## 当前阶段

里程碑：M01

## 关键约束
- 技术约束：
- 合规约束：
- 资源约束：

## 关键干系人

| 姓名 | 角色 | 关注点 |
|------|------|--------|
| | | |

## 备注
"""
    context_path.write_text(context_content, encoding="utf-8")


def create_iteration_register(base_dir: Path, project_name: str, is_portfolio: bool = False):
    """创建迭代登记册文件"""
    register_path = base_dir / "plans" / "iteration-register.md"
    if register_path.exists():
        return

    templates_dir = get_templates_dir()
    copy_template(templates_dir, register_path, "iteration-register-template.md")


def create_ai_log(base_dir: Path, name: str, scope: str = "project"):
    """创建 AI 操作日志"""
    log_path = base_dir / "logs" / "ai-generation-log.md"
    log_content = f"""---
doc_type: ai-generation-log
{scope}: "{name}"
---

# AI 操作日志

| Time | Action | Source | Suggested Target | Summary | Confirm Status |
|------|--------|--------|------------------|---------|----------------|
"""
    log_path.write_text(log_content, encoding="utf-8")


def create_lessons_file(base_dir: Path, name: str, scope: str = "project"):
    """创建经验教训文件"""
    lessons_path = base_dir / "reviews" / "lessons-learned.md"
    if lessons_path.exists():
        return
    lessons_content = f"""---
doc_type: lessons-learned
{scope}: "{name}"
version: v1.0
date: "{datetime.now().strftime("%Y-%m-%d")}"
status: 草稿
---

# 经验教训库

本文件持续累积项目过程中的经验教训，按时间倒序排列。

---

## {datetime.now().strftime("%Y-%m-%d")} 初始化

- 项目工作区初始化完成。
"""
    lessons_path.write_text(lessons_content, encoding="utf-8")


def create_project_rules(base_dir: Path, name: str, is_portfolio: bool = False):
    """创建项目级规则覆盖文件"""
    prompts_dir = base_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    scope = "项目集" if is_portfolio else "项目"

    rules_path = prompts_dir / "project-rules.md"
    if rules_path.exists():
        return
    rules_content = f"""---
doc_type: {"portfolio-rules" if is_portfolio else "project-rules"}
{"portfolio" if is_portfolio else "project"}: "{name}"
---

# {scope}特有规则

本文件记录当前{scope}特有的管理规则，优先级高于 Skill 默认规则（但不可覆盖安全底线）。

## {scope}级规则

（在此添加{scope}特有的管理规则，例如：
- 所有客户口头需求必须进入 change-log.md 的 submitted 状态
- 所有日报必须在每天 18:00 前收集
- 所有高风险必须在周报中单独列出
）
"""
    rules_path.write_text(rules_content, encoding="utf-8")


def create_glossary(project_root: str, mode: str):
    """创建领域词库模板，内置用户已确认初始词条，不自动抽取历史术语"""
    templates_dir = get_templates_dir()
    template_name = "domain-glossary-template.md"
    src = templates_dir / template_name

    if mode == "portfolio":
        target_dir = Path(project_root) / "ai" / "portfolio" / "context"
    else:
        target_dir = Path(project_root) / "ai" / "context"

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "domain-glossary.md"

    if target_path.exists():
        print(f"  词库文件已存在，跳过: {target_path}")
        return

    if src.exists():
        shutil.copy2(src, target_path)
        print(f"  创建领域词库: {target_path}")
        print(f"  内置初始词条：外资→外商投资、农专→农民专业合作社")
        print(f"  不自动抽取历史术语")
    else:
        print(f"  警告: 模板文件不存在: {src}")


RI_CATEGORY_FILES = [
    "contractual", "procurement", "approval",
    "compliance", "technical", "operational",
]


def create_ri_skeleton(ai_dir: Path):
    """创建跨源需求归集（RI）骨架文件（CR-20260813-001）。

    在工作区 ai/requirements/ 下创建 canonical/ 与 atoms/ 的 L1/L2/L3 骨架，
    供 0.7.0 工作区初始化与迁移复用（内容由 AI/PM 后续填充，不预填数据）。
    """
    cats_dir = ai_dir / "requirements" / "atoms"
    can_dir = ai_dir / "requirements" / "canonical"

    headers = {
        "atom-index.md": "---\ndoc_type: atom-index\nversion: v1.0\nlast_updated:\n---\n\n# ATOM 主索引（L1 路由）\n\n| source_category | ATOM 数 | L2 索引文件 | L3 全文文件 | last_source_version | last_updated |\n|---|---|---|---|---|---|\n",
        "canonical-index.md": "---\ndoc_type: canonical-index\nversion: v1.0\nlast_updated:\n---\n\n# Canonical 索引\n\n| CAN_ID | norm_text 摘要 | scope_scope | evidence 数 | status | 文件 |\n|---|---|---|---|---|---|\n",
    }
    for cat in RI_CATEGORY_FILES:
        headers[f"{cat}-index.md"] = (
            "---\ndoc_type: category-index\ncategory: " + cat + "\nversion: v1.0\nlast_updated:\n---\n\n"
            f"# {cat} 类别倒排索引（L2）\n\n| keyword | ATOM ID | norm_text 摘要 | source_type | authority |\n|---|---|---|---|---|\n"
        )
        headers[f"{cat}.md"] = (
            "---\ndoc_type: atom-category\ndoc_type_category: " + cat + "\nversion: v1.0\nlast_updated:\n---\n\n"
            f"# {cat} ATOM 全文（L3）\n"
        )

    for name, content in headers.items():
        if "canonical" in name:
            path = can_dir / name
        else:
            path = cats_dir / name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")


def create_pm_profile(project_root: str, mode: str):
    """创建 PM 偏好档案模板，不自动抽取历史偏好"""
    templates_dir = get_templates_dir()
    template_name = "pm-profile-template.md"
    src = templates_dir / template_name

    if mode == "portfolio":
        target_dir = Path(project_root) / "ai" / "portfolio" / "context"
    else:
        target_dir = Path(project_root) / "ai" / "context"

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "pm-profile.md"

    if target_path.exists():
        print(f"  PM 偏好档案已存在，跳过: {target_path}")
        return

    if src.exists():
        shutil.copy2(src, target_path)
        print(f"  创建 PM 偏好档案: {target_path}")
        print(f"  AI 将在交互中被动学习用户习惯，写入 pending 后经用户确认升为 confirmed")
    else:
        print(f"  警告: 模板文件不存在: {src}")


def generate_single_readme(project_name: str) -> str:
    """生成单项目 README.md"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""---
doc_type: workspace-readme
project: "{project_name}"
version: v1.0
date: "{today}"
---

# ChronoPM 项目管理工作区

本目录是 ChronoPM 技能的项目实例（单项目模式）。

## 相关目录

- `ai/`（本目录）：事实源、规则、模板、项目管理记录
- `outputs/`（同级）：AI 生成物和导出文件（周报/月报/Excel/Word/PDF等）

## 版本信息

- Skill 版本：{SKILL_VERSION}
- Workspace Schema 版本：{WORKSPACE_SCHEMA_VERSION}
- 模式：single
- 详细变更见 Skill 包 `CHANGELOG.md`
- AI 进入工作区时先读取 `.skill-version.json` 检查版本兼容性

## 目录结构

```
ai/
├── README.md                      # 本文件
├── prompts/                       # 项目级提示词
│   └── project-rules.md           # 项目特有规则
├── context/                       # 项目背景记忆
│   └── project-context.md
├── requirements/                  # 需求管理
│   ├── requirement-register.md
│   └── change-log.md
├── plans/                         # 计划类事实源
│   ├── progress-plan.md
│   └── budget.md
├── milestones/                    # 里程碑
│   └── milestone-board.md
├── tasks/                         # 任务管理
│   ├── board.md
│   └── backlog.md
├── meetings/                      # 会议纪要
├── reports/                       # 报告
│   ├── daily/                     # 日报
│   ├── weekly/                    # 周报
│   └── monthly/                   # 月报
├── risks/                         # 风险登记册
├── issues/                        # 问题登记册
├── decisions/                     # 决策记录
├── reviews/                       # 复盘与经验
├── templates/                     # 文档模板
└── logs/                          # AI 操作日志
```

## 事实源文件

- `tasks/board.md` - 任务状态
- `risks/risk-register.md` - 风险登记册
- `issues/issue-register.md` - 问题登记册
- `decisions/decision-log.md` - 决策记录
- `milestones/milestone-board.md` - 里程碑状态
- `plans/progress-plan.md` - 进度计划
- `plans/budget.md` - 预算与 P&L
- `requirements/requirement-register.md` - 需求登记册
- `requirements/change-log.md` - 需求变更记录

## 提示词路由

| 场景 | 必须加载 | 可选加载 |
|------|----------|----------|
| 日报处理 | 00 + 01 + 06 | 03、04、07 |
| 会议纪要处理 | 00 + 02 + 06 | 03、04、07、08 |
| 需求评审/变更 | 00 + 07 + 08 + 06 | 03 |
| 任务看板更新 | 00 + 03 + 06 | - |
| 风险评估 | 00 + 04 | - |
| 项目状态查询 | 00 + 05 | 按问题类型按需加载 |

## 规则优先级

```
Level 0: 平台/系统安全规则（不可覆盖）
Level 1: Skill 核心底线（不可覆盖）
Level 2: 项目级规则（project-rules.md）
Level 3: 本次任务运行时指令
Level 4: 用户提供的输入资料
```
"""


def generate_portfolio_readme(portfolio_name: str, sub_projects: list) -> str:
    """生成项目集 README.md"""
    today = datetime.now().strftime("%Y-%m-%d")
    sub_tree = ""
    for idx, sub_name in enumerate(sub_projects, 1):
        prj_id = f"PRJ-{idx:03d}"
        sub_tree += f"│   ├── {sub_name}/             # {prj_id}\n"
    # 最后一个去掉 ├── 改为 └──
    lines = sub_tree.rstrip().split("\n")
    if lines:
        lines[-1] = lines[-1].replace("├──", "└──")
    sub_tree = "\n".join(lines) + "\n"

    return f"""---
doc_type: workspace-readme
portfolio: "{portfolio_name}"
version: v1.0
date: "{today}"
---

# ChronoPM 项目集管理工作区

本目录是 ChronoPM 技能的项目实例（**项目集模式**）。

## 相关目录

- `ai/`（本目录）：事实源、规则、模板、项目管理记录
- `outputs/`（同级）：AI 生成物和导出文件（周报/月报/Excel/Word/PDF等）

## 版本信息

- Skill 版本：{SKILL_VERSION}
- Workspace Schema 版本：{WORKSPACE_SCHEMA_VERSION}
- 模式：portfolio
- 详细变更见 Skill 包 `CHANGELOG.md`
- AI 进入工作区时先读取 `.skill-version.json` 检查版本兼容性

## 目录结构

```
ai/
├── README.md                      # 本文件
├── portfolio/                     # 项目集级管理文件
│   ├── context/
│   │   ├── project-index.md      # 子项目索引（PRJ-NNN）
│   │   └── project-context.md    # 项目集背景
│   ├── reports/
│   │   └── weekly/               # 项目集汇总周报
│   ├── risks/
│   │   └── board.md              # 跨项目风险看板
│   ├── plans/
│   │   └── budget-summary.md     # 整体 P&L
│   ├── resources/
│   │   ├── resource-register.md  # 人员资源当前状态
│   │   └── transfer-log.md       # 人员流转历史
│   ├── meetings/                 # 跨项目会议纪要
│   └── logs/
├── projects/                      # 各子项目管理文件
{sub_tree}└── logs/
    └── ai-generation-log.md
```

## 事实源文件

### 项目集级
- `portfolio/context/project-index.md` - 子项目索引
- `portfolio/risks/board.md` - 跨项目风险看板
- `portfolio/plans/budget-summary.md` - 整体 P&L
- `portfolio/resources/resource-register.md` - 人员资源当前状态
- `portfolio/resources/transfer-log.md` - 人员流转历史

### 子项目级（每个子项目）
- `tasks/board.md` - 任务状态
- `risks/risk-register.md` - 风险登记册
- `issues/issue-register.md` - 问题登记册
- `milestones/milestone-board.md` - 里程碑状态
- `plans/budget.md` - 预算与 P&L
- `requirements/requirement-register.md` - 需求登记册
- `requirements/change-log.md` - 需求变更记录

## 资源管理说明

人员资源采用**状态与历史分离**模式：

| 文件 | 定位 | 更新方式 |
|------|------|----------|
| `portfolio/resources/resource-register.md` | 当前状态 | 覆盖更新 |
| `portfolio/resources/transfer-log.md` | 流转历史 | 只追加 |

资源 ID：`RES-NNN`（资源）、`RTF-YYYYMMDD-NNN`（流转记录）

## 报告层级

```
各子项目日报（每日）→ 各子项目周报（每周）→ 项目集汇总周报（每周）
```

## 提示词路由

| 场景 | 必须加载 | 可选加载 |
|------|----------|----------|
| 日报处理 | 00 + 01 + 06 | 03、04、07、09 |
| 项目集周报 | 00 + 01 + 09 + 06 | 04 |
| 会议纪要处理 | 00 + 02 + 06 | 03、04、07、08 |
| 需求评审/变更 | 00 + 07 + 08 + 06 | 03 |
| 任务看板更新 | 00 + 03 + 06 | - |
| 风险评估 | 00 + 04 | 09（跨项目风险） |
| 项目状态查询 | 00 + 05 | 09（跨项目查询） |
| 资源管理 | 00 + 09 + 06 | 05（资源查询） |

## 规则优先级

```
Level 0: 平台/系统安全规则（不可覆盖）
Level 1: Skill 核心底线（不可覆盖）
Level 2: 项目集级规则（portfolio/prompts/）
Level 2.5: 子项目级规则（projects/{{子项目}}/prompts/）
Level 3: 本次任务运行时指令
Level 4: 用户提供的输入资料
```

## 业务目录不侵入原则

AI 生成的所有管理文件统一存放在 `ai/` 目录下，**严禁在业务代码目录或项目交付物目录中创建任何 AI 管理文件**。

## ID 编码体系

| 前缀 | 含义 | 格式 |
|------|------|------|
| T- | 任务 | T-YYYYMMDD-NNN |
| R- | 风险 | R-YYYYMMDD-NNN |
| I- | 问题 | I-YYYYMMDD-NNN |
| MTG- | 会议 | MTG-YYYYMMDD-NNN |
| RES- | 资源 | RES-NNN |
| RTF- | 资源流转 | RTF-YYYYMMDD-NNN |
| PRJ- | 子项目 | PRJ-NNN |
"""
