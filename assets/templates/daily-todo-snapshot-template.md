---
doc_type: daily-todo-snapshot
snapshot_date: YYYY-MM-DD
target_date: YYYY-MM-DD
created_at: YYYY-MM-DD HH:MM
source_type: personal_daily_reports
status: frozen
---

# Daily Todo Snapshot - {snapshot_date}

> 本快照记录 {snapshot_date} 形成的 {target_date} 计划。冻结后不可静默覆盖，修订需追加 Revision Log。
> `source_type` 取值：`personal_daily_reports` / `pm_todo` / `meeting` / `external_import`（历史计划批量导入，见 `references/15-snapshot-rules.md` §8a）。

## 1. PM Direct Todos

| Todo ID | Owner | Project | Task | Priority | Source Ref | Status At Snapshot |
|---|---|---|---|---|---|---|
| TODO-20260810-001 | [姓名] | [子项目] | [任务] | P0 | [来源] | planned |

## 2. Team Plan By Project

### [子项目1名称]

| Todo ID | Owner | Task | Related Milestone | Risk Flag | Source Ref | Status At Snapshot |
|---|---|---|---|---|---|---|
| TODO-20260810-002 | [姓名] | [明日任务] | M0x | ⚠️/✅ | [日报来源] | planned |

### [子项目2名称]

| Todo ID | Owner | Task | Related Milestone | Risk Flag | Source Ref | Status At Snapshot |
|---|---|---|---|---|---|---|

## 3. Risks To Follow

| Risk ID | Project | Risk | Level | Suggested Action |
|---|---|---|---|---|

## 4. Issues To Follow

| Issue ID | Project | Issue | Status | Suggested Action |
|---|---|---|---|---|

## 5. Milestone Watch

| Project | Milestone | Planned Date | Current Status | Deviation |
|---|---|---|---|---|

## 6. Resource Alerts

| Person | Project | Change | Impact |
|---|---|---|---|

## 7. No Plan Projects

| Project | Reason / Note |
|---|---|

## Revision Log

| Time | Change | Reason | Operator |
|---|---|---|---|
