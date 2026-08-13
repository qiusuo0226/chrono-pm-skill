# ChronoPM v1.15.0

Markdown 驱动的 AI 项目管理技能。

## 简介

为项目经理（尤其 To G / To B 政企数字化转型领域）提供一套以 Markdown 文件为事实源、AI 为辅助、人工确认为最终控制点的项目管理技能。覆盖需求管理、任务跟踪、进度管控、风险与问题、里程碑、成本与 P&L、日报周报、会议纪要、决策记录、复盘、项目集统筹、人员资源协调与流转、更新意图识别、初始化向导、迭代管理、信息完整性巡检与补全提醒、历史计划导入与变更追溯、领域术语词库、PM 偏好学习与输出适配、主动变更 + 人工确认更新模式等全链路。

核心设计理念：**事实源文件（board、register、log）是项目状态的唯一真相；过程记录（日报、会议纪要）是信息输入，不能直接替代事实源**。所有 AI 管理文件以项目文件夹下的 `ai/` 目录为载体，AI 负责识别、填写、校验、汇总与提醒，人工确认后才写入事实源。

## 工作模式

- **单项目模式（single）**：适用于独立项目，所有管理文档放在项目根目录下的 `ai/` 中。
- **项目集模式（portfolio）**：适用于一个项目集经理统筹多个子项目的场景，按 `portfolio/`（项目集级）和 `projects/{子项目名}/`（子项目级）分层管理。核心原则：信息自下而上汇总、决策自上而下通知，项目集不直接改动子项目事实源。

## 核心能力（CAP-001 ~ CAP-026）

| 能力点 | 名称 | 说明 | 引入版本 |
|---|---|---|---|
| CAP-001 | Workspace Initialization | 初始化项目工作区，`init_workspace.py` 支持 single/portfolio 模式 | 基础 |
| CAP-002 | Daily Report Management | 日报处理，含合并幂等性 + 个人进度联动 | 基础 |
| CAP-003 | Weekly Report & Portfolio Rollup | 子项目周报 + 项目集月报汇总 | 基础 |
| CAP-004 | PM Daily Todo（9 段全景） | 全团队聚合待办视图，禁止只列 PM 个人任务 | 基础 |
| CAP-005 | Quick Query（索引优先） | 索引优先查询，禁止默认全量扫描 | 基础 |
| CAP-006 | Output Artifact Management | 输出物批次目录 + 草稿/确认/导出流程 | 基础 |
| CAP-007 | Risk & Issue Management | 风险与问题登记，含多源交叉校验 | 基础 |
| CAP-008 | Requirement Management | 需求登记与需求追踪矩阵 | 基础 |
| CAP-009 | Change Control | 变更流程 + 影响分析 | 基础 |
| CAP-010 | Resource Management | 资源登记，状态与历史分离 | 基础 |
| CAP-011 | Historical Continuity | 项目阶段衔接（存量导入依赖人工确认） | 基础 |
| CAP-012 | Todo Snapshot & Actuals | 快照冻结 + 计划 vs 实际对比 | 基础 |
| CAP-013 | Self-Check & Completeness | D/M/R/T 分层自查清单 | 基础 |
| CAP-014 | Excel Generation | 8 种文档 sheet 结构/列头/验证/公式/条件格式 | 基础 |
| CAP-015 | Version & Compatibility | 工作区健康检查 + 兼容模式 + 迁移脚本 | 基础 |
| CAP-016 | Update Trigger & Intent Detection | 四级触发 + 权限分级 | 基础 |
| CAP-017 | Skill Governance | 变更工单（CR/IA/RR）+ AP 审查 + 回归保护 | 基础 |
| CAP-018 | Blueprint & External Review | 架构决策 + 能力矩阵 + 外部审查入口 | 基础 |
| CAP-019 | Domain Glossary | 领域术语词库：归一化 + 置信度 + 纠错 + 确认式学习 | v1.7.0 |
| CAP-020 | Project Initialization Wizard | 六步引导建档，含进度记忆、断点续接、确认写入 | v1.8.0 |
| CAP-021 | Information Completeness Inspection | 7 层缺失检查维度，P0-P3 分级提醒，静默策略，巡检报告 | v1.8.0 |
| CAP-022 | Entry Router & Knowledge Navigation | SKILL.md 主入口路由器，规则下沉至 references | v1.8.0 |
| CAP-023 | PM Profile & Preference Learning | 用户习惯学习与偏好适配输出 | v1.9.0 |
| CAP-024 | Historical Plan Import & Change/Delay Track | 存量计划批量导入 + 变更/延期计数与追溯 | v1.10.0 |
| CAP-025 | Proactive Change & Pending Window | 主动变更 + 人工确认更新模式，待确认记录不参与超期判定 | v1.11.0 |
| CAP-026 | Change Log Tiered Archive | 活跃区/归档区分层归档，自动月份导航 | v1.11.0 |
| —（CAP 扩展） | Requirement Intelligence (RI) | 跨源需求拆词/归并/范围判定/三级索引检索 | v1.15.0 |

## 关键机制

- **实体级联传播**（v1.13.0）：6 个实体规则文件内置 `§级联传播规则`，采用 AUTO / CHECK / SUGGEST 三级动作自动处理实体间状态联动，级联冲突标记 ⚠ 交 PM 决策。
- **标准工作流数据路径**（v1.14.0）：00 号 §9 预定义 WF-1~WF-6 高频操作（待办更新/日报/会议/变更/周报/资源流转）的端到端读/写文件顺序，减少 AI 逐步临时推导；§9.1 判断阶段强化规则确保路径预定义不弱化判断性推导。05 号 §2.5 Quick Update 路由表与 Quick Query 对称。
- **跨源需求归集与判定（RI）**（v1.15.0）：07 号新增 ATOM→Canonical→REQ 三层模型，双层来源分类（6 类 source_category + 项目级可扩展 source_type），三级索引 + 分级加载 + P1 语义兜底，解答"需求在不在合同/招投标/立项范围内"并给出证据链；PM 随笔 project-notes 双入口。workspace schema 0.7.0。
- **更新意图识别**（v1.10.0）：SKILL.md 作为路由器，根据用户意图自动路由到对应规则处理，支持批量识别（一周日报一次性处理）。
- **信息完整性巡检**（v1.8.0）：主动扫描工作区缺失信息，P0-P3 分级提醒，支持静默策略。
- **PM 偏好学习**（v1.9.0）：复用领域词库状态机，被动观察 → pending → confirmed，输出适配个人习惯。
- **主动变更 + 人工确认**（v1.11.0）：低/中风险变更可直接写入事实源并登记 pending-changes，确认后方生效；重大变更触发完整回归。

## 目录结构

```
ChronoPM Skill/
├── SKILL.md              # 核心契约（Skill 主提示词 / 入口路由器）
├── SKILL_BLUEPRINT.md    # 能力蓝图（架构决策 + 能力矩阵 + 数据流）
├── skill.json            # Skill 元数据
├── VERSION               # 版本号
├── CHANGELOG.md          # 变更历史
├── QODER_RULES.md        # Qoder 环境配置入口
├── assets/               # 模板与资源文件（含 decision-log-template 等）
├── governance/           # 治理契约（contracts/skill-contract.md）+ 变更治理（CR/IA/RR/基线）+ 方案设计（planning/）
├── references/           # 规则声明文件（00~21 共 22 号规则）
├── scripts/              # 自动化脚本（init/migrate/sync_version 等）
└── tests/                # 回归测试套件（198 用例）
```

## 版本信息

| 项目 | 值 |
|------|-----|
| Skill 版本 | 1.15.0 |
| Workspace Schema | 0.7.0 |
| 默认工作模式 | portfolio |
| 规则文件数 | 22（00~21） |
| 回归用例数 | 198 |
| 能力点数 | 26（CAP-001~026） |

## 升级日志

详见 [CHANGELOG.md](CHANGELOG.md)。
