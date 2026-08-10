---
doc_type: daily-todo-actuals
actual_date: YYYY-MM-DD
created_at: YYYY-MM-DD HH:MM
source_type: daily_reports
status: draft
---

# Daily Todo Actuals - {actual_date}

> 本文件记录 {actual_date} 当天实际完成情况，用于与计划快照对比。

## 1. Completion Summary

| Todo ID | Owner | Project | Planned Task | Actual Result | Completion Status | Evidence Ref | Notes |
|---|---|---|---|---|---|---|---|
| TODO-20260810-001 | [姓名] | [子项目] | [计划任务] | [实际结果] | planned_done | [日报来源] | - |

### Completion Status 取值

| 状态 | 说明 |
|---|---|
| planned_done | 原计划且已完成 |
| planned_not_done | 原计划但未完成 |
| blocked | 原计划但被阻塞 |
| cancelled | 原计划取消 |
| carried_forward | 原计划延期/结转 |
| unplanned_done | 未计划但实际完成 |
| no_evidence | 缺少实际证据 |

## 2. Unplanned Work

| Owner | Project | Work | Evidence Ref | Impact |
|---|---|---|---|---|

## 3. Delayed / Carried Forward

| Todo ID | Owner | Task | New Target Date | Reason |
|---|---|---|---|---|

## 4. Daily Summary

- 原计划：X 项
- 已完成：X 项（X%）
- 未完成：X 项（阻塞 X / 延期 X / 取消 X）
- 计划外完成：X 项

## Revision Log

| Time | Change | Reason | Operator |
|---|---|---|---|
