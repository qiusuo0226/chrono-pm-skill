---
doc_type: project-lineage
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
---

# 项目阶段谱系

> 本文件记录大项目各阶段的关系链，让 AI 理解当前项目不是孤立的，而是某个阶段链上的一环。

## 阶段谱系

| Stage ID | Stage Name | Time Range | AI Workspace | Relation | Status | Notes |
|---|---|---|---|---|---|---|
| STG-001 | [阶段1名称] | 2026-01 ~ 2026-06 | [ai 目录路径] | previous | completed | 已验收 |
| STG-002 | [阶段2名称] | 2026-07 ~ 2026-10 | ./ai | current | active | 当前阶段 |

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Stage ID | 阶段唯一标识 | STG-001 ~ STG-999 |
| Stage Name | 阶段名称 | [名称] |
| Time Range | 时间范围 | YYYY-MM ~ YYYY-MM |
| AI Workspace | ai 目录路径 | 绝对路径或相对路径 |
| Relation | 与当前阶段的关系 | previous / current / next / parallel |
| Status | 阶段状态 | planned / active / completed / suspended / cancelled |
| Notes | 备注 | 补充信息 |

## 阶段间衔接记录

| From Stage | To Stage | Carryover Items | Imported At | Status |
|---|---|---|---|---|
| STG-001 | STG-002 | [数量] 项 | YYYY-MM-DD | pending / completed |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
