---
doc_type: todo-history-index
portfolio: [项目集名称]
version: v1.0
last_updated: YYYY-MM-DD HH:MM
---

# Todo History Index

> 本文件是历史计划快照和实际执行摘要的目录索引。查询历史计划时优先读取本文件定位，不扫描 snapshots/ 目录。

## 快照索引

| Snapshot ID | Snapshot Date | Target Date | Type | File | Source Range | Status |
|---|---|---|---|---|---|---|
| SNAP-20260809-D | 2026-08-09 | 2026-08-10 | daily | snapshots/daily/20260809.md | 2026-08-09 daily reports | frozen |
| SNAP-2026W33-W | 2026-W33 | 2026-W33 | weekly | snapshots/weekly/2026-W33.md | weekly plan | frozen |

## 实际执行索引

| Actuals ID | Actual Date | Type | File | Source | Status |
|---|---|---|---|---|---|
| ACT-20260810-D | 2026-08-10 | daily | actuals/daily/20260810.md | daily reports | draft |
| ACT-2026W33-W | 2026-W33 | weekly | actuals/weekly/2026-W33.md | weekly report | draft |

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Snapshot ID | 快照唯一标识 | SNAP-{YYYYMMDD}-D（日）/ SNAP-{YYYY}W{WW}-W（周） |
| Snapshot Date | 快照生成日期 | YYYY-MM-DD |
| Target Date | 计划目标日期 | YYYY-MM-DD |
| Type | 类型 | daily / weekly / monthly |
| File | 文件路径 | snapshots/daily/xxx.md |
| Source Range | 来源范围 | 如 "2026-08-09 daily reports" |
| Status | 状态 | frozen / draft |

## 索引维护规则

1. 每次生成快照时追加一行到「快照索引」。
2. 每次生成实际执行摘要时追加一行到「实际执行索引」。
3. 不删除历史记录。
4. `last_updated` 字段记录最后一次更新时间。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
