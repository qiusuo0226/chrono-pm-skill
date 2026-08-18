# 升级到 1.13.1

> 从 1.13.0 升级到 1.13.1
> 发布日期：2026-08-12
> Schema 变更：无
> CR 编号：—

## 变更摘要

v1.13.1 skill.json versionHistory 排序修复并同步 updated_at；治理层修复，无工作区结构变更。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.13.1 段）。

## 模板变更

- 无

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.13.1）


## CHANGELOG 摘录

## 1.13.1 — 2026-08-12（已发布 · released）

> 发布归档：Patch（v1.13.0 升级后治理修复）。修复 versionHistory 数组排序倒置（indices 15-33 从升序改为降序，对齐"最新在前"约定）；SKILL.md `updated_at` 日期同步缺口修复（sync_version.py 新增 updated_at 同步）；versionHistory 条目去重与排序一致性保障。

### Fixed
- versionHistory 数组 indices 15-33（0.1.0→1.6.0）排序从"最旧在前"修正为"最新在前"（1.6.0→0.1.0），与 indices 0-14 约定一致。
- SKILL.md frontmatter `updated_at` 字段由 2026-08-11 修正为 2026-08-12（v1.13.0 发布日期）。
- `scripts/sync_version.py` 新增 `updated_at` 同步逻辑，防止后续版本再出现日期缺口。

### Changed
- 版本 1.13.0 → 1.13.1（Patch）；Workspace Schema 保持 0.6.0（无迁移）。

---
