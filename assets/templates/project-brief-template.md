---
doc_type: project-brief
project: [项目名 / 项目集名]
version: v1.0
date: YYYY-MM-DD
status: 草稿
author: AI辅助生成
---

# 项目简报 — AI 快速入口

> 本文件是 AI 处理任何用户输入前的**必读文件**。AI 在解析日报、会议纪要、需求文件、评审材料等内容前，必须先读取本文件，以此判断输入内容与当前项目的关联度，确定项目归属和作用范围。
>
> 本文件应保持精炼（建议 ≤ 100 行），只放 AI 快速判断所需的关键信息。详细背景见 `project-context.md`。

## 1. 项目基本信息

- **项目名称**：[项目名 / 项目集名]
- **项目类型**：单项目 / 项目集
- **当前阶段**：M0x [里程碑名称]
- **立项时间**：YYYY-MM-DD
- **启动日期**：YYYY-MM-DD
- **计划完成**：YYYY-MM-DD

## 2. 子项目清单（项目集模式填写）

| 项目ID | 子项目名称 | 一句话描述 | 当前里程碑 | PM | 状态 |
|---|---|---|---|---|---|
| PRJ-001 | [子项目1] | [一句话描述] | M0x | [姓名] | 进行中 |
| PRJ-002 | [子项目2] | [一句话描述] | M0x | [姓名] | 进行中 |
| PRJ-003 | [子项目3] | [一句话描述] | M0x | [姓名] | 进行中 |

## 3. 计划概览

> 仅放一行摘要，明细见各子项目 `plans/PLAN-NNN-{name}.md` 计划文件。

- [子项目1]：0 个计划阶段 / 0 个需求 / 0 名资源
- [子项目2]：0 个计划阶段 / 0 个需求 / 0 名资源
- [子项目3]：0 个计划阶段 / 0 个需求 / 0 名资源

## 4. 团队成员

> 人员当前状态以各子项目 `projects/{子项目}/resources/resource-register.md` 为事实源（v2.0.0 零数据源，项目集层不存人员数据）。
> 此处仅保留指针，不复制完整团队列表，避免与 register 不一致。

→ 人员当前状态：各子项目 `projects/{子项目}/resources/resource-register.md`
→ 人员流转历史：各子项目 `projects/{子项目}/resources/transfer-log.md`
→ 跨项目共享人员：`portfolio/resources/shared-resource-index.md`（只读指针索引）

（旧版 brief 中如已有团队列表，建议在 register 更新后逐步删除冗余信息，替换为本指针。）

## 5. 技术栈与关键约束

- **后端**：[如 Java + Spring Boot]
- **前端**：[如 Vue.js]
- **数据库**：[如 达梦 / 海量]
- **信创要求**：[如 国密算法 / 国产化适配]
- **关键约束**：[如 需通过安全合规评估、需适配政务云环境]

## 6. 管理约定

- **日报截止时间**：每天 18:00 前
- **周报频率**：每周五汇总
- **评审要求**：[如 需求变更需 CCB 审批]
- **风险升级阈值**：[如 高风险 24 小时内升级]

## 7. 文件路由速查

> AI 处理内容时，按此表快速定位目标文件

| 内容类型 | 目标文件 |
|---|---|
| 人员变动 / 请假 / 借调 | `projects/{子项目}/resources/transfer-log.md` + `resource-register.md`（跨项目时同步 portfolio/resources/ 只读索引指针） |
| 新需求 / 需求变更 | `projects/{子项目}/requirements/requirement-register.md` 或 `change-log.md` |
| 任务进展 / 任务完成 | `projects/{子项目}/todos/{date}/{owner}.md` |
| 风险识别 | `projects/{子项目}/risks/risk-register.md`（项目集级 → `portfolio/risks/`）|
| 问题 / 阻塞 | `projects/{子项目}/issues/issue-register.md` |
| 决策 / 结论 | `projects/{子项目}/decisions/decision-log.md` |
| 里程碑变更 | `projects/{子项目}/plans/progress-plan.md` |
| 成本 / 预算变动 | `projects/{子项目}/plans/budget.md`（项目集级 → `portfolio/plans/budget.md`）|
| 日报归档 | `projects/{子项目}/reports/daily/` |
| 会议纪要 | `projects/{子项目}/meetings/`（跨项目 → `portfolio/meetings/`）|

## 8. AI 处理前必读声明

AI 在处理以下任何类型输入前，**必须先读取本文件**：

- 用户粘贴的文本内容
- 用户上传的文件（评审材料、会议纪要、日报、需求文档等）
- 用户口述的项目信息
- 用户要求"记录一下""更新一下""整理到项目里"时

**判断流程：**

1. 读取本文件，获取项目基本信息、子项目清单、团队成员
2. 扫描输入内容，提取关键词（人名、子项目名、需求编号、任务编号等）
3. 与本文件中的信息进行匹配，判断关联度和项目归属
4. 关联度高 → 按 `10-update-trigger-rules.md` 进入更新流程
5. 关联度低 → 提示用户"该内容似乎与当前项目不匹配，请确认是否需要纳入管理"

## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
