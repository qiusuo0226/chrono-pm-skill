---
name: chrono-pm-source-split
description: ChronoPM-Project 源文档拆解能力边界清单。清单性文件，非运行时加载入口。宿主不得把本目录当作独立 Skill 发现。
---

# source-split-skill — 能力边界清单（非加载入口）

> **清单性文件，非加载入口。** 规则权威仍在 `ChronoPM-Project/references/07` 等原文件。本目录不参与运行时规则加载。未来独立成包时按 `references/` 清单搬迁。

## 定位

把源文档拆成 `requirements/sources/{编号}/` 六件套（meta/_digest/atoms/facts/ledger/parse-log），服务 REQ↔WP 绑定与跨项目同源互认。

## 触发词

拆解、源文档、对账、查重、二次拆解、重拆、parse-log、同源。

## 输入 / 输出

- 输入：PM 提供的源文档指针（不入库原文）+ 可选版本。
- 输出：`sources/{编号}/` 目录 + `_index.md` 行 + REQ SUGGEST + 术语候选攒批。

## 独立化红线

拆解能力不得反向依赖 PM 日报/待办等无关模块。唯一允许的交叉点：REQ/WP 编号体系、术语入流（17 号）。详见 `references/`。
