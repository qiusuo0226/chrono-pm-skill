# 升级到 1.16.2

> 从 1.16.1 升级到 1.16.2
> 发布日期：2026-08-14
> Schema 变更：无
> CR 编号：—

## 变更摘要

分发包幽灵引用修复(Patch)：pack.ps1 governance 排除细化为例外放行 contracts/skill-contract.md（核心契约被 7 个运行时规则引用）+路径分隔符修复；SKILL.md 移除 16 号规则路由条目；排除 SKILL_BLUEPRINT.md（仅文档层引用，无运行时依赖）；skill.json blueprint.file 字段移除（BLUEPRINT 不在发行包内）；skill-contract.md L94 基线规则加注“仅开发者仓库”；release-checklist 新增幽灵引用检查项。无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.16.2 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.16.2）


## CHANGELOG 摘录

## 1.16.2 — 2026-08-14（已发布 · released）

> 发布归档：Patch（分发包幽灵引用修复）。修复 v1.16.1 分发包中 governance/ 整目录排除导致的核心契约断链：例外放行 `governance/contracts/skill-contract.md`（被 7 个运行时规则引用第 5 条）；排除 `SKILL_BLUEPRINT.md`（仅文档层引用）；移除 SKILL.md 中 16 号规则路由；skill-contract.md 基线规则加注“仅开发者仓库”；skill.json 移除 `blueprint.file` 字段。无 workspace schema 变更，无规则/模板/能力变更。

### Fixed
- **pack.ps1**：governance 排除细化——例外放行 `governance/contracts/skill-contract.md`（核心契约）；修复 Windows 路径分隔符匹配（`\` → `/` 归一化后再比对例外清单）。
- **幽灵引用消除**：排除 `SKILL_BLUEPRINT.md`（被 references/16 号和 BLUEPRINT 自身引用的 governance 路径不再进入发行包）；SKILL.md 移除 16 号规则路由条目。

### Changed
- **skill-contract.md**：L94 基线规则加注“仅适用于完整开发仓库，分发包不含 baselines/tests”。
- **skill.json**：移除 `blueprint.file` 字段（BLUEPRINT 不在发行包内，保持元数据自洽）。
- **release-checklist**：Distribution Packaging 段更新排除清单（标注例外放行）+ 新增幽灵引用检查项。
- **pack-skill/SKILL.md**：排除清单说明同步更新。

### Notes
- 无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。
- 包体新增 `governance/contracts/skill-contract.md`（~5.5 KB），移除 `SKILL_BLUEPRINT.md`（~15 KB）和 `references/16-skill-governance-rules.md`（~8 KB），净体积略降。

---
