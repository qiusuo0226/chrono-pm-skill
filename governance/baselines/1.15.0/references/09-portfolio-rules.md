# 项目集管理约束规则（子约束）

本规则适用于项目集（Portfolio）模式下的跨项目管理，包括汇总周报、跨项目风险、整体P&L、里程碑总览、人员资源协调与流转。使用本约束时，必须同时遵守主约束。

---

## 1. 项目集模式总则

### 1.1 业务目录不侵入规则

AI 管理文件只能写入根目录 `ai/` 下。不得在业务子项目目录下创建 `ai/`、`prompts/`、`templates/`、`reports/` 等管理目录，除非用户显式要求。业务目录只作为被引用对象，不作为 AI 管理文件存放位置。

### 1.2 层级职责

| 层级 | 管什么 | 不管什么 |
|------|--------|----------|
| 项目集级 `portfolio/` | 跨项目风险、整体P&L、汇总周报、人员资源、项目集决策、里程碑总览 | 不复制子项目明细 |
| 子项目级 `projects/{name}/` | 需求、任务、日报、周报、项目内风险、项目内里程碑 | 不管跨项目事项 |

### 1.3 数据流方向

信息从子项目流向项目集（向上汇总），项目集决策通知子项目执行（向下通知），但项目集不直接修改子项目事实源——只能通过"建议更新清单"提出。

## 2. 项目集汇总周报

### 2.1 生成流程

```
1. 读取 portfolio/context/project-index.md 获取子项目清单
2. 遍历每个子项目的当前周报或当周日报
3. 汇总各子项目本周完成、风险、问题、里程碑
4. 合并跨项目事项（资源冲突、共性问题、需协调事项）
5. 读取 portfolio/resources/resource-register.md 补充人员变动
6. 读取 portfolio/todos/ 下的待办索引，汇总个人待办
6. 读取 portfolio/risks/risk-register.md 补充跨项目风险
7. 生成汇总周报
```

### 2.2 汇总原则

- 项目集周报只汇总关键事项、跨项目事项、需升级事项，不复制全部子项目明细。
- 每个子项目在汇总周报中占一个章节，概括本周进展和下周重点。
- 跨项目事项单独列出（资源冲突、共性问题、整体进度偏差）。
- 所有引用的子项目数据必须标注来源文件路径。

## 3. 跨项目风险管理

### 3.1 什么风险应登记在项目集级

以下风险应登记在 `portfolio/risks/risk-register.md` 而非子项目级：

| 场景 | 示例 |
|------|------|
| 资源在项目间冲突 | 陈佳菁同时被全链通和企业通共用，实际产能不足 |
| 人员变动影响多个项目 | 严维彬请假，全链通和企业通都受影响 |
| 跨项目依赖 | 信用监管改造未完成，登记注册无法启动联调 |
| 整体进度风险 | 三个子项目整体进度偏差超10%，影响10月上线 |
| 整体成本风险 | 人力成本合计逼近总合同额预警线 |

### 3.2 风险与子项目的关联

项目集级风险必须标注影响哪些子项目（PRJ-NNN），并与子项目级风险通过 ID 互相关联。

## 4. 整体P&L管理

`portfolio/plans/budget.md` 汇总所有子项目的成本数据：

| 子项目 | 合同额 | 50%成本线 | 已投入人月 | 已投入人日 | 人力成本 | CPI | 偏差 |
|--------|--------|-----------|-----------|-----------|----------|-----|------|
| PRJ-001 全链通重构 | | | | | | | |
| PRJ-002 企业通重构 | | | | | | | |
| PRJ-003 信用监管重构 | | | | | | | |
| **合计** | | | | | | | |

当合计人力成本占总合同额比重超过预警线时，必须主动预警。

## 5. 人员资源管理

### 5.1 核心原则

1. 人员资源是项目集级管理对象，统一维护在 `portfolio/resources/`。
2. 子项目级不单独维护资源登记册。
3. 当前人员分配状态记录在 `resource-register.md`（事实源）。
4. 人员进场、离场、借调、请假、角色变化、分配比例变化记录在 `transfer-log.md`（独立文件）。
5. 任何人员流转不得只更新当前状态，必须先登记流转记录。
6. AI 不得将未经确认的人员变动直接写为事实，应标记为待确认。

### 5.2 resource-register.md 字段

| 字段 | 说明 | 取值 |
|------|------|------|
| Resource ID | 唯一标识 | RES-NNN |
| 姓名 | 人员姓名 | |
| 角色/岗位 | 职能 | 项目经理/产品经理/前端开发/后端开发/测试/QA |
| 当前状态 | 是否在岗 | active / on_leave / left / transferred_out / pending_join |
| 分配方式 | 全职或共享 | full_time / shared / backup / temporary |
| 主项目 | 当前主要所在 | PRJ-NNN |
| 同时参与项目 | 其他项目 | PRJ-NNN, PRJ-NNN |
| 分配详情 | 各项目占比 | 如：全链通50% / 企业通30% / 信用监管20% |
| 进场日期 | 最早进场 | YYYY-MM-DD |
| 计划离场日期 | 预计离场 | YYYY-MM-DD |
| 实际离场日期 | 实际离场 | YYYY-MM-DD |
| 累计流转次数 | 在项目集内换了几次 | 数字 |
| B角 | 替补人员 | RES-NNN |
| 风险等级 | 资源风险 | low / medium / high |
| Source Type | 来源类型 | meeting / daily / manual |
| Source Ref | 来源引用 | 文件路径或会议ID |
| 最近更新 | 最后更新日期 | YYYY-MM-DD |

### 5.3 transfer-log.md 字段

| 字段 | 说明 | 取值 |
|------|------|------|
| Transfer ID | 唯一标识 | RTF-YYYYMMDD-NNN |
| Resource ID | 人员编号 | RES-NNN |
| 姓名 | 人员姓名 | |
| 流转类型 | 进/出/调换 | transfer_in / transfer_out / role_change / share_adjust / temporary_support / leave_start / leave_end / return_to_project / replacement |
| 来源项目 | 从哪个项目 | PRJ-NNN 或 外部 |
| 目标项目 | 到哪个项目 | PRJ-NNN 或 外部 |
| 生效日期 | 何时生效 | YYYY-MM-DD |
| 结束日期 | 临时支援的结束日期 | YYYY-MM-DD（永久流转留空） |
| 原因 | 为什么流转 | 如：全链通线上文书开发结束，返还资源 |
| 变更后分配 | 转入后的分配方式 | 如：企业通100% 或 企业通70%/信用监管30% |
| 审批人 | 谁确认的 | |
| 关联风险 | 是否触发风险 | R-YYYYMMDD-NNN |
| 关联问题 | 是否关联问题 | I-YYYYMMDD-NNN |
| 关联决策 | 是否有决策记录 | D-YYYYMMDD-NNN |
| Source Type | 来源类型 | meeting / daily / manual |
| Source Ref | 来源引用 | 文件路径或会议ID |

### 5.4 资源风险触发规则

以下情况必须提示资源风险并建议写入 `portfolio/risks/risk-register.md`：

| 编号 | 触发条件 | 风险等级 |
|------|----------|----------|
| RR-01 | 关键岗位无 B 角 | high |
| RR-02 | 同一人员同时参与 2 个以上 P0/P1 项目 | high |
| RR-03 | 人员状态为 on_leave，但仍承担关键任务 | high |
| RR-04 | 人员被抽调导致原项目关键任务无人负责 | high |
| RR-05 | 共享人员分配比例合计超过 100% | high |
| RR-06 | 计划离场日期早于关键里程碑完成日期 | medium |
| RR-07 | 某项目核心角色缺失（无后端/无测试/无产品） | high |
| RR-08 | 人员连续多次流转（≥3次），影响项目稳定性 | medium |

### 5.5 联动规则

人员资源变动时，AI 必须检查并输出以下联动建议：

```
人员变动
  → transfer-log.md（记录流转）
  → resource-register.md（更新当前状态）
  → 若触发资源风险 → portfolio/risks/risk-register.md
  → 若影响成本 → portfolio/plans/budget.md
  → 若影响子项目任务 → projects/{子项目}/tasks/board.md
  → 若需要管理决策 → portfolio/decisions/decision-log.md
```

AI 不直接修改子项目任务负责人，只能通过"建议更新清单"提出。

### 5.6 resource-register 与 project-context 一致性检查（v1.6.1 新增）

**核心原则：**

1. `resource-register.md` 是人员当前状态的**唯一主源**。
2. `project-context.md` 中的团队列表是 register 的**投影**，不是独立事实源。
3. 日报目录中的人员信息只能是**候选证据**，不能自动覆盖 register。
4. AI **不得未经用户确认**直接修改 `resource-register.md` 或 `project-context.md`。

**一致性检查触发条件：**

- 人员资源流转后更新 register 时
- 用户要求"检查资源一致性"时
- 生成项目集汇总周报时（作为周报流程的前置检查）

**差异类型与处理方式：**

| 差异类型 | 处理方式 | AI 行为 |
|---|---|---|
| register 有此人但 context 没有 | 输出差异报告，标记"context 需同步" | 不自动修改 context |
| context 有此人但 register 没有 | 输出差异报告，标记"register 可能缺失，需确认" | 不自动修改 register |
| 日报显示某人参与但 register 未登记 | 输出候选资源变更 | 不自动添加到 register |
| register 状态与 transfer-log 记录不一致 | 以 transfer-log 历史记录为佐证，输出差异报告 | 请用户确认 |
| 同一人在不同子项目用不同名字 | 输出"可能存在身份映射问题"警告 | 请用户确认是否同一人 |

**差异报告输出格式：**

```markdown
## 资源一致性差异报告

### 检查范围
- resource-register.md vs projects/{子项目}/context/project-context.md

### 差异项

| 子项目 | 差异类型 | register 记录 | context 记录 | 建议操作 |
|---|---|---|---|---|
| PRJ-002 | 状态不一致 | RES-003 王五: on_leave | 王五: active | A.以register为准更新context / B.以context为准修正register / C.暂不处理 / D.补充说明 |
| PRJ-001 | 人员缺失 | 无"赵六" | "赵六: 测试工程师" | A.确认后添加到register / B.从context删除 / C.暂不处理 |

### 规则
- AI 不自动修改任何文件
- 用户选择后，AI 按选择执行并记录到 Change Log
```

## 6. 里程碑总览

`portfolio/milestones/milestone-board.md` 汇总所有子项目的里程碑状态：

| 子项目 | 里程碑 | 计划日期 | 实际日期 | 状态 | 风险评估 |
|--------|--------|----------|----------|------|----------|
| PRJ-001 全链通 | M06 | | | | |
| PRJ-001 全链通 | M07 | | | | |
| PRJ-002 企业通 | M05 | | | | |
| ... | | | | | |

## 7. 项目索引维护

`portfolio/context/project-index.md` 是项目集的入口文件，AI 生成汇总周报或执行跨项目操作前必须先读取此文件：

| Project ID | Project Name | Management Path | Business Path | PM | Status | Priority | Include In Weekly |
|------------|-------------|-----------------|---------------|-----|--------|----------|-------------------|
| PRJ-001 | 全链通重构 | ai/projects/全链通重构 | 全链通重构/ | | in_progress | P0 | yes |
| PRJ-002 | 企业通重构 | ai/projects/企业通重构 | 企业通重构/ | | in_progress | P0 | yes |
| PRJ-003 | 信用监管登记注册重构 | ai/projects/信用监管登记注册重构 | 信用监管登记注册重构/ | | in_progress | P0 | yes |

新增子项目时必须在此文件登记，不得通过扫描文件夹代替索引读取。

## 8. 级联传播规则

本实体（Resource / 项目集级实体）状态变更时，按以下规则触发下游动作。动作分三类：
- [AUTO] 写派生视图（索引/待办），低风险，直接执行
- [CHECK] 只读校验，检查关联是否存在/一致
- [SUGGEST] 写事实源或影响其他实体，加入建议更新清单待 PM 确认

> **AUTO 作用域声明**：AUTO 仅作用于非事实源的派生视图，不触碰任何事实源文件。事实源写入（含 pending 登记）一律受 `skill-contract.md` 第 5 条约束。

执行顺序：先 AUTO → 再 CHECK → 最后 SUGGEST。
同一处理流程内，级联动作只执行一次；多个 SUGGEST 汇总为同一批建议清单，流程末尾统一输出。
执行完毕后，14 号自查清单验证完整性。

Resource 状态 → offboard/transferred →
  [SUGGEST] 其名下所有 open/in_progress task → 建议重新分配或 blocked
  [AUTO] 更新 personal-todo-index：移除或标记该人的待办
  [SUGGEST] 更新 resource-register，记录流转日志

Resource 状态 → onboard →
  [AUTO] 在 personal-todo-index 中创建该人的空条目

### 8.1 transfer-log 归档规则

transfer-log.md 归档规则：
- 拆分触发：>100 条记录 或 文件 >300 行
- 拆分策略：按年度归档到 `logs/archive/YYYY-transfer-log.md`
- 归档后维护 `logs/index.md` 索引
- 归档操作本身记录在 Change Log 中
- 注意：transfer-log 为只追加型文件，归档只移动历史条目，不删除任何内容

### 8.2 resource-register 生命周期管理

resource-register 生命周期管理：
- 状态为 `left`/`transferred_out` 且离场超过 90 天的人员 → 归档到 `resource-register-archive.md`
- 归档触发：在周报生成时检查
- 归档后主体文件仅保留 `active`/`onboard` 状态的资源
- 归档操作记录在 Change Log 中

> 端到端工作流数据路径见 `00-pm-main-rules.md` §9（WF-1~WF-6）。本文件 §8 定义 Resource 实体的级联规则，00号 §9 WF-6 定义人员流转的完整读/写路径，两者互补不替代。
