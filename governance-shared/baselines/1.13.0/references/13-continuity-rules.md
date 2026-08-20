# 项目阶段衔接规则

本规则用于支持大项目分阶段管理场景。当一个大项目被拆分为多个阶段，且每个阶段可能存在独立 `ai/` 工作区时，AI 必须能够根据用户提供的历史 `ai/` 目录、历史文件、上传材料或口述内容，将历史阶段与当前阶段进行衔接。

---

## 1. 核心原则

1. **历史阶段内容不得直接等同于当前阶段事实源。**
2. 历史内容必须先登记为 legacy source。
3. 历史内容必须经过映射和结转判断。
4. 未经用户确认，不得将历史风险、问题、需求、任务、预算、里程碑直接写入当前事实源。
5. 默认不得覆盖当前阶段已有文件。
6. 历史日报、周报、会议纪要等过程材料默认只引用或摘要，不整体迁入当前阶段。
7. 只结转仍有效、未关闭、需沿用、会影响当前阶段的内容。
8. 所有历史导入动作必须记录到 `ai/continuity/import-log.md`。

---

## 2. 与"计划批量导入"(R1) 的边界判定

本文件（13）处理**跨阶段/跨工作区**的历史衔接。R1（历史计划批量导入）处理**当前工作区内**的存量计划（.pod / Excel 等外部载体）回溯灌入快照。

当收到一份历史计划材料时，按以下判定表决定走哪条规则：

| 判定条件 | 处理规则 | 说明 |
|---|---|---|
| 材料是历史 `ai/` 目录 / 上一阶段的工作区 | **13 号**（本文件） | 按 legacy source 流程衔接 |
| 材料是当前项目的存量计划（.pod / Excel / 遗留 board 导出），无独立历史工作区 | **15 号 + 03 号**（R1） | 走 external_import 批量导入快照（见 `15-snapshot-rules.md` §8a） |
| 材料含"计划 + 已完成记录"，需回溯灌入快照 | **R1** | 生成 imported-{date}.md 冻结快照 + 登记 board |
| 材料是跨阶段衔接（沿用需求/风险/进度） | **13 号** | carryover 流程 |
| 用户表达"上一阶段""一期""承接"等 | **13 号** | 触发历史衔接（见 §3） |
| 用户表达"批量导入历史计划""灌入快照""把现有计划同步进来" | **R1** | 触发批量导入（见 `15-snapshot-rules.md` §8a） |

**关键区别：**
- 13 号：存在"历史阶段"这个独立主体，需 legacy-sources / carryover / 确认后写入当前阶段。
- R1：同一工作区内的存量计划，直接固化到快照体系，无阶段边界、无 legacy 登记，不产生 carryover。

两套流程共用"确认后写入"的安全底线，但不共用登记册与目录。

---

## 3. 衔接目录

当前阶段工作区维护 `ai/continuity/`：

```
ai/continuity/
├── project-lineage.md       # 阶段谱系
├── legacy-sources.md         # 历史来源登记
├── import-plan.md            # 导入计划
├── continuity-map.md         # 历史到当前的映射关系
├── carryover-register.md     # 结转事项登记册
├── delta-analysis.md         # 差异分析
└── import-log.md             # 导入日志
```

---

## 4. 触发表达

当用户输入包含以下表达时，必须触发历史衔接流程：

| 触发词 | 说明 |
|---|---|
| 导入历史项目 / 导入上一阶段 | 历史导入 |
| 衔接上一阶段 / 接续上一期 / 承接上一阶段 | 阶段衔接 |
| 把一期内容接过来 / 把历史 ai 合并进来 | 目录合并 |
| 这是旧项目的 ai 目录 / 这是上一阶段的 ai 文件 | 目录/文件识别 |
| 把之前的风险接上 / 把上一阶段遗留问题带过来 | 结转事项 |
| 把历史需求继承过来 / 沿用上一阶段决策 | 继承 |
| 把旧项目内容迁移到当前项目 | 迁移 |
| 基于上一阶段继续做 / 当前项目是二期 / 上一期的延续 | 阶段识别 |
| 历史遗留 / 结转事项 | 通用触发 |

### 隐式触发

当用户上传或粘贴文件，文件名/内容出现"一期""二期""上一阶段""历史""遗留""结转""沿用""承接""延续"等词时，AI 应主动询问是否需要启动历史衔接流程。

---

## 5. 支持的输入方式

| 输入方式 | 说明 | AI 处理 |
|---|---|---|
| 历史 `ai/` 目录路径 | 用户提供路径如 `D:/市监一期/ai` | 扫描目录结构，读取 .skill-version.json 和各事实源 |
| 压缩包/文件夹 | 用户上传打包文件 | 解压后识别 ai/ 目录结构 |
| 单个或多个文件 | 逐个上传 Markdown 文件 | 按文件名和内容自动识别类型并登记 |
| 用户粘贴文本 | 口述历史背景 | 提取关键信息作为历史来源入库候选 |
| 历史 Excel/Word | 导出的历史报告 | 解析内容，提取结构化事项 |

---

## 6. 导入模式

| 模式 | 说明 | 适用内容 |
|---|---|---|
| `reference_only` | 只建立引用，不导入事实源 | 历史周报/日报/会议纪要 |
| `summarize_merge` | 摘要合并到当前上下文 | 项目背景/经验教训/技术约束 |
| `carryover_open_only` | 仅结转未关闭事项 | open 风险/问题/未完成任务 |
| `selective_import` | AI 提取候选项，用户确认后导入（默认模式） | 需求/决策/资源/预算/里程碑 |
| `full_migration_plan` | 生成完整迁移计划但不执行 | 全量迁移场景 |

> 注：R1（计划批量导入）不使用本表模式，其导入方式见 `15-snapshot-rules.md` §8a。

---

## 7. 内容路由表

| 历史内容 | 默认处理方式 | 当前阶段目标 |
|---|---|---|
| 项目背景 | `summarize_merge` | `context/project-context.md` |
| 已确认需求 | `selective_import` | `requirements/requirement-register.md` |
| 需求变更记录 | `reference_only` | `requirements/change-log.md` |
| 未完成任务 | `carryover_open_only` | `tasks/backlog.md` |
| 未关闭风险 | `carryover_open_only` | `risks/risk-register.md` |
| 未关闭问题 | `carryover_open_only` | `issues/issue-register.md` |
| 历史决策 | `summarize_reference` | `decisions/decision-log.md` |
| 里程碑 | `selective_import` | `milestones/milestone-board.md` |
| 预算/P&L | `selective_import` | `plans/budget.md` |
| 人员资源 | `selective_import` | `portfolio/resources/resource-register.md` |
| 人员流转 | `reference_only` | `portfolio/resources/transfer-log.md` |
| 经验教训 | `summarize_merge` | `reviews/lessons-learned.md` |
| 周报/月报 | `reference_only` + 摘要 | `continuity/delta-analysis.md` |
| 日报 | `reference_only` | 一般不导入 |
| 会议纪要 | `reference_only` + 抽取决策/行动项 | `decisions/`、`tasks/`、`risks/`、`issues/` |

---

## 8. 衔接流程

```
用户触发（给路径/传文件/口述）
  → 登记 legacy-sources.md
  → 读取历史内容，识别类型
  → 生成 import-plan.md（导入范围）
  → 生成 continuity-map.md（映射关系）
  → 提取结转候选 → carryover-register.md
  → 生成 delta-analysis.md（差异分析）
  → 用户确认结转事项
  → 确认后写入当前阶段事实源
  → 记录 import-log.md
```

**核心链路：** 历史内容 → 登记 → 映射 → 结转 → 确认 → 写入当前事实源

不得跳过确认步骤直接写入。

---

## 9. 结转事项登记册

`carryover-register.md` 是衔接流程的核心文件。所有可能影响当前阶段的历史事项必须先进入此文件，经用户确认后才能写入当前阶段事实源。

### 字段

| Carryover ID | Type | Source Stage | Source Ref | Title | Summary | Target Project | Target File | Carryover Status | Confirmation Status | Owner | Due Date | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Carryover Status

- `candidate`：AI 提取的候选
- `pending_import`：等待导入
- `imported`：已导入当前事实源
- `merged`：已合并到当前已有事项
- `referenced`：仅建立引用
- `ignored`：用户选择忽略
- `duplicate`：与当前事项重复
- `cancelled`：取消

### Confirmation Status

- `pending_confirm`：等待用户确认
- `confirmed`：已确认
- `rejected`：已拒绝
- `needs_more_info`：需要更多信息

---

## 10. 冲突检测

当历史事项与当前阶段已有事项相似时，AI 不得重复写入，必须提示冲突并请求用户确认。

冲突处理选项：

1. 合并到当前已有事项（历史来源作为 Source 补充）
2. 作为独立事项导入
3. 仅建立历史引用
4. 标记为重复并忽略
5. 暂缓，等待更多信息

---

## 11. 不可覆盖规则

**历史导入默认不得覆盖当前阶段已有文件。**

| 操作 | 是否允许 |
|---|---|
| 新增历史来源记录 | 允许 |
| 新增结转候选 | 允许 |
| 追加历史摘要 | 允许 |
| 生成导入建议 | 允许 |
| 经确认后追加到当前事实源 | 允许 |
| 覆盖当前事实源 | 禁止 |
| 删除当前事项 | 禁止 |
| 将历史状态直接替换当前状态 | 禁止 |
| 未确认即关闭或批准事项 | 禁止 |

---

## 12. 版本兼容

若历史工作区存在 `.skill-version.json`，AI 应比较历史版本和当前版本。如版本或 workspace schema 不一致，先生成结构映射建议，不得直接复制历史文件。

---

## 13. ID 规则

| 前缀 | 含义 | 格式 |
|---|---|---|
| LEG-NNN | 历史来源 | LEG-001 |
| IMP-YYYYMMDD-NNN | 导入批次 | IMP-20260809-001 |
| CO-NNN | 结转事项 | CO-001 |
| STG-NNN | 阶段 | STG-001 |

> R1 批量导入使用 `imported-{date}.md` 命名与 `external_import` source_type（见 `15-snapshot-rules.md`），不使用 LEG/CO 前缀。

---

## 14. 项目集模式适配

- 历史是单项目 → 导入到 `ai/projects/{project}/...`
- 历史是项目集 → 导入到 `ai/portfolio/...` + `ai/projects/{project}/...`
- 历史项目名与当前不一致 → 通过 `project-index.md` 建映射

---

## 15. 输出格式

触发历史衔接流程时，AI 输出：

```markdown
## 历史衔接意图识别

- 输入类型：[目录/文件/口述/压缩包]
- 历史阶段：[阶段名]
- 当前阶段：[阶段名]
- 目标范围：[项目集/子项目]
- 建议导入模式：[模式]
- 版本差异：[有/无]

### 建议读取/解析内容

| Source | Purpose | Priority |
|---|---|---|

### 初步结转候选

| Type | Title | Source | Target | Need Confirmation |
|---|---|---|---|---|

### Suggested File Updates

| Target File | Update Type | Suggested Change | Need Confirmation |
|---|---|---|---|
```

---

## 16. 与其他规则的关系

| 规则 | 衔接时的职责 |
|---|---|
| `10-update-trigger-rules.md` | 识别历史导入触发词 |
| `06-file-rules.md` | 不可覆盖规则、continuity/ 目录管理 |
| `05-query-rules.md` | 历史/遗留事项查询路由 |
| `11-output-artifact-rules.md` | 阶段衔接报告输出到 outputs/ |
| `09-portfolio-rules.md` | 项目集模式下的资源/里程碑衔接 |
| `15-snapshot-rules.md` | R1 计划批量导入（external_import）的执行方 |
