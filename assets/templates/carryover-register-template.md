---
doc_type: carryover-register
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
---

# 结转事项登记册

> 所有从历史阶段结转到当前阶段的事项必须先登记在此文件中，经用户确认后才能写入当前阶段事实源。

## 结转事项清单

| Carryover ID | Type | Source Stage | Source Ref | Title | Summary | Target Project | Target File | Carryover Status | Confirmation Status | Owner | Due Date | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Carryover ID | 结转事项唯一标识 | CO-001 ~ CO-999 |
| Type | 事项类型 | risk / issue / task / requirement / decision / milestone / budget / resource |
| Source Stage | 来源阶段 | STG-NNN [阶段名] |
| Source Ref | 来源引用 | LEG-NNN:文件名#条目ID |
| Title | 事项标题 | 简短描述 |
| Summary | 事项摘要 | 详细说明 |
| Target Project | 目标子项目 | PRJ-NNN [子项目名] |
| Target File | 目标文件 | ai/projects/{子项目}/... |
| Carryover Status | 结转状态 | candidate / pending_import / imported / merged / referenced / ignored / duplicate / cancelled |
| Confirmation Status | 确认状态 | pending_confirm / confirmed / rejected / needs_more_info |
| Owner | 负责人 | 姓名 |
| Due Date | 截止日期 | YYYY-MM-DD |
| Notes | 备注 | 补充信息 |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
