---
doc_type: work-package
wp_id: WP-NNN
project: [子项目名]
plan_ref: PLAN-NNN
status: 已规划
is_milestone: false
created_at: YYYY-MM-DD
---

# WP-NNN - {WP 名称}

## 1. 基本信息
| 字段 | 值 |
|---|---|
| WP 编号 | WP-NNN |
| WP 名称 | [名称] |
| 是否里程碑 | 是/否 |
| 所属阶段 | M0X |
| 负责人 | [姓名] |
| 执行人 | [自动聚合下辖待办 owner，纯派生不落盘] |
| 开始时间 | YYYY-MM-DD |
| 结束时间 | YYYY-MM-DD |
| 所属计划 | PLAN-NNN |
| 关联需求 | REQ-xxx / — |

## 2. 关联需求（强制字段）
| 需求编号 | 描述 | 来源文件 |
|---|---|---|
| REQ-xxx | [描述] | requirement-register.md / contract-register.md |

> 未找到需求出处时填 `—`，并按 WF-8 溯源流程 ASK：是否仍创建（将登记需求蔓延风险）。存量 WP 空值不强制回填。

## 3. 阶段明细（可选，复杂 WP 展开）

| 阶段 | 时间区间 | 关键动作 | 出口条件 |
|---|---|---|---|
| M0X | YYYY-MM-DD ~ YYYY-MM-DD | [动作] | [条件] |

## 4. 下辖待办（派生视图，AI 实时聚合）

> 从 `todos/{date}/{owner}.md` 按 WP Ref 实时聚合，**不落盘**。改待办 WP Ref **不得**回写本段。

## 5. 风险/问题（可选）
| Ref | 类型 | 描述 | 状态 |
|---|---|---|---|
| R-xxx / I-xxx | 风险/问题 | [描述] | [状态] |

> 04 号不加回指。本表为可选正向指针。

## 6. 变更记录
| 时间 | 变更内容 | 原因 | 操作人 |
|---|---|---|---|
| YYYY-MM-DD | [变更] | [原因] | [姓名] |
