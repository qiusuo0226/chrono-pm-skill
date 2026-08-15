---
doc_type: iteration-register
project: ""
version: v1.0
date: "{{date}}"
status: 草稿
---

# 迭代登记册

> 本文件是项目迭代管理的**事实源**，登记每个迭代的基线信息（时间/需求/资源/里程碑关联）与工作包（WP）粗规划。
> **迭代 = 一组工作包（WP）**。WP 是计划编排的粗粒度单元（谁，几号~几号，交付什么）；
> 每日执行条目为 `tasks/board.md` 中带 `WP Ref` 的 Task（日/周计划 = board 按 Due Date 的时间切片，无独立可写载体）。
> 需求明细见 `requirements/requirement-register.md`。

## 迭代总览

| 迭代ID | 迭代名称 | 计划开始 | 计划结束 | 需求数 | 需求ID列表 | 资源 | 状态 | 关联里程碑 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|
| ITR-01 | 迭代一 | | | 0 | 待补充 | | planned | | |
| ITR-02 | 迭代二 | | | 0 | 待补充 | | planned | | |
| ITR-03 | 迭代三 | | | 0 | 待补充 | | planned | | |
| ITR-04 | 迭代四 | | | 0 | 待补充 | | planned | | |

## 字段说明

| 字段 | 说明 | 取值 |
|------|------|------|
| 迭代ID | 唯一标识，创建后不变 | ITR-01 ~ ITR-99 |
| 迭代名称 | 迭代的业务名称 | 如：需求与设计迭代、核心开发迭代 |
| 计划开始 | 迭代计划开始日期 | YYYY-MM-DD |
| 计划结束 | 迭代计划结束日期 | YYYY-MM-DD |
| 需求数 | 该迭代包含的需求数量 | 整数 |
| 需求ID列表 | 关联的需求ID | REQ-XXX-001, REQ-XXX-002, ... 或 "待补充" |
| 资源 | 参与该迭代的人员 | 姓名(角色), 姓名(角色) |
| 状态 | 迭代当前状态 | planned / in_progress / completed / cancelled |
| 关联里程碑 | 关联的里程碑（可选） | M-NN, M-NN 或空（不强关联） |
| 备注 | 补充说明 | 自由文本 |

## 迭代详情

### ITR-01: [迭代名称]

- **计划时间段**：YYYY-MM-DD ~ YYYY-MM-DD
- **需求数**：0
- **需求ID列表**：待补充
- **资源**：
- **状态**：planned
- **关联里程碑**：
- **编排方式**：正向 / 倒排（倒排时填下方倒排元数据）
- **备注**：

#### ITR-01 工作包规划表（WP）

| WP ID | Title | Owner | Start | End | Req Ref | Milestone Ref | Deliverable | Status | Depends On |
|---|---|---|---|---|---|---|---|---|---|
| WP-ITR01-01 | | | | | | | | planned | |

#### ITR-01 倒排元数据（仅倒排创建的迭代填写）

- **目标**：
- **锚点日期**（截止日）：YYYY-MM-DD
- **关键路径**：WP-ITR01-NN → WP-ITR01-NN
- **缓冲天数**：0

### ITR-02: [迭代名称]

- **计划时间段**：YYYY-MM-DD ~ YYYY-MM-DD
- **需求数**：0
- **需求ID列表**：待补充
- **资源**：
- **状态**：planned
- **关联里程碑**：
- **编排方式**：正向 / 倒排
- **备注**：

#### ITR-02 工作包规划表（WP）

| WP ID | Title | Owner | Start | End | Req Ref | Milestone Ref | Deliverable | Status | Depends On |
|---|---|---|---|---|---|---|---|---|---|
| WP-ITR02-01 | | | | | | | | planned | |

## 状态说明

| 状态 | 说明 |
|------|------|
| planned | 已规划，未开始 |
| in_progress | 进行中 |
| completed | 已完成 |
| cancelled | 已取消 |

## 工作包（WP）说明

| 字段 | 说明 | 取值 |
|------|------|------|
| WP ID | 唯一标识，创建后不变 | WP-ITRNN-NN（如 WP-ITR01-01） |
| Title | 粗任务名（谁在什么时间完成什么） | 自由文本 |
| Owner | 负责人 | 姓名 |
| Start / End | WP 排期（正向排或倒排算出） | YYYY-MM-DD |
| Req Ref | 关联需求（迭代来源基于需求） | REQ-XXX-NNN 或空 |
| Milestone Ref | 关联里程碑（可选） | M-NN 或空 |
| Deliverable | 交付物 | 自由文本 |
| Status | WP 状态 | planned / in_progress / completed |
| Depends On | 前置依赖 WP（可选） | WP ID 或空 |

**WP 与 Task 的边界**：

- WP = 计划层（"打算做什么"，粗粒度，本文件唯一维护）。
- Task = 执行层（"具体哪天做什么"，在 `tasks/board.md`，每条 Task 带 `WP Ref` + `Due Date`）。
- 一个 WP 拆解为 N 个 Task；**WP 进度由 board 中该 WP 关联 Task 的完成比例实时聚合（派生，不另存）**。
- WP 下所有 Task done → WP 状态 completed；所有 WP completed → 建议迭代 completed。
- 日计划 = board 按 Due Date 过滤（带 WP Ref 的 Task）；周计划 = board 按周切片按 WP 归集。

**倒排编排**：从锚点日期（截止日）反向推算各 WP 的 Start/End 与依赖，倒排元数据（目标/锚点/关键路径/缓冲）随迭代段存储，不另立体系。详见 `references/00-pm-main-rules.md` WF-7。

## 迭代与里程碑关联说明

- 迭代（ITR-NN）与里程碑（M01-M12）是**并存**关系，可选关联。
- 一个迭代可以关联一个或多个里程碑（如 ITR-01 关联 M03、M04）。
- 也允许迭代暂不关联里程碑（关联里程碑字段为空）。
- 里程碑仍是项目阶段管理主线，迭代是项目执行周期管理实体。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|------|-------------|-------------|--------|--------------|
| | | | | |
