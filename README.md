# ChronoPM 1.10.0 — 历史计划全量同步与变更追溯（补丁包）

> 对应 CR：CR-20260810-008（V0.4 定稿，单 CR 分 Phase）
> 版本：1.9.0 → 1.10.0（Minor / contract_change / capability-change）
> Workspace Schema：0.5.0（不变，无需迁移）

## 说明

本补丁包由 Skill 升级总控（Agent A，经 B 双轮审核 + 用户确认）产出。
由于执行环境无法直接写入 Skill 包目录，本包以"逐文件补丁 + 完整替换稿"形式交付，请按下方顺序在 Skill 根目录 `c:\Users\qiusuo\.trae-cn\skills\chronopm` 应用。

## 应用顺序（先压后增，行数约束先验证）

| 步 | 文件 | 操作 | 约束验证 |
|---|---|---|---|
| P0-1 | `governance/change-requests/CR-20260810-008.md` | 新增 | 见 `/CR-1.10.0/CR-20260810-008.md` |
| P1-1 | `SKILL.md` | MN-1 压缩 + 路由/索引 | ≤290 行 |
| P1-2 | `references/06-file-rules.md` | MN-2 压缩 + 指针 + 注释 | ≤295 行 |
| P2-1 | `references/03-task-board-rules.md` | 字段 + B 类超期规则 | — |
| P2-2 | `references/15-snapshot-rules.md` | external_import + source_type 统一 | — |
| P2-3 | `references/05-query-rules.md` | A 类秒答 + B 类状态路由 | — |
| P2-4 | `references/08-change-control-rules.md` | 概念域 B + plan_change | — |
| P2-5 | `references/13-continuity-rules.md` | R1 边界表 | — |
| P2-6 | `references/00-pm-main-rules.md` | 意图检测新增 | — |
| P3-1..9 | `assets/templates/*` | 9 改 + 2 新 | — |
| P4-1 | `tests/regression-suite.md` | 新模块 + BP 刷新 | — |
| P4-2 | `VERSION` / `skill.json` / `CHANGELOG.md` / `SKILL_BLUEPRINT.md` / `SKILL.md` front matter | 版本触点 1.10.0 | — |

## 目录结构

- `/CR-1.10.0/` — 治理工单（CR-20260810-008）
- `/patches/` — 分阶段修改日志（阶段 1-4）
- `/full/` — 需大改或压缩文件的完整建议稿（规则层）
- `/full/templates/` — 9 个修改模板 + 2 个新增模板完整稿
- `/full/tests/` — 更新后的回归套件（149 用例）
- `/full/version-touchpoints.md` — 4 个版本触点的精确补丁规格
- `/full/验收清单.md` — 8 条 AC + 9 组测试用例发布前核对

## 交付状态

| Phase | 内容 | 状态 |
|---|---|---|
| Phase0 | CR 治理工单 | ✅ |
| Phase1 | SKILL.md(248) + 06(292) 压缩 | ✅ |
| Phase2 | 00/03/05/08/13/15 六规则 | ✅ |
| Phase3 | 9 模板改 + 2 新模板 | ✅ |
| Phase4 | 回归套件 + 版本触点 + 验收清单 | ✅ |

> 每个 Phase 的逐文件改动见 `/patches/改造日志-阶段*.md`。

## 验收要点

- SKILL.md ≤290、06 ≤295（先压后增，逐文件验证行数）
- 两概念域分离：plan_change 仅入概念域 B（08/change-log-template），board Change Log（概念域 A）不改
- B 类超期：读索引不扫日报、双触发（日报处理 + PM 查询）、换人交接前归原 Owner、确认窗口期 v2 未确认用 v1
- R4 聚合秒答只读 board.md
- BP-002（1.10.0）+ BP-003（22 规则）刷新
