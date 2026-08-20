# 升级到 1.6.1

> 从 1.6.0 升级到 1.6.1
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

资源事实源修复：人员查询优先级规则(05§5.4a)、候选资源变更规则(01)、register/context一致性检查(09§5.6)、project-brief指针化(06/模板)、Blueprint版本号修正及CAP-019补全、目录树缩进修正

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.6.1 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.6.1）


## CHANGELOG 摘录

## 1.6.1 — 2026-08-10

### Fixed
- 修正 `SKILL_BLUEPRINT.md` 版本号：1.5.0 → 1.6.1，补全 v1.6.0 词库能力记录（CAP-019）
- 修正 `SKILL_BLUEPRINT.md` 成熟度统计：L3 能力从 14 项更新为 15 项
- 修正 `SKILL.md` §3.1 工作区目录树：修复 `outputs/` 重复出现和 `prompts/`、`templates/`、`continuity/` 缩进层级错误问题

### Added
- `05-query-rules.md` 新增 §5.4a 人员查询事实源优先级：定义 4 级数据来源优先级（register > transfer-log > context > 日报目录），明确人员查询默认只读 register，字段缺失时降级推断并标注"未确认"
- `01-daily-report-rules.md` 新增候选资源变更规则：日报中人员变动信号只能产生候选变更，不得自动覆盖 register；明确禁止将日报中出现的人员自动认定为正式项目成员
- `09-portfolio-rules.md` 新增 §5.6 resource-register 与 project-context 一致性检查：5 种差异类型处理规则、差异报告输出格式、用户选择 A/B/C/D 确认机制

### Changed
- `06-file-rules.md` §1.1a 修改 project-brief.md 规则：团队信息指针化，不复制 register 完整团队列表，改为指向 register 的指针；不自动删除 brief 已有团队列表，只新增指针并标记冗余待清理
- `project-brief-template.md` 团队成员部分改为指针化，指向 resource-register.md 和 transfer-log.md
- `SKILL.md` frontmatter 版本号更新为 1.6.1
- `skill.json` 版本号更新为 1.6.1
- `SKILL_BLUEPRINT.md` 版本号更新为 1.6.1

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段）
- 不新增规则文件（不拆分 06-file-rules.md）
- 不合并路由表（42 行路由保持不变）
- 不修改 QODER_RULES.md
- 不新增治理通道
- 不修改 resource-register.md 模板字段（"参与子项目"字段留待 v1.6.2）
- 不删除、不弱化任何现有能力

### Blueprint Impact
- full：版本号修正、能力矩阵补充 CAP-019、Known Limitations 无变化
- workspace schema 不变

### Upgrade Notes
- 从 1.6.0 升级：Patch 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心修复**：资源事实源优先级规则澄清。人员查询时默认只读 `resource-register.md`，不再合并搜索 4 处文件。日报中人员变动只能产生候选变更，不自动覆盖事实源。
- `project-brief.md` 模板团队部分已指针化，旧 brief 中的团队列表不自动删除，需用户确认后清理。
- 本次不涉及路由表合并、06 拆分、模板字段新增等结构级变更，这些留待后续版本。

---
