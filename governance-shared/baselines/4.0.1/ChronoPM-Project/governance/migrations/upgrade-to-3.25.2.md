# 升级到 3.25.2

> 从 3.25.1 升级到 3.25.2  
> 发布日期：2026-09-04  
> Schema：保持 **0.16.0**  
> CR：CR-20260904-003  
> IA：IA-20260904-003  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（仅 Project description）。  
> 回归合计 **909**（905+4）。

## 变更摘要

Project「触发：」补工作包、计划、项目、结转、派活等单项目口语。Portfolio 触发列表与 §2 硬闸不改。匹配层双命中可接受。

## 施工禁区

- 禁止改 §2 三态硬闸
- 禁止改 Portfolio「触发：」
- 禁止改写 `baselines/3.25.1/`
- 禁止升 schema / 新规则文件 / 代更 Grok
- 发布删 AP

## A. 施工

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR / IA / 本文件 / migrations-history / Portfolio 锁步指针 / migrations README | 治理 |
| A2 | Project SKILL.md description、skill.json description | 扩词 |
| A3 | `_version.py` 3.25.2 + sync_version | 锁步 |
| A4 | 两包 CHANGELOG、BLUEPRINT §11.3、README 用例 909 | 文档 |
| A5 | Module 83 TR-015～018 | 回归 |
| A6 | `baselines/3.25.2/` 新建；不改 3.25.1 基线；删 AP；audit；打包 |

## 验证

P 触发含工作包/计划/项目；F 触发无这些裸词；硬闸原文不变；audit 17/17。
