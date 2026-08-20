# 升级到 1.8.3

> 从 1.8.2 升级到 1.8.3
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

查询/需求/输出物规则表格化(CR-20260810-005, Patch)：05-query-rules.md 413→252行、11-output-artifact-rules.md 341→204行库内规范化(CAP-005/006)，07-requirement-rules.md 保持139行格式统一(CAP-008)，不删语义、不新增模板文件

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.8.3 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.8.3）


## CHANGELOG 摘录

## 1.8.3 — 2026-08-10

### Changed
- 查询/需求/输出物规则表格化（CR-20260810-005，Patch，覆盖 CAP-005/CAP-006/CAP-008）：
  - `references/05-query-rules.md`（CAP-005）由 413 行瘦身至 **252 行**：问题类型路由表（12 类）、项目集路由、Quick Query 路由表、PM 待办 9 章节、历史查询、人员查询优先级、最小读取、数据来源声明均以紧凑表格/要点保留，未删语义
  - `references/11-output-artifact-rules.md`（CAP-006）由 341 行瘦身至 **204 行**：富批次目录结构、输出状态机、多轮修改复用批次、来源追溯、输出物确认规则等压缩为要点，未删语义
  - `references/07-requirement-rules.md`（CAP-008）保持 **139 行**：仅格式统一微调，字段定义与状态机未变

### 说明
- 全部采用库内规范化，未新增模板文件（`assets/templates/` 仍 38 个）也未新增规则文件（references 仍 21 个）

### 回归测试
- `tests/regression-suite.md` 新增 23. Query/Requirement/Artifact Rules 模块（QR-1A~1D），覆盖 05/11 瘦身、07 契约不变、模拟查询+需求登记语义完整
- 用例合计 118 → 122

Blueprint Impact: metadata + 既有 CAP-005/CAP-006/CAP-008 承载规则文件 05/11/07 重构，无新增能力点

---
