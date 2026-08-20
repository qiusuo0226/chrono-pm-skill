---
doc_type: import-log
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
---

# 导入日志

> 记录每次历史导入操作的过程和结果。覆盖两类：跨阶段衔接导入（`references/13-continuity-rules.md`）与计划批量导入 R1（`references/15-snapshot-rules.md` §8a）。

## 导入记录

| Import ID | Time | Source | Action | Items Found | Items Imported | Result | Operator |
|---|---|---|---|---|---|---|---|

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Import ID | 导入批次唯一标识 | IMP-YYYYMMDD-NNN |
| Time | 操作时间 | YYYY-MM-DD HH:MM |
| Source | 来源 | LEG-NNN（衔接导入）/ external_import + 原始文件路径（R1 批量导入） |
| Action | 操作类型 | scan / extract / map / carryover / confirm / write / import_plan |
| Items Found | 发现的候选数 | 数字 |
| Items Imported | 实际导入数 | 数字 |
| Result | 结果 | success / partial / failed / pending_confirm |
| Operator | 操作人 | 用户姓名或 AI辅助 |

> R1 批量导入记录建议 `Source=external_import`、`Action=import_plan`，并在备注关联 `snapshots/daily/imported-{date}.md`。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
