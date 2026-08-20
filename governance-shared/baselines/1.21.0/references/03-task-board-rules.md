# 任务看板约束规则

本规则适用于任务看板的字段定义、状态流转、计划变更计数、延期统计与超期判定。

---

## 1. 任务看板字段

`tasks/board.md` 是任务管理的核心事实源，字段定义如下：

| 字段 | 说明 | 必填 | 取值 |
|------|------|------|------|
| Task ID | 唯一标识 | 是 | T-YYYYMMDD-NNN |
| Title | 任务标题 | 是 | 自由文本 |
| Owner | 负责人 | 是 | 姓名 |
| Status | 当前状态 | 是 | todo / in_progress / blocked / review / done / cancelled |
| Priority | 执行优先级 | 是 | P0 / P1 / P2 / P3 |
| Plan Ref | 关联计划项 | 否 | P-NN |
| Milestone Ref | 关联里程碑 | 否 | M-NN |
| Requirement Ref | 关联需求（需求溯源："做什么"） | 否 | REQ-XXX-NNN |
| WP Ref | 关联工作包（执行归属："排到哪个迭代工作包"） | 否 | WP-ITRNN-NN 或 none（创建时经 WF-8 归属判定，见 §8.1；Requirement Ref 与 WP Ref 并存不冲突） |
| Risk Ref | 关联风险 | 否 | R-YYYYMMDD-NNN |
| Issue Ref | 关联问题 | 否 | I-YYYYMMDD-NNN |
| Due Date | 预计完成日期 | 是 | YYYY-MM-DD |
| Original Due Date | 最初计划完成日期 | 否 | YYYY-MM-DD（设定后不可变，见 §1a） |
| Actual Date | 实际完成日期 | 否 | YYYY-MM-DD |
| Plan Change Count | 计划变更累计次数 | 否 | 整数，默认 0（见 §1a） |
| Delay Count | 延期累计次数 | 否 | 整数，默认 0（见 §1a） |
| Source | 来源 | 是 | meeting / daily / manual / requirement / import |
| Source Ref | 来源文件 | 是 | 文件路径或会议 ID |
| Notes | 备注 | 否 | 自由文本 |

### 1a. 计划变更与延期计数字段

本组字段用于"历史计划全量同步与变更追溯"（R2/R3）：

1. **Original Due Date**：任务的**最初计划完成日期**，在任务首次设定 Due Date 时记录，**一旦设定即不可变**（除非人工纠正录入错误，且必须在 Change Log 中记录并保留历史）。它是追溯"最初计划何时完成"的唯一可靠锚点。
2. **Plan Change Count**：任务计划发生变更的累计次数（整数，默认 0）。因 Owner 更换、范围调整、Due Date 任意方向移动、进度重排等计划变化均计入。
3. **Delay Count**：任务**延期**累计次数（整数，默认 0）。**仅当 Due Date 向后移动（比原计划更晚）时才 +1**。延期是计划变更的一个子集——不是每次计划变更都计延期。

**判定规则**：
- 概念域 A（记录操作）：board 底部 Change Log 使用 `add/update/remove/status/archive`，**不新增计划变更类型**；计划变更通过 `update` 操作 + Description 注明 `plan_change` 体现（见 §7）。
- 概念域 B（变更影响分类）：计划变更的分类（`plan_change` 等）在需求变更审批中由 `references/08-change-control-rules.md` 管理，与 board 计数字段解耦。
- `Plan Change Count` / `Delay Count` 由 AI 在确认的计划变更发生后更新，先输出"建议更新清单"，人工确认后落库。
- 旧工作区兼容：新字段缺失时视为 0，回退到 Change Log 统计并标注"推断，未确认"。
- 待确认（`Confirmed By: 待确认`）的 Due Date **不参与**"已确认计划延期/超期"计数，仅在"待确认变更"区块逐条提示原值 vs 新值；不新增字段列，pending 状态以 `Confirmed By` 值 + `pending-changes.md` 索引判定（见方案 3.5.3、B-03）。

## 5a. 超期判定与追责归属规则（B 类）

**定义区分**：
- **A 类（计数器）**：`Delay Count` 仅统计 Due Date 后移次数，见 §1a。回答"延期了几次"。
- **B 类（状态判定）**：给定某时刻，判断任务**当前是否超期**及归属，见本节。回答"现在哪些任务超期了"。**B 类判定不写入 Delay Count 计数器。**

### 5a.1 触发时机

B 类超期判定在**两个时机**触发：
1. **日报处理时**：汇总项目日报时同步评估各任务超期状态。
2. **PM 查询进度/状态时**：用户问"现在进度怎么样""哪些任务超期了""XX 延期/超期了吗"时，**实时计算**，确保每次查询都是最新结论。

### 5a.2 数据源（索引优先，禁止扫描日报原文）

判定数据来自 **board.md + 预建索引**，不得在查询时临时扫描日报原文或创建脚本遍历目录（对齐 `references/05-query-rules.md` 最小读取原则）：
- board.md：当前 Due Date / Owner / Original Due Date / Status / 计划变更确认状态。
- 索引：任务最近完成状态（读 `todos/daily-todo-index.md` / `personal-todo-index.md` 等预建索引，索引在日报处理后自动维护）。
- 若索引 >24h 未更新，AI 先提示"索引过期，建议重建"，不拿过期数据当结论（对齐 `references/14-self-check-rules.md`）。

### 5a.3 当前有效 Due Date（确认窗口期）

延期/超期以**当前有效 Due Date** 为基准：
- 新计划变更**已确认**（`Confirmed By: PM 姓名`）：使用新 Due Date。
- 新计划变更**待确认**（`Confirmed By: 待确认`，空窗期）：仍按旧版（未变前的）Due Date 判定；待确认新计划**不参与**延期/超期判定，一过旧截止日未完成即判超期（预警），仅在"待确认变更"区块提示原值 vs 新值。

**场景判定**：
| 场景 | 判定 |
|---|---|
| v1 8/10，v2 8/15 未确认，8/11 未完成 | 按 v1 判超期（预警）；不 +Delay（Delay 于 v2 确认后按 v2 计） |
| v1 8/10，v2 8/15 未确认，8/11 已完成 | 不算延期；提醒核查"截止日期后移是否为误操作" |
| v1 8/10，v2 8/15 已确认 | 按 8/15，8/16 起未完成才算超期；8/11-8/15 空窗未完成仅预警 |
| v1 8/10，无 v2，8/11 未完成 | 直接超期（Due Date 过未完成） |
| v1 8/10，v2 8/5（提前） | 不判延期；按最终确认的 8/5 判后续超期；可触发"计划收紧"提醒 |

### 5a.4 换人归属

同一任务在两版计划之间发生 Owner 变更时，超期归属按**交接时间点**切分：
- 交接前（变更发生时任务状态为"未完成"）的延期/超期，归属**原负责人**。
- 交接后的延期/超期，归属**新负责人**。
- 变更发生时任务已完成，则不产生换人延期归属问题。

## 2. 任务状态流转

```
todo → in_progress → review → done
                ↓          ↑
             blocked ───────┘

任何状态 → cancelled
```

### 2.1 状态定义

| 状态 | 说明 | 进入条件 |
|------|------|----------|
| todo | 已分配但未开始 | 任务已创建，负责人已确认 |
| in_progress | 正在进行 | 负责人已开始执行 |
| blocked | 被阻塞 | 存在依赖未满足或外部问题 |
| review | 待评审 | 开发完成，等待代码审查或测试 |
| done | 已完成 | 评审通过，交付物已提交 |
| cancelled | 已取消 | 任务不再需要 |

### 2.2 流转规则

1. `todo → in_progress`：必须有负责人确认。
2. `in_progress → blocked`：必须记录阻塞原因和关联的 Issue ID。
3. `blocked → in_progress`：必须记录解除阻塞的条件和时间。
4. `in_progress → review`：必须有交付物或完成标准可验证。
5. `review → done`：必须通过评审，评审人需记录。
6. 任何状态 → `cancelled`：必须记录取消原因和决策人。

## 3. 任务与需求的关联

1. 需求描述"要实现什么"，任务描述"如何实现或交付"。
2. AI 不得将需求直接登记为任务，除非已明确拆解为可执行事项。
3. 每个任务必须能追溯到来源需求或来源会议/日报。
4. 一个需求可拆解为多个任务，但一个任务原则上只关联一个主需求。

## 4. 任务优先级

| 优先级 | 含义 | 判定标准 |
|--------|------|----------|
| P0 | 紧急且重要 | 阻断里程碑、影响验收、生产事故 |
| P1 | 重要不紧急 | 核心功能、关键路径任务 |
| P2 | 一般 | 辅助功能、优化类任务 |
| P3 | 低 | 非紧急、可延后 |

优先级不代表执行顺序，执行顺序由依赖关系和负责人安排决定。

## 5. 任务依赖

在 Notes 字段中记录依赖关系：

```markdown
depends_on: T-20260809-001
blocks: T-20260809-003, T-20260809-005
```

- `depends_on`：本任务依赖的前置任务。
- `blocks`：本任务阻塞的后续任务。

依赖关系变更时，必须在 Change Log 中记录。

## 6. Backlog 管理

`tasks/backlog.md` 用于存放：
- 尚未排期的任务。
- 需求拆解后尚未分配到迭代的任务。
- 会议中提出的待确认事项。

Backlog 中的任务字段简化：

| 字段 | 说明 |
|------|------|
| Task ID | T-YYYYMMDD-NNN |
| Title | 任务标题 |
| Source | 来源 |
| Priority | P0-P3 |
| Status | backlog |
| Notes | 备注 |

从 backlog 移入 board 时，状态改为 `todo`，并补全完整字段。

## 7. Change Log

`tasks/board.md` 底部必须维护 Change Log：

```markdown
## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
| 2026-08-09 | add | 新增 T-20260809-001 | MTG-20260809-001 | 张三 |
| 2026-08-09 | status | T-20260808-005: review → done | 日报 2026-08-09 | 李四 |
| 2026-08-10 | update | T-20260809-001: plan_change，Due Date 8/10→8/15（Delay +1，Original 8/10 不可变） | PM 确认 | 张三 |
```

**概念域说明**：board 底部 Change Log 的 Change Type 属**记录操作类型**（`add/update/remove/status/archive`），**不新增 `plan_change` 类型**。计划变更通过 `update` 操作 + Description 标注 `plan_change` 体现；其影响分类（requirement/scope/schedule/cost/resource/plan_change）由 `references/08-change-control-rules.md`（概念域 B）管理，两者解耦。

Change Log 活跃区上限 50 行或超过 30 天时，触发按月归档到 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航。主动变更（pending）记录在写入时合并写入，同会话确认只记 1 条。

## 8. 级联传播规则

本实体（Task）状态变更时，按以下规则触发下游动作。动作分三类：
- [AUTO] 写派生视图（索引/待办），低风险，直接执行
- [CHECK] 只读校验，检查关联是否存在/一致
- [SUGGEST] 写事实源或影响其他实体，加入建议更新清单待 PM 确认

> **AUTO 作用域声明**：AUTO 仅作用于非事实源的派生视图（todo 索引/各类派生 index），不触碰任何事实源文件。事实源写入（含 pending 登记）一律受 `skill-contract.md` 第 5 条约束。

执行顺序：先 AUTO → 再 CHECK → 最后 SUGGEST。
同一处理流程内，级联动作只执行一次；多个 SUGGEST 汇总为同一批建议清单，流程末尾统一输出。
执行完毕后，14 号自查清单验证完整性。

> **强制执行要求**（见 `00-pm-main-rules.md` §8a）：以上 AUTO/CHECK/SUGGEST 动作不得静默跳过。SUGGEST 必须呈现给 PM 确认，不得以"用户未要求"为由省略。流程末尾必须输出"级联完整性"结论。

Task 创建 →
  [CHECK] 若含 Risk Ref → 验证关联风险存在且状态合理（§1 Ref 字段）
  [CHECK] 若含 Issue Ref → 验证关联问题存在且状态合理（§1 Ref 字段）
  [CHECK] 若含 Requirement Ref → 验证关联需求存在（§1 Ref 字段）
  [CHECK] 若含 WP Ref → 验证 iteration-register 中该 WP 存在且状态合理；若上下文可识别归属但 WP Ref 缺失 → 补填（WF-8 兜底）

Task 状态 → done →
  [AUTO] 更新 personal-todo-index 中对应条目状态为 done（14 §2.2）
  [AUTO] 更新 daily-todo-index 对应条目（14 §2.2）
  [CHECK] 若含 Issue Ref → 检查关联 issue 是否可关闭
  [CHECK] 若含 WP Ref → 聚合该 WP 关联 Task 完成比例；若该 WP 全部 Task done → [SUGGEST] 更新 iteration-register 中 WP 状态为 completed；所有 WP completed → [SUGGEST] 迭代状态 completed 并检查关联里程碑可达性（触发时机与 Task→todo-index 同一事件链，不额外新增维护动作）

Task Due Date 变更 →
  [CHECK] 若含 WP Ref → 检查新 Due Date 是否超出 WP End；若超出 → [SUGGEST] 同步调整 WP 排期（iteration-register，plan_change 记录见 §7）

Task 状态 → blocked →
  [SUGGEST] 若因 Issue 阻塞 → 建议确认 issue-register 中对应 issue 状态为 open

Task Owner 变更 →
  [AUTO] 更新 personal-todo-index 中该任务的 Owner 字段

Task 状态变更 →
  [CHECK] 若含 Requirement Ref → 验证关联需求当前状态是否与任务进展一致
  [SUGGEST] 若不一致（如任务 done 但需求仍 in_progress）→ 建议同步更新需求状态

Task Owner 委派（新建任务或 Owner 变更）→
  [CHECK] 被委派人是否为非 PM 本人的团队成员
  [SUGGEST] 若是 → 建议在委派方（PM）的 personal-todo-index 追加跟进条目："跟进 {被委派人姓名} - {任务 Title}（{Task ID}）"，Due Date = 任务 Due Date

> 端到端工作流数据路径见 `00-pm-main-rules.md` §9（WF-1~WF-8）。本文件 §8 定义 Task 实体的级联规则，00号 §9 定义跨实体的完整工作流路径，两者互补不替代。

### 8.0 WP 进度与分层视图（派生，不另存）

> WP（工作包）是迭代计划的组成单元（迭代 = 一组 WP），粗规划表唯一维护在 `plans/iteration-register.md`；board 是执行唯一事实源。

1. **WP 进度 = board 中该 WP 关联 Task 完成比例的实时聚合**（查询时单文件按 WP Ref 过滤计算，不建进度索引文件、不另存进度值，保证与事实源永远一致）。
2. **日计划 = board 按 Due Date 过滤**（带 WP Ref 的 Task）；**周计划 = board 按周切片按 WP 归集**（PM 微调周计划 = 走 WP 日期变更链路，不新增可写事实源）。
3. **看板分层查询**（按迭代/WP/日/周）见 `05-query-rules.md` §6.7；倒排倒计时读 iteration-register 倒排元数据。
4. Task 的 Requirement Ref（需求溯源）与 WP Ref（执行归属）并存不冲突：REQ 管"做什么"，WP 管"排到哪个迭代工作包"。

### 8.1 待办创建归属与状态级联（WF-8 统一入口）

> 背景：personal-todo-index 是完全派生索引（来源：board + 日报 + 会议纪要）。待办/任务创建的所有入口（口述/日报明日计划/纪要行动项/需求拆解/变更批准）必须先走 `00-pm-main-rules.md` WF-8 归属判定再落位；**正式任务只有 board 一个可写载体，禁止"只写索引不落 board"**。不是每条待办都该落 board——一次性提醒落 Task 会污染看板。

待办/任务创建（任何入口）→
  [MANDATORY] 执行 WF-8 归属判定（预筛候选 WP → 高置信语义匹配 → WP/独立/提醒三分；证据不足必须追问）
  [MANDATORY] 归属 WP → 写 board Task（WP Ref + Due Date）；独立任务 → 写 board Task（WP Ref: none）；字段优先继承已有值（Owner/Priority/Due Date/Source），缺失字段由 PM 补充
  [MANDATORY] 一次性提醒（无 Owner、无 Deadline、无明确交付物）→ 唯一不落 board 路径，仅写 todo 索引，且必须在输出中呈现判定理由
  [AUTO] 落 board 后派生 personal-todo-index / daily-todo-index（派生视图，直接执行）；写 board + 派生索引 + WP 进度聚合为同一建议更新清单内的原子动作，不留半更新

待办状态 → done →
  [CHECK] 关联的 board 任务是否也已完成
  [SUGGEST] 若 board 任务未完成 → 建议同步更新 board 状态为 done/review

> 本 §8.1 待办**创建**由 `00-pm-main-rules.md` WF-8 统一接管（含口述/日报/纪要/需求拆解/变更批准五入口）；待办**状态更新**由 WF-1 步骤 18.5 与 `10-update-trigger-rules.md` 待办信号触发。

### 8.2 Task 生命周期推导触发（来自日报/纪要中的里程碑终态事件）

> 本 §8.2 由 `00-pm-main-rules.md` §10 推导基线触发，复用 §8 级联传播机制。

日报/纪要处理中检测到里程碑终态事件 →
  [CHECK] 推导触发事件是否属于 `00-pm-main-rules.md` §10.3 推导链中的触发事件（或 entity-registry §2 项目级覆盖中的触发事件）
  [SUGGEST] 若推导结论与当前 Task 状态不一致 → 建议同步 Task 状态，标注"推导状态（来源：{过程记录}）"
  [SUGGEST] 输出矛盾标注（走 §8a 强制呈现）
  [CHECK] 受影响任务集识别：按 `00-pm-main-rules.md` §10.5 四级降级定位目标任务
