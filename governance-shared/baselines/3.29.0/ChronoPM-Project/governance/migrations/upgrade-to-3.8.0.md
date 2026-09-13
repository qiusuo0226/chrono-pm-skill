# 升级到 3.8.0

> 从 3.7.0 升级到 3.8.0  
> 发布日期：2026-08-22  
> Schema 变更：workspace schema **0.12.0 → 0.13.0**（各项目 `ai/` 新增空目录 `backup/`）  
> CR：CR-20260822-001  
> 施工依据：CR-20260822-001 + baseline 3.8.0。决策见本文件与 CHANGELOG 3.8.0 段。AP 草稿已按治理规则删除。  
> 用户拍板：N-44 A/B；创建契机 if-else；花名册=index §1；禁止未来日待办；岗位单源；归档/备份双概念

## 变更摘要

人员事实源改到待办体系（resource-register / transfer-log 退役进 backup）；对外确认说人话；Portfolio 新增 V-11 共享文件拆分与 V-12 术语指针索引；个人待办 §0.6 升为公司中立人工成本台账（日合计拷贝追加，不建历史空目录）。

## 明确不做（施工禁区）

| 禁 | 处理 |
|---|---|
| 代迁市监业务仓待办/register 数据 | 只出分类清单，PM 确认后才搬。本发布不改 `C:\Users\qiusuo\Downloads\市监重构项目管理` 业务文件 |
| 删除 `todos/2026-08-23/` | 自查列出即可，不删 |
| 搬根级 `backup-v2.1.0-*` | 位址豁免，只在 migration-log 记「视为 backup」 |
| 灌任何一家历史工时 xls | 不导入 |
| 新建独立成本台账文件 | 成本只在个人待办 §0.6 |
| 写死人日/人时/金额/外部列名 | 单位只读 project-context |
| 回写历史日个人 md 的 §0.6 | 新文件拷贝旧表再追加 |
| 为回填建历史空目录 | 禁止 |
| 词库总库（方案 A） | 不做 |
| AI 凭空编造成本数字 | 禁止；对账由 PM 负责 |

---

## A. 技能包施工（本发布必须做完）

每行 = 一个改造点。动作必须落到指定路径，禁止「相关规则一并更新」这类空句。

### A1. 版本与元数据

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `ChronoPM-Project/scripts/_version.py` | `SKILL_VERSION="3.8.0"`；`WORKSPACE_SCHEMA_VERSION="0.13.0"` |
| A1.2 | 运行 `python ChronoPM-Project/scripts/sync_version.py` | 同步 Project `VERSION` / `SKILL.md` frontmatter / `skill.json` |
| A1.3 | `ChronoPM-Project/skill.json` | `supportedWorkspaceSchema.current`→`0.13.0`；`migrations` 数组**头部**新增 `{from:0.12.0,to:0.13.0,description:"v3.8.0：backup/ 空目录；人员事实源改待办体系。脚本只建空 backup/ + 升 schema，不改业务文件。"}` |
| A1.4 | `ChronoPM-Project/CHANGELOG.md` | 顶部新增 3.8.0 段（Added/Changed/Notes + Blueprint Impact: full） |
| A1.5 | `ChronoPM-Project/SKILL.md` | frontmatter version/schema/updated_at；§3 结构树 `resources/` 改为「退役，见 backup/；人员读 todos/_index」并加 `backup/`；§4 事实源表删除 resource-register/transfer-log 行，改为 `todos/{date}/_index.md` 花名册+TD 缩写、个人文件 §0/§0.5/§0.6；补一句：跨项目一份文件要进多个成员项目 → 换 Portfolio，禁止本包代写 |
| A1.6 | `ChronoPM-Portfolio/VERSION` + `skill.json` + `SKILL.md` frontmatter + `CHANGELOG.md` | 锁步 3.8.0；workspace_schema 0.13.0（集层结构不加 backup 义务，成员项目 ai 才有） |
| A1.7 | `ChronoPM-Project/SKILL_BLUEPRINT.md` | §1 当前版本 3.8.0；§11.3 演进表新增 3.8.0 行；CAP-010 人员登记改待办体系 |
| A1.8 | 仓库根 `README.md` + `README.en.md` | 版本 3.8.0；Project 模板数 38→36（归档 2）；Portfolio 模板 3→5；回归合计 380→390 |

### A2. 人员体系（需求五）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `assets/templates/daily-todo-binding-template.md` | **整文件按新节序重写**：YAML 头保留。§1 在组名单（花名册，7 列：姓名\|缩写\|岗位\|状态(在岗/空闲/请假/借出/待进场/已出组)\|首次进组\|分配方式\|备注）。§2 结转标记原样保留（2.1/2.2/2.3）。§3 当日参与=现行 §1 表后移（Owner/缩写/File Ref/Todo Count/来源/Generated At/备注）；缩写注释改为抄本文件 **§6**，禁止再写 resource-register。§4 当日待办概览=现行 §3。§5 共享人力=现行 §4。**§6 TD 缩写映射**（姓名\|现行缩写\|历史别名\|冻结日\|备注），位置钉死在 §5 后、Revision Log 前。禁止另建花名册.md |
| A2.2 | `assets/templates/personal-daily-todo-template.md` | §0 只留联系方式、负责模块（删岗位/首次进组/当前在组状态三行）；注释改读花名册 §1，删「与 resource-register 冲突以 register 为准」。状态格删「待评审」。§0.6：日表 4 列不变；注释写单位取自 project-context、禁止写死单位；**可选**「分次明细」小节（5 列：日期\|填报时间\|当次量\|外部任务/内容\|关联 TD），无则整节省略禁止空表；金额列不加。T+1：新建文件从该人最新文件整表拷贝 §0.6 再追加当日行（N-44 B） |
| A2.3 | `assets/templates/project-brief-template.md` | 团队信息指针：resource-register/transfer-log → `todos/{最新合法日}/_index.md` §1 + 个人待办 §0.5 |
| A2.4 | `assets/templates/project-context-template.md` | 两段重复「成本核算方式」**合并为一段**。必填：人工计量单位、默认能耗规则；选填：成本单价。新增可选段「外部填报映射」（用途\|列名\|示例\|备注，4 列，人员/时间/量/任务均可空）。禁止写死任何公司列名 |
| A2.5 | `assets/templates/pm-profile-template.md` | DF-014 改指待办 §0.5；DF-012 状态枚举删「待评审」 |
| A2.6 | `assets/templates/resource-register-template.md` | **归档**到 `assets/templates/archive/resource-register-template.md`（建 archive 目录） |
| A2.7 | `assets/templates/transfer-log-template.md` | **归档**到 `assets/templates/archive/transfer-log-template.md` |
| A2.8 | `assets/templates/wp-template.md` | §3b 在现有实体表下新增「评审门清单」可选小节（≤7 列：评审门\|评审对象\|评审人\|状态\|评审待办\|通过日期）；头 status 三态不动；「WP 待评审」=评审门未过的派生结论，不落 status |
| A2.9 | `assets/templates/pending-changes-index-template.md` | 表体改为 ≤7 列；增加类型列（含「人员状态提醒」）；「已经写了等点头」与「还没写等准许」分表或每表标注，禁止混在一张不标注的表；对外表头白话 |

### A3. Project 规则

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `references/00-pm-main-rules.md` | WF-6 读待办 §0.5 + 花名册，不再读 register；WF-7 反向 WBS 读待办；WF-8 缩写查重读 `_index` §6；WF-8 明日计划只写当天个人 §2，禁止建 `date>今天` 目录。§4d T+1 含 §0.6 整表拷贝+追加当日行。§5a 待办状态枚举删「待评审」；人员状态用花名册六态。§3.3 D-23 增「进度=100% 写入路径」：标 100% 必须同时落已完成（用户拍板）；日报原文表明完成的直接落已完成。§10.3 推导链去掉待办「待评审」。评审待办 100% → 翻对应 WP 评审门。关单 SUGGEST 仅当待办挂了未过评审门才问。§5.1 删「必须包含建议更新清单」。新增「对外确认专节」：两套输出分离；禁止对用户说路径/编号/工序名；「请你确认」只=认不认或准不准；每问含背景+建议+选项+后果+回复模板；横幅白话。归档路由表「Change Log 活跃区 → change-log/archive」行保留 |
| A3.2 | `references/01-daily-report-rules.md` | 双轨仲裁改双向闭环（状态已完成⇔进度 100%）。§5.4 白名单按 00 D-23 改写。人员检测读 `_index` §1 / 待办 §0.5。**§5.6**：明日/本周计划只进当天 §2，禁止创建未来日待办目录或行。**§1.6 N-44**：投喂=一个数或一张表或对话里提到的人工成本；表头对不上就问，映射写入 project-context 可选段；按人+日 SUM；禁止写死列名；AI 禁止凭空编数；人工改行必须改来源列；对账 PM 负责 |
| A3.3 | `references/22-carried-over-rules.md` | 时机 0 改写成 N-43 if-else（碰今天任一待办 md 或今天 index → 先看 index 与 `carryover_done_for_today`；不是 true 则先按最新合法日 §1 全员 Step 0，再改点名的人）。扫描名单=最新合法 `_index` §1（date≤今天）。开始/结束/原始结束时间结转原样搬运。扫描排除 archive/ 与 backup/。Step 0.5 读 §1 备注「同时参与」。Step 0.8 空闲检测：次日无待办无日报→花名册标空闲+pending 提醒，不直接出组；只打曾有待办或曾在 §3 的在岗人员。N-37/N-38 禁止未来日；休息日无人上班不建目录。**N-44 B**：§0.6 只拷最新文件再追加；禁止为历史日建空目录；仅今天的能耗投喂才起链 |
| A3.4 | `references/05-query-rules.md` | 资源/人员路由改 todos + `_index`（Quick Query「资源情况」与 §6.3「人员状态」两处）。新增查词义路由：读 `context/domain-glossary.md`。未办结枚举删「待评审」。保留 change-log 月归档与风险/问题归档册读链。人员六态。**N-44**：新增「某人能耗/成本损耗/能效」→ 该人最新文件 §0.6 按日并置 §1/§3；预算成本仍走 `plans/budget.md`，两路不得混 |
| A3.5 | `references/06-file-rules.md` | §1.5/§1.6/§2.1 删除 resource-register、transfer-log。新增「归档/备份双概念」：归档=06 §9 七类+change-log 月归档，索引受控可读；backup/=升级垃圾，禁读/不巡检/不作源；migration-log 标记「视为 backup」的根级目录同效力。§9 表删除 resource 行与 transfer-log 行 |
| A3.6 | `references/18-init-wizard-rules.md` | Step 5 不再创建 resource-register；引导建当天 `_index.md`（含 §1 花名册与 §6 缩写）。Step 1 成本核算方式仍只必填单位+默认规则，映射/分次/折金额不进向导 |
| A3.7 | `references/19-info-completeness-rules.md` | 人员覆盖检查改 `_index` §1 + 待办文件 |
| A3.8 | `references/14-self-check-rules.md` | 增：列出 `todos/{date>今天}/` 为非法；`_index` §3 每人必须出现在同文件 §1；File Ref 必须存在；N-29/N-30 断言 |
| A3.9 | `references/20-workspace-version-rules.md` | 事实源列表删两退役文件。§10 拆开归档 vs backup。对照表增 3.8.0 / schema 0.13.0：缺 `backup/` 则建空目录；人员仍读 register 则提示改读待办体系 |
| A3.10 | `references/10-update-trigger-rules.md` | 资源信号改 `_index` 花名册 / 待办 §0.5。工时表/日志量/能耗投喂 → 01 §1.6，禁止改走 budget |
| A3.11 | `references/12-excel-generation-rules.md` | 「人员资源登记表」数据源改花名册 + 待办 §0 |
| A3.12 | `references/13-continuity-rules.md` | 人员导入指向改待办体系 |
| A3.13 | `references/15-snapshot-rules.md` | change-log 月归档保留索引受控可读；§3.2 归档日报协议不改 |
| A3.14 | `references/16-skill-governance-rules.md` | §2.2 前新增：设计阶段只改 AP；CR 仅用户准许执行时在 `governance-shared/change-requests/` 创建；业务对话严禁创建 governance 文件 |
| A3.15 | `references/21-pm-profile-rules.md` | DF-005/006/015/019 只改指针到 00 对外确认专节，不复述正文 |
| A3.16 | `references/11-output-artifact-rules.md` | 生成物确认加指针到 00 对外确认专节 |
| A3.17 | `QODER_RULES.md` | §7 删「处理类=正文+建议更新清单」；改为指向 00 对外确认专节。§8.2 删两退役人员文件 |

### A4. 脚本

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | `scripts/chronopm_init/config.py` | `SINGLE_PROJECT_DIRS` 增加 `"backup"`；`ALL_TEMPLATE_FILES` 删除 `resource-register-template.md`、`transfer-log-template.md` |
| A4.2 | `scripts/chronopm_init/file_registry.py` | README/简报生成逻辑删除对两退役文件的引用，改为 `_index.md` §1 / 待办 §0.5 |
| A4.3 | `scripts/migrate_workspace.py` | `VERSION_CAPABILITIES` 增 3.8.0 / schema 0.13.0 / `new_dirs:["backup"]` / 空 new_files。`needs_v380` 打印块：脚本只建空 `backup/` + 升 schema；分类器清单由 AI 出、PM 确认后搬；不改待办。升级阶段禁止按 N-30/31 批量改业务待办 |

### A5. Portfolio

| # | 文件 | 动作（写死） |
|---|---|---|
| A5.1 | `ChronoPM-Portfolio/SKILL.md` | §6 增 V-11（共享文件拆分，输出建议更新清单，不代写）、V-12（术语指针索引）。进入工作区：扫 `projects/` 一级 → 新目录问收编 → 收编后自动刷 glossary-index。§8 对外不说「建议更新清单」，改白话；内部能力名 V-9 保留。V-3 数据源改各项目 todos §0/§0.5 + `_index`，删除 resource-register。模板索引加两份新模板 |
| A5.2 | `references/01-readonly-boundary-rules.md` | 可写清单说明 V-11 只写 `portfolio/` 建议清单，不写成员项目 |
| A5.3 | `references/02-aggregation-query-rules.md` | 新增 §9 V-11：默认各放一份（拆一次+拷贝）；不主动建议指针关联；拷贝时注意各项目索引可能不同。V-3 改待办体系。未办结枚举删「待评审」。补集层查词：glossary-index → 指针取证 |
| A5.4 | `assets/templates/shared-file-split-template.md` | **新建** V-11 输出模板（归属建议 / 将复制到哪些项目 / 注意索引差异 / 须确认后才执行） |
| A5.5 | `references/03-mount-awareness-rules.md` | V-1 登记成功后追加：扫描该项目词库 confirmed 条目，写入/更新 `portfolio/context/glossary-index.md`。写明无后台盯盘；`{名}/ai/` 缺失不收编；收编须 PM 点头 |
| A5.6 | `assets/templates/glossary-index-template.md` | **新建** ≤7 列：术语\|标准词\|出现项目\|G 号指针\|确认状态\|备注。只存指针不存全文 |
| A5.7 | `references/05-resource-shared-rules.md` | 人员唯一事实源=各项目待办 §0/§0.5 + `_index`；归并键中文名；缩写读 `_index` §6；流转读 §0.5。跨项目能耗只读聚合各项目最新 §0.6，禁止写入 |
| A5.8 | `references/04-portfolio-report-rules.md` | 周报/资源变动数据源改各项目 §0.5 + `_index` §1 |
| A5.9 | `assets/templates/portfolio-weekly-template.md` | 人力配置表数据源改各项目 `_index` §1 |
| A5.10 | `assets/templates/suggested-update-list-template.md` | 对内表保留。对外增加白话摘要段（标题不用「建议更新清单」）。示例行改待办路径，删除 resource-register 示例 |

### A6. 治理与回归

| # | 文件 | 动作（写死） |
|---|---|---|
| A6.1 | `tests/regression-suite.md` | DR-005 期望改为提示更新花名册/§0.5，不再写 resource-register。新增 Module「v3.8.0 Personnel/Confirm/Cost (PC)」10 条：PC-001 对外不说建议更新清单；PC-002 进度 100% 必须已完成；PC-003 禁止建未来日目录；PC-004 创建契机先全员 Step 0；PC-005 花名册=index §1 无第二文件；PC-006 日合计无分次空表；PC-007 同日多行 SUM；PC-008 能效按日并置不伪造分摊；PC-009 历史回填不建空日目录；PC-010 待办状态无「待评审」。合计 380→390。RM/V3/人员旧路径用例同步改待办体系 |
| A6.2 | `governance-shared/review-checklists/release-checklist.md` | 增 D5：发布验证通过且用户检查完毕后，删除本版 `upgrade-plan-v*.md`。**本发布先保留 `upgrade-plan-v3.8.0.md` 供用户检查**；删除 `upgrade-plan-v3.7.0.md`（Q-4） |
| A6.3 | `governance-shared/migrations-history/upgrade-template.md` | 末尾强制步骤：删除本版 AP 草稿 + CHANGELOG 登记 Removed（发布后执行） |
| A6.4 | `governance-shared/scripts/audit_release.py` | 第 14 条 **警告不阻断**：发现「版本号≠当前」的 `upgrade-plan-v*.md`，或 `planning/` 除 README.md 以外的 `.md`，打印 WARN。当前版 AP 允许留待检查。禁止把本条做成退出码非零 |
| A6.12 | `governance-shared/planning/` | **Q-4**：删除 `requirements-intelligence-scheme.md`（已落地 v1.15.0）与 `contract-scope-ri-scheme.md`（已落地 v1.16.0）。保留目录 + README 写生命周期（Q-5） |
| A6.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.8.0.md |
| A6.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.8.0.md` | 指针文件，指向主包 |
| A6.7 | `governance-shared/change-requests/CR-20260822-001.md` | 本 CR |
| A6.8 | `governance-shared/impact-analysis/IA-20260822-001.md` | 本 IA |
| A6.9 | `governance-shared/regression-reports/rr-20260822-3.8.0.md` | 本 RR |
| A6.10 | 拷贝 `upgrade-to-3.8.0.md` 到 `governance-shared/migrations-history/` | 版本链连续 |
| A6.11 | `governance-shared/baselines/3.8.0/` | 双子树快照：ChronoPM-Project + ChronoPM-Portfolio（发布清洁后复制） |

---

## B. 业务工作区（本发布脚本可做 / AI 清单 / 禁止代做）

对任意已有项目 `ai/`（含市监仓，**本发布不代做数据搬家**）：

| 步骤 | 谁做 | 动作 |
|---|---|---|
| B1 | 脚本 `migrate_workspace.py` | 建空 `ai/backup/`；`.skill-version.json` schema→0.13.0、skillVersion→3.8.0；打印分类器入口 |
| B2 | AI | 分类清单：A 类活历史（issues/archive、change-log/archive 等）留 archive；B 类退役人员文件（resource-register.md、transfer-log.md、resource-register-archive.md、logs/archive 里 transfer-log 年度切片）→ 建议搬 `backup/3.8.0/`；C 类升级垃圾（v1-legacy、v*-legacy*、entity-registry-*、retired-templates-*、*drafts*、未清 v3.7.0-*）→ 建议搬 backup。夹源文档的目录单独列出问人 |
| B3 | PM | 确认清单 |
| B4 | AI（确认后） | 按清单搬 B/C 到 `{ai}/backup/3.8.0/`；去指向（索引只留去向一行写 `logs/migration-log.md`）；**不改待办正文、不按 N-30/31 批量修日期/进度** |
| B5 | AI（确认后） | register 有、无待办文件的人 → 只写入最新合法日 `_index` §1，禁止建空待办。有待办者：下次起链时按新模板补 §0（只联系方式/负责模块）与空 §0.6，**不回填历史能耗数字** |
| B6 | 禁止 | 不删 8-23；不搬工作区根 `backup-*`；根级快照只在 migration-log 记视为 backup |

市监仓本发布：**停在 B1 打印 + 本 RR 注明未代迁**。用户检查技能包后再决定是否迁业务仓。

---

## C. 验证检查

- [ ] `_version.py` 3.8.0 / 0.13.0
- [ ] Project 与 Portfolio VERSION / skill.json / SKILL.md frontmatter 一致
- [ ] `python ChronoPM-Project/scripts/sync_version.py` 已跑
- [ ] `python governance-shared/scripts/audit_release.py` 退出码 0
- [ ] 模板：Project `assets/templates/` 根目录不再有 resource-register / transfer-log（在 archive/）
- [ ] 花名册节序：binding 模板 §1=花名册 §6=TD 缩写
- [ ] 个人模板 §0 无岗位/进组/在组；§0.6 无金额列；分次小节标注可省略
- [ ] 00 号待办状态无「待评审」；有对外确认专节
- [ ] 22 号含 N-43 if-else 与 N-44 B
- [ ] 01 §1.6 含对话检出人工成本 + 禁止编造 + 对账 PM 负责
- [ ] 05 号人员能耗与 budget 两路分开
- [ ] Portfolio SKILL 有 V-11、V-12
- [ ] 新模板 shared-file-split、glossary-index 存在且 ≤7 列
- [ ] 回归合计 390
- [ ] baselines/3.8.0 双子树存在
- [ ] 未改市监业务仓待办；未删 8-23；未搬根级 backup
- [x] `upgrade-plan-v3.7.0.md` 已删；`upgrade-plan-v3.8.0.md` 已于 3.9.0 Step 0 删除（记录闭合）

## D. 发布

1. 提交技能包全部改动（含本文件、CR、IA、RR、基线）。
2. 打 annotated tag：`v3.8.0`，中文说明：`release v3.8.0：人员文件整合 + 确认话术 + 共享文件拆分/术语索引 + 兼容人工成本台账；workspace schema 0.12.0→0.13.0`。
3. `git push origin master --follow-tags`。
4. 3.8.0 AP 已在 3.9.0 Step 0 删除（CR + 本文件 + 基线已接住思路）。
