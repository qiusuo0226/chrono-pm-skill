# 查询约束规则

本规则适用于用户查询项目状态时的信息检索和回答规范。

---

## 1. 查询处理流程

```
用户提问 → 判断问题类型 → 按路由表加载对应提示词 → 读取相关事实源 → 前置检查 pending-changes.md（见 §1a） → 读取相关事实源 → 按时间或ID定位过程记录 → 输出结论+信息来源+不确定项+冲突标注
```

### 1a 待确认变更前置检查

查询处理前（读取事实源之前），先检查 `pending-changes.md` 是否存在待确认项（单项目 `ai/pending-changes.md`，项目集 `ai/portfolio/pending-changes.md`）：

- `total_pending > 0` 时，在查询结果正文之前输出"**存在 N 项待确认变更**"提醒区块，逐条列出原值/新值（含 Change Log 指针、Change Summary、Risk Level）。
- 查询数据中与待确认变更直接相关的条目，在正文数据后标注 `(待确认)`。
- 若本轮即处理待确认项（PM 在确认/驳回），则不重复输出提醒区块。
- 简单查询不加载 `pending-changes.md`（见 §6.3），仅执行确认/驳回/管理待确认项，或查询结果受待确认变更影响时加载。

## 1.5 查询术语归一化

查询处理流程增加前置步骤：读 `ai/portfolio/context/domain-glossary.md`（如存在）→ 扫提问中的术语缩写 → 仅 `confirmed` 映射替换（`pending` 输出提示"按候选理解"）→ 按标准名称进入路由表 → 正常查询流程。

**示例：** 用户问"农专注销进度"；"农专"为 confirmed，映射为"农民专业合作社"，按"农民专业合作社+注销"路由到任务/风险/里程碑查询。

---

## 2. 问题类型与路由

| 问题类型 | 示例 | 需读取的事实源 |
|----------|------|----------------|
| 进度查询 | "项目进展怎么样？" | tasks/board.md, milestones/milestone-board.md, plans/progress-plan.md |
| 风险查询 | "当前有哪些高风险？" | risks/risk-register.md |
| 问题查询 | "有什么阻塞？" | issues/issue-register.md, tasks/board.md（blocked状态） |
| 任务查询 | "张三在做什么？" | tasks/board.md（按 Owner 筛选） |
| 需求查询 | "需求完成多少了？" | requirements/requirement-register.md |
| 成本查询 | "预算执行情况？" | plans/budget.md |
| 决策查询 | "上次为什么决定用A方案？" | decisions/decision-log.md |
| 里程碑查询 | "M02什么时候能过？" | milestones/milestone-board.md, tasks/board.md（按 Milestone Ref 筛选） |
| 周报查询 | "本周周报呢？" | reports/weekly/ 当前周文件 |
| 资源查询 | "团队有几个人？""张三现在在哪个项目？" | portfolio/resources/resource-register.md, transfer-log.md |
| 资源流转查询 | "张三什么时候调走的？""本周人员变动" | transfer-log.md（按日期筛选） |
| 跨项目查询 | "三个项目整体进度如何？""哪个项目风险最高？" | ai/portfolio/ 下各子项目汇总 + portfolio/resources/ |
| 计划变更计数 | "XX 变更了几次？" | tasks/board.md（Plan Change Count，单文件） |
| 延期计数 | "XX 延期了几次？" | tasks/board.md（Delay Count，单文件） |
| 超期状态 | "现在哪些任务超期了？""还有什么没做完的？" | tasks/board.md + 预建索引（见 §6.5/§6.6） |

### 2.0a 查询默认过滤行为

任务/待办类查询（"XX 在做什么""还有什么没做完""任务列表"）默认仅输出**未完成项**（Status ≠ done / cancelled）。用户明确说"全部""含已完成""所有任务"时输出全部。

### 2.1 项目集模式查询路由

项目集模式下按触发条件判断查询范围：

| 触发条件 | 查询范围 | 路由动作 |
|---|---|---|
| 提到具体子项目名（「全链通」「企业通」） | 单子项目 | 读 `ai/projects/{子项目}/` 对应事实源 |
| 提到「整体」「所有项目」「全局」「项目集」 | 项目集级 | 读 `ai/portfolio/` 汇总 + 各子项目关键事实源 |
| 提到「人员」「资源」「人手」「团队」 | 资源级 | 读 `portfolio/resources/resource-register.md` + `transfer-log.md` |
| 提到「成本」「预算」「P&L」且未限定子项目 | 项目集成本 | 读各子项目 `plans/budget.md` + `portfolio/plans/budget-summary.md` |
| 未限定且无法判断 | 项目集级（默认） | 提示确认范围，或默认返回项目集整体概要 |

**跨项目对比查询：** 逐个读取各子项目事实源 → 按统一维度汇总成对比表 → 标注各子项目数据截止时间（统一基准）→ 标注数据缺失项。

---

## 2.5 快速查询路由（Quick Query Routing）

用户提待办/计划/进展类查询时，AI 必须优先读取索引文件，不得默认全量扫描日报、会议纪要和历史文件。

### PM 待办查询输出规范

PM 问"我明天的待办""明天做什么"时，AI 必须输出 **PM 全景待办视图**（非仅个人任务），缺一不可的 9 章节：

| # | 章节 | 内容要点 |
|---|------|----------|
| 1 | PM 直接任务 | PM 本人需亲自完成的任务 |
| 2 | 全团队明日计划 | 按子项目分组，含进度、关联里程碑、风险标记 |
| 3 | 需重点跟进的风险 | open 高/中风险，含今日变化和建议动作 |
| 4 | 需重点跟进的问题 | 未关闭问题，含是否延期和建议动作 |
| 5 | 里程碑进度 | 各子项目当前里程碑偏差和阻塞项 |
| 6 | 资源变动提醒 | 请假/借调/离场人员及其影响 |
| 7 | 本周计划对照 | 本周计划项是否按计划推进 |
| 8 | 待协调事项 | 跨项目/需管理层协调的事项 |
| 9 | 无计划项提醒 | 明确标注哪些子项目/人员无直接计划项 |

输出模板见 `assets/templates/pm-daily-todo-template.md`。

**数据读取路径（按优先级）：** ①`personal-todo-index.md`（PM 待办）→ ②`daily-todo-index.md`（全团队）→ ③各子项目 `tasks/board.md`（进度）→ ④`risks/risk-register.md`（open 风险）→ ⑤`issues/issue-register.md`（未关闭问题）→ ⑥`milestones/milestone-board.md`（里程碑）→ ⑦`portfolio/resources/resource-register.md`（资源变动）→ ⑧各子项目最近日报索引 → ⑨各子项目最近会议纪要。

**禁止行为：** 只列 PM 个人任务就结束；不读任务看板就答"没有相关任务"；不展示团队成员明日计划。

### Quick Query 路由表

| 用户问题 | 优先读取 | 兜底读取 | 禁止 |
|---|---|---|---|
| 我明天/今天的待办 | `personal-todo-index.md` + `daily-todo-index.md` | 相关项目 `tasks/board.md` + 最近日报索引 | 全量扫描所有日报/会议 |
| 明天大家做什么 | `daily-todo-index.md` | `projects/*/tasks/board.md` | 创建临时脚本扫描 |
| 本周重点是什么 | `weekly-todo-index.md` | 最近周报 + 任务看板 | 全量扫描历史周报 |
| 某人的任务 | `personal-todo-index.md`（按 Owner 筛选） | `projects/*/tasks/board.md` | 逐日扫描该人日报 |
| 项目进展如何 | `tasks/board.md` + `milestones/milestone-board.md` | 最近日报索引 | 全量扫描所有过程记录 |
| 当前风险 | `risks/risk-register.md`（open） | 最近周报 | 全量扫描历史周报 |
| 当前问题 | `issues/issue-register.md`（未关闭） | `tasks/board.md`（blocked） | 全量扫描历史日报 |
| 资源情况 | `portfolio/resources/resource-register.md` | `transfer-log.md` | - |
| 变更了几次/延期了几次 | `tasks/board.md`（Plan/Delay Count，单文件） | Change Log（计数缺失时） | 扫描快照/日报 |
| 现在哪些任务超期 | `tasks/board.md` + 预建索引（daily-todo-index） | 最近日报索引 | 扫描日报原文 |
| 某需求在不在合同/招投标/立项范围内（范围判定） | `contract-register.md`（Step0 前置路由）→ `requirements/atoms/atom-index.md`(L1) → 目标 `{category}-index.md`(L2) → 命中 ATOM 全文(L3) → `requirements/canonical/canonical-index.md` | 命中 ATOM 全文(L3) → `canonical-index.md` | 全量扫描所有 ATOM/category 文件 |
| 某需求在不在合同 N 范围内（指定合同） | `contract-register.md` 定位合同 scope_level → 对应层级（portfolio 或子项目）`canonical/` + 三级索引 | 直接进子项目 atoms/canonical | 全量扫描所有 ATOM/category 文件 |

### Quick Query 路由注：RI 范围判定四步路由（CR-20260813-002）

跨源范围判定查询（"XX 需求在不在 X 范围内"）必须按**四步路由**执行，对齐 §6.1 最小读取。合同与子项目为多对多关系，先经 contract-register 定位层级，再走三级索引：

- **Step 0 读 contract-register**：读取合同登记册（位置：项目集 `portfolio/requirements/contract-register.md`；单项目 `requirements/contract-register.md`）。**登记册为空 → 触发补录引导**（最小字段：ID/名称/scope_level/覆盖/status），不返回臆造结论（D5）。合同登记册结构见 07 号 §8.9。
- **Step 1 解析合同指向**：
  - 用户指定合同（CON-XXX 或合同名）→ 查该合同 scope_level：`portfolio` → 搜 `portfolio/requirements/canonical/`；`project` → 搜对应子项目 canonical；`supplement` → 经 `parent_contract_id` 回溯父合同 scope_level 后按父合同层级路由（D7）。
  - 用户未指定合同 → 先列出 contract-register 中所有合同候选供用户选择；或按"全部范围"逐合同检索后合并、按合同标注各结论。
  - 登记册为空/无匹配合同 → 提示补录，不臆造。
- **Step 2 目标层级三级索引加载**（对齐原三级索引）：
  1. 加载 L1 `{目标层级}/atoms/atom-index.md`（路由表，~6 行）→ 判断搜索哪些 category。
  2. 加载目标 `{目标层级}/atoms/{category}-index.md`（L2 类别倒排，含 `norm_text` 摘要覆盖索引）→ keyword + 语义扫读定位候选。
  3. 仅加载命中的 ATOM 全文（L3，3-5 条）→ 看 raw_text + evidence。
  4. 关联 `{目标层级}/canonical/canonical-index.md` → scope_scope + 证据链。
- **Step 3 输出带合同维度的结论**：返回 `scope_scope(result)` + `contract_refs`（关联合同 ID 列表）+ 证据链。场景 G（子项目被多合同覆盖）→ 逐合同列结论；`supplement` 结果含补充协议与父合同双 ID。

单次范围判定总加载约 200-400 行，不加载未命中 category 文件。**P1 语义兜底**：查询前查 17 号词库扩展同义词；未命中时用 L2 norm_text 摘要语义扫读；仍无果输出降级提示（换关键词 / 查词库同义词 / P2 向量增强），不臆造结论。

### Quick Update 路由表

用户提待办/状态/进展类更新时，AI 必须按 WF 路径执行，不得逐步临时推导。
> ⚠️ 写入动作仍须遵循 SKILL.md §7 安全底线第 2 条（事实源写入待人工确认 + pending-changes 登记），不因路由预定义而绕过确认环节。

| 用户指令 | WF 路径 | 核心读文件 | 核心写文件 | 禁止 |
|---|---|---|---|---|
| 更新某人的待办/状态 | WF-1 | personal-todo-index + board + issue/risk-register | todo-index + board + register + pending-changes | 不加载 01/06/10 规则文件 |
| 提交日报/个人进展 | WF-2 | project-context + board | 日报 + todo-index + 快照 | 不跳过待办索引同步 |
| 提交会议纪要 | WF-3 | 纪要原文 + board + register | 纪要归档 + 事实源建议清单 | 不跳过行动项提取 |
| 需求变更 | WF-4 | requirement-register + board | change-log + 影响分析 | 不跳过影响分析 |
| 写周报/生成周报 | WF-5 | project-index + 各子项目事实源 | 周报 + 项目集汇总周报 | 不遗漏子项目 |
| 人员变动/资源流转 | WF-6 | resource-register + board | transfer-log + register + todo-index | 不自动改 register（须确认） |

### 查询性能规则

1. 查询类请求必须优先读取索引文件。
2. 不得默认扫描全部日报、会议纪要、周报和历史文件。
3. **不得为简单查询默认创建临时脚本扫描目录。**
4. 查询优先读取最近时间范围：待办=今天/明天/本周；日报=最近 7 天或当前 `YYYYMM` 索引；周报=最近 2 周；会议=最近 5 次索引；风险/问题=当前 open。
5. 索引缺失时提示用户是否重建，不自行全量扫描。
6. 仅当用户明确要求"全面回顾/追溯/从历史中找"时才扩大扫描范围。

### Historical Todo Query Routing（历史计划查询）

查询历史计划/往日计划/实际完成/计划偏差时，**不得扫描个人日报**，必须优先读取计划快照与实际执行摘要。

**触发词：** 往日计划、历史计划、过去某天、之前某天、某月某日原计划、实际完成、计划完成情况、计划偏差、计划有没有完成、上周计划对照、某人上周每天计划。

**查询顺序：** ①读 `ai/portfolio/todos/history-index.md` → ②定位 `snapshots/daily/{date}.md` 或 `snapshots/weekly/{week}.md` → ③查实际完成读 `actuals/` 对应文件 → ④快照/摘要不存在则读对应月日报索引 → ⑤用户确认后才允许扫描日报明细。

| 用户问题 | 读取路径 |
|---|---|
| 8月10日大家原计划做什么 | `history-index.md` → `snapshots/daily/20260809.md` |
| 8月10日实际做了什么 | `actuals/daily/20260810.md` |
| 8月10日计划完成了吗 | `snapshots/daily/20260809.md` + `actuals/daily/20260810.md` |
| 上周计划偏差 | `snapshots/weekly/{week}.md` + `actuals/weekly/{week}.md` |
| 某人过去一周每天计划 | `history-index.md` → 多个 daily snapshots |
| 导入的那批计划 | `history-index.md` → `snapshots/daily/imported-{date}.md` |

**热/冷数据分离：** `daily-todo-index.md` 只存近期热数据（过去 7 天 + 未来 14 天），更早历史转向 `history-index.md` + `snapshots/` + `actuals/`。详见 `15-snapshot-rules.md`。

### 索引缺失时的处理

发现快速待办索引缺失时，提示"我建议先重建待办索引"，可扫描范围：当前任务看板、最近 7 天日报索引、最近 5 次会议纪要、本周计划/周报，并询问是否现在重建。

### 禁止默认临时脚本规则

简单查询不得默认创建临时脚本（.js/.py/.sh）扫描目录。简单查询包括：今天/明天/本周待办、某人任务、当前风险/问题、项目进展、本周重点、哪些问题未关闭、变更/延期计数。**必须优先读索引和事实源**，仅以下情况允许脚本：①用户明确要求全量扫描/统计大量文件；②索引缺失且用户确认允许扫描重建；③复杂数据分析需编程处理。

---

## 3. 信息检索优先级

1. 优先读事实源文件（board/register/log）——当前状态真实来源。
2. 事实源无信息再查过程记录（日报、会议纪要）。
3. 过程记录与事实源矛盾时以事实源为准，但须标注矛盾并提示项目经理确认。
4. 记忆有而事实源无的信息须标注"记忆中有但事实源中未记录"。

### (3)a 里程碑终态事件豁免

当过程记录（日报、会议纪要、评审记录）中包含**里程碑级终态事件**（如"评审通过""验收通过""测试通过""上线完成""联调通过""集成验证通过"等，完整列表见 `00-pm-main-rules.md` §10.2）且该事件结论与事实源（任务板）状态矛盾时：

1. **不适用**本条 (3)"以事实源为准"规则。
2. AI 应：
   - 基于过程记录中的终态事件推导结论（推导链见 `00-pm-main-rules.md` §10.3）；
   - 在输出中标注矛盾："⚠️ 任务板显示 {状态A}，但 {过程记录} 记录 {终态事件}，推导为 {结论}"；
   - 输出 SUGGEST 建议同步任务板状态（走 `00-pm-main-rules.md` §8a 强制呈现）。
3. 推导结论**不直接修改**事实源，仅通过 SUGGEST 建议同步。
4. 项目可在 `context/entity-registry.md` §3 扩展终态事件列表。

此豁免确保推导基线（`00-pm-main-rules.md` §10）能正常生效，不被本条 (3) 压制。

## 4. 回答规范

### 4.1 输出结构

```
# [标题]
## 1. 回答正文（直接回答，结构化呈现）
## 2. 信息来源（[来源]：文件路径+章节/行号）
## 3. 不确定项（原因/影响 + 缺失信息需补充什么）
```

### 4.2 回答原则

先结论后展开；状态/进度/成本用表格呈现；每个关键数据点标注来源；信息矛盾不可隐藏须显式标注；信息不足直接说明"当前事实源中无此信息"不推测填充；**查询类回答不输出"建议更新清单"**（除非用户明确要求"帮我更新"）。聚合计数/超期查询除遵循本节外，另见 §6.5/§6.6 及输出模板 `delay-stats-template.md`。

---

## 5. 特殊查询处理

### 5.1 项目健康度查询

"项目健康吗？"按以下维度评估：

| 维度 | 评估指标 | 数据来源 |
|------|----------|----------|
| 进度健康 | 里程碑偏差、任务延期率 | milestones/, tasks/ |
| 成本健康 | CPI、预算执行率 | plans/budget.md |
| 风险健康 | 高/极高风险数量 | risks/risk-register.md |
| 质量健康 | 未解决问题数、P0/P1问题数 | issues/issue-register.md |
| 范围健康 | 需求变更次数、未确认需求数 | requirements/ |

**输出格式：** `项目健康度评估` 表（维度|状态🟢🟡🔴|指标|说明）→ `总体判断`（一段话）→ `需关注事项`。**状态判定：** 🟢 正常=偏差在容忍度内；🟡 关注=接近容忍度上限；🔴 预警=超出容忍度。

### 5.2 管理层摘要查询

"给一版管理层汇报"时输出结构化摘要，聚焦：里程碑进展、关键风险（高及以上）、关键问题（未解决 P0/P1）、成本偏差（CPI）、需管理层决策事项。

### 5.3 历史追溯查询

问"某个需求/任务/决策的历史"时：先查事实源当前记录 → 再查事实源底部 Change Log → 最后查过程记录（日报、会议纪要）→ 按时间线输出变更历程。

**待确认口径：** `Confirmed By: 待确认` 的记录**不进入**已确认口径的追溯结论（不计入"已确认的变更次数/确认生效的决策"），逐条标注"待确认"；已确认记录按正常口径输出。追溯路径适配 Change Log 分层归档：优先查活跃区 → `change-log/index.md` 导航 → 按月归档 `change-log/archive/YYYYMM-change-log.md`。

### 5.4 资源查询处理

| 查询意图 | 读取文件 | 输出格式 |
|---|---|---|
| 当前团队全貌 | `portfolio/resources/resource-register.md` | 按子项目分组的资源表格（姓名/角色/状态/分配方式） |
| 某人当前状态 | `resource-register.md`（按姓名） | 单人信息卡（角色/所属项目/分配方式/B角/风险等级） |
| 某人流转历史 | `transfer-log.md`（按姓名） | 时间线（流转日期/类型/来源项目/目标项目/原因） |
| 本周人员变动 | `transfer-log.md`（按日期本周） | 流转记录表 + 影响分析 |
| 项目人手是否足够 | `resource-register.md`（按项目）+ 09 容忍度规则 | 人力配置表 + 容忍度评估 + 风险提示 |

**资源查询回答原则：** ①当前状态以 `resource-register.md` 为准、流转历史以 `transfer-log.md` 为准；②某人状态为「借出/休假」须同时显示 B 角；③触发资源容忍度风险规则（见 09）须在末尾标注「资源风险触发」；④流转类型按 9 种分类显示（见 09）。

### 5.4a 人员查询事实源优先级

人员查询须遵循来源优先级，不得默认合并搜索多文件：

| 优先级 | 数据来源 | 用途 | 说明 |
|---|---|---|---|
| 1（主源） | `portfolio/resources/resource-register.md` | 人员当前状态 | 查询状态默认只读此文件 |
| 2（历史） | `portfolio/resources/transfer-log.md` | 流转历史追溯 | 仅查历史变动时读取 |
| 3（投影） | `projects/{子项目}/context/project-context.md` | 项目背景团队列表 | 是 register 投影，非独立事实源 |
| 4（候选） | `reports/daily/personal/` 日报目录 | 参与信号/候选证据 | 只能产生候选变更，不能自动认定为正式成员 |

**查询规则：** ①"某项目有哪些人/某人在哪/团队几人"默认只读 `resource-register.md`，不主动扫日报/transfer-log/project-context；②"参与子项目"字段存在且包含目标项目则直接返回；③字段为空/不存在（旧工作区）可从 `transfer-log.md` 推断但**标注"推断，未确认"**；④register 不存在则读 `project-context.md`，标注来源与可能不准确；⑤register 和 context 均不存在才扫日报目录，标注"候选名单，未经确认"；⑥全无数据则输出"无法确定人员信息，建议初始化 resource-register.md"，不编造；⑦**禁止**：不得将日报出现过的人员自动认定为正式成员，不得未经确认自动修改 register。

### 5.5 项目集健康度查询

"项目集整体健康吗？"在单项目基础上增加：资源健康（各子项目人力配置率、关键岗位缺口）、跨项目风险（数量、依赖阻塞）、整体 P&L（总成本偏差、各子项目 CPI 对比）、人员流转（本周流转次数、流出未补充人数）。输出为各子项目健康度对比表 + 项目集整体评估。

---

## 6. 最小读取原则（全局规则）

### 6.1 原则

先按问题判断最小文件集合；简单查询只读 1-2 个数据文件；不因存在路由表/参考资料而默认全量加载；不得枚举 ai/、references/、projects/ 目录；不在简单查询中读完整 SKILL.md 或 references/ 规则文件。

### 6.2 简单查询 vs 复杂任务

| 类型 | 判断标准 | 文件读取规则 |
|---|---|---|
| 简单查询 | 版本/待办/风险列表/项目概况/日报提交状态/变更·延期计数 | 最多读 1-2 个数据文件；超 3 个须说明原因 |
| 复杂任务 | 日报处理/周报生成/风险评估/变更分析/需求评审 | 可读多文件，但须列出读取清单 |

### 6.3 快捷查询文件映射

| 查询意图 | 直接读取文件 | 跳过的环节 |
|---|---|---|
| 版本查询 | ai/.skill-version.json | 不读 SKILL.md、不读 06-file-rules |
| 待办查询 | 优先 `personal-todo-index.md`；可辅读 `daily-todo-index.md` | 不读 SKILL.md、不读 01-daily-report-rules |
| 风险列表 | `portfolio/risks/risk-register.md` 或 `projects/{子项目}/risks/` | 不读 SKILL.md、不读 04-risk-issue-rules |
| 项目概况 | `portfolio/context/project-brief.md` 或 `projects/{子项目}/context/` | 不读 SKILL.md、不读 06-file-rules |
| 人员状态 | `portfolio/resources/resource-register.md` | 不读 SKILL.md、不读 09-portfolio-rules |
| 变更/延期计数 | `tasks/board.md`（单文件） | 不读 SKILL.md、不扫快照/日报 |

**最小读取补充（B-17）：** 简单查询**不加载** `pending-changes.md`；仅当执行待确认项的确认/驳回/管理，或查询结果受待确认变更直接影响（需标注 `(待确认)`）时才加载该索引文件。

### 6.5 聚合计数路由（A 类：计划变更/延期计数）

用户问"XX 变更了几次""XX 延期了几次""谁延期最多"等**聚合计数**问题时：
1. 只读 `tasks/board.md` **单文件**，按字段聚合：`Plan Change Count`（按人/任务）、`Delay Count`（按人）。
2. **不扫描** `snapshots/`、`actuals/`、日报或创建临时脚本（对齐 §6.1 最小读取 + 禁止临时脚本规则）。
3. 若 board 计数字段缺失/为 0（旧工作区），回退到 board 底部 Change Log 统计并在输出标注"推断，未确认"。
4. 输出按人/按任务的计数表，标注数据来源为 `tasks/board.md`（采用 `assets/templates/delay-stats-template.md` 结构）。

**待确认口径（B-18）：** `Confirmed By: 待确认` 的记录**不参与**"已确认的计划变更次数 / 延期次数"聚合统计；聚合正文数据后，与该类记录直接相关的条目标注 `(待确认)`，使其与已确认计数区分。

### 6.6 状态查询路由（B 类：超期判定）

用户问"现在哪些任务超期了""项目进度怎么样了""还有什么没做完/超期"等**状态判定**问题时，**实时计算**（非仅日报处理时）：
1. 读取 `tasks/board.md`（当前 Due Date / Owner / Status / 计划变更确认状态）。
2. 读取预建索引（`daily-todo-index.md` / `personal-todo-index.md`）取最近完成状态——**不得临时扫描日报原文**。
3. 当前有效 Due Date 与今天对比：确认窗口期内（新变更未确认）按旧版 Due Date 判定；换人场景交接前归原 Owner（判定规则见 `references/03-task-board-rules.md` §5a）。
4. 若索引 >24h 未更新，先提示"索引过期，建议重建"，不拿过期数据当结论。
5. 输出超期清单 + 归属 + 预警项；**不写入 Delay Count 计数器**（计数与状态判定分离）。

**待确认口径（B-18）：** `Confirmed By: 待确认` 的 Due Date 视为**未确认计划**，**不参与**"已确认计划延期/超期"判定与已完成统计；在状态判定正文数据后标注 `(待确认)` 逐条提示（含原值 vs 新值）。存量 board 无 `Confirmed By` 的行按"已确认"处理。

### 6.7 WP 分层查询与倒排倒计时路由

用户问"ITR-01 进度怎么样""本周计划做什么""今天做什么""WP-ITR01-01 做了没""倒排还剩几天"等**计划分层/倒计时**问题时：

| 查询场景 | 数据访问 | 输出 |
|---|---|---|
| 迭代整体进度（ITR-NN） | 读 `plans/iteration-register.md` 对应迭代 WP 表 + board 按 WP Ref 聚合 | WP 列表 + 各 WP 进度 + 迭代总进度 |
| 某 WP 进度（WP-ITRNN-NN） | board 单文件按 WP Ref 过滤（实时聚合，不读迭代详情） | Task 列表 + 完成比例 |
| 今天做什么 | 优先读 `daily-todo-index.md` 热索引；溯源时按 Due Date = 今天过滤 board | 当日 Task 列表（含 WP 归属） |
| 本周计划 | 优先读 `weekly-todo-index.md` 热索引；溯源时按本周 Due Date 过滤 board 按 WP 归集 | 按 WP 分组的 Task 列表 |
| 倒排倒计时 | 读 `plans/iteration-register.md` 倒排元数据（锚点日期/关键路径）+ board 未完成 Task | 距截止日剩余天数 + 未完成 WP + 关键路径预警 |
| 哪些任务超期 | 复用 §6.6 B 类判定（含 WP Ref 归属标注） | 超期清单 |

**性能约束**：WP 进度一律为 board 单文件实时聚合（不建进度索引文件）；日/周查询优先走既有热索引（索引优先原则，见 §6）；迭代登记册只读 WP 粗规划表，不扫描其他段。

---

## 7. 数据来源声明

### 7.1 适用范围

版本/任务/风险/项目概况/日报提交状态 5 类查询的回答末尾必须标注数据来源。复杂报告类（周报、分析报告等）按原输出规范，不额外增加数据来源声明。聚合计数与超期查询标注来源 `tasks/board.md`（及所用索引）。

### 7.2 统一格式

```
数据来源：
- {文件路径}
文件更新时间：{实际时间 / 当前环境未提供，无法确认}
```

多文件时逐行列出路径，更新时间同样不可得则标注"当前环境未提供，无法确认"。

### 7.3 文件修改时间降级规则

能获取文件最后修改时间则显示；无法获取不得编造，仅显示数据来源路径并标注"当前环境未提供，无法确认"。
