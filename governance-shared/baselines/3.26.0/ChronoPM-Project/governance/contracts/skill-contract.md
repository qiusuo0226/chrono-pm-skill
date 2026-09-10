# Skill Contract

> 本文件是 ChronoPM Skill 的核心契约，AI 修改 Skill 时必须先读取本文件，不得违反以下硬约束。

## Skill Purpose

本文件是 **ChronoPM-Project**（单项目管理）核心契约。跨项目归集见 ChronoPM-Portfolio（工人不手搓成员正文；手递须 CALL 本包写过程；高风险走建议更新后手递；聚合不落盘为数据源；人的视图实时聚合）。

## Hard Constraints

1. `ai/` 是事实源目录，`outputs/` 是生成物目录，两者不得混用。
2. 生成文件不得混入 `ai/`，事实源更新不得写入 `outputs/`。**唯一例外（v3.17.0）**：`wps/_wp-chart.md` 是 Index 派生视图（非事实源、非生成物），不走 P-OUTPUT，禁止写入 `outputs/`。
3. 历史项目内容不得直接覆盖当前事实源，必须走衔接流程。
4. 查询类请求必须索引优先，禁止默认创建临时脚本。
5. 事实源更新口径以 `references/00-pm-main-rules.md` §3.3 为单一事实源，本条只锁契约：
   (a) 必须确认级（里程碑/成本/决策/删除覆盖/跨项目镜像；终态默认路径除外）：确认前不写该笔；确认后生效。跨项目镜像=把 A 项目任务写入 B 项目待办，禁止。集层手递到**归属项目**的过程记录走 (b)。
   (b) 直接落库与先写后告知（含白名单 D-23/DF-013、集层手递日报存档/过程性待办/当日能耗）：写入即生效；Change Log 记 `Confirmed By: auto`；不登记 `pm-decisions.md` 块 8「已经写了等点头」；计入到期判定与已完成统计。
   (c) 仅 `Confirmed By: 待确认` 的记录不计入到期判定与已完成统计。
   (d) 确认清单与横幅不得阻断同一轮其他录入、查询、结转、出报。
   (e) `confirmation_level: strict` 时 (b) 恢复为待确认 + 进块 8 子节「已经写了等点头」+ 不进统计。
5a. 不得在本项目待办文件镜像他项目任务。
6. Skill 变更必须先生成变更工单。
7. 未经用户确认，不得修改核心契约层。
8. 任何目录结构变更必须提升 workspace schema 版本。
9. 快照冻结后不可静默覆盖，修改需追加 Revision Log。
10. 同一人同一天只允许一份日报文件，多次提交合并追加不覆盖。

## Fact Source（事实源清单）

### 目录与决策文件（v3.9.0）

| 文件 | 用途 |
|---|---|
| `ai/pm-decisions.md` | PM 决策文件（八块开放项 + 决策记录；懒建，不预建实例） |
| `requirements/_index.md` | 需求检索索引（超 50 条按模块分片；查询先读索引） |
| `logs/ops/_index.md` | 对话过程留痕日期指针（懒建；不是进度事实源） |

### requirements/ 需求领域新增事实源（v1.15.0，CR-20260813-001）

| 文件 | 用途 |
|---|---|
| `requirements/canonical/` | 归并后的规范需求（Canonical），聚合多来源 evidence |
| `requirements/atoms/atom-index` | 需求原子 ATOM 总索引（三级索引 L1） |
| `requirements/atoms/{category}-index` | 需求原子按类别索引（三级索引 L2） |
| `requirements/atoms/{category}` | 需求原子文件（三级索引 L3） |
| `requirements/source-type-registry.md` | 来源类型登记（source_type 注册表，未登记不静默归类） |

### 合同作用域 RI 新增事实源（v1.16.0，CR-20260813-002）

| 文件 | 用途 |
|---|---|
| `requirements/contract-register.md` | 本项目合同登记册（v3.0.0 起各项目一份） |
| `requirements/{type}-source/` | 拆解产物（单簇 ledger 记 source_id + seg 平铺；簇 ID 在登记册） |
| `requirements/canonical/` `requirements/atoms/` | 本项目 RI 归集 |

> v3.0.0：废除「集层唯一登记册、子项目不复制」。跨项目成套文档每项目各存一套；跨项目检索由 Portfolio 遍历+指纹去重。补充协议 parent_contract_id 必填（D7）仍有效，存储随父合同在本项目。

### ai/context/ 项目备忘（v1.15.0，CR-20260813-001）

| 文件 | 用途 |
|---|---|
| `context/project-notes.md` | PM 方法论/干系人/洞察/策略随笔（只追加，低/中风险追加写入，AI 感知+PM 主动双入口） |

## Protected Capabilities

以下能力必须长期保持可用，修改时必须跑对应回归用例：

| Capability | ID | Description |
|---|---|---|
| daily_report | DAILY | 个人/项目日报管理（含合并幂等性） |
| weekly_report | WEEKLY | 本项目周报生成（集周报属 ChronoPM-Portfolio） |
| pm_daily_todo | PMTODO | PM 每日待办（9 章节全景视图） |
| quick_query | QUERY | 快速查询（索引优先） |
| output_artifact | OUTPUT | 输出物管理（批次目录+草稿确认） |
| continuity | CONT | 历史阶段衔接（结转+不可覆盖） |
| resource_management | RES | 资源管理（状态+历史分离） |
| todo_snapshot | SNAP | 计划快照和实际对照 |
| self_check | CHECK | 自查与完整性校验 |
| versioning | VER | 版本管理和兼容性检查 |
| excel_generation | EXCEL | Excel 生成规范 |
| update_trigger | TRIG | 更新意图识别和触发 |
| init_wizard | INIT | 项目初始化向导（六步引导建档） |
| completeness_check | COMPLENESS | 信息完整性巡检与补全提醒（P0-P3分级） |
| cross_source_requirement_intelligence | RI | 本项目 contract-register + atoms/canonical + {type}-source；跨项目由 Portfolio |

## Rule Layer Classification

| Layer | Files | Protection Level |
|---|---|---|
| 核心契约层 | SKILL.md, skill.json, governance/contracts/skill-contract.md, references/00-pm-main-rules.md | 强保护：变更工单 + contract_change + 全量回归 + 用户确认 |
| 执行规则层 | references/01~15 | 受控迭代：变更工单 + 影响分析 + 相关回归 |
| 模板与测试层 | assets/templates/, tests/ | 低风险迭代：记录 CHANGELOG |
| 文档层 | SKILL_BLUEPRINT.md（仅开发者完整仓库，分发包不含） | 轻量治理：普通更新记录 CHANGELOG；结构性变更走 CR |
| 脚本层 | scripts/ | 受控迭代：变更工单 + 语法检查 + 相关回归 |

## Version Rules

| 变更类型 | 版本提升 |
|---|---|
| 核心契约变化 | Major 或 Minor |
| 新增能力或目录结构 | Minor + workspace schema |
| 规则修复 | Patch |
| 仅新增测试或模板 | Patch |

### Schema 版本说明（v3.0.0）

Skill 本体与工作区结构采用两个独立版本号，随契约 diff 联动（D-24 概念分离）：

| 概念 | 载体 | v3.0.0 变化 | 说明 |
|---|---|---|---|
| skill schemaVersion | `skill.json` 顶层 `schemaVersion` | 0.6.0 → **0.7.0** | Skill 包契约/元数据结构版本；双包拆分属架构变更，提升 Minor |
| workspace schema | `scripts/_version.py` `WORKSPACE_SCHEMA_VERSION` | 0.8.0 → **0.9.0** | 工作区目录结构版本；RI 下沉项目级、去集层目录，联邦挂载 ChronoPM-Portfolio |

**现行 workspace schema：0.16.0**（3.15.0：pm-profile `current_operator`；存量数据受控迁移）。两版本号不得混用：Skill 包升级改 schemaVersion；工作区目录结构变更改 workspace schema（硬约束 8）。

## ChronoPM-Portfolio 伴生包契约（v3.0.0）

ChronoPM-Portfolio 为只读归集伴生包（skill name `chrono-pm-portfolio`，modes `viewer`，无 init 脚本），与 ChronoPM-Project 同版本发布、双基线归档。只读五条硬约束：

1. **对成员项目 `ai/` 零写**：不得向任何成员项目的事实源目录写入。
2. **只写 `portfolio/` 归集区**：伴生包自身仅可在归集工作区 `portfolio/` 下产出。
3. **变更走建议更新清单**：需改成员项目数据时，只产出建议更新清单，由成员项目的 ChronoPM-Project 确认后执行。
4. **聚合不落盘为数据源**：跨项目聚合结果仅作为视图产物，不得成为后续计算的事实源。
5. **人的视图实时聚合**：面向人的汇总视图按请求实时聚合生成，不维护常驻副本。

存量 portfolio 工作区（如市监重构项目管理）不在本次拆分迁移范围，原地升级由 `scripts/migrate_workspace.py` 的 is_portfolio 存量兼容分支承载（见 upgrade-to-3.0.0.md）。

## Baseline Rule

> 注：基线规则仅适用于 Skill 完整开发仓库。分发包不含 `governance/baselines/` 与 `tests/`，本条对发行包使用者不适用。

每个稳定版本必须生成基线快照到 `governance/baselines/{version}/`，至少包含 SKILL.md、VERSION、skill.json、references/、tests/regression-suite.md。
