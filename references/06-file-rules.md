# 文件管理约束规则

本规则适用于项目记忆库中文件的命名、创建、更新、拆分和归档。

## 1. AI 文件目录边界规则（项目集模式）

### 1.1 核心原则：业务目录不侵入

AI 生成的所有管理文件必须统一存放在 `ai/` 目录下，**严禁在业务代码目录或项目交付物目录中创建任何 AI 管理文件**。

### 1.1a project-brief.md — AI 首读文件

`context/project-brief.md`（项目集模式为 `portfolio/context/project-brief.md`）是 AI 的**快速入口文件**。

**规则：**

1. AI 在处理任何用户输入（文本、文件、口述）前，**必须先读取 `project-brief.md`**，获取项目基本信息、子项目清单、团队成员、文件路由速查表。
2. AI 通过 `project-brief.md` 中的信息判断输入内容与当前项目的关联度，确定项目归属和作用范围。
3. `project-brief.md` 应保持精炼（建议 ≤ 100 行），只放 AI 快速判断所需的关键信息。详细背景见 `project-context.md`。
4. `project-brief.md` 是事实源文件，更新需经用户确认。
5. 项目初始化时由 `init_workspace.py` 自动生成空模板。
6. **团队信息指针化（v1.6.1 新增）**：`project-brief.md` 中的团队信息不应复制 `resource-register.md` 的完整团队列表，而应使用指针指向 register。brief 中的团队部分应替换为：
   ```markdown
   ## 3. 团队成员
   → 见 `portfolio/resources/resource-register.md`（人员当前状态主源）
   → 见 `portfolio/resources/transfer-log.md`（人员流转历史）
   ```
   **迁移规则**：不自动删除 brief 中已有的团队列表，只新增主源指针说明并标记冗余信息待确认清理。下次 register 更新时，AI 提示用户"brief 中的团队列表已指针化，建议删除冗余的团队信息"，用户确认后删除冗余信息。

| 目录 | 是否允许创建AI文件 | 说明 |
|---|---|---|
| `ai/portfolio/` | ✅ 允许 | 项目集级管理文件 |
| `ai/projects/{子项目}/` | ✅ 允许 | 子项目级管理文件 |
| `ai/portfolio/resources/` | ✅ 允许 | 人员资源管理文件（项目集级） |
| 业务代码目录 / 需求文档目录 / 交付物目录 | ❌ 禁止 | AI 不得在此创建或修改任何文件 |

### 1.2 项目集模式目录结构

```
ai/
├── portfolio/                          # 项目集级管理文件
│   ├── context/
│   │   └── project-index.md           # 子项目索引（PRJ-NNN）
│   │   └── project-context.md         # 项目集背景信息
│   ├── reports/
│   │   └── weekly/YYYY/YYYY-Wxx.md    # 项目集汇总周报
│   ├── risks/
│   │   └── board.md                   # 跨项目风险看板
│   ├── plans/
│   │   └── budget-summary.md           # 整体P&L
│   ├── todos/                       # 待办查询加速层
│   │   ├── personal-todo-index.md  # 按人聚合待办
│   │   ├── daily-todo-index.md     # 按日期聚合待办
│   │   ├── weekly-todo-index.md    # 按周聚合待办
│   │   ├── history-index.md       # 历史快照索引
│   │   ├── snapshots/             # 计划快照（冻结）
│   │   │   ├── daily/
│   │   │   └── weekly/
│   │   └── actuals/               # 实际执行摘要
│   │       ├── daily/
│   │       └── weekly/
│   ├── resources/
│   │   ├── resource-register.md       # 人员资源当前状态
│   │   └── transfer-log.md            # 人员流转历史
│   └── meetings/YYYYMM/                # 跨项目会议纪要
├── projects/
│   ├── {子项目1}/                     # 子项目1管理文件
│   │   ├── tasks/
│   │   ├── risks/
│   │   ├── issues/
│   │   ├── plans/
│   │   ├── requirements/
│   │   ├── milestones/
│   │   ├── decisions/
│   │   ├── reports/
│   │   └── meetings/
│   ├── {子项目2}/
│   └── {子项目3}/
└── logs/
    └── ai-generation-log.md
```

### 1.3 单项目模式目录结构

```
ai/
├── tasks/
├── risks/
├── issues/
├── plans/
├── requirements/
├── milestones/
├── decisions/
├── reports/
├── meetings/
└── logs/
```

### 1.4 更新权限分级

默认采用 `auto_write_low_risk` 模式。项目可在 `prompts/project-rules.md` 中修改权限级别。

**低风险更新（可主动生成或直接更新）：**
- 日报归档、会议纪要草稿归档、评审纪要归档
- 周报/月报草稿生成
- 资源流转日志候选、AI 操作日志更新
- backlog 新增待确认任务
- 风险/问题候选新增为 open

**高风险更新（必须确认后才能更新）：**
- 需求状态确认/取消、需求变更批准
- 预算/P&L 金额调整、里程碑日期调整
- 任务关闭、风险/问题关闭
- 正式决策记录、验收结论
- 人员正式离场、删除/覆盖/重写历史记录

详细触发机制和路由见 `10-update-trigger-rules.md`。

### 1.5 资源文件状态与历史分离规则

人员资源管理遵循「状态与历史分离」原则：

| 文件 | 定位 | 内容 | 更新方式 |
|---|---|---|---|
| `portfolio/resources/resource-register.md` | 当前状态事实源 | 人员当前状态快照（角色/状态/分配方式/B角等） | 覆盖更新（每次只保留最新状态） |
| `portfolio/resources/transfer-log.md` | 流转历史记录 | 所有人员进出、调配、角色变更的完整流水 | 追加更新（只增不改不删） |

**规则：**
1. `resource-register.md` 只反映当前状态，不保留历史状态。历史状态通过 `transfer-log.md` 追溯。
2. `transfer-log.md` 是只追加文件，已录入的流转记录不可修改或删除。
3. 两个文件通过「资源 ID（RES-NNN）」和「姓名」关联。
4. AI 检测到资源变动时，必须同时建议更新两个文件：在 `transfer-log.md` 追加流转记录，在 `resource-register.md` 更新状态。

## 2. 文件命名规范

### 2.1 事实源文件

固定文件名，不附加日期：
```
tasks/board.md
tasks/backlog.md
risks/risk-register.md
issues/issue-register.md
decisions/decision-log.md
milestones/milestone-board.md
plans/progress-plan.md
plans/budget.md
requirements/requirement-register.md
requirements/change-log.md
```

### 2.2 项目集级事实源文件（项目集模式）

固定文件名，不附加日期：
```
portfolio/context/project-index.md
portfolio/context/project-context.md
portfolio/reports/weekly/YYYY/YYYY-Wxx.md
portfolio/risks/board.md
portfolio/plans/budget-summary.md
portfolio/resources/resource-register.md
portfolio/resources/transfer-log.md
```

### 2.3 过程记录文件

按日期命名，格式：`YYYY-MM-DD-[描述].md`

**目录层级规则：按月归档，使用 `YYYYMM` 单级目录，不再使用 `YYYY/MM` 两级。**

```
reports/daily/personal/YYYYMM/YYYY-MM-DD-[name].md
reports/daily/project/YYYYMM/YYYY-MM-DD-[project]-项目日报.md
reports/weekly/YYYY-Wxx-[project]-周报.md
reports/monthly/YYYYMM-[project]-月报.md
meetings/YYYYMM/YYYY-MM-DD-[topic].md
reviews/YYYYMM/YYYY-MM-DD-[event]-retrospective.md
```

**个人进度汇总文件（新增）：**

```
reports/daily/personal/summaries/[name]-progress.md
```

每个团队成员维护一份个人进度汇总文件，记录该成员当前负责的任务、里程碑关联、风险点和历史进展概要。当该成员的日报更新时，自动同步更新此文件。

### 2.4 月度文件数量阈值规则

默认一个月内所有个人日报放在同一个 `YYYYMM/` 目录下。

当单月个人日报文件数量超过 **800** 个时，AI 应建议启用按日期二级拆分：

```
reports/daily/personal/YYYYMM/YYYY-MM-DD/[name].md
```

未超过阈值时不应主动拆分，以避免目录过深。

### 2.5 索引文件

固定文件名：`index.md`，放在对应目录下。

## 3. 文档元数据头
每份正式文档头部必须包含：

```yaml
---
doc_type: [文档类型]
project: [项目名]
milestone: [当前里程碑]
version: v1.0
date: YYYY-MM-DD
status: 草稿 / 评审中 / 已确认 / 已归档
author: AI辅助生成
---
```

## 4. 文件创建规则
1. 新文件创建时必须从 `templates/` 目录对应模板复制。
2. 如果模板不存在，先创建模板再创建文件。
3. 创建后必须在对应 `index.md` 中登记。
4. 文件创建时状态默认为"草稿"。

## 5. 文件更新规则

1. 事实源文件更新必须经过人工确认。
2. 更新前必须读取文件当前内容，确认版本一致。
3. 状态为"已确认"或"已归档"的文件不可直接修改：
   - 已确认文件：追加新版本，保留旧版本。
   - 已归档文件：不可修改。
4. 每次更新必须在文件底部 Change Log 中记录。
5. 更新后版本号递增（v1.0 → v1.1 小修订，v1.0 → v2.0 大变更）。

## 6. 文件瘦身规则

### 6.1 拆分触发条件

当单个 Markdown 文件满足以下任一条件时，AI 应建议拆分：

1. 超过 300 行。
2. 超过 30 条记录。
3. 包含超过 3 个月的连续记录。
4. 同时包含多个不同管理对象。
5. 用户需要频繁检索其中某类子记录。

### 6.2 拆分规则

| 文件类型 | 拆分方式 |
|----------|----------|
| 日报 | 按天拆分（已执行） |
| 会议纪要 | 按会议拆分（已执行） |
| 复盘 | 按事件或里程碑拆分 |
| Change Log | 超过100行时从主文件拆出为 `*-change-log.md` |
| 风险登记册 | 超过30条时按类别或时间段拆分，保留 index |
| 需求登记册 | 超过50条时按模块拆分，保留 index |
| 任务看板 | 超过50条时按里程碑拆分，保留 index |

### 6.3 拆分后处理

1. 拆分后必须建立或更新 `index.md`。
2. 原文件保留为"当前状态"视图，只保留活跃记录。
3. 历史记录移入归档文件，命名 `YYYY/archive-[描述].md`。

## 7. 索引文件规范
索引文件必须包含相应的列定义，完整 markdown 模板见 `assets/templates/index-formats.md`。

### 7.1 日报索引

必须包含列：`Date | Type | File | Owner | Summary | Task Sync | Risk Sync | Issue Sync | Weekly Sync`

### 7.2 会议索引

必须包含列：`Date | Meeting ID | Title | Key Decisions | Action Items | File`

### 7.3 周报索引

必须包含列：`Week | Date Range | File | Status | Key Highlights`

### 7.4 复盘索引
必须包含列：`Date | Event | Milestone | File | Key Lessons`
## 8. Change Log 规范
事实源文件底部必须包含 Change Log，格式见 `assets/templates/index-formats.md`：

- Change Type：`add` / `update` / `remove` / `status` / `archive`
- Source：来源文件或会议 ID
- Confirmed By：确认人姓名（AI 建议的记录为"待确认"）

## 9. 归档规则

1. 超过 3 个月的过程记录可归档到 `YYYY/archive/` 目录。
2. 已关闭的风险/问题可定期归档。
3. 归档操作必须记录在原文件的 Change Log 中。
4. 归档文件状态改为"已归档"。

## 10. 安全规则
1. 不得在文件中记录密码、密钥、Token 等凭证。
2. 涉及客户敏感信息时使用脱敏代号。
3. 不得删除或覆盖状态为"已确认"的文件，只能新增版本。

## 11. PM Profile 文件规范

| 模式 | 路径 | 说明 |
|---|---|---|
| portfolio | `ai/portfolio/context/pm-profile.md` | 项目集级 PM 偏好档案 |
| single | `ai/context/pm-profile.md` | 单项目 PM 偏好档案 |

规则：

1. 文件不存在时，不视为错误，降级跳过偏好加载。
2. 初始化新工作区时自动创建（`init_workspace.py` 默认行为）。
3. 旧工作区可通过 `migrate_workspace.py --create-profile` 补建。
4. 已存在时不得覆盖。
5. 不得将 pending 偏好当作 confirmed 偏好应用。
6. 每条偏好记录必须保留 Source 或观察依据。
7. 详见 `references/21-pm-profile-rules.md`。
