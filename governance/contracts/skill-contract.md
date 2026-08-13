# Skill Contract

> 本文件是 ChronoPM Skill 的核心契约，AI 修改 Skill 时必须先读取本文件，不得违反以下硬约束。

## Skill Purpose

本 Skill 用于项目集/项目管理，支持日报、周报、任务、风险、问题、资源、输出物、历史衔接、待办查询、计划快照、自查校验等管理场景。

## Hard Constraints

1. `ai/` 是事实源目录，`outputs/` 是生成物目录，两者不得混用。
2. 生成文件不得混入 `ai/`，事实源更新不得写入 `outputs/`。
3. 历史项目内容不得直接覆盖当前事实源，必须走衔接流程。
4. 查询类请求必须索引优先，禁止默认创建临时脚本。
5. 事实源更新必须经过确认、明确触发，或按主动变更模式写入并标记待确认（`Confirmed By: 待确认`）；任何先写后确认的记录必须先登记于 `pending-changes.md`，人工确认后方视为持久化且生效，未经确认的记录在到期判定、已完成统计中一律不视为已确认。
6. Skill 变更必须先生成变更工单。
7. 未经用户确认，不得修改核心契约层。
8. 任何目录结构变更必须提升 workspace schema 版本。
9. 快照冻结后不可静默覆盖，修改需追加 Revision Log。
10. 同一人同一天只允许一份日报文件，多次提交合并追加不覆盖。

## Fact Source（事实源清单）

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
| `portfolio/requirements/` | 项目集级跨源需求归集目录（canonical/ + atoms/ + 索引） |
| `portfolio/requirements/contract-register.md` | 合同登记册（项目集模式唯一）；scope_level / parent_contract_id / coverage / 文档簇关联 |
| `portfolio/requirements/source-type-registry.md` | 项目集级来源类型登记 |
| `requirements/contract-register.md`（单项目模式） | 合同登记册（单项目无 portfolio 分层） |

> 项目集模式下合同登记册唯一在 `portfolio/requirements/`，子项目不复制（D4）；补充协议（supplement）登记在对应模式的登记册中，parent_contract_id 必填（D7）。

### ai/context/ 项目备忘（v1.15.0，CR-20260813-001）

| 文件 | 用途 |
|---|---|
| `context/project-notes.md` | PM 方法论/干系人/洞察/策略随笔（只追加，低/中风险追加写入，AI 感知+PM 主动双入口） |

## Protected Capabilities

以下能力必须长期保持可用，修改时必须跑对应回归用例：

| Capability | ID | Description |
|---|---|---|
| daily_report | DAILY | 个人/项目日报管理（含合并幂等性） |
| weekly_report | WEEKLY | 周报生成和项目集汇总 |
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
| cross_source_requirement_intelligence | RI | 跨源需求归集：拆词/归并/范围判定/三级索引检索（requirements/atoms + canonical + source-type-registry），CR-20260813-001；合同作用域扩展：portfolio/requirements 层级存储 + contract-register 合同登记册 + 按 scope_level 路由 + 带合同维度 scope 判定（contract_refs），CR-20260813-002 |

## Rule Layer Classification

| Layer | Files | Protection Level |
|---|---|---|
| 核心契约层 | SKILL.md, skill.json, governance/contracts/skill-contract.md, references/00-pm-main-rules.md | 强保护：变更工单 + contract_change + 全量回归 + 用户确认 |
| 执行规则层 | references/01~15 | 受控迭代：变更工单 + 影响分析 + 相关回归 |
| 模板与测试层 | assets/templates/, tests/ | 低风险迭代：记录 CHANGELOG |
| 文档层 | SKILL_BLUEPRINT.md | 轻量治理：普通更新记录 CHANGELOG；结构性变更走 CR |
| 脚本层 | scripts/ | 受控迭代：变更工单 + 语法检查 + 相关回归 |

## Version Rules

| 变更类型 | 版本提升 |
|---|---|
| 核心契约变化 | Major 或 Minor |
| 新增能力或目录结构 | Minor + workspace schema |
| 规则修复 | Patch |
| 仅新增测试或模板 | Patch |

## Baseline Rule

每个稳定版本必须生成基线快照到 `governance/baselines/{version}/`，至少包含 SKILL.md、VERSION、skill.json、references/、tests/regression-suite.md。
