---
doc_type: personal-todo-index
portfolio: [项目集名称]
version: v1.0
last_updated: YYYY-MM-DD HH:MM
---

# 个人待办索引

> 本文件按人聚合所有待办事项，是查询「某人明天/本周做什么」的快速入口。AI 查询待办时优先读取本文件。

## 待办清单

| Todo ID | Owner | Project | Task | Due Date | Priority | Status | Source Ref | Updated At |
|---|---|---|---|---|---|---|---|---|
| TODO-001 | [姓名] | [子项目] | [任务描述] | 2026-08-10 | P0 | open | board.md#T-001 | 2026-08-09 |

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Todo ID | 唯一标识 | TODO-001 ~ TODO-999 |
| Owner | 负责人 | 姓名 |
| Project | 所属子项目 | 子项目名称 |
| Task | 任务描述 | 简短描述 |
| Due Date | 截止日期 | YYYY-MM-DD |
| Priority | 优先级 | P0/P1/P2/P3 |
| Status | 状态 | open / in_progress / done / cancelled / deferred |
| Source Ref | 来源引用 | board.md#T-NNN / meeting#A-NNN / daily#name-date |
| Updated At | 最后更新时间 | YYYY-MM-DD HH:MM |

## 索引维护规则

1. 本索引从任务看板、会议纪要行动项、日报明日计划中自动提取。
2. 任务完成时（board.md 中状态变为 done），对应 Todo 状态同步更新为 done。
3. 新增任务或行动项时，追加新行。
4. `last_updated` 字段记录最后一次更新时间。
5. AI 查询时如发现 `last_updated` 超过 24 小时，应提示用户「索引可能过期，建议重建」。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
