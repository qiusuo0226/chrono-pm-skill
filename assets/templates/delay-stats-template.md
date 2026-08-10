---
doc_type: delay-stats
project: ""
portfolio: ""
period: ""
version: v1.0
date: "{{date}}"
status: 草稿
---

# 延期统计（Delay Stats）

> 用于 A 类聚合查询（R4）："某任务变更了几次 / 延期了几次"。数据源为 `tasks/board.md` 单文件（只读该文件，不扫描快照/日报）。计数口径见 `references/03-task-board-rules.md` §1a。统计口径见 `references/05-query-rules.md` §6.5。

## 1. 延期计数（per-person）

| Owner | 变更次数(Plan Change Count) | 延期次数(Delay Count) | 备注 |
|---|---|---|---|
| [姓名] | | | |

## 2. 变更次数（per-task）

| Task ID | Task | Plan Change Count | Delay Count | Current Due Date | Status |
|---|---|---|---|---|---|
| T-YYYYMMDD-NNN | [任务] | | | YYYY-MM-DD | |

## 3. 汇总

- 任务总数：X
- 发生计划变更的任务数：X
- 发生延期（Due Date 后移）的任务数：X
- 延期率：X%

## 4. 数据口径声明

- [ ] 数据来源：`tasks/board.md`（单文件，未扫描快照/日报）。
- [ ] 若 board 缺 Plan Change Count / Delay Count（旧工作区），改从 Change Log 统计并标注**"推断，未确认"**。
- [ ] 完工任务（done）不参与延期告警，但可保留计数历史。
- [ ] 超过仪表数据置信区间时，提示 PM 核对 board 字段完整度。

## 信息来源

| 数据项 | 来源 | 置信度 |
|---|---|---|
| Plan Change Count | tasks/board.md | 高 / 中（推断） |
| Delay Count | tasks/board.md | 高 / 中（推断） |
