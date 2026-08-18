# 升级到 1.10.2

> 从 1.10.1 升级到 1.10.2
> 发布日期：2026-08-11
> Schema 变更：无
> CR 编号：CR-20260810-009

## 变更摘要

脚本层版本治理修复(CR-20260810-009, Patch)：新建 scripts/_version.py 作为 SKILL_VERSION/WORKSPACE_SCHEMA_VERSION 单一版本源，init/migrate 脚本与 config.py 统一从该源读取，消除 config.py(1.9.0)与 migrate_workspace.py(1.6.0)的硬编码版本失步；修复 migrate --target-version 被忽略的 bug（update_version_file/append_migration_log 现实际使用目标版本写入）；补全 VERSION_CAPABILITIES(1.7.0~1.10.1)；README 生成改用版本源插值；release-checklist 新增脚本层版本一致性检查项；新增回归用例 SC-1G~1K

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.10.2 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.10.2）


## CHANGELOG 摘录

## 1.10.2 — 2026-08-11

### Fixed
- 脚本层版本治理（CR-20260810-009, Patch）：修复版本号分散且不同步问题。
  - 新建 `scripts/_version.py` 作为 `SKILL_VERSION` / `WORKSPACE_SCHEMA_VERSION` 的单一版本源；`init_workspace.py`、`migrate_workspace.py` 与 `chronopm_init/config.py` 统一从该源读取，消除了 `config.py`（落后为 1.9.0）与 `migrate_workspace.py`（落后为 1.6.0）的硬编码版本失步。
  - 修复 `migrate_workspace.py --target-version` 被忽略的 bug：`update_version_file()` 与 `append_migration_log()` 现接受并使用目标版本写入 `.skill-version.json` 与 `migration-log.md`（缺省回落单一版本源），此前打印显示目标版本但实际写入旧常量。
  - 补全 `VERSION_CAPABILITIES` 能力检测表（新增 1.7.0/1.8.0/1.9.0/1.10.0/1.10.1 条目）。
  - `file_registry.py` 中 single/portfolio README 的硬编码版本（0.4.0/0.2.0）改为 `{SKILL_VERSION}`/`{WORKSPACE_SCHEMA_VERSION}` 插值。

### Changed
- `governance/review-checklists/release-checklist.md` 新增「Script Version Consistency（脚本层版本一致性）」检查项，防止版本分散问题复发。

### 影响范围
- 无能力变更：不新增/不删除任何 CAP（CAP-001 ~ CAP-024 保持不变）。
- 无契约变更：规则层（references 00-21）、模板层均未改动。
- Workspace Schema 保持 0.5.0，无迁移。
- 脚本行为：`--target-version` 现在实际生效（行为修正）；不传参时默认版本由 1.6.0 修正为单一版本源 1.10.2。
- 回归：新增 SC-1G~1K 共 5 个脚本契约用例，回归套件由 149 增至 154 用例；其余既有 149 用例不受本次改动影响。
- Blueprint Impact: none（仅脚本层修复，不涉及能力矩阵/架构正文）。

---
