# 升级到 1.6.0

> 从 1.5.0 升级到 1.6.0
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

领域术语词库：17-domain-glossary-rules.md(状态机+置信度+9步归一化+纠错+自动学习pending+确认式学习+索引+去重+扩容)、domain-glossary-template.md(内置外资/农专初始词条)、01/02/05/06/10规则增加术语归一化预处理、SKILL.md路由追加17、init/migrate脚本新增--glossary/--create-glossary参数

## 新增目录

- 无

## 新增文件

- `portfolio/context/domain-glossary.md`
- `context/domain-glossary.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.6.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.6.0）


## CHANGELOG 摘录

## 1.6.0 — 2026-08-10

### Added
- 新增领域术语词库能力：`references/17-domain-glossary-rules.md`（16 节完整规则，含状态机、置信度判定、9 步归一化流程、纠错、自动学习 pending、确认式学习、索引、去重、扩容、异常处理）
- 新增词库模板文件：`assets/templates/domain-glossary-template.md`（内置用户已确认初始词条：外资→外商投资、农专→农民专业合作社）
- 日报处理增加术语归一化预处理（`01-daily-report-rules.md` §1.2b，9 步流程）
- 评审记录处理增加术语归一化预处理（`02-meeting-rules.md` §0b）
- 查询路由增加术语归一化（`05-query-rules.md` §1.5）
- 更新触发增加术语归一化前置步骤（`10-update-trigger-rules.md` §1b）
- 文件管理增加词库文件规范和瘦身规则（`06-file-rules.md` §0c）
- `SKILL.md` 路由表追加 17 规则（日报/评审/查询/更新触发场景），新增"词库管理"独立场景
- `SKILL.md` front matter 增加词库管理触发关键词：术语、词库、缩写、纠正、domain-glossary
- `SKILL.md` §15 详细规则索引新增 17 规则条目
- `init_workspace.py` 新增 `--glossary` 参数，新项目初始化时创建词库模板（内置初始词条，不自动抽取历史术语）
- `migrate_workspace.py` 新增 `--create-glossary` 选项，旧工作区可创建词库模板

### Changed
- Skill 版本升级 1.5.0 → 1.6.0
- `init_workspace.py` SKILL_VERSION 常量更新为 1.6.0
- `migrate_workspace.py` CURRENT_SKILL_VERSION 常量更新为 1.6.0

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段）
- 不删除、不弱化任何现有能力
- 路由表仅追加 17 规则，不移除原有必须加载规则

### Blueprint Impact
- minor：新增能力（领域术语词库）
- workspace schema 不变

### Upgrade Notes
- 从 1.5.0 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增**：领域术语词库能力。词库不存在时完全兼容现有流程，不影响旧工作区。
- 旧工作区如需启用词库功能：`python scripts/migrate_workspace.py --project-root . --create-glossary`
- 新工作区初始化时如需创建词库：`python scripts/init_workspace.py --project-root . --mode portfolio --sub-projects ... --glossary`
- 词库内置用户已确认初始词条（外资→外商投资、农专→农民专业合作社），不自动抽取历史术语。

---
