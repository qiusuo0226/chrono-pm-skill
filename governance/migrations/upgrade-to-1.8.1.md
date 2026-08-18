# 升级到 1.8.1

> 从 1.8.0 升级到 1.8.1
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

文件管理规则重构(CR-20260810-003, Patch)：06-file-rules.md 瘦身 587→299行，§0工作区版本外移至新建 20-workspace-version-rules.md，§0c词库文件规范并入17§17，§6索引格式代码块移至 assets/templates/index-formats.md，06章节编号修复为§1-§10

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.8.1 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.8.1）


## CHANGELOG 摘录

## 1.8.1 — 2026-08-10

### Changed
- 文件管理规则重构（CR-20260810-003，Patch）：`references/06-file-rules.md` 由 587 行瘦身至 **299 行**，收敛为纯文件管理规则（命名/目录边界/创建/更新/瘦身/索引/归档/安全）
- §0 工作区版本兼容性检查（原 231 行）整体外移至新建 `references/20-workspace-version-rules.md`（版本检查/健康检查/兼容模式/兜底逻辑/升级提醒/触发词/迁移模式）
- §0c 词库文件规范并入 `references/17-domain-glossary-rules.md` 末尾（新增 §17 词库文件规范）
- §6 索引格式完整 markdown 代码块移至 `assets/templates/index-formats.md`，06 仅保留列定义
- §0 原有目录树章节编号合并修复，06 现为 §1-§10 连续编号

### Fixed
- 修复 06-file-rules.md 两个 `## 1.` 重复章节编号

### 回归测试
- `tests/regression-suite.md` 新增 21. File Contract 模块（FC-1A~1D），覆盖 06 瘦身/20 外移完整性/17 词库文件规范/路由指针
- 更新 SK-1E 规则索引计数（00-19 → 00-20，共 21 条）

Blueprint Impact: metadata + 规则清单映射更新（CAP-015、§7.1 清单、§7.2 依赖图补充 20 号）

---
