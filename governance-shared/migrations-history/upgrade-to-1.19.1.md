# 升级到 1.19.1

> 从 1.19.0 升级到 1.19.1
> 发布日期：2026-08-15
> Schema 变更：无
> CR 编号：—

## 变更摘要

v1.19.1 修复 migrate_workspace.py 模板同步缺口；脚本层修复，无工作区结构变更。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.19.1 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.19.1）


## CHANGELOG 摘录

## 1.19.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（迁移脚本参考模板库同步缺口 + 健康检查模板检测盲区修复）。双 Agent 审核收敛（V0.1→V0.2，B 复核通过-待修订）。核心升级：修复 `migrate_workspace.py` 从不把 Skill 包模板同步到 `ai/templates/` 参考库、且规则 20 健康检查不检测模板缺失的双层缺口——从旧版本升级或版本号已对齐但模板缺失的工作区（真实痛点场景）会永久缺失新增模板。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；但对已有工作区建议跑一次 `migrate_workspace.py` 补齐参考模板库。

Blueprint Impact: metadata-only

### Added
- **`sync_templates()` 无条件前置（migrate_workspace.py）**：置于版本检查之前、`ai_dir` 存在检查之后，复用 `ALL_TEMPLATE_FILES` 单一事实源，只补不覆盖（保护用户自定义内容）；`--dry-run` 也能报告模板缺失。同时补齐 `outputs/.templates/manifest-template.md`（复用 `create_outputs_dir`，已有 `outputs/index.md` 不被覆盖）。
- **规则 20 §2 第 3b 条 模板完整性检查**：健康检查新增 `ai/templates/` 参考模板库完整性核对（对照 `ALL_TEMPLATE_FILES`）+ `outputs/.templates/manifest-template.md` 存在性，缺失则列入健康报告并建议迁移补齐。

### Changed
- **config.py `ALL_TEMPLATE_FILES` 39→42**：新增 `decision-log-template.md`、`project-notes-template.md`（AI 运行时格式参考副本）、`source-type-registry-template.md`（已实例化事实源，按全量副本库口径纳入）。

### Notes
- 修复 V0.1 阻塞问题：`sync_templates()` 调用点原设计在“创建缺失文件之后”会被“版本已匹配/无缺失”两个提前 return 跳过，导致真实痛点场景下修复失效；已提升为无条件前置步骤。
- 端到端实测双场景通过：版本已对齐 1.19.0 但模板缺失（dry-run 报告 40 缺失 + 真实迁移补齐 42 个且已有模板不被覆盖）；旧版本 1.10.0 升级（补齐 42 模板 + 34 能力文件 + 自定义 outputs/index.md 不被覆盖）。
- 遗留待办（非本次）：`decisions/decision-log.md` 实例化仍用 `change-log-template.md`，如需独立格式另行调整映射。

---
