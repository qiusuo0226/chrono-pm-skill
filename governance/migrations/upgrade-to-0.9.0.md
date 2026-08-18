# 升级到 0.9.0

> 从 0.8.0 升级到 0.9.0
> 发布日期：2026-08-09
> Schema 变更：无
> CR 编号：—

## 变更摘要

快速查询路由+待办索引体系：Quick Query路由表+查询性能规则+禁止默认临时脚本+portfolio/todos/目录+PM待办模板(全团队聚合)

## 新增目录

- `portfolio/todos`

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（0.9.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 0.9.0）


## CHANGELOG 摘录

## 0.9.0 — 2026-08-09

### Added
- `05-query-rules.md` 新增 §2.5 快速查询路由：Quick Query 路由表（8种查询场景的优先读取/兜底读取/禁止动作）、查询性能规则（6条）、索引缺失处理流程、禁止默认临时脚本规则
- 新增 `ai/portfolio/todos/` 目录：personal-todo-index.md（按人聚合）、daily-todo-index.md（按日期聚合）、weekly-todo-index.md（按周聚合）
- 新增 `assets/templates/pm-daily-todo-template.md`：PM 每日待办模板（PM直接任务 + 全团队明日计划 + 风险 + 问题 + 里程碑 + 资源变动 + 本周计划对照 + 待协调事项 + 无计划项提醒）
- 新增 `assets/templates/personal-todo-index-template.md`：个人待办索引模板
- 新增 `assets/templates/daily-todo-index-template.md`：每日待办索引模板
- 新增 `assets/templates/weekly-todo-index-template.md`：每周待办索引模板
- `01-daily-report-rules.md` 新增 §5.6b 待办索引同步规则（日报→todo index 自动同步）
- `10-update-trigger-rules.md` 新增待办信号触发词
- `09-portfolio-rules.md` 增加待办索引引用
- `06-file-rules.md` 目录结构新增 todos/ 目录

### Changed
- `init_workspace.py` 初始化时创建 `ai/portfolio/todos/` 目录

### Upgrade Notes
- **从 0.8.0 升级**：无 schema 变更（均为 0.4.0）。旧工作区需手动创建 `ai/portfolio/todos/` 目录，或重新运行 `init_workspace.py`。
- **核心改变**：AI 查询待办时优先读索引文件，不再默认全量扫描日报/会议纪要。禁止为简单查询创建临时脚本。

---
