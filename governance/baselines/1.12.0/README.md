# Baseline 1.12.0

- **版本**：1.12.0（Minor / governance）
- **Workspace Schema**：0.6.0（不变）
- **生成日期**：2026-08-11
- **CR**：CR-20260811-003
- **性质**：工作空间清洁度治理（发布归档基线）

## 包含文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 核心契约（v1.12.0 / schema 0.6.0） |
| `VERSION` | 版本号（1.12.0） |
| `skill.json` | Skill 元数据（version/schema/migrations/versionHistory/blueprint） |
| `CHANGELOG.md` | 变更历史（含 1.12.0 条目） |
| `tests/regression-suite.md` | 回归套件（167 用例） |
| `references/` | 22 份规则声明文件（00-21） |
| `SKILL_BLUEPRINT.md` | 能力蓝图（26 CAP 矩阵、成熟度分布、schema 表） |

## 回滚参考

回滚至 1.11.0 的步骤：恢复 `governance/baselines/1.11.0/` 中的文件覆盖当前版本。回滚触发条件：任一回归失败且无法当场修复。

## 校验

- 版本触点：`_version.py` / `VERSION` / `SKILL.md` / `skill.json` 四面均 1.12.0 / 0.6.0。
- 回归：167 用例（含新增 CL-001~CL-004），AC 验收 12/12 通过。
