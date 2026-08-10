---
doc_type: import-log
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
---

# 导入日志

> 记录每次历史导入操作的过程和结果。

## 导入记录

| Import ID | Time | Source | Action | Items Found | Items Imported | Result | Operator |
|---|---|---|---|---|---|---|---|

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Import ID | 导入批次唯一标识 | IMP-YYYYMMDD-NNN |
| Time | 操作时间 | YYYY-MM-DD HH:MM |
| Source | 来源 LEG-NNN | LEG-001 |
| Action | 操作类型 | scan / extract / map / carryover / confirm / write |
| Items Found | 发现的候选数 | 数字 |
| Items Imported | 实际导入数 | 数字 |
| Result | 结果 | success / partial / failed / pending_confirm |
| Operator | 操作人 | 用户姓名或 AI辅助 |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
