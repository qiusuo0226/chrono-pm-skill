# 升级到 1.21.0

> 从 1.20.0 升级到 1.21.0
> 发布日期：2026-08-16
> Schema 变更：无
> CR 编号：—

## 变更摘要

倒排每日矩阵查询视图(Minor/contract_change)：双 Agent 三轮审核收敛（V0.1→V0.3）。05号 §6.7 新增倒排每日矩阵查询视图（人员×日期矩阵，portfolio 多 board 遍历+存量降级策略）；00号 WF-7 草案行补充读文件列+输出规范（初始草案=WBS/刷新=board/WF-8 闭环，contract_change 全量回归）；10号追加查询附带提示。回归套件新增 Module 38（BDM-001~010，总计 269）。零新增文件/模板，schema 保持 0.8.0。Blueprint Impact metadata。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.21.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 见下方 CHANGELOG 摘录中工作流相关条目

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.21.0）


## CHANGELOG 摘录

## 1.21.0 — 2026-08-16（已发布 · released）

> 发布归档：Minor（倒排每日矩阵查询视图）。⚠ contract_change（00号 WF-7 草案行修改，触发全量回归）。双 Agent 审核三轮收敛（V0.1→V0.3，B1/B2 终审通过-可执行）。核心升级：解决 PM 无法按人按天跟踪倒排进度的痛点——05号 §6.7 新增"倒排每日矩阵"查询视图（人员×日期矩阵，支持 portfolio 多 board 遍历 + 存量降级策略）；00号 WF-7 草案行补充读文件列 + 输出规范（初始草案=WBS 产出/刷新=board 派生/WF-8 闭环）；10号追加查询附带提示（board 变更后建议刷新矩阵）。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；0 新增文件、0 新增模板。

Blueprint Impact: metadata（CAP-005 查询路由增强）

### Added
- **倒排每日矩阵查询视图（05号 §6.7）**：人员×日期矩阵（行=Owner 去重，列=工作日，格=Task 简述）；数据访问支持 portfolio 模式（遍历 project-index 圈定的子项目 board）和 single 模式；两文件读（iteration-register + board），与既有"倒排倒计时"行模式一致；可选角色括注（从 resource-register 查）。
- **降级策略（05号 §6.7）**：无 iteration-register 时按日期窗口过滤；无 WP Ref 时行按 Owner、格按 Task Title，标注"未关联 WP"；存量工作区矩阵仍可生成。
- **倒排草案查询提示（10号 §2 L3）**：PM 查询倒排相关内容时，board 有变更则附带"建议刷新倒排矩阵"提示；不新增独立触发类型。

### Changed
- **WF-7 草案行输出规范（00号 §9）**：读文件列从"—"改为 board + iteration-register；输出新增倒排每日矩阵；区分两阶段数据源（初始草案=WBS 产出，刷新=board 派生）；WF-8 闭环（口述先落库再生成矩阵）。⚠ 核心契约修改，触发 contract_change + 全量回归。

### Notes
- 回归套件新增 Module 38 Backward Scheduling Daily Matrix（BDM-001~010，10 用例，总计 269）；含 contract_change 全量回归声明。
- 零新增规则文件、零新增模板、零 schema 变更；workspace schema 保持 0.8.0。
- 方案经三轮 B 审核收敛：V0.1→V0.3；关键决策链：数据源多 board 遍历（非单文件）、存量降级策略、初始草案/刷新区分两数据源、contract_change 确认触发、C-03 保鲜降级为查询附带提示。

---
