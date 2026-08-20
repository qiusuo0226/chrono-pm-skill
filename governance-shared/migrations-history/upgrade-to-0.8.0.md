# 升级到 0.8.0

> 从 0.7.1 升级到 0.8.0
> 发布日期：2026-08-09
> Schema 变更：0.3.0 → 0.4.0
> CR 编号：—

## 变更摘要

项目阶段衔接：13-continuity-rules.md(5种导入模式+内容路由+结转流程+冲突检测+不可覆盖)、continuity/目录、4个模板

## 新增目录

- `continuity`

## 新增文件

- `continuity/project-lineage.md`
- `continuity/legacy-sources.md`
- `continuity/carryover-register.md`
- `continuity/import-log.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（0.8.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 0.8.0）


## CHANGELOG 摘录

## 0.8.0 — 2026-08-09

### Added
- 新增 `references/13-continuity-rules.md`：项目阶段衔接规则（5种导入模式、内容路由表、结转流程、冲突检测、不可覆盖规则、版本兼容、ID规则）
- 新增 `assets/templates/carryover-register-template.md`：结转事项登记册模板
- 新增 `assets/templates/project-lineage-template.md`：阶段谱系模板
- 新增 `assets/templates/legacy-sources-template.md`：历史来源登记模板
- 新增 `assets/templates/import-log-template.md`：导入日志模板
- 新增 `ai/continuity/` 目录（project-lineage / legacy-sources / carryover-register / import-log）

### Changed
- `SKILL.md` 版本升级到 0.8.0；schema 升级到 0.4.0；路由表新增5个阶段衔接场景；规则索引新增第13条；工作区结构新增 continuity/ 目录
- `scripts/init_workspace.py` 初始化时创建 `ai/continuity/` 目录及模板文件

### Upgrade Notes
- **从 0.7.1 升级**：schema 从 0.3.0 升级到 0.4.0（新增 continuity/ 目录）。旧工作区需手动创建 `ai/continuity/` 目录，或重新运行 `init_workspace.py`（已有文件不会被覆盖）。
- **迁移方法**：在现有项目根目录运行初始化脚本，会自动创建 continuity/ 目录和模板文件。

---
