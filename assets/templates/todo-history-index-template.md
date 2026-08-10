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
| IMP-20260810-001 | 2026-08-10 | 2026-08-31 | import | snapshots/imported/20260810.md | external_import: 存量计划(.pod/Excel) | frozen |

## 实际执行索引

| Actuals ID | Actual Date | Type | File | Source | Status |
|---|---|---|---|---|---|
| ACT-20260810-D | 2026-08-10 | daily | actuals/daily/20260810.md | daily reports | draft |
| ACT-2026W33-W | 2026-W33 | weekly | actuals/weekly/2026-W33.md | weekly report | draft |

## 外部导入登记（R1）

历史计划批量导入（external_import）在本表登记，每批一行：

| Import ID | Import Date | Source File | Target | Count | Status |
|---|---|---|---|---|---|
| IMP-YYYYMMDD-NNN | YYYY-MM-DD | [.pod/Excel 路径] | board.md + snapshots/imported/{date}.md | [任务数] | frozen |

- 导入即冻结：`snapshots/imported/{date}.md` 生成后不可静默覆盖。
- board 中记 `Source: import`；计数字段（Plan Change Count / Delay Count）首版记 0。
- 规则详见 `references/15-snapshot-rules.md` §8a、`references/03-task-board-rules.md` §1。

## 字段说明

| 字段 | 说明 | 取值 |
|---|---|---|
| Snapshot ID | 快照唯一标识 | SNAP-{YYYYMMDD}-D（日）/ SNAP-{YYYY}W{WW}-W（周）/ IMP-*（导入） |
| Snapshot Date | 快照生成日期 | YYYY-MM-DD |
| Target Date | 计划目标日期 | YYYY-MM-DD |
| Type | 类型 | daily / weekly / monthly / import |
| File | 文件路径 | snapshots/daily/xxx.md / snapshots/imported/xxx.md |
| Source Range | 来源范围 | 如 "2026-08-09 daily reports"、external_import |
| Status | 状态 | frozen / draft |

## 索引维护规则

1. 每次生成快照时追加一行到「快照索引」。
2. 每次生成实际执行摘要时追加一行到「实际执行索引」。
3. 每次历史计划批量导入时追加一行到「外部导入登记」。
4. 不删除历史记录。
5. `last_updated` 字段记录最后一次更新时间。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
