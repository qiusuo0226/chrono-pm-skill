# 升级到 1.4.0

> 从 1.3.1 升级到 1.4.0
> 发布日期：2026-08-09
> Schema 变更：无
> CR 编号：—

## 变更摘要

Blueprint与外部审查：新增SKILL_BLUEPRINT.md(13章节架构蓝图)+skill.json blueprint元数据+治理规则§17+发布检查清单+文档层分类

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.4.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.4.0）


## CHANGELOG 摘录

## 1.4.0 — 2026-08-09

### Added
- 新增 `SKILL_BLUEPRINT.md`：13 章节架构蓝图文档（架构决策+能力矩阵与成熟度+Schema演进+规则依赖图+数据流+已知局限分类+Roadmap+外部审查指南+更新策略）
- `skill.json` 新增 `blueprint` 元数据对象（file/lastUpdated/lastVersion/updateRequiredOn/metadataUpdateRequiredOn/optionalOn）
- `skill.json` versionHistory 补全 1.3.0、1.3.1、1.4.0 条目
- `16-skill-governance-rules.md` 新增 §17 Blueprint 更新规则（分级触发：必更/应更/免更 + 结构性变更走CR + 普通更新轻量流程 + 层级归属 + CHANGELOG标注要求）
- `governance/review-checklists/release-checklist.md` Documentation 章节新增 3 个 Blueprint 检查项
- `governance/contracts/skill-contract.md` Rule Layer Classification 表新增文档层分类
- `governance/change-requests/CR-template.md` 新增 Blueprint Impact 标注字段
- `tests/regression-suite.md` 新增 Blueprint 模块测试用例（BP-001 到 BP-010，10 个用例）

### Blueprint Impact
- full：本次为 Blueprint 首次创建，全文新增

### Upgrade Notes
- 从 1.3.1 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增**：`SKILL_BLUEPRINT.md` 可随时复制给外部 AI 审查 Skill 能力和待补充项。
- Blueprint 更新纳入发布检查清单，后续每次版本发布时需检查 Blueprint 是否需要更新。

---
