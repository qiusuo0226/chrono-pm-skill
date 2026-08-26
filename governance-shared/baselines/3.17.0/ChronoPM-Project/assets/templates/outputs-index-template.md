---
doc_type: outputs-index
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
---

# 生成物索引

本文件记录所有 AI 生成物输出批次，按创建时间排列。

## 输出批次记录

| Batch ID | Created At | Request | Type | Status | Main File | Related AI File |
|---|---|---|---|---|---|---|
| | | | | | | |

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Batch ID | 批次目录名（时间戳） | YYYYMMDDHHMMSS |
| Created At | 创建时间 | YYYY-MM-DD HH:MM:SS |
| Request | 用户原始请求 | [文本] |
| Type | 生成类型 | weekly_report / meeting_minutes / requirement_review / design_review / export_excel / export_word / export_pdf / skill_gap（集周报归 ChronoPM-Portfolio，本包不写）。skill_gap 的 Main File=`需求-{短标题}.md`，无 manifest |
| Status | 当前状态 | draft / pending_confirmation / revising / final / exported / archived / cancelled |
| Main File | 主文件路径 | outputs/{batch_id}/draft.md 或 files/xxx.xlsx |
| Related AI File | 关联的事实源文件（归档后填写） | reports/weekly/YYYY/... 或 pending |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
