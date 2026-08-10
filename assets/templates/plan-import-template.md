---
doc_type: plan-import
import_date: YYYY-MM-DD
source_type: external_import
status: draft
---

# 历史计划批量导入 - {import_date}

> 用于 R1（历史计划全量同步）。将存量计划（.pod / Excel / 遗留 board 导出）批量导入快照体系与任务看板。

## 1. 导入批次信息

| 字段 | 值 |
|---|---|
| Import ID | IMP-YYYYMMDD-NNN |
| 导入日期 | YYYY-MM-DD |
| 来源载体 | [.pod / Excel / 文本] |
| 来源文件 | [路径] |
| 数据确认 | 已确认 / 待确认（未确认不得写入） |
| 任务总数 | [N] |

## 2. 导入前校验

- [ ] 来源结构与目标 board 字段映射已确认（见 `references/03-task-board-rules.md` 字段映射）。
- [ ] 无独立历史工作区（若有，走 `references/13-continuity-rules.md`）。
- [ ] 目标日期范围内的既有任务已识别（避免重复导入）。

## 3. 导入清单（候选）

| Task ID | Task | Owner | Due Date | Progress | Status | Source Note |
|---|---|---|---|---|---|---|
| T-YYYYMMDD-NNN | [任务] | [姓名] | YYYY-MM-DD | 0% | todo | import |

## 4. 冻结确认

- [ ] 已生成 `snapshots/imported/{date}.md`（冻结快照）。
- [ ] 已写入 `tasks/board.md`（Source=import，Plan Change Count/Delay Count 记 0）。
- [ ] 已在 `todo-history-index-template.md`「外部导入登记」追加一行。
- [ ] 导入后按 `references/15-snapshot-rules.md` §8a 步骤 6-9 完成索引登记。

## 5. 导入校验（完成后）

- [ ] 每个导入任务在 board 可见。
- [ ] 每个导入任务有对应冻结快照行。
- [ ] 既有任务未被覆盖（不可覆盖规则，见 `references/13-continuity-rules.md` §11）。

## Revision Log

| Time | Change | Reason | Operator |
|---|---|---|---|
