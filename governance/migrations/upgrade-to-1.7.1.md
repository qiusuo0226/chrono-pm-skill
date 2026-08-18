# 升级到 1.7.1

> 从 1.7.0 升级到 1.7.1
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

脚本重构(CR-20260810-001)：init_workspace.py 拆分为 chronopm_init 包，9处硬编码202608改动态月份，CLI与产物结构不变

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.7.1 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.7.1）


## CHANGELOG 摘录

## 1.7.1 — 2026-08-10

### Changed
- 脚本重构（CR-20260810-001）：`scripts/init_workspace.py` 由 1269 行单体脚本重构为入口壳 + `scripts/chronopm_init/` 包（config/template_renderer/file_registry/validators/workspace_builder），CLI 参数与生成物目录结构完全不变
- Skill 版本升级 1.7.0 → 1.7.1（Patch：脚本内部重构，向后兼容，不改 references/模板/schema）

### Fixed
- `init_workspace.py` 9 处硬编码月份目录 `202608` 改为动态生成（`datetime.now().strftime("%Y%m")`），避免月份过期时初始化出错误的历史月份目录

### 回归测试
- `tests/regression-suite.md` 新增 19. 脚本契约模块（SC-1A~1F），覆盖 CLI 参数、产物目录结构、动态日期、参数校验行为

Blueprint Impact: metadata-only

---
