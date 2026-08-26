# SKILL_BLUEPRINT.md

> ChronoPM Skill 架构决策与能力审查蓝图。本文件可随时复制给外部 AI 进行审查和补充建议。

---

## Document Boundary

本文件不是 `SKILL.md` 的复制，也不是运行手册。

- `SKILL.md` 负责描述 Skill 如何被调用、如何路由、如何执行（回答"怎么做"）；
- `SKILL_BLUEPRINT.md` 负责描述 Skill 为什么这样设计、当前能力全景、能力成熟度、已知缺口和演进方向（回答"为什么"和"还差什么"）。

本文件只在必要处引用 `SKILL.md` 的章节编号，不复制完整目录树、规则全文或状态枚举。如需操作细节，请阅读 `SKILL.md` 及 `references/` 下的规则文件。

---

## 1. Basic Information

| 属性 | 值 |
|---|---|
| Skill 名称 | ChronoPM — Markdown 驱动的 AI 项目管理技能 |
| 当前版本 | 3.17.0（ChronoPM-Project + ChronoPM-Portfolio 共用版本线；版本单一事实源为 `scripts/_version.py`） |
| Workspace Schema | 详见 `scripts/_version.py`（WORKSPACE_SCHEMA_VERSION） |
| 创建日期 | 2026-08-09 |
| 最后更新 | 2026-08-20（v3.6.0 CR-F：sources/ 文档级拆解 + schema 0.11.0）；2026-08-20（v3.5.0 CR-E：wps/ 独立 WP + schema 0.10.0）；2026-08-20（v3.4.0 CR-D：报告存根 + 时间线报）；2026-08-20（v3.3.0 CR-C：关联待办 + TD Ref + 缩写治理）；2026-08-20（v3.2.0 CR-B：DF-017/018 + 加载场景分类）；2026-08-20（v3.1.1 CR-G：开发仓三目录重组 ChronoPM-Project/ + governance-shared/，schema 仍 0.9.0）；2026-08-20（v3.1.0 CR-A：路径残留清理 + 日报查询/更新路由补全 + 月报残留清理，workspace schema 仍 0.9.0）；2026-08-19（v3.0.0 双包拆分：09 号整文件迁 ChronoPM-Portfolio）；2026-08-18 (v2.1.0 个人待办体系与工作区路径整合：新增 22 号个人待办规则（§0 六字段+T+1 沿用+冲突仲裁+Step 0 结转）+ 18 号向导 Step 5 §0 引导 + 04 号 DF-002 关闭门禁 + 09 号双层数据流微调/可用性聚合动态视图硬约束 + 11/12/13/20 号 outputs/→ai/outputs/ 与 continuity/→context/ 路径迁移 + 待办模板进度列/§2 日报存档段 + 升级文件体系 governance/migrations（版本链 0.1.0→2.1.0 权威执行源）+ VERSION_CAPABILITIES 补齐 29 个历史缺口；v1.21.0 倒排每日矩阵查询视图：05号 §6.7 新增倒排每日矩阵（人员×日期，portfolio 多 board 遍历+存量降级）+ 00号 WF-7 草案输出规范（contract_change）+ 10号查询附带提示 + Module 38 回归；v1.20.0 需求双视图与开发文档关联：07号 §8.10 双视图机制（view_business 派生/view_dev+原型链接挂 REQ 层）+ scope_scope 聚合排除硬约束 + WF-2 需求上下文加载 + 开发侧 source_type 扩展 + 词库开发侧分类/预筛懒加载 + Module 37 回归；v1.17.1 治理一致性修复：分发包幽灵引用根治 + 版本失步修正 + audit_release.py 自动断言 + 基线补档；v1.17.0 PM 偏好通用化升级：5 能力模块（日报集成审查/跨实体联动/关闭佐证/委派跟踪/沟通质量）；v1.16.3 级联强制执行修复：待办→board 反向链路 + SUGGEST 强制呈现；v1.16.2 分发包幽灵引用修复：governance 例外放行 skill-contract + 排除 BLUEPRINT + 移除 16 号路由；v1.16.1 分发包标准化；v1.16.0 合同作用域 RI；v1.15.0 跨源需求归集 RI；v1.14.0 标准工作流数据路径；v1.13.1 升级后治理修复；v1.13.0 架构精简改造；v1.12.0 工作空间清洁度治理) |
| 维护方式 | 随 Skill 版本同步更新（详见 §13 Update Policy） |
| 入口文件 | `SKILL.md` |
| 元数据 | `skill.json` |
| 核心契约 | `governance/contracts/skill-contract.md` |
| 文件总数 | 约 140 个（23 份规则 + 36 个模板 + 5 个脚本 + 包内当前 upgrade + 共享历史链归档 + 1 个回归套件 + 版本/蓝图文件） |

---

## 2. Purpose and Design Philosophy

### 2.1 核心目的

给项目经理的 AI 副手——尤其 To G / To B 政企项目。Markdown 是唯一事实，AI 只建议，你确认才生效。人走茶凉、报表对不上、合同范围说不清，都在项目文件夹里解决，而不是再上一套项目管理软件。

### 2.2 设计哲学

ChronoPM 建立在三层信任模型之上：

```
事实源文件（Markdown）  ←  唯一真相，人工确认后才能更新
        ↑
  AI 辅助引擎           ←  分析、建议、生成草稿，不直接修改事实源
        ↑
  人工确认控制点         ←  项目经理审查后决定是否采纳
```

核心信念：

1. **事实源不可绕过**：项目状态以 `ai/` 目录下的事实源文件为唯一真相，日报和会议纪要只是信息输入，不能直接替代事实源。
2. **AI 不决策**：AI 是副手和参谋，不是决策者。涉及资源调配、范围变更、里程碑调整的决策必须由项目经理做出。
3. **过程可追溯**：每条记录必须有 Source 字段，可追溯到来源文档或口述。

---

## 3. Target Users and Operating Context

### 3.1 目标用户

| 用户画像 | 说明 |
|---|---|
| 主要用户 | 项目经理 / 项目集经理，持有 PMP/PRINCE2/CSPM-3 等认证 |
| 行业背景 | To G / To B 政企数字化转型，智慧政务领域 |
| 典型场景 | 省级政务平台建设与交付，多子项目并行管理 |
| 管理规模 | 千万级合同额，多子项目，10-30 人团队 |
| 技术底盘 | Java+Vue 全栈、微服务架构、信创国产化适配 |

### 3.2 运行环境

- AI 平台：灵犀桌面助手（支持 SKILL.md 加载、文件读写、脚本执行）
- 文件系统：本地工作区，`ai/` 目录为事实源载体
- 脚本环境：Python 3.9+

---

## 4. Architectural Decisions

以下每个决策都包含"为什么这样选"和"否决了什么替代方案"。

### AD-01. 使用 Markdown 作为主事实源格式

**决策**：项目状态以 Markdown 文件存储，不使用数据库或在线系统。

**理由**：Markdown 是人类可读、AI 可解析、Git 可追踪的格式。项目经理可以直接打开文件阅读和修改，不依赖任何平台。AI 可以读取和生成 Markdown，无需额外接口。

**否决方案**：
- SQLite 数据库：需要额外工具查看，非技术用户不友好，Git diff 不可读
- 在线 PMS（Jira/禅道）：引入外部依赖，无法离线使用，且项目集跨系统汇总困难

### AD-02. ai/ 与业务目录分离

**决策**：所有 AI 管理文件只存在于根目录 `ai/` 下，不侵入业务子项目目录。

**理由**：业务目录是交付团队的工作空间，AI 管理文件混入其中会造成干扰、增加 Git 冲突风险、模糊管理边界。

**否决方案**：每个子项目下生成 `ai/` 文件夹 — 侵占业务空间，项目集汇总需要跨目录读取

### AD-03. outputs/ 与 ai/ 分离

**决策**：AI 生成物（周报、Excel、报告等）放在 `outputs/` 目录，与 `ai/` 事实源同级但分离。

**理由**：生成物是"输出"，事实源是"输入"。混在一起会导致 AI 难以区分哪些文件可以覆盖（生成物）哪些不能（事实源）。

**否决方案**：生成物直接写入 ai/ — 违反事实源不可污染原则

### AD-04. 项目集模式采用集中式 ai/portfolio + ai/projects

**决策**：项目集模式下，所有管理文档集中在根目录 `ai/` 中，按 `portfolio/`（项目集级）和 `projects/{子项目名}/`（子项目级）分层。

**理由**：项目集经理需要全局视角，集中式管理便于跨项目汇总（周报、风险、资源）。向上汇总、向下不下沉。

**否决方案**：分散式管理（每个子项目独立 ai/）— 汇总时需要跨目录扫描，效率低且易遗漏

### AD-05. 查询采用定向读取，不默认全量扫描

**决策**：查询类请求必须先读待办文件（`todos/{date}/{执行人}.md`）与绑定文件（`todos/{date}/_index.md`），不默认创建临时脚本全量扫描文件。

**理由**：项目文件数量增长后，全量扫描耗时且不可控。待办按日按人组织可直接定位，确保查询性能稳定。

**否决方案**：每次查询临时扫描 — 性能差，且可能遗漏或重复

### AD-06. 历史导入采用 context/carryover（原 continuity/），不直接覆盖

**决策**：历史项目内容通过 `context/` 目录的衔接流程导入（v2.1.0 起 `continuity/` 已并入 `context/`），先登记、再结转、最后确认，不直接覆盖当前事实源。

**理由**：历史数据可能包含已过时的信息，直接覆盖会导致当前项目状态丢失。

**否决方案**：直接复制历史 ai/ 目录 — 无法处理冲突，无法选择性继承

### AD-07. Skill 变更采用治理流程和回归保护

**决策**：任何 Skill 修改必须先生成变更工单（CR）、升级方案审查文档（AP）、影响分析（IA），经用户确认后才能执行。变更后必须运行回归测试。

**理由**：Skill 已有 64+ 个文件，随意修改会导致已有能力失效且难以回溯。

**否决方案**：直接修改文件 — 无法追踪变更影响，无法回滚

### AD-08. 工作区升级需用户确认，不静默迁移

**决策**：Skill 版本升级后，旧工作区不自动迁移。AI 检测到版本差异时提示用户，用户确认后才执行迁移脚本。

**理由**：静默迁移可能破坏已有项目数据，用户需要知道发生了什么变更。

**否决方案**：自动迁移 — 用户不知情，迁移失败时无法回溯

### AD-09. SKILL.md 采用"入口路由器"架构

**决策**：`SKILL.md` 主入口只保留定位、工作模式、工作区结构概要、核心工作流路由、提示词路由表、安全底线、ID 编码、规则索引；状态枚举、输出规范、里程碑体系、例外容忍度等规则详情下沉到 `references/00-pm-main-rules.md`（§5a/§5.4/§5.5/§5b/§5c），主入口以引用指针指向它们。

**理由**：主入口作为 AI 每次必读的文件，若承载过多规则正文会显著增加上下文负担、降低导航效率。将详情下沉到单一事实源 references，可避免同一条规则在多处重复维护（单一来源），并使主入口保持精简（v1.8.0 由 478 行降至 297 行）。

**否决方案**：
- 主入口保留全部规则正文 — 上下文过重、跨文件维护时易出现不一致
- 将详情分散下沉到多个 references — 增加路由复杂度、追查困难

### Design Decisions Not To Change Lightly

以下是当前 Skill 的核心设计决策，外部审查者可以挑战，但必须给出充分理由和迁移成本评估：

1. 使用 Markdown 作为主事实源格式（而非数据库）
2. `ai/` 与业务目录分离（不侵入业务空间）
3. `outputs/` 与 `ai/` 分离（生成物不污染事实源）
4. 项目集模式采用集中式 `ai/portfolio + ai/projects`
5. 查询采用索引优先，不默认全量扫描
6. 历史导入采用 context/carryover（原 continuity/），不直接覆盖当前事实源
7. Skill 变更采用治理流程和回归保护
8. 工作区升级必须用户确认，不静默迁移
9. 同一人同一天只允许一份日报文件，多次提交合并追加不覆盖
10. 快照冻结后不可静默覆盖，修改需追加 Revision Log
11. `SKILL.md` 作为入口路由器，规则详情下沉至 references（见 AD-09）

---

## 5. Capability Map and Maturity Matrix

### 5.1 成熟度模型

| 等级 | 含义 |
|---|---|
| L0 | 仅想法，未实现 |
| L1 | 有规则文件，无完整模板或脚本支撑 |
| L2 | 有规则和模板，但部分流程依赖人工操作 |
| L3 | 规则、模板、流程完整，可稳定使用 |
| L4 | 有自动化脚本和回归测试覆盖 |
| L5 | 长期验证稳定，有迁移和回滚机制 |

### 5.2 能力矩阵

| Capability ID | Capability | Status | Maturity | Rule Files | Templates | Notes |
|---|---|---|---|---|---|---|
| CAP-001 | Workspace Initialization | stable | L4 | `06-file-rules.md` | project-context, project-index, workspace-health 等 | init_workspace.py 仅产单项目工作区（v3.0.0 P-14：portfolio 初始化分支删除；集工作区归 ChronoPM-Portfolio，无 init） |
| CAP-002 | Daily Report Management | stable | L4 | `01-daily-report-rules.md`, `00-pm-main-rules.md` | personal-daily-todo, project-daily, daily-todo-binding | 含合并幂等性 + 工作日志段联动；v2.1.0：日报两步流程（原文先逐字存档 §2 日报存档段，再映射加工进 §3） |
| CAP-003 | Weekly Report (Project) | stable | L3 | `01-daily-report-rules.md` | weekly-report | 本项目周报；跨项目汇总周报归 ChronoPM-Portfolio（F-6，v3.0.0：09 号迁出、集周报模板迁伴生包） |
| CAP-004 | PM Daily Todo (9-section Panorama) | stable | L3 | `05-query-rules.md`, `22-carried-over-rules.md` | 待办文件 + 绑定文件 | 全团队聚合视图，禁止只列 PM 个人任务；v2.1.0：核心执行表新增进度列（8 列硬上限）+ 进度↔状态双轨仲裁 |
| CAP-005 | Quick Query (Targeted-Read-First) | stable | L3 | `05-query-rules.md`, `14-self-check-rules.md` | 待办文件 + 绑定文件 | 定向读取优先，禁止默认全量扫描；v1.21.0 新增 §6.7 倒排每日矩阵查询路由（人员×日期，portfolio 多子项目待办文件遍历+存量降级） |
| CAP-006 | Output Artifact Management | stable | L3 | `11-output-artifact-rules.md` | outputs-index, output-manifest | 批次目录 + 草稿/确认/导出流程；v2.1.0：outputs/ → ai/outputs/ 路径整合 |
| CAP-007 | Risk & Issue Management | stable | L4 | `04-risk-issue-rules.md` | risk-register, issue-register | 含多源交叉校验；v2.1.0：DF-002 关闭确认门禁（编号+佐证+关联影响+PM 确认，日报/周报后批量罗列候选） |
| CAP-008 | Requirement Management | stable | L3 | `07-requirement-rules.md` | requirement-register, change-log | 需求追踪矩阵 |
| CAP-009 | Change Control | stable | L3 | `08-change-control-rules.md` | change-log | 变更流程 + 影响分析 |
| CAP-010 | Resource Management | stable | L3 | `06-file-rules.md` + `22-carried-over-rules.md` + `_index` §1 | todos/{date}/_index.md 花名册、个人待办 §0.5/§0.6（v3.8.0 退役 resource-register / transfer-log） | 花名册单一权威；进出组在个人文件；能耗滚存拷贝追加；跨项目归 Portfolio 只读聚合 |
| CAP-011 | Historical Continuity | partial | L2 | `13-continuity-rules.md` | legacy-sources, project-lineage, import-log；v2.0.0 起结转字段化到待办文件（是否结转/延期次数）；v2.1.0 起随路径整合入 context/ | 规则完整但导入仍依赖人工操作 |
| CAP-012 | Todo Snapshot & Actuals | stable | L3 | `15-snapshot-rules.md` | 仅保留 external_import 导入快照；v2.0.0 起前向快照/actuals 已砍，待办文件本身即历史 | 导入快照冻结 + 历史回查 |
| CAP-013 | Self-Check & Completeness | stable | L3 | `14-self-check-rules.md` | — | D1-D16/M1-M7/R1-R6/T1-T7 自查清单 |
| CAP-014 | Excel Generation | stable | L3 | `12-excel-generation-rules.md` | — | 8 种文档 sheet 结构/列头/验证/公式/条件格式 |
| CAP-015 | Version & Compatibility | stable | L4 | `20-workspace-version-rules.md` | workspace-health, .skill-version.json | 健康检查 + 兼容模式 + 迁移脚本 |
| CAP-016 | Update Trigger & Intent Detection | stable | L3 | `10-update-trigger-rules.md` | — | 四级触发 + 权限分级 |
| CAP-017 | Skill Governance | stable | L3 | `16-skill-governance-rules.md` | CR-template, IA-template, RR-template, release-checklist | 变更工单 + AP 审查 + 回归保护 |
| CAP-018 | Blueprint & External Review | stable | L3 | `16-skill-governance-rules.md §17` | SKILL_BLUEPRINT.md (本文件) | 架构决策 + 能力矩阵 + 外部审查入口 |
| CAP-019 | Domain Glossary | stable | L3 | `17-domain-glossary-rules.md` | domain-glossary | 术语归一化 + 置信度 + 纠错 + 确认式学习 |
| CAP-020 | Project Initialization Wizard | stable | L3 | `18-init-wizard-rules.md` | project-brief（计划概览段） | 六步引导建档（合同→项目→计划→需求→资源→里程碑），含进度记忆、断点续接、确认写入；v2.0.0：PLAN 文件由 AI 正式排计划时按需创建，向导不预建；v2.1.0：Step 5 新增待办 §0 人员信息录入引导 |
| CAP-021 | Information Completeness Inspection | stable | L3 | `19-info-completeness-rules.md` | — | 7层检查维度（合同/项目/计划/需求/待办/资源/里程碑），P0-P3分级提醒，静默策略，巡检报告 |
| CAP-022 | Entry Router & Knowledge Navigation | stable | L4 | `SKILL.md`, `00-pm-main-rules.md` | — | v1.8.0：SKILL.md 主入口改为路由器，规则详情下沉至 references（AD-09），由 SK-1A~1G 回归护航 |
| CAP-023 | PM Profile & Preference Learning | stable | L3 | `21-pm-profile-rules.md` | pm-profile-template | v1.9.0：用户习惯学习与偏好适配，复用 domain-glossary 状态机，被动观察→pending→confirmed |
| CAP-024 | Historical Plan Import & Change/Delay Tracking | stable | L3 | `05,08,13,15,00` | plan-import, change-log；v2.0.0 起计数字段化到待办文件（计划变更次数/延期次数） | v1.10.0：R1 批量导入存量计划(→external_import 冻结快照)、R2 计划变更追踪、R3 延期计数、R4 聚合查询；v2.0.0：计数改为待办文件字段，聚合只读待办文件，delay-stats/task-board/todo-history-index 模板已删 |
| CAP-025 | Proactive Change & Pending Window | stable | L3 | `00,01,05,06,10,14,19`, `skill-contract` | pending-changes-index, change-log, change-log-index, change-log-archive | v1.11.0：主动变更+人工确认更新模式；待确认记录不参与延期/超期判定(确认窗口期)；权限模型 proactive/passive/progressive；skill-contract #5 与 SKILL.md §7 安全底线 #2 修改(三防线：审计/超时/回滚) |
| CAP-026 | Change Log Tiered Archive | stable | L2 | `06-file-rules.md` | change-log-index, change-log-archive | v1.11.0：活跃区 50 行/30 天触发按月归档至 change-log/archive/，维护 change-log/index.md 月份导航 |
| CAP-027 | Personal Todo System | stable | L3 | `22-carried-over-rules.md`（结转机制），`00-pm-main-rules.md` §4d（T+1/仲裁/人员双层身份，v3.0.0 自 09 号 §1.3 承接），`01-daily-report-rules.md`（D-26 双轨仲裁） | personal-daily-todo | v2.1.0：§0 人员信息六字段录入规范（岗位/姓名/联系方式/负责模块/进组日期/离组日期）+ T+1 沿用 + 冲突仲裁（以 resource-register 为准）+ 结转入口 Step 0（创建待办前 MANDATORY 扫描前日 _index.md）；v3.0.0：§0.5 进出组记录/§0.6 能耗 |
| —（CAP 扩展） | Requirement Intelligence (RI) | stable | L3 | `07` + `05` + `17` + `06` | requirements/atoms/(L1/L2/L3)+canonical + contract-register（项目级）；v3.0.0 起 RI 全部下沉项目级，跨项目检索归 Portfolio | v1.15.0：跨源需求拆词/归并/范围判定/三级索引检索；v1.16.0 扩展合同作用域（contract-register + scope_level 路由 + contract_refs 判定，CR-20260813-002）；v3.0.0：废除集层存储，各项目一套 + {type}-source/ledger 台账（§8.9.5）；归属现有 CAP 扩展（非独立 CAP），CR-20260813-001/002 |
| —（CAP 扩展） | Reasoning Baseline（推导基线） | stable | L3 | `00` §10 + `05` §3(3)a + `01` §6.2 + `00` §9 级联 | WP §3b + project-context 项目级推导规则 | v1.18.0 引入；v3.7.0 废 entity-registry，实体状态唯一载体=WP §3b |
| —（CAP 扩展） | Backward Scheduling & Unified Intake（倒排计划与统一归属路由） | stable | L3 | `00` §9 WF-7/WF-8 + `01` §5.6 + `02` §3 + `07` §3.2 + `08` §6.1 + `05` §6.7 | `wps/WP-NNN.md` + `wps/_index.md`（v3.5.0）、plans/PLAN-NNN-{name}.md（§3 引用简表+倒排元数据）、todos/{date}/ 待办文件（WP Ref 字段） | v1.19.0：倒排 = 计划编排方式。v3.5.0：WP 独立文件 + 索引加速器；计划只留 4 列简表；schema 0.10.0 |

> **WF 标准工作流数据路径（v1.14.0 新增）**：WF-1~WF-8 不是独立 CAP，而是 CAP-002/003/004/005/009/010/017 的**执行效率优化层与统一入口约束层**，集中声明于 `00-pm-main-rules.md` §9。它将高频操作场景的读/写文件顺序预定义，判断性推导（状态判定、匹配逻辑、关闭条件）仍保留在判断阶段不弱化（§9.1）。v1.19.0 新增 WF-7（倒排计划编排）与 WF-8（待办创建归属排布，所有任务创建入口的 MANDATORY 前置路由）。Quick Update 路由表（`05-query-rules.md` §2.5）为 CAP-005 的对称扩展（查询→更新）。不新增独立能力 ID、规则文件、ID 前缀（WP Ref 为待办文件可选字段）。

### 5.3 成熟度分布

详见 `tests/regression-suite.md` 各模块成熟度标注。§5.2 矩阵按实际行数统计 per level。

---

## 6. Workspace Schema Evolution

### 6.1 演进路径

| Schema | Skill Version | 关键变更 | 迁移方式 |
|---|---|---|---|
| 0.1.0 | 0.1.0 - 0.2.0 | 初始结构：ai/ 基础目录 + 9 份规则 + 11 个模板 | 无需迁移（初始） |
| 0.2.0 | 0.3.0 - 0.4.0 | 项目集模式 + 资源管理 + 业务目录不侵入 + project-brief | migrate_workspace.py |
| 0.3.0 | 0.5.0 - 0.8.1 | outputs/ 目录 + continuity/ 目录 | migrate_workspace.py |
| 0.4.0 | 0.9.0 - 1.0.1 | todos/ 目录 + snapshots/ + actuals/ + 索引体系 | migrate_workspace.py --index-mode |
| 0.5.0 | 1.1.0 - 1.10.2 | 快照冻结规则 + actuals 可追加 + 历史索引 | 无需迁移（规则增强） |
| 0.6.0 | 1.11.0 - 1.12.0 | 待确认变更索引 pending-changes.md + change-log 分层归档（archive/ 目录） | migrate_workspace.py (SCHEMA_060) |
| 0.7.0 | 1.13.0 - 1.17.1 | 架构精简改造 + 标准工作流数据路径 + 级联传播强制执行 + 倒排计划与统一归属路由 + PM 偏好通用化 + 治理一致性修复 + 分发包标准化 | migrate_workspace.py (SCHEMA_070) |
| 0.8.0 | 1.18.0 - 1.21.0 | 推导基线 + 跨源需求归集 RI + 合同作用域 RI + 需求双视图与开发文档关联 + 倒排每日矩阵查询视图 | migrate_workspace.py (SCHEMA_080) |

### 6.2 兼容性策略

- `skill.json` 中 `supportedWorkspaceSchema.min` 标记最低兼容版本
- AI 进入工作区时读取 `.skill-version.json` 检查版本差异
- 版本差异时输出迁移建议，不自行迁移
- `migrate_workspace.py` 支持 `--dry-run` 预览和 `--index-mode` 控制索引重建范围

---

## 7. Rule Module Dependency Map

### 7.1 规则文件清单

| 编号 | 文件 | 定位 |
|---|---|---|
| 00 | `00-pm-main-rules.md` | 总纲：角色、原则、行为边界、意图检测 |
| 01 | `01-daily-report-rules.md` | 日报：合并、工作日志段、联动 |
| 02 | `02-meeting-rules.md` | 会议：纪要、行动项提取、§6 级联传播规则 |
| ~~03~~ | （v2.0.0 起删除） | 原任务看板规则，board 砍掉，能力下沉到待办层，级联规则迁入 00 号 WF |
| 04 | `04-risk-issue-rules.md` | 风险/问题：识别、评估、升级、§9 级联传播规则 |
| 05 | `05-query-rules.md` | 查询：路由、索引优先、PM 待办输出 |
| 06 | `06-file-rules.md` | 文件：命名、目录边界、创建/更新/瘦身/归档、索引、安全 |
| 07 | `07-requirement-rules.md` | 需求：分类、评审、追踪矩阵、§7 级联传播规则 |
| 08 | `08-change-control-rules.md` | 变更：流程、影响分析、审批、§9 级联传播规则 |
| 09 | `09-portfolio-rules.md` | 退役指针页（v3.0.0）：不加载、无规则条款，仅指向 ChronoPM-Portfolio；原规则实体已迁伴生包（单项目资源条款并入 06） |
| 10 | `10-update-trigger-rules.md` | 触发：四级触发、语义信号、权限分级 |
| 11 | `11-output-artifact-rules.md` | 输出物：批次目录、草稿确认导出 |
| 12 | `12-excel-generation-rules.md` | Excel：8 种文档生成规范 |
| 13 | `13-continuity-rules.md` | 衔接：历史导入、结转、冲突检测 |
| 14 | `14-self-check-rules.md` | 自查：索引预建、D1-D10/M1-M7/R1-R6/T1-T7 |
| 15 | `15-snapshot-rules.md` | 快照：冻结、actuals、历史索引、偏差对比 |
| 16 | `16-skill-governance-rules.md` | 治理：变更工单、AP 审查、回归、Blueprint 更新 |
| 17 | `17-domain-glossary-rules.md` | 词库：术语归一化、置信度、纠错、自动学习 |
| 18 | `18-init-wizard-rules.md` | 初始化向导：六步引导建档、进度记忆、断点续接 |
| 19 | `19-info-completeness-rules.md` | 完整性巡检：7层检查维度、P0-P3分级提醒、静默策略 |
| 20 | `20-workspace-version-rules.md` | 工作区版本：版本检查、健康检查、兼容模式、迁移 |
| 21 | `21-pm-profile-rules.md` | PM 偏好：用户习惯学习、5 类偏好分类、pending→confirmed 状态机 |
| 22 | `22-carried-over-rules.md` | 待办结转：3 时机、Step 0 HARD BLOCK 增强算法、编号硬约束、E1~E5 错误处理、状态机 |

### 7.2 依赖关系

```
00 (总纲) ──被所有规则依赖──
  │
  ├── 01 (日报) ──依赖──→ 04 (风险), 09 (项目集), 15 (快照)
  ├── 02 (会议) ──依赖──→ 04 (风险), 08 (变更)
  ├── 05 (查询) ──依赖──→ 01 (日报), 14 (自查), 15 (快照)
  ├── 06 (文件) ──被所有文件操作依赖──
  ├── 07 (需求) ──依赖──→ 08 (变更)
  ├── 09 (项目集) ──依赖──→ 01 (日报), 04 (风险)
  ├── 10 (触发) ──依赖──→ 01-09 (按事项类型路由)
  ├── 11 (输出物) ──依赖──→ 06 (文件)
  ├── 12 (Excel) ──依赖──→ 11 (输出物)
  ├── 13 (衔接) ──依赖──→ 04 (风险), 07 (需求)
  ├── 14 (自查) ──依赖──→ 01 (日报), 02 (会议), 04 (风险)
  ├── 15 (快照) ──依赖──→ 01 (日报), 03 (任务, R1导入联动), 13 (衔接, R1边界判定)
  ├── 17 (词库) ──依赖──→ 01, 02, 05, 06, 10 (术语归一化前置)
  ├── 18 (初始化向导) ──依赖──→ 00, 06 (触发检测+文件写入)
  ├── 19 (完整性巡检) ──依赖──→ 00, 10 (意图检测+更新触发后检查)
  ├── 20 (工作区版本) ──依赖──→ 06 (文件规则), 16 (治理，CHANGELOG 判定)
  ├── 21 (PM 偏好) ──依赖──→ 00 (总纲), 06 (文件规则), 10 (更新触发), 17 (术语归一化), 20 (版本检查)
  └── 16 (治理) ──元规则，约束 Skill 自身变更──
```

> 实体间的**级联/传播依赖**不在本图重复声明，改由各实体规则文件自身的 `§级联传播规则` 声明（见 03 §8、04 §9、07 §7、09 §8、02 §6、08 §9）。本图仅保留模块级引用关系。

### 7.3 关键交互说明

- **00 是总纲**：所有场景必须加载，定义角色定位和行为边界
- **10 是入口路由**：用户输入先经 10 判断意图和路由，再加载对应规则
- **14 是质量守卫**：01/02 处理后必须经 14 自查，确保不遗漏
- **16 是元规则**：不约束项目管理业务，约束 Skill 自身的变更行为

---

## 8. Key Data Flows

### 8.1 日报数据流

```
个人工作汇报输入
  → [01] 写入该成员当日待办文件工作日志段 (todos/{date}/{姓名}.md)
  → [01] 按需生成项目日报 (reports/daily/project/)
  → [10] 检测更新信号 → 输出建议更新清单
  → [14] 执行 D1-D16 自查清单
  → [09] 检测资源变动 → 更新 resource-register + transfer-log
  → [04] 检测风险/问题 → 输出风险候选
```

### 8.2 周报数据流

```
[11] 用户说"生成周报" → 进入 outputs/ 批次目录
  → [09] 读取 portfolio/context/project-index.md 获取子项目清单
  → [01] 读取每个子项目当周待办文件工作日志段（逐日累积）
  → [04] 汇总各子项目风险/问题
  → [09] 汇总跨项目事项（资源冲突、共性问题）
  → 生成汇总周报草稿 (outputs/{timestamp}/draft.md)
  → 用户确认 → 生成 final.md → 导出
```

### 8.3 变更数据流

```
变更请求输入
  → [08] 登记到 change-log.md (submitted)
  → [08] 影响分析（范围/进度/成本/质量/风险/里程碑）
  → [00] 项目经理决策 → 记录决策
  → 若批准：[07] 更新 requirement-register.md + [00 WF] 更新待办文件/PLAN 文件 + [04] 更新风险
```

### 8.4 历史导入数据流

```
历史项目内容输入（ai 目录/文件/口述）
  → [13] 识别导入模式（ai目录/文件/地址/口述）
  → [13] 登记到 legacy-sources.md
  → [13] 内容路由（风险/问题/需求/任务/里程碑/决策）
  → [13] 冲突检测（与当前事实源对比）
  → [13] 进入 delta-analysis.md 结转候选段等待确认
  → 用户确认后 → 更新对应事实源文件
  → [13] 记录到 import-log.md
```

### 8.5 查询数据流

```
用户提问
  → [05] 判断问题类型和层级
  → [05] 定向读取（待办文件/绑定文件/登记册/快照）
  → 命中 → 读取对应事实源文件
  → 待办目录/绑定文件不存在 → 提示工作区可能未升级，不自行全量扫描
  → 输出结论 + 信息来源 + 不确定项
```

### 8.6 初始化向导数据流

```
新工作区检测 / 用户说"初始化项目"
  → [18] 检测 project-brief.md status=草稿
  → [18] 启动六步向导
  → Step 1: 合同层 → 录入合同/立项/启动/完工时间 → 写入 project-context + project-brief
  → Step 2: 项目层 → 确认子项目清单 → 写入 project-index
  → Step 3: 计划层 → 录入阶段名称/时间 → 写入 project-brief（计划概览段）
  → Step 4: 需求层 → 录入需求数量 → 写入 requirement-register
  → Step 5: 资源层 → 录入资源 → 写入 project-brief + resource-register
  → Step 6: 里程碑层 → 补充里程碑时间 → 写入 progress-plan
  → [18] 生成确认摘要 → 用户确认 → 写入所有文件
  → project-brief.md status 改为"已确认"
```

### 8.7 信息完整性巡检数据流

```
用户发起日常操作（查询/生成报告/分析风险/推导计划）
  → [19] 判断操作涉及的管理域
  → [19] 读取相关事实源文件
  → [19] 按检查维度表逐字段检查
  → [19] 判断缺失项严重程度（P0-P3，含动态升降级）
  → P0 → 必须提醒，可能阻塞当前任务
  → P1 → 主动提醒，标注结论限制
  → P2 → 回答后简短提示
  → P3 → 不提醒
  → 用户选择补充/稍后/忽略
  → 如补充 → 更新对应事实源文件
```

### 8.8 Skill 变更数据流

```
用户提出 Skill 变更请求
  → [16] 生成变更工单 (CR)
  → [16] 生成升级方案审查文档 (AP, 7 章节)
  → [16] 生成影响分析 (IA)
  → 用户确认
  → [16] 执行最小变更
  → [tests] 运行回归测试
  → [16] 生成回归报告 (RR)
  → [16] 更新 VERSION / skill.json / CHANGELOG.md
  → [16] 更新 SKILL_BLUEPRINT.md (按 §13 Update Policy)
  → [16] 生成基线快照
```

### 8.9 跨源需求归集（RI）数据流

> 对应 CR-20260813-001（v1.15.0）+ CR-20260813-002 合同作用域（v1.16.0）。覆盖跨源需求拆词、归并、范围判定与三级索引检索，并支持合同与子项目多对多映射。

```
跨源输入（合同条款/招标文件/口述需求/立项/密评）
  → [18v1.16.0] 初始化向导 step1 登记合同 → contract-register.md（scope_level/parent_contract_id/coverage/文档簇）
  → [07] 需求拆词 → 生成 ATOM（含 source_type/authority/raw_text/norm_text，按合同 scope_level 存层级 ATOM：portfolio/requirements/atoms 或 projects/{sub}/requirements/atoms）
  → [07] 登记 source_type 至对应层级 source-type-registry.md（未登记则触发提示，不静默归类）
  → [17] 词库同义词扩展 → 相同语义的 ATOM 建立关联
  → [07] 归并 → 归属同一 Canonical（evidence 汇聚多来源；跨层/跨子项目归 portfolio 级，storage_level=portfolio；contract_refs 记录关联合同）
  → [07][05] 范围判定 → 输出 scope + contract_refs + 证据链（合同/招标/口述来源比对）
  → [06] 维护对应层级三级索引（atoms/atom-index、{category}-index、{category}）

检索路由（05 号 §Quick Query 四步）：
  Step0 读 contract-register（空 → 触发补录引导，不臆造）
  Step1 解析合同指向（scope_level=portfolio→portfolio canonical；project→子项目 canonical；supplement→经 parent_contract_id 回溯父合同层级）
  Step2 目标层级 canonical 走 L1→L2→L3 三级索引（单次 200-400 行）
  Step3 输出 scope_scope(result) + contract_refs + 证据链（多合同覆盖逐合同列结论）

合同变更联动（07 号 §8.9.4，复用 08 号 scope/cost/requirement）：
  合同拆分 → 旧条 superseded_by、ATOM 归属迁移、Canonical 重判
  范围扩大/补充协议 → 增量 ATOM(supplement)、归并、scope 重判
  范围缩小 → 相关 ATOM stale、原 in_contract 的 Canonical 可能变 not_in_scope
  源文档出新版本 → 相关 ATOM 标记 stale、Canonical evidence_stale
```

---

## 9. Current Version Assessment

### 9.1 稳定能力（L3+）

详见 `tests/regression-suite.md` Module 成熟度标注中 L3 及以上的能力。

### 9.2 实验性/部分实现能力（L2）

- 历史阶段衔接（L2）：规则完整，5 种导入模式和冲突检测已实现，但导入过程仍依赖人工操作，缺少自动化导入脚本
- Change Log 分层归档（L2，CAP-026，本次新增）：框架与规则已落地，归档触发依赖规则执行，尚未脚本化自动触发

### 9.3 版本成熟度总结

当前 v1.13.1 是正式版（v1.0.0 起的第 24 个版本），核心能力均达到 L3 以上成熟度。整体处于"功能完备、持续优化"阶段。§5.2 矩阵共 26 个 CAP：L2 = 2（CAP-011、CAP-026），L3 = 19，L4 = 5（CAP-001、CAP-002、CAP-007、CAP-015、CAP-022）。最近的 1.7.x 聚焦脚本与规则体量精简，1.8.x 聚焦 SKILL.md 路由化与规则职责收敛（如 06 文件规则瘦身、工作区版本规则外移至 20 号、01 日报规则瘦身与模板指针化、05/11/07 规则表格化）。v1.8.4 为升级路线收尾。v1.9.0 新增 PM Profile 用户习惯学习（CAP-023），复用 domain-glossary 的 pending→confirmed 状态机，实现 AI 输出的个性化适配。v1.10.0 新增历史计划全量同步与变更追溯（CAP-024），覆盖 R1 批量导入、R2 计划变更追踪、R3 延期计数、R4 聚合查询路由。v1.10.1 为 CR-008 遗留计数 bugfix：修正 §5.3 成熟度分布统计，与 §5.2 能力矩阵对齐。v1.11.0 引入主动变更+人工确认更新模式（CAP-025/026），新增 pending-changes 索引与 Change Log 分层归档。v1.12.0 完成工作空间清洁度治理（新增§18白名单/§19交付物控制/§20引用约束）。v1.13.0 完成架构精简改造：实体级联嵌入、文件膨胀治理、索引派生分级、版本同步收口、Blueprint 瘦身。v1.13.1 为升级后治理修复：versionHistory 排序修正 + updated_at 同步缺口修复。

---

## 10. Known Limitations and Design Debt

### 10.1 Known Boundaries

以下是有意为之的设计边界，不是缺陷：

| 边界 | 说明 | 设计理由 |
|---|---|---|
| 不直接连接真实项目管理系统 | 不对接 Jira/禅道/OA 等 | Markdown 事实源是核心设计决策，外部系统对接属于扩展而非核心 |
| 不替代正式 OA/ERP/PMS | AI 是辅助而非替代 | 项目经理是决策者，AI 是副手 |
| 默认不全量扫描历史文件 | 查询走索引优先 | 全量扫描性能不可控，索引预建确保稳定性 |
| 默认不静默迁移旧工作区 | 升级需用户确认 | 静默迁移可能破坏已有数据 |
| 不自动执行人员调配决策 | 人员变动需人工确认 | 资源调配是项目经理的决策权 |
| 不自动审批变更 | 变更必须人工审批 | 变更影响范围大，AI 不替代决策 |
| Blueprint 不参与运行时路由 | Blueprint 是被动文档 | Blueprint 供外部审查，不影响 AI 执行行为 |
| 每轮注入过重导致屏闪 | 简单查询少读规则 | 简单查询仅加载 05；SKILL.md 保持瘦；写入才加载 00。不设宿主专用入口 |
| PM Profile 不影响事实源 | PM Profile 仅影响 AI 输出方式和交互风格，不影响事实源内容 | 事实源准确性是核心设计决策，偏好学习仅优化输出体验 |

### 10.2 Design Debt / Gaps

以下是已知待修缺陷，后续要补：

| 编号 | 缺陷 | 影响 | 建议优先级 |
|---|---|---|---|
| DEBT-01 | 历史导入缺少自动化脚本 | 导入效率低，依赖人工操作 | P1 |
| DEBT-02 | 回归测试尚未完全自动化 | 每次变更需人工执行测试用例 | P2 |
| DEBT-03 | 历史索引重建依赖人工确认 | 索引过期时需用户手动触发 | P2 |
| DEBT-04 | 跨项目人员身份映射可能不完整 | 同一人在不同子项目可能用不同名 | P2 |
| DEBT-05 | 模板数量（38个）增加后缺少模板索引 | 查找模板需要遍历目录 | P1 |
| DEBT-06 | 成本测算表尚无自动汇总公式 | 需人工填写汇总 | P2 |
| DEBT-07 | Blueprint 更新依赖人工记忆 | 发布检查清单可捕获，但非自动 | P2 |
| DEBT-08 | 倒排每日矩阵尚无独立模板 | 矩阵输出由规则约束（05号 §6.7），无独立模板；PM 如需要固定格式可后续新增 | P3 |

---

## 11. Roadmap and Backlog

### 11.1 已规划能力

| 编号 | 能能 | 描述 | 优先级 | 依赖 |
|---|---|---|---|---|
| TODO-01 | 模板索引 | 自动生成模板目录索引，支持按场景查找模板 | P1 | 无 |
| TODO-02 | 历史导入自动化脚本 | 脚本化导入流程，减少人工操作 | P1 | DEBT-01 |
| TODO-03 | 验收管理 | deliverables/ 和 acceptance/ 目录的完整规则和模板 | P2 | 无 |
| TODO-04 | 缺陷跟踪 | quality/ 目录规则，或 issues 中 type=defect 的细化规则 | P2 | 无 |
| TODO-05 | 回归测试自动化 | 将 163 个回归用例脚本化执行 | P2 | DEBT-02 |

### 11.2 评估中能力

| 编号 | 能力 | 描述 | 评估状态 |
|---|---|---|---|
| EVAL-01 | 多项目集管理 | 支持多个独立项目集的跨集查询和汇总 | 待评估需求场景 |
| EVAL-02 | Blueprint 自动生成 | 根据规则文件和模板自动生成能力矩阵 | 当前人工维护足够 |
| EVAL-03 | 成本预警自动化 | 当 CPI/SPI 超阈值时自动生成预警 | 待评估触发机制 |

### 11.3 已落地结构变更

详见 `governance/change-requests/` 各 CR 工单的 Scope 和 Blueprint Impact 段。

| Version | Change | CR ID |
|---------|--------|-------|
| 1.13.1 | versionHistory 排序修正 + updated_at 同步缺口修复 | Patch (v1.13.0 治理) |
| 1.13.0 | 实体级联传播 + 归档治理 + 索引分级 + 版本同步 + Blueprint 瘦身 | CR-20260812-001 |
| 1.14.0 | 标准工作流数据路径（WF-1~WF-6）+ Quick Update 路由表 + 各实体规则交叉引用 + SKILL_BLUEPRINT 同步 | CR-20260812-001 续 |
| 1.15.0 | 跨源需求归集（RI）+ 三级索引（requirements/atoms、canonical、source-type-registry）；schema 0.7.0 | CR-20260813-001 |
| 1.16.0 | 合同作用域（portfolio/requirements + contract-register + scope_level 路由 + contract_refs）；schema 0.8.0 | CR-20260813-002 |
| 1.16.1 | 分发包标准化：通用打包 skill (tools/pack-skill/) + release-checklist Distribution Packaging + .gitignore 补强 | Patch (分发包治理) |
| 1.16.2 | 分发包幽灵引用修复：governance 例外放行 skill-contract + 排除 BLUEPRINT + 移除 16 号路由 + skill.json blueprint.file 移除 | Patch (幽灵引用修复) |
| 1.16.3 | 级联强制执行修复：待办→board 反向链路 + SUGGEST 强制呈现 + WF-2/5 补验证 + 14号去重引用 | Patch (级联强制) |
| 1.17.0 | PM 偏好通用化升级：5 能力模块（日报集成审查+主动提问/跨实体联动/关闭佐证/委派跟踪/沟通质量）+ 查询默认过滤；CQ-1/2/3 回归 PM Profile 层 | 无独立 CR（偏好沉淀） |
| 1.17.1 | 治理一致性修复：SKILL.md 路由表 16 号幽灵引用移除 + 版本失步全触点修正 + README×2 用例数/目录树修正 + Module 35 补档 + audit_release.py + 基线补档 | Patch (治理一致性) |
| 1.18.0 | 推导基线（Reasoning Baseline）：00号 §10 推导规则（推导链+跨源矛盾+动作规范+任务集关联）+ 05号 §3(3)a 终态事件豁免 + entity-registry 数据模板 + 周报/日报推导增强 + 脚本层同步 | Minor (推导能力升级) |
| 1.18.1 | 打包分发包命名标准化：新增 pack.py 本机主打包入口（产物命名 {BrandName}-Skill-v{version}.zip），排除模型实读 pack.ps1 单一事实源；audit 新增命名漂移守门断言；版本失步修正 + baselines/1.18.1 基线补档 | Patch (打包命名标准化) |
| 1.19.0 | 倒排计划能力+待办统一归属路由：WF-7 倒排编排 + WF-8 五入口归属路由 + WP 粗规划表/倒排元数据 + WP Ref 字段 + §8.1 流程反转 + WP 进度实时聚合 + 05号 §6.7 分层查询 + D15/D16 + Module 36（249 用例） | Minor (倒排计划与统一归属路由) |
| 1.19.1 | 迁移脚本参考模板库同步缺口修复：migrate sync_templates() 无条件前置补齐 ai/templates/ 参考库 + 规则20 §2 新增模板完整性检查(3b) + ALL_TEMPLATE_FILES 39→42 + outputs/.templates 补齐 + 双 Agent 审核收敛（V0.1→V0.2） | Patch (模板同步修复) |
| 1.20.0 | 需求双视图与开发文档关联：07号 §8.10 双视图机制（view_business = business 类 ATOM norm_text 派生聚合不加字段；view_dev 实现视图 + 原型/文档链接挂 REQ 层新增 2 可选列）+ §8.5 scope_scope 聚合排除硬约束（technical 类 ATOM 不参与范围判定）+ §8.6 触发 D 开发侧文档提取 + 大文档渐进导入；source-type-registry 新增 dev_prd/design_doc/api_spec/prototype/ui_spec；WF-2 需求上下文加载（00/05号，单次≤10条 REQ）+ 05号需求详情路由；17号词库开发侧分类标签 + 分类预筛/懒加载；12号 Excel 扩展列 U/V；19号双视图存在性巡检；日报模板关联原型/文档可选节；Module 37 Dual View（DV-001~010，总计 259） | Minor (需求双视图能力升级) |
| 1.21.0 | 倒排每日矩阵查询视图：05号 §6.7 新增倒排每日矩阵（人员×日期，portfolio 多 board 遍历+存量降级）+ 00号 WF-7 草案输出规范（contract_change）+ 10号查询附带提示；Module 38 Backward Scheduling Daily Matrix（BDM-001~010，总计 269） | Minor (contract_change) |
| 2.0.0 | 待办文件体系重构：todos/{date}/{owner}.md 个人待办 + daily-todo-binding 绑定索引 + board/里程碑板/旧索引归档 v1-legacy + 迭代并入 PLAN 文件体系 + 升级文件体系治理 | 升级方案（governance/migrations/upgrade-to-2.0.0.md） |
| 2.1.0 | 个人待办体系强化：22 号结转规则（Step 0 硬阻断）+ §0 六字段/T+1 沿用/冲突仲裁 + 进度列与双轨仲裁 + 目录简化（continuity→context、outputs→ai/）+ 报告结构规范化 + 升级执行文件体系（governance/migrations/ 49 回填）+ migrate 双迁移函数；CAP-027 | 升级方案 V0.42（governance/migrations/upgrade-to-2.1.0.md） |
| 3.0.0 | 双包拆分 + 单项目回归（architecture_change）：ChronoPM-Project 纯单项目录入 + ChronoPM-Portfolio 只读归集伴生包（只读五条/V-1~V-10/无 init）；09 号退役迁出；联邦挂载 schema（workspace 0.8.0→0.9.0，skill schemaVersion 0.6.0→0.7.0）；录入归属判定/禁镜像/废弃 PM 跟进条；登记册时间戳编号；RI 下沉项目级；Module 39 Dual-Pack（V3-001~030，总计 299） | 升级方案 V0.9.2a（governance/migrations/upgrade-to-3.0.0.md） |
| 3.1.0 | 路径残留纠偏 + 日报路由补全（Minor/fix）：个人日报查询/更新默认落 todos/{date}/{owner}.md；项目日报为按需生成存根（可能不存在）；月报残留清理；R1-R18（R9 除外，并入 CR-D）；workspace schema 仍 0.9.0；Module 40 QR-DR-001~003（总计 302） | CR-20260820-001 / upgrade-to-3.1.0.md |
| 3.1.1 | 开发仓三目录重组（Patch/infra）：ChronoPM-Project 包根自足 + governance-shared + 包内只留当前 upgrade；业务工作区零迁移，schema 仍 0.9.0；Module 41 LG-001~003（总计 305） | CR-20260820-002 / upgrade-to-3.1.1.md |
| 3.2.0 | DF-017 溯源标注 + 加载场景分类 + DF-018 主动识别习惯（Minor）；DF-007=P-WF-1+WF-8、DF-014=P-WF-2；存量零强制迁移；Module 42–43（总计 311） | CR-20260820-003 / upgrade-to-3.2.0.md |
| 3.3.0 | 关联待办 + 工作日志 TD Ref + 缩写治理小表（Minor）；WF-Linked 仅 SUGGEST；旧号不重编；Module 44–46（总计 321） | CR-20260820-004 / upgrade-to-3.3.0.md |
| 3.4.0 | 报告存根范式 + 时间线报（Minor）；非精确重合整段重汇聚；timeline 懒建不升 schema；Module 47 ST-001~006（总计 327） | CR-20260820-005 / upgrade-to-3.4.0.md |
| 3.5.0 | WP 独立存储（Minor/schema_change）：wps/WP-NNN.md + _index.md 加速器；计划 §3 改 4 列简表；写后必检 + D20/D21；WF-8 局部绑定检测 + 创建溯源 + DF-019；短号不变；workspace schema 0.9.0→0.10.0；Module 48–52（总计 344） | CR-20260820-006 / upgrade-to-3.5.0.md |
| 3.5.1 | 措辞残留修复（Patch）：project-brief §4 人员路由统一为本项目 resources；14 号月度索引改「停维」口径；outputs 模板 portfolio 枚举清理；project-notes/workspace-health 对齐；workspace schema 0.10.0 不变；零迁移，用例总数不变（344） | c7d000f / upgrade-to-3.5.1.md |
| 3.6.0 | 通用来源文档拆解（Minor/schema_change）：requirements/sources/{编号}/ 五件套 + 台账加速器；ATOM kind 扩展；source_type 全生命周期基线包按需启用；D22 限局部；互认键=簇固定号+指纹；schema 0.10.0→0.11.0；Module 53 SD-001~006（总计 350） | CR-20260820-007 / upgrade-to-3.6.0.md |
| 3.7.0 | 拆解增强+废 entity-registry+风险问题重构（Minor/schema_change/contract_change）：WF-SD-1/2、parse-log、ledger 9 列、分片、零清；WP §3b 实体行；登记册分表≤7 列、判定卡、短号 R-NNN/I-NNN；schema 0.11.0→0.12.0；Module 54–56（总计 380） | CR-20260820-008 / 021-001 / 021-002 / upgrade-to-3.7.0.md |
| 3.8.0 | 人员文件整合+确认话术+V-11/V-12+兼容人工成本台账（Minor/schema_change/contract_change）：register/transfer-log 退役进 backup；花名册=`_index` §1；待办无「待评审」；禁止未来日待办；§0.6 日合计拷贝追加；schema 0.12.0→0.13.0；Module 57 PC-001~010（总计 390） | CR-20260822-001 / upgrade-to-3.8.0.md |
| 3.9.0 | 过程日志+inbox合并+需求只绑WP+决策文件+关联处理方式AUTO；source-split无嵌套SKILL.md；对外给文件不给章节号；schema 0.13.0→0.14.0；Module 58（总计 443） | CR-20260822-002 / upgrade-to-3.9.0.md |
| 3.10.0 | 对话日志改列+集层 logs+投喂能耗入库+全员建档+TD 编号+WP 时间盒；schema 保持 0.14.0；Module 59（总计 470） | CR-20260823-001 / upgrade-to-3.10.0.md |
| 3.11.0 | WP 状态链+阶段执行人+词库感应+生成物落盘约束+计划 5 节与投影闸；schema 保持 0.14.0；Module 60–64（总计 525） | CR-20260824-001 / upgrade-to-3.11.0.md |
| 3.12.0 | 过程索引+简单查询仅05+删QODER特例；待办恰好1个WP；派活查重；拆文件强制sources入库；schema 保持 0.14.0；Module 65–67（总计 552） | CR-20260824-002/003/004 / upgrade-to-3.12.0.md |
| 3.13.0 | WP联动SCAN/ADVANCE+计划节点子行+effect正常/废弃+V-13时间窗归集+skill-gap-skill；schema 保持 0.14.0；Module 68（总计 589） | CR-20260824-005 / upgrade-to-3.13.0.md |
| 3.14.0 | 计划6节去子行+13标准阶段+ASCII编号+project-info/+删is_milestone+SCAN冻结+看计划全文；schema 0.14.0→0.15.0；Module 69（总计 601） | CR-20260825-001 / upgrade-to-3.14.0.md |
| 3.15.0 | 存量受控迁移+§4模板人期+skill_gap单文件+current_operator+日报载22+四套verify+init README转义；schema 0.15.0→0.16.0 | CR-20260825-002 / upgrade-to-3.15.0.md |
| 3.16.0 | 日期格式+WP§8字段边界+§4 verify分通道+版本/模板权威源+related_wps+Mermaid仅对话；schema 保持 0.16.0；Module 70（总计 620） | CR-20260826-001 / upgrade-to-3.16.0.md |
| 3.17.0 | 关联记录盖章+图形态/派生落盘+查询摘要链接+skill-gap辅助+功能点阶段全齐AUTO；schema 保持 0.16.0；Module 71（总计 642） | CR-20260826-002 / upgrade-to-3.17.0.md |

---

## 12. External AI Review Guide

### 12.1 审查目标

外部 AI 阅读本文件后，应能够：

1. 理解 ChronoPM Skill 的设计目的、架构决策和当前能力
2. 识别能力矩阵中的薄弱环节（L2 及以下）
3. 评估已知局限中哪些是可改进的设计债务
4. 对 Roadmap 中的规划能力提出建议
5. 发现 Blueprint 中遗漏的能力或风险

### 12.2 审查维度

| 维度 | 关注点 |
|---|---|
| 能力完整性 | 是否有项目管理场景未被覆盖？能力矩阵是否有遗漏？ |
| 规则一致性 | 规则之间是否有冲突？依赖关系是否正确？ |
| 成熟度合理性 | 成熟度评级是否准确？L2 能力是否有明确的提升路径？ |
| 设计债务 | Design Debt 清单是否完整？是否有未识别的债务？ |
| 数据流完整性 | 数据流是否有断点？是否有数据进入但无处去的情况？ |
| 边界合理性 | Known Boundaries 是否合理？是否有应该突破的边界？ |
| Roadmap 合理性 | 规划能力的优先级是否合理？是否遗漏了关键能力？ |

### 12.3 不可轻易推翻的设计决策

审查者在挑战以下决策时，必须给出充分理由和迁移成本评估（见 §4 "Design Decisions Not To Change Lighty"）：

1. 使用 Markdown 作为主事实源格式
2. ai/ 与业务目录分离
3. outputs/ 与 ai/ 分离
4. 项目集模式采用集中式
5. 查询采用索引优先
6. 历史导入不直接覆盖
7. Skill 变更采用治理流程
8. 工作区升级需用户确认
9. 同人同天日报合并追加不覆盖
10. 快照冻结后不可静默覆盖

### 12.4 反馈格式要求

外部 AI 审查后建议按以下格式输出：

```markdown
## 审查结论

### 总体评价
[一段话概述对 Skill 的整体评价]

### 发现的问题

| 编号 | 类型 | 严重程度 | 描述 | 建议改进 |
|---|---|---|---|---|
| REV-001 | 能力遗漏 / 规则冲突 / 成熟度误评 / 设计债务未识别 / 数据流断点 / 其他 | 高/中/低 | [具体描述] | [具体建议] |

### 对 Roadmap 的建议
[对规划能力的优先级调整或新增建议]

### 对设计决策的挑战（如有）
[仅当认为某设计决策需要调整时填写，必须包含迁移成本评估]
```

### 12.5 审查注意事项

1. **不要试图操作 Skill**：Blueprint 是被动文档，不包含执行指令
2. **不要建议推翻核心设计决策**：除非能证明当前决策导致了不可接受的后果
3. **聚焦薄弱环节**：L2 能力（历史衔接）是最需要建议的部分
4. **关注完整性**：是否有应该有但没有的能力？数据流是否有断点？
5. **区分边界与缺陷**：Known Boundaries 是有意为之的，Design Debt 才是待修的

---

## 13. Update Policy

### 13.1 分级触发

| 触发条件 | 更新级别 | 更新内容 |
|---|---|---|
| Major 版本发布 | 必更 | 全文审查：能力地图、架构决策、Roadmap、Limitations |
| Minor 版本发布 | 必更 | 能力地图、版本状态、Roadmap、Known Limitations、数据流 |
| 新增/删除能力 | 必更 | Capability Map、Rule Dependency |
| workspace schema 变化 | 必更 | Schema Evolution |
| 新增治理机制 | 必更 | Governance Model |
| 新增核心数据流 | 必更 | Data Flow |
| 新增迁移/升级机制 | 必更 | Workspace Upgrade |
| Patch 版本发布 | 应更 | 版本元数据（版本号、日期） |
| 仅新增模板/测试/措辞 | 免更 | CHANGELOG 标注 "Blueprint Impact: none" |

### 13.2 结构性变更需走 CR

以下 Blueprint 变更需走完整 CR 流程（见 `16-skill-governance-rules.md` §2）：

- 新增/删除一级章节
- 新增/删除 Capability ID
- 改变能力分类体系
- 将某能力标记为废弃
- 修改核心设计决策解释
- 修改外部审查标准
- 修改 Document Boundary 定义
- 与 SKILL.md / skill.json 出现能力口径不一致

### 13.3 普通更新走轻量流程

以下 Blueprint 变更只需 CHANGELOG 记录：

- 版本号更新
- Roadmap 补充
- Known Limitations 补充
- 状态从已规划改为部分落地 / 已落地
- 审查指南措辞优化

### 13.4 层级归属

Blueprint 属于**文档层（Documentation Layer）**，不属于核心契约层。

- 普通更新：无需 CR，记录 CHANGELOG
- 结构性变更：需走 CR
- 发布前必检：VERSION / skill.json / CHANGELOG / Blueprint 版本一致性

### 13.5 CHANGELOG 标注要求

每次版本发布时，CHANGELOG 中必须标注 Blueprint 影响：

```markdown
Blueprint Impact: [full / metadata-only / none]
```

- `full`：正文内容有实质性更新（能力矩阵、架构决策、数据流等）
- `metadata-only`：仅更新版本号和日期
- `none`：本次变更不影响 Blueprint 内容
