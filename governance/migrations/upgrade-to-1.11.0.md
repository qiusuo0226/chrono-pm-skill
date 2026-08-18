# 升级到 1.11.0

> 从 1.10.2 升级到 1.11.0
> 发布日期：2026-08-11
> Schema 变更：0.5.0 → 0.6.0
> CR 编号：CR-20260811-002

## 变更摘要

主动变更+人工确认更新模式(CR-20260811-002, Minor/contract_change)：事实源更新从悲观确认改为主动写入+标记待确认+登记pending-changes，确认后持久化；权限模型改名(auto_write_low_risk→proactive默认/suggest_only→passive/移除confirm_before_write映射proactive/auto_write_all_except_critical→progressive)；新增运行时索引 pending-changes.md(single/portfolio)；Change Log 分层归档(50行/30天→archive/YYYYMM-change-log.md+index.md)；待确认 Due Date 不参与延期/超期判定(§5a.3空窗期，不新增字段列)；skill-contract #5 与 SKILL.md §7 安全底线 #2 修改(三防线：审计/超时/回滚)；SKILL_BLUEPRINT Impact=full；workspace schema 0.5.0→0.6.0；回归套件新增 PW/CLA 用例

## 新增目录

- `change-log/archive`
- `portfolio/change-log/archive`

## 新增文件

- `pending-changes.md`
- `change-log/index.md`
- `portfolio/pending-changes.md`
- `portfolio/change-log/index.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.11.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.11.0）


## CHANGELOG 摘录

## 1.11.0 — 2026-08-11（已发布 · released）

> 发布归档：CR-20260811-002。基线快照见 `governance/baselines/1.11.0/`，回归见 `governance/regression-reports/rr-20260811-1.11.0.md`。

### Added (contract_change)
- 新增「主动变更 + 人工确认」更新模式（CR-20260811-002, Minor）：事实源更新从悲观确认改为主动写入 → 标记 `Confirmed By: 待确认` → 登记 `pending-changes.md` → 人工确认后持久化生效；确认前在到期判定、已完成统计中一律视为未确认，且支持 7/14 天催办与驳回回滚。
- 新增运行时索引 `pending-changes.md`（单项目 `ai/pending-changes.md`、项目集 `ai/portfolio/pending-changes.md`），作为 Change Log 中待确认条目的子集视图/指针索引；新增 `assets/templates/pending-changes-index-template.md`。
- Change Log 分层归档：活跃区 50 行或超 30 天触发按月归档至 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航；新增 `change-log-index-template.md` 与 `change-log-archive-template.md` 两个模板。
- §5a.3 确认窗口期（待确认 Due Date 空窗期）：待确认记录的 Due Date 不参与延期/超期判定（复用 Confirmed By 值 + pending-changes 索引判定，不新增字段列）。

### Changed (contract_change)
- `governance/contracts/skill-contract.md`：硬约束 #5 修改为「事实源更新必须经过确认、明确触发，或按主动变更模式写入并标记待确认（`Confirmed By: 待确认`）；任何先写后确认的记录必须先登记于 `pending-changes.md`，人工确认后方视为持久化且生效」。
- `SKILL.md`：§7 安全底线 #2 增加主动变更模式路径（低/中风险允许先写后确认，需标记待确认 + 登记 pending + 可回滚），§4 序言补充 pending-changes 说明，frontmatter 版本/schema 同步。
- 权限模型改名：`auto_write_low_risk` → `proactive`（新默认）、`suggest_only` → `passive`、移除 `confirm_before_write`（存量映射 `proactive`）、`auto_write_all_except_critical` → `progressive`；涉及 00/01/10 等规则文件统一枚举。
- 参考规则批量适配：06-file-rules（归档 50 行/30 天 + 待确认注释）、03-task-board（待确认不参与延期计数 + 确认窗口期）、04/07/08（归档对齐 + 概念域 B 注释）、05-query（待确认前置检查 + 聚合 pending 标注）、14-self-check（索引维护 + D11/D12）、19-info-completeness（P0-P3 分级超期）等。

### Compatibility
- Workspace Schema 0.5.0 → 0.6.0：`migrate_workspace.py` 新增 `SCHEMA_060_DIRS`/`PORTFOLIO_060_DIRS`（`change-log/archive`）与 `VERSION_CAPABILITIES` 1.11.0 条目，`check_missing_dirs/files` 模式感知（portfolio vs single）；`scripts/_version.py` 单一版本源 bump。
- 迁移时区分活跃 pending 与历史遗留：仅将 Change Log 中 `Confirmed By: 待确认` 的活跃条目写回 pending-changes，历史已确认条目仅归档。
- 旧工作区降级策略：无 pending-changes 时按既有确认流程工作，不报致命错误。
- 无新增规则文件、无新增字段列、无新增 ID 前缀、无新增操作类型枚举（概念域 B 仅注释说明，不新增 `proactive_change` 枚举）。

### 回归测试
- 用例合计 154 → 163（新增 PW-001~006 待确认窗口期用例 6 个 + CLA-001~003 change-log 归档用例 3 个）。
- 分类：99 positive（94 + PW-001,2,3 + CLA-001,2 = +5）、64 regression（60 + PW-004,5,6 + CLA-003 = +4）。
- UT-001 / SG-001 / SG-002 预期更新，适配主动变更模式与 contract_change。

Blueprint Impact: full — §1 基本信息/能力地图新增 Proactive Change、Pending Index、Change Log Archive；§5 能力矩阵与成熟度统计、§9.1 稳定能力、§11.3 已落地变更追加 1.11.0 行。

---
