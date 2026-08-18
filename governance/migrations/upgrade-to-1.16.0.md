# 升级到 1.16.0

> 从 1.15.0 升级到 1.16.0
> 发布日期：2026-08-13
> Schema 变更：0.7.0 → 0.8.0
> CR 编号：CR-20260813-002

## 变更摘要

合同作用域与多对多映射(CR-20260813-002, Minor/capability_change + schema_change + contract_change)：新增项目集级 portfolio/requirements/ 跨源需求归集与合同登记册 contract-register（scope_level: portfolio/project/supplement、parent_contract_id、coverage、文档簇关联）；ATOM/Canonical 按 scope_level 存储归属（supplement 跟随父合同）；带合同维度 scope 判定（Canonical 新增伴随字段 contract_refs，scope_scope 5 值枚举不变）；RI 四步检索路由（Step0 读登记册→Step1 合同指向→Step2 目标层级三级索引→Step3 输出 contract_refs）；合同变更三级联动（复用 08 号 scope/cost/requirement，不改概念域枚举）；07号新增§8.9、05号路由扩展、06/09/00/18/14 联动；新增模板 contract-register-template；脚本补齐 config(P1-P3 修复)/workspace_builder/file_registry/migrate(新增 sub_project_dirs/sub_project_files + 子项目遍历，修复 CR-001 遗留项目集 RI 缺口)；SKILL.md §4/§6/§8 与 description 更新；workspace schema 0.7.0→0.8.0(structure-only, island: portfolio/requirements)；回归套件新增 Module 34 Contract Scope(CS-001~017)+RI-012 复核。Blueprint Impact full。

## 新增目录

- `portfolio/requirements/canonical`
- `portfolio/requirements/atoms`
- `projects/{子项目}/requirements/canonical`
- `projects/{子项目}/requirements/atoms`

## 新增文件

- `portfolio/requirements/contract-register.md`
- `portfolio/requirements/source-type-registry.md`
- `requirements/contract-register.md`
- `portfolio/requirements/canonical/canonical-index.md`
- `portfolio/requirements/atoms/atom-index.md`
- `portfolio/requirements/atoms/contractual-index.md`
- `portfolio/requirements/atoms/contractual.md`
- `portfolio/requirements/atoms/procurement-index.md`
- `portfolio/requirements/atoms/procurement.md`
- `portfolio/requirements/atoms/approval-index.md`
- `portfolio/requirements/atoms/approval.md`
- `portfolio/requirements/atoms/compliance-index.md`
- `portfolio/requirements/atoms/compliance.md`
- `portfolio/requirements/atoms/technical-index.md`
- `portfolio/requirements/atoms/technical.md`
- `portfolio/requirements/atoms/operational-index.md`
- `portfolio/requirements/atoms/operational.md`
- `projects/{子项目}/requirements/source-type-registry.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.16.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.16.0）


## CHANGELOG 摘录

## 1.16.0 — 2026-08-13（已发布 · released）

> 发布归档：Minor（合同作用域与多对多映射）。在 v1.15.0 跨源需求归集 RI 之上补齐"合同与子项目多对多"缺口（capability_change + schema_change + contract_change）。workspace schema 0.7.0→0.8.0（structure-only 迁移，新增 portfolio/requirements 与 contract-register）。

### Added
- **contract-register.md 合同登记册**（RI 检索入口事实源）：项目集模式唯一在 `portfolio/requirements/`，单项目在 `requirements/`；字段含 scope_level（portfolio/project/supplement）、parent_contract_id（补充协议必填，D7）、coverage 覆盖对象、关联招投标/立项/密评（文档簇）、status/superseded_by（合同血缘）。
- **项目集级 portfolio/requirements/**：canonical + atoms + 三级索引 + source-type-registry。
- **合同变更三级联动**：合同拆分为两份（旧条 superseded_by 血缘）、范围扩大/补充协议（增量 ATOM(supplement) + scope 重判）、范围缩小（ATOM stale + not_in_scope 重判）；复用 08 号既有 `scope`/`cost`/`requirement` 类型，不改 08 号概念域 B 枚举（D8）。
- **回归套件 Module 34 Contract Scope**（CS-001~017）：覆盖多对多、supplement 跟随父合同、空登记册补录引导（negative）、迁移遍历、合同变更联动、CR-001 遗留修复验证。

### Changed
- **07 号新增 §8.9 合同作用域**：contract-register 结构、ATOM/Canonical 按 scope_level 存储归属（supplement 跟随父合同）、Canonical 跨层归 portfolio（storage_level）、contract_refs 伴随字段（scope_scope 5 值枚举不变）、检索路由、合同变更联动。
- **05 号 RI 路由扩展为四步**：Step0 读 contract-register（空则触发补录）→ Step1 解析合同指向（supplement 经 parent_contract_id 回溯父合同层级）→ Step2 目标层级三级索引 → Step3 输出 scope_scope + contract_refs + 证据链。
- **06 号**：目录树/事实源清单补 portfolio/requirements 与 contract-register（两级）；**09 号**：项目集级职责补跨项目合同/招投标/立项范围登记；**00 号**：意图检测补"合同登记/合同变更"；**18 号**：初始化向导 Step1 多合同循环登记；**14 号**：自查补登记册完整性。
- **契约**：skill.json current schema→0.8.0 + migrations（0.7.0→0.8.0）+ versionHistory；SKILL.md §4 事实源表/§6 RI 路由/§8 CON- 前缀/description 触发词更新；SKILL_BLUEPRINT 合同作用域数据流；skill-contract 事实源/能力扩展。
- **脚本**：_version.py →1.16.0/0.8.0；config.py 修复 P1-P3（PORTFOLIO_DIRS/FACT 加 requirements 与 contract-register、SUB_PROJECT 补 RI 目录与 source-type-registry、ALL_TEMPLATE 补新模板）；file_registry.py create_ri_skeleton 参数化 + create_contract_register + README 补齐；migrate_workspace.py 新增 sub_project_dirs/sub_project_files 键 + 子项目遍历（D10 守卫），修复 CR-20260813-001 遗留的项目集 RI 迁移缺口。
- **模板**：新增 contract-register-template.md；index-formats 补 contract_refs/storage_level/parent_contract_id 列格式。

### Tests
- 回归套件新增 Module 34 Contract Scope（CS-001~017），RI-012 复核（contract_refs 同步）；总计 198→215 用例（198 既有 + 17 新增）。

---
