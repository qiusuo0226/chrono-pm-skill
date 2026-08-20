# 文件管理约束规则

本规则适用于项目记忆库中文件的命名、创建、更新、拆分和归档。

## 1. AI 文件目录边界规则（项目集模式）

### 1.1 核心原则：业务目录不侵入

AI 生成的所有管理文件必须统一存放在 `ai/` 目录下，**严禁在业务代码目录或项目交付物目录中创建任何 AI 管理文件**。

### 1.1a project-brief.md — AI 首读文件

`context/project-brief.md`（项目集模式为 `portfolio/context/project-brief.md`）是 AI 的**快速入口文件**。

**规则：**
1. AI 在处理任何用户输入（文本、文件、口述）前，**必须先读取 `project-brief.md`**，获取项目基本信息、子项目清单、团队成员、文件路由速查表。
2. AI 通过 `project-brief.md` 判断输入与当前项目的关联度，确定项目归属和作用范围。
3. `project-brief.md` 应保持精炼（建议 ≤ 100 行），只放 AI 快速判断所需关键信息。详细背景见 `project-context.md`。
4. `project-brief.md` 是事实源文件，更新需经用户确认。
5. 项目初始化时由 `init_workspace.py` 自动生成空模板。
6. **团队信息指针化（v1.6.1 新增）**：`project-brief.md` 中的团队信息不应复制 `resource-register.md` 完整团队列表，而应使用指针。brief 团队部分替换为：
   ```markdown
   ## 3. 团队成员
   → 见 `projects/{子项目}/resources/resource-register.md`（各子项目人员当前状态主源；单项目模式为 `resources/resource-register.md` 或从待办推导）
   → 见对应子项目 `resources/transfer-log.md`（人员流转历史）
   → 项目集模式跨项目共享人员参照 `portfolio/resources/shared-resource-index.md`（只读索引）
   ```
   **迁移规则**：不自动删除 brief 已有团队列表，只新增主源指针并标记冗余待清理。下次 register 更新时提示用户"brief 团队列表已指针化，建议删除冗余信息"，确认后删除。

| 目录 | 是否允许创建AI文件 | 说明 |
|---|---|---|
| `ai/portfolio/` | ✅ 允许 | 项目集级管理文件 |
| `ai/projects/{子项目}/` | ✅ 允许 | 子项目级管理文件 |
| `ai/portfolio/resources/` | ✅ 允许 | 跨项目人员索引（shared-resource-index/transfer-index，只读指针，不存实体） |
| `ai/projects/{子项目}/resources/` | ✅ 允许 | 子项目人员资源事实源（resource-register/transfer-log） |
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
│   │   └── cross-project-risk-index.md     # 跨项目风险索引（只读指针，实体在主归属子项目）
│   ├── plans/
│   │   └── budget-summary.md           # 合同额汇总索引（指向子项目 budget，实时聚合）
│   ├── requirements/                   # 项目集级跨源需求归集（合同作用域，CR-20260813-002）
│   │   ├── contract-register.md        # 合同登记册（RI 检索入口事实源）
│   │   ├── canonical/                  # 项目集级 Canonical（跨层/跨子项目归并）
│   │   └── atoms/                      # 项目集级 ATOM（portfolio 级合同证据）
│   ├── resources/
│   │   ├── shared-resource-index.md   # 跨项目共享资源索引（只读指针，不存实体）
│   │   └── transfer-index.md          # 跨项目流转索引（只读指针，不存实体）
│   └── meetings/YYYYMM/                # 跨项目会议纪要
├── projects/
│   ├── {子项目1}/                     # 子项目1管理文件
│   │   ├── todos/                     # 每人每日待办文件 + 绑定文件 _index.md
│   │   ├── risks/
│   │   ├── issues/
│   │   ├── plans/                     # 含 PLAN-NNN-{name}.md 计划文件、budget.md
│   │   ├── requirements/
│   │   ├── decisions/
│   │   ├── resources/                 # resource-register.md + transfer-log.md（人员事实源）
│   │   ├── reports/
│   │   └── meetings/
│   ├── {子项目2}/
│   └── {子项目3}/
└── logs/
    └── ai-generation-log.md
```

### 1.3 单项目模式目录结构

单项目模式结构与项目集模式的单个子项目相同，直接放 `ai/` 下（无 `portfolio/`、`projects/` 分层）：
```
ai/ ├── todos/ ├── risks/ ├── issues/ ├── plans/ ├── requirements/ ├── decisions/
   ├── reports/ ├── meetings/ ├── continuity/ └── logs/
```
完整树见 `SKILL.md` §3.2。

### 1.4 更新权限分级

默认采用 `proactive` 模式（主动变更 + 人工确认）。项目可在 `prompts/project-rules.md` 中修改权限级别。

**低/中风险更新（proactive 模式下直接写入事实源，并标记 `Confirmed By: 待确认`，同步登记 `pending-changes.md`，待 PM 确认后持久化）：**
- 日报归档、会议纪要草稿归档、评审纪要归档
- 周报/月报草稿生成
- 资源流转日志候选、AI 操作日志更新
- 未排期待办候选新增（登记 `pending-changes.md`）
- 风险/问题候选新增为开放
- 任务 Due Date / 状态中途 / Owner 等过程性更新（写事实源并标记待确认）

> 低/中风险先在事实源记录新值并标 `Confirmed By: 待确认`，PM 确认后翻转为 PM 姓名，驳回则恢复原值并追加 `已驳回` 记录。若配置 `update_mode: passive` 则回退为"仅输出建议清单，不写事实源"。

**高风险更新（必须确认后才能更新）：**
- 需求状态确认/取消、需求变更批准
- 预算/P&L 金额调整、里程碑日期调整
- 任务关闭、风险/问题关闭
- 正式决策记录、验收结论
- 人员正式离场、删除/覆盖/重写历史记录

详细触发机制和路由见 `10-update-trigger-rules.md`。

### 1.5 资源文件状态与历史分离规则

人员资源管理遵循「状态与历史分离」原则（v2.0.0 零数据源：事实源在各子项目，项目集层只留索引）：

| 文件 | 定位 | 内容 | 更新方式 |
|---|---|---|---|
| `projects/{子项目}/resources/resource-register.md` | 当前状态事实源 | 本项目人员当前状态快照（角色/状态/分配方式/B角等） | 覆盖更新（每次只保留最新状态） |
| `projects/{子项目}/resources/transfer-log.md` | 流转历史记录 | 本项目人员进出、调配、角色变更的完整流水 | 追加更新（只增不改不删） |
| `portfolio/resources/shared-resource-index.md` | 跨项目共享资源索引 | 编号+指向子项目+共享状态（只读指针） | 指针维护，不存实体 |
| `portfolio/resources/transfer-index.md` | 跨项目流转索引 | 编号+指向子项目+日期（只读指针） | 指针维护，不存实体 |

**规则：**
1. `resource-register.md` 只反映当前状态，不保留历史状态。历史状态通过 `transfer-log.md` 追溯。
2. `transfer-log.md` 是只追加文件，已录入的流转记录不可修改或删除。
3. 两个文件通过「资源 ID（RES-NNN）」和「姓名」关联。
4. AI 检测到资源变动时，必须同时建议更新两个文件：在 `transfer-log.md` 追加流转记录，在 `resource-register.md` 更新状态。

## 2. 文件命名规范

### 2.1 事实源文件

固定文件名，不附加日期：
```
todos/{date}/{owner}.md
todos/{date}/_index.md
pending-changes.md
risks/risk-register.md
issues/issue-register.md
decisions/decision-log.md
plans/progress-plan.md
plans/PLAN-NNN-{name}.md
plans/budget.md
requirements/requirement-register.md
requirements/change-log.md
requirements/source-type-registry.md
requirements/contract-register.md
requirements/canonical/canonical-index.md
requirements/canonical/CAN-*.md
requirements/atoms/atom-index.md
requirements/atoms/{category}-index.md
requirements/atoms/{category}.md
```

### 2.2 项目集级事实源文件（项目集模式）

固定文件名，不附加日期：
```
portfolio/context/project-index.md
portfolio/context/project-context.md
portfolio/reports/weekly/YYYY/YYYY-Wxx.md
portfolio/risks/risk-register.md
portfolio/plans/budget-summary.md
portfolio/requirements/contract-register.md
portfolio/requirements/source-type-registry.md
portfolio/requirements/canonical/canonical-index.md
portfolio/requirements/canonical/CAN-*.md
portfolio/requirements/atoms/atom-index.md
portfolio/requirements/atoms/{category}-index.md
portfolio/requirements/atoms/{category}.md
portfolio/resources/shared-resource-index.md   # 只读指针索引，非数据源（v2.0.0 零数据源，见 09 号 §5）
portfolio/resources/transfer-index.md          # 只读指针索引，非数据源
```

> v2.0.0 零数据源：人员资源事实源在各子项目 `projects/{子项目}/resources/`，项目集层 resources/ 只有上述两个只读指针索引，不存实体数据。

### 2.3 过程记录文件

按日期命名，格式：`YYYY-MM-DD-[描述].md`

**目录层级规则：按月归档，使用 `YYYYMM` 单级目录，不再使用 `YYYY/MM` 两级。**

```
reports/daily/project/YYYYMM/YYYY-MM-DD-[project]-项目日报.md
reports/weekly/YYYY-Wxx-[project]-周报.md
reports/monthly/YYYYMM-[project]-月报.md
meetings/YYYYMM/YYYY-MM-DD-[topic].md
reviews/YYYYMM/YYYY-MM-DD-[event]-retrospective.md
```

> **v2.0.0**：个人日报文件与个人进度汇总文件（原 `reports/daily/personal/` 及 `summaries/[name]-progress.md`）已删除；成员工作汇报写入待办文件工作日志段，个人进度由待办文件实时聚合。

### 2.4 月度文件数量阈值规则

默认一个月的项目日报放在同一 `YYYYMM/` 目录。当单月日报数量超过 **800** 个时，AI 建议启用按日期二级拆分：
```
reports/daily/project/YYYYMM/YYYY-MM-DD/[project]-项目日报.md
```
未超过阈值不主动拆分，避免目录过深。

### 2.5 索引文件

固定文件名：`index.md`，放在对应目录下。

### 2.6 历史计划导入快照（external_import）

历史计划批量导入（R1）生成的快照复用 `todos/snapshots/daily|weekly/` 目录，文件名以 `imported-` 前缀区分：`imported-{YYYYMMDD}.md`，frontmatter 标注 `source_type: external_import`。文件命名、元数据与冻结规范详见 `references/15-snapshot-rules.md`（本文件不重复）。

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
| Change Log | 活跃区上限 50 行或超过 30 天触发按月归档到 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航 |
| 风险登记册 | 超过30条时按类别或时间段拆分，保留 index |
| 需求登记册 | 超过50条时按模块拆分，保留 index |
| 待办文件 | 按人按日天然拆分（`todos/{date}/{执行人}.md`），无需再拆；绑定文件 `_index.md` 与待办文件同日同目录 |
| PLAN 文件 | 每计划一文件（`plans/PLAN-NNN-{name}.md`）天然拆分，无需再拆；WP 粗规划表保持一行/WP，不内嵌每日明细 |
| decision-log | 超过30条或文件超300行时按季度拆分到 `decisions/archive/YYYY-QN-decision-log.md`，保留 index |
| issue-register | 超过30条时按状态拆分（`已解决`/`已关闭` 归档，主体保留活跃），保留 index |
| transfer-log | 超过100条或文件超300行时按年度拆分到 `logs/archive/YYYY-transfer-log.md`，保留 index |

> Change Log 归档采用统一的「活跃区 50 行 / 30 天」规则：活跃区超过 50 行或距上次归档超过 30 天时，将历史条目按月归入 `change-log/archive/YYYYMM-change-log.md`（YYYYMM 为归档月份），并在 `change-log/index.md` 登记该月份导航。主动变更（pending）记录在写入时合并写入，同会话确认只记 1 条。

### 6.3 拆分后处理

1. 拆分后必须建立或更新 `index.md`。
2. 原文件保留为"当前状态"视图，只保留活跃记录。
3. 历史记录移入归档文件，命名 `YYYY/archive-[描述].md`。
4. **持续拆分模式**（适用于随状态持续增长的文件，如 issue-register）：主体文件只保留活跃状态记录，已关闭/已解决记录定期移入 `archive/` 下的分片文件（命名 `YYYY-[类型]-register.md`）。归档后仍维护主体 `index.md`。此模式与"第 3 点单文件归档"命名并存，二者均为正式规范。

## 7. 索引文件规范
索引文件必须包含相应的列定义，完整 markdown 模板见 `assets/templates/index-formats.md`。

### 7.1 日报索引
必须包含列：`Date | Type | File | Owner | Summary | Task Sync | Risk Sync | Issue Sync | Weekly Sync`
### 7.2 会议索引
必须包含列：`Date | Meeting ID | Title | Key Decisions | Action Items | File`
### 7.3 周报索引
必须包含列：`Week | Date Range | File | Status | Key Highlights`

## 8. Change Log 规范
事实源文件底部必须包含 Change Log，格式见 `assets/templates/index-formats.md`：

- Change Type：`add` / `update` / `remove` / `status` / `archive`
- Source：来源文件或会议 ID
- Confirmed By：确认人姓名（AI 建议的记录为"待确认"）

> 主动变更模式下，`Confirmed By: 待确认` 的条目还必须同步登记到 `pending-changes.md`（待确认变更索引），与该条目一一对应；PM 确认/驳回后按 §1.4 处理并更新 pending-changes.md。

> 注：此处的 Change Type 是**记录操作类型**（对事实源记录执行的操作），与 `references/08-change-control-rules.md` 中需求变更**影响分类**（requirement/scope/schedule/cost/resource/plan_change）是两个不同概念域，不可混用。计划变更（plan_change）在待办文件底部 Change Log 中以 `update` 操作 + Description 标注体现，不在本枚举中新增类型。

## 9. 归档规则

以下实体满足触发条件时，AI 应在当前处理流程末尾执行归档检查（通常为日报处理 §5.8 通用归档检查、周报生成或相应实体变更流程）：

| 实体 | 触发条件 | 归档目标 | 索引 |
|------|----------|----------|------|
| issue（已关闭） | >30 条 | `issues/archive/YYYY-issue-register.md` | `issues/index.md` |
| risk（已关闭） | >30 条 | `risks/archive/YYYY-risk-register.md` | `risks/index.md` |
| decision（已执行） | >30 条 | `decisions/archive/YYYY-QN-decision-log.md` | `decisions/index.md` |
| transfer-log | >100 条 | `logs/archive/YYYY-transfer-log.md` | `logs/index.md` |
| resource（已离场） | 离场 >90 天 | `resource-register-archive.md` | — |
| snapshot/actuals | >90 天 | `snapshots/archive/YYYY/`、`actuals/archive/YYYY/` | —（v2.0.0 起无 history-index，目录内按月直查） |
| outputs（已导出） | >90 天 | `outputs/archive/YYYY/` | `outputs/index.md` |

归档检查时机：日报处理末尾（01 号 §5.8 通用归档检查）、周报生成时、或对应实体变更流程末尾（见各实体级联传播规则 [AUTO]/[SUGGEST]）。

运维规则：
1. 归档操作本身必须记录在原文件的 Change Log 中（Change Type: `archive`）。
2. 归档文件状态改为"已归档"；主体文件保留"当前状态"视图。
3. 涉及移动/归档**事实源**文件的动作走 SUGGEST（待 PM 确认）；仅派生视图（索引）刷新走 AUTO。

统一归档粒度标准：
- Change Log（各事实源底部）：50 行 / 30 天 → 月归档（已有，不变）
- 注册表主体（risk/issue/requirement/待办文件）：按条数触发（30-50 条）→ 按类别/状态拆分
- 日志型文件（transfer-log/decision-log）：按条数触发（30-100 条）→ 按时间拆分
- 目录型文件（snapshots/outputs/daily-reports）：按时间触发（90 天）→ 年度归档
- ATOM 类别文件 `{category}.md`：超 300 行 → 按 source_type 分片（如 `technical-design_spec.md`），并新增对应 L2 `{category}-index.md` 分片条目
- Canonical 文件：超 50 条 → 按 scope_scope/类别拆分
- project-notes：超 100 条 / 6 个月 → 季度归档到 `context/project-notes-archive/`
- 所有归档后必须维护索引

## 10. 安全规则
1. 不得在文件中记录密码、密钥、Token 等凭证。
2. 涉及客户敏感信息时使用脱敏代号。
3. 不得删除或覆盖状态为"已确认"的文件，只能新增版本。

## 11. PM Profile 文件规范

| 模式 | 路径 | 说明 |
|---|---|---|
| portfolio | `ai/portfolio/context/pm-profile.md` | 项目集级 PM 偏好档案 |
| single | `ai/context/pm-profile.md` | 单项目 PM 偏好档案 |

规则：文件不存在时降级跳过（不视为错误）；初始化时自动创建；旧工作区可 `migrate_workspace.py --create-profile` 补建；已存在不覆盖；pending 偏好不按 confirmed 应用；每条记录保留 Source。详见 `references/21-pm-profile-rules.md`。
