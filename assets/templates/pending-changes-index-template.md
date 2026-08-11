# 待确认变更索引（pending-changes）

> 本文件是 Change Log 中 `Confirmed By: 待确认` 条目的**子集视图（指针索引）**，非独立数据来源。
> 唯一数据实全在 Change Log；本文件只做导航与计数。路径：单项目 `ai/pending-changes.md`，项目集 `ai/portfolio/pending-changes.md`。
> 维护规则见 `references/14-self-check-rules.md` §2.2/§2.3（D11）与 `references/05-query-rules.md` §1a。

- Skill 版本：1.12.0
- Schema 版本：0.6.0
- 最后更新：YYYY-MM-DD

## 计数

- total_pending：0（与 Change Log 中 `Confirmed By: 待确认` 条目一一对应）
- 超 7 天未确认：0（进入日常提醒）
- 超 14 天未确认：0（升级 critical）

## 待确认条目

| 序号 | Change Log 指针（文件+Change ID） | Change Summary | 原值 | 新值 | Risk Level | Created At | 逾期状态 |
|----|----|----|----|----|----|----|----|
| 1 | `ai/.../tasks/board.md` T-YYYYMMDD-NNN | 任务 Due Date 调整 | 2026-08-11 | 2026-08-18 | low | 2026-08-11 | 正常 |
| 2 | - | - | - | - | - | - | - |

## 已确认条目（最近，供追溯参考）

> 确认后从待确认条目移除；完整记录保留在 Change Log（`Confirmed By: PM 姓名`）。

| 序号 | Change Log 指针 | Change Summary | 最终值 | 确认人 | Confirmed At |
|----|----|----|----|----|----|
| 1 | `ai/.../tasks/backlog.md` T-YYYYMMDD-NNN | 任务新增 | (值) | (PM 姓名) | YYYY-MM-DD |
| 2 | - | - | - | - | - |

## 驳回记录（审计，不删除）

> 驳回时 Change Log 追加"修改原因: 驳回-恢复原值"，AI 恢复事实源原值；此处保留驳回轨迹。

| 序号 | Change Log 指针 | Change Summary | 驳回原因 | 驳回人 | Rejected At |
|----|----|----|----|----|----|
| 1 | - | - | - | - | - |
