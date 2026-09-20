---
doc_type: plan-index
project: "{name}"
derived: true
---

# 计划索引

> 查找加速器，**不是存在性判据**。存在性以 `plans/PLAN-*.md` 为准。
> 索引缺行但文件存在 → D43 补行，不判死、不删除文件。
> 索引有行而文件缺失 → 登记 pm-decisions。
> 列与 PLAN YAML 镜像；缺锚点写 `—`。存量不改文件名。
> **纯查询缺本文件**：提示一次是否重建；未同意则读 PLAN 标题/§1，禁止查询中全量扫描（14 §2.1）。
> 写入 / P-VIEWS / 用户同意重建时按本模板建或覆盖。

## 1. 正常

| PLAN 编号 | 名称 | status | business_modules | time_window | batch | scope_include | scope_exclude | related_plans | 文件路径 |
|---|---|---|---|---|---|---|---|---|---|
| PLAN-YYYYMMDD-NNN | [名称] | 正常 | 开办/变更 / — | 2026-10-01~10-07 / — | 国庆 / — | — | 外企主体 / — | PLAN-… (mutually_exclusive) / — | plans/PLAN-YYYYMMDD-NNN-{name}.md |

## 2. 废弃

| PLAN 编号 | 名称 | status | business_modules | time_window | batch | scope_include | scope_exclude | related_plans | 文件路径 |
|---|---|---|---|---|---|---|---|---|---|
| PLAN-YYYYMMDD-NNN | [名称] | 废弃 | — | — | — | — | — | superseded_by=PLAN-… / — | plans/PLAN-YYYYMMDD-NNN-{name}.md |
