# 升级到 1.8.4

> 从 1.8.3 升级到 1.8.4
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

升级路线收尾(CR-20260810-006, Patch)：C9 全量回归 23模块/122用例(73正向/49回归)全部通过，C10 版本治理收尾全触点同步至1.8.4，Blueprint 元数据校正(DEBT-05模板数35→38、TODO-05回归用例数70→122)，生成正式回归报告

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.8.4 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.8.4）


## CHANGELOG 摘录

## 1.8.4 — 2026-08-10

### Changed
- 升级路线收尾（CR-20260810-006，Patch）：C9 全量回归 + C10 版本治理收尾
  - 全量回归 `tests/regression-suite.md` 23 模块 / 122 用例（正向 73 / 回归 49）全部通过，无规则缺陷（情形 A）
  - 版本触点全量同步至 1.8.4：VERSION / skill.json（version + versionHistory[0] + blueprint.lastVersion）/ SKILL.md frontmatter / SKILL_BLUEPRINT.md §1/§9.3/§11.3

### Fixed
- Blueprint 元数据校正（版本治理收尾范围）：
  - `SKILL_BLUEPRINT.md` §10.2 DEBT-05 模板数量 35 → **38**（实际 `assets/templates/` 38 个）
  - `SKILL_BLUEPRINT.md` §11.1 TODO-05 回归用例数 70 → **122**（当前套件 23 模块 / 122 用例）

### Docs
- 生成正式回归报告至 `governance/regression-reports/rr-20260810-1.8.4.md`（依 RR-template）
- 持久化怪癖（CR-3/CR-4 曾出现的"编辑首次回显未落盘"）本次 CR-6 连续两版未复现，作为历史教训记录，未写入 Blueprint（保持精简）

### 回归测试
- 全量回归 23 模块 / 122 用例通过；用例合计保持 122（73 正向 / 49 回归）

Blueprint Impact: metadata + 既有能力点回归验证与版本收尾，无新增能力点、无规则语义变更

---
