---
doc_type: wp-index
project: "{name}"
---

# WP 索引

> 查找加速器，**不是存在性判据**。文件存在性以 `wps/WP-*.md` 为准。
> 索引缺行但文件存在 → D20 补行，不判死、不删除文件。
> 索引有行而文件缺失 → 登记 pm-decisions 交你裁定。
> 新编号 `WP-YYYYMMDD-NNN`；存量短号/中文名不重编。plan_ref / 状态 / 关联需求必须与 WP 文件镜像一致。
> **12 列**（v3.18.0 末尾追加完成时间/废弃时间）。生效不成列。一行只出现在下面三段之一。
> 状态：四枚举镜像头进度；`effect=废弃` 时本列写 `废弃`。
> 默认查询/默认图只读 §1 进行中。

## 1. 进行中

| WP 编号 | WP 名称 | 状态 | plan_ref | 负责人 | 关键阶段 | 关联需求 | 文件路径 | 上游 WP | 下游 WP | 完成时间 | 废弃时间 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WP-YYYYMMDD-NNN | [名称] | 待确认/已规划/进行中 | PLAN-YYYYMMDD-NNN / — | [姓名] | 上线 / — | REQ-xxx / — | wps/WP-YYYYMMDD-NNN.md | WP-xxx / — | WP-aaa / — | — | — |

## 2. 已完成归档

| WP 编号 | WP 名称 | 状态 | plan_ref | 负责人 | 关键阶段 | 关联需求 | 文件路径 | 上游 WP | 下游 WP | 完成时间 | 废弃时间 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WP-YYYYMMDD-NNN | [名称] | 已完成 | PLAN-YYYYMMDD-NNN / — | [姓名] | 上线 / — | REQ-xxx / — | wps/WP-YYYYMMDD-NNN.md | — | — | YYYY-MM-DD | — |

## 3. 废弃归档

| WP 编号 | WP 名称 | 状态 | plan_ref | 负责人 | 关键阶段 | 关联需求 | 文件路径 | 上游 WP | 下游 WP | 完成时间 | 废弃时间 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WP-YYYYMMDD-NNN | [名称] | 废弃 | — | [姓名] | — | REQ-xxx / — | wps/WP-YYYYMMDD-NNN.md | — | — | YYYY-MM-DD / — | YYYY-MM-DD |
