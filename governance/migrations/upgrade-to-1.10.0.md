# 升级到 1.10.0

> 从 1.9.0 升级到 1.10.0
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

历史计划全量同步与变更追溯(CR-20260810-008, Minor/contract_change)：新增 CAP-024、R1-R4。R1 历史计划批量导入(.pod/Excel→external_import冻结快照+history登记)；R2 计划变更追踪(board新增Original Due Date/Plan Change Count/Delay Count字段+概念域B追加plan_change)；R3 延期计数与聚合(概念域A/B拆分、A类计数只读board单文件、B类超期实时计算+索引优先)；R4 聚合查询路由(05新增§6.5计数路由/§6.6状态路由)；13号新增R1边界判定表；00意图检测新增4路由；9模板+2新模板(plan-import/delay-stats)；回归套件新增第25模块

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.10.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.10.0）


## CHANGELOG 摘录

## 1.10.0 — 2026-08-10

### Added
- 新增 CAP-024：历史计划全量同步与变更追溯（R1-R4）
- R1 历史计划批量导入：将存量计划（.pod / Excel / 遗留 board 导出）经 `references/15-snapshot-rules.md` §8a 固化为 external_import 冻结快照（`snapshots/daily/imported-{date}.md`），登记 `history-index.md`，并联动写入 board（Source=import）
- 新增 `assets/templates/plan-import-template.md`：R1 批量导入工作表
- 新增 `assets/templates/delay-stats-template.md`：A 类延期/变更统计表
- 回归套件新增第 25 模块「Historical Plan Import & Change Tracking」（HP-001 ~ HP-017，17 用例：11 正向 / 6 回归）

### Changed (contract_change)
- `references/03-task-board-rules.md`：board 新增字段 Original Due Date（不可变）/ Plan Change Count / Delay Count；新增 §1a 计数字段判定、§5a B 类超期判定与追责归属（确认窗口期/负责人变更/双触发时机/索引优先）；§7 补概念域说明
- `references/15-snapshot-rules.md`：新增 §8a external_import 批量导入快照规则；source_type 统一为 4 值（personal_daily_reports/pm_todo/meeting/external_import）
- `references/05-query-rules.md`：新增 §6.5 聚合计数路由（A 类，只读 board 单文件）、§6.6 状态查询路由（B 类，实时计算 + 索引优先）；查询类型表/Quick Query 表补 R1-R4 行
- `references/08-change-control-rules.md`：概念域 B 枚举追加 `plan_change`（requirement/scope/schedule/cost/resource/plan_change）；新增 §1.1 概念域说明（与概念域 A 不合并）
- `references/13-continuity-rules.md`：新增 §2 与 R1 的边界判定表（按是否独立历史工作区路由 13 号或 R1）
- `references/00-pm-main-rules.md`：§2.7 意图检测新增 4 路由（历史计划批量导入/计划变更追踪/延期统计/超期查询）
- `SKILL.md`：压缩至 248 行（MN-1），§6 路由表/§15 索引表补 R1-R4 条目，frontmatter version → 1.10.0
- 模板层：task-board（字段映射表）/ change-log（plan_change）/ index-formats（概念域注释）/ daily-todo-snapshot / daily-todo-actuals / weekly-todo-snapshot / weekly-todo-actuals / todo-history-index（外部导入登记）/ import-log 共 9 个模板更新

### Compatibility
- Workspace Schema 保持 0.5.0（不变，无迁移）
- 不删除、不弱化 CAP-001 ~ CAP-023
- 旧工作区 board 无计数字段时缺省按 0 处理；聚合查询可回退 Change Log 并标注"推断，未确认"
- `daily_reports` 作为 `personal_daily_reports` 的兼容旧值保留
- 不影响事实源内容准确性和安全底线

### 回归测试
- 用例合计 132 → 149（新增第 25 模块 17 用例，11 正向 / 6 回归）
- BP-002 硬编码版本 1.7.1 → 1.10.0；BP-003 规则文件数 17 → 22（00-21）
- SK-1E 规则索引计数更新为 00-21（共 22 条）
- FC-1A/SK-1A 行数校验：SKILL.md=248、06=292、15=297、05=276、08=196、13=280、00=262 均 ≤300

Blueprint Impact: full — §1 基本信息、§5.2 能力矩阵追加 CAP-024、§5.3 成熟度统计更新、§7.1/§7.2 规则清单与依赖、§8 数据流、§9.1 稳定能力、§11.3 已落地变更追加 1.10.0 行

---
