# Baseline 1.10.2

- **版本**：1.10.2（Patch / release）
- **Workspace Schema**：0.5.0
- **生成日期**：2026-08-11（由 git tag `v1.10.2` 重建）
- **CR**：CR-20260810-009
- **性质**：脚本层版本治理修复（发布归档基线）

本基线由 git tag `v1.10.2`（提交 1611c75，release: v1.10.2 脚本层版本治理修复）通过 `git archive` 干净导出重建，作为回滚至 1.10.2 的权威来源。

## 包含文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 核心契约（v1.10.2 / schema 0.5.0） |
| `VERSION` | 版本号（1.10.2） |
| `skill.json` | Skill 元数据（version 1.10.2 / schema 0.5.0） |
| `CHANGELOG.md` | 变更历史（含 1.10.2 条目） |
| `SKILL_BLUEPRINT.md` | Skill 蓝图/成熟度快照 |
| `tests/regression-suite.md` | 回归套件（154 用例） |
| `references/` | 22 份规则声明文件（00-21） |

## 回滚参考

1.10.2 为 1.11.0 的前一稳定基线，用于升级失败时的回滚目标。回滚步骤见 `governance/impact-analysis/IA-20260811-002-v2.md` 的 Rollback Plan；1.11.0 基线位于同目录 `1.11.0/`。

## 校验

- 版本触点：`VERSION` / `SKILL.md` / `skill.json` 三面均 1.10.2、schema 0.5.0（已实测）。
- 回归：154 用例（对应 1.10.2 回归套件）。
- 相关发布记录：`governance/change-requests/CR-20260810-009.md`、`governance/regression-reports/rr-20260810-1.10.2.md`。
