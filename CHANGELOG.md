# Changelog

本文件记录 ChronoPM Skill 的版本变更历史。版本号遵循语义化版本（MAJOR.MINOR.PATCH）。

---

## 1.9.0 — 2026-08-10

### Added
- 新增 CAP-023：PM Profile 用户习惯学习与偏好适配
- 新增 `references/21-pm-profile-rules.md`：PM Profile 学习规则全量定义（定位、边界、5 类偏好分类、九步学习流程、五状态机、确认交互、应用规则、异常处理、扩容规则、禁止事项）
- 新增 `assets/templates/pm-profile-template.md`：PM Profile 文件模板（偏好映射表 + 待确认表 + 已否决/已废弃表 + 索引 + Change Log）
- 新增 PM Profile 数据文件：`ai/portfolio/context/pm-profile.md`（项目集模式）/ `ai/context/pm-profile.md`（单项目模式）
- 新增规则优先级 Level 2.5：PM Profile confirmed 偏好（软偏好，项目规则未指定时生效）
- 新增触发词："我的偏好""习惯设置""PM Profile""偏好学习""以后按这种格式"

### Changed (contract_change)
- `SKILL.md` 增加 PM Profile 路由说明、触发词、Level 2.5 优先级、§15 规则索引 21 号条目；frontmatter version → 1.9.0
- `references/00-pm-main-rules.md` §2.7 意图检测前增加 PM Profile 加载步骤；§6 规则优先级新增 Level 2.5
- `references/06-file-rules.md` 新增 §11 PM Profile 文件规范
- `references/20-workspace-version-rules.md` §2 健康检查新增 1.9.0+ 检查项；§5 兜底逻辑新增 pm-profile.md 缺失策略
- 初始化与迁移脚本支持 PM Profile 文件创建
- 修复 `scripts/chronopm_init/config.py` 中 `SKILL_VERSION` 长期滞后问题（自 v1.7.1 起未同步，1.7.0 → 1.9.0）

### Compatibility
- Workspace Schema 保持 0.5.0（不变）
- 不删除、不弱化 CAP-001 ~ CAP-022
- PM Profile 文件不存在时降级跳过，不影响既有流程
- 不影响事实源内容准确性和安全底线

### 回归测试
- `tests/regression-suite.md` 新增第 24 模块「PM Profile（用户偏好学习）」，含 PP-001 ~ PP-010（10 用例：7 正向 / 3 回归）
- 用例合计 122 → 132
- SK-1E 规则索引计数更新：00-20 → 00-21（共 22 条）
- VR-001 版本号更新：1.8.4 → 1.9.0

Blueprint Impact: full — §5.2 能力矩阵追加 CAP-023、§5.3 成熟度统计更新、§7.1/§7.2 规则清单与依赖图追加 21 号、§8 追加 PM Profile 数据流、§9.1 稳定能力列表追加、§10.1 边界表追加、§11.3 已落地变更追加 1.9.0 行、§1 基本信息（版本/文件总数/描述）

---

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

## 1.8.3 — 2026-08-10

### Changed
- 查询/需求/输出物规则表格化（CR-20260810-005，Patch，覆盖 CAP-005/CAP-006/CAP-008）：
  - `references/05-query-rules.md`（CAP-005）由 413 行瘦身至 **252 行**：问题类型路由表（12 类）、项目集路由、Quick Query 路由表、PM 待办 9 章节、历史查询、人员查询优先级、最小读取、数据来源声明均以紧凑表格/要点保留，未删语义
  - `references/11-output-artifact-rules.md`（CAP-006）由 341 行瘦身至 **204 行**：富批次目录结构、输出状态机、多轮修改复用批次、来源追溯、输出物确认规则等压缩为要点，未删语义
  - `references/07-requirement-rules.md`（CAP-008）保持 **139 行**：仅格式统一微调，字段定义与状态机未变

### 说明
- 全部采用库内规范化，未新增模板文件（`assets/templates/` 仍 38 个）也未新增规则文件（references 仍 21 个）

### 回归测试
- `tests/regression-suite.md` 新增 23. Query/Requirement/Artifact Rules 模块（QR-1A~1D），覆盖 05/11 瘦身、07 契约不变、模拟查询+需求登记语义完整
- 用例合计 118 → 122

Blueprint Impact: metadata + 既有 CAP-005/CAP-006/CAP-008 承载规则文件 05/11/07 重构，无新增能力点

---

## 1.8.2 — 2026-08-10

### Changed
- 日报规则重构（CR-20260810-004，Patch）：`references/01-daily-report-rules.md` 由 594 行瘦身至 **221 行**
- 6 个文件模板代码块外移为模板指针（personal-daily / project-daily / weekly-report / personal-progress / portfolio-weekly / index-formats），模板仍复用 `assets/templates/` 既有文件
- 术语归一化 §1.2b 下沉至 `references/17-domain-glossary-rules.md`（§4/§6 完整九步流程），01 仅保留入口要点 + 指针
- 压缩 AI 输出片段代码块（候选资源变更/资源变动建议更新清单/周报更新/项目集汇总/个人进度联动）为内联格式要点
- 索引输出格式压缩为列要点引用 `assets/templates/index-formats.md`

### Fixed
- 修复 01-daily-report-rules.md 重复的 §2.3 汇总规则块（原行 262-266 与 254-258 重复）

### 回归测试
- `tests/regression-suite.md` 新增 22. Daily Report Rules 模块（DR-1A~1D），覆盖 01 瘦身/模板引用有效性/术语下沉/资源变动内联格式
- 用例合计 114 → 118

Blueprint Impact: metadata + 既有 CAP-002（Daily Report）/CAP-003（Weekly Report）承载规则文件 01 重构，无新增能力点

---

## 1.8.1 — 2026-08-10

### Changed
- 文件管理规则重构（CR-20260810-003，Patch）：`references/06-file-rules.md` 由 587 行瘦身至 **299 行**，收敛为纯文件管理规则（命名/目录边界/创建/更新/瘦身/索引/归档/安全）
- §0 工作区版本兼容性检查（原 231 行）整体外移至新建 `references/20-workspace-version-rules.md`（版本检查/健康检查/兼容模式/兜底逻辑/升级提醒/触发词/迁移模式）
- §0c 词库文件规范并入 `references/17-domain-glossary-rules.md` 末尾（新增 §17 词库文件规范）
- §6 索引格式完整 markdown 代码块移至 `assets/templates/index-formats.md`，06 仅保留列定义
- §0 原有目录树章节编号合并修复，06 现为 §1-§10 连续编号

### Fixed
- 修复 06-file-rules.md 两个 `## 1.` 重复章节编号

### 回归测试
- `tests/regression-suite.md` 新增 21. File Contract 模块（FC-1A~1D），覆盖 06 瘦身/20 外移完整性/17 词库文件规范/路由指针
- 更新 SK-1E 规则索引计数（00-19 → 00-20，共 21 条）

Blueprint Impact: metadata + 规则清单映射更新（CAP-015、§7.1 清单、§7.2 依赖图补充 20 号）

---

## 1.8.0 — 2026-08-10

### Changed (contract_change)
- SKILL.md 瘦身（CR-20260810-002，Minor）：478 行 → **297 行**，主入口改为"路由器"
- 状态枚举、输出规范、里程碑体系、例外容忍度下沉至 `references/00-pm-main-rules.md`（§5a/§5.4/§5.5/§5b/§5c）
- §3 工作区结构精简为高层级目录树，细目录指向 `references/06-file-rules.md`
- §5 核心工作流由完整流程代码块精简为"一行摘要 + reference 指针"
- §6 提示词路由表、§7 安全底线、§8 ID 编码、§15 规则索引**完整保留不变**

### Fixed
- `SKILL.md`/`00` 中指向"SKILL.md 第 12/13 节"的旧引用改为指向 00 内部新节（§5b/§5c）

### 回归测试
- `tests/regression-suite.md` 新增 20. SKILL Navigation 模块（SK-1A~1G），覆盖行数、路由表/安全底线/ID编码/规则索引完整性、下沉落点

Blueprint Impact: contract_change（Capability Map / Decision Log / Roadmap 已同步更新）

---

## 1.7.1 — 2026-08-10

### Changed
- 脚本重构（CR-20260810-001）：`scripts/init_workspace.py` 由 1269 行单体脚本重构为入口壳 + `scripts/chronopm_init/` 包（config/template_renderer/file_registry/validators/workspace_builder），CLI 参数与生成物目录结构完全不变
- Skill 版本升级 1.7.0 → 1.7.1（Patch：脚本内部重构，向后兼容，不改 references/模板/schema）

### Fixed
- `init_workspace.py` 9 处硬编码月份目录 `202608` 改为动态生成（`datetime.now().strftime("%Y%m")`），避免月份过期时初始化出错误的历史月份目录

### 回归测试
- `tests/regression-suite.md` 新增 19. 脚本契约模块（SC-1A~1F），覆盖 CLI 参数、产物目录结构、动态日期、参数校验行为

Blueprint Impact: metadata-only

---

## 1.7.0 — 2026-08-10

### Added
- 新增项目初始化向导能力：`references/18-init-wizard-rules.md`（六步引导流程：合同层→项目层→迭代层→需求层→资源层→里程碑层，含触发条件、跳过机制、进度记忆、断点续接、确认写入、文件上传解析规则）
- 新增项目信息完整性巡检与补全提醒能力：`references/19-info-completeness-rules.md`（7层检查维度：合同/项目/迭代/需求/任务/资源/里程碑，P0-P3分级提醒，强/弱触发场景，静默模式，完整性巡检报告）
- 新增迭代登记册模板：`assets/templates/iteration-register-template.md`（ITR-NN编码、迭代总览表、迭代详情、关联里程碑可选关联）
- 新增迭代 ID 编码 `ITR-NN`（SKILL.md §8）
- `SKILL.md` 路由表新增"项目初始化向导"和"项目信息完整性巡检"两个场景
- `SKILL.md` §5.1c 新增初始化向导工作流描述
- `SKILL.md` §15 规则索引新增 18 和 19 规则条目
- `SKILL.md` front matter 新增初始化向导/迭代管理/完整性巡检的触发关键词和描述
- `00-pm-main-rules.md` §2.7 默认意图检测新增"初始化"和"完整性巡检/补全提醒"两个意图类型
- `10-update-trigger-rules.md` 新增 §8 更新后关联字段完整性检查机制（检查时机、P0-P3分级、与14-self-check的协作边界）
- `init_workspace.py` 新增 `create_iteration_register()` 函数，单项目和项目集模式均生成 `plans/iteration-register.md`
- `init_workspace.py` 完成提示新增初始化向导引导（"对 AI 说：初始化项目"）
- `init_workspace.py` `ALL_TEMPLATE_FILES` 新增 `iteration-register-template.md`
- 6 个模板增强：
  - `project-context-template.md`：新增合同信息表（合同名称/总额/类型/范围摘要/立项时间/启动时间/计划完工时间/测算周期）
  - `project-brief-template.md`：新增立项时间字段、迭代概览一行摘要小节、completeness_status/last_completeness_check 可选字段
  - `project-index-template.md`：子项目清单新增迭代数列
  - `requirement-register-template.md`：总览表新增所属迭代列（ITR-NN / 未分配）
  - `resource-register-template.md`：新增迭代分配视图小节
  - `init_workspace.py` 中 `create_brief_file()` 和 `create_context_file()` 增加对应占位字段

### Changed
- Skill 版本升级 1.6.1 → 1.7.0（Minor：新增能力，向后兼容）
- `init_workspace.py` SKILL_VERSION 常量更新为 1.7.0（修正原 1.6.0 落后问题）
- `SKILL.md` front matter version 更新为 1.7.0
- `skill.json` version 更新为 1.7.0
- `skill.json` blueprint.lastVersion 更新为 1.7.0
- `skill.json` versionHistory 新增 1.7.0 条目
- `SKILL_BLUEPRINT.md` 版本号更新为 1.7.0，能力矩阵新增 CAP-020/CAP-021，规则清单新增 18/19，数据流新增初始化/巡检流程
- `skill-contract.md` Protected Capabilities 新增 INIT_WIZARD 和 COMPLENESS
- `tests/regression-suite.md` 新增 17. 初始化向导（IW-001~IW-005）和 18. 信息完整性巡检（IC-001~IC-005）模块

### Fixed
- 修复 portfolio 模式下 `ai/logs/` 目录缺失导致 `migration-log.md` 创建失败的预存 Bug
- 修复 `generate_portfolio_readme()` 中 `{子项目}` 被 f-string 解析为变量导致 `NameError` 的预存 Bug
- 修正 `init_workspace.py` SKILL_VERSION 常量从 1.6.0 更新至 1.7.0（原 1.6.0 落后于 VERSION 文件的 1.6.1）

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段，不改变目录结构模式）
- 不删除、不弱化任何现有能力
- 路由表仅新增 2 行，不移除原有路由
- 14-self-check-rules.md 不修改职责，与 19-info-completeness-rules.md 保持边界分离

### Blueprint Impact
- full：新增 CAP-020（初始化向导）和 CAP-021（信息完整性巡检），规则清单新增 18/19，数据流新增初始化向导和完整性巡检流程，成熟度统计更新，已知局限更新
- workspace schema 不变

### Upgrade Notes
- 从 1.6.1 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增能力**：
  1. 初始化向导：用户说"初始化项目"即可启动六步向导，引导录入合同/项目/迭代/需求/资源/里程碑基线信息
  2. 迭代登记册：新增 `plans/iteration-register.md` 文件，正式管理迭代信息（ITR-NN 编码，可选关联里程碑）
  3. 信息完整性巡检：日常使用中自动检查字段缺失，P0/P1 缺失会主动提醒
- 旧工作区如需使用迭代登记册，可手动创建 `plans/iteration-register.md`（从模板复制）或对 AI 说"初始化项目"补录。
- 已有需求登记册中新增了"所属迭代"列，默认值为"未分配"，不影响现有数据。
- 已有资源登记册中新增了"迭代分配视图"小节，不影响现有资源清单表。

---

## 1.6.1 — 2026-08-10

### Fixed
- 修正 `SKILL_BLUEPRINT.md` 版本号：1.5.0 → 1.6.1，补全 v1.6.0 词库能力记录（CAP-019）
- 修正 `SKILL_BLUEPRINT.md` 成熟度统计：L3 能力从 14 项更新为 15 项
- 修正 `SKILL.md` §3.1 工作区目录树：修复 `outputs/` 重复出现和 `prompts/`、`templates/`、`continuity/` 缩进层级错误问题

### Added
- `05-query-rules.md` 新增 §5.4a 人员查询事实源优先级：定义 4 级数据来源优先级（register > transfer-log > context > 日报目录），明确人员查询默认只读 register，字段缺失时降级推断并标注"未确认"
- `01-daily-report-rules.md` 新增候选资源变更规则：日报中人员变动信号只能产生候选变更，不得自动覆盖 register；明确禁止将日报中出现的人员自动认定为正式项目成员
- `09-portfolio-rules.md` 新增 §5.6 resource-register 与 project-context 一致性检查：5 种差异类型处理规则、差异报告输出格式、用户选择 A/B/C/D 确认机制

### Changed
- `06-file-rules.md` §1.1a 修改 project-brief.md 规则：团队信息指针化，不复制 register 完整团队列表，改为指向 register 的指针；不自动删除 brief 已有团队列表，只新增指针并标记冗余待清理
- `project-brief-template.md` 团队成员部分改为指针化，指向 resource-register.md 和 transfer-log.md
- `SKILL.md` frontmatter 版本号更新为 1.6.1
- `skill.json` 版本号更新为 1.6.1
- `SKILL_BLUEPRINT.md` 版本号更新为 1.6.1

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段）
- 不新增规则文件（不拆分 06-file-rules.md）
- 不合并路由表（42 行路由保持不变）
- 不修改 QODER_RULES.md
- 不新增治理通道
- 不修改 resource-register.md 模板字段（"参与子项目"字段留待 v1.6.2）
- 不删除、不弱化任何现有能力

### Blueprint Impact
- full：版本号修正、能力矩阵补充 CAP-019、Known Limitations 无变化
- workspace schema 不变

### Upgrade Notes
- 从 1.6.0 升级：Patch 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心修复**：资源事实源优先级规则澄清。人员查询时默认只读 `resource-register.md`，不再合并搜索 4 处文件。日报中人员变动只能产生候选变更，不自动覆盖事实源。
- `project-brief.md` 模板团队部分已指针化，旧 brief 中的团队列表不自动删除，需用户确认后清理。
- 本次不涉及路由表合并、06 拆分、模板字段新增等结构级变更，这些留待后续版本。

---

## 1.6.0 — 2026-08-10

### Added
- 新增领域术语词库能力：`references/17-domain-glossary-rules.md`（16 节完整规则，含状态机、置信度判定、9 步归一化流程、纠错、自动学习 pending、确认式学习、索引、去重、扩容、异常处理）
- 新增词库模板文件：`assets/templates/domain-glossary-template.md`（内置用户已确认初始词条：外资→外商投资、农专→农民专业合作社）
- 日报处理增加术语归一化预处理（`01-daily-report-rules.md` §1.2b，9 步流程）
- 评审记录处理增加术语归一化预处理（`02-meeting-rules.md` §0b）
- 查询路由增加术语归一化（`05-query-rules.md` §1.5）
- 更新触发增加术语归一化前置步骤（`10-update-trigger-rules.md` §1b）
- 文件管理增加词库文件规范和瘦身规则（`06-file-rules.md` §0c）
- `SKILL.md` 路由表追加 17 规则（日报/评审/查询/更新触发场景），新增"词库管理"独立场景
- `SKILL.md` front matter 增加词库管理触发关键词：术语、词库、缩写、纠正、domain-glossary
- `SKILL.md` §15 详细规则索引新增 17 规则条目
- `init_workspace.py` 新增 `--glossary` 参数，新项目初始化时创建词库模板（内置初始词条，不自动抽取历史术语）
- `migrate_workspace.py` 新增 `--create-glossary` 选项，旧工作区可创建词库模板

### Changed
- Skill 版本升级 1.5.0 → 1.6.0
- `init_workspace.py` SKILL_VERSION 常量更新为 1.6.0
- `migrate_workspace.py` CURRENT_SKILL_VERSION 常量更新为 1.6.0

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段）
- 不删除、不弱化任何现有能力
- 路由表仅追加 17 规则，不移除原有必须加载规则

### Blueprint Impact
- minor：新增能力（领域术语词库）
- workspace schema 不变

### Upgrade Notes
- 从 1.5.0 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增**：领域术语词库能力。词库不存在时完全兼容现有流程，不影响旧工作区。
- 旧工作区如需启用词库功能：`python scripts/migrate_workspace.py --project-root . --create-glossary`
- 新工作区初始化时如需创建词库：`python scripts/init_workspace.py --project-root . --mode portfolio --sub-projects ... --glossary`
- 词库内置用户已确认初始词条（外资→外商投资、农专→农民专业合作社），不自动抽取历史术语。

---

## 1.5.0 — 2026-08-09

### Added
- 新增 `QODER_RULES.md`：Qoder 环境专用轻量入口（~4KB），包含适用前提、快捷路由表（5 种常见查询只读 1-2 个文件）、最小读取原则、数据来源声明（统一列表格式 + 文件修改时间降级处理）、安全底线（精简版）、复杂场景按需加载引用、安全升级触发规则
- `references/05-query-rules.md` 新增 §6 最小读取原则（全局规则）：区分简单查询（1-2 文件）和复杂任务（按需多文件但列清单）、快捷查询文件映射表、禁止全目录扫描
- `references/05-query-rules.md` 新增 §7 数据来源声明：5 种查询回答末尾标注数据来源路径、文件修改时间降级规则（无法获取时不编造）

### Blueprint Impact
- full：Known Limitations 增加 Qoder 屏闪说明 + Runtime Compatibility 记录

### Upgrade Notes
- 从 1.4.0 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增**：`QODER_RULES.md` 供 Qoder 环境使用，减少每轮上下文注入量和链式文件读取，缓解屏闪。
- `05-query-rules.md` 新增的最小读取原则适用于所有环境，但不影响复杂任务（日报处理、周报生成等）的文件读取。
- 数据来源声明仅限 5 种查询（版本/任务/风险/项目概况/日报提交状态），复杂报告按原输出规范。

---

## 1.4.0 — 2026-08-09

### Added
- 新增 `SKILL_BLUEPRINT.md`：13 章节架构蓝图文档（架构决策+能力矩阵与成熟度+Schema演进+规则依赖图+数据流+已知局限分类+Roadmap+外部审查指南+更新策略）
- `skill.json` 新增 `blueprint` 元数据对象（file/lastUpdated/lastVersion/updateRequiredOn/metadataUpdateRequiredOn/optionalOn）
- `skill.json` versionHistory 补全 1.3.0、1.3.1、1.4.0 条目
- `16-skill-governance-rules.md` 新增 §17 Blueprint 更新规则（分级触发：必更/应更/免更 + 结构性变更走CR + 普通更新轻量流程 + 层级归属 + CHANGELOG标注要求）
- `governance/review-checklists/release-checklist.md` Documentation 章节新增 3 个 Blueprint 检查项
- `governance/contracts/skill-contract.md` Rule Layer Classification 表新增文档层分类
- `governance/change-requests/CR-template.md` 新增 Blueprint Impact 标注字段
- `tests/regression-suite.md` 新增 Blueprint 模块测试用例（BP-001 到 BP-010，10 个用例）

### Blueprint Impact
- full：本次为 Blueprint 首次创建，全文新增

### Upgrade Notes
- 从 1.3.1 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增**：`SKILL_BLUEPRINT.md` 可随时复制给外部 AI 审查 Skill 能力和待补充项。
- Blueprint 更新纳入发布检查清单，后续每次版本发布时需检查 Blueprint 是否需要更新。

---

## 1.3.1 — 2026-08-09

### Added
- `16-skill-governance-rules.md` 新增 §2.1 升级方案审查文档（AP）输出要求：7 个必填章节（变更概述/影响点详细分析/变更策略与设计思路/修改范围清单/回归测试计划/风险评估与回滚方案/版本影响）
- `16-skill-governance-rules.md` 新增 §2.2 审查输出格式要求（标准化 markdown 模板）
- `16-skill-governance-rules.md` 新增 §2.3 禁止跳过审查规则（即使用户说"直接改"也必须先输出 AP-1 到 AP-4）
- `CR-template.md` 新增升级方案审查文档章节（AP-1 到 AP-7 完整模板）

### Upgrade Notes
- 从 1.3.0 升级：PATCH 版本，直接覆盖即可。
- **核心改变**：以后每次 Skill 变更前，AI 必须先输出 7 章节升级方案审查文档，用户审查确认后才执行。

---

## 1.3.0 — 2026-08-09

### Added
- `06-file-rules.md` 新增 6 个工作区升级感知规则：
  - §0.0b 功能触发时检查（用 todo 但索引缺失→提示升级而非扫描）
  - §0.0c 兼容模式（用户拒绝升级时明确提示降级影响）
  - §0.0e 升级提醒频率控制（`ignored_until` 防止反复弹窗）
  - §0.0f 升级触发词（12 个触发表达式）
  - §0.0g 工作区健康文件（`.workspace-health.md` 人类可读）
  - §0.0h 迁移模式（structure-only / recent-7-days / current-month / full-rebuild）
- 新增 `assets/templates/workspace-health-template.md`：工作区健康状态模板
- `skill.json` 新增 `supportedWorkspaceSchema`（min/current）和 `migrations` 迁移路径
- `migrate_workspace.py` 新增 `--index-mode` 参数、健康文件生成、索引重建函数

### Migration
- Workspace schema: 无变更（仍为 0.5.0）
- Migration required: No（规则增强，无需迁移已有工作区）

### Upgrade Notes
- 从 1.2.1 升级：直接覆盖即可。已有工作区无需迁移。
- 新增的 `.workspace-health.md` 会在下次运行 `migrate_workspace.py` 时自动生成。

---

## 1.2.1 — 2026-08-09

### Added
- 新增 `scripts/migrate_workspace.py`：工作区迁移脚本，自动检测版本差距、缺失目录和文件，支持 `--dry-run` 预览模式
- `06-file-rules.md` 新增 §0.0a 工作区健康检查：每次会话首次交互时自动检测工作区版本和能力完整性，输出健康报告和迁移建议
- `06-file-rules.md` 新增 §0.0b 兜底逻辑：缺失能力时不报错中断，按兜底策略处理（如 todos 缺失退化为读 board + 日报索引）

### Upgrade Notes
- **从 1.2.0 升级**：PATCH 版本，直接覆盖即可。
- **使用方法**：当 Skill 升级后，用户在工作区执行 `python scripts/migrate_workspace.py --project-root .` 即可一键迁移。

---

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

## 1.1.0 — 2026-08-09

### Added
- 新增 `references/15-snapshot-rules.md`：计划快照与实际执行规则（快照冻结/实际摘要/历史索引/热冷分离/计划vs实际对比/Todo ID稳定）
- 新增 5 个模板：daily-todo-snapshot / daily-todo-actuals / weekly-todo-snapshot / weekly-todo-actuals / todo-history-index
- 新增 `ai/portfolio/todos/snapshots/` 目录（daily + weekly）
- 新增 `ai/portfolio/todos/actuals/` 目录（daily + weekly）
- 新增 `ai/portfolio/todos/history-index.md`
- `05-query-rules.md` 新增历史查询路由（触发词 + 查询顺序 + 常见路由表 + 热冷数据分离）
- `01-daily-report-rules.md` 新增 §5.6c 快照与实际执行生成规则
- `10-update-trigger-rules.md` 新增快照信号触发
- `06-file-rules.md` 目录结构新增 snapshots/ 和 actuals/

### Changed
- schema 从 0.4.0 升级到 0.5.0（新增 todos/snapshots/ 和 todos/actuals/ 目录）
- `init_workspace.py` 初始化时创建 snapshots/actuals 目录

### Upgrade Notes
- **从 1.0.1 升级**：schema 从 0.4.0 升级到 0.5.0。旧工作区需手动创建 `ai/portfolio/todos/snapshots/daily/`、`snapshots/weekly/`、`actuals/daily/`、`actuals/weekly/` 目录，或重新运行 `init_workspace.py`。
- **核心改变**：当前待办查索引，历史计划查快照，执行结果查 actuals；支持计划vs实际偏差对比。

---

## 1.0.1 — 2026-08-09

### Fixed
- `05-query-rules.md` 新增 PM 待办查询输出规范：当 PM 问"我明天的待办"时，必须输出 9 章节全景视图（PM直接任务 + 全团队明日计划 + 风险 + 问题 + 里程碑 + 资源变动 + 本周计划对照 + 待协调事项 + 无计划项提醒），而非仅列出 PM 个人任务
- 明确数据读取路径（9 个数据源按优先级读取）
- 新增禁止行为（只列 PM 个人任务就结束、不读看板就回答没任务、不展示团队明日计划）

### Upgrade Notes
- 从 1.0.0 升级：PATCH 版本，直接覆盖即可。

---

## 1.0.0 — 2026-08-09

### Added
- 新增 `references/14-self-check-rules.md`：自查与完整性校验规则
  - 索引预建规则（禁止边查边建、索引自动维护时机、索引一致性检查）
  - 日报处理自查清单 D1-D10（今日完成/进行中/明日计划/阻塞/风险/资源/工时/月度索引/个人进度/合并检查）
  - 会议纪要处理自查清单 M1-M7（行动项/决策/风险/问题/变更/资源/索引）
  - 评审材料处理自查清单 R1-R6（结论/待确认/风险/行动项/变更/归档）
  - 风险/问题追溯自查清单 T1-T7（多源交叉校验：登记册 vs 日报 vs 会议 vs 周报 vs 问题 vs 任务看板）
  - 遗漏补救规则（立即补充、原因分析、遗漏统计）
  - 索引过期检测（24h/7d 阈值 + 过期提示格式）
  - 多轮自查规则（用户追问时重新执行 + 扩大范围）

### Changed
- `SKILL.md` 版本号升级到 1.0.0（正式版）；路由表新增2个自查场景；规则索引新增第14条

### Upgrade Notes
- **从 0.9.0 升级**：无 schema 变更（均为 0.4.0）。直接覆盖即可。
- **核心改变**：AI 每次处理文档后必须执行自查清单并输出结果；查询时禁止边查边建索引；风险/问题追溯必须多源交叉校验。
- **1.0.0 标记**：本版本为 ChronoPM Skill 正式版，核心能力体系已完整。

---

## 0.9.0 — 2026-08-09

### Added
- `05-query-rules.md` 新增 §2.5 快速查询路由：Quick Query 路由表（8种查询场景的优先读取/兜底读取/禁止动作）、查询性能规则（6条）、索引缺失处理流程、禁止默认临时脚本规则
- 新增 `ai/portfolio/todos/` 目录：personal-todo-index.md（按人聚合）、daily-todo-index.md（按日期聚合）、weekly-todo-index.md（按周聚合）
- 新增 `assets/templates/pm-daily-todo-template.md`：PM 每日待办模板（PM直接任务 + 全团队明日计划 + 风险 + 问题 + 里程碑 + 资源变动 + 本周计划对照 + 待协调事项 + 无计划项提醒）
- 新增 `assets/templates/personal-todo-index-template.md`：个人待办索引模板
- 新增 `assets/templates/daily-todo-index-template.md`：每日待办索引模板
- 新增 `assets/templates/weekly-todo-index-template.md`：每周待办索引模板
- `01-daily-report-rules.md` 新增 §5.6b 待办索引同步规则（日报→todo index 自动同步）
- `10-update-trigger-rules.md` 新增待办信号触发词
- `09-portfolio-rules.md` 增加待办索引引用
- `06-file-rules.md` 目录结构新增 todos/ 目录

### Changed
- `init_workspace.py` 初始化时创建 `ai/portfolio/todos/` 目录

### Upgrade Notes
- **从 0.8.0 升级**：无 schema 变更（均为 0.4.0）。旧工作区需手动创建 `ai/portfolio/todos/` 目录，或重新运行 `init_workspace.py`。
- **核心改变**：AI 查询待办时优先读索引文件，不再默认全量扫描日报/会议纪要。禁止为简单查询创建临时脚本。

---

## 0.8.0 — 2026-08-09

### Added
- 新增 `references/13-continuity-rules.md`：项目阶段衔接规则（5种导入模式、内容路由表、结转流程、冲突检测、不可覆盖规则、版本兼容、ID规则）
- 新增 `assets/templates/carryover-register-template.md`：结转事项登记册模板
- 新增 `assets/templates/project-lineage-template.md`：阶段谱系模板
- 新增 `assets/templates/legacy-sources-template.md`：历史来源登记模板
- 新增 `assets/templates/import-log-template.md`：导入日志模板
- 新增 `ai/continuity/` 目录（project-lineage / legacy-sources / carryover-register / import-log）

### Changed
- `SKILL.md` 版本升级到 0.8.0；schema 升级到 0.4.0；路由表新增5个阶段衔接场景；规则索引新增第13条；工作区结构新增 continuity/ 目录
- `scripts/init_workspace.py` 初始化时创建 `ai/continuity/` 目录及模板文件

### Upgrade Notes
- **从 0.7.1 升级**：schema 从 0.3.0 升级到 0.4.0（新增 continuity/ 目录）。旧工作区需手动创建 `ai/continuity/` 目录，或重新运行 `init_workspace.py`（已有文件不会被覆盖）。
- **迁移方法**：在现有项目根目录运行初始化脚本，会自动创建 continuity/ 目录和模板文件。

---

## 0.7.1 — 2026-08-09

### Added
- `01-daily-report-rules.md` 新增 §1.3 日报合并幂等性约束：同一人同一天只允许一份日报文件；多次提交必须合并追加，不得覆盖；6种字段分别定义合并策略（追加/更新/覆盖/累加）；合并后必须在更新记录中追加日志
- `01-daily-report-rules.md` 新增 §1.4 日报合并更新记录格式（Time/Action/Items Added/Items Updated/Merged By）
- 个人日报模板新增「更新记录」区块

### Upgrade Notes
- **从 0.7.0 升级**：PATCH 版本，无 schema 变更。直接覆盖即可。

---

## 0.7.0 — 2026-08-09

### Added
- 新增 `assets/templates/personal-progress-template.md`：个人进度汇总模板（当前任务/风险/问题/近期进展/工时投入）
- `01-daily-report-rules.md` 新增 §5 个人进度自动联动规则：日报更新时自动同步任务进度/任务看板/里程碑/风险/问题/近期进展/工时/月度索引；低风险可主动更新个人汇总，高风险需确认
- `06-file-rules.md` 新增 `summaries/` 目录和个人进度汇总文件规则

### Changed
- 目录层级优化：`YYYY/MM` 两级改为 `YYYYMM` 单级（日报/会议/复盘）
- 周报/月报不再按年份建子目录，直接平铺
- `01-daily-report-rules.md` 新增月度索引规则（`YYYYMM/index.md`）和检索优先级（先读索引再读具体日报）
- `06-file-rules.md` 新增月度文件数量阈值规则（>800时建议按日期二级拆分）

### Upgrade Notes
- **从 0.6.0 升级**：无 schema 变更（均为 0.3.0）。目录结构变更属于建议性调整，旧工作区可保留 `YYYY/MM` 结构或迁移到 `YYYYMM`。
- **迁移方法**：将 `reports/daily/personal/2026/08/` 下的文件移动到 `reports/daily/personal/202608/`，删除空的 `2026/` 目录。同理处理 project/meetings/reviews。
- **新增个人进度汇总**：旧工作区可手动创建 `reports/daily/personal/summaries/` 目录，后续日报更新时 AI 会自动生成个人进度文件。

---

## 0.6.0 — 2026-08-09

### Added
- 新增 `references/12-excel-generation-rules.md`：8种文档Excel生成规范，包括sheet结构、精确列头、数据验证下拉框、公式（延期计算/SUM/SUMIF/CPI）、条件格式（风险等级颜色/状态颜色/成本占比预警）、冻结窗格、成本测算表询问式细化（按角色汇总vs按个人明细）

### Changed
- `SKILL.md` 版本号升级到 0.6.0；路由表新增6个Excel生成场景；规则索引新增第12条

### Upgrade Notes
- **从 0.5.0 升级**：无 schema 变更（均为 0.3.0）。直接覆盖 Skill 包即可。旧工作区无需迁移。
- **依赖**：Excel 生成依赖 xlsx 技能（SKILL.md），生成后必须通过 recalc + audit 校验。

---

## 0.5.0 — 2026-08-09

### Added
- 新增 `references/11-output-artifact-rules.md`：输出物管理规则（目录规则、批次目录、草稿/确认/导出流程、文件格式询问、生成物索引、归档到ai/规则、环境兼容）
- 新增 `assets/templates/outputs-index-template.md`：生成物索引模板
- 新增 `assets/templates/output-manifest-template.md`：批次清单模板
- 工作区初始化时生成 `outputs/` 目录及 `outputs/index.md`

### Changed
- `SKILL.md` 新增 outputs/ 目录结构说明、路由表新增6个输出物场景、规则索引新增第11条、description 触发词扩展（生成周报/导出文件等）、front matter 版本号升级到 0.5.0
- schema 版本从 0.2.0 升级到 0.3.0（新增 outputs/ 目录）

### Upgrade Notes
- **从 0.4.0 升级**：schema 从 0.2.0 升级到 0.3.0。旧工作区需要在项目根目录下手动创建 `outputs/` 目录及 `outputs/index.md`，或重新运行 `init_workspace.py`。
- **迁移方法**：在现有项目根目录运行 `python init_workspace.py --mode portfolio --project-root . --sub-projects ...`，脚本会自动创建 outputs/ 目录（已存在的文件不会被覆盖）。
- **不兼容变更**：无。旧工作区的 ai/ 目录结构不变，只是新增了同级 outputs/ 目录。

---

## 0.4.0 — 2026-08-09

### Added
- 新增 `references/10-update-trigger-rules.md`：四级触发机制（L1显式指令→L2文件类型→L3语义信号→L4纯查询）、12种文件类型识别路由表、6类语义信号词典、更新权限分级（auto_write_low_risk）、最小追问规则
- 新增 `assets/templates/project-brief-template.md`：AI 快速入口文件（项目信息+子项目清单+团队+技术栈+文件路由速查表+AI处理前必读声明）
- 新增版本控制体系：`VERSION`、`skill.json`、`CHANGELOG.md`
- `init_workspace.py` 初始化时生成 `ai/.skill-version.json`（记录 Skill 版本 + workspace schema 版本 + 模式 + 时间）
- `init_workspace.py` 初始化时生成 `ai/logs/migration-log.md`（迁移历史记录）

### Changed
- `references/00-pm-main-rules.md` 新增 2.7 默认意图检测：处理任何输入前先判断六类意图（查询/生成/分析/更新/归档/文件解析入库）
- `references/06-file-rules.md` 新增 project-brief 首读规则、更新权限分级（低风险/高风险清单）
- `SKILL.md` description 触发词扩展（评审/会议/文件解析入库等）；路由表新增 7 个场景；规则索引新增第 10 条；front matter 新增 version/schema_version 字段

### Upgrade Notes
- **从 0.3.0 升级**：无 schema 变更（均为 0.2.0），直接覆盖 Skill 包即可。旧工作区无需迁移，AI 会自动读取新规则。
- **需要做的操作**：将新 Skill 包复制到灵犀安装目录替换旧版；在工作区的 `project-brief.md` 中填写项目信息（新初始化的项目会自动生成，旧项目需手动创建）。

---

## 0.3.0 — 2026-08-09

### Added
- 新增项目集模式（portfolio mode）：`ai/portfolio/` + `ai/projects/{子项目}/` 分层管理
- 新增 `references/09-portfolio-rules.md`：项目集总则、汇总周报流程、跨项目风险管理、整体P&L、人员资源管理（字段/流转/8条风险触发规则/联动规则）
- 新增 `assets/templates/portfolio-weekly-template.md`：项目集汇总周报模板
- 新增 `assets/templates/resource-register-template.md`：人员资源当前状态模板（RES-NNN/角色/状态/分配方式/B角/风险等级）
- 新增 `assets/templates/transfer-log-template.md`：人员流转记录模板（RTF-YYYYMMDD-NNN/9种流转类型）
- 新增 `assets/templates/project-index-template.md`：子项目索引模板（PRJ-NNN）

### Changed
- `SKILL.md` 重写为项目集模式（16,802字符）：双模式支持、业务目录不侵入规则、新ID编码（RES-NNN/RTF-YYYYMMDD-NNN/PRJ-NNN）、新状态枚举（资源状态/分配方式/流转类型）
- `references/01-daily-report-rules.md` 新增资源变动检测（6类关键词）、项目集周报分层规则、项目集汇总周报更新片段
- `references/05-query-rules.md` 新增项目集模式查询路由、跨项目对比查询、资源查询处理（5种查询意图）、项目集健康度查询
- `references/06-file-rules.md` 新增业务目录不侵入规则、项目集目录结构定义、资源文件状态与历史分离规则
- `scripts/init_workspace.py` 重写：支持 `--mode portfolio` 和 `--sub-projects` 参数

### Upgrade Notes
- **从 0.2.0 升级**：schema 从 0.1.0 升级到 0.2.0。旧工作区（各子项目下各有 ai/ 目录）需要迁移到集中式结构。
- **迁移方法**：运行 `python init_workspace.py --mode portfolio` 重新初始化，将旧 ai/ 下的文件迁移到新结构的对应位置。详见 `scripts/init_workspace.py` 的迁移说明。
- **不兼容变更**：旧工作区的分布式 ai/ 目录结构（每个子项目下各有 ai/）不再推荐，改为集中式（根目录 ai/ 下统一管理）。

---

## 0.2.0 — 2026-08-09

### Added
- 新增 `assets/templates/lessons-learned-template.md`：经验教训库模板（9字段结构化）
- 新增 `assets/templates/project-context-template.md`：项目背景模板

### Changed
- 根据用户实际项目管理云文档（9份xlsx）重写8个模板：requirement-register/risk-register/issue-register/task-board/weekly-report/project-status/lessons-learned/project-context
- 模板贴合实际管理习惯：优先级用描述性文字（紧急/高/中/低）、风险状态用中文（识别中/监控中/已关闭/已发生）

### Upgrade Notes
- **从 0.1.0 升级**：无 schema 变更（均为 0.1.0）。直接覆盖 Skill 包即可。旧工作区无需迁移。

---

## 0.1.0 — 2026-08-09

### Added
- 初始版本发布
- `SKILL.md` 核心入口：角色定位、工作流、路由表、安全底线、ID编码、状态枚举
- `references/00-pm-main-rules.md` ~ `08-change-control-rules.md`：共9份提示词规则
- `assets/templates/`：11个文档模板（personal-daily/project-daily/weekly-report/meeting/task-board/risk-register/issue-register/milestone-board/requirement-register/change-log/project-status）
- `scripts/init_workspace.py`：单项目模式初始化脚本
