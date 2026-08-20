# 升级到 1.3.0

> 从 1.2.0 升级到 1.3.0
> 发布日期：2026-08-09
> Schema 变更：0.5.0 → 0.4.0
> CR 编号：—

## 变更摘要

工作区升级感知：健康检查+功能触发检查+兼容模式+迁移模式(structure-only/recent-7-days/full-rebuild)+提醒频率控制+migrate_workspace.py增强

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.3.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.3.0）


## CHANGELOG 摘录

## 1.3.0 — 2026-08-09

### Added
- `06-file-rules.md` 新增 6 个工作区升级感知规则：
  - §0.0b 功能触发时检查（用 todo 但索引缺失→提示升级而非扫描）
  - §0.0c 兼容模式（用户拒绝升级时明确提示降级影响）
  - §0.0e 升级提醒频率控制（`ignored_until` 防止反复弹窗）
  - §0.0f 升级触发词（12 个触发表达式）
  - §0.0g 工作区健康文件（`.workspace-health.md` 人类可读）
  - §0.0h 迁移模式（structure-only / recent-7-days / current-month / full-rebuild）
- 新增 `assets/templates/workspace-health-template.md`：工作区健康状态模板
- `skill.json` 新增 `supportedWorkspaceSchema`（min/current）和 `migrations` 迁移路径
- `migrate_workspace.py` 新增 `--index-mode` 参数、健康文件生成、索引重建函数

### Migration
- Workspace schema: 无变更（仍为 0.5.0）
- Migration required: No（规则增强，无需迁移已有工作区）

### Upgrade Notes
- 从 1.2.1 升级：直接覆盖即可。已有工作区无需迁移。
- 新增的 `.workspace-health.md` 会在下次运行 `migrate_workspace.py` 时自动生成。

---
