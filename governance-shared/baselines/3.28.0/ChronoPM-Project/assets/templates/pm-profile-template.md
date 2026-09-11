---
doc_type: pm-profile
project: "[项目名或项目集名]"
pm_name: "[项目经理，1～2 位：张三 或 张三 / 李四]"
current_operator: ""
confirmation_level: normal
version: v1.0
date: YYYY-MM-DD
status: 活跃
---

# PM 偏好档案

> 本文件由 ChronoPM 技能自动维护。AI 在每次交互中被动观察用户行为，自动写入 pending 偏好，经用户确认后升为 confirmed。
>
> **pm_name**：项目基本信息里的项目经理（1～2 位，斜杠分隔）。不是「我」。禁止按 todos 岗位自动填充。
> **current_operator**：当前操作人。查「我的待办」只认此字段。空则 ASK「请问您是？」，禁止回退 pm_name。
>
> 用户也可手动编辑本文件。手动编辑后，AI 会在下次加载时检测格式一致性。

## 1. 偏好映射表

> **内置默认偏好**（DF-NNN）：系统内置行为基线，用户可覆盖或禁用，**不可删除 DF 行**。禁用后状态记 `disabled`（仅 DF 可用），行仍留在本表；**禁止将 DF 行移入 §3**。
> **用户自定义偏好**（PF001、PF002...）：通过交互学习到的偏好。
> 两套编号互不干扰。

| 编号 | 类别 | 偏好项 | 偏好值 | 状态 | 加载场景 | 来源 | 首次观察 | 最近观察 | 观察次数 | 备注 |
|------|------|--------|--------|------|---------|------|---------|---------|---------|------|
| DF-001 | P-OUT | 待确认问题编号 | 必须 1/2/3/4/5 编号罗列 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 便于逐条作答 |
| DF-002 | P-CFM | 可关闭项确认关闭 | 日报后罗列可关闭的风险/问题，明确到具体编号（I-XXXX/R-XXXX）并附详细描述和佐证，PM 确认后才改库 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 关闭必须佐证 |
| DF-003 | P-WRK | PM 同步进度自动记日报 | 白天 PM 同步的成员进度自动记为当日日报；晚间自写日报作为补充自动合并；歧义编号罗列确认 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 日报合并机制 |
| DF-004 | P-WRK | 查询必须实读文件 | PM 说"再查一下/查一下"时必须实际重读事实源文件，不得凭记忆或缓存，以实读结果为准并说明差异 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 与 CQ-5 互补 |
| DF-005 | P-STY | 禁止内部文件术语 | 向 PM 提问或建议不用 board/Task N 等术语，用通俗语言解释文件用途并给推荐方案 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 沟通面向 PM |
| DF-006 | P-STY | 操作建议说人话 | 提操作建议不抛技术术语，需讲清改哪个字段、改成什么值、效果是什么 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 可操作性优先 |
| DF-007 | P-WRK | PM 待办只记本人 | PM 待办只记本人要动手的事，不为成员新增待办自动生成跟进条 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 不自动生成跟进条 |
| DF-008 | P-WRK | 日报联动待办文件 | 每次更新日报时同步更新待办文件 `todos/{date}/{owner}.md`、需求登记册，并更新本项目日报；禁止引用已删除的 board | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 非 board |
| DF-009 | P-WRK | 核对联动提醒 | 每日核对日报时对比计划日期与日报、对比问题与风险，告知关闭/新增/需跟进；紧急待跟进内容只要与 PM 对话就提醒一次 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | |
| DF-010 | P-WRK | 梳理主动提问 | 梳理日报时主动提出疑问点与分析思路，结合风险/问题/计划/里程碑多角度审视 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | |
| DF-011 | P-OUT | 完整引用 | 引用任务须写出项目名称+归属计划（PLAN）+任务完整名称，禁止缩略写法 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | |
| DF-012 | P-OUT | 查询默认未办结 | 待办清单查询默认仅输出未办结（待处理/进行中/已阻塞）；已办结规范见 05 号；展开须显式触发词 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 见 05 号 |
| DF-013 | P-WRK | 日报100%自动完成 | 日报填写 100% 或「已完成」时对应待办自动改为已完成（先写后告知，`Confirmed By: auto`，计入统计，见 00 §3.3）；进度不足 100% 不自动关单 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | |
| DF-014 | P-WRK | 间接配合进出组 | 间接配合人员进出组：当日有日报=进组/在岗，当日无日报不自动离组；判定落点为待办 §0.5；不得写具体人名 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 无具体人名 |
| DF-015 | P-CFM | 一次问完 | 待确认事项必须同一轮一次问完（按类分组、编号+背景+选项、回复模板）；完整协议见 21 号 §5.1b | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 指向 §5.1b |
| DF-016 | P-WRK | 非本项目不入库 | 成员日报/口述中属于其他项目的工作，本项目不建待办、不写日报存档以外的事实源 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | |
| DF-017 | P-OUT | 数据来源标注 | 回复涉及文件读取/改动/移动时打印路径（查询出数据来源，写入出已写路径）；禁罗列扫描过程 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 见 00 号 §9.0 |
| DF-018 | P-CFM | 主动识别习惯 | 每轮结束主动观察偏好；连续 3 次一致 → pending + SUGGEST；每轮最多 1 条；不打断主任务 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 见 21 号 §5.1 |
| DF-019 | P-OUT | 待绑定/待确认提醒简洁 | 待办未绑定 WP 等提醒必须编号清单直问，禁止长段落解释工作包定义 | confirmed | — | built-in default | YYYY-MM-DD | YYYY-MM-DD | — | 见 00 号 §8b |

> 字段说明：
> - **编号**：两套编号体系互不干扰——内置默认偏好为 DF-NNN（DF-001 起，系统预填）；用户自定义偏好为 PF + 三位数字（PF001、PF002...），全局唯一递增
> - **类别**：P-OUT（输出格式）/ P-FOC（管理重点）/ P-STY（沟通风格）/ P-WRK（工作流）/ P-CFM（确认行为）
> - **状态**：confirmed / pending / rejected / conflict / deprecated / disabled（仅 DF；禁用留痕，行不删除、不移入 §3）
> - **加载场景**：PF 行填 `P-ALWAYS` / `P-REPLY` / `P-WF-{N}`（缺省或无本列 = `P-ALWAYS`）。**DF 行本列填 —**（标签只在 21 号 §5.1a 主表，不存实例）
> - **来源**：首次观察的交互内容摘要或用户明确声明
> - **首次观察 / 最近观察**：YYYY-MM-DD 格式
> - **观察次数**：累计观察到该偏好的次数

## 2. 待确认偏好

| 编号 | 类别 | 偏好项 | 候选值 | 观察依据 | 首次观察 | 最近观察 | 观察次数 | 状态 |
|------|------|--------|--------|---------|---------|---------|---------|------|

> 待确认偏好表用于存放自动推断中（1-2 次行为）的候选偏好，尚未达到 pending 写入阈值（3 次）。
> 达到 3 次一致行为后，迁移到偏好映射表，状态标记为 pending。

## 3. 已否决 / 已废弃偏好

| 编号 | 类别 | 偏好项 | 原偏好值 | 状态 | 处理原因 | 处理时间 | Source |
|------|------|--------|----------|------|----------|----------|--------|

> 此表记录被用户否定（rejected）或废弃（deprecated）的偏好，便于后续恢复参考。

## 4. 索引

### 4.1 按类别索引

| 类别 | 编号范围 | 偏好项数 |
|------|---------|---------|

### 4.2 按状态索引

| 状态 | 数量 |
|------|------|

## Change Log

| Date | Change Type | Description | Source |
|------|-------------|-------------|--------|

> Change Type 取值：auto-detected（自动发现）、confirmed（用户确认）、modified（用户修正）、rejected（用户否定）、restored（用户恢复）、deprecated（用户废弃）、manual-edit（手动编辑）
