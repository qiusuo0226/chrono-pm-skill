---
doc_type: workspace-health
project: [项目名 / 项目集名]
version: v1.0
last_checked: YYYY-MM-DD HH:MM
last_prompted_upgrade_at: 
ignored_until: 
---

# 工作区健康状态

> 本文件是人类可读的工作区健康报告，AI 检查"工作区健康吗"时优先读取本文件。

## 版本状态

| Item | Value |
|---|---|
| Skill Version | |
| Workspace Schema | |
| Workspace Skill Version | |
| Status | healthy / outdated / needs_migration / needs_rebuild |

## 能力状态

| Capability | Status | Notes |
|---|---|---|
| daily_report | ok / missing / degraded | |
| weekly_report | ok / missing / degraded | |
| pm_daily_todo | ok / missing / degraded | |
| quick_query | ok / missing / degraded | |
| output_artifact | ok / missing / degraded | |
| continuity | ok / missing / degraded | |
| resource_management | ok / missing / degraded | |
| todo_snapshot | ok / missing / degraded | |
| self_check | ok / missing / degraded | |
| excel_generation | ok / missing / degraded | |
| update_trigger | ok / missing / degraded | |
| workspace_upgrade | ok / missing / degraded | |

## 索引状态

> v2.0.0 起旧待办索引（personal/daily/weekly-todo-index、history-index）与个人进度汇总已删除；待办事实源为 `todos/{date}/{执行人}.md`，绑定文件为 `todos/{date}/_index.md`。

| Index File | Exists | Last Updated | Records | Status |
|---|---|---|---|---|
| todos/{date}/_index.md（当日绑定文件） | yes/no | | | fresh / stale / empty / missing |
| YYYYMM/index.md | yes/no | | | |
| change-log/index.md | yes/no | | | |

## 推荐动作

1. 
2. 

## 升级提醒控制

| Field | Value |
|---|---|
| Last Prompted | |
| Ignored Until | |
| Reminder Frequency | once_per_session / once_per_day / once_per_week |

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
