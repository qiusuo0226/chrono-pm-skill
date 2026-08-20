# 升级到 1.1.0

> 从 1.0.1 升级到 1.1.0
> 发布日期：2026-08-09
> Schema 变更：0.4.0 → 0.5.0
> CR 编号：—

## 变更摘要

计划快照与实际执行：snapshots(冻结)+actuals(可追加)+history-index+热冷分离+计划vs实际偏差对比+Todo ID稳定

## 新增目录

- `portfolio/todos/snapshots/daily`
- `portfolio/todos/snapshots/weekly`
- `portfolio/todos/actuals/daily`
- `portfolio/todos/actuals/weekly`

## 新增文件

- `portfolio/todos/history-index.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.1.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.1.0）


## CHANGELOG 摘录

## 1.1.0 — 2026-08-09

### Added
- 新增 `references/15-snapshot-rules.md`：计划快照与实际执行规则（快照冻结/实际摘要/历史索引/热冷分离/计划vs实际对比/Todo ID稳定）
- 新增 5 个模板：daily-todo-snapshot / daily-todo-actuals / weekly-todo-snapshot / weekly-todo-actuals / todo-history-index
- 新增 `ai/portfolio/todos/snapshots/` 目录（daily + weekly）
- 新增 `ai/portfolio/todos/actuals/` 目录（daily + weekly）
- 新增 `ai/portfolio/todos/history-index.md`
- `05-query-rules.md` 新增历史查询路由（触发词 + 查询顺序 + 常见路由表 + 热冷数据分离）
- `01-daily-report-rules.md` 新增 §5.6c 快照与实际执行生成规则
- `10-update-trigger-rules.md` 新增快照信号触发
- `06-file-rules.md` 目录结构新增 snapshots/ 和 actuals/

### Changed
- schema 从 0.4.0 升级到 0.5.0（新增 todos/snapshots/ 和 todos/actuals/ 目录）
- `init_workspace.py` 初始化时创建 snapshots/actuals 目录

### Upgrade Notes
- **从 1.0.1 升级**：schema 从 0.4.0 升级到 0.5.0。旧工作区需手动创建 `ai/portfolio/todos/snapshots/daily/`、`snapshots/weekly/`、`actuals/daily/`、`actuals/weekly/` 目录，或重新运行 `init_workspace.py`。
- **核心改变**：当前待办查索引，历史计划查快照，执行结果查 actuals；支持计划vs实际偏差对比。

---
