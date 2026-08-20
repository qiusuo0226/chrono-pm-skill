# ChronoPM v1.15.0

Markdown 驱动的 AI 项目管理技能。

## 简介

为项目经理（尤其 To G / To B 政企数字化转型领域）提供一套以 Markdown 文件为事实源、AI 为辅助、人工确认为控制点的项目管理技能。覆盖需求管理、任务跟踪、进度管控、风险与问题、里程碑、成本与 P&L、日报周报、会议纪要、决策记录、复盘、项目集统筹、人员资源协调与流转、更新意图识别、初始化向导、迭代管理、信息完整性巡检与补全提醒、PM 偏好学习与输出适配、**跨源需求归集与判定（RI）** 等全链路。

## 工作模式

- **单项目模式（single）**：适用于独立项目，所有管理文档放在项目根目录下的 `ai/` 中。
- **项目集模式（portfolio）**：适用于一个项目集经理统筹多个子项目的场景，按 `portfolio/`（项目集级）和 `projects/{子项目名}/`（子项目级）分层管理。

## 目录结构

```
ChronoPM Skill/
├── SKILL.md              # 核心契约（Skill 主提示词）
├── SKILL_BLUEPRINT.md    # 能力蓝图
├── skill.json            # Skill 元数据
├── VERSION               # 版本号
├── CHANGELOG.md          # 变更历史
├── QODER_RULES.md        # Qoder 环境配置入口
├── assets/               # 模板与资源文件（含 source-type-registry / project-notes 模板）
├── governance/           # 治理归档（CR、IA、RR、基线等）
├── references/           # 规则声明文件（00~21 号规则）
├── scripts/              # 自动化脚本
└── tests/                # 回归测试套件
```

## 版本信息

| 项目 | 值 |
|------|-----|
| Skill 版本 | 1.15.0 |
| Workspace Schema | 0.7.0 |
| 默认工作模式 | portfolio |
| 规则文件数 | 22（00~21） |
| 回归用例数 | 192 |
| 模板数 | 46（含新增 source-type-registry / project-notes） |
| 能力点数 | 26（CAP-001~026，RI 为 CAP 扩展） |

## 核心能力

需求管理、任务看板、进度计划、风险/问题管理、日报/周报/会议纪要处理、变更控制、文件管理、查询路由、输出物管理、Excel 生成、项目阶段衔接、自查校验、计划快照、变更治理、领域术语词库、初始化向导、信息完整性巡检、PM 偏好学习、工作空间清洁度治理、**跨源需求归集与判定（RI）**。

## 本版本亮点（1.15.0）

**跨源需求归集与判定（Requirement Intelligence, RI）**：

- **三层数据模型**：ATOM（证据层，只读）→ Canonical（归并层）→ REQ（管理登记册）。把"需求在不在合同/招投标/立项范围内"从扯皮变成可取证，输出 scope_scope 范围判定 + 证据链。ATOM raw_text 只存条款级原文（≤500 字），原始文档不入库只存指针。
- **双层来源分类**：source_category 固定 6 类（contractual/procurement/approval/compliance/technical/operational）+ source_type 项目级可扩展（source-type-registry.md），覆盖 12+ 类实际源文档。
- **kind 四类型**（需求/要求/约定/约束）统一链路拆解；密评/等保 compliance 强制门禁；里程碑复用 milestone-board 并新增合规门禁列。
- **三级索引 + 分级加载**：L1 路由 → L2 类别倒排（含 norm_text 覆盖索引）→ L3 全文，单次范围判定 ≤400 行，对齐最小读取。
- **P1 语义兜底**：词库同义词扩展 / norm_text 扫读 / 降级提示，解决"AI 检索不全"。
- **PM 随笔 project-notes**：AI 主动感知 + PM 主动要求双入口，只追加时间线。
- **workspace schema 0.7.0**：requirements/ 下新增 canonical/、atoms/、source-type-registry，含迁移脚本。

**不改变项**：既有能力语义（CAP-001~026）、既有规则文件数与核心字段、REQ 层现有字段（`来源`字段指针化，旧工作区仍为自由文本向后兼容）。

## 基线快照信息

| 项 | 值 |
|---|---|
| 基线版本 | 1.15.0 |
| 快照生成日期 | 2026-08-13 |
| 关联工单 | CR-20260813-001 |
| 关联回归报告 | `governance/regression-reports/rr-20260813-1.15.0.md` |
| 前置基线 | `governance/baselines/1.14.0/` |
| 快照内容 | references/（22 文件）+ SKILL.md + skill.json + VERSION + CHANGELOG.md + SKILL_BLUEPRINT.md + regression-suite.md |

## 升级日志

详见 [CHANGELOG.md](CHANGELOG.md)。
