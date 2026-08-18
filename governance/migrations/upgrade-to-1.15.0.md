# 升级到 1.15.0

> 从 1.14.0 升级到 1.15.0
> 发布日期：2026-08-13
> Schema 变更：0.6.0 → 0.7.0
> CR 编号：CR-20260813-001

## 变更摘要

跨源需求归集与判定 RI(CR-20260813-001, Minor/capability_change + schema_change)：07号新增跨源证据链/ATOM→Canonical→REQ三层模型/scope_scope范围判定/双层来源分类(source_category 6类固定+source_type项目级可扩展source-type-registry)/kind四类型(需求/要求/约定/约束)全链路拆解；新增三级索引(L1路由/L2类别倒排含norm_text覆盖索引/L3全文)+分级加载+P1语义兜底(词库同义词扩展/norm_text扫读/降级提示)；PM随笔project-notes双入口(AI主动感知+PM主动)；workspace schema 0.6.0→0.7.0(requirements/canonical、atoms、source-type-registry)+迁移脚本；新增模板 source-type-registry/project-notes，register新增Canonical ID/scope_scope列，milestone-board新增合规门禁列；回归套件新增Module 32(RI-001~006)/Module 33(PN-001~002)。不新增独立规则文件/CAP/状态机。

## 新增目录

- `requirements/canonical`
- `requirements/atoms`

## 新增文件

- `requirements/source-type-registry.md`
- `requirements/canonical/canonical-index.md`
- `requirements/atoms/atom-index.md`
- `requirements/atoms/contractual-index.md`
- `requirements/atoms/contractual.md`
- `requirements/atoms/procurement-index.md`
- `requirements/atoms/procurement.md`
- `requirements/atoms/approval-index.md`
- `requirements/atoms/approval.md`
- `requirements/atoms/compliance-index.md`
- `requirements/atoms/compliance.md`
- `requirements/atoms/technical-index.md`
- `requirements/atoms/technical.md`
- `requirements/atoms/operational-index.md`
- `requirements/atoms/operational.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.15.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.15.0）


## CHANGELOG 摘录

## 1.15.0 — 2026-08-13（已发布 · released）

> 发布归档：Minor（跨源需求归集与判定 RI）。新增"需求在不在合同/招投标/立项范围内"的取证与归集能力（capability_change + schema_change）。workspace schema 0.6.0→0.7.0（结构变更，需迁移）。

### Added
- **07 号新增跨源需求归集章节**：ATOM（证据层）→ Canonical（归并层）→ REQ（管理层）三层数据模型；ATOM schema（kind/source_type/authority/raw_text≤500字/supersedes/norm_text）；Canonical 归并 + evidence 证据链 + scope_scope 范围判定 + evidence_stale。
- **双层来源分类**：source_category 固定 6 类（contractual/procurement/approval/compliance/technical/operational）+ source_type 项目级可扩展（source-type-registry.md）。
- **kind 四类型**（需求/要求/约定/约束）统一链路拆解；密评 compliance 强制门禁；里程碑复用 milestone-board 并新增合规门禁列。
- **三级索引**（L1 路由 / L2 类别倒排含 norm_text 覆盖索引 / L3 全文）+ 分级加载（单次范围判定 ≤400 行，对齐 05 号最小读取）+ P1 语义兜底（词库同义词扩展 / norm_text 扫读 / 降级提示）。
- **PM 随笔 project-notes**：AI 主动感知 + PM 主动要求双入口，只追加时间线。

### Changed
- **17 号**：术语级 vs 句子级归一边界（§6.4）；**05 号**：跨源范围判定查询路由 + 分级加载对齐；**00 号**：RI 意图 + 备忘建议输出点；**06 号**：canonical/atoms(L1/L2/L3)/source-type-registry 目录与归档、拆分阈值适配。
- **模板**：register 新增 Canonical ID + scope_scope 列；milestone-board 新增合规门禁列；index-formats 新增三级索引/Canonical/source-type-registry 格式；glossary 补密评/等保词条；新增 source-type-registry-template、project-notes-template。
- **契约**：skill.json current schema→0.7.0 + migrations + versionHistory；SKILL.md 路由新增 RI 行；SKILL_BLUEPRINT 新增 RI 数据流；skill-contract 事实源/能力更新。
- **scripts**：_version.py →0.7.0；migrate_workspace.py 新增 0.7.0 迁移（单项目/项目集）；chronopm_init/config.py + file_registry.py 初始化新目录。

### Tests
- 回归套件新增 Module 32 Requirement Intelligence（RI-001~006）+ Module 33 Project Notes（PN-001~002），总计 184→192 用例。

---
