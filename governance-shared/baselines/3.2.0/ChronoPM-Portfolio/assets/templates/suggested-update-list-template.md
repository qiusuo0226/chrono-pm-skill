---
doc_type: suggested-update-list
portfolio: [项目集名称]
date: YYYY-MM-DD
status: 草稿
author: AI辅助生成
generated_from: []
updated: YYYY-MM-DDTHH:MM
stale_after: YYYY-MM-DD
---

# 建议更新清单

> 本文件是 ChronoPM-Portfolio 的派生产物，**不是事实源**。列出后须由各目标项目的 ChronoPM-Project 对话执行。本包不得按本清单改 `projects/*/ai`。

## 摘要

- 条目数：
- 涉及项目：
- P0 数：

## 清单

| ID | 目标项目 | 目标文件（相对该项目 ai/） | 建议内容 | 理由与来源 | 优先级 | 状态 |
|---|---|---|---|---|---|---|
| SU-YYYYMMDD-HHmmss | PRJ-001 [项目名] | todos/YYYY-MM-DD/张三.md | 将 TD-xxx 状态改为已阻塞，备注：跨项目依赖未解除 | 集查询 V-4：R-… 仍开放且阻塞该待办 | P0 | 待执行 |
| SU-YYYYMMDD-HHmmss | PRJ-002 [项目名] | resources/resource-register.md | 将王某状态改为请假 YYYY-MM-DD~YYYY-MM-DD | 共享人力漂移：PRJ-001 已请假，本项目仍在岗 | P1 | 待执行 |

## 字段说明

| 字段 | 要求 |
|------|------|
| ID | `SU-{YYYYMMDD}-{HHmmss}`；同秒追加 `-02` |
| 目标项目 | project-index 名称或 PRJ-NNN，必须已登记 |
| 目标文件 | 相对该项目 `ai/`，具体到文件，禁止只写目录 |
| 建议内容 | 可执行改动，禁止空泛「请关注」 |
| 理由与来源 | 触发证据（查询/周报/巡检路径） |
| 优先级 | P0 / P1 / P2 |
| 状态 | 待执行 / 已转交 / 已关闭（关闭仅表示集层跟踪结束，不证明项目侧已写） |

## 执行说明

请到各目标项目的 ChronoPM-Project 对话，携带对应行执行。本包不跟踪成员项目 pending-changes；回访时重新实时读取验证。
