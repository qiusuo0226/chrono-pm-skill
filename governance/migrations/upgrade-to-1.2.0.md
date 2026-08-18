# 升级到 1.2.0

> 从 1.1.0 升级到 1.2.0
> 发布日期：2026-08-09
> Schema 变更：无
> CR 编号：—

## 变更摘要

变更治理与回归测试：16-skill-governance-rules(变更工单+核心契约保护+最小补丁+回滚)+governance/目录+tests/regression-suite(70用例14模块)

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.2.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.2.0）


## CHANGELOG 摘录

## 1.2.0 — 2026-08-09

### Added
- 新增 `references/16-skill-governance-rules.md`：Skill 变更治理规则（变更工单流程、核心契约保护、最小补丁、回归必跑、回滚规则、基线管理、规则重构审查）
- 新增 `governance/` 目录体系：
  - `contracts/skill-contract.md`：核心契约（硬约束10条+12个保护能力+规则分层+版本规则）
  - `change-requests/CR-template.md`：变更工单模板
  - `impact-analysis/IA-template.md`：影响分析模板
  - `regression-reports/RR-template.md`：回归报告模板
  - `review-checklists/release-checklist.md`：发布检查清单
  - `baselines/`：版本基线目录
- 新增 `tests/regression-suite.md`：回归测试套件（14个模块、70个用例，含正向和回归用例）

### Changed
- `SKILL.md` 版本升级到 1.2.0；路由表新增 Skill 变更治理场景；规则索引新增第16条

### Upgrade Notes
- **从 1.1.0 升级**：无 schema 变更（均为 0.5.0）。直接覆盖即可。governance/ 和 tests/ 只在 Skill 包，不进入生成的 ai/ 工作区。
- **核心改变**：以后 AI 修改 Skill 必须先出变更工单，不得直接改文件。回归测试套件覆盖 14 个能力模块、70 个用例。

---
