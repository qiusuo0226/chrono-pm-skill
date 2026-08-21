# Changelog

本文件记录 ChronoPM Skill 的版本变更历史。版本号遵循语义化版本（MAJOR.MINOR.PATCH）。v3.0.0 起 ChronoPM-Project 与 ChronoPM-Portfolio 共用同一条版本线。

---

## 3.8.0 — 2026-08-22（本次发布 · released）

> 发布归档：Minor + schema_change + contract_change。人员文件整合、对外确认话术、V-11/V-12、兼容人工成本台账。workspace schema 0.12.0 → 0.13.0。

Blueprint Impact: full

### Added
- `_index.md` §1 花名册（含岗位）+ §6 TD 缩写映射；空目录 `backup/`
- 对外确认专节（白话提问；「请你确认」只=认不认/准不准）
- Portfolio V-11 共享文件拆分、V-12 术语指针索引（glossary-index）
- §0.6 兼容人工成本台账：日合计拷贝追加；分次明细按需；对话检出人工成本可记；能效按日并置
- 回归 Module 57 PC-001~010（合计 390）

### Changed
- resource-register / transfer-log 退役，模板进 `assets/templates/archive/`
- 待办状态删除「待评审」；评审=独立待办；关单 SUGGEST 仅未过评审门
- 禁止提前建未来日待办；创建契机 N-43 if-else 先全员结转
- 结转三时间原样搬运；空闲不自动出组
- 人员查询/聚合改读待办体系

### Notes
- ⚠ 本发布不代迁业务工作区数据、不删 8-23、不搬根级 backup 快照、不灌历史工时表。脚本只建空 backup/ + 升 schema。
- 成本对账由 PM 负责；AI 不编造数字。历史日个人 md 不回写 §0.6。
- `upgrade-plan-v3.8.0.md` 保留供用户检查，确认后再删。

## 3.7.0 — 2026-08-21（released）

> 发布归档：Minor + schema_change + contract_change。三 CR 并轨（H 拆解增强 / I 废 entity-registry / J 风险问题重构）。workspace schema 0.11.0 → 0.12.0。

Blueprint Impact: full

### Added
- WF-SD-1 接收侧对账、WF-SD-2 增量重拆、parse-log、atoms/facts 分片、REQ 自动编号、术语节流、source-split-skill 清单
- WP §3b 实体/功能点行（实体状态唯一载体）；project-context 项目级推导规则
- 风险/问题识别判定卡；登记册索引+条目块（单表 ≤7 列）；D24/D26
- 回归 Module 54/55/56（合计 380）

### Changed
- 3.6.0 一次性迁移改为零清重建（已建 sources/ 保护）
- 00 §10 推导载体改 WP §3b + project-context；删除 entity-registry 模板
- 风险/问题新号 `R-NNN`/`I-NNN`（三格式兼容）；仅高等级强制绑定待办
- SKILL.md §8 ID 表拆分 Risk/Issue vs Decision

### Notes
- ⚠ 不代清零/代迁业务工作区。脚本只打印指引。P9：验证通过 + PM 确认后清 archive 快照。
- 00 号已超 300 行瘦身线，§10 再改，债务记本条。

## 3.6.0 — 2026-08-20（released）

> 发布归档：Minor + schema_change（CR-F）。通用来源文档拆解。workspace schema 0.10.0 → 0.11.0。

Blueprint Impact: full（RI 存储模型 + init/migrate）

### Added
- `requirements/sources/{编号}/` 五件套（meta/_digest/atoms/facts/ledger）+ `_index.md` 台账加速器
- ATOM kind：background / baseline / hardware / spec / term / milestone_fact（非需求类不进 Canonical）
- source-type 全生命周期基线包（按需启用、不预灌）
- D22 需求蔓延巡检（限局部）
- SRC-NNN 项目内短号；共享用簇固定号（含 SUP-/TRN-）

### Changed
- 拆解发生地从 `{type}-source/` 改为 sources/{编号}/；存量一次性迁移 + fallback + 截止条件
- 伴生包 V-8 兼容期双形态只读；去重键不变

### Notes
- ⚠ 不代迁业务工作区。脚本不自动删旧目录。

---

## 3.5.1 — 2026-08-20（已发布 · released）
> 发布归档：Patch。措辞残留修复正式治理（c7d000f 修复 + 基线重建）。workspace schema 不变（0.10.0）。
Blueprint Impact: none（纯措辞，无行为/结构变化）

### Fixed
- project-brief 模板 §4 人员路由统一为本项目 `resources/`（删除 `projects/{子项目}/`、`portfolio/resources/shared-resource-index.md` 存储路径，仅留禁止性说明）
- 14 号自检规则：月度索引 4 处表述改「停维/存量可留」口径（对齐「v3.4.0 停维」）
- outputs-index / output-manifest 模板：清理 portfolio_weekly_report 等枚举残留
- project-notes 模板位置指针、workspace-health 模板停维标注对齐

### Notes
- 业务工作区零迁移、零数据影响；baseline 3.5.0 已重建为全包快照，3.5.1 基线与发布包逐文件一致

---

## 3.5.0 — 2026-08-20（本次发布 · released）

> 发布归档：Minor + schema_change（CR-E）。WP 独立存储。workspace schema 0.9.0 → 0.10.0。编号短号不变。

Blueprint Impact: full（WP 存储模型 + WF-8 + init/migrate）

### Added
- `wps/WP-NNN.md` 独立 WP 文件 + `wps/_index.md`（8 列，查找加速器，非存在性判据）
- 模板 `wp-template.md` / `wp-index-template.md`
- D20 WP 数据一致性巡检；D21 WP 绑定完整性（限局部扫描）
- DF-019 待绑定/待确认提醒简洁化
- WF-8：抽取门禁、未绑定检测、创建溯源、计划回填、写后必检

### Changed
- 计划 §3 改为 4 列引用简表（编号/名称/状态/里程碑）；关联需求只存 WP 文件 §2
- init 预建 `wps/`；migrate 升 schema 0.10.0 并打印一次性抽取入口
- 05 §6.7 / 10 号倒排落点改读 WP 文件

### Notes
- 存量编号零迁移。计划内嵌 WP **一次性抽取**（截止条件：首次周报或新建待办前）。脚本不自动删内嵌表。
- ⚠ 不执行 CR-F。不代迁业务工作区。

---

## 3.4.0 — 2026-08-20（已发布 · released）

> 发布归档：Minor（CR-D）。报告存根范式 + 时间线报。schema 0.9.0。timeline/ 懒建。

Blueprint Impact: full（01/05 报告路由 + 废缓存索引）

### Added
- 时间线报：`reports/timeline/YYYY-MM-DD_YYYY-MM-DD-*.md`，懒建，判重四案
- D23 存根区间巡检（仅当次目录）

### Changed
- 项目日报/周报改为区间汇聚 + 存根；废止 R-3 缓存、每日草稿、§4.1/§4.2 索引（含 R9 Task Sync 预建）
- 月报 = 时间线报自然月特例
- 11/19/20、伴生包 04 对齐

### Notes
- 存量日报/周报即存根。缺 timeline/ 不是 P0。

---

## 3.3.0 — 2026-08-20（已发布 · released）

> 发布归档：Minor（CR-C）。关联待办 + 工作日志 TD Ref + 人员缩写治理。schema 0.9.0。存量零强制迁移。

Blueprint Impact: full（待办数据模型 + WF-Linked + 缩写权威源）

### Added
- §1.3「关联待办」列；WF-Linked（SUGGEST，禁止 AUTO）
- §3 工作日志 `TD Ref` / 待归属
- resource-register「TD 编号治理」小表；05 双键反查；22 进组缩写 ASK
- 伴生包：跨项目人员按中文名归并

### Notes
- 首次 WF-8/进组前完成本项目缩写回填。旧号不重编。业务数据（如储金晶）不进 Skill 包。

---

## 3.2.0 — 2026-08-20（已发布 · released）

> 发布归档：Minor（CR-B，feature）。DF-017 回复溯源 + 加载场景分类 + DF-018 主动识别习惯。workspace schema 保持 0.9.0。存量 pm-profile 零强制迁移。

Blueprint Impact: full（21 号加载模型 + 00 号输出格式）

### Added
- **DF-017**：查询必出「数据来源」（路径+章节）；写入出「已写路径」；禁止罗列扫描过程。落地 00 号 §9.0。P-REPLY。
- **DF-018**：每轮结束主动观察偏好；连续 3 次一致 → pending + 末尾 SUGGEST；每轮最多 1 条。P-ALWAYS。
- **加载场景**：Skill 主表 §5.1a 新列（P-ALWAYS / P-REPLY / P-WF-{N}）。PF 实例可有同名列，缺省 P-ALWAYS。

### Changed
- DF-001~016 按 21 号原文补标；B 复审 P1：DF-007=`P-WF-1+WF-8`，DF-014=`P-WF-2`（结转加载 22 号时同载）。
- 21 号 §2.2 改为按场景应用（规则文件仍前置加载）。
- pm-profile 模板预填 DF-017/018；加载场景列 DF 行填 —。

### Notes
- ⚠ 不执行 CR-C～F。缺 DF-017/018 行按 21 号 2a 补行，不覆盖同义 PF。

---

## 3.1.1 — 2026-08-20（已发布 · released）

> 发布归档：Patch（开发仓三目录重组，infra）。CR-G（CR-20260820-002）。workspace schema 保持 0.9.0。业务工作区零迁移。分发包 zip 内部仍以 `SKILL.md` 为顶层（布局对安装用户不变）；开发仓复制安装改为复制 `ChronoPM-Project/`。

Blueprint Impact: metadata-only（§1 版本 + §11.3 演进表 3.1.1 行；目录树说明随 README）

### Changed
- **开发仓布局**：Project 包文件迁入 `ChronoPM-Project/`；共享治理迁入 `governance-shared/`（baselines / CR / IA / RR / audit / planning / 历史 upgrade）。
- **升级执行文件**：包内 `governance/migrations/` 只留当前 `upgrade-to-3.1.1.md`；49+ 份历史归档 `governance-shared/migrations-history/`（Q16）。
- **伴生包**：补齐 `ChronoPM-Portfolio/governance/migrations/` 指针文件（主包为准）。
- **打包/审计**：`pack.ps1` 放行 `governance/migrations/` 前缀；`pack.py` 以兄弟目录感知 Portfolio，zip 默认写仓库根；`audit_release.py` 双根定位，基线读 `governance-shared/baselines/`，3.1.1+ 要求双子树。
- **基线**：`baselines/3.1.1/ChronoPM-Project/` + `ChronoPM-Portfolio/`。≤3.1.0 冻结快照不改内部布局。

### Notes
- ⚠ 不执行 CR-B～F。不迁移业务工作区。
- 开发仓安装：把 `ChronoPM-Project/` 复制到 AI 工具的 Skill 目录（不要复制整个仓库根）。

---

## 3.1.0 — 2026-08-20（已发布 · released）

> 发布归档：Minor（路径残留纠偏 + 日报查询/更新路由补全 + 月报残留清理，fix）。CR-A（CR-20260820-001）。workspace schema 保持 0.9.0；skill schemaVersion 保持 0.7.0。存量工作区零迁移，重装载规则即生效。施工清单 = AP-4（≠ 方案 §7 整表）。R9（config.py 日报索引 Task Sync 表头）并入 CR-D，本版不执行。

Blueprint Impact: full（AD-06 continuity→context 纠偏 + §11.3 演进表 3.1.0 行）

### Changed
- **日报查询/更新路由**：05 号新增「个人日报/昨天日报风险点→todos/{date}/{owner}.md §2+§3」，禁止先探测 `reports/daily/`；项目日报行补优先级（内容查询先 todos；仅找生成文档才读 `reports/daily/project/`；目录不存在=未生成，不报错）。10 号「本项目日报」拆两行（个人→todos，项目日报存根→reports/daily/project/）。
- **SKILL.md**：§3 `reports/` 注释改为「项目日报按需生成（存根，可能不存在）+周报；个人日报在 todos」；§5.2/5.3 补查询落点。禁止使用「缓存」措辞。
- **file_registry.py**：L237 拆两行映射（禁整行改 todos）；结构树删 `monthly/`，daily 标注「仅项目日报按需生成的存根」；生成工作区 README 文案删「月报」。
- **config.py**：删除 `reports/monthly` 预建与月报索引模板。不改 Task Sync 表头（R9 ∈ CR-D）。
- **文案纠偏**：20 号兼容模式去掉 `tasks/board.md`；13 号纪要行动项 `tasks/`→`todos/`；01 号归档读 `requirements/change-log.md`；06 号删月报路径；19 号完整性检查去月报。
- **模板**：project-brief §7 路由速查整表改单项目路径；outputs-index Related AI File 示例改 `reports/weekly/YYYY/`。
- **README 双语**：月报/项目集月报能力表述清理；CAP-003 改指向伴生包。
- **回归**：OA-005 改「引导切 Portfolio，本包不写 portfolio/」；新增 Module 40 QR-DR-001~003（合计 302）。
- **伴生包**：仅版本锁步到 3.1.0（G-2 / audit 断言 13）；规则零改动。04 号 L35 随 CR-D。

### Notes
- ⚠ 不执行 CR-B～G（DF-017/018、linked todos、存根范式+时间线报、wps/、RI、三目录重组）。
- ⚠ 不迁移业务工作区。存量若残留禁用路径，按 06 号 §12.5 既有机制触发迁移补做。
- 活文档 `governance/upgrade-plan-v3.1.0.md` 待发布验证通过后按 R10 删除。

---

## 3.0.0 — 2026-08-19（已发布 · released）

> 发布归档：Major（双包拆分 + 单项目回归，architecture_change）。ChronoPM-Project 纯单项目录入 + ChronoPM-Portfolio 只读归集。废弃旧 portfolio 作为日常录入口；写归 Project，读归 Portfolio。联邦结构 `ai/portfolio/` + `ai/projects/{名}/ai/`。Portfolio 只读契约五条、能力 V-1～V-10；无 init 脚本（F-10）。旧 09 号项目集规则整文件迁入 Portfolio 包。Init 仅单项目。skill schemaVersion 0.6.0 → 0.7.0；workspace schema 0.8.0 → 0.9.0（联邦挂载协议）。两概念分离，禁止绑死。

Blueprint Impact: full（双包架构 + 09 号迁出 + 联邦挂载 schema）

### Added
- **ChronoPM-Portfolio 包（新建）**：viewer 只读 Skill。跨多个项目 ai 归集检索进度、风险、合同、周报。禁止写入成员项目事实源。references 01～06 + 建议更新清单/集周报/项目索引模板。
- **联邦挂载协议**：成员项目解压到 `projects/{名}/ai/`；动态感知扫描发现候选、登记须确认；防套娃（项目 ai 内禁 portfolio/projects）。

### Changed
- **职责分界**：日常录入只在 ChronoPM-Project 单项目 `ai/`；跨项目归集/检索改用 ChronoPM-Portfolio 对话。
- **初始化**：仅 `--mode single`。无 Portfolio init 脚本；联邦骨架由 AI 按模板创建。

### Removed
- **upgrade-plan-v3.0.0.md 草稿删除（R10，2026-08-19）**：发布验证通过后按 AP 生命周期规则清理（16 号 §19）；实质已固化于 governance/migrations/upgrade-to-3.0.0.md + baselines/3.0.0/ + 本 CHANGELOG 段。同批前置：upgrade-to-2.1.0.md L6 引用修正 + upgrade-plan-v2.1.md 删除（P-20 ①②，已提前执行）。

### 收尾修复补记（2026-08-19，发布后门禁闭环，不另起版本）
- audit_release.py 门禁失败 6 项修复：README×2/skill.json/SKILL.md 版本触点同步；回归统计修正（IR-006 重复登记去重、V3 实测 15/15、合计 299）；SKILL.md §15 规则索引改全文件名。
- audit 扩展：断言 13 双包一致性（Portfolio VERSION/skill.json/viewer/双基线）；Case ID 正则兼容 V3 前缀；门禁 12→13 类。
- is_portfolio 代码级清理：init 侧删 portfolio 分支（create_portfolio/generate_portfolio_readme/PORTFOLIO_* 常量）；migrate_workspace.py 存量兼容分支有意保留（双文件 docstring 互补声明）。
- 契约补全：skill-contract 新增 Schema 版本说明（schemaVersion 0.7.0 / workspace schema 0.9.0，D-24）+ ChronoPM-Portfolio 伴生包契约块（只读五条）。
- 05 号新增 §1.6 登记册编号双格式兼容（R16 查询侧，新旧号同时识别）。
- 第二批收尾（方案关账，G-5 三目录重组除外）：
  - P-13 集层模板剔除：portfolio-weekly-template / 集级 project-index-template 自 Project assets/templates/ 删除（Portfolio 包已有副本），ALL_TEMPLATE_FILES 同步移除，模板总数 35→33（README×2 + BLUEPRINT 触点同步）。
  - P-14 init 残留清理：SUB_PROJECT_DIRS / SUB_PROJECT_FACT_SOURCE_FILES 死代码删除；SUB_PROJECT_INDEX_TEMPLATES 改名 SINGLE_PROJECT_INDEX_TEMPLATES。
  - P-25 ledger 契约落地：07 号新增 §8.9.5 ledger.md 字段规范（source_id/file/source_fingerprint/parsed_by/parsed_at）；contract-register 模板补指针。
  - P-18 文档跟完：BLUEPRINT 能力矩阵 CAP-001/003/010/027 + RI 扩展行去 09/portfolio 旧指向；QODER_RULES 快捷路由改单项目路径。
  - G-3 双包打包：pack.ps1 排除集增 ChronoPM-Portfolio；pack.py 伴生包自动感知，仓库根一次产出两 zip；pack-skill SKILL.md + README×2 命名段同步。
  - P-10 口径正式化：09 号定为「退役迁出 + 保留指针页」（upgrade-to-3.0.0.md），验证清单 15 项收尾回填。
  - 偏差登记：G-5 三目录重组延后（见 upgrade-to-3.0.0.md 偏差记录，建议随下一 Major 执行）。
  - 基线刷新（2026-08-19）：governance/baselines/3.0.0/ 按当前 HEAD 重刷（SKILL.md/CHANGELOG/BLUEPRINT/regression-suite/references 含 09 指针页/Portfolio 子树），逐文件哈希校验与 HEAD 一致；第一批快照过期内容（BLUEPRINT 矩阵旧指向、09 旧描述、SKILL.md §15 缺 09）清除。
  - SKILL_BLUEPRINT.md 规则文件一览 09 行改为退役指针页描述（文档残留修复）。

### Notes
- ⚠ 存量集工作区（如市监）本次不迁移。日后按 `governance/migrations/upgrade-to-3.0.0.md` 原地升级 + 补建自足性最小文件集。
- 双包 version 均为 3.0.0。Project 包 09 号退役，内容在 ChronoPM-Portfolio。

---

## 2.1.0 — 2026-08-18（已发布 · released）

> 发布归档：Minor（个人待办体系与工作区路径整合，capability_change）。双 Agent 审核十三轮收敛（V0.1→V0.42，13 个需求，终审通过-可执行）。核心升级：新增 22 号个人待办规则（§0 六字段录入规范 + T+1 沿用 + 冲突以 resource-register 为准仲裁 + 结转入口 Step 0）；18 号向导 Step 5 新增 §0 引导；04 号 DF-002 PM 确认门禁；09 号人员信息双层数据流微调 + 可用性/排期聚合=动态视图硬约束（实时计算不落盘）；11/12/13/20 号 outputs/→ai/outputs/ 全链路更新；13 号 continuity/→context/ 路径迁移。存量工作区路径整合（continuity/*→context/、根 outputs/→ai/outputs/）与历史报告迁移（§7.3.2b 检测→迁移→验证→删除）由 migrate_workspace.py 新增 migrate_v210_paths/migrate_v210_reports 执行；VERSION_CAPABILITIES 补齐 29 个历史版本缺口；新建升级文件体系 governance/migrations/（版本链 0.1.0→2.1.0 权威执行源，49 个历史版本回填 + 2.1.0 手写）。workspace schema 保持 0.8.0，skill schemaVersion 保持 0.6.0。

Blueprint Impact: full（新增 CAP-027 Personal Todo System + 多 CAP 联动标注 + 升级文件体系）

### Added
- **22 号待办结转规则（references/22-carried-over-rules.md，新建）**：结转触发时机（3 时机）、Step 0 执行流程（HARD BLOCK，创建待办前 MANDATORY 读取前一天 _index.md 全员扫描）、编号硬约束与场景区分、E1~E5 错误处理、状态机与 AI 自检清单。
- **个人待办体系配套规则（承载于既有规则文件）**：§0 人员信息六字段录入规范（岗位/姓名/联系方式/负责模块/进组日期/离组日期，personal-daily-todo-template §0 + 18 号向导 Step 5 引导）、T+1 沿用与冲突仲裁（以 resource-register 为准，00 号 §4d + 09 号 §1.3）、进度↔状态双轨仲裁（01 号 D-26）。
- **升级文件体系（governance/migrations/，需求十一/D-18）**：upgrade-template.md + README.md 总索引（版本链 0.1.0→2.1.0 权威执行源，AI 升级 MANDATORY 逐级执行）；49 个历史版本升级文件按三批次回填（批次 1 P0 ≥ 1.10.2 完整 7 类操作；批次 2 P1 0.8.0~1.10.1；批次 3 P2 <0.8.0 可标"信息不全"）；upgrade-to-2.1.0.md 含完整迁移执行步骤。
- **v2.1.0 专项迁移双函数（migrate_workspace.py）**：migrate_v210_paths（continuity/*→context/ 4 文件含 carryover-register、根 outputs/*→ai/outputs/，不覆盖合并，同名冲突保留源并提示）；migrate_v210_reports（项目日报→reports/daily/project/YYYYMM/、周报→reports/weekly/YYYY/YYYY-Wxx.md 文件级规范化，文件数核对验证，登记 context/import-log.md；个人日报为 AI 内容级迁移，脚本仅检测提示不动源）。
- **VERSION_CAPABILITIES 补齐 29 个历史版本缺口**：0.1.0~2.1.0 全 51 版本条目连续无断点。
- **sync_version.py 扩展（D-19 版本触点架构）**：新增 README.md/README.en.md 标题+版本表、SKILL.md 版本控制表、SKILL_BLUEPRINT.md §1、skill.json blueprint.lastVersion/lastUpdated 共 5 个派生触点同步。

### Removed
- **project-daily-template.md 删除**（方案 §7.3.2/A-9 删除清单）：v1 项目日报模板，项目日报改为按需生成、无独立模板（01 号规则 §2.2）；config.py ALL_TEMPLATE_FILES 同步移除，模板总数 36→35。

### Changed
- **personal-daily-todo-template.md**：核心执行表新增"进度"列（7→8 列，D-24 硬上限）+ 新增 §2 日报存档段（D-25 两步流程：日报原文先逐字存档，再映射加工进 §3 工作日志段）。
- **pm-profile-template.md**：DF-001~DF-006 内置默认偏好预填。
- **daily-todo-binding-template.md**：_index.md 新增 §2 结转追溯标记 + 参与人员表"来源（新建/结转）"列。
- **portfolio-weekly-template.md**：项目集周报联动微调。
- **04 号 §9.1 DF-002 PM 确认门禁**：问题关闭=编号+佐证+关联影响+PM 确认四要素；日报/周报流程后主动批量罗列可关闭候选。
- **09 号**：§1.3 人员信息双层数据流微调（register 唯一事实源，shared-resource-index 指针索引）；§5.4 可用性/排期聚合=动态视图硬约束（实时计算输出，禁止写入 shared-resource-index 或任何索引落盘）。
- **13 号**：continuity/ → context/ 路径迁移；carryover-register.md 保留并随并入 context/（承载跨阶段结转，与 22 号日常待办结转互不干涉）。
- **11/12/20 号**：outputs/ → ai/outputs/ 全链路路径更新；00/01/05/06/21 号联动微调。
- **进度↔状态双轨仲裁（D-26）**：状态列为唯一权威源；状态=已完成⇒进度必须 100%（自动修正）；进度=100% 但状态≠已完成⇒仅输出建议不自动提升（终态需 PM 确认）。

### Notes
- ⚠ 存量工作区升级须执行路径整合与报告迁移：先 `python scripts/migrate_workspace.py --project-root <根> --dry-run` 检测，PM 确认后执行；个人日报内容级迁移（入 todos §3 工作日志段）由 AI 按 upgrade-to-2.1.0.md 步骤 2b 执行，验证通过前禁止删除源文件。
- 规则文件 21→22 份；模板仍 36 个；workspace schema 保持 0.8.0（路径整合为存量迁移，不引入新 schema）；skill schemaVersion 保持 0.6.0。
- 方案经十三轮审核收敛（V0.1→V0.42）；关键决策链：待办 §0 六字段+T+1 沿用、冲突以 register 为准、outputs 归入 ai/、carryover-register 保留澄清、§7.3.2b 检测→迁移→验证→删除四阶段硬约束、动态视图不落盘、升级文件权威源三层信息架构。

---

## 2.0.0 — 2026-08-17（已发布 · released）

> 发布归档：Major（项目集零数据源 + 待办文件唯一事实源体系重构）。⚠ 破坏性架构变更，升级须执行存量数据迁移。双 Agent 审核十轮收敛（V2.0→V2.10，B 终审通过-可执行）。核心升级：解决旧体系"多源双写、数据不一致"顽疾——删除 board/迭代登记册/里程碑板/旧待办索引等旧体系，执行状态唯一事实源切换为 `todos/{date}/{owner}.md` 每人每日待办文件 + `_index.md` 绑定文件；项目集层零数据源（实体下放子项目，项目集只留指针索引）；状态枚举全中文；里程碑并入 WP；PM Profile 增姓名字段。workspace schema 保持 0.8.0，但属破坏性变更，需按 09 号 §5 执行存量数据迁移（旧文件归档 v1-legacy 只读保留）。

Blueprint Impact: full（架构重构）

### Added
- **待办文件唯一事实源（todos/{date}/{owner}.md + _index.md）**：替代旧 board/迭代登记册；PLAN 文件承载计划编排（WP 粗规划表，唯一计划事实源）；WP 进度 = 待办文件按 WP Ref 实时聚合。
- **三个新模板**：plan-template.md（计划文件，含 WP 清单/门禁/资源统筹）、personal-daily-todo-template.md（每人每日待办文件，含 9.1 全字段）、daily-todo-binding-template.md（当日绑定 _index.md，含共享人力软兜底提示）。
- **PM Profile 姓名字段（pm_name，21 号 §2.4）**：用于"我"的身份推导与 TD 编号人名缩写段。

### Changed
- **项目集层零数据源（09 号重写）**：资源/预算/里程碑/风险等实体下放子项目；项目集层只留 shared-resource-index / transfer-index 等只读指针索引；T1/T3 共享人力跨项目排期提示软兜底。
- **状态枚举全中文（00 号 §5a）**：需求/待办/风险/问题/变更/WP 六类状态全部中文化（待处理/进行中/待评审/已完成/已阻塞/已取消/已转出等）。
- **里程碑并入 WP（需求 C）**：里程碑=里程碑型 WP，不再独立枚举。
- **删除 03 号规则 + 16 个废弃模板**；05 号查询路由整体改指待办文件与子项目事实源。
- **迁移脚本适配（config/file_registry/migrate_workspace）**：只做版本/模板/目录补缺；存量数据迁移由 AI/PM 按 09 号 §5 执行。

### Notes
- ⚠ 破坏性架构变更：升级前必须先按方案 11.5 / 09 号 §5 执行存量数据迁移（读取旧 board/索引 → 生成草案 → PM 确认 → 落 todos/{date}/{owner}.md → 下放 portfolio 实体 → 建项目集索引 → 旧文件归档 v1-legacy），否则升级后 AI 按新规则读子项目 todos/ 会找不到存量数据（读取断层）。
- workspace schema 保持 0.8.0（无 schema 版本号变更），但文件结构与数据源发生根本重构。
- 方案经十轮 B 审核收敛（V2.0→V2.10）；关键决策链：待办唯一事实源 → 项目集零数据源（用户最高优先级架构决策）→ 状态中文 → 里程碑=WP → 倒排计划拆分三子项目。

---

## 1.21.0 — 2026-08-16（已发布 · released）

> 发布归档：Minor（倒排每日矩阵查询视图）。⚠ contract_change（00号 WF-7 草案行修改，触发全量回归）。双 Agent 审核三轮收敛（V0.1→V0.3，B1/B2 终审通过-可执行）。核心升级：解决 PM 无法按人按天跟踪倒排进度的痛点——05号 §6.7 新增"倒排每日矩阵"查询视图（人员×日期矩阵，支持 portfolio 多 board 遍历 + 存量降级策略）；00号 WF-7 草案行补充读文件列 + 输出规范（初始草案=WBS 产出/刷新=board 派生/WF-8 闭环）；10号追加查询附带提示（board 变更后建议刷新矩阵）。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；0 新增文件、0 新增模板。

Blueprint Impact: metadata（CAP-005 查询路由增强）

### Added
- **倒排每日矩阵查询视图（05号 §6.7）**：人员×日期矩阵（行=Owner 去重，列=工作日，格=Task 简述）；数据访问支持 portfolio 模式（遍历 project-index 圈定的子项目 board）和 single 模式；两文件读（iteration-register + board），与既有"倒排倒计时"行模式一致；可选角色括注（从 resource-register 查）。
- **降级策略（05号 §6.7）**：无 iteration-register 时按日期窗口过滤；无 WP Ref 时行按 Owner、格按 Task Title，标注"未关联 WP"；存量工作区矩阵仍可生成。
- **倒排草案查询提示（10号 §2 L3）**：PM 查询倒排相关内容时，board 有变更则附带"建议刷新倒排矩阵"提示；不新增独立触发类型。

### Changed
- **WF-7 草案行输出规范（00号 §9）**：读文件列从"—"改为 board + iteration-register；输出新增倒排每日矩阵；区分两阶段数据源（初始草案=WBS 产出，刷新=board 派生）；WF-8 闭环（口述先落库再生成矩阵）。⚠ 核心契约修改，触发 contract_change + 全量回归。

### Notes
- 回归套件新增 Module 38 Backward Scheduling Daily Matrix（BDM-001~010，10 用例，总计 269）；含 contract_change 全量回归声明。
- 零新增规则文件、零新增模板、零 schema 变更；workspace schema 保持 0.8.0。
- 方案经三轮 B 审核收敛：V0.1→V0.3；关键决策链：数据源多 board 遍历（非单文件）、存量降级策略、初始草案/刷新区分两数据源、contract_change 确认触发、C-03 保鲜降级为查询附带提示。

---

## 1.20.0 — 2026-08-15（已发布 · released）

> 发布归档：Minor（需求双视图与开发文档关联）。双 Agent 审核四轮收敛（V0.1→V0.4，B1/B2 终审放行）。核心升级：解决"合同需求（业务视角）⇄ 开发需求（实现视角）"语义断层——业务视图为 business 类 ATOM norm_text 派生聚合（不新增字段），实现视图与原型/文档链接为 REQ 层新增可选列；WF-2 日报处理按 Task→REQ 链路加载需求上下文，使 AI 能同时理解日报中的业务语言与实现语言。technical 类 ATOM 硬约束排除出 scope_scope 聚合（数据正确性红线）。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；新增字段均为可选，存量工作区向后兼容。

Blueprint Impact: full（WF-2 数据路径 + 双视图能力 + 版本演进表）

### Added
- **需求双视图机制（07 号 §8.10）**：view_business = business 类（contractual/procurement/approval/compliance/operational）ATOM norm_text 派生聚合，查时现算不新增字段；view_dev = 登记册"实现视图"列（摘要级 ≤100 字，挂 REQ 层与 Task→REQ 日报链路对齐）；"原型/文档链接"列存指针，原文档不入库。
- **开发侧 source_type 扩展（source-type-registry）**：dev_prd / design_doc / api_spec / prototype / ui_spec 五个 technical 类类型（authority L3）；design_doc（开发侧）与 design_spec（甲方侧）语义边界显式区分。
- **WF-2 需求上下文加载（00 号/05 号）**：Task 带 Requirement Ref 时读对应 REQ 的功能描述+实现视图+原型链接；单次最多 10 条 REQ，字段缺失降级不阻塞（05 号 §2.5 需求上下文加载规范）。
- **Quick Query 需求详情路由（05 号）**："某需求具体做什么/怎么实现/原型在哪"走 requirement-register，与既有范围判定路由（contract-register）显式区分。
- **词库开发侧支持（17 号）**：类别自由文本补充"模块名/接口名/技术组件"标签示例（§3.1）；分类预筛 + 懒加载性能策略（§5.1a，复用 §12.2 拆分不新增索引）；开发侧术语归一规则（§6.3a）。
- **日报模板可选段**：个人日报/项目日报新增"关联原型/文档（可选）"节，原文档不入库仅记指针。
- **Excel 扩展列 U/V（12 号 §1.3）**：实现视图 + 原型/文档链接，与既有 O-T 扩展列连续。

### Changed
- **07 号 §8.5 scope_scope 聚合排除硬约束**：判定仅由五类 business ATOM evidence 参与，technical 类 ATOM 不参与范围判定，仅填充 REQ 实现视图/原型链接；§8.7 级联新增对应 CHECK 红线。
- **07 号 §8.6 提取流程扩展**：新增触发 D（开发侧文档提取）；technical 类 ATOM 按模块/接口/页面维度原子化切块，norm_text 保留技术术语原样；命中 Canonical 时 SUGGEST 填充实现视图；新增大文档渐进导入（分批 2000-5000 字，source_ref 到章节号支持断点续导）。
- **19 号双视图巡检（存在性校验非强制必填）**：confirmed REQ 的实现视图/原型链接覆盖率作 P3 提示；已填 Requirement Ref 的 Task 校验 REQ 存在性（P2）；Requirement Ref 为可选字段不得变相强制。

### Notes
- 回归套件新增 Module 37 Dual View（DV-001~010，10 用例，总计 259）；DV-001（dev_prd 不污染 scope_scope）为数据正确性红线用例。
- 零新增规则文件；requirement-register 新增 2 个可选列（总览表 23→25 列），旧数据无此列不影响既有功能；workspace schema 保持 0.8.0。
- 方案经四轮 B 审核收敛：V0.1→V0.4；关键决策链：双视图挂 REQ 层（非 Canonical）、view_business 派生不加字段、technical 隔离红线、12 号扩展列方案 α（追加 U/V）。

---

## 1.19.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（迁移脚本参考模板库同步缺口 + 健康检查模板检测盲区修复）。双 Agent 审核收敛（V0.1→V0.2，B 复核通过-待修订）。核心升级：修复 `migrate_workspace.py` 从不把 Skill 包模板同步到 `ai/templates/` 参考库、且规则 20 健康检查不检测模板缺失的双层缺口——从旧版本升级或版本号已对齐但模板缺失的工作区（真实痛点场景）会永久缺失新增模板。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；但对已有工作区建议跑一次 `migrate_workspace.py` 补齐参考模板库。

Blueprint Impact: metadata-only

### Added
- **`sync_templates()` 无条件前置（migrate_workspace.py）**：置于版本检查之前、`ai_dir` 存在检查之后，复用 `ALL_TEMPLATE_FILES` 单一事实源，只补不覆盖（保护用户自定义内容）；`--dry-run` 也能报告模板缺失。同时补齐 `outputs/.templates/manifest-template.md`（复用 `create_outputs_dir`，已有 `outputs/index.md` 不被覆盖）。
- **规则 20 §2 第 3b 条 模板完整性检查**：健康检查新增 `ai/templates/` 参考模板库完整性核对（对照 `ALL_TEMPLATE_FILES`）+ `outputs/.templates/manifest-template.md` 存在性，缺失则列入健康报告并建议迁移补齐。

### Changed
- **config.py `ALL_TEMPLATE_FILES` 39→42**：新增 `decision-log-template.md`、`project-notes-template.md`（AI 运行时格式参考副本）、`source-type-registry-template.md`（已实例化事实源，按全量副本库口径纳入）。

### Notes
- 修复 V0.1 阻塞问题：`sync_templates()` 调用点原设计在“创建缺失文件之后”会被“版本已匹配/无缺失”两个提前 return 跳过，导致真实痛点场景下修复失效；已提升为无条件前置步骤。
- 端到端实测双场景通过：版本已对齐 1.19.0 但模板缺失（dry-run 报告 40 缺失 + 真实迁移补齐 42 个且已有模板不被覆盖）；旧版本 1.10.0 升级（补齐 42 模板 + 34 能力文件 + 自定义 outputs/index.md 不被覆盖）。
- 遗留待办（非本次）：`decisions/decision-log.md` 实例化仍用 `change-log-template.md`，如需独立格式另行调整映射。

---

## 1.19.0 — 2026-08-15（已发布 · released）

> 发布归档：Minor（倒排计划能力 + 待办统一归属路由）。双 Agent 审核六版收敛（V0.1→V0.6，五轮 B 审核，B1/B2 五审均 A 级放行）。核心升级：引入 WP（工作包）概念与倒排编排（WF-7），任务创建五入口（口述/日报明日计划/纪要行动项/需求拆解/变更批准）统一 WF-8 归属路由，§8.1 流程反转（正式任务强制落 board），从架构上根治待办↔看板数据不一致。无 workspace schema 变更（仍 0.8.0），无需工作区迁移。

Blueprint Impact: full（§5.2 WF 注释 WF-1~WF-8 + CAP 扩展条目 + 版本演进表）

### Added
- **倒排计划编排 WF-7（00号 §9）**：倒排 = 迭代计划的编排方式，不另立体系；澄清→查重→反向 WBS（关键路径+缓冲）→草案确认→落 iteration-register WP 表 + board Task→级联→验证。§2.7 新增意图；10号新增倒排计划信号。
- **待办创建与归属排布 WF-8（00号 §9）**：所有任务创建入口的统一前置规则；归属判定三步链（预筛候选 WP→高置信语义匹配→WP/独立/一次性提醒三分），置信度不足必须追问不得静默落库；兜底句覆盖直接看板建任务等边缘入口。§2.7 新增意图；10号新增待办归属信号。
- **迭代登记册 WP 粗规划表（iteration-register-template）**：每迭代段新增工作包规划表（WP ID/Title/Owner/Start/End/Req Ref/Milestone Ref/Deliverable/Status/Depends On）+ 倒排元数据（目标/锚点日期/关键路径/缓冲）+ WP 说明段。
- **board 新增 WP Ref 字段（03号 §1）**：Task 的 Requirement Ref（需求溯源）与 WP Ref（执行归属）并存不冲突。
- **WP 进度与分层视图（03号 §8.0）**：WP 进度 = board 按 WP Ref 实时聚合（派生，不建进度索引文件）；日/周计划 = board 按 Due Date 时间切片（无可写载体）。
- **WP 分层查询与倒排倒计时路由（05号 §6.7）**：6 种查询场景 + 不建进度索引的性能约束。
- **自查 D15/D16（14号）**：todo 索引正式条目 vs board 一致性（存量工作区升级后首次自查批量对齐）+ 孤儿半写检测。
- **快照与日计划职责边界（15号 §1 第2b条）**：快照 = 冻结历史记录，日计划 = board 切片，并行不悖，快照机制不变。

### Changed
- **03号 §8.1 流程反转**：“先写索引→SUGGEST board”改为“[MANDATORY] WF-8 归属判定→正式任务强制落 board→[AUTO] 派生索引”，禁止只写索引不落 board（一次性提醒除外）。
- **WF-1 步骤 18.5 拆分（00号）**：待办状态更新走 §8.1 级联；待办创建统一路由 WF-8。
- **五入口条款对齐**：01号 §5.6b 日报明日计划（MANDATORY 落 board）、02号 §2/§3 纪要正式行动项（MANDATORY）、07号 §3.2 需求拆解 Task（已映射迭代 WP 直接继承 Ref）、08号 §6.1 步骤3 变更批准后新增任务。
- **03号 §8 级联扩展**：新增 WP 存在校验、Task done→WP 进度聚合→SUGGEST WP completed、Due Date 超 WP End 检查三级联。
- **00号 §5a 新增 WP 状态枚举**：planned → in_progress → completed。
- **06号拆分注释**：board 拆分保留 WP Ref 跨分片过滤；迭代登记册新增拆分规则。
- **SKILL.md**：desc 触发词（倒排/给XX加待办）；§1 计划体系单一数据源声明；§4 事实源表补 iteration-register；§6 路由表新增 3 行。

### Notes
- 回归套件新增 Module 36 Backward Scheduling & Unified Intake（BS-001~024，24 用例，总计 249）。
- 零新增规则文件/模板文件/workspace schema；事实源层唯一新增字段 WP Ref（可选，旧工作区无此字段不影响既有功能）。
- 存量对齐：升级后首次自查由 D15 驱动，把既有 todo 索引中的正式任务批量补落 board 并归属，避免零散噪音。
- 方案经五轮 B 审核收敛：入口穷举从三入口修正为五入口（07号需求拆解、08号变更批准为 B2 五审发现），教训：入口穷举必须实测核验。

---

## 1.18.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（打包命名标准化）。双 Agent 审核收敛（A 命名漂移诊断 → B 审核发现改错对象 → V3 修正为 pack.py 主路径 + 排除模型单一事实源）。核心升级：新增 Python 打包入口 pack.py，产物统一为 `{BrandName}-Skill-v{version}.zip`；排除模型实读 pack.ps1（唯一事实源）；audit_release.py 新增“命名漂移守门”断言；修复 v1.18.0 版本失步（blueprint.lastVersion / SKILL_BLUEPRINT 当前版本）+ 补 baselines/1.18.1 基线。无规则/模板/能力变更，无 workspace schema 变更，无需工作区迁移。

Blueprint Impact: metadata-only

### Added
- **pack.py 本机主打包入口**：`tools/pack-skill/scripts/pack.py`，产物命名 `{BrandName}-Skill-v{version}.zip`，排除模型实读 pack.ps1 四组数组（单一事实源），无 displayName 时拒绝打包。

### Changed
- **pack.ps1**：新增 displayName 品牌提取（按 `—`/`(` 切）+ 无 displayName 拒绝打包 + 头部标注“跨平台参考实现”。
- **audit_release.py**：新增断言 11“命名漂移守门”（仓库根禁止 `{name}-{version}.zip` 类产物）。
- **SKILL.md / tools/pack-skill/SKILL.md**：补充 Python 主路径与产物命名规范。
- **README.md / README.en.md**：新增“分发包命名规范”说明，版本号同步 1.18.1。
- **版本触点修正**：skill.json blueprint.lastVersion、SKILL_BLUEPRINT 当前版本与演进表同步 1.18.1。

### Notes
- 新增 `governance/baselines/1.18.1/` 基线快照。

---

## 1.18.0 — 2026-08-15（本次发布 · released）

> 发布归档：Minor（推导能力升级）。双 Agent 四轮审核收敛（A V0.1→V1.0，B1+B2 独立审核）。核心升级：引入推导基线（Reasoning Baseline）机制，新增 00号 §10 推导规则（生命周期推导链 + 跨源矛盾处理 + 推导后动作规范 + 任务集 4 级降级关联），新增 entity-registry 数据模板，05号 §3(3)a 终态事件豁免，周报/日报推导增强，脚本层同步。无 workspace schema 变更，无需工作区迁移。

Blueprint Impact: metadata-only（CAP 扩展条目 + 版本演进表行，无结构性变更）

### Added
- **推导基线规则（00号新增 §10）**：§10.1 推导基线定义（派生投影优先级）+ §10.2 跨源矛盾处理（里程碑终态事件豁免）+ §10.3 生命周期推导链（6 步通用推导链 + 项目覆盖机制）+ §10.4 推导后动作规范（SUGGEST + §8a 强制呈现 + 推导链路可追溯）+ §10.5 推导→任务集关联（4 级降级识别 + 作用域隔离）。
- **终态事件豁免（05号新增 §3(3)a）**：过程记录含里程碑终态事件时豁免"以事实源为准"规则，推导结论通过 SUGGEST 建议同步，不直接修改事实源。
- **日报/周报推导增强（01号）**：§6.2 集成审查新增"里程碑事件 vs 任务板状态"维度；§3.3 追加第 5/6 条（实体枚举校验 + 状态推导标注）。
- **任务板推导级联（03号新增 §8.2）**：Task 生命周期推导触发，复用 §8 级联传播机制。
- **自查清单新增 D14（14号）**：推导基线 entity-registry 完整性检查。
- **完整性巡检新增推导基线维度（19号 §3.3a）**：4 项检查（存在性/覆盖度/关联任务填充/状态一致性）。
- **初始化向导可选步骤（18号 §7a）**：多模块/多阶段项目引导创建 entity-registry。
- **entity-registry 数据模板**：新增 `assets/templates/entity-registry-template.md`（实体清单 + 项目级推导链覆盖 + 终态事件扩展 + 更新规则 + 回填触发）。
- **周报模板推导输出段**：`weekly-report-template.md` + `portfolio-weekly-template.md` 新增"状态推导说明"输出段。
- **project-context 推导基线引用**：`project-context-template.md` 末尾新增推导基线引用段。

### Changed
- **脚本层同步**：`config.py` ALL_TEMPLATE_FILES 追加 entity-registry-template.md；`migrate_workspace.py` template_map 追加 entity-registry 映射；`file_registry.py` 目录树追加 entity-registry.md 注释。
- **SKILL.md**：路由表新增"状态推导/跨源校验/生命周期推导"行；§15 规则索引更新 00/01/03/05/14/18/19 号描述；front matter version 同步。
- **SKILL_BLUEPRINT.md**：CAP 扩展条目（Reasoning Baseline）+ 版本演进表 1.18.0 行。

### Notes
- 00号属核心契约层，已标注 contract_change + 全量回归。
- 00号新增后约 ~541 行，已超 06号 >300 行瘦身参考阈值，列入后续版本瘦身候选（可评估独立为 22 号）。
- entity-registry 是事实源的派生投影，非独立事实源；统计表自动推导不得手工维护。
- W33 周报数据修复与本次 Skill 升级解耦，待单独确认执行。

---

## 1.17.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（治理一致性修复）。双 Agent 审核驱动（A 方案 V0.2 经两轮 B 独立复核通过）：修复分发包内幽灵引用、版本/文档失步，补齐治理产物断档，新增发布前自动断言脚本。无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。

### Fixed
- **分发包幽灵引用根治（SKILL.md）**：§6 路由表移除“Skill 变更治理 | 00 + 16”行——16 号规则被 pack.ps1 排除在分发包外，该行对分发包用户构成幽灵引用（落实 1.16.2“移除 16 号路由条目”的未除净部分；实测 references/ 其余 21 个运行时文件无任何 16 号引用，修复点唯一）。
- **版本失步修正**：SKILL.md 版本控制表“当前 1.16.0”→当前版本；skill.json `blueprint.lastVersion` 1.16.1→当前版本；SKILL_BLUEPRINT.md §1 当前版本 1.16.3→当前版本。
- **SKILL_BLUEPRINT.md §11.3 演进表**：补 1.17.0/1.17.1 行；修正 1.16.2/1.16.3 行序倒置。
- **README.md / README.en.md**：回归用例数 185→225（中英共 6 处）；目录树移除 workspace-template 注释（该目录 git 未追踪、无任何脚本引用），改为“ai/ 目录树由 init 脚本程序化创建”说明。

### Added
- **回归套件 Module 35 PM Preference Generalization（IR-001~010，10 用例，总计 215→225）**：补 v1.17.0 五个能力模块（日报集成审查/主动提问、跨实体联动、关闭佐证、委派跟踪、沟通质量规则 + 查询默认过滤）的对应用例，消除发布口径缺口。
- **governance/scripts/audit_release.py**：发布前自动断言脚本（11 条机器可判检查），覆盖版本四触点/blueprint 元数据/BLUEPRINT 版本/README 用例数/回归套件自洽/§15 索引覆盖/仓库内幽灵引用/分发包保留集幽灵引用（实读 pack.ps1 四类排除模型）/基线存在性/README 目录树真实性；任一失败退出码非零，接入 release-checklist，跑不过禁发。落位 governance/（分发包排除目录，不进包）。
- **基线补档**：自 git tag 重建 `governance/baselines/1.16.2/`、`1.16.3/`、`1.17.0/`；新建 `1.17.1/`；登记 1.16.1 缺档原因（无 v1.16.1 tag，无法精确重建）。
- **governance/regression-reports/rr-20260815-1.17.1.md**：本次发布回归报告。

### Changed
- **release-checklist.md**：新增“发布前自动断言”检查项，引用 `python governance/scripts/audit_release.py`。

### Notes
- 版本记录口径说明：1.16.3 之前合入的 README 补全类 commit 未在该版 CHANGELOG 中单独声明，本次不追溯改写历史条目。
- 无 workspace schema 变更，无模板/脚本（运行时）变更，无需工作区迁移。
- 本地 `assets/workspace-template/` 空目录（git 未追踪、无引用）可由用户自行删除，不影响任何功能。

---

## 1.17.0 — 2026-08-14（已发布 · released）

> 发布归档：Minor（PM 偏好通用化升级）。将 12 条 PM 偏好中 10 条高通用性偏好升级为 Skill 通用能力，归并为 5 个能力模块 + 1 可选增强。沟通风格类偏好（CQ-1 通俗表达 / CQ-2 完整引用 / CQ-3 操作建议三要素）回归 PM Profile 个性化层，不固化为 Skill 通用规则。无 workspace schema 变更，无模板/脚本变更，无需工作区迁移。

### Added
- **日报集成审查模式（01号新增 §6）**：日报处理后自动对比计划 vs 完成、风险/问题变化、任务进度偏差三个维度，输出集成审查表。
- **主动提问规则（01号新增 §7）**：集成审查后从阻塞解除、风险应对、关键任务遗漏、明日计划可行性四个角度主动提问。
- **沟通质量规则（00号新增 §5.1a）**：CQ-4 待确认事项必须编号罗列（便于对话引用）；CQ-5 实读禁缓存（查询必须基于本轮实际读取的文件内容）。
- **关闭确认佐证强制要求（04号新增 §9.1）**：关闭建议必须显式列出候选编号 + 佐证 + 关联影响，禁止无佐证输出关闭建议。
- **查询默认过滤（05号新增 §2.0a）**：任务/待办类查询默认仅输出未完成项，用户明确说"全部"时输出全部。

### Changed
- **跨实体联动同步（01号 §5.3）**：联动表新增"需求登记册同步"行——日报进展与 Requirement 状态不一致时建议同步。
- **Task 状态变更需求一致性检查（03号 §8）**：新增 Task 状态变更 → [CHECK] 验证关联需求状态一致性 + [SUGGEST] 不一致时建议同步。
- **委派跟踪级联（03号 §8）**：新增 Task Owner 委派 → [CHECK] 被委派方身份 + [SUGGEST] 为委派方生成跟进待办。
- **WF-1 工作流增强（00号）**：新增步骤 4.5（需求状态检查）+ 步骤 18.6（委派跟踪级联）。
- **SKILL.md**：description 追加新能力关键词；§15 规则索引更新 00/01/03/04/05 文件描述。

### Notes
- 无 workspace schema 变更，无模板/脚本变更，无需工作区迁移。
- 若项目工作区已部署 ai/prompts/ 副本，需同步 references/ 下 00/01/03/04/05 五个文件的改动。

---

## 1.16.3 — 2026-08-14（已发布 · released）

> 发布归档：Patch（级联强制执行修复）。修复级联传播规则被 AI 选择性执行导致待办↔看板↔风险↔问题之间数据不一致。根因有二：(1) SUGGEST 语义被弱化为"可选建议"，AI 可跳过级联动作；(2) 体系缺失"待办→board"反向链路——personal-todo-index 是完全派生索引，新增待办只写索引、不落看板。无 workspace schema 变更。

### Fixed
- **级联强制执行（00号新增 §8a）**：明确 SUGGEST ≠ 可选，而是"必须呈现给 PM 确认"；定义输出前级联完成验证流程（§8a.2）与用户跳过留痕（§8a.3）。
- **待办→board 反向链路（03号新增 §8.1）**：此前仅 board→待办索引单向同步（board 为事实源、待办为派生索引），新增待办不落看板。现新增待办创建级联：CHECK 是否已有对应任务 + SUGGEST 区分正式任务/一次性提醒（正式建议建 Task、一次性不建但呈现判断）+ 待办 done 时检查 board 任务状态。
- **WF-2/WF-5 补验证**：00号 WF-1 新增步骤 18.5（待办→board 级联引导）；WF-2 日报处理、WF-5 周报生成补上此前缺失的级联完成验证行（此前仅 WF-1/3/4/6 有）。

### Changed
- **各实体规则文件（02/03/04/07/08/09）**：级联传播规则处新增"强制执行要求"注释，禁止静默跳过 AUTO/CHECK/SUGGEST。
- **10号更新流程**：新增步骤 8（级联传播执行）、10（Suggested File Updates 含全部级联 SUGGEST）、11（级联完成验证）；待办信号触发追加 §8.1 级联检查引用。
- **14号 §2.5**：改为引用式（以 00号 §8a.2 为唯一权威定义，消除跨文件重复），并限定仅写入场景触发、纯查询（Level 4）不触发。

### Notes
- 无 workspace schema 变更，无模板/脚本变更，无需工作区迁移。
- 若项目工作区已部署 ai/prompts/ 副本，需同步 references/ 下 00/03/10/14 四个文件的改动。

---

## 1.16.2 — 2026-08-14（已发布 · released）

> 发布归档：Patch（分发包幽灵引用修复）。修复 v1.16.1 分发包中 governance/ 整目录排除导致的核心契约断链：例外放行 `governance/contracts/skill-contract.md`（被 7 个运行时规则引用第 5 条）；排除 `SKILL_BLUEPRINT.md`（仅文档层引用）；移除 SKILL.md 中 16 号规则路由；skill-contract.md 基线规则加注“仅开发者仓库”；skill.json 移除 `blueprint.file` 字段。无 workspace schema 变更，无规则/模板/能力变更。

### Fixed
- **pack.ps1**：governance 排除细化——例外放行 `governance/contracts/skill-contract.md`（核心契约）；修复 Windows 路径分隔符匹配（`\` → `/` 归一化后再比对例外清单）。
- **幽灵引用消除**：排除 `SKILL_BLUEPRINT.md`（被 references/16 号和 BLUEPRINT 自身引用的 governance 路径不再进入发行包）；SKILL.md 移除 16 号规则路由条目。

### Changed
- **skill-contract.md**：L94 基线规则加注“仅适用于完整开发仓库，分发包不含 baselines/tests”。
- **skill.json**：移除 `blueprint.file` 字段（BLUEPRINT 不在发行包内，保持元数据自洽）。
- **release-checklist**：Distribution Packaging 段更新排除清单（标注例外放行）+ 新增幽灵引用检查项。
- **pack-skill/SKILL.md**：排除清单说明同步更新。

### Notes
- 无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。
- 包体新增 `governance/contracts/skill-contract.md`（~5.5 KB），移除 `SKILL_BLUEPRINT.md`（~15 KB）和 `references/16-skill-governance-rules.md`（~8 KB），净体积略降。

---

## 1.16.1 — 2026-08-14（已发布 · released）

> 发布归档：Patch（分发包标准化）。新增通用打包 skill（tools/pack-skill/），支持任意 Qoder Skill 项目一键打包分发包 zip；release-checklist 新增 Distribution Packaging 段；.gitignore 补强排除项；删除旧专用脚本 scripts/pack_dist.ps1。无 workspace schema 变更，无规则/模板/能力变更。

### Added
- **tools/pack-skill/**：通用 Skill 分发包打包 skill（SKILL.md + scripts/pack.ps1）。策略“包含全部，排除已知”（黑名单模式），不预设任何 Skill 特有目录结构。默认排除 governance/、tests/、tools/、.git/、.idea/、.qoder/、__pycache__/ 等开发者产物。支持 -DryRun 预览、-Exclude 自定义排除。
- **release-checklist Distribution Packaging 段**：打包命令、排除清单、升级路径验证检查项。

### Changed
- **.gitignore**：补强 `*.zip`、`*.tar.gz`、`.vscode/` 排除项。
- **scripts/pack_dist.ps1**：已删除，被通用版 tools/pack-skill/scripts/pack.ps1 取代。

### Notes
- 无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。
- 分发包体积从 ~4 MB（含 governance）降至 ~270 KB。

---

## 1.16.0 — 2026-08-13（已发布 · released）

> 发布归档：Minor（合同作用域与多对多映射）。在 v1.15.0 跨源需求归集 RI 之上补齐"合同与子项目多对多"缺口（capability_change + schema_change + contract_change）。workspace schema 0.7.0→0.8.0（structure-only 迁移，新增 portfolio/requirements 与 contract-register）。

### Added
- **contract-register.md 合同登记册**（RI 检索入口事实源）：项目集模式唯一在 `portfolio/requirements/`，单项目在 `requirements/`；字段含 scope_level（portfolio/project/supplement）、parent_contract_id（补充协议必填，D7）、coverage 覆盖对象、关联招投标/立项/密评（文档簇）、status/superseded_by（合同血缘）。
- **项目集级 portfolio/requirements/**：canonical + atoms + 三级索引 + source-type-registry。
- **合同变更三级联动**：合同拆分为两份（旧条 superseded_by 血缘）、范围扩大/补充协议（增量 ATOM(supplement) + scope 重判）、范围缩小（ATOM stale + not_in_scope 重判）；复用 08 号既有 `scope`/`cost`/`requirement` 类型，不改 08 号概念域 B 枚举（D8）。
- **回归套件 Module 34 Contract Scope**（CS-001~017）：覆盖多对多、supplement 跟随父合同、空登记册补录引导（negative）、迁移遍历、合同变更联动、CR-001 遗留修复验证。

### Changed
- **07 号新增 §8.9 合同作用域**：contract-register 结构、ATOM/Canonical 按 scope_level 存储归属（supplement 跟随父合同）、Canonical 跨层归 portfolio（storage_level）、contract_refs 伴随字段（scope_scope 5 值枚举不变）、检索路由、合同变更联动。
- **05 号 RI 路由扩展为四步**：Step0 读 contract-register（空则触发补录）→ Step1 解析合同指向（supplement 经 parent_contract_id 回溯父合同层级）→ Step2 目标层级三级索引 → Step3 输出 scope_scope + contract_refs + 证据链。
- **06 号**：目录树/事实源清单补 portfolio/requirements 与 contract-register（两级）；**09 号**：项目集级职责补跨项目合同/招投标/立项范围登记；**00 号**：意图检测补"合同登记/合同变更"；**18 号**：初始化向导 Step1 多合同循环登记；**14 号**：自查补登记册完整性。
- **契约**：skill.json current schema→0.8.0 + migrations（0.7.0→0.8.0）+ versionHistory；SKILL.md §4 事实源表/§6 RI 路由/§8 CON- 前缀/description 触发词更新；SKILL_BLUEPRINT 合同作用域数据流；skill-contract 事实源/能力扩展。
- **脚本**：_version.py →1.16.0/0.8.0；config.py 修复 P1-P3（PORTFOLIO_DIRS/FACT 加 requirements 与 contract-register、SUB_PROJECT 补 RI 目录与 source-type-registry、ALL_TEMPLATE 补新模板）；file_registry.py create_ri_skeleton 参数化 + create_contract_register + README 补齐；migrate_workspace.py 新增 sub_project_dirs/sub_project_files 键 + 子项目遍历（D10 守卫），修复 CR-20260813-001 遗留的项目集 RI 迁移缺口。
- **模板**：新增 contract-register-template.md；index-formats 补 contract_refs/storage_level/parent_contract_id 列格式。

### Tests
- 回归套件新增 Module 34 Contract Scope（CS-001~017），RI-012 复核（contract_refs 同步）；总计 198→215 用例（198 既有 + 17 新增）。

---

## 1.15.0 — 2026-08-13（已发布 · released）

> 发布归档：Minor（跨源需求归集与判定 RI）。新增"需求在不在合同/招投标/立项范围内"的取证与归集能力（capability_change + schema_change）。workspace schema 0.6.0→0.7.0（结构变更，需迁移）。

### Added
- **07 号新增跨源需求归集章节**：ATOM（证据层）→ Canonical（归并层）→ REQ（管理层）三层数据模型；ATOM schema（kind/source_type/authority/raw_text≤500字/supersedes/norm_text）；Canonical 归并 + evidence 证据链 + scope_scope 范围判定 + evidence_stale。
- **双层来源分类**：source_category 固定 6 类（contractual/procurement/approval/compliance/technical/operational）+ source_type 项目级可扩展（source-type-registry.md）。
- **kind 四类型**（需求/要求/约定/约束）统一链路拆解；密评 compliance 强制门禁；里程碑复用 milestone-board 并新增合规门禁列。
- **三级索引**（L1 路由 / L2 类别倒排含 norm_text 覆盖索引 / L3 全文）+ 分级加载（单次范围判定 ≤400 行，对齐 05 号最小读取）+ P1 语义兜底（词库同义词扩展 / norm_text 扫读 / 降级提示）。
- **PM 随笔 project-notes**：AI 主动感知 + PM 主动要求双入口，只追加时间线。

### Changed
- **17 号**：术语级 vs 句子级归一边界（§6.4）；**05 号**：跨源范围判定查询路由 + 分级加载对齐；**00 号**：RI 意图 + 备忘建议输出点；**06 号**：canonical/atoms(L1/L2/L3)/source-type-registry 目录与归档、拆分阈值适配。
- **模板**：register 新增 Canonical ID + scope_scope 列；milestone-board 新增合规门禁列；index-formats 新增三级索引/Canonical/source-type-registry 格式；glossary 补密评/等保词条；新增 source-type-registry-template、project-notes-template。
- **契约**：skill.json current schema→0.7.0 + migrations + versionHistory；SKILL.md 路由新增 RI 行；SKILL_BLUEPRINT 新增 RI 数据流；skill-contract 事实源/能力更新。
- **scripts**：_version.py →0.7.0；migrate_workspace.py 新增 0.7.0 迁移（单项目/项目集）；chronopm_init/config.py + file_registry.py 初始化新目录。

### Tests
- 回归套件新增 Module 32 Requirement Intelligence（RI-001~006）+ Module 33 Project Notes（PN-001~002），总计 184→192 用例。

---

## 1.14.0 — 2026-08-12（本次发布 · released）

> 发布归档：Minor（标准工作流数据路径性能优化）。在不弱化任何现有能力（CAP-001~026 全保留）的前提下，为高频操作场景预定义端到端读/写文件路径，减少 AI 逐步临时推导；判断性推导（状态判定、匹配逻辑、关闭条件）完整保留于判断阶段。无 workspace schema 变更（保持 0.6.0，无迁移）。

### Added
- **00 号 §9 标准工作流数据路径**：新增 WF-1 待办状态更新（18 步定位→判断→写入→补全→输出）、WF-2 日报处理、WF-3 会议纪要处理、WF-4 需求变更处理、WF-5 周报生成、WF-6 人员资源流转，集中声明跨实体端到端读/写文件顺序。
- **00 号 §9.1 判断阶段强化规则**：5 条规则明确待办匹配、状态判定、问题/风险关闭判定、日报补全判定不得因路径预定义而简化。
- **05 号 §2.5 Quick Update 路由表**：与 Quick Query 对称的更新场景快捷入口（6 条场景→WF 编号），含 SKILL.md §7 底线 #2 安全声明（写入仍须 pending-changes 登记）。
- **交叉引用**：01/02/03/04/09 号级联传播规则末尾各追加指向 00 号 §9 的交叉引用（声明"互补不替代"）。

### Changed
- SKILL.md §6 路由表 L136 "待办索引同步"替换为"待办状态更新（WF-1）"（必须加载 00+01+03+04+06+10），新增与"任务看板更新"行的分工边界说明。
- SKILL.md 版本控制表 L243 过期版本号修复（"当前 1.12.0"→"当前 1.14.0"）。
- QODER_RULES.md §3 新增 WF-1 快捷路由行；§6 新增 WF-1/WF-2/WF-3 加载指引行；§6 加载规则追加 WF 例外说明（WF 场景委托 SKILL.md 路由表，不受 2 文件上限约束）。
- SKILL_BLUEPRINT.md §5.2 能力矩阵新增 WF 路径注释（执行效率优化层，非独立 CAP）；§11.3 追加 1.14.0 结构变更行。

### Tests
- 回归套件新增 Module 31 Workflow Data Path（WF-001~005，5 用例：3 正向 + 2 回归），总计 179→184 用例。

---

## 1.13.1 — 2026-08-12（已发布 · released）

> 发布归档：Patch（v1.13.0 升级后治理修复）。修复 versionHistory 数组排序倒置（indices 15-33 从升序改为降序，对齐"最新在前"约定）；SKILL.md `updated_at` 日期同步缺口修复（sync_version.py 新增 updated_at 同步）；versionHistory 条目去重与排序一致性保障。

### Fixed
- versionHistory 数组 indices 15-33（0.1.0→1.6.0）排序从"最旧在前"修正为"最新在前"（1.6.0→0.1.0），与 indices 0-14 约定一致。
- SKILL.md frontmatter `updated_at` 字段由 2026-08-11 修正为 2026-08-12（v1.13.0 发布日期）。
- `scripts/sync_version.py` 新增 `updated_at` 同步逻辑，防止后续版本再出现日期缺口。

### Changed
- 版本 1.13.0 → 1.13.1（Patch）；Workspace Schema 保持 0.6.0（无迁移）。

---

## 1.13.0 — 2026-08-12（已发布 · released）

> 发布归档：CR-20260812-001（架构精简改造）。覆盖 5 条改造线：实体级联嵌入、文件膨胀治理、索引派生分级、版本同步收口、Blueprint 瘦身。基线快照见 `governance/baselines/1.13.0/`，回归见 `governance/regression-reports/rr-20260812-1.13.0.md`。

### Added
- **A 线 · 实体级联嵌入**：6 个实体规则文件新增 `§级联传播规则`（03 §8、04 §9、07 §7、08 §9、09 §8、02 §6），声明实体状态变更后 AUTO（写派生视图）/CHECK（只读校验）/SUGGEST（写事实源待确认）三类下游动作；00 号新增 §8 级联冲突处理；AUTO 作用域限定非事实源的派生视图（受 `skill-contract.md` 第 5 条约束）。
- **B 线 · 文件膨胀治理**：06 号 §6.2 新增 decision-log/issue-register/transfer-log 拆分行，§6.3 新增持续拆分模式，§9 归档规则操作化为通用归档表（实体/触发/目标/索引）；02 号新增 decision-log 归档规则；08 号归档粒度改为纯条数触发+归档索引；09 号新增 transfer-log 归档 + resource 生命周期；01 号 §5.8 扩展为通用归档检查；15 号新增 §15 存储生命周期；11 号新增 §16 存储生命周期。
- **C 线 · 索引派生分级**：14 号新增 §2.4 索引派生分级（完全派生 AUTO / 增量维护 / 独立累积）；§2.2 加"实体级联完成后"维护项；D13/M8/R7 级联完整性自查项。
- **D 线 · 版本同步收口**：新增 `scripts/sync_version.py`（自 `_version.py` 单一源同步 VERSION/SKILL.md/skill.json）；release-checklist 新增运行检查。
- **E 线 · Blueprint 瘦身**：§1 版本行、§5.3 分布、§9.1 稳定能力、§11.3 结构变更改为指向单一事实源或 CHANGELOG；§7.2 补充级联依赖声明说明。
- 新增模板 `assets/templates/decision-log-template.md`（决策日志此前无模板）。

### Changed
- 版本 1.12.0 → 1.13.0（Minor）；Workspace Schema 保持 0.6.0（无迁移）。
- SKILL.md §15 规则索引为 6 个实体文件补充级联传播说明。

### Regression
- 回归套件新增级联传播场景用例；全量回归见 rr-20260812-1.13.0.md。

### Risk
- **contract_change**：00-pm-main-rules.md 新增 §8 级联冲突处理（检测 CHECK/SUGGEST 结果与上下文矛盾，标记 ⚠ 级联异常交 PM 决策，不自动解决）。
- **AUTO 作用域约束**：所有 §级联传播规则声明 AUTO 仅作用于非事实源的派生视图（todo 索引/各类派生 index），事实源写入一律受 `skill-contract.md` 第 5 条约束。

---

## 1.12.0 — 2026-08-11（已发布 · released）

### Added
- 新增 §18 根目录白名单（15 项：9 文件 + 6 目录含 .git/），AP-4 驱动维护机制。
- 新增 §19 交付物类型控制（CR/AP/IA/RR/基线快照，未列举类型不得创建），作用域 governance/。
- 新增 §20 引用完整性约束（归档文档中引用的文件路径必须指向实际存在的文件）。
- §2 流程从 10 步扩展为 12 步：第 10 步清理、第 11 步验证、第 12 步基线快照（时序修正）。
- release-checklist 新增"Project Cleanliness"检查组（6 项）+ 已知污染类型附录（P-01~P-06）。
- 回归套件新增 Module 28 Workspace Cleanliness（CL-001~CL-004），总计 167 用例。

### Fixed
- F-01~F-05：清除根目录非标准文件（A-升级方案、RELEASE-NOTES×3、CR-1.10.0/）。
- F-06：清除 scripts/__pycache__/ 构建缓存。
- F-07~F-10：修复 CHANGELOG/CR/基线 README/RR 中的幽灵引用（RELEASE-NOTES、A-升级方案）。
- F-11：修复 SKILL.md 版本控制表陈旧版本号（1.10.0→1.11.0）。

---

## 1.11.0 — 2026-08-11（已发布 · released）

> 发布归档：CR-20260811-002。基线快照见 `governance/baselines/1.11.0/`，回归见 `governance/regression-reports/rr-20260811-1.11.0.md`。

### Added (contract_change)
- 新增「主动变更 + 人工确认」更新模式（CR-20260811-002, Minor）：事实源更新从悲观确认改为主动写入 → 标记 `Confirmed By: 待确认` → 登记 `pending-changes.md` → 人工确认后持久化生效；确认前在到期判定、已完成统计中一律视为未确认，且支持 7/14 天催办与驳回回滚。
- 新增运行时索引 `pending-changes.md`（单项目 `ai/pending-changes.md`、项目集 `ai/portfolio/pending-changes.md`），作为 Change Log 中待确认条目的子集视图/指针索引；新增 `assets/templates/pending-changes-index-template.md`。
- Change Log 分层归档：活跃区 50 行或超 30 天触发按月归档至 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航；新增 `change-log-index-template.md` 与 `change-log-archive-template.md` 两个模板。
- §5a.3 确认窗口期（待确认 Due Date 空窗期）：待确认记录的 Due Date 不参与延期/超期判定（复用 Confirmed By 值 + pending-changes 索引判定，不新增字段列）。

### Changed (contract_change)
- `governance/contracts/skill-contract.md`：硬约束 #5 修改为「事实源更新必须经过确认、明确触发，或按主动变更模式写入并标记待确认（`Confirmed By: 待确认`）；任何先写后确认的记录必须先登记于 `pending-changes.md`，人工确认后方视为持久化且生效」。
- `SKILL.md`：§7 安全底线 #2 增加主动变更模式路径（低/中风险允许先写后确认，需标记待确认 + 登记 pending + 可回滚），§4 序言补充 pending-changes 说明，frontmatter 版本/schema 同步。
- 权限模型改名：`auto_write_low_risk` → `proactive`（新默认）、`suggest_only` → `passive`、移除 `confirm_before_write`（存量映射 `proactive`）、`auto_write_all_except_critical` → `progressive`；涉及 00/01/10 等规则文件统一枚举。
- 参考规则批量适配：06-file-rules（归档 50 行/30 天 + 待确认注释）、03-task-board（待确认不参与延期计数 + 确认窗口期）、04/07/08（归档对齐 + 概念域 B 注释）、05-query（待确认前置检查 + 聚合 pending 标注）、14-self-check（索引维护 + D11/D12）、19-info-completeness（P0-P3 分级超期）等。

### Compatibility
- Workspace Schema 0.5.0 → 0.6.0：`migrate_workspace.py` 新增 `SCHEMA_060_DIRS`/`PORTFOLIO_060_DIRS`（`change-log/archive`）与 `VERSION_CAPABILITIES` 1.11.0 条目，`check_missing_dirs/files` 模式感知（portfolio vs single）；`scripts/_version.py` 单一版本源 bump。
- 迁移时区分活跃 pending 与历史遗留：仅将 Change Log 中 `Confirmed By: 待确认` 的活跃条目写回 pending-changes，历史已确认条目仅归档。
- 旧工作区降级策略：无 pending-changes 时按既有确认流程工作，不报致命错误。
- 无新增规则文件、无新增字段列、无新增 ID 前缀、无新增操作类型枚举（概念域 B 仅注释说明，不新增 `proactive_change` 枚举）。

### 回归测试
- 用例合计 154 → 163（新增 PW-001~006 待确认窗口期用例 6 个 + CLA-001~003 change-log 归档用例 3 个）。
- 分类：99 positive（94 + PW-001,2,3 + CLA-001,2 = +5）、64 regression（60 + PW-004,5,6 + CLA-003 = +4）。
- UT-001 / SG-001 / SG-002 预期更新，适配主动变更模式与 contract_change。

Blueprint Impact: full — §1 基本信息/能力地图新增 Proactive Change、Pending Index、Change Log Archive；§5 能力矩阵与成熟度统计、§9.1 稳定能力、§11.3 已落地变更追加 1.11.0 行。

---

## 1.10.2 — 2026-08-11

### Fixed
- 脚本层版本治理（CR-20260810-009, Patch）：修复版本号分散且不同步问题。
  - 新建 `scripts/_version.py` 作为 `SKILL_VERSION` / `WORKSPACE_SCHEMA_VERSION` 的单一版本源；`init_workspace.py`、`migrate_workspace.py` 与 `chronopm_init/config.py` 统一从该源读取，消除了 `config.py`（落后为 1.9.0）与 `migrate_workspace.py`（落后为 1.6.0）的硬编码版本失步。
  - 修复 `migrate_workspace.py --target-version` 被忽略的 bug：`update_version_file()` 与 `append_migration_log()` 现接受并使用目标版本写入 `.skill-version.json` 与 `migration-log.md`（缺省回落单一版本源），此前打印显示目标版本但实际写入旧常量。
  - 补全 `VERSION_CAPABILITIES` 能力检测表（新增 1.7.0/1.8.0/1.9.0/1.10.0/1.10.1 条目）。
  - `file_registry.py` 中 single/portfolio README 的硬编码版本（0.4.0/0.2.0）改为 `{SKILL_VERSION}`/`{WORKSPACE_SCHEMA_VERSION}` 插值。

### Changed
- `governance/review-checklists/release-checklist.md` 新增「Script Version Consistency（脚本层版本一致性）」检查项，防止版本分散问题复发。

### 影响范围
- 无能力变更：不新增/不删除任何 CAP（CAP-001 ~ CAP-024 保持不变）。
- 无契约变更：规则层（references 00-21）、模板层均未改动。
- Workspace Schema 保持 0.5.0，无迁移。
- 脚本行为：`--target-version` 现在实际生效（行为修正）；不传参时默认版本由 1.6.0 修正为单一版本源 1.10.2。
- 回归：新增 SC-1G~1K 共 5 个脚本契约用例，回归套件由 149 增至 154 用例；其余既有 149 用例不受本次改动影响。
- Blueprint Impact: none（仅脚本层修复，不涉及能力矩阵/架构正文）。

---

## 1.10.1 — 2026-08-10

### Fixed
- 修复 `SKILL_BLUEPRINT.md` §5.3 成熟度分布统计的计数错误（CR-20260810-008 执行遗留）：L3 由 19 修正为 18，占比由 79% 修正为 75%，L2 占比由 0% 修正为 4%。修正后与 §5.2 能力矩阵（24 项 CAP，L4=5 / L3=18 / L2=1）及 §9.1 稳定能力列表（22 项 = 4 L4 + 18 L3）完全对齐。

### 影响范围
- 无能力变更：不新增/不删除任何 CAP（CAP-001 ~ CAP-024 保持不变）。
- 无契约变更：规则层（references 00-21）、模板层、回归套件内容均未改动。
- Workspace Schema 保持 0.5.0，无迁移。
- 回归：149 用例不变（BluePrint 相关 BP-002/BP-003 不受影响）。
- Blueprint Impact: none（仅 §5.3 一处文档统计修正，不涉及能力矩阵正文）。

---

## 1.10.0 — 2026-08-10

### Added
- 新增 CAP-024：历史计划全量同步与变更追溯（R1-R4）
- R1 历史计划批量导入：将存量计划（.pod / Excel / 遗留 board 导出）经 `references/15-snapshot-rules.md` §8a 固化为 external_import 冻结快照（`snapshots/daily/imported-{date}.md`），登记 `history-index.md`，并联动写入 board（Source=import）
- 新增 `assets/templates/plan-import-template.md`：R1 批量导入工作表
- 新增 `assets/templates/delay-stats-template.md`：A 类延期/变更统计表
- 回归套件新增第 25 模块「Historical Plan Import & Change Tracking」（HP-001 ~ HP-017，17 用例：11 正向 / 6 回归）

### Changed (contract_change)
- `references/03-task-board-rules.md`：board 新增字段 Original Due Date（不可变）/ Plan Change Count / Delay Count；新增 §1a 计数字段判定、§5a B 类超期判定与追责归属（确认窗口期/负责人变更/双触发时机/索引优先）；§7 补概念域说明
- `references/15-snapshot-rules.md`：新增 §8a external_import 批量导入快照规则；source_type 统一为 4 值（personal_daily_reports/pm_todo/meeting/external_import）
- `references/05-query-rules.md`：新增 §6.5 聚合计数路由（A 类，只读 board 单文件）、§6.6 状态查询路由（B 类，实时计算 + 索引优先）；查询类型表/Quick Query 表补 R1-R4 行
- `references/08-change-control-rules.md`：概念域 B 枚举追加 `plan_change`（requirement/scope/schedule/cost/resource/plan_change）；新增 §1.1 概念域说明（与概念域 A 不合并）
- `references/13-continuity-rules.md`：新增 §2 与 R1 的边界判定表（按是否独立历史工作区路由 13 号或 R1）
- `references/00-pm-main-rules.md`：§2.7 意图检测新增 4 路由（历史计划批量导入/计划变更追踪/延期统计/超期查询）
- `SKILL.md`：压缩至 248 行（MN-1），§6 路由表/§15 索引表补 R1-R4 条目，frontmatter version → 1.10.0
- 模板层：task-board（字段映射表）/ change-log（plan_change）/ index-formats（概念域注释）/ daily-todo-snapshot / daily-todo-actuals / weekly-todo-snapshot / weekly-todo-actuals / todo-history-index（外部导入登记）/ import-log 共 9 个模板更新

### Compatibility
- Workspace Schema 保持 0.5.0（不变，无迁移）
- 不删除、不弱化 CAP-001 ~ CAP-023
- 旧工作区 board 无计数字段时缺省按 0 处理；聚合查询可回退 Change Log 并标注"推断，未确认"
- `daily_reports` 作为 `personal_daily_reports` 的兼容旧值保留
- 不影响事实源内容准确性和安全底线

### 回归测试
- 用例合计 132 → 149（新增第 25 模块 17 用例，11 正向 / 6 回归）
- BP-002 硬编码版本 1.7.1 → 1.10.0；BP-003 规则文件数 17 → 22（00-21）
- SK-1E 规则索引计数更新为 00-21（共 22 条）
- FC-1A/SK-1A 行数校验：SKILL.md=248、06=292、15=297、05=276、08=196、13=280、00=262 均 ≤300

Blueprint Impact: full — §1 基本信息、§5.2 能力矩阵追加 CAP-024、§5.3 成熟度统计更新、§7.1/§7.2 规则清单与依赖、§8 数据流、§9.1 稳定能力、§11.3 已落地变更追加 1.10.0 行

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
