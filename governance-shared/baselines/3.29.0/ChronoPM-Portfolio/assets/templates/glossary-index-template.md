---
doc_type: glossary-index
portfolio: [项目集名称]
version: v1.0
date: YYYY-MM-DD
status: 草稿
author: AI辅助生成
generated_from: []
updated: YYYY-MM-DDTHH:MM
stale_after: YYYY-MM-DD
---

# 术语指针索引

> **V-12 落点。** 本文件是 `portfolio/context/glossary-index.md` 的指针加速器，**不是词库事实源**。只存指针，不存全文/释义。事实以各成员项目 `context/domain-glossary.md` 表格行为准。收编成功后自动刷新；无后台盯盘。pending 条目不收录。

## 指针表

| 术语 | 标准词 | 出现项目 | G号指针 | 确认状态 | 备注 |
|---|---|---|---|---|---|
| 外资 | 外商投资 | PRJ-001, PRJ-002 | PRJ-001#G001；PRJ-002#G003 | confirmed | — |
| 农专 | 农民专业合作社 | PRJ-001 | PRJ-001#G002 | confirmed | — |
| 企信码 | 企信码 / 企业码 | PRJ-001, PRJ-003 | PRJ-001#G010；PRJ-003#G004 | confirmed | 漂移：标准词不一致，待集经理裁决 |

> 列约束：本表 ≤6 列（硬上限 7）。G 号指针格式 `{PRJ-NNN}#{G号}`，指向该项目 `context/domain-glossary.md` 对应行。禁止把释义、context_hint、命中次数写入本表。

## 字段说明

| 字段 | 说明 |
|---|---|
| 术语 | 原词（各项目词库表格「原词」列） |
| 标准词 | 该原词在各项目已确认的标准名；跨项目不一致时并列并在备注标漂移 |
| 出现项目 | 已收编且词库含该词的 PRJ-NNN |
| G号指针 | 各项目条目编号，只作导航 |
| 确认状态 | 集层只收录 confirmed |
| 备注 | 漂移 / stale / 刷新提示；禁止写定义全文 |

## 刷新规则

- 触发：V-1 收编成功（自动，不再问第二次）；或集经理说「刷新术语索引」。
- `{名}/ai/` 缺失或未点头收编 → 不写入本表。
- 查询：先本表，再按指针去项目词库表格行取证；指针失效 → 标 stale，提示刷新。

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
