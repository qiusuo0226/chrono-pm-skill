# 升级到 2.0.0

> 从 1.21.0 升级到 2.0.0
> 发布日期：2026-08-17
> Schema 变更：无
> CR 编号：—

## 变更摘要

待办查询体系重构(Major/architecture_change)：删除任务看板(board)体系，全面转向待办文件体系。删除 03-task-board-rules.md；精简 15-snapshot-rules.md 为仅保留 external_import + 快照读取；待办文件 todos/{date}/{owner}.md 成为执行状态唯一事实源；PLAN 文件成为计划编排唯一事实源；项目集层零数据源原则（仅保留指针索引 + 只读聚合视图）；倒排计划拆分为子项目级别；共享人力软兖底（T1 排期冲突提示 + T3 属性变更提示）；统一门禁达成度聚合（实时聚合不落盘）；M01-M12 作为参考框架不设独立检查项；entity-registry 保留现状。双 Agent 十轮审核收敛，累计 68 项问题修复。workspace schema 保持 0.8.0。

## 新增目录

- `todos`
- `projects/{子项目}/todos`

## 新增文件

- 无

## 删除文件/目录

- `tasks/board.md` / 里程碑板 / 旧待办索引（personal-todo-index/history-index）/ snapshots/ / actuals/ — v2 待办文件体系重构，存量按 09 号 §5 归档 `archive/v1-legacy/` 只读保留
- `tasks/iteration-register.md` — 迭代登记册由 PLAN 计划文件替代（归档+删除）
- `tasks/backlog.md` 与 `tasks/_historic/` — 不归档直接删除（升级方案 §7.3.3 强约束；_historic 若含历史 board 数据建议随 board 一并归档）；完成后删除空的 `tasks/` 目录
- `reviews/` — §7.3.2a 特殊处理后删除：index.md（空表）直接删；lessons-learned.md 由 AI 基于历史待办自动总结经验教训写入 `portfolio/reports/lessons-learned.md` 后删除原文件；评审内容迁入对应人员 todos/ 备注/工作日志段
- `logs/`、`prompts/` — v1 机制废弃，不归档直接删除（升级方案 §7.3.3）；⚠ 例外：migration-log.md 为 v2 活跃迁移记录，保留；prompts/project-rules.md 若含有效项目规则，先迁入 `context/project-rules-migrated.md` 再删
- 16 个 v1 模板（task-board/iteration-register/milestone-board/todo 索引/快照/actuals/delay-stats/pm-daily/personal-progress/personal-daily/project-daily 等）— Skill 源模板层删除

## 规则变更

详见下方 CHANGELOG 摘录（2.0.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 2.0.0）


## CHANGELOG 摘录

## 2.0.0 — 2026-08-17（本次发布 · released）

> 发布归档：Major（项目集零数据源 + 待办文件唯一事实源体系重构）。⚠ 破坏性架构变更，升级须执行存量数据迁移。双 Agent 审核十轮收敛（V2.0→V2.10，B 终审通过-可执行）。核心升级：解决旧体系"多源双写、数据不一致"顽疾——删除 board/迭代登记册/里程碑板/旧待办索引等旧体系，执行状态唯一事实源切换为 `todos/{date}/{owner}.md` 每人每日待办文件 + `_index.md` 绑定文件；项目集层零数据源（实体下放子项目，项目集只留指针索引）；状态枚举全中文；里程碑并入 WP；PM Profile 增姓名字段。workspace schema 保持 0.8.0，但属破坏性变更，需按 09 号 §5 执行存量数据迁移（旧文件归档 v1-legacy 只读保留）。

Blueprint Impact: full（架构重构）

### Added
- **待办文件唯一事实源（todos/{date}/{owner}.md + _index.md）**：替代旧 board/迭代登记册；PLAN 文件承载计划编排（WP 粗规划表，唯一计划事实源）；WP 进度 = 待办文件按 WP Ref 实时聚合。
- **三个新模板**：plan-template.md（计划文件，含 WP 清单/门禁/资源统筹）、personal-daily-todo-template.md（每人每日待办文件，含 9.1 全字段）、daily-todo-binding-template.md（当日绑定 _index.md，含共享人力软兜底提示）。
- **PM Profile 姓名字段（pm_name，21 号 §2.4）**：用于"我"的身份推导与 TD 编号人名缩写段。

### Changed
- **项目集层零数据源（09 号重写）**：资源/预算/里程碑/风险等实体下放子项目；项目集层只留 shared-resource-index / transfer-index 等只读指针索引；T1/T3 共享人力跨项目排期提示软兜底。
- **状态枚举全中文（00 号 §5a）**：需求/待办/风险/问题/变更/WP 六类状态全部中文化（待处理/进行中/待评审/已完成/已阻塞/已取消/已转出等）。
- **里程碑并入 WP（需求 C）**：里程碑=里程碑型 WP，不再独立枚举。
- **删除 03 号规则 + 16 个废弃模板**；05 号查询路由整体改指待办文件与子项目事实源。
- **迁移脚本适配（config/file_registry/migrate_workspace）**：只做版本/模板/目录补缺；存量数据迁移由 AI/PM 按 09 号 §5 执行。

### Notes
- ⚠ 破坏性架构变更：升级前必须先按方案 11.5 / 09 号 §5 执行存量数据迁移（读取旧 board/索引 → 生成草案 → PM 确认 → 落 todos/{date}/{owner}.md → 下放 portfolio 实体 → 建项目集索引 → 旧文件归档 v1-legacy），否则升级后 AI 按新规则读子项目 todos/ 会找不到存量数据（读取断层）。
- workspace schema 保持 0.8.0（无 schema 版本号变更），但文件结构与数据源发生根本重构。
- 方案经十轮 B 审核收敛（V2.0→V2.10）；关键决策链：待办唯一事实源 → 项目集零数据源（用户最高优先级架构决策）→ 状态中文 → 里程碑=WP → 倒排计划拆分三子项目。

---
