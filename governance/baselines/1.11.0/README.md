# Baseline 1.11.0

- **版本**：1.11.0（Minor / contract_change）
- **Workspace Schema**：0.6.0
- **生成日期**：2026-08-11
- **CR**：CR-20260811-002
- **性质**：主动变更 + 人工确认更新模式（发布归档基线）

## 包含文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 核心契约（v1.11.0 / schema 0.6.0） |
| `VERSION` | 版本号（1.11.0） |
| `skill.json` | Skill 元数据（version/schema/migrations/versionHistory/blueprint） |
| `CHANGELOG.md` | 变更历史（含 1.11.0 条目） |
| `tests/regression-suite.md` | 回归套件（163 用例） |
| `references/` | 22 份规则声明文件（00-21） |
| `SKILL_BLUEPRINT.md` | 能力蓝图（26 CAP 矩阵、成熟度分布、schema 表） |

## 回滚参考

回滚至 1.10.2 的步骤见 `governance/impact-analysis/IA-20260811-002-v2.md` 的 Rollback Plan；1.10.2 基线与本文档同目录按需补齐。回滚触发条件：任一回归失败且无法当场修复、或工作区迁移出现致命错误。

## 校验

- 版本触点：`_version.py` / `VERSION` / `SKILL.md` / `skill.json` 四面均 1.11.0 / 0.6.0（已实测 CONSISTENT_ALL=True）。
- 脚本编译：9 个脚本 py_compile 全部通过。
- 回归：163 用例全通过，结论 D（见 `governance/regression-reports/rr-20260811-1.11.0.md`）。
