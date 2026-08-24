# 文件管理约束规则

本规则适用于项目记忆库中文件的命名、创建、更新、拆分和归档。

## 1. AI 文件目录边界规则

### 1.1 核心原则：业务目录不侵入

AI 生成的所有管理文件必须统一存放在 `ai/` 目录下，**严禁在业务代码目录或项目交付物目录中创建任何 AI 管理文件**。本包为单项目工作区；集层目录不属于本包结构，跨项目归集见 ChronoPM-Portfolio。

### 1.1a project-brief.md — AI 首读文件

本项目 `context/project-brief.md` 是 AI 的**快速入口文件**（R4 归属判定配套）。

**规则：**
1. AI 在处理任何用户输入（文本、文件、口述）前，**必须先读取 `project-brief.md`**，获取项目基本信息、团队成员、文件路由速查表，并判定输入与本项目的关联度（他项目内容按 01 号 §1.0 分流，禁代写）。
2. AI 通过 `project-brief.md` 判断输入与当前项目的关联度，确定项目归属和作用范围。
3. `project-brief.md` 应保持精炼（建议 ≤ 100 行），只放 AI 快速判断所需关键信息。详细背景见 `project-context.md`。
4. `project-brief.md` 是事实源文件，更新需经用户确认。
5. 项目初始化时由 `init_workspace.py` 自动生成空模板。
6. **团队信息指针化**：`project-brief.md` 中的团队信息不应复制花名册全文，而应使用指针。brief 团队部分替换为：
   ```markdown
   ## 3. 团队成员
   → 见最新合法日 `todos/{date}/_index.md` §1 花名册（人员当前状态主源）
   → 见个人待办 §0.5（有待办者的进出组历史）
   ```
   **迁移规则**：不自动删除 brief 已有团队列表，只新增主源指针并标记冗余待清理。下次花名册更新时提示用户"brief 团队列表已指针化，建议删除冗余信息"，确认后删除。禁止再指向已退役 `resource-register.md` / `transfer-log.md`。

| 目录 | 是否允许创建AI文件 | 说明 |
|---|---|---|
| `ai/` 下本项目目录（todos/wps/risks/issues/plans/requirements/decisions/reports/meetings/context/outputs/logs/backup） | ✅ 允许 | 本项目管理工作区。`resources/` 已退役，人员读 todos；`backup/` 禁读（见 §1.7）。过程日志=`logs/ops/`；决策文件=`pm-decisions.md`（懒建） |
| 业务代码目录 / 需求文档目录 / 交付物目录 / **工作区根下除 `ai/` 外的一切（含与 `ai/` 平级）** | ❌ 禁止 | AI 不得在此创建或修改任何文件。生成物只进 `ai/outputs/{timestamp}/`。宿主 final workspace folder / cwd 若等于项目根，忽略并改映射到 outputs |
| 他项目 `ai/` | ❌ 禁止 | 不得代写；跨项目可见性由 ChronoPM-Portfolio 只读聚合 |

### 1.2 集层目录（本包不使用）

`portfolio/` 集层目录**不是**本包工作区结构。跨项目索引 / 汇总周报 / 共享人力请使用 ChronoPM-Portfolio。本包只维护下方单项目树。

### 1.3 单项目目录结构

直接放 `ai/` 下（无 `portfolio/`、`projects/` 分层）：
```
ai/ ├── todos/ ├── wps/ ├── risks/ ├── issues/ ├── plans/ ├── requirements/ ├── decisions/
   ├── reports/ ├── meetings/ ├── context/ ├── outputs/ ├── logs/ops/ ├── backup/
   └── pm-decisions.md（懒建，不预建）
```
> v2.1.0：原 `continuity/` 目录合并入 `context/`（4 个文件：carryover-register/import-log/legacy-sources/project-lineage）；原工作区根目录 `outputs/` 移入 `ai/outputs/`，工作区根目录只留一个 `ai/` 顶层目录。
> v3.11.0：写任何文件前走 00 P-ALWAYS 三路分类。生成物禁止落到项目根。PLAN 文件必为 `plans/PLAN-NNN-{name}.md`，5 节，`status: 正常|废弃`。WP 文件必含 §7 状态历史（缺=待补全不判死）。
完整树见 `SKILL.md` §3.2。

### 1.4 更新权限分级

默认采用 `proactive` 模式（主动变更 + 人工确认）。项目可在 `prompts/project-rules.md` 中修改权限级别。

**低/中风险更新（proactive 模式下直接写入事实源，并标记 `Confirmed By: 待确认`，同步登记 `pm-decisions.md` 对应块，待 PM 确认后持久化）：**
- 日报归档、会议纪要草稿归档、评审纪要归档
- 周报草稿生成
- 花名册/§0.5 人员变动候选、AI 操作日志 / 过程日志更新
- 待办缺负责人 → `pm-decisions.md` **块 6**（不落无主待办）；未绑定 WP → **块 5**；已经写了等点头 → **块 8**
- 风险/问题候选新增为开放
- 任务 Due Date / 状态中途 / Owner 等过程性更新（写事实源并标记待确认）

> 低/中风险先在事实源记录新值并标 `Confirmed By: 待确认`，PM 确认后翻转为 PM 姓名，驳回则恢复原值并追加 `已驳回` 记录。若配置 `update_mode: passive` 则回退为"仅输出建议清单，不写事实源"。

**高风险更新（必须确认后才能更新）：**
- 需求状态确认/取消、需求变更批准
- 预算/P&L 金额调整、里程碑日期调整
- 任务关闭、风险/问题关闭
- 正式决策记录、验收结论
- 人员正式离场、删除/覆盖/重写历史记录

详细触发机制和路由见 `10-update-trigger-rules.md`。

### 1.5 人员状态与历史分离规则（v3.8.0）

人员事实源在待办体系，**禁止**再写 `resources/resource-register.md` / `transfer-log.md`（已退役，见 `backup/`）。禁止另建 `花名册.md`。

| 位置 | 定位 | 内容 | 更新方式 |
|---|---|---|---|
| 最新合法日（date≤今天）`todos/{date}/_index.md` **§1 花名册** | 当前状态主源 | 全员名录（姓名/缩写/岗位/状态六态/首次进组/分配方式/备注） | 覆盖更新该节；无待办者进出组也只改这里 |
| 同文件 **§3 当日参与** | 当天目录派生 | 当天实际有待办文件的人（Owner/File Ref/Todo Count/来源） | 由当日个人文件重建，不独立维护；**扫描排除整个 `inbox/`**（含 `.claim-*` 与点文件） |
| 同文件 **§6 TD 缩写** | 缩写权威 | 姓名/现行缩写/历史别名/冻结日 | 一人一行；冲突 ASK |
| 个人待办 **§0** | 有待办者身份细节 | 只留联系方式、负责模块 | T+1 拷贝；岗位/在组状态以花名册为准 |
| 个人待办 **§0.5** | 有待办者流转历史 | 进组/出组日期、触发依据 | 追加事件行，不删历史行 |

**规则：**
1. 当前状态只写最新合法 `_index` §1；§3 必须能在同文件 §1 找到对应人；File Ref 必须指向已存在文件。§3 扫描排除整个 `inbox/`（含 claim）与点文件，inbox 稿不是当日参与。
2. 应建档人员进出组追加当天 §0.5（当天读/写 todos 则必有文件）；已出组只改花名册（状态 + 首次进组 + 备注含离场日/原因）。禁止仅为查询给已出组建档。
3. 跨项目共享人力索引不在本包维护；查询请使用 ChronoPM-Portfolio。
4. 检测到资源变动时，建议更新花名册 §1，有待办者同时追加 §0.5；须确认后写入。

### 1.6 单项目人员管理（接替原 resources/ 归档）

不再对 resource-register / transfer-log 做年度或 90 天归档（§9 已删这两行）。存量退役文件经分类器、PM 确认后搬入 `backup/`，不留归档读链。人员历史回看读最新结构：花名册 + §0.5。

### 1.7 归档 / 备份双概念（v3.8.0）

| 概念 | 是什么 | 读 | 巡检 | 作源 |
|---|---|---|---|---|
| **归档** | 06 §9 表内存活类型（issue/risk/decision/snapshot-actuals/outputs）+ change-log 月归档 + parse-log / project-notes 归档 + ops 跨月归档 `logs/archive/YYYYMM-ops.md` + pm-decisions 决策记录月归档 | **索引受控可读**：先读 index，按指向读分片，禁止遍历目录 | 不巡检归档分片字段 | 可按索引回看（活历史） |
| **备份** `backup/` | 升级垃圾与退役人员文件（如 resource-register / transfer-log 及年度切片） | **禁读**（用户显式单次解封或本次迁移步骤除外） | 不巡检 | **不作源** |

`logs/migration-log.md` 标记「视为 backup」的根级目录（如工作区根 `backup-v*` / `*-pre-*upgrade*`）与 `backup/` **同效力**：禁读、不巡检、不作源，不搬入 `ai/backup/`。

索引对已搬入 backup 的退役文件只留去向一行（写 migration-log），不给读路径。

## 2. 文件命名规范

### 2.1 事实源文件

固定文件名，不附加日期：
```
todos/{date}/{owner}.md
todos/{date}/_index.md
pm-decisions.md
logs/ops/_index.md
logs/ops/YYYY-MM-DD.md
risks/risk-register.md
issues/issue-register.md
decisions/decision-log.md
plans/progress-plan.md
plans/PLAN-NNN-{name}.md
plans/budget.md
wps/_index.md
wps/WP-NNN.md
requirements/_index.md
requirements/requirement-register.md
requirements/change-log.md
requirements/source-type-registry.md
requirements/contract-register.md
requirements/sources/_index.md
requirements/sources/{编号}/meta.md
requirements/sources/{编号}/ledger.md
requirements/sources/{编号}/parse-log.md
requirements/sources/{编号}/atoms.md（或 atoms/ 分片，>300 条或 >1500 行；软阈值可在本文件本条调整）
requirements/canonical/canonical-index.md
requirements/canonical/CAN-*.md
requirements/atoms/atom-index.md
requirements/atoms/{category}-index.md
requirements/atoms/{category}.md
```

### 2.2 集层事实源（本包不写）

集层 `portfolio/` 路径已迁 ChronoPM-Portfolio。本包事实源仅 §2.1 所列本项目文件。

### 2.3 过程记录文件

按日期命名，格式：`YYYY-MM-DD-[描述].md`

**目录层级规则：按月归档，使用 `YYYYMM` 单级目录，不再使用 `YYYY/MM` 两级。**

```
reports/daily/project/YYYYMM/YYYY-MM-DD-[project]-项目日报.md
reports/weekly/YYYY/YYYY-Wxx.md
meetings/YYYYMM/YYYY-MM-DD-[topic].md
reviews/YYYYMM/YYYY-MM-DD-[event]-retrospective.md
```

> **v2.0.0**：个人日报文件与个人进度汇总文件（原 `reports/daily/personal/` 及 `summaries/[name]-progress.md`）已删除；成员工作汇报写入待办文件工作日志段，个人进度由待办文件实时聚合。
>
> **v2.1.0 废弃路径标注**：`reports/daily/personal/`（任何子目录层级）已废弃，**禁止写入**（见 01 号 §1.2a 与本文件 §12 禁用清单）；周报路径统一为 `reports/weekly/YYYY/YYYY-Wxx.md`（R-1，以 01 号 §3.0 单项目周报为准，不再使用 `YYYY-Wxx-[project]-周报.md` 旧命名）。
>
> **v3.4.0**：`reports/timeline/` 懒建（首次生成时间线报时创建），**不列入本标准结构表**，健康检查不得因缺该目录报 P0。历史 `todos/{date}/{owner}.md` **不可变留档**（存根有效性前提）；回改必须登记 `pm-decisions.md` 并标注受影响报告存根可能失效。**受控例外（v3.10.0）**：能耗补录回写**已有**历史日个人文件的 §0.6 允许，须登记 pm-decisions + 存根影响；禁止 `*-energy-*.md`；无该日文件仍不建历史空目录。
>
> **v3.9.0**：过程日志 `logs/ops/` 懒建（无 `_index.md` = 尚未发生，不报 P0）。`pm-decisions.md` 懒建，不预建实例。旧 `pending-changes.md` 迁入后进 `backup/`，不再当事实源读。

### 2.4 月度文件数量阈值规则

默认一个月的项目日报放在同一 `YYYYMM/` 目录。当单月日报数量超过 **800** 个时，AI 建议启用按日期二级拆分：
```
reports/daily/project/YYYYMM/YYYY-MM-DD/[project]-项目日报.md
```
未超过阈值不主动拆分，避免目录过深。

### 2.5 索引文件

固定文件名：`index.md`，放在对应目录下。

### 2.6 历史计划导入快照（external_import）

历史计划批量导入（R1）生成的快照复用 `todos/snapshots/daily|weekly/` 目录，文件名以 `imported-` 前缀区分：`imported-{YYYYMMDD}.md`，frontmatter 标注 `source_type: external_import`。文件命名、元数据与冻结规范详见 `references/15-snapshot-rules.md`（本文件不重复）。

### 2.7 路径书写基准（v2.1.0 新增，需求十二）

为消除各规则文件路径前缀不一致（有的带 `ai/` 前缀有的不带），统一书写基准：

1. 规则中书写的路径均为**本项目 `ai/` 根相对路径**，如 `reports/weekly/` = `ai/reports/weekly/`
2. 本包不使用 `ai/portfolio/` 或 `ai/projects/{子项目}/` 作为默认存储路径
3. 跨项目引用由 ChronoPM-Portfolio 处理；本包需提示时只给项目名 / 兄弟项目 ai 路径指针，不代写

### 2.8 过程日志、inbox 与临时文件（v3.10.0）

过程日志**不是**事实源，记的是对话过程（用户摘要、本轮动作、改动文件、出处），不是 token 表。查询先读 `logs/ops/_index.md`（无则尚未发生）。路径单一事实源：一律 `logs/ops/_index.md`，禁止再写 `ops-index.md`。ops 懒建，不预建。

**有用户消息就写一行。** 用户摘要 ≤80 字，禁止贴会话全文。改动文件无则写「无」。用量：宿主给了才写「模型 token 秒」，不给写「—」，禁止「未知」填满一行。

**新旧切换：** 升级后新建的日期文件一律新 7 列（时间 / 用户摘要 / 本轮动作 / 改动文件 / 结果 / 出处 / 用量）。已存在的旧列日文件**整文件冻结只读，不追加**。升级当天该日已有旧文件、本轮还要记 → 新建 `YYYY-MM-DD-p2.md` 用新列；禁止同文件双表头。查询旧文件声明「旧格式，不作数」。

**落盘（活跃区按日）**

| 文件 | 内容 | 上限 | 超限 |
|---|---|---|---|
| `logs/ops/_index.md` | 日期指针；场景摘要=当天对话要点，不是「收尾」 | 自身 ≤100 行 | 旧月指针进 archive 索引 |
| `logs/ops/YYYY-MM-DD.md` | 表 A 对话流水 | **300 行** | 拆 `YYYY-MM-DD-p2.md`，index 加一行 |
| `logs/ops/YYYY-MM-DD-errors.md` | 表 B 字段错误（无错误则不建） | **300 行** | 同样 -p2 |
| `logs/ops/runs/{run_id}/{隔离键}.md` | 运行中工人私有，逐步 flush | 单文件 ≤100 行 | 工人不得改别人的 run 文件 |
| `logs/archive/YYYYMM-ops.md` | **跨月**整包（不是超 300 行的去处） | — | 活历史，index 受控可读 |

收尾必须把 `runs/{run_id}/` **并入当天文件后删除该 run 目录**。禁止把分片当长期存储。禁止等整批结束再补写当天日志。禁止编造 token/模型/耗时。token 是用量，不是 API Key。禁止全未知行。

**临时文件三件套（结束必须空）**

| 文件 | 有没有业务内容 | 谁建 | 谁删 | 禁令 |
|---|---|---|---|---|
| `todos/{date}/inbox/{owner}-{HHmmss}-{agent}.md` | **有**（日报/行动项原文） | 工人 | 第一者按实读清单 L 删；冲突则保留，ops 表 B 记失败，下轮/巡检 AUTO 接走 | **禁止静默删；禁止 ASK 挂起** |
| `todos/{date}/inbox/.claim-{owner}-{ISO}-{run_id}.md` | 无 | 每个进入 C' 的人 | 任何结局都删自己的；收尾把剩余 claim 全删 | 可直接删 |
| `logs/ops/runs/{run_id}/` | 过程日志，收尾并入当天 ops | A/B | 并入后删目录 | 可直接删 |

inbox 不是第二份日报。凡改 `{owner}.md` 一律 inbox → C'，无豁免。§3 派生扫描 **必须排除** 整个 `inbox/`（含 claim）与点文件。

## 3. 文档元数据头
每份正式文档头部必须包含：

```yaml
---
doc_type: [文档类型]
project: [项目名]
milestone: [当前里程碑]
version: v1.0
date: YYYY-MM-DD
status: 草稿 / 评审中 / 已确认 / 已归档
author: AI辅助生成
---
```

## 4. 文件创建规则
1. **模板权威 = Skill 包** `assets/templates/`。工作区 `ai/templates/` 只是给人看的副本，**不是权威**。写业务文件前读 Skill 包模板，禁止以工作区过期副本或「昨天那份文件的章节」当规范。
2. 升级时现行模板**覆盖同步**工作区副本；退役模板搬 `backup/`，禁止继续当现行。
3. 新文件必须从 Skill 包对应模板复制。Skill 包没有该 `doc_type` 模板 → **禁止新建**，禁止现场发明模板或章节。
4. 一级标题必须是该 `doc_type` 模板上的节；多出来的节 = 失败。T+1 只拷贝允许的字段，不拷贝已删除的列/节。
5. 创建后必须在对应 `index.md` 中登记（完全派生索引由协调者收尾重建，工人不写 `_index.md`）。
6. 文件创建时状态默认为"草稿"。

## 5. 文件更新规则

1. 事实源文件更新必须经过人工确认。
2. 更新前必须读取文件当前内容，确认版本一致。
3. 状态为"已确认"或"已归档"的文件不可直接修改：
   - 已确认文件：追加新版本，保留旧版本。
   - 已归档文件：不可修改。
4. 每次更新必须在文件底部 Change Log 中记录。
5. 更新后版本号递增（v1.0 → v1.1 小修订，v1.0 → v2.0 大变更）。

## 6. 文件瘦身规则

### 6.1 拆分触发条件

当单个 Markdown 文件满足以下任一条件时，AI 应建议拆分：
1. 超过 300 行。
2. 超过 30 条记录。
3. 包含超过 3 个月的连续记录。
4. 同时包含多个不同管理对象。
5. 用户需要频繁检索其中某类子记录。

### 6.2 拆分规则

| 文件类型 | 拆分方式 |
|----------|----------|
| 日报 | 按天拆分（已执行） |
| 会议纪要 | 按会议拆分（已执行） |
| 复盘 | 按事件或里程碑拆分 |
| Change Log | 活跃区上限 50 行或超过 30 天触发按月归档到 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航 |
| 风险登记册 | 超过30条时按类别或时间段拆分，保留 index |
| 需求登记册 | 超过 **50** 条时按模块拆分 + `requirements/_index.md` 检索索引；查询先读索引再打开命中分片，禁止默认通读整册 |
| 待办文件 | 按人按日天然拆分（`todos/{date}/{执行人}.md`），无需再拆；绑定文件 `_index.md` 与待办文件同日同目录 |
| PLAN 文件 | 每计划一文件（`plans/PLAN-NNN-{name}.md`）天然拆分；必含 5 节；头 `status: 正常\|废弃`；§3 六列（编号/名称/当前状态/执行人/排期/是否里程碑），**父行+节点子行**（子行编号列重复 WP-NNN，名称列 `└ ` 阶段名；空岗写在执行人/排期格，禁止第 7 列），禁止 TD、禁止需求列、禁止按状态分章。只纳入 `effect=正常` 的 WP。投影列不得当独立事实改 |
| WP 文件 | 每 WP 一文件（`wps/WP-NNN.md`）；必含 §7 状态历史（缺=待补全）；§8 阶段清单可跟执行人与排期（列表，不改宽表）；YAML `effect: 正常\|废弃`（缺省=正常），废弃必填 `superseded_by`；头 `status` 仅四枚举；`plan_ref` 多值用 ` / `；索引 `wps/_index.md` 一行/WP 仍 8 列；下辖待办不落盘 |
| decision-log | 超过30条或文件超300行时按季度拆分到 `decisions/archive/YYYY-QN-decision-log.md`，保留 index |
| issue-register | 超过30条时按状态拆分（`已解决`/`已关闭` 归档，主体保留活跃），保留 index |
| 过程日志 ops | 按日 `logs/ops/YYYY-MM-DD.md`；超 **300 行**拆 `-p2`（不是去月归档）；跨月整包归档到 `logs/archive/YYYYMM-ops.md` |
| pm-decisions 决策记录 | 活跃区 **50 行 / 30 天** → `ai/pm-decisions-archive/YYYYMM.md` + 索引指针。开放项不随决策记录一起归档 |

> Change Log 归档采用统一的「活跃区 50 行 / 30 天」规则：活跃区超过 50 行或距上次归档超过 30 天时，将历史条目按月归入 `change-log/archive/YYYYMM-change-log.md`（YYYYMM 为归档月份），并在 `change-log/index.md` 登记该月份导航。主动变更写入时合并写入，同会话确认只记 1 条。`pm-decisions` 决策记录同样 50 行 / 30 天。

### 6.3 拆分后处理

1. 拆分后必须建立或更新 `index.md`。
2. 原文件保留为"当前状态"视图，只保留活跃记录。
3. 历史记录移入归档文件，命名 `YYYY/archive-[描述].md`。
4. **持续拆分模式**（适用于随状态持续增长的文件，如 issue-register）：主体文件只保留活跃状态记录，已关闭/已解决记录定期移入 `archive/` 下的分片文件（命名 `YYYY-[类型]-register.md`）。归档后仍维护主体 `index.md`。此模式与"第 3 点单文件归档"命名并存，二者均为正式规范。

## 7. 索引文件规范
索引文件必须包含相应的列定义，完整 markdown 模板见 `assets/templates/index-formats.md`。

### 7.1 日报同步索引（v3.4.0 废弃）

原 `reports/daily/index.md`（Task Sync / Todo Sync 列）随存根范式停维。存量文件不删。新工作区 init **不再预建**。报告判重改读存根文件名与 YAML `covered`（01 号 §4）。
### 7.2 会议索引
必须包含列：`Date | Meeting ID | Title | Key Decisions | Action Items | File`
### 7.3 周报索引
必须包含列：`Week | Date Range | File | Status | Key Highlights`
### 7.4 WP 索引（v3.5.0）

`wps/_index.md` 必须包含 8 列：`WP 编号 | WP 名称 | 状态 | plan_ref | 负责人 | 是否里程碑 | 关联需求 | 文件路径`。

**状态**合法值：`待确认` / `已规划` / `进行中` / `已完成` / `废弃`。前四值镜像头进度；`effect=废弃` 时本列写 `废弃`（不加第 9 列）。待确认不拆待办、不进计划时间盒。废弃 WP 禁止新待办、不进正常计划。

**语义**：查找加速器，**不是存在性判据**。文件存在性以 `wps/WP-*.md` 为准；索引缺行补行不删除文件；索引有行文件缺失 → 登记 `pm-decisions.md`。plan_ref/状态/关联需求必须与 WP 文件镜像一致（00 号 §8c）。
### 7.5 源文档台账索引（v3.6.0）

`requirements/sources/_index.md` 必须包含 7 列：`编号 | 源文档名称 | source_type | 生命周期阶段 | 版本 | 拆解状态 | 产出计数`。

**语义**：查找加速器。存在性以 `requirements/sources/*/meta.md` 为准；缺行补行。禁止再新建 `{type}-source/`。明细见各目录 ledger，本表不双写。

**分片例外（v3.7.0）**：`sources/{编号}/atoms/` 与 `facts/` 在超过 **300 条或 1500 行**（可配置软阈值，只改本条）时目录化为合法形态。按章节分片，一条 ATOM 不跨片。parse-log 活跃区超限归档同目录 `parse-log-archive.md`。

## 8. Change Log 规范
事实源文件底部必须包含 Change Log，格式见 `assets/templates/index-formats.md`：

- Change Type：`add` / `update` / `remove` / `status` / `archive`
- Source：来源文件或会议 ID
- Confirmed By：确认人姓名（AI 建议的记录为"待确认"）

> 主动变更模式下，`Confirmed By: 待确认` 的「已经写了等点头」还必须同步登记到 `pm-decisions.md` **块 8**，与该条目一一对应；PM 确认/驳回后按 14 号处理。块 1–7 以决策文件为权威，禁止用 Change Log 重建。完整机制见 `14-self-check-rules.md`。

> 注：此处的 Change Type 是**记录操作类型**（对事实源记录执行的操作），与 `references/08-change-control-rules.md` 中需求变更**影响分类**（requirement/scope/schedule/cost/resource/plan_change）是两个不同概念域，不可混用。计划变更（plan_change）在待办文件底部 Change Log 中以 `update` 操作 + Description 标注体现，不在本枚举中新增类型。

## 9. 归档规则

以下实体满足触发条件时，AI 应在当前处理流程末尾执行归档检查（通常为日报处理 §5.8 通用归档检查、周报生成或相应实体变更流程）：

| 实体 | 触发条件 | 归档目标 | 索引 |
|------|----------|----------|------|
| issue（已关闭） | >30 条 | `issues/archive/YYYY-issue-register.md` | `issues/index.md` |
| risk（已关闭） | >30 条 | `risks/archive/YYYY-risk-register.md` | `risks/index.md` |
| decision（已执行） | >30 条 | `decisions/archive/YYYY-QN-decision-log.md` | `decisions/index.md` |
| snapshot/actuals | >90 天 | `snapshots/archive/YYYY/`、`actuals/archive/YYYY/` | —（v2.0.0 起无 history-index，目录内按月直查） |
| outputs（已导出） | >90 天 | `ai/outputs/archive/YYYY/`（v2.1.0 起 outputs/ 在 ai/ 下） | `ai/outputs/index.md` |
| ops 过程日志 | 跨月 | `logs/archive/YYYYMM-ops.md`（超 300 行拆 `-p2`，不去月归档） | `logs/ops/_index.md` |
| pm-decisions 决策记录 | 50 行 / 30 天 | `ai/pm-decisions-archive/YYYYMM.md` | 文件内指针 |

归档检查时机：日报处理末尾（01 号 §5.8 通用归档检查）、周报生成时、或对应实体变更流程末尾（见各实体级联传播规则 [AUTO]/[SUGGEST]）。

运维规则：
1. 归档操作本身必须记录在原文件的 Change Log 中（Change Type: `archive`）。
2. 归档文件状态改为"已归档"；主体文件保留"当前状态"视图。
3. 涉及移动/归档**事实源**文件的动作走 SUGGEST（待 PM 确认）；仅派生视图（索引）刷新走 AUTO。

统一归档粒度标准：
- Change Log（各事实源底部）：50 行 / 30 天 → 月归档（已有，不变）
- `pm-decisions.md` 决策记录：50 行 / 30 天 → `ai/pm-decisions-archive/YYYYMM.md`
- 过程日志 ops：按日 + 300 行拆 `-p2`；跨月归档 `logs/archive/YYYYMM-ops.md`
- 注册表主体（risk/issue/requirement/待办文件）：按条数触发（30-50 条）→ 按类别/状态拆分；需求超 50 条按模块分片 + `requirements/_index.md`
- 日志型文件（decision-log）：按条数触发（30-100 条）→ 按时间拆分。人员流转不再走独立 transfer-log 归档
- 目录型文件（snapshots/outputs/daily-reports）：按时间触发（90 天）→ 年度归档
- ATOM 类别文件 `{category}.md`：超 300 行 → 按 source_type 分片（如 `technical-design_spec.md`），并新增对应 L2 `{category}-index.md` 分片条目
- Canonical 文件：超 50 条 → 按 scope_scope/类别拆分
- project-notes：超 100 条 / 6 个月 → 季度归档到 `context/project-notes-archive/`
- 所有归档后必须维护索引

## 10. 安全规则
1. 不得在文件中记录密码、密钥、Token 等凭证。
2. 涉及客户敏感信息时使用脱敏代号。
3. 不得删除或覆盖状态为"已确认"的文件，只能新增版本。

## 11. PM Profile 文件规范

| 模式 | 路径 | 说明 |
|---|---|---|
| 本项目 | `ai/context/pm-profile.md` | 本项目 PM 偏好档案 |

规则：文件不存在时降级跳过（不视为错误）；初始化时自动创建；旧工作区可 `migrate_workspace.py --create-profile` 补建；已存在不覆盖；pending 偏好不按 confirmed 应用；每条记录保留 Source。详见 `references/21-pm-profile-rules.md`。

## 12. v1.x 遗留路径禁用清单（v2.1.0 新增，读写均禁，统一维护点）

**设计动机**：规则中指向不明、模糊描述（如"继续作为历史缓存""查询兜底仍读"）是 AI 继续插入/维护低版本目录的根因。除物理删除外，规则层明确：**高版本 AI 不得再查低版本目录文件**。本清单为全部 v1.x 遗留禁用路径的**唯一维护点**（需求五三层防护与需求十二三层禁令共用本清单）。

**禁用清单（迁移完成后生效）**：

| 禁用路径 | 禁用原因 | v2 替代入口 |
|---|---|---|
| `projects/*/reports/daily/personal/` | v1 个人日报，能力已并入待办工作日志 | `todos/{date}/{owner}.md` §3 工作日志段 |
| `projects/*/summaries/` | v1 个人进度汇总 | 待办文件实时聚合 |
| `projects/*/tasks/board.md` 及 `tasks/_historic/` | v1 看板体系 | `todos/{date}/` 待办文件 |
| `projects/*/tasks/backlog.md` | v1 遗留 | `pm-decisions.md` |
| v1.x 非标准命名/层级的日报周报文件 | 迁移后不应存在 | v2 标准结构（YYYYMM/ 单级、YYYY/Wxx） |

**禁止读写**：AI 对禁用路径的任何读/写/创建操作均视为严重错误，必须中止并输出警告「⚠️ 命中 v1.x 禁用路径 {path}，已中止。正确入口：{v2 替代入口}」。

**路径校验规则（需求五第三层）**：
1. AI 写入前必须检查目标路径是否在当前版本允许列表中（本文件 §2 命名规范 + 目录树）；命中禁用清单 → 中止并警告。
2. **历史遗留文件识别**：若目标路径下存在大量按日期排列的历史文件，AI 应怀疑这是旧体系遗留，不得照其格式创建新文件（联动 `00-pm-main-rules.md` §4a 执行前自检）；检测到禁用路径存在文件时，提示"迁移未完成"并按 `governance/migrations/upgrade-to-2.1.0.md` 补做迁移，而非就地读取/维护。
3. 版本层拦截见 `20-workspace-version-rules.md`（工作区版本 ≥ 2.1.0 检测到禁用路径存在文件或 AI 试图引用 → 阻断 + 提示迁移/整改）；查询路由排除见 `05-query-rules.md` §2.5 查询性能规则第 5 条。
