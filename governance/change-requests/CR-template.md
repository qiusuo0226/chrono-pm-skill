# Change Request

## Basic Info

| Field | Value |
|---|---|
| CR ID | CR-YYYYMMDD-NNN |
| Current Version | |
| Current Workspace Schema | |
| Requester | |
| Created At | |
| Change Type | feature / fix / refactor / contract_change / template / test |
| Priority | P0 / P1 / P2 / P3 |
| Status | draft / pending_review / approved / rejected / in_progress / completed / rolled_back |

## Change Goal

> 必须是可验证目标，不允许写"优化一下""更智能""更好用"

## Problem Statement

当前问题：

## Scope

| File | Change Type | Reason |
|---|---|---|

## Non-goals

本次明确不做：

## Acceptance Criteria

1. 
2. 
3. 

## Test Cases

| Case ID | Input | Expected Result | Type |
|---|---|---|---|
| | | | positive / regression / negative |

## Risk Assessment

| Capability | Risk Level | Mitigation |
|---|---|---|

## Approval

- [ ] approved
- [ ] rejected
- [ ] need more info

---

## 升级方案审查文档（AP）

> 本章节为必填项，AI 必须在用户确认前完整输出。详见 `references/16-skill-governance-rules.md` §2.1。

### AP-1. 变更概述

### AP-2. 影响点详细分析

| 影响项 | 当前状态 | 变更后状态 | 影响描述 | 影响程度 | 是否可逆 |
|---|---|---|---|---|---|

### AP-3. 变更策略与设计思路

1. 为什么选择这个方案：
2. 设计思路：
3. 关键决策点：
4. 与现有规则的交互关系：
5. 替代方案对比（至少 1 个被否决的方案）：

### AP-4. 修改范围清单

| 文件 | 修改类型 | 修改内容摘要 | 是否核心契约 |
|---|---|---|---|

### AP-5. 回归测试计划

| Case ID | 模块 | 输入 | 预期结果 | 类型 | 阻断项 |
|---|---|---|---|---|---|

### AP-6. 风险评估与回滚方案

| 风险项 | 发生概率 | 影响程度 | 预防措施 | 回滚方案 |
|---|---|---|---|---|

回滚步骤：
1. 
2. 

### AP-7. 版本影响

| 维度 | 变更前 | 变更后 |
|---|---|---|
| Skill Version | | |
| Workspace Schema | | |
| 是否需要工作区迁移 | | |
| 迁移模式 | | |
| 是否影响核心契约 | | |
| 是否影响已有工作区 | | |

### Blueprint Impact

> 本次变更对 SKILL_BLUEPRINT.md 的影响，详见 `references/16-skill-governance-rules.md` §17。

- [ ] full — 正文内容有实质性更新（能力矩阵、架构决策、数据流等）
- [ ] metadata-only — 仅更新版本号和日期
- [ ] none — 本次变更不影响 Blueprint 内容

Blueprint 更新内容（如选 full 或 metadata-only）：
