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

# 请你拍板

> 本文件是 ChronoPM-Portfolio 的派生产物，**不是事实源**。列出后须由各目标项目的 ChronoPM-Project 对话执行。本包不得按本文件改 `projects/*/ai`。
>
> **对外只展示「白话摘要」段。** 内部能力名仍为 V-9。禁止对用户说出「建议更新清单」六字。人问「改哪些文件」再给对内表。

## 白话摘要

- 有 {N} 件事需要你点头，涉及 {项目列表}。其中要紧的 {P0 数} 件。
- 例子：{项目A} 里张三那条待办，建议标成卡住，因为跨项目依赖还没解开。
- 例子：{项目B} 花名册里王某还写着在岗，但 {项目A} 已经记他请假，建议两边对齐。

请回编号即可：

1. [一句话背景]
   我建议：……
   A. ……（选了之后会到对应项目对话执行）
   B. ……（选了之后先不动）
   C. 先放着，这题以后再说

回复模板：`1A；2B；3C`

## 对内清单

> 助手留痕。默认不对用户展示本表头。

| ID | 目标项目 | 目标文件（相对该项目 ai/） | 建议内容 | 理由与来源 | 优先级 | 状态 |
|---|---|---|---|---|---|---|
| SU-YYYYMMDD-HHmmss | PRJ-001 [项目名] | todos/YYYY-MM-DD/张三.md | 将 TD-xxx 状态改为已阻塞，备注：跨项目依赖未解除 | 集查询 V-4：R-… 仍开放且阻塞该待办 | P0 | 待执行 |
| SU-YYYYMMDD-HHmmss | PRJ-002 [项目名] | todos/YYYY-MM-DD/_index.md | §1 将王某状态改为请假 YYYY-MM-DD~YYYY-MM-DD | 共享人力漂移：PRJ-001 待办 §0.5 已请假，本项目花名册仍在岗 | P1 | 待执行 |
| SU-YYYYMMDD-HHmmss | PRJ-002 [项目名] | todos/YYYY-MM-DD/王某.md | §0.5 追加请假行 YYYY-MM-DD~YYYY-MM-DD | 与上条同一漂移，人员事实源=待办体系 | P1 | 待执行 |

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
