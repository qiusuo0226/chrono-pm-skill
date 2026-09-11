---
doc_type: plan-import
import_date: YYYY-MM-DD
source_type: external_import
status: draft
---

# 历史计划批量导入 - {import_date}

> 用于 R1（历史计划全量同步）。将存量计划（.pod / Excel / 遗留导出）批量导入快照体系与待办文件。

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

- [ ] 来源结构与目标待办文件字段映射已确认。
- [ ] 无独立历史工作区（若有，走 `references/13-continuity-rules.md`）。
- [ ] 目标日期范围内的既有任务已识别（避免重复导入）。

## 3. 导入清单（候选）

| 待办编号 | 标题 | Owner | 结束时间 | 进度 | 状态 | Source Note |
|---|---|---|---|---|---|---|
| TD-{人名缩写}-{YYYYMMDD}-{NNN} | [任务] | [姓名] | YYYY-MM-DD | 0% | 待处理 | import |

## 4. 冻结确认

- [ ] 已生成 `snapshots/daily/imported-{date}.md`（冻结快照）。
- [ ] 已写入 `todos/{date}/{owner}.md` 待办文件（来源=import，计划变更次数/延期次数记 0）。
- [ ] 已在 `continuity/import-log.md` 登记导入批次（IMP-YYYYMMDD-NNN）。
- [ ] 导入后按 `references/15-snapshot-rules.md` §5 完成冻结确认。

## 5. 导入校验（完成后）

- [ ] 每个导入任务在待办文件可见。
- [ ] 每个导入任务有对应冻结快照行。
- [ ] 既有任务未被覆盖（不可覆盖规则，见 `references/13-continuity-rules.md` §11）。

## Revision Log

| Time | Change | Reason | Operator |
|---|---|---|---|
