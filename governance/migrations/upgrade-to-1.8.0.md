# 升级到 1.8.0

> 从 1.7.1 升级到 1.8.0
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

SKILL.md 瘦身(CR-20260810-002, Minor/contract_change)：478行→297行，状态枚举/输出规范/容忍度/里程碑下沉至 00-pm-main-rules.md，目录树高层级化，工作流改引用

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.8.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.8.0）


## CHANGELOG 摘录

## 1.8.0 — 2026-08-10

### Changed (contract_change)
- SKILL.md 瘦身（CR-20260810-002，Minor）：478 行 → **297 行**，主入口改为"路由器"
- 状态枚举、输出规范、里程碑体系、例外容忍度下沉至 `references/00-pm-main-rules.md`（§5a/§5.4/§5.5/§5b/§5c）
- §3 工作区结构精简为高层级目录树，细目录指向 `references/06-file-rules.md`
- §5 核心工作流由完整流程代码块精简为"一行摘要 + reference 指针"
- §6 提示词路由表、§7 安全底线、§8 ID 编码、§15 规则索引**完整保留不变**

### Fixed
- `SKILL.md`/`00` 中指向"SKILL.md 第 12/13 节"的旧引用改为指向 00 内部新节（§5b/§5c）

### 回归测试
- `tests/regression-suite.md` 新增 20. SKILL Navigation 模块（SK-1A~1G），覆盖行数、路由表/安全底线/ID编码/规则索引完整性、下沉落点

Blueprint Impact: contract_change（Capability Map / Decision Log / Roadmap 已同步更新）

---
