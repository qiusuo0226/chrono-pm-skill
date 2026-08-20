# 升级到 1.16.1

> 从 1.16.0 升级到 1.16.1
> 发布日期：2026-08-14
> Schema 变更：无
> CR 编号：—

## 变更摘要

分发包标准化(Patch)：新增通用打包 skill tools/pack-skill/(SKILL.md + scripts/pack.ps1)，支持任意 Qoder Skill 项目一键打包分发包 zip（包含全部、排除已知黑名单模式，默认排除 governance/tests/tools/.git/.idea/.qoder/__pycache__ 等）；支持 -DryRun 预览、-Exclude 自定义排除；release-checklist 新增 Distribution Packaging 段（打包命令+排除清单+升级路径验证）；.gitignore 补强 *.zip/*.tar.gz/.vscode/ 排除项；删除旧专用脚本 scripts/pack_dist.ps1。分发包体积从 ~4 MB 降至 ~270 KB。无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。Blueprint Impact metadata-only。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.16.1 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.16.1）


## CHANGELOG 摘录

## 1.16.1 — 2026-08-14（已发布 · released）

> 发布归档：Patch（分发包标准化）。新增通用打包 skill（tools/pack-skill/），支持任意 Qoder Skill 项目一键打包分发包 zip；release-checklist 新增 Distribution Packaging 段；.gitignore 补强排除项；删除旧专用脚本 scripts/pack_dist.ps1。无 workspace schema 变更，无规则/模板/能力变更。

### Added
- **tools/pack-skill/**：通用 Skill 分发包打包 skill（SKILL.md + scripts/pack.ps1）。策略“包含全部，排除已知”（黑名单模式），不预设任何 Skill 特有目录结构。默认排除 governance/、tests/、tools/、.git/、.idea/、.qoder/、__pycache__/ 等开发者产物。支持 -DryRun 预览、-Exclude 自定义排除。
- **release-checklist Distribution Packaging 段**：打包命令、排除清单、升级路径验证检查项。

### Changed
- **.gitignore**：补强 `*.zip`、`*.tar.gz`、`.vscode/` 排除项。
- **scripts/pack_dist.ps1**：已删除，被通用版 tools/pack-skill/scripts/pack.ps1 取代。

### Notes
- 无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。
- 分发包体积从 ~4 MB（含 governance）降至 ~270 KB。

---
