---
doc_type: upgrade-plan
ap_version: V0.4
status: closed
skill_version_from: 3.30.3
skill_version_to: 4.0.0
workspace_schema: 0.17.0
demands:
  - SG-20260923-001
author: Agent A
created_at: 2026-09-23
workspace: "C:\\Users\\qiusuo\\Downloads\\ChronoPM Skill"
head: d663a40
---

# 升级方案审查文档（Agent A V0.1）

目标版本 **4.0.0**。工作区 schema 保持 **0.17.0**。设计阶段只改本文件。不写 CR，不改技能正文，不执行。

# 1. 方案版本与当前共识

当前方案版本：V0.4  
本轮状态：B2 结语为「修订-需再审」。B2-1、B2-2、B2-3 已按代码改写。B2-4、B2-5、B2-6 不采纳，理由在修订记录。须再审 B2-1 与 B2-2。尚未获「同意执行」，不改技能文件。工作区仍为 `C:\Users\qiusuo\Downloads\ChronoPM Skill`，Skill 3.30.3。

已确认并写入本方案：

1. 单项目查询收成 `ChronoPM-Project/query-skill/`，查询规则和查询脚本都在这个目录里。
2. ChronoPM-Portfolio 收成 `ChronoPM-Project/portfolio-skill/`。不再打 Portfolio 包。项目工作区目录与现在两个技能时相同。
3. 词库、别名、口语说法合并成一份说法表。升级脚本处理旧数据，不问用户，做不完不盖版本戳。
4. 每个权威事实源有机器版本戳。给人看的依据使用已经存在的指针（来源指针、文档链接、工作包编号、Change Log），不新建 `ai/wiki/`。
5. 能由程序判定的步骤用 Python。规则正文只保留推导和路由。

本轮明确不做：Qoder 下架、改本机已安装技能目录、改业务仓库、把所有 Markdown 手写收成脚本。

# 1.5 工作空间版本确认（出方案前）

| 项目 | 值 |
|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` |
| 版本标识来源 | `ChronoPM-Project/skill.json` version |
| 版本标识值 | 3.30.3；schema current 0.17.0；Portfolio VERSION 同为 3.30.3 |
| 快照生成时间 | 2026-09-23（写本文件时） |
| 距上次确认是否有变更 | 否。用户已回复「路径正确」，并要求按已确认范围生成方案 |
| 关键文件 | `ChronoPM-Project/`、`ChronoPM-Portfolio/`、`governance-shared/planning/`（本文件写入前只有 README） |

# 1.6 需求辩论裁决确认

| 项 | 内容 |
|---|---|
| A 上轮建议 | 调整后实施 |
| 用户裁决 | 生成已确认部分的方案；版本 **4.0.0**。查询独立成能力目录。Portfolio 只做合并、工作区保持原样、不再发 Portfolio 包。词库与各种别名合并成一个东西，升级脚本处理存量且不问用户。给人读的依据本轮一起做。下架不在范围内 |
| 留待后议（不阻塞本草稿） | ① 合并后的口语说法能否进入范围登记枚举。② 是否把全部 Markdown 写入收口到脚本 |
| 需求基线 | 下文第 2–18 节。后议两点见第 19 节，执行前若改口，只修订本文件 A 正文 |

# 2. 改造后的整体定位

对外只有一个技能：ChronoPM-Project 4.0.0。它同时做单项目读写和跨项目只读归集。

技能包内两个新能力目录，形态与 `source-split-skill/` 相同：有 `CAPABILITY.md`，没有 `SKILL.md`，宿主扫不到第二个技能。

- `query-skill/`：单项目查询。认说法、对版本戳、打开原件。
- `portfolio-skill/`：原 Portfolio 的归集、挂载、集周报、手递。跨项目查询调用 `query-skill` 的同一套脚本，不再复制一套认词逻辑。

项目磁盘上的 `ai/`、`ai/portfolio/`、`ai/projects/{名}/ai/` 不改形。Portfolio 仍然只查、不手搓成员正文。

# 3. 能力变更设计

| 类别 | 内容 |
|---|---|
| 保留 | 单项目写入、待办、工作包、计划、合同、风险、拆文件、词库的领域术语语义、联邦目录、只读五条、主题页「已绑」链、升级程序盖戳闸 |
| 新增 | `query_locate.py`：一句话进，JSON 出（路径、是否变了、给人看的指针）。说法表合并脚本。事实源版本戳清单 |
| 修改 | 查询热路径不再调用 `refresh_views.py --all`。`05` 正文迁入 `query-skill`。Portfolio 规则迁入 `portfolio-skill`。Project 路由不再要求另装 Portfolio |
| 删除/弱化 | 可独立安装的 ChronoPM-Portfolio 技能入口（根目录 `SKILL.md` / `skill.json` / 第二个 zip）。双包锁步这句话从 4.0.0 起停止 |
| 可选增强 | 无 |
| 不纳入 | Qoder 商品下架；全量写入收口；新建 `ai/wiki/`；接 Jev 云端接口；升 workspace schema |

# 4. 用户交互流程

1. 用户用口语提问（不提供标准名）。
2. 模型运行 `query-skill/scripts/query_locate.py`，传入项目根和原话。不先跑全量刷新。
3. 脚本只读说法表，命中 1 条则只对该文件做哈希比对。
4. 未变：模型只打开该原件，按原件写结论。JSON 里的指针随结论给出。
5. 已变：脚本重读该文件，更新这一条路径和这一条戳，模型再读原件。
6. 0 条：脚本退出码 2，这一次调用不写说法表、不编结论。为了登记而定位绑定目标时，模型按查询路由打开至多 1 个事实文件。这个「至多 1 个」只限制登记用的绑定定位。回答本身仍按现有 05 §2 的读取预算打开事实文件，不因 0 命中而改成只许打开 1 个。定位到唯一登记名和路径时，本轮收尾运行 `query_locate.py --register`，写入一行（来源=`对话登记`，状态=`pending`，热度初值 1）。确定不了则不登记，不编造登记名。
7. 多条：脚本退出码 3，不登记。模型最多再打开 3 个候选原件。仍不唯一则列出候选。
8. 用户当场纠正：运行 `--correct` 改这一行。用户不纠正：已有行保留。不另开确认流程。
9. 会话收尾：若本会话有命中，运行一次 `--flush-heat`，只改热度与最近命中。命中当时不写说法表。
10. 结论若还引用了命中文件以外的原件：`changed` 只描述命中的那一个文件。其余文件以本次打开的原文为准，不承诺它们的戳。
11. 跨项目问题走 `portfolio-skill` 路由，对每个相关成员项目调用同一步骤 2。不读集层周报缓存当答案。

写入日报、待办、会议的交互不变。写完之后仍可跑 `scripts/refresh_views.py` 做视图重建。这一步不在提问热路径上。

不给 `refresh_views.py` 增加 `--read-only` 或 `--query-fast-path`。查询不调用它。它仍然负责写入之后的视图和全量指纹。提问变快靠 `query_locate.py` 只哈希命中的那一个文件，不靠把 `collect_facts` 改成先遍历目录找变化。`.state.json` 缺失或损坏时，定位脚本仍只哈希这一份，`stamp_prev` 为空，`changed` 为真，然后读原件。不因此改走全库。

# 5. 输入输出规范

`query_locate.py` 参数：

- `--project-root` 成员项目根（其下直接有 `ai/`）。集根拒绝，退出码 4。
- `--text` 用户原话。

另支持四个写子命令，写前重读全表，用临时文件替换：

- `--register`：说法、登记名、路径。来源固定 `对话登记`，状态固定 `pending`，热度 1。路径为空则拒绝。已有同一「说法 + 登记名」行则不新增。
- `--correct`：按说法改登记名和路径，来源改为 `用户纠正`，状态改为 `confirmed`。
- `--flush-heat`：只增加热度、更新最近命中。不改登记名、路径、状态。
- `--fill-path`：只给已有行补空路径。条件是该说法恰好一行且路径为空，传入路径唯一。不改登记名、状态、热度、来源。路径已有则原样退出 0。多行则退出 3，不写。

stdout 只许是一份 JSON，字段：

| 字段 | 含义 |
|---|---|
| `hits` | 列表。每项含 `path`（相对 `ai/`）、`id`、`speech`、`canonical`、`changed`（bool）、`stamp_prev`、`stamp_now` |
| `evidence` | 与 hit 对齐。`file`、`section`、`req_id`、`source_pointer`、`doc_link`、`wp_id`、`changelog_tail`。文件里没有的键写 `null`，禁止编造 |
| `ambiguous` | 命中数不是 1 时为 true |
| `candidate_count` | 整数 |

退出码：`0` 唯一命中；`2` 无命中；`3` 多命中；`4` 根路径不合法；`1` 说法表或戳文件损坏。

脚本不输出给用户看的句子。句子由模型读原件后写。

说法表文件仍是 `ai/context/domain-glossary.md` 的「## 1. 术语映射表」。不另建第二份别名文件。目标列 13 个，必须含路径列和状态列：

`编号 | 说法 | 登记名 | 路径 | 类别 | context_hint | 状态 | 来源 | 热度 | 首次出现 | 最近命中 | updated | 备注`

路径相对成员项目 `ai/`。纯术语行允许路径为空。查询时路径为空，则再用登记名对工作包名、需求标题做一次精确匹配。唯一命中时调用 `--fill-path` 把路径写回该行。不另用 `--register` 做这件事。

热度与最近命中的变更不使说法表的版本戳失效。`fact_stamps` 对这个文件哈希时，先去掉这两列再计算。

查询轮模型不得手改此文件。能写它的只有 `query_locate.py` 的四个子命令、`migrate_workspace.py` 的合并、`refresh_views.py` 的废弃指向修正。同一工作区同一时刻只许一个写方。

# 6. Skill 语法 / 配置 / 提示词设计

- `query-skill/CAPABILITY.md` 声明：不是独立技能，禁止命名为 `SKILL.md`。
- `query-skill/references/query-rules.md` 承接现在的 `references/05-query-rules.md`。文首硬步骤改为调用 `query_locate.py`。删除「每一次查询都跑 `refresh_views.py --all`」。迁入正文必须写上两条收尾：有命中则会话结束运行 `--flush-heat`；0 命中且绑定成功则收尾运行 `--register`。原 §1.5「查询轮禁止写词库」改为：「查询轮模型不得手改说法表；登记、纠正、补路径、加热度只经 `query_locate.py`」。
- `references/05-query-rules.md` 只留指针，指向 `query-skill/references/query-rules.md`。不保留第二份正文。
- `SKILL.md` 简单查询行改为加载 `query-skill/references/query-rules.md`。
- `portfolio-skill/CAPABILITY.md` 同样禁止 `SKILL.md`。原 `ChronoPM-Portfolio/references/*.md` 原样迁入 `portfolio-skill/references/`。
- `SKILL.md` 里「请安装 ChronoPM-Portfolio」改为加载 `portfolio-skill` 对应规则。
- `skill.json` description 去掉「请安装 ChronoPM-Portfolio」。集层触发词写进 Project 这一份 description。
- `pack.py` 不再因发现兄弟目录 `ChronoPM-Portfolio/SKILL.md` 而打第二个 zip。
- 规则里凡是「认词、找文件、判断变没变」的句子，改成「运行某脚本，服从它的 JSON」。推导结论的句子留在规则里。
- 不调用 Jev HTTP API。借用的只是形状：状态（说法表 + 文件戳）加类型化问题（哪条路径、变了没有），答案是 JSON。

# 7. 文件级改动清单

| 文件路径 | 操作类型 | 修改内容 | 修改原因 | 是否必须 | 优先级 | 风险等级 | 是否需 B 复核 |
|---|---|---|---|---|---|---|---|
| `ChronoPM-Project/query-skill/CAPABILITY.md` | 新增 | 能力目录声明 | 查询与拆文件同一形态 | 是 | P0 | 低 | 是 |
| `ChronoPM-Project/query-skill/references/query-rules.md` | 新增（自 05 迁入） | 热路径改为 `query_locate.py`。正文含收尾 `--flush-heat`，以及 0 命中绑定成功后的 `--register`。回答的读取预算仍按原 §2 | 查询正文归位，登记和热度在运行时发生 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/query-skill/scripts/query_locate.py` | 新增 | 说法匹配 + 单文件对戳 + 指针抽出 + `--fill-path` | 热路径程序化 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/references/05-query-rules.md` | 改为指针 | 只保留新路径。迁入正文改写 §1.5，并写入上述两条收尾 | 避免两份正文，并去掉与登记冲突的禁写句 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/SKILL.md` | 修改路由、描述与 §2 集根逻辑 | 见下方「集根改写」。不只改 description | 删掉独立包之后，集根不能再要求另装 Portfolio | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/skill.json` | 修改 description | 写入集层触发词，去掉「另装 Portfolio」 | 市场只看见一个技能 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/portfolio-skill/**` | 自 `ChronoPM-Portfolio/` 迁入 | 规则、模板、CAPABILITY.md；不带 `SKILL.md`。正文中的「本包」「须同时安装」改为「本能力目录，由 ChronoPM-Project 加载」 | 合并且口径一致 | 是 | P0 | 高 | 是 |
| `ChronoPM-Portfolio/` 整树 | 迁入校验后删除 | 含 references、templates、VERSION、CHANGELOG、governance。不只删 SKILL.md 与 skill.json。回滚从 `baselines/3.30.3/ChronoPM-Portfolio` 找回 | 仓库根不再被扫成第二个技能 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/scripts/migrate_workspace.py` | 修改 | 按现有 `VERSION_CAPABILITIES` 与 `needs_v390` 这种版本块接入 4.0.0。没有名为 MIGRATIONS 的字典。失败不盖戳 | 迁移引擎在此文件 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/scripts/enforce_workspace_upgrade.py` | 修改 | 只调度到 migrate 的 4.0.0 步骤，不在此文件实现合并 | 入口与引擎分开 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/scripts/sync_version.py` | 修改 | 4.0.0 起若 Portfolio 根已无 `SKILL.md`，跳过锁步，不报错 | 单包后锁步会空转或报错 | 是 | P0 | 高 | 是 |
| `governance-shared/scripts/audit_release.py` | 修改 | 断言 13 改为单包。删除 `PORTFOLIO` 常量（约 L51）和文件头第 13 条双包注释（约 L29–30）。4.0.0 基线只含 Project 树 | 常量留着会继续要求已删除的目录 | 是 | P0 | 高 | 是 |
| `README.md`、`README.en.md` | 修改 | 安装与发布物只保留 Project 一个 zip。集层写明在包内 `portfolio-skill/` | 现有双包指引会过时 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/assets/templates/domain-glossary-template.md` | 修改 | 第 1 表改为第 5 节的 13 列。纠错表与待确认表改为「已并入第 1 表」 | 新项目否则仍生成旧 11 列 | 是 | P0 | 高 | 是 |
| `tools/pack-skill/scripts/pack.ps1` | 修改 | 去掉伴生包注释与第二包防呆。`query-skill/`、`portfolio-skill/` 不得进入排除目录 | 排除数组以本文件为准 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/scripts/refresh_views.py` | 修改 | 继续负责写入后的视图重建；不再被查询热路径调用；别名写入改为调用说法表同一实现 | 避免两套别名 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/references/17-domain-glossary-rules.md` | 修改全文中的表结构与写入句 | 第 1 表改为 13 列。§6.1、§8.1、pending→confirmed、纠错表、候选表改为：权威只在第 1 表；模型不得手写；脚本可登记。范围枚举仍只读来源=`词库` 且状态=`confirmed` | 与模板、脚本三层一致 | 是 | P0 | 高 | 是 |
| `ChronoPM-Project/references/06-file-rules.md` | 修改 | §2.1 补上 `registers/scope-register.md`；集层路径改指向 `portfolio-skill` | 事实源清单与代码对齐 | 是 | P0 | 中 | 是 |
| `ChronoPM-Project/SKILL_BLUEPRINT.md` | 修改架构段 | 4.0.0 改为单包加 `query-skill/`、`portfolio-skill/`。保留「不建 `ai/wiki/`」。CHANGELOG 的 Blueprint Impact 标 full | 3.0.0 双包描述会过时。发布审计不检查这段散文 | 是 | P1 | 低 | 否 |
| `tools/pack-skill/scripts/pack.py` | 修改 | 去掉伴生包第二 zip | 只发 Project | 是 | P0 | 中 | 是 |
| `governance/migrations/upgrade-to-4.0.0.md` | 执行阶段才新建 | 施工清单含「工作区存量」节 | 16 号 §2.1b | 是 | P0 | 高 | 是 |
| 回归用例 | 执行阶段追加 | 见 AP-5 | 热路径与存量闸 | 是 | P0 | 中 | 是 |

执行阶段才写 CR、IA、CHANGELOG、基线。本草稿不写。

## 7.1 集根改写（SKILL.md）

`SKILL.md` §2 第（1）（3）句现在写着：集根上的投喂、日报、入库、混报、进度表和跨项目查询交给 ChronoPM-Portfolio；没装就提示到技能市场安装。独立包删除后这三句会指向不存在的技能。

改写范围：

- front matter 的 description 去掉「请安装并调用 ChronoPM-Portfolio」。集层触发词留在本技能。
- §1 的 v3.0.0 句、§2（1）（2）（3）、§5.3、路由表里「已删除路由：改用 Portfolio」、§15 的 09 号指针、底线 12：凡是「另装 / 调用 ChronoPM-Portfolio」都改为加载 `portfolio-skill/references/` 里对应规则。
- 集根检测不变：当前根同时有 `ai/portfolio/` 与 `ai/projects/` 时，仍禁止把集根当单项目写入，仍禁止把某个 `projects/{名}` 当成集根落盘。
- 集根上的投喂、日报、入库、混报、进度表、xlsx/csv、跨项目查询：加载 portfolio-skill 里已迁入的原规则（含原 01 §2.1、§2.2）。包内没有这些文件就报规则缺失。不提示另装一个技能。
- 成员根仍只写该根。P-HANDOFF 的调用关系不变：集层规则发起，写过程仍进 Project，`--project-root` 仍是成员根。只读五条不放宽。
- §5.3 本项目查询改为加载 `query-skill/references/query-rules.md`，不再每次先跑 `refresh_views.py --all`。跨项目查询走 portfolio-skill，由它按成员根调用 `query_locate.py`。
- §5.1b 的 P-VIEWS 留在写入之后和显式重建，查询不调用。

## 7.2 迁移入口（migrate_workspace.py）

这个文件没有名为 `MIGRATIONS` 的字典，也没有按能力名自动调用函数的表。版本表是 `VERSION_CAPABILITIES`。`get_capabilities_since()` 从工作区当前 `skillVersion` 之后把表截出来，供打印和缺目录检查。真正干活的是 `migrate_workspace()` 里一截一截的 `needs_v390` 这类判断，然后在 `stamp_skill_version` 之前调用 `ensure_stock_compiled`。

4.0.0 按这个结构接，不新造分派表：

1. 在 `VERSION_CAPABILITIES` 末尾加一条：`version` = `4.0.0`，`schema` = `0.17.0`，`capabilities` = `speech_table_merge` 与 `fact_stamps_init`，`new_dirs` 与 `new_files` 都为空。这两个名字只用于检测打印。
2. 在 `migrate_workspace()` 里、调用 `stamp_skill_version` 之前，加 `needs_v400`：目标版本 ≥ 4.0.0，且工作区 `skillVersion` < 4.0.0，或者第 1 表还不是 13 列，或者 `fact_stamps` 没覆盖应打戳的文件。
3. 成员根（`mode=single`）在这个分支调用说法表合并和戳初始化。任一失败就 return，不盖戳。
4. 集根（`mode=portfolio`）不在集根建说法表，也不写 `fact_stamps`。只在各成员已经合并成功之后重写 `glossary-index.md` 的指针。成员未完成则集根也不盖戳。
5. 工作区版本已经等于 4.0.0 时，现有代码会先跑存量检查再返回。这个检查必须包含第 2 步的同一套条件。表没并完不能因为版本号相同就当成功。

# 8. 数据、索引、分块与扩展性设计

涉及项目里已有的 `ai/context/domain-glossary.md` 和 `ai/.state.json`。不新增必填目录，因此 schema 保持 0.17.0。

说法表就是词库文件第 1 表。升级时并入的别名来自 `context/active-entities.json` 的 `alias_index`（`refresh_views.py` 写在这里；`.state.json` 没有这个键）、`brain.md` 别名短表，以及 `refresh_views.py` 解析工作包时得到的名称、编号、功能点、supersedes。工作包 frontmatter 没有 `aliases` 键，合并不得去读这个键。并完之后，查询只读第 1 表。`brain.md` 与 `active-entities.json` 的 `alias_index` 改为由第 1 表生成的投影，脚本可覆盖，不再当第二份权威。`.state.json` 只追加 `fact_stamps`，不存放别名。

单文件膨胀：沿用 17 号已有的词库分片阈值。热度只排序，不删行。摘要仍禁止超过 200 字；说法表存的是说法和登记名，不存文件正文。

版本戳放在 `.state.json` 的 `fact_stamps` 映射里：`相对路径 → sha256`。升级时走一遍下面的权威清单，写成初始戳。之后查询只重算被命中的那一个文件。

索引深度 2：说法 → 登记名与路径。不超过 3 层。

# 8.1 事实源清单与变更状态

「变更状态」在本方案里是机器戳：该文件的 sha256 与 `fact_stamps` 里上次记录是否相同。脚本计算，不要求人在每个文件手写 `updated`。

给人看的依据不是另一套状态。查询 JSON 的 `evidence` 从该文件已有字段抽出。3.30.3 已禁止新建 `ai/wiki/`，也禁止 Obsidian `[[wikilink]]`。本方案继续禁止。已有指针是：

- 需求上的「来源指针」「原型/文档链接」
- 主题页「已绑」里的工作包编号
- 事实源文件底部 Change Log（06 §8：操作类型、来源、确认人）

这三样一起构成给人看的链。文件里没有的环节写 `null`。

## 权威事实源（答案必须来自原件；全部打机器戳）

| # | 路径（相对成员项目 `ai/`） | 回答什么 | 机器戳 | 给人看的指针 |
|---|---|---|---|---|
| 1 | `todos/{date}/{owner}.md` | 谁的待办、执行人、工作日志、人员流转 §0.5、能耗 §0.6 | 要 | 待办号、WP Ref、Change Log 末行 |
| 2 | `todos/{date}/_index.md` | 花名册 §1、当日参与 §3、TD 缩写 §6 | 要 | 节号 |
| 3 | `wps/WP-*.md` | 工作包正文、分工矩阵、功能点 | 要 | WP 号、§2 需求编号、Change Log 末行 |
| 4 | `plans/PLAN-*.md` | 计划与阶段 | 要 | PLAN 号、§3 的 WP 号 |
| 5 | `project-info/progress-plan.md` | 进度计划说明 | 要 | 路径 |
| 6 | `project-info/budget.md` | 预算 | 要 | 路径 |
| 7 | `requirements/requirement-register.md`（及分片） | 需求正文 | 要 | 来源指针、原型/文档链接、工作包编号 |
| 8 | `requirements/contract-register.md` | 合同作用域 | 要 | 合同号、来源 |
| 9 | `requirements/change-log.md` | 需求变更记录 | 要 | 行本身 |
| 10 | `requirements/canonical/CAN-*.md` | 归并后的需求 | 要 | CAN 号、来源 ATOM |
| 11 | `requirements/atoms/{category}.md` 与 `atoms/` 分片 | 条款证据 | 要 | ATOM 的 source_ref |
| 12 | `requirements/sources/{编号}/meta.md` | 源文档身份 | 要 | 源编号 |
| 13 | `requirements/sources/{编号}/ledger.md` | 拆解台账 | 要 | 源编号 |
| 14 | `requirements/sources/{编号}/atoms.md` 或 `atoms/` | 该源的条款 | 要 | 条款号、页码 |
| 15 | `requirements/sources/{编号}/rows.md` | 弱结构抽出行 | 要 | 批次与行号 |
| 16 | `requirements/sources/{编号}/original.*` | 原件副本 | 要 | 路径。不把原件正文抄进说法表 |
| 17 | `requirements/sources/{编号}/_digest.md` | 单源主题页 | 要 | 「已绑」列。过期时改读 atoms，沿用 3.30 的 `source_digest_status` |
| 18 | `registers/scope-register.md` | 上线范围、批次、纳入 | 要 | 行号、WP、PLAN。06 §2.1 清单目前漏了此文件，本版补上 |
| 18a | `requirements/source-type-registry.md` | 源类型与弱表列如何对上槽位 | 要 | 类型编号。06 §2.1 已列此文件 |
| 19 | `risks/risk-register.md` | 风险 | 要 | 风险号、Change Log 末行 |
| 20 | `issues/issue-register.md` | 问题 | 要 | 问题号、Change Log 末行 |
| 21 | `decisions/decision-log.md` | 已记录决策 | 要 | 决策号 |
| 22 | `pm-decisions.md` | 待裁定 | 要 | 块号。查询仍只先读开放行计数，规则见 05 §1a |
| 23 | `context/domain-glossary.md` | 说法 → 登记名（合并后的唯一说法表） | 要。哈希时去掉热度与最近命中两列，这两列变化不算源已变 | 行的路径、来源、状态 |
| 24 | `context/project-brief.md` | 项目是谁、归属 | 要 | 路径。06 已标明它是事实源 |
| 25 | `context/project-context.md` | 项目背景 | 要 | 路径 |
| 26 | `context/pm-profile.md` | 这个 PM 的偏好 | 要 | 偏好编号。pending 不当 confirmed 用 |

## 集层（目录不变；Portfolio 仍然不把这些当成成员进度的事实源）

| # | 路径（相对集根 `ai/`） | 回答什么 | 机器戳 | 给人看的指针 |
|---|---|---|---|---|
| 27 | `portfolio/context/project-index.md` | 有哪些成员 | 不适用。集层查询直读原件，不建戳、不对戳 | 成员名与管理路径 |
| 28 | `portfolio/context/glossary-index.md` | 术语在哪个成员 | 不适用。集层查询直读原件，不建戳、不对戳 | 只存指针。升级后由各成员说法表重新生成，不抄全文 |
| 29 | `portfolio/context/ingest-maps.md` | 弱表的列怎么对上槽位 | 不适用。集层查询直读原件，不建戳、不对戳 | 指纹与列映射 |
| 30 | `portfolio/resources/shared-resource-index.md` | 某人还在哪些项目。落盘只许静态索引元数据（姓名、项目指针、共享状态导航）。可用性、排期摘要是查询时现算的动态视图，不写入此文件 | 不适用。集层查询直读原件，不建戳、不对戳 | 姓名 + 项目指针 |
| 31 | `portfolio/resources/transfer-index.md` | 借调指针 | 不适用。集层查询直读原件，不建戳、不对戳 | Transfer ID |
| 32 | `portfolio/reports/ingest/{batch}/rows.md` | 这批材料抽出了哪些行 | 不适用。集层查询直读原件，不建戳、不对戳 | 批次路径。进度仍以成员工作包和待办为准 |

成员项目里的第 1–26 项，集层查询通过只读这些文件回答，不在集层复制一份。

## 不是事实源（可以有戳，禁止拿来当答案）

| 路径 | 原因 |
|---|---|
| `wps/_index.md`、`plans/_index.md`、`requirements/_index.md`、`requirements/sources/_index.md`、`registers/_index.md` | 查找加速器。06 写明不是存在性判据 |
| `context/brain.md`、`context/active-entities.json`、`.state.json` | 脚本投影。`.state.json` 只存放戳和指纹 |
| `reports/daily/`、`reports/weekly/`、`reports/timeline/` | 存根。非精确重合的区间要从待办重汇 |
| `meetings/`、`reviews/` | 过程记录。引用会议时可以打开，进度与分工以工作包和待办为准 |
| `logs/ops/`、`logs/journal/` | 06 §2.8 写明过程日志不是事实源。§2.1 虽列了 ops 路径，以 §2.8 为准 |
| `todos/{date}/inbox/`、`backup/` | 草稿与退役。查询禁止当事实源 |
| `requirements/sources/{编号}/parse-log.md`、`figures/` | 过程与佐证图。缺图不健康失败 |
| `requirements/canonical/canonical-index.md`、`requirements/atoms/atom-index.md`、`requirements/atoms/{category}-index.md` | 查找加速器。存在性以 CAN 文件和条款文件为准 |
| `requirements/artifacts/` | 原型压缩截图的对账目录。原件不入库，需求上只留文档链接 |
| `portfolio/reports/` 里除 ingest `rows.md` 以外的周报、建议清单 | 派生物，带 `generated_from`。不得当后续查询数据源 |

# 8.2 工作区存量（执行时写入 upgrade-to，缺了不得开工）

谁执行：第 7.2 节的 `needs_v400`。`enforce_workspace_upgrade.py` 只负责调用 `migrate_workspace()`。每个成员项目根跑一次。集根不编主题页，也不写 `fact_stamps`；各成员合并成功后才重写 `glossary-index.md` 的指针。

旧 11 列到新 13 列，逐列如下。旧号不重编。

| 旧列 | 新列 | 规则 |
|---|---|---|
| 编号 | 编号 | 原样。新行用 `G-{时间戳}` |
| 原词 | 说法 | 原样 |
| 标准词 | 登记名 | 原样 |
| （无） | 路径 | 见下方填充。旧词库行默认空 |
| 类别 | 类别 | 原样，空则 `—` |
| context_hint | context_hint | 原样 |
| 状态 | 状态 | `confirmed` / `pending` 原样。对话登记新行写 `pending` |
| 来源 | 来源 | 旧值原样。并入行另用下表枚举 |
| 命中次数 | 热度 | 整数原样，空为 0 |
| 首次出现 | 首次出现 | 原样。新行为登记日 |
| 最近命中 | 最近命中 | 原样 |
| （无） | updated | 该行最后一次被脚本改写的日期 |
| 备注 | 备注 | 原样 |

第 2 节纠错表、第 3 节待确认表的行并入第 1 表：错误写法或术语 → 说法，正确写法或可能的标准名称 → 登记名，纠错行来源写 `纠错`，待确认行来源写 `待确认`、状态 `pending`。并完后这两节只留一句「已并入第 1 表，禁止再追加」。

说法表合并，不问用户：

1. 读第 1、2、3 表全部行。
2. 读 `context/active-entities.json` 的 `alias_index`（不读 `.state.json` 取别名）、`brain.md` 别名短表。工作包别名复用 `refresh_views.py` 的解析：名称、编号、功能点、supersedes。不读 frontmatter 里不存在的 `aliases` 键，不另写一套解析。
3. 以「说法 + 登记名」为键求并集。已有行不删除。
4. 同一说法指向两个登记名：两行都留，来源记 `冲突`。脚本不挑选赢家。
5. 来源取值：`词库`、`别名表`、`工作包`、`脑图`、`标题`、`纠错`、`待确认`、`对话登记`、`用户纠正`、`冲突`。旧行已有来源则保留。查询解析使用全部状态不是 `废弃` 的行。
6. 路径：alias 自带 `path` 则用它。`type=wp` 时在 `wps/` 找文件名以该 id 开头的唯一文件。`type=plan` 时同样处理 `plans/`。`type=req` 时路径为 `requirements/requirement-register.md`。`type=person` 路径留空。其余留空。旧词库行没有文件指针，路径留空是对的。不根据来源把路径写成「对话」「文件」或「系统」。那不是 `ai/` 下的路径，定位脚本会去开一个不存在的文件。之后查询用登记名对工作包名和需求标题做精确匹配，唯一命中才 `--fill-path`。
7. 工作包 `effect=废弃` 时，按 `refresh_views.py` 的 `_successor_id` 规则把该行的登记名和路径改到后继包。无后继则状态写 `废弃`，路径保留，备注追加「无后继」。
8. 写出的键必须覆盖全部输入键。少一键即非 0。第二遍不得制造重复行。

版本戳初始化：只处理成员项目表里机器戳为「要」的文件，算 sha256，写入该成员 `.state.json` 的 `fact_stamps`。集层第 27–32 行不写入。说法表先去掉热度与最近命中两列再哈希。文件不存在则跳过该键。清单内文件读失败则失败。

完成闸：说法表合并成功，且 `fact_stamps` 已写入，且 3.30.3 已有的「已绑」闸仍成功，才允许 `stamp_skill_version` 把该工作区写成 4.0.0。只改模板或只改版本文件不算完成。别名键没并进则禁止盖戳，禁止写「可以投入使用」。

范围登记枚举仍然只消费来源为 `词库` 且状态为 `confirmed` 的行，直到第 19 节第 1 点被用户改口。对话登记行状态是 `pending`、来源是 `对话登记`，查询会用，枚举不用。这是同一张表上的过滤，不是第二份词库。

# 9. 上下文与输出分块策略

查询轮加载：`query-skill/references/query-rules.md` 与脚本 JSON。不加载 `reply-norm-skill` 全文，不加载 00 全文，不加载 Portfolio 全文。

跨项目轮才加载 `portfolio-skill` 里命中的那一份规则。

方案正文过长时分块只发生在对话里。本周期只有这一个方案文件。

进入共识的是：版本 4.0.0、schema 0.17.0、两个能力目录、一份说法表、热路径不对全库、存量不问用户、不建 wiki 目录。文件路径以本文件第 7 节为准。

# 10. 异常场景处理

| 场景 | 行为 |
|---|---|
| 无 Python 或脚本退出码 1 | 不把旧 brain 当答案。定向打开路由表指定的 1 个事实文件，声明 as-of。不跑全量刷新 |
| 退出码 2 无命中 | 这一次调用不写表。模型按路由打开至多 1 个文件。唯一绑定成功则收尾 `--register`；绑定失败则不登记 |
| 退出码 3 多命中 | 最多打开 3 个原件。仍不唯一则告诉用户有哪几个候选 |
| 退出码 4 把集根当项目根 | 拒绝。集层按成员根逐个调用 |
| 戳不一致 | 只重读该文件并更新该条戳。不刷新其他文件 |
| 说法表合并不完整 | 升级失败，不盖戳 |
| 用户纠正说法 | 脚本改行。下一次查询用新行 |
| 手改了工作包但说法表路径还指着它 | 下一次问到该文件时哈希对不上，重读原件。这是本轮对「未收口全部写入口」的兜底 |

# 11. 风险与边界

见第 12.5 节与第 18 节。边界：本方案不改变联邦目录，不让 Portfolio 获得手搓成员正文的权力，不把派生索引当成事实源。

# 12. 兼容旧能力方式

- 工作区目录与 3.30.3 相同，旧项目不必搬目录。
- 成员与集根的 `.skill-version.json` 里 `skillName` 保持原值。盖戳只改版本号，两种角色都由 Project 4.0.0 这一个技能来做。
- 旧词库行全部保留。别名并入后旧叫法仍能命中。
- `refresh_views.py --all` 命令还在，供写入之后和人工重建。查询规则不再调用它。
- 主题页过期仍读 atoms。`source_digest_status` 不并入说法表。
- 无 Python 时的降级是直读路由文件，不是拒绝回答。

# 12.5 方案影响与必要性评估

## 13.1 影响范围

| 影响维度 | 是否受影响 | 具体影响 | 程度 |
|---|---|---|---|
| 现有能力 | 是 | 查询热路径从全量刷新改为单文件对戳。集层从独立技能变为能力目录 | 高 |
| 现有文件 | 是 | 05 迁走，Portfolio 根入口删除，词库文件被升级脚本重写 | 高 |
| 输入输出 | 是 | 查询前多一次脚本 JSON。用户仍用口语，不要求报标准名 | 中 |
| 交互流程 | 部分 | 写入流程不变。查询少一次全量等待 | 中 |
| 数据结构 | 是 | 词库增加来源与热度列；`.state.json` 增加 `fact_stamps`。无新必填目录 | 中 |
| 上下文 | 是 | 查询轮不再为了保真去读全库 | 高 |
| 模块依赖 | 是 | Portfolio 查询改为调用 query-skill 脚本 | 高 |
| 性能 | 是 | 见下方性能说明 | 高 |
| 触发词 | 是 | 集层词留在 Project 的 description 里 | 中 |

## 性能说明（为何「先判断每个文件变没变」会慢）

现在 `05` §0 要求每一次提问都执行 `refresh_views.py --all`。`run()` 在发现指纹没变、决定不写盘之前，已经执行了 `collect_facts`：工作包、当天全部待办、计划、风险、问题、需求、词库、范围表、每个源的 `meta.md` 都要读入并算哈希。省下的只是写索引，读完全库已经发生。文件一多，这一步就是几分钟，和问题是不是一句「谁做后端」无关。

若新方案改成「先遍历全部事实源，判断哪些变了，再决定读谁」，遍历本身又把目录走遍，提问时的开销回到接近全量读取。本方案不采用这种判断方式。

本方案的提问步骤只做两小步：在说法表里查这一句话（只读一个词库文件），然后只对命中的那一个路径算哈希。没被这句话点到的文件，哪怕刚被改过，这一问也不打开。大批量修改不会让这一问变回全量解析。全量算戳只发生在升级脚本那一次，以及以后写入路径主动重建视图的时候。

## 13.2 历史使用体验

部分改变。提问更快，仍然读原件。只安装过 Portfolio、没有 Project 的用法不再存在，因为不再发行那个包。已经按两个技能建好的项目目录不用改。总体是增强查询，发行入口收成一个。

## 13.3 其他模块

受影响：`SKILL.md` 路由、`refresh_views.py`、`migrate_workspace.py`、`sync_version.py`、`audit_release.py`、README 两份、词库模板、17 号、06 号、打包脚本。`enforce_workspace_upgrade.py` 只增加调度。不改变拆文件六件套、不改变待办结转三问、不改变主题页编译程序的盖戳条件（在其上再加说法表闸）。

## 13.4 必要性

必须升级。不改则每次提问继续付全库解析，且 Portfolio 仍是可单独安装的技能。收益是提问只碰命中文件，旧项目的说法并进一张表。成本是查询规则搬迁和一次存量脚本。结论：必须升级。

## 13.5 匹配度

符合「单项目读写 + 跨项目只读」的现有定位。真实场景来自 SG-20260923-001 和用户关于 Qoder 上单独下载 Portfolio 无法检索的说明。本方案不处理商店下架。没有为了合并去改工作区形状。

## 13.6 综合意见

支持按本文件执行设计。需要用户稍后讨论的两点不在本版执行范围里。取舍：手改原件要到下一次问到该文件才被戳发现，换来不必在 4.0.0 重写全部写入规则。

# 12.6 方案关键断言与放行门槛声明

## 关键断言清单

| 关键断言 | 依据 | 若被证伪 |
|---|---|---|
| 查询热路径当前强制 `refresh_views.py --all`，且指纹未变时仍已跑过 `collect_facts` | `05-query-rules.md` §0；`refresh_views.py` `run()` 先采集再判断跳过写盘 | 阻塞 |
| 词库、`alias_index`、brain 别名、WP aliases 是分开的入口 | `17` §8.1、`refresh_views.py` `build_entities()`、`05` §0 读 brain | 阻塞 |
| 查询轮禁止把生词写进词库 confirmed | `05` §1.5、`17` §8.1 | 阻塞。本方案改为脚本写同一张表，B 需核对没有第二份权威 |
| 独立 Portfolio 由 `pack.py` 发现 `SKILL.md` 后打第二 zip | `pack.py` 文件头与 `find_companion()` | 阻塞 |
| 能力目录的既有形态是 `CAPABILITY.md` 且禁止 `SKILL.md` | `source-split-skill/CAPABILITY.md` | 阻塞 |
| 3.30.3 禁止新建 `ai/wiki/` | `SKILL_BLUEPRINT.md` 3.30 决策；`test_ue017_no_wiki_dir` | 阻塞 |
| 联邦目录是 `ai/portfolio/` + `ai/projects/{名}/ai/`，本方案不改这些路径 | Portfolio `SKILL.md` 目录树；06 §1.2 | 阻塞 |
| 权威事实源以 06 §2.1 为主，且 `scope-register.md` 实际存在但不在 §2.1 列表 | 06 §2.1 与 §7.7 | 非阻塞，本方案补清单 |
| `logs/ops` 被 §2.1 列入又被 §2.8 否定为事实源 | 06 §2.1 与 §2.8 | 非阻塞，本方案以 §2.8 为准 |

## 放行门槛

- 通过-可执行 / 通过-待修订：上表阻塞级断言未被证伪，且无新的阻塞问题。已声明的取舍不构成障碍。
- 修订-需再审：任一阻塞级断言被证伪，或方案把热路径又写回全量刷新，或又出现第二份说法权威，或新建 `ai/wiki/`，或改了联邦目录。
- 重做-需再审：方案实质变成两个仍可单独安装的技能，或查询答案改由缓存正文提供。

## 已识别取舍与局限

| 取舍 | 影响 | 缓解 | 是否阻塞 |
|---|---|---|---|
| 用户明确要求说法与词库是一个东西。A 曾反对口语进入范围枚举 | 范围登记若误用口语行，枚举会被污染 | 合并进同一文件、同一个解析函数；范围登记在第 19 节讨论结束前只读 `来源=词库` 且 confirmed 的行 | 否 |
| 用户明确要求本轮不收口全部写入口 | 手改 Markdown 不会立刻改说法表 | 问到该文件时哈希不一致就重读 | 否 |
| 给人看的链使用已有指针和 Change Log，不新建 wiki 目录 | 没有指针的待办行，证据只有路径、待办号、WP Ref | 有的字段才填，没有则为 null | 否 |
| 首次全量戳发生在升级脚本，不发生在每次提问 | 升级时间变长 | 只跑一次；失败不盖戳 | 否 |
| 不处理商店里已发布的 Portfolio 条目 | 商店可能仍显示旧包 | 用户要求本方案不管下架 | 否 |

## 已知遗留

见第 19 节。

# 13. 测试与验收标准

| 编号 | 输入 | 预期 | 类型 |
|---|---|---|---|
| Q-001 | 说法表已有「办理进度 → 某 WP」，该 WP 文件哈希未变 | 脚本退出码 0，只报告这一条路径，`changed=false`。测试替身计数：除词库与该 WP 外无其他事实文件被打开 | positive |
| Q-002 | 同上，但该 WP 哈希已变 | `changed=true`，戳被更新为新哈希。其他文件戳不变 | positive |
| Q-003 | 一句话命中 0 条 | 退出码 2，这一次调用不写说法表，不编结论 | negative |
| Q-011 | 退出码 2 之后，用确定的登记名和路径调用 `--register` | 新增一行：来源=`对话登记`，状态=`pending`，路径等于传入值 | positive |
| Q-012 | 废弃工作包有后继，其别名在 alias_index 中 | 合并后该行路径指向后继包，不指向废弃包 | regression |
| Q-013 | 只跑 `--flush-heat` | 热度增加。`fact_stamps` 里说法表的有效戳不变 | regression |
| Q-004 | 一句话命中 2 条 | 退出码 3，`ambiguous=true` | negative |
| Q-005 | `--project-root` 指向同时含 `portfolio/` 与 `projects/` 的集根 | 退出码 4 | negative |
| Q-006 | 旧项目同时有词库行、`alias_index`、WP aliases | 升级后三处的键都在 `domain-glossary.md`，第二遍运行行数不增加 | regression |
| Q-007 | 合并故意少写一行 | 进程非 0，`.skill-version.json` 的 skillVersion 仍不是 4.0.0 | negative |
| Q-008 | 打包 Project | zip 内无 `ChronoPM-Portfolio/SKILL.md`，无第二个 Portfolio zip；含 `query-skill/` 与 `portfolio-skill/CAPABILITY.md` | regression |
| Q-009 | 查询规则全文 | 不包含每次查询调用 `refresh_views.py --all` | regression |
| Q-010 | 主题页已绑仍空且无登记边 | 沿用 3.30.3：该闸失败则不盖戳 | regression |

现有 1028 条回归在执行时重跑。阻断项是 Q-001～Q-013，加上 3.30.3 的已绑闸，以及被审版本为 4.0.0 时的单包审计。新的总条数在执行时按套件实数写入，不在本草稿里预写一个假总数。

验收口径：同类口语查询的程序步骤只碰说法表和命中文件；结论句子能指回原件路径；旧项目升级后说法表包含升级前的词库行和别名键。

# 14. 全量改动项清单

| 编号 | 类型 | 模块 | 说明 | 原因 | 影响 | 风险 | 必须 |
|---|---|---|---|---|---|---|---|
| C1 | 搬迁 | 查询 | 05 与新脚本进入 `query-skill/` | 与拆文件同一形态 | 路由 | 高 | 是 |
| C2 | 搬迁 | 集层 | Portfolio 进入 `portfolio-skill/`，删除独立入口 | 只发一个技能 | 打包、触发词 | 高 | 是 |
| C3 | 脚本 | 说法 | 升级时合并词库与各类别名 | 旧数据已经分开 | 全部旧项目 | 高 | 是 |
| C4 | 脚本 | 戳 | 权威清单初始化 `fact_stamps`；查询只对一条 | 避免每次全库 | 查询性能 | 高 | 是 |
| C5 | 规则 | 证据 | JSON 抽出已有指针与 Change Log 末行 | 给人看的链与机器戳一起做 | 查询输出 | 中 | 是 |
| C6 | 规则 | 06 | 补 scope-register；集层改口 | 清单与现实一致 | 文件规则 | 中 | 是 |
| C7 | 打包 | pack | 停止第二 zip | 用户要求不再发 Portfolio 包 | 发布物 | 中 | 是 |
| C8 | 版本 | 4.0.0 | Major。schema 仍 0.17.0 | 用户指定 4.0.0；目录形状不变 | 版本线 | 中 | 是 |
| C9 | 发布链 | audit、sync_version、README×2、pack.ps1、模板 | 单包审计、停止锁步、安装指引、13 列模板 | B1-5：否则发布必失败 | 发布 | 高 | 是 |
| C10 | 迁移引擎 | migrate_workspace.py | 合并与盖戳闸放在此文件 | B1-1/B1-5：enforce 只调度 | 存量 | 高 | 是 |

# 15. 需求实现偏差验证

| 原始需求点 | 理解 | 设计 | 完全覆盖 | 有扩展 | 还需用户确认 | 需 B 复核 |
|---|---|---|---|---|---|---|
| 查询约 1 分钟且读原件 | 热路径不再全库解析 | `query_locate.py` 只碰命中文件，模型读原件 | 是 | 否 | 否 | 是 |
| 口语说法不丢、不靠用户报标准名；0 命中且定位成功后无感登记 | 并进第 1 表；`--register` 在收尾写入 | 第 4、5、8.2 节 | 是 | 否 | 否 | 是 |
| 词库和别名是一个东西，旧数据要合并且不问用户 | 一张表、升级脚本、失败不盖戳 | 第 8.2 节 | 是 | 否 | 否 | 是 |
| 许多事实源都要有变更状态 | 按清单打机器戳 | 第 8.1 节 | 是 | 否 | 否 | 是 |
| 给人读的证据链本轮要做 | 使用已有指针和 Change Log，不建 wiki 目录 | 第 8.1 节、JSON `evidence` | 是 | 否 | 否 | 是 |
| 查询独立成能力目录 | `query-skill/` | 第 6、7 节 | 是 | 否 | 否 | 是 |
| Portfolio 合并进 Project 文件夹，工作区不变，不再发包 | `portfolio-skill/`，目录树不改 | 第 2、7 节 | 是 | 否 | 否 | 是 |
| 判定用 Python，推导可留文字 | 脚本 JSON + 规则只写推导 | 第 6 节 | 是 | 否 | 否 | 是 |
| 借用 Jev 的模式 | 状态 + 类型化是否/选择，本地脚本 | 不接云端 | 是 | 否 | 否 | 是 |
| 版本 4.0.0 | Major，schema 不动 | AP-7 | 是 | 否 | 否 | 是 |
| 下架商店里的旧包 | 用户要求不管 | 不纳入 | 是 | 否 | 否 | 否 |
| 两处反对稍后讨论 | 枚举过滤与写入口收口 | 第 19 节，不在本版执行 | 是 | 否 | 是，后议 | 是 |

当前方案忠实于已裁决需求：是。目标偏移：否。

# 16. 现有能力扩展优先评估

| 新增需求 | 现有能力 | 扩展方式 | 扩展成本 | 另起一套的成本 | 扩展可行 | 推荐 | 理由 |
|---|---|---|---|---|---|---|---|
| 查询目录化 | `source-split-skill` 形态 + 05 | 搬家，不新写平行路由 | 低 | 高 | 是 | 扩展 | 已有能力目录约定 |
| 集层合并 | Portfolio 规则全文 | 搬进 `portfolio-skill` | 中 | 重写归集 | 是 | 扩展 | 规则可原样搬 |
| 说法合并 | `domain-glossary.md` | 升级脚本并入别名键 | 中 | 新文件会变成第二权威 | 是 | 扩展 | 用户要求一个东西 |
| 单文件对戳 | `refresh_views` 的哈希函数 | 查询脚本复用 `_file_sha`，不在提问时调用 `--all` | 中 | 再写一套哈希 | 是 | 扩展 | 哈希已存在 |
| 给人看的链 | 来源指针、文档链接、已绑、Change Log | 脚本抽出 | 低 | 新建 wiki 目录已被 3.30.3 否决 | 是 | 扩展 | 禁止新目录 |

复杂度：

| 指标 | 升级前 | 新增 | 移走或收成指针 | 升级后 | 变化率 | 超阈值 |
|---|---|---|---|---|---|---|
| Project Markdown | 126 | Portfolio 规则迁入约 44，加 2 个 CAPABILITY | 根上 Portfolio 不再单独存在；05 变为指针 | 包内增加，仓库合计基本持平 | 仓库净增低于 20% | 否 |
| Python | Project 22 | `query_locate.py` 1 个；合并逻辑放进已有升级脚本 | 无第二套刷新脚本 | +1 | 低于 20% | 否 |
| 规则文件 | 05 为 559 行查询正文 | 正文迁入能力目录 | 原路径只留指针，不保留第二份 | 规则条数不双份 | 低于 15% | 否 |
| 对外技能数 | 2 | 0 | 1 个入口删除 | 1 | — | 否 |

补偿：删除独立技能入口和第二 zip，避免两份查询正文。发布链触点（README×2、audit、sync_version、migrate、模板、pack.ps1）是修改已有文件，不另增一套规则正文。

# 17. 索引合理性评估

| 评估项 | 当前 | 本次 | 结论 | 要调整 |
|---|---|---|---|---|
| 深度 | 说法在 brain / 词库 / alias 三处 | 说法表一层，路径在行内 | 2 层，未超过 3 | 是，收成一处 |
| 粒度 | 索引行指向整个 WP 或计划 | 保持文件级，不把分工矩阵拆成格级索引 | 适中 | 否 |
| 覆盖 | 别名覆盖取决于上次全量刷新 | 升级脚本按清单补戳；说法按并集补行 | 升级完成即覆盖 | 是 |
| 一致性 | 三处说法可能不一致 | 权威只剩词库文件 | 投影可覆盖 | 是 |
| 元数据 | brain 短表没有「变没变」 | 第 1 表 13 列，含路径、登记名、来源、状态、热度；戳在 `fact_stamps` | 与第 5 节同一列结构 | 是 |
| 可导航 | 现场推理 | 原话 → 说法表 → 1 个文件，然后读原件 | ≤3 跳 | 是 |
| 膨胀 | 全量刷新产物大 | 说法表只增不删，热度排序；正文不进表 | 沿用 17 号分片 | 是 |

优化：不建新的查找文件。旧 `alias_index` 降为投影。

# 18. 联动更新设计

| 源 | 依赖方 | 类型 | 触发 | 当前 | 及时 | 旧数据风险 |
|---|---|---|---|---|---|---|
| 事实源文件 | `fact_stamps` 中该键 | 状态同步 | 查询命中或升级初始化 | 全库指纹 | 命中时对一条 | 手改后要问到才发现 |
| 说法表 | `query_locate.py` | 索引依赖 | 读表 | 三处入口 | 只读这一份 | 合并失败则不盖戳 |
| 成员说法表 | `glossary-index.md` | 派生 | 成员合并成功之后 | 收编时刷新 | 升级末尾一次 | 指针仍指向成员文件，不抄正文 |
| `active-entities.json` 的 alias_index、工作包 aliases | 说法表第 1 表 | 数据引用 | 仅升级合并 | 刷新时写进 active-entities.json | 升级时并入第 1 表 | 之后第 1 表为权威；active-entities 只是投影 |
| 写入流程 | `refresh_views.py` | 派生计算 | 写入之后 | 每次查询也跑 | 本方案把查询调用去掉 | 视图可能比重建更旧；查询不读视图当答案 |

| 场景 | 顺序 | 每步更新什么 | 原子性 | 失败回退 |
|---|---|---|---|---|
| 升级一个成员 | 读旧键 → 写说法表临时文件 → 校验键齐全 → 替换原文件 → 写 `fact_stamps` | 说法表与戳 | 替换用临时文件；校验失败不替换 | 保留原词库与原 `.state.json`，不盖戳 |
| 升级集 | 全部成员成功后重写 glossary-index 指针 | 只改指针文件 | 成员失败则不改集层索引 | 集层版本也不盖戳 |
| 一次查询 | 读说法表 → 哈希 1 个命中文件 → 若变了则更新该戳。当时不写热度 | 仅该事实文件的戳 | 单键写回 | 写失败则报告 `changed=true` 且戳未更新，模型仍读原件 |
| 会话收尾加热度 | `--flush-heat` 重读全表 → 只改热度与最近命中 → 原子替换 | 说法表这两列 | 与合并、纠正互斥 | 替换失败则保持原表 |
| 废弃包后继 | `refresh_views.py` 重建投影时只改指向死包的行 | 登记名与路径 | 不新增行、不改热度 | 无后继则标废弃，不删行 |

| 风险 | 条件 | 影响 | 检测 | 缓解 |
|---|---|---|---|---|
| 读到半份说法表 | 替换中断 | 说法变少 | 键数量校验 | 临时文件替换；失败保持原文件。合并、登记、加热度、废弃修正同一时刻只许一个写方 |
| 热度把说法表戳打失效 | 每次命中就改热度 | 只读查询变成写盘，并误判说法表已变 | 命中当时不写；戳哈希去掉热度与最近命中 | Q-013 |
| 索引新、原件旧 | 本方案不允许缓存正文 | 无正文幻读 | 答案必须来自本次打开的原件 | JSON 只有路径和指针 |
| 原件新、戳旧 | 手改 | 可能多读一次旧戳 | 哈希不等 | 重读该文件 |
| 路由已改、文件还在旧路径 | 05 指针未写 | 模型加载失败 | Q-009 | 指针与搬迁同一 CR |

# 19. 当前待确认问题

1. 合并后，来源不是 `词库` 或状态不是 `confirmed` 的说法，能否用于 `registers/scope-register.md` 的枚举？本草稿在讨论结束前不允许。这是上轮反对点之一。
2. 是否在后续版本把所有 Markdown 写入改成只经脚本？本草稿不收口，只靠命中文件的哈希兜底。这是上轮反对点之二。
3. 需求文件 R4 的两个待决，本版收口如下，不再单列待拍板：给人看的依据记到文件级（路径、已有指针、Change Log 末行），不记到某一个格子。高风险不另做一张清单，也不另做分级器；沿用 00 号已有的必须确认级，以及 06 §8 已规定的 Change Log。
4. 版本号已定为 4.0.0。下架不讨论。

# 20. A 自审结果

| 审核项 | 结论 | 问题 | 已修订 | 说明 |
|---|---|---|---|---|
| 目标一致性 | 通过 | 无 | 是 | 只含已裁决项 |
| 目录扫描 | 通过 | 06 与代码有两处清单差 | 是 | 已写入断言 |
| 升级约束 | 通过 | 存量节在本文件，upgrade-to 待执行时落地 | 是 | 设计阶段不写 CR |
| 文件清单 | 通过 | 执行时路径以仓库实文件为准 | 否 | B 需自己扫 |
| 扩展性 | 通过 | 说法表只增不删 | 是 | 沿用分片 |
| 性能 | 通过 | 已写明为何不做全库判断 | 是 | 第 12.5 节 |
| 兼容 | 通过 | 目录不迁 | 是 | schema 不动 |
| 测试 | 通过 | 总数执行时再定 | 是 | 阻断项已列 |
| 辩论与评估 | 通过 | 两处反对留在第 19 节 | 是 | 用户要求后议 |
| 索引与联动 | 通过 | 无 | 是 | 第 17、18 节 |
| 复杂度 | 通过 | 仓库净增未超阈值 | 是 | 第 16 节 |
| 可交给 B | 通过 | V0.4 待复审 B2-1、B2-2 | 是 | 仍不可执行 |

# 21. 当前结论

忠实于已裁决目标：是。目标偏移：否。覆盖完整：是。可落地：待复审未再指出入口错误。需要再审：是，只复核第 7.1 节和第 7.2 节。可以直接执行：否。尚未获「同意执行」。

---

# AP-1. 变更概述

ChronoPM 从 3.30.3 升到 4.0.0。查询收进 `query-skill/`，用脚本做说法匹配和单文件版本戳，不再每次提问全库刷新。Portfolio 收进 `portfolio-skill/`，不再单独发包。项目目录保持现在的联邦形状。词库与各类别名合并成 `domain-glossary.md` 一张表，升级脚本处理旧项目且不问用户，做不完不盖戳。给人看的依据抽出已有的来源指针、文档链接、工作包编号和 Change Log，不新建 wiki 目录。schema 保持 0.17.0。

# AP-2. 影响点详细分析

| 影响项 | 当前 | 变更后 | 影响 | 程度 | 可逆 |
|---|---|---|---|---|---|
| `05-query-rules.md` §0 | 每次 `--all` | 调用 `query_locate.py` | 提问不再全库解析 | 高 | 是，规则可回退 |
| `refresh_views.py` | 查询与写入都调用 | 仅写入后与人工重建 | 视图可能比重建时刻旧；查询不读它当答案 | 高 | 是 |
| `domain-glossary.md` | 领域术语 | 再加上别名与标题 | 旧项目文件会被脚本重写 | 高 | 是，失败不替换 |
| `.state.json` | 指纹、facts、views。无 alias_index | 追加 `fact_stamps`。别名不放这里 | 戳是查询对账依据 | 中 | 是 |
| `context/active-entities.json` | 内含 alias_index | 改为说法表的投影，不再当权威 | 合并必须读升级前的这一份 | 高 | 是 |
| Portfolio 技能根 | 独立 SKILL.md 与第二 zip | 能力目录，无 SKILL.md | 不能再单独安装 | 高 | 需从基线找回文件 |
| 联邦 `ai/portfolio` 与 `ai/projects` | 两技能共用 | 路径相同，只由 Project 操作 | 工作区无迁移搬目录 | 低 | 是 |
| 范围登记枚举 | 只用词库 confirmed | 草稿阶段仍只用这类行 | 口语行先不进枚举 | 中 | 是 |
| 回归 | 1028 | 执行时追加 Q-001～Q-013 并重跑 | 总数执行时确定 | 中 | 是 |
| 核心契约 | 两技能分工 | 一个技能、两种工作区角色 | 安装单元变化，数据契约不变 | 高 | 是 |
| 已有工作区 | schema 0.17.0 | 仍 0.17.0，脚本改说法表和戳 | 必须跑升级程序 | 高 | 失败则版本不变 |

# AP-3. 变更策略与设计思路

选择「扩展现有词库文件 + 扩展现有哈希函数 + 搬迁现有规则」，不新建第二套检索产品。

1. 为什么是这个方案：全库刷新的成本在 `collect_facts`，不在写盘。只对命中文件哈希，才能在不缓存正文的前提下变快。说法已经散落在词库、alias_index、brain、WP aliases，用户要求并成一个东西，所以权威落在已有的 `domain-glossary.md`，而不是再造一个别名库。
2. 与现有规则的关系：00 的写入流程不动。05 的「读原件、禁止对话记忆当证据」保留，找路改由脚本完成。17 的确认语义保留给 `来源=词库` 的行，直到第 19 节改口。06 的 Change Log 就是给人看的「为什么改」。3.30.3 的已绑链继续是「依据哪份标准文件」。
3. 关键决策：schema 不升，因为没有新的必填目录。版本用用户指定的 4.0.0，因为对外从一个可安装技能变成一个。存量失败不盖戳，沿用 3.30.2 的硬闸。
4. 否决的替代：每次提问遍历全部事实源再决定读谁。遍历成本接近现在的全量解析，1 分钟目标达不到。另一被否决项是新建 `ai/wiki/`。3.30.3 已经否决，本需求用已有指针就能给人看。

# AP-4. 修改范围清单

| 文件 | 修改类型 | 修改内容摘要 | 新增/修改行数 | 是否核心契约 |
|---|---|---|---|---|
| `query-skill/**` | new_file | 能力目录、查询正文（含收尾登记与加热度）、`query_locate.py`（含 `--fill-path`） | 正文自 05 迁入，脚本新写 | 否 |
| `references/05-query-rules.md` | edit_full | 改为指针 | 约 10 行 | 否 |
| `portfolio-skill/**` | new_file | 自 Portfolio 迁入，入口改 CAPABILITY | 搬迁 | 是，只读边界原文要在 |
| `ChronoPM-Portfolio/SKILL.md`、`skill.json` | delete | 去掉独立入口 | — | 是 |
| `SKILL.md`、`skill.json` | edit_section | 描述、路由，以及 §2 集根三态。见 §7.1 | 数十行 | 是 |
| `migrate_workspace.py` | edit_section | `VERSION_CAPABILITIES` 加 4.0.0；`needs_v400` 在盖戳前执行。见 §7.2 | 执行时定 | 是 |
| `enforce_workspace_upgrade.py` | edit_section | 只增加对 4.0.0 步骤的调度 | 局部 | 否 |
| `sync_version.py` | edit_section | 4.0.0 起跳过 Portfolio 锁步 | 局部 | 是 |
| `audit_release.py` | edit_section | 断言 13 改为单包，并删除 `PORTFOLIO` 常量与双包注释 | 局部 | 是 |
| `README.md`、`README.en.md` | edit_section | 单包安装与发布物 | 局部 | 否 |
| `domain-glossary-template.md` | edit_section | 13 列 | 表头 | 否 |
| `pack.ps1` | edit_section | 停第二包；能力目录不排除 | 局部 | 否 |
| `refresh_views.py` | edit_section | 查询不再是它的调用方；别名投影改读说法表 | 局部 | 否 |
| `17-domain-glossary-rules.md` | edit_section | 唯一说法入口 | 局部 | 否 |
| `06-file-rules.md` | edit_section | 补 scope-register，改集层指向 | 局部 | 否 |
| `pack.py` | edit_section | 取消第二 zip | 局部 | 否 |
| 回归 | edit_section | Q-001～Q-013 | 13 条阻断 | 否 |

# AP-5. 回归测试计划

见第 13 节 Q-001～Q-013。阻断项是这 13 条，加上 3.30.3 的盖戳闸（空已绑且无登记边不得盖戳），以及被审版本 ≥ 4.0.0 时审计断言 13 的单包口径。

受影响的旧用例：凡是断言「查询必须先跑 refresh_views --all」的用例改为断言「查询不得跑 --all」。凡是断言「存在 ChronoPM-Portfolio zip」的用例改为断言只有 Project zip，且包内有 `portfolio-skill/CAPABILITY.md`。

# AP-6. 风险评估与回滚方案

| 风险 | 概率 | 影响 | 预防 | 回滚 |
|---|---|---|---|---|
| 说法合并丢行 | 中 | 旧叫法失效 | 键齐全才替换 | 不替换原文件，不盖戳 |
| 查询仍被写成全库 | 中 | 速度目标失败 | Q-001、Q-009 | 回退查询规则到 3.30.3 基线 |
| 删掉 Portfolio 入口后集层规则丢失 | 低 | 跨项目不可用 | 搬迁与删除同一版本，包内必须有 CAPABILITY | 从 `baselines/3.30.3` 找回 Portfolio 树，版本回到 3.30.3 |
| 工作区被误搬目录 | 低 | 联邦集损坏 | 脚本禁止改 `portfolio/` 与 `projects/` 的位置 | 本方案无目录迁移，无需迁回 |

回滚版本：3.30.3。操作：技能包换回 3.30.3 的 Project 与 Portfolio 两个 zip。工作区 schema 未变，不必做结构回滚。已经并进说法表的行可以留下，3.30.3 会把它当词库读；多出来的列按 17 号忽略未知列。4.0.0 的单文件对戳在回滚后不可用，查询回到全量刷新。

# AP-7. 版本影响

| 维度 | 变更前 | 变更后 |
|---|---|---|
| Skill Version | 3.30.3 | 4.0.0 |
| Workspace Schema | 0.17.0 | 0.17.0 |
| 是否需要工作区迁移 | 否（不搬目录） | 是（要跑程序改说法表和戳，不搬目录） |
| 迁移模式 | — | 程序处理存量；不是 structure-only，也不是只改版本文件 |
| 是否影响核心契约 | — | 是。安装单元从一个技能承载两种角色 |
| 是否影响已有工作区 | — | 是。必须跑升级程序才算 4.0.0 |

---

# 给 B 的审核输入包

你现在是 Skill 升级独立审核 Agent，代号 B。

请注意：

1. 不要基于 A 的缓存、记忆或结论直接判断。
2. 你必须自己扫描 Skill 项目目录，眼见为实。
3. A 的方案只能作为待审核对象，不能作为事实依据。
4. 如果 A 的文件判断、约束判断、实现路径与项目实际不符，请直接指出。
5. 你的输出需要能被我直接复制回 A，让 A 修订方案。
6. 不要直接执行改造，只做审核和建议。
7. 先确认你的工作空间与下面的快照一致。不一致则停止。
8. 向用户确认工作空间路径之后才审核。
9. 对需求做独立辩论，不要照搬 A。
10. 辩论「该不该做」和审核「该怎么做」分开写。

用户原始需求：

- 文件 `C:\Users\qiusuo\Downloads\市监重构项目管理\ai\outputs\20260923194000\需求-查询提速与零偏差.md`（SG-20260923-001）。请直接读该文件，不要只看 A 的转述。
- 用户随后要求：查询能力像拆文件一样放进 Project 内独立文件夹，查询相关文件和脚本都放进去；事实源变更状态要列清；已确认的先出方案；Portfolio 只做合并，工作区与两个技能时一样，以后不再发 Portfolio 包，不要考虑下架；词库、别名、新别名是一个东西，要合并，并用升级脚本处理历史项目里已经分开的内容，不问用户，高优先级；给人读的证据链本轮一起做；技能版本 4.0.0。
- 用户把 A 的两处反对留到以后讨论：口语说法进范围枚举是否污染；要不要先把所有写入收成脚本。

A 的需求理解与辩论见本文件第 1.6、12.5、19 节。A 的方案即本文件第 2 节至 AP-7。工作空间快照见第 1.5 节。

请按 `ChronoPM-Project/references/16-upgrade-dual-agent.md` 的 B 章节输出。V0.1 的审核已在下方 `## B1 审核结果`。V0.2 的处理记录在 B1 之前。复审请追加 `## B2 审核结果`，不要改 A 正文，也不要改 B1。

# 修订记录 V0.2（处理 B1，不改 B1 正文）

工作区与 B1 核对一致：`C:\Users\qiusuo\Downloads\ChronoPM Skill`，Skill 3.30.3。需求裁决维持继续实施。B1 结语为修订-需再审，以下全部落在 A 正文。

| B 问题编号 | B 的问题 | A 是否采纳 | 理由 | 对方案的修改 | 是否需再次给 B |
|---|---|---|---|---|---|
| B1-1 | alias_index 不在 `.state.json` | 采纳 | `refresh_views.py` 写到 `context/active-entities.json` | 第 8、8.2、18 节改为读该文件。`.state.json` 只追加 `fact_stamps` | 是 |
| B1-2 | 行结构三处不一致，缺旧列映射 | 采纳 | 模板与存量都是 11 列 | 第 5 节定为 13 列，含路径与状态。第 8.2 节逐列映射。类别、context_hint、备注保留 | 是 |
| B1-3 | 触发式登记缺失，Q-003 与 R2 冲突 | 采纳 | R2 已定稿 | 第 4 节：0 命中的那一次调用不写表；定位成功后收尾 `--register`。新增 Q-011。来源增加 `对话登记` | 是 |
| B1-4 | 查询轮禁写与脚本写入矛盾 | 采纳 | 两句不能同时留在迁入正文里 | 第 6、7 节：禁的是模型手改；登记、纠正、加热度只经脚本 | 是 |
| B1-5 | 发布链与迁移引擎未入清单 | 采纳 | 否则审计与版本同步会失败 | 第 7、14 节与 AP-4 补上 migrate、enforce 只调度、sync_version、audit 断言 13、README×2、模板、pack.ps1 | 是 |
| B1-6 | 事实源清单漏文件 | 采纳 | 06 §2.1 已有 source-type-registry；索引不是事实源 | 第 8.1 节补 18a 与三条非权威 | 是，随复审 |
| B1-7 | 共享人力索引未限定落盘范围 | 采纳 | 与既有澄清一致 | 第 8.1 节第 30 行写明只落静态元数据 | 是，随复审 |
| B1-8 | R4 两问未收口 | 采纳 | 用户要求本轮一起做 | 第 19 节第 3 点：文件级；不新建高风险分级器 | 是，随复审 |
| B1-9 | Portfolio 残留树与旧口径 | 采纳 | 只删两个入口文件会留下可被扫描的目录 | 第 7 节：校验后删除整树；迁入正文改能力目录口径 | 是，随复审 |
| B1-10 | 热度写放大 | 采纳 | 否则只读查询会改说法表并打失效戳 | 命中当时不写。收尾 `--flush-heat`。戳哈希去掉热度与最近命中。三写方互斥写入第 5、18 节 | 是，随复审 |
| B1-11 | 废弃工作包别名不再追随 | 采纳 | `_successor_id` 今天会追随 | 第 8.2 节第 7 步与 Q-012。refresh_views 只修正死链，不新增行 | 是，随复审 |

是否偏离目标：否。修订都是把已确认的合并、登记和单包发布写成与仓库实际一致的步骤，没有加新能力，没有改联邦目录，没有新建 wiki 目录。

# 修订记录 V0.3（处理第二轮，不改 B1 正文）

第二轮结语：**通过-待修订**。无阻塞项。按该结论修订后不再送审。执行仍等用户说「同意执行」。

| 编号 | 问题 | 采纳 | 改了什么 | 再审 |
|---|---|---|---|---|
| R2-1 | 工作包 frontmatter 没有 aliases | 采纳 | 第 8 节与第 8.2 节第 2 步改为复用 `refresh_views.py` 的解析：名称、编号、功能点、supersedes | 否 |
| R2-2 | 迁入正文没写收尾钩子；「至多 1 个文件」会被读成回答限制 | 采纳 | 第 4 节第 6 步限定这句只约束登记定位。第 6、7 节写明收尾 `--flush-heat` 与 `--register`。回答仍按 05 §2 的读取预算 | 否 |
| R2-3 | 空路径写回没有子命令 | 采纳 | 新增 `--fill-path`，只补空路径。`--register` 不承担补路径 | 否 |
| R2-4 | 集层 27–32 的戳没有读写方 | 采纳 | 这六行改为「不适用」。戳初始化不写集层文件。集层查询直读原件 | 否 |
| R2-5 | AP-2、AP-4 仍写 10 条 | 采纳 | 改为 Q-001～Q-013 | 否 |
| R2-6 | BLUEPRINT 仍写双包 | 采纳 | 第 7 节列入执行时改架构段，Blueprint Impact 标 full。不改「不建 wiki」 | 否 |

是否偏离目标：否。

# 修订记录 V0.4（处理 B2，不改 B1 与 B2 正文）

B2 结语：**修订-需再审**。工作区未变，仍是 Skill 3.30.3。

| 编号 | 处理 | 理由 | 落在哪里 |
|---|---|---|---|
| B2-1 | 采纳 | `migrate_workspace.py` 没有 `MIGRATIONS` 字典。版本表是 `VERSION_CAPABILITIES`，执行靠 `needs_v390` 这种判断，盖戳前有 `ensure_stock_compiled`。B2 引用的「追加 migrate_v400_glossary」不是 V0.3 的原句，入口仍按代码写明 | 第 7.2 节、第 8.2 节、AP-4 |
| B2-2 | 采纳 | `SKILL.md` §2 第 19–21 行仍要求集根去安装 ChronoPM-Portfolio。只改 description 不够 | 第 7.1 节 |
| B2-3 | 采纳 | `PORTFOLIO` 常量在约第 51 行，双包注释在约第 29–30 行。4.0.0 审计只检查当前仓库，不再留一套双包分支 | 第 7 节审计行、AP-4 |
| B2-4 | 不采纳 | 方案没有把 `collect_facts` 改成按变化文件重算。提问不调用它。先遍历目录再决定读谁，是已经否决的慢路径。单文件哈希、戳文件损坏时仍只读命中的那一份，写在第 4 节 | 第 4 节补了这句边界 |
| B2-5 | 不采纳 | 路径列是 `ai/` 下的文件路径。旧词库行是「原词 → 标准词」，没有文件指针，留空是对的。把来源写成「对话 / 文件 / 系统」会让脚本去开一个不存在的文件 | 第 8.2 节第 6 步写明禁止这种推断 |
| B2-6 | 不采纳 | 方案没有 `--read-only`。查询用 `query_locate.py`。`refresh_views.py` 仍只在写入之后重建视图，不增加只读开关 | 第 4 节 |

是否偏离目标：否。B2-1 与 B2-2 需要再看一眼落盘文字。其余三项不改变已定的查询机制。

## B1 审核结果

> 2026-09-23。B1 独立审核，按 `16-upgrade-dual-agent.md` B 章节输出（#0～#11，含 #2.5/#10.5）。审核前已自行扫描 Skill 项目目录与实际工作区（市监重构项目管理/ai/），未采信 A 缓存结论。

# 0. 工作空间版本核对

| 核对项 | A 的快照值 | B1 的实测值 | 是否一致 |
|---|---|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` | 同（B1 工作目录即该路径） | 是 |
| 版本标识来源 | `ChronoPM-Project/skill.json` version | 同 | 是 |
| 版本标识值 | 3.30.3；schema current 0.17.0；Portfolio VERSION 3.30.3 | Project VERSION=3.30.3 / skill.json=3.30.3 / supportedWorkspaceSchema current=0.17.0；Portfolio VERSION=3.30.3 / skill.json=3.30.3 | 是 |
| 关键文件清单 | `ChronoPM-Project/`、`ChronoPM-Portfolio/`、`governance-shared/planning/` | 三目录实存；planning/ 内即本文件 | 是 |

用户本轮指令已显式指定本文件绝对路径并指名 B1 审核，路径与 A 快照一致，B1 据此开工。另实测工作区侧：集根 `ai/.skill-version.json` skillVersion=3.30.2 / schema 0.17.0 / mode=portfolio；成员（全链通）3.30.2 / mode=single，与需求文件"执行包 3.30.3、工作区登记 3.30.2"吻合。

# 1. B1 自行扫描的目录与文件清单

| 路径 | 类型 | 是否已读取 | 作用判断 | 与本次升级关系 | 与 A 判断是否一致 |
|---|---|---|---|---|---|
| `ChronoPM-Project/references/05-query-rules.md` | 规则 | 是（§0/§1a/§1.5/§0.1/§2） | 查询硬步骤与禁写条款 | 迁移源 | 一致 |
| `ChronoPM-Project/scripts/refresh_views.py` | 脚本 | 是（run L1168-1192、collect_facts L816、build_entities L1031、active-entities 写出 L1251、_file_sha L37） | 视图刷新引擎 | 热路径改造对象 | 大体一致；alias_index 写出位置 A 写错（见 B1-1） |
| `ChronoPM-Project/scripts/migrate_workspace.py` | 脚本 | 是（2639 行；MIGRATIONS 版本分派、stamp_skill_version、ensure_stock_compiled 3.30.2 闸） | 存量迁移真正引擎 | §8.2 合并与盖戳闸的实际载体 | **A 未列**（见 B1-5） |
| `ChronoPM-Project/scripts/enforce_workspace_upgrade.py` | 脚本 | 是（172 行入口/guard） | 升级入口调度 | §7 列为合并载体 | 载体定位不精确（见 B1-5） |
| `ChronoPM-Project/scripts/sync_version.py` | 脚本 | 是（L106-119 Portfolio 锁步） | 版本同步 | 4.0.0 单包后须改 | **A 未列** |
| `governance-shared/scripts/audit_release.py` | 脚本 | 是（断言 13 L371-405） | 发布审计 | 删 Portfolio 入口后必然 FAIL | **A 未列** |
| `tools/pack-skill/scripts/pack.py` + `pack.ps1` | 脚本 | 是（find_companion L104-111；$excludeDirs/$includeExceptions） | 打包 | 停第二 zip | pack.py 已列；pack.ps1 注释与防呆未列 |
| `ChronoPM-Project/source-split-skill/` | 目录 | 是（CAPABILITY.md+assets+references，无 SKILL.md） | 能力目录形态范本 | 新目录照此形态 | 一致 |
| `ChronoPM-Project/SKILL_BLUEPRINT.md` / `tests/test_enforce_workspace_upgrade.py` | 文档/测试 | 是（L127/129 禁 wiki 决策；L143 test_ue017_no_wiki_dir） | 架构决策与回归 | 佐证断言 6 | 一致 |
| `ChronoPM-Project/references/06-file-rules.md` | 规则 | 是（§2.1 完整清单 L115-147、§2.8 L200-202、§7.7 L330-334、§8 L260） | 事实源与文件规则 | 补清单对象 | 一致（scope-register 确实缺席 §2.1） |
| `ChronoPM-Project/references/17-domain-glossary-rules.md` | 规则 | 是（§6.1 九步流程、§8.1 自动发现、类别字段说明 L66） | 词库状态机 | 列结构耦合方 | 一致但工作量被低估 |
| `ChronoPM-Project/assets/templates/domain-glossary-template.md` | 模板 | 是（L15 十一列表头、L25 错误更正表、L30 候选表） | 新项目初始化词库 | **A 未列**（三层同步缺口） |
| `README.md` / `README.en.md` | 文档 | 是（L7/17/19/59/68/80/105 双包分工与安装指引） | 用户安装入口 | 4.0.0 后为错误指引 | **A 未列** |
| `governance-shared/baselines/3.30.3/` | 基线 | 是（ChronoPM-Project + ChronoPM-Portfolio 双树实存） | 回滚依据 | AP-6 可行 | 一致 |
| 实际工作区：集根 `ai/portfolio/`+`ai/projects/{全链通重构,企业通重构,信用监管登记注册重构}/ai/` | 数据 | 是 | 联邦结构实证 | 断言 7 | 一致 |
| 全链通 `ai/context/domain-glossary.md` | 数据 | 是（11 列：编号/原词/标准词/类别/context_hint/状态/来源/首次出现/最近命中/命中次数/备注；G001-G007 confirmed） | 存量词库 | 合并输入 | **列结构与 §5 五字段口径不符** |
| 全链通 `ai/.state.json` | 数据 | 是（仅 6 键：facts_fingerprint/journal_fingerprint/facts/journal/views/source_digest_status，**无 alias_index**） | 戳与指纹 | fact_stamps 落点 | **alias_index 位置 A 写错** |
| 全链通 `ai/context/brain.md` | 数据 | 是（frontmatter facts_fingerprint；L131 起别名跳转表：政务服务网对接→WP-055 等） | 别名短表 | 合并输入 | 一致 |
| 全链通 `ai/registers/scope-register.md`、`requirements/source-type-registry.md` | 数据 | 是（均存在） | 事实源 | 8.1 清单对齐 | scope-register 一致；source-type-registry A 未列 |

# 2. 对 A 需求理解的审核

| 原始需求点 | A 的理解 | B1 的判断 | 是否有偏差 | 修正建议 |
|---|---|---|---|---|
| 查询约 1 分钟且读原件 | 热路径不再全库解析，`query_locate.py` 只碰命中文件 | 正确；05 §0 现行 `--all` + run() 先 collect_facts（L1178/1186）实证成立 | 否 | — |
| 口语说法不丢、不靠用户报标准名 | 并进词库文件、脚本维护（§8.2） | **存量合并部分成立；但 R2 定稿四约束之「触发式登记=无感自动落盘」在方案中无对应步骤**，Q-003 还断言「命中 0 条不写说法表」 | **是** | 见 B1-3 |
| 词库与别名一个东西、升级脚本处理存量不问用户 | 一张表、脚本合并、失败不盖戳 | 方向正确；但合并输入源写错（alias_index 不在 .state.json） | **是（实现细节）** | 见 B1-1 |
| 许多事实源都要有变更状态 | 按清单打机器戳 | 正确；8.1 对 06 §2.1 的补齐不完整 | 部分 | 见 B1-6 |
| 给人读的证据链本轮做 | 已有指针 + Change Log，不建 wiki | 正确；R4 两个待决问题（高风险由谁判/粒度）未显式收口 | 部分 | 见 B1-8 |
| 查询独立成能力目录 | `query-skill/` | 正确，形态有范本 | 否 | — |
| Portfolio 合并、工作区不变、不再发包 | `portfolio-skill/`，联邦不改 | 正确；残留树处置与迁入口径未明确 | 部分 | 见 B1-9 |
| 判定用 Python、推导留文字 | 脚本 JSON + 规则写推导 | 正确 | 否 | — |
| 借 Jev 模式 | 本地脚本，不接 HTTP | 正确 | 否 | — |
| 版本 4.0.0 | Major，schema 不动 | 正确（无新必填目录，19 号无词库列校验） | 否 | — |
| 下架不管、两处反对后议 | 不纳入/第 19 节 | 与用户裁决一致 | 否 | — |

# 2.5 B1 对需求本身的独立辩论

（1）B1 的独立合理性论证

| 论证项 | B1 的独立结论 | 依据（落到具体文件/能力） | 与 A 的辩论是否一致 |
|---|---|---|---|
| 需求是否符合 Skill 定位与能力边界 | 符合。查询是 PM 日常最高频动作，改造热路径不触碰写入契约与联邦边界 | 05 §0 现行设计把保真成本放在查询侧；方案只动读侧 | 一致 |
| 需求是否有真实使用场景 | 有。需求文件证据链完整（四关卡分析、复现步骤、同工作区对照实验） | SG-20260923-001 §一/§七；collect_facts 实测要读工作包/待办/计划/风险/问题/需求/词库/范围表/各源 meta | 一致 |
| 需求是否与现有能力重复/重叠/冲突 | 不重复。「只缓存路径、不缓存内容」与既有零幻读红线一致；与 05 §0.1 矩阵失败门、禁对话记忆当证据等约束不冲突 | 05 §0/§0.1；06 §328 索引加速器语义 | 一致 |
| 需求是否合理 | 合理。保真成本前移到写入/升级时刻是正确的机制归位 | 需求文件 §2.3「保真机制错位」诊断与 B1 对代码的实测互相印证 | 一致 |

（2）B1 对需求必要性的独立分级

**必须加**。05 §0「每一次查询（同一会话第 2 问也一样）」跑 `--all`，run() 在指纹比对前已 collect_facts 全库（L1178→L1186），文件量增长后 1 分钟目标不可达；不升级则需求文件所述「小问题不敢问」持续。

（3）B1 补充的扩展改动风险点（A 未识别到的）

| 风险维度 | 风险说明 | 严重程度 | 建议 |
|---|---|---|---|
| 热度写放大 | 说法表自身在 8.1 权威清单第 23 项（要打戳）。每次命中即加热度 → 该文件变 → 其戳过期 → 「只读查询」实际触发说法表+戳两处写入，读多写少假设被侵蚀，且查询轮变写轮（与 05 简单查询底线的精神有摩擦） | 中 | 热度列定义延迟批量更新策略（如会话收尾一次写），或明确「热度列变更不触发该文件戳失效」的口径，写进 §5/§8.1 |
| 多文件答案的新鲜度语义 | `changed` 只对命中文件有意义；模型答案若引用第二个事实源（e.g. WP+待办），后者无戳校验 | 低 | 规则补一句：非命中文件不承诺 changed 语义，结论以本次实读原件为准（现状本来如此，写明防误用） |
| 说法表三写入方互斥 | query_locate（纠正/热度/登记）、refresh_views（投影重建）、migrate（合并）三处写同一文件，无锁序/互斥设计 | 低 | §18 补一句「同一工作区同一时刻仅一个写方；脚本写前重读全表、临时文件原子替换」（原子替换已有，补互斥声明即可） |
| 触发式登记行与「不丢词」的清理边界 | 新登记行若来源值不在既有过滤条件（只认 `来源=词库`）内，后续任何"清表"操作可能误删口语行 | 低 | 17 号补「说法表只增不删」硬句（方案 §8 已有此意，落到规则） |

（4）B1 的需求裁决建议

**支持继续实施**。需求真实、方向正确（保真成本从查询侧移到写入侧）、与既有红线无冲突；但方案在存量实施细节上有 5 项阻塞缺口（见 #9），修订后可收敛，无须重做。

# 3. 对 A 目录扫描结果的审核

| 文件/目录 | A 的判断 | B1 的实际观察 | 是否一致 | 问题说明 |
|---|---|---|---|---|
| alias_index 存放于 `.state.json` | §8「brain.md 与 .state.json 的 alias_index 改为投影」；§8.2「读入 .state.json 的 alias_index」 | **`.state.json` 仅 6 键，无 alias_index；alias_index 在 `context/active-entities.json`**（refresh_views.py L1251 写出；05 §0「active-entities.json 的完整 alias」） | **否** | 见 B1-1 |
| 存量执行器 = `enforce_workspace_upgrade.py` | §7 第 9 项把合并与盖戳闸全归它 | 该文件仅 172 行入口（guard/调度）；真正迁移引擎是 `migrate_workspace.py`（2639 行，MIGRATIONS 分派 + `stamp_skill_version` + `ensure_stock_compiled` 已绑闸） | 部分 | 见 B1-5；"谁执行"方向对，文件定位须修正 |
| 能力目录形态 CAPABILITY.md 禁 SKILL.md | source-split-skill 为范本 | 实测一致；pack.ps1 L157 亦有同款注释 | 是 | — |
| pack.py 因兄弟 SKILL.md 打第二 zip | find_companion | 实测一致（L16-17/L104-111）；但排除数组单一事实源在 pack.ps1 | 是 | pack.ps1 的 companion 相关注释行未列入修改清单 |
| 06 §2.1 漏 scope-register | 实际存在但缺席 | 实测一致：§2.1 清单（L115-147）无 `registers/scope-register.md`；文件实存；05 §0.1/L124 实际消费 | 是 | 方案补清单正确 |
| 06 §2.1 列 logs/ops、§2.8 否定 | 以 §2.8 为准 | 实测一致（L120-121 vs L200-202） | 是 | — |
| 8.1 权威清单补齐 06 §2.1 | §7 第 12 项 | 补了 scope-register，但漏 `requirements/source-type-registry.md` 与 canonical-index/atom-index/{category}-index/artifacts 四类 | 部分 | 见 B1-6 |
| 存量词库/别名/brain 形态 | §8.2 输入清单 | 词库 11 列（含状态/类别/context_hint/命中次数）；brain 别名短表实存；WP aliases 为解析产物；**模板同为 11 列** | 部分 | 行结构与映射未定义，见 B1-2 |

# 4. 对项目内升级约束遵循情况的审核

| 约束来源文件 | 约束内容 | A 是否遵循 | 问题 | 修正建议 |
|---|---|---|---|---|
| `16-skill-governance-rules.md` §2.1b | 改查询形态/索引/关联方式的升级，upgrade-to 必须有「工作区存量」节 | 是（§8.2 + §7 第 14 项声明执行时含存量节） | 无 | — |
| `16-upgrade-dual-agent.md` B 骨架与四档结语 | 方案含 #1-21 + AP1-7 + 审核输入包 | 是 | 无 | — |
| `SKILL_BLUEPRINT.md` 3.30 决策 | 不新建 `ai/wiki/` | 是（继续禁止；test_ue017 实存） | 无 | — |
| 3.0.0 联邦契约 | `ai/portfolio/` + `ai/projects/{名}/ai/` 不改形 | 是（§2/§12；实测三成员联邦结构完好） | 无 | — |
| workspace schema 0.17.0 | 无新必填目录不升 schema | 是；19 号无词库列校验，列结构变更不触发 schema 升级 | 无 | — |
| `pack.ps1` L157 | 能力目录必须进包且禁 SKILL.md | 是（query-skill/portfolio-skill 不在 $excludeDirs，默认进包） | 未知口径未写入方案 | §7 补一句：两新目录禁入 pack.ps1 excludeDirs（防呆） |
| 20 号版本戳惯例 | 施工只认回归 1028 | 是（§13 声明执行时按套件实数） | 无 | — |

# 5. 对文件级改动清单的审核

| 文件路径 | A 计划操作 | B1 审核结论 | 是否同意 | 风险 | 建议 |
|---|---|---|---|---|---|
| `query-skill/**`（CAPABILITY/references/scripts） | 新增 | 同意 | 是 | 低 | CAPABILITY.md 里写明「能力目录禁命名 SKILL.md」 |
| `references/05-query-rules.md` | 改为指针 | 同意，但**须同时改写 §1.5 查询轮禁写条款** | 是 | 中 | 见 B1-4：迁移正文里「查询轮禁止写词库」与「脚本改行/加热度/触发登记」矛盾，§7 修改描述未列此项 |
| `references/17-domain-glossary-rules.md` | 修改（唯一入口、脚本加热度） | 方向同意，工作量低估 | 是 | 高 | 列结构耦合：§6.1 九步、§8.1 自动发现、pending→confirmed 状态机、错误更正表/候选表（模板 L25/L30）全要随新行结构改写；AP-4 的「局部」定性不准 |
| `assets/templates/domain-glossary-template.md` | **未列** | 必须补 | **否（须补）** | 高 | 三层同步（17 号规则/模板/脚本）：模板不改，新项目初始化生成旧 11 列，与 4.0.0 解析器冲突 |
| `scripts/enforce_workspace_upgrade.py` | 修改（合并+盖戳闸） | 载体须修正 | 是（修正后） | 高 | 实际合并/闸须落 `migrate_workspace.py`（MIGRATIONS 加 4.0.0 步骤、stamp 门禁链）；enforce 只改调用 |
| `scripts/sync_version.py` | **未列** | 必须补 | **否（须补）** | 高 | L106-119 Portfolio 锁步在 4.0.0 报错/空转；「双包同号」惯例自 4.0.0 停止须在此落地 |
| `governance-shared/scripts/audit_release.py` | **未列** | 必须补 | **否（须补）** | 高 | 断言 13（L371-405）：Portfolio 目录缺失/skill.json 缺失/双基线缺失均记 FAIL——删独立入口后发布审计必红灯；AP-5 的审计验收无载体 |
| `README.md` / `README.en.md` | **未列** | 必须补 | **否（须补）** | 中 | L7/17/19/59/68/105 的双包分工、加装 Portfolio、双 zip 发布产物全部过时，用户按 README 装不到 Portfolio 包 |
| `tools/pack-skill/scripts/pack.ps1` | 未列 | 建议补 | 部分 | 低 | companion 相关注释行同步；两新能力目录防呆声明 |
| `ChronoPM-Portfolio/SKILL.md`、`skill.json` | 删除 | 同意，但残留树处置未明确 | 是（补明确） | 中 | 见 B1-9：迁入后其余文件（references/templates/VERSION/…）删/留未写；AP-6 回滚「从 baselines/3.30.3 找回」暗示整树删除，§7 须写明 |
| `pack.py` 停第二 zip | 修改 | 同意 | 是 | 低 | Q-008 可加 pack.ps1 断言 |
| `governance/migrations/upgrade-to-4.0.0.md` | 执行阶段新建 | 同意（位置与 16 号 §2.1b 合规） | 是 | 低 | — |

# 6. 对数据、索引、分块、扩展性的审核

- **说法表行结构三处口径不一致（阻塞，见 B1-2）**：§5 写「说法、登记名、来源、热度、updated」五字段（无路径列）；§17 写「行含路径、登记名、来源、热度」；实测存量与模板为 11 列（含状态/类别/context_hint/首次出现/最近命中/命中次数/备注）。§4 步骤 3 与 Q-001 要求行内可寻址到目标文件——无路径列则脚本无法定位。confirmed/pending 状态在新表的承载未定义，而 §8.2 末段范围枚举过滤又依赖「原状态为 confirmed」。
- **旧→新字段映射缺失**：11 列→目标态的逐列映射、命中次数→热度、备注/类别/context_hint 去留均未写。v2.1.0 第十三轮已有「字段映射变体表」先例（旧 17 列/16 列之争），本方案须补同类映射表，否则 Q-006 的「键都在」可测、「值正确」不可测。
- **触发式登记缺失（阻塞，见 B1-3）**。
- **8.1 清单补齐不完整（非阻塞，见 B1-6）**：`requirements/source-type-registry.md`（实存，弱表列对槽位的判定依据）应进权威表；`canonical-index.md`/`atom-index.md`/`{category}-index.md`/`requirements/artifacts/` 应进「不是事实源」表并给理由，否则 §8.2 初始化戳按 8.1 清单漏打。
- 膨胀控制：只增不删+分片阈值沿用，可行。**supersede 追随退化（非阻塞，见 B1-11）**：现状 alias_index 每次重建自动把废弃 WP 别名追随到后继包（build_entities `_successor_id`）；并入静态说法表后该行不再自动追随，WP 废弃后口语行指向死包。§8.2 须补：合并时废弃 WP 的别名行指向后继（或标记），此后由 refresh_views 投影校验。
- 热度写放大与三写入方互斥：见 #2.5(3)。

# 7. 对上下文限制和输出分块策略的审核

同意。查询轮加载量下降（说法表+单文件 vs 全库+brain+05 全文），分块策略与 9 节声明一致，无问题。

# 7.5 对现有能力扩展优先评估的审核

| 新增能力 | A 是否评估了现有能力可扩展性 | A 的扩展评估是否充分 | B1 判断应扩展还是新增 | 问题说明 |
|---|---|---|---|---|
| query-skill | 是（05 迁移+source-split 形态） | 充分 | 扩展（搬迁） | — |
| portfolio-skill | 是（规则原样迁入） | 基本充分 | 扩展（搬迁） | 迁入规则的「本包/须同时安装」口径须改写（见 B1-9） |
| 说法合并 | 是（词库为落点） | 载体充分、映射不充分 | 扩展 | 见 B1-2 |
| 单文件对戳 | 是（复用 _file_sha） | 充分（L37 实存） | 扩展 | — |
| 证据链 | 是（已有指针） | 充分 | 扩展 | — |
| 17 号改造 | 写「edit_section 局部」 | **不充分** | 扩展 | 列结构耦合 §6.1/§8.1/状态机/错误更正表/候选表，实为结构性改写；复杂度表应如实反映 |

有简化项（删独立入口、停第二 zip、05 变指针），非只增不减 ✅。净增复杂度整体未超阈值，但 §16「仓库合计基本持平」未计 README×2/audit/migrate 的触点，表述偏乐观，不改变结论。

# 7.6 对索引合理性的审核

| 评估项 | A 的判断 | B1 的实际观察 | 是否一致 | 问题说明 |
|---|---|---|---|---|
| 深度 | 说法→路径两层 | 成立 | 是 | 前提是行内有路径列（B1-2 收口后成立） |
| 粒度 | 文件级 | 成立 | 是 | — |
| 覆盖 | 升级后全覆盖 | 成立（三输入源并集） | 是 | 输入源位置须修正（B1-1） |
| 一致性 | 权威只剩词库 | 成立 | 是 | 三写入方互斥须补声明 |
| 原子性 | 临时文件替换+键齐全校验 | 成立（§18） | 是 | 幂等第二遍（Q-006）设计好 |
| 孤儿/悬空 | 未评估 | 废弃 WP 行指向死包是悬空索引实例 | 部分 | 见 B1-11 |

# 7.7 对联动更新设计的审核

- 升级顺序（成员全成→集层重写 glossary-index 指针）底层→上层，正确；失败回退（不盖戳、保留原文件）可靠。
- 遗漏一：三写入方（query_locate/refresh_views/migrate）对说法表无互斥口径（低风险，补声明）。
- 遗漏二：热度更新使权威表 23 号自戳循环（§18「一次查询」行已写单键写回，但没处理说法表自身戳随热度变化的问题）。
- 遗漏三：query-skill 指针文件与搬迁同一 CR ✅（§18 风险表已有，正确）。

# 8. 对风险、异常处理、兼容性、测试验收的审核

- Q-001～Q-010 设计质量高：测试替身计数（Q-001）、幂等（Q-006）、失败不盖戳（Q-007）、打包断言（Q-008）均务实。
- **Q-003「不写说法表」与 R2 定稿冲突（B1-3）**；缺触发式登记的测试断言；缺「废弃 WP 行指向后继」断言（B1-11）。
- 无 Python 降级（直读路由文件+as-of）保留完整 ✅。
- AP-6 回滚可行：baselines/3.30.3 双树实测存在；「多出来的列按 17 号忽略未知列」回滚兼容设计合理。
- 异常表（§10）覆盖替读/冲突/手改兜底，其中「手改后问到才发现」已由用户裁决接受 ✅。

# 8.5 对方案影响与必要性评估的审核

六项齐全；影响范围表真实（05/词库/Portfolio 根/.state/打包/工作区全覆盖）；历史体验判断客观（增强查询、发行入口收一）；必要性成立（collect_facts 实证 + 1 分钟目标）；匹配度成立（SG-20260923-001 + Qoder 无法检索 Portfolio 的场景）。B1 独立意见：影响范围表漏了「发布审计链（audit_release/sync_version/README）」与「迁移引擎（migrate_workspace）」两个维度，补齐后评估才完整；不改变必要性结论。

# 8.6 对方案关键断言与放行门槛声明的审核

| # | 关键断言（12.6） | B1 核验结果 |
|---|---|---|
| 1 | 05 §0 强制每次查询 `--all`；指纹未变仍已跑 collect_facts | **未证伪**。05 §0 L46-52「每一次查询（同一会话第 2 问也一样）」实证；run() L1178 先 collect_facts、L1186 才比指纹 |
| 2 | 词库、alias_index、brain 别名、WP aliases 分开的入口 | 断言本身**未证伪**（四入口确分立）；**但其 §8/§8.2 实施载体「alias_index 位于 .state.json」被证伪**（实际在 context/active-entities.json） |
| 3 | 查询轮禁止生词写进词库 confirmed | **未证伪**（05 §1.5 L96 实证）。A 声明「改为脚本写同一张表」方向可，但 §7 未列禁写条款的改写项（B1-4） |
| 4 | pack.py 因兄弟 SKILL.md 打第二 zip | **未证伪**（L16-17/L104-111） |
| 5 | 能力目录 CAPABILITY.md 且禁 SKILL.md | **未证伪**（source-split-skill 实测） |
| 6 | 3.30.3 禁止新建 ai/wiki/ | **未证伪**（BLUEPRINT L127/129 + test_ue017 L143） |
| 7 | 联邦目录不改 | **未证伪**（集根+三成员实测） |
| 8 | scope-register 存在但不在 06 §2.1 | **未证伪**（§2.1 清单实查无此文件；文件实存；05 实际消费） |
| 9 | logs/ops §2.1 列入、§2.8 否定 | **未证伪**（L120-121 vs L200-202），以 §2.8 为准正确 |

放行门槛核对：12.6 表内 9 条断言均未被证伪；但放行门槛同时要求「**无新的阻塞问题**」——B1 新发现 5 项阻塞（#9 B1-1～B1-5），其中 B1-1 属方案正文实施载体与项目实际不符（16 号审核包第 4 条），B1-3 使第 15 节「完全覆盖=是」的断言失实。按 A 自设门槛与 16 号判级标准，不达「通过」。

# 9. B1 发现的问题清单

| 编号 | 问题 | 严重程度 | 是否阻塞执行 | 建议修复方式 |
|---|---|---|---|---|
| B1-1 | alias_index 存放位置写错：§8/§8.2 称读 `.state.json` 的 alias_index；实测 `.state.json` 仅 6 键无此键，alias_index 在 `context/active-entities.json`（refresh_views L1251 写出、05 §0 引用）。按 §8.2 写合并脚本将读不到存量别名 → WP 标题/人员缩写/待办别名全部漏并 → 存量丢词，Q-006 必挂 | 阻塞 | 是 | §8/§8.2 输入源改为 `context/active-entities.json` 的 `alias_index`；§8「降为投影」的落点同步改写 |
| B1-2 | 说法表目标态行结构未定义且三处口径不一（§5 五字段无路径 / §17 行含路径 / 实测+模板 11 列）；§4+Q-001 要求行内寻址；confirmed/pending 在新表无承载而 §8.2 过滤又依赖它；旧→新逐列映射缺失 | 阻塞 | 是 | §5 定稿行结构（须含路径列与状态列，或显式声明状态并入某列）；给 11 列→目标态逐列映射表（含命中次数→热度、类别/context_hint/备注去留）；§17/§8.2 同步 |
| B1-3 | 触发式登记缺失：R2 定稿四约束之一「触发式登记=无感自动落盘」在 §4 交互流程无对应步骤（0 命中→定位成功→登记）；Q-003 断言「不写说法表」与 R2 定稿直接冲突；§8.2 来源枚举无「对话登记」；第 15 节该需求点「完全覆盖=是」失实 | 阻塞 | 是 | §4 补登记步骤（0 命中→模型按路由定位→对话收尾脚本写新行：说法/登记名/路径/来源=对话登记/热度初值/状态口径）；Q-003 改口径并新增登记测试；§8.2 枚举补值；第 15 节如实改 |
| B1-4 | 05 §1.5「查询轮禁止写词库（v3.22.0）」及 17 §6.1 第 6 步/§8.1 联动禁令与方案「脚本写同一张表」（纠正回填/加热度/触发登记）冲突，§7 迁移行的修改描述未列禁写条款改写 → 迁移正文残留自相矛盾 | 阻塞 | 是 | §7 两个文件行补「改写禁写条款为『仅脚本可写、查询轮 AI 不得手写』」，语义边界写清 |
| B1-5 | 发布链与迁移引擎文件缺失于 §7/§14：① `audit_release.py` 断言 13 双包一致性（L371-405）删 Portfolio 入口后必 FAIL，且要求 baselines/4.0.0/ChronoPM-Portfolio 双基线；② `sync_version.py` L106-119 Portfolio 锁步；③ `README.md`/`README.en.md` 双包分工与安装指引；④ `migrate_workspace.py`（真正迁移引擎与盖戳闸，§7 只写 enforce）；⑤ `domain-glossary-template.md`（11 列模板，三层同步）；⑥ `pack.ps1` companion 相关注释。AP-4/AP-5 须同步 | 阳塞 | 是 | §7/§14/AP-4 补齐 6 处；audit 断言 13 改写为 4.0.0 单包口径（含 4.0.0 基线单树要求） |
| B1-6 | 8.1 清单对 06 §2.1 补齐不完整：漏 `requirements/source-type-registry.md`（权威类）与 canonical-index/atom-index/{category}-index/artifacts（非权威类） | 非阻塞 | 否 | 补入对应表并给理由；否则 §8.2 初始化戳漏文件 |
| B1-7 | shared-resource-index 历轮硬性澄清（第十/十一轮：可用性摘要=动态视图不落盘，落盘仅限静态索引元数据）再次未写入方案文本；8.1 集层表 30 号列为权威事实源且「回答什么」未限定字段范围 | 非阻塞 | 否 | 8.1 表 30 号行补「落盘仅限静态索引元数据；可用性/排期摘要为实时聚合动态视图，不落盘」 |
| B1-8 | R4 两个待决问题（高风险清单由谁判/证据链粒度）未显式收口，第 19 节未列 | 非阻塞 | 否 | 补一句显式处置：证据链=文件级（evidence 字段已隐含）；高风险分级本轮不采用，依赖既有 06 §8 Change Log 义务；或列入第 19 节 |
| B1-9 | ChronoPM-Portfolio/ 残留树处置未明确（§7 只删 SKILL.md+skill.json；AP-6 回滚暗示整树删除）；portfolio-skill 迁入规则含「本包/须同时安装」旧口径（Portfolio SKILL.md L7 实证）未列改写 | 非阻塞 | 否 | §7 写明：迁入校验后整树删除（回滚自 baselines/3.30.3）；迁入口径统一改「能力目录」 |
| B1-10 | 热度写放大：权威表 23 号（说法表）自打戳，每次命中加热度→文件变→戳失效循环，「只读查询」实际写两个文件 | 非阻塞 | 否 | 热度延迟批量更新或声明「热度列变更不触发戳失效」；同时补三写入方互斥声明 |
| B1-11 | supersede 追随退化：现状 alias_index 重建时经 `_successor_id` 自动把废弃 WP 别名追随到后继包；并入静态说法表后行不自动追随，WP 废弃后口语行指向死包 | 非阻塞 | 否 | §8.2 合并规则补「废弃 WP 的别名行指向后继包」；refresh_views 重建时校验行指向 |

# 10. B1 给 A 的修订建议

按 #9 逐条修订，全部落本文件 A 正文（设计阶段只改本文件）：

1. **§8/§8.2（B1-1）**：两处「`.state.json` 的 alias_index」改为「`context/active-entities.json` 的 alias_index」；§8 末段投影落点同步改。改完检查 §18 联动表「alias 投影」行。
2. **§5/§17/§8.2（B1-2）**：说法表行结构定稿（建议七列：说法/登记名/路径/来源/热度/状态/updated，A 可自定但**必须含路径列与状态列**）；给出旧 11 列→新结构的逐列映射表；§17「行含路径」与 §5 统一；§8.2 补「confirmed/pending 在新表如何承载、范围枚举过滤如何作用于新行」。
3. **§4/§8.2/§13/§15（B1-3）**：交互流程补触发式登记步骤与失败兜底；Q-003 预期改为「退出码 2，本轮不编结论」并新增「0 命中且模型定位成功后说法表新增一行」断言；§8.2 来源枚举补「对话登记」；第 15 节对应行如实改「部分覆盖」并在修订后回到「完全覆盖」。
4. **§7（B1-4）**：05 迁入行与 17 号行各补禁写条款改写描述（「仅脚本可写」边界）。
5. **§7/§14/AP-4（B1-5）**：补 6 个文件项——audit_release.py（断言 13 改单包口径+4.0.0 基线单树）、sync_version.py（去 Portfolio 锁步）、migrate_workspace.py（4.0.0 迁移步骤与 stamp 门禁）、README.md+README.en.md（双包→单包安装指引）、domain-glossary-template.md（新行结构）、pack.ps1（companion 注释+能力目录防呆）。
6. **§8.1（B1-6）**：补 source-type-registry（权威）与三 index+artifacts（非权威，注明理由）。
7. **§8.1 集层表 30 号（B1-7）**：写入历轮澄清（可用性摘要=动态视图不落盘）。
8. **第 19 节或 §8.1（B1-8）**：R4 两待决问题显式收口声明。
9. **§7（B1-9）**：Portfolio 残留树处置写明（建议迁入校验后整树删除）；迁入规则口径改写列入 portfolio-skill 行。
10. **§5/§8.1/§18（B1-10）**：热度更新策略与三写入方互斥声明。
11. **§8.2（B1-11）**：废弃 WP 别名行的后继指向规则。

# 10.5 发现问题严重度映射表

| B1 问题编号 | 问题 | 严重度 | 判定依据（对照判级标准表） | 对照 A 的关键断言/放行门槛 |
|---|---|---|---|---|
| B1-1 | alias_index 位置写错 | 阻塞 | A 的实施路径与项目实际不符（16 号审核包第 4 条）；影响存量合并正确性→数据不一致 | 放行门槛「无新的阻塞问题」不满足；12.6 断言 2 实施载体被证伪 |
| B1-2 | 行结构未定义、三处口径不一、映射缺失 | 阻塞 | 须新增字段/规则才能成立；脚本无法落码 | 放行门槛不满足 |
| B1-3 | 触发式登记缺失 | 阻塞 | 已裁决需求（R2 定稿）未覆盖；第 15 节断言失实 | 放行门槛不满足；#15「完全覆盖」被证伪 |
| B1-4 | 禁写条款冲突未列改写 | 阻塞 | 规则残留自相矛盾→影响现有能力正确性（执行歧义） | 放行门槛不满足 |
| B1-5 | 发布链/迁移引擎 6 文件未入清单 | 阻塞 | 方案无法闭环到发布（审计必 FAIL、版本同步报错、安装指引错误、新项目模板错结构） | 放行门槛不满足；AP-5 验收无载体 |
| B1-6 | 8.1 补齐不完整 | 非阻塞 | 不影响主链路，补清单即可 | — |
| B1-7 | shared-resource-index 澄清未写入 | 非阻塞 | 原则框架（纯聚合层）已覆盖，执行期注意事项 | — |
| B1-8 | R4 待决未收口 | 非阻塞 | 取舍已隐含，补声明即可 | — |
| B1-9 | 残留树与迁入口径 | 非阻塞 | 补明确即可，方向无争议 | — |
| B1-10 | 热度写放大/互斥 | 非阻塞 | 性能与一致性兜底类，不改变已定机制 | — |
| B1-11 | supersede 追随退化 | 非阻塞 | 兜底类，可在合并规则内修复 | — |

# 11. B1 最终结论

判级依据：12.6 表内 9 条关键断言经逐条实测均未被证伪（方向性正确、无重做级问题），但 B1 新发现 5 项阻塞问题（B1-1～B1-5）：其中 B1-1 属实施载体与项目实际不符、B1-3 使第 15 节覆盖断言失实、B1-5 使发布链无法闭环——按 16 号判级标准「阻塞问题：方案无法闭环 / A 声明的断言被证伪 / 影响现有能力正确性 / 产生数据不一致」与 A 自设放行门槛「无新的阻塞问题」，均不满足「通过」条件。

**B 审核结论：修订-需再审。** A 按第 10 节修订后须再次提交 B1 复审，重点复核 B1-1/B1-2/B1-3/B1-5 四项的落盘文本。

需求层面裁决建议（供用户决策，不等同于方案结语）：

**B1 的需求裁决建议：支持继续实施**——需求真实（全量刷新实证、证据链完整）、方向正确（保真成本从查询侧移到写入侧）、与既有红线零冲突；全部阻塞项均为存量与发布链实施细节，修订后可收敛，无重做必要。


---

# B1 第二轮复审（V0.2，2026-09-23）

> 复审对象：本文件 V0.2（A 按 B1 第一轮 11 项意见修订）。落盘说明：A 文内建议以 `## B2 审核结果` 命名新节；按 16 号「B 只在该 AP 文末写/更新 `## B1 审核结果`」，本轮复审仍由 B1 执行，故追加于 B1 节内文末，第一轮内容（上方）未改动。审核基于本轮重新扫描仓库与实际工作区，未采信 A 的处理记录自述。

## R2-0 工作空间版本核对

| 核对项 | A 的快照值 | B1 实测值 | 是否一致 |
|---|---|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` | 同（本轮 Bash cwd 即该路径） | 是 |
| 版本标识值 | Skill 3.30.3 / schema 0.17.0 | Project VERSION=3.30.3、skill.json=3.30.3、supportedWorkspaceSchema current=0.17.0；Portfolio VERSION=3.30.3 | 是 |
| 方案版本 | ap_version V0.2，status a_v0.2_pending_b1_rereview | 实读文件头一致 | 是 |
| B1 首轮节 | 应未被删改 | L688–941 完整在文，首轮结论原文未动 | 是 |

用户已显式指示第二轮复审，B1 据此开工。工作区侧无变化（集根与成员 .skill-version.json 仍 3.30.2/0.17.0）。

## R2-1 B1 自行扫描的目录与文件清单（本轮增量）

本轮在第一轮全量扫描基础上，重点复核修订涉及面：§5/§8/§8.2 的新载体描述（active-entities.json、13 列）、§7 新增 6 文件（migrate_workspace.py、sync_version.py、audit_release.py、README×2、模板、pack.ps1）、Q-011~Q-013、§18 新场景、§19.3 收口、AP-2/4/5。另对 V0.2 新引入的实现断言做了代码级实证（见 R2-6）。

## R2-2 对 A 需求理解的审核（V0.2）

V0.1 审核中三处偏差（触发式登记、alias 载体、证据链待决）已消除：§4 步骤 6/8/9 与 R2 定稿四约束逐条对回——不丢词（只增不删+键覆盖校验+冲突双行保留）、热度 AI 自动算且命中当时不写（收尾 `--flush-heat`）、回填不走人工确认（`--register` 自动 pending、`--correct` 用户纠正即改 confirmed）、触发式登记无感落盘（0 命中→定位→收尾登记）；§19.3 对 R4 两问显式收口（文件级、不建高风险分级器，沿用 00 确认级与 06 §8 Change Log）。R1 三验收口径（1 分钟级/零偏差/AI 独立维护前提）与「写入同次更新索引」取舍（哈希兜底，用户裁决本轮不收口写入口）一致。无新增理解偏差。

## R2-2.5 B1 对需求本身的独立辩论（第二轮）

维持第一轮结论：**必须加、支持继续实施**。本轮补充一点独立观察：V0.2 的修订全部是把已裁决需求写成与仓库实际一致的步骤（合并载体、行结构、登记闭环、发布链），没有借修订夹带新能力、没有改联邦目录、没有新建 wiki 目录——需求忠实性经第二轮文本核验成立。

## R2-3 对 A 目录扫描结果的审核（V0.2 增量核验）

| V0.2 声称 | B1 实测 | 是否一致 |
|---|---|---|
| alias_index 在 `context/active-entities.json`，`.state.json` 无此键 | `.state.json` 实测 6 键（facts_fingerprint/journal_fingerprint/facts/journal/views/source_digest_status）；refresh_views.py L1251 写出 active-entities | 一致（B1-1 修复成立） |
| 说法表 13 列，含路径与状态；旧 11 列逐列映射 | §5 列定义与 §8.2 映射表覆盖旧 11 列全部字段（含命中次数→热度、类别/context_hint/备注保留、纠错表/待确认表并入）；模板行同步进 §7/AP-4 | 一致（B1-2 修复成立） |
| 断言 13 按版本分叉（≥4.0.0 单包、根上不得有 Portfolio/SKILL.md、基线只要求 Project 树；≤3.30.3 双包） | audit_release.py L371-405 现状为双包断言，分叉设计可行且向后兼容 | 一致（B1-5①成立） |
| sync_version「4.0.0 起 Portfolio 无 SKILL.md 则跳过锁步不报错」 | 实测 sync_version.py L106-119 本就有 if-exists 守卫，树删后即静默跳过——该修改实为确认性修改，描述与实际行为一致 | 一致（B1-5②成立） |
| 迁移引擎 migrate_workspace.py、enforce 只调度 | migrate_workspace.py 2639 行（MIGRATIONS 分派+stamp_skill_version+ensure_stock_compiled 已绑闸）、enforce 172 行入口——§7/§8.2/AP-4 已按此定位 | 一致（B1-1/B1-5④成立） |
| audit 断言 12 计数口径 | 实测 n_rules 只数 `PROJECT/references/*.md`，能力目录不计入；Portfolio 规则迁入 `portfolio-skill/references/` 后 n_rules 不变，README×2 与 BLUEPRINT §1 的数量断言不会因搬迁 FAIL（README 安装/发布物描述仍须改，§7 已列） | 一致（本轮新核验，非阻塞） |

## R2-4 对文件级改动清单的审核

第一轮要求补的 6 个文件全部进入 §7 与 AP-4（migrate/enforce 分工、sync_version、audit、README×2、模板、pack.ps1），C9/C10 进 §14。Portfolio 整树「迁入校验后删除」处置明确，回滚口径与 AP-6/baselines/3.30.3 一致。17 号行的修改描述从「局部」升级为「全文表结构与写入句」——与 B1 第一轮「结构性改写」的判断一致。清单无缺漏。

## R2-5 对数据、索引、联动、测试的审核（增量）

- **热度写放大**：命中当时不写、收尾 `--flush-heat`、戳哈希去掉热度与最近命中两列、三写方互斥（§5/§18/Q-013）——机制自洽。哈希按「去两列后内容」计算是实现约定，实现时需保证去列后序列化稳定（同一写方唯一，可行）。
- **supersede 追随**：§8.2 第 7 步按 `_successor_id` 规则改指后继、无后继标废弃不删行；refresh_views 重建时只修死链不增行；Q-012 回归——投影时代的追随能力在静态表得到保留。
- **Q-011~Q-013**：登记、后继追随、戳不变性均有断言；Q-003 改为「这一次调用不写表」与收尾登记不再冲突。
- **集层 glossary-index**：仍为指针重生成、不抄全文，零数据源边界保持。

## R2-6 B1 第二轮新发现的问题清单

| 编号 | 问题 | 严重程度 | 是否阻塞执行 | 建议修复方式 |
|---|---|---|---|---|
| R2-1 | §8/§8.2「工作包 YAML 的 aliases」表述与实测不符：WP frontmatter 无 aliases 键；别名实为 refresh_views.parse_wps 派生（`aliases = [name, wp_id] + 功能点 + supersedes`，L214-227）。照字面读 YAML 会读空。因 alias_index 本身已含 WP 派生键、Q-006 有兜底，实际损失≈零，但表述必须改，防实现歧义与漏读 | 非阻塞 | 否 | §8.2 步骤 2 改为「按 refresh_views 同一 WP 解析取别名键（名称、编号、功能点、supersedes），复用解析函数，不另写一套」 |
| R2-2 | §6/§7 对 query-rules.md 迁入正文的修改描述未包含两条新硬步骤的规则化：①会话收尾 `--flush-heat` 钩子；②0 命中后收尾 `--register` 触发。漏写则 R2「无感登记/自动热度」在运行时不发生。另 §4 步骤 6「按查询路由打开至多 1 个事实文件」需注明「≤1 仅指为登记定位绑定目标；回答本身仍按 05 §2 路由预算」，防止被读成 0 命中时回答只许开 1 个文件 | 非阻塞 | 否 | §6/§7 query-rules 行修改描述补「迁入正文须含收尾钩子与 0 命中登记步骤」；§4 步骤 6 补半句限定 |
| R2-3 | §5 路径回填写方未指定：「查询时路径为空则…唯一命中才把路径写回该行」——三个子命令（--register/--correct/--flush-heat）均不覆盖此场景，与「能写它的只有三个子命令+合并+废弃修正」存在口径张力 | 非阻塞 | 否 | 明确路径回填走哪条路（如 `--register` 幂等更新既有行，或增设第四子命令），写进 §5 |
| R2-4 | 8.1 集层表 27~32 标「要」机器戳，但唯一对戳工具 query_locate 拒绝集根（退出码 4）、§4 步骤 11 集层查询只对成员根调用——集层文件的戳既无初始化执行者也无消费者，是死数据 | 非阻塞 | 否 | 集层表 27~32 的机器戳列改标「不适用（集层直读原件）」，或给 portfolio-skill 补集层戳机制；二选一，写明即可 |
| R2-5 | 文字残留：AP-2 回归行与 AP-4 回归行仍写「Q-001～Q-010／10 条阻断」，与 §13/AP-5 的 Q-001～Q-013（13 条）不一致 | 非阻塞 | 否 | AP-2/AP-4 两处同步为 Q-001～Q-013 |
| R2-6 | SKILL_BLUEPRINT.md 双包架构段（3.0.0 双包拆分描述）在 4.0.0 过时。实测 audit 断言 12 只校验 §1 的数字（数量口径不变不会 FAIL），故非阻塞；但架构文档漂移应防 | 仅建议 | 否 | 执行时更新 BLUEPRINT 架构段为单包+双能力目录；CHANGELOG 的 Blueprint Impact 标 full |

## R2-7 B1 给 A 的修订建议

R2-1～R2-5 属文本修订，可并入执行阶段首个 CR 或出 V0.3 一并落盘，无需再走 B 轮：①§8.2 步骤 2 别名键来源改为「复用 refresh_views 的 WP 解析」；②§6/§7 补迁入正文两条硬步骤+§4 步骤 6 加「≤1 仅指绑定定位」限定；③§5 指定路径回填的执行子命令；④8.1 集层表戳列二选一收口；⑤AP-2/AP-4 回归条目数字同步。R2-6 执行时顺手处理。

## R2-8 严重度映射表

| 编号 | 问题 | 严重度 | 判定依据 | 对照放行门槛 |
|---|---|---|---|---|
| R2-1 | 「YAML aliases」表述与代码事实不符 | 非阻塞 | 属表述修正；alias_index 已含派生键、Q-006 兜底，不破坏闭环、无数据不一致 | 不触发修订-需再审 |
| R2-2 | 迁入正文缺收尾/登记步骤的规则化 | 非阻塞 | 机制已在 §4 定义，属执行载体描述补句 | 不触发 |
| R2-3 | 路径回填写方未指定 | 非阻塞 | 补一句指定即可，不改变已定机制 | 不触发 |
| R2-4 | 集层戳无消费者 | 非阻塞 | 死数据不产生错误答案（集层直读原件），标「不适用」即消除 | 不触发 |
| R2-5 | AP-2/AP-4 数字残留 | 非阻塞 | 纯文字同步 | 不触发 |
| R2-6 | BLUEPRINT 架构段漂移 | 仅建议 | audit 不校验该段 | 不触发 |

## R2-9 B1 最终结论（第二轮）

**逐条复核结论**：第一轮 11 项（B1-1～B1-11）全部实质落盘 A 正文——B1-1 载体改对（active-entities.json 实证）；B1-2 十三列+逐列映射+三层同步齐备；B1-3 登记闭环（§4 步骤 6/--register/Q-011/来源枚举/§15 如实）成立；B1-4 禁写条款改写（禁模型手写、仅脚本可写）语义边界清晰；B1-5 六文件+断言 13 版本分叉+回滚口径全进清单；B1-6～B1-11（清单补齐、动态视图澄清首次入文、R4 收口、整树处置与口径改写、热度戳豁免与写方互斥、supersede 追随保留）逐条验证通过。12.6 表内 9 条关键断言第二轮重验仍未被证伪。历轮硬性澄清（shared-resource-index 动态视图）经三轮追讨**首次写入方案文本**。

**判级**：无阻塞级新问题；新发现 6 项全部为非阻塞建议/仅建议（表述级、文字残留级）。按 16 号判级标准「非阻塞建议 → 通过-待修订」，A 按第 R2-7 节修订后即可执行，无需再审。

**B 审核结论：通过-待修订。**

需求层面裁决建议（供用户决策，不等同于方案结语）：

**B1 的需求裁决建议：支持继续实施**——维持两轮一致结论；V0.2 已把已裁决需求落成与仓库实际一致的闭环步骤，剩余 5 项文本修订不涉及机制变更。

---

## B2 审核结果

> 2026-09-23。B2 独立复审，按 `16-upgrade-dual-agent.md` B 章节输出。审核前已自行重新扫描 Skill 项目目录与实际工作区，未采信 A 缓存结论，亦未因 B1 两轮"通过-待修订"而放松。B2 聚焦 B1 未覆盖的深度机制问题，不重复 B1 已逐项核验通过的内容。

### B2-0 工作空间版本核对

| 核对项 | A/B1 的快照值 | B2 实测值 | 是否一致 |
|---|---|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` | 同 | 是 |
| Skill 版本 | 3.30.3 / schema 0.17.0 | Project skill.json version=3.30.3, schema_version=0.17.0；Portfolio VERSION=3.30.3 | 是 |
| 方案版本 | V0.3，B1 第二轮结语"通过-待修订" | 实读文件头与 B1 节一致 | 是 |

实际工作区侧：全链通重构 `ai/.state.json` 含 200+ 文件指纹（facts 键），views 含 active_entities/brain 等 6 个视图；`ai/context/domain-glossary.md` 为 11 列结构（G001-G022 confirmed，来源 manual/contract）。与需求文件"执行包 3.30.3、工作区登记 3.30.2"吻合。

### B2-1 B2 自行扫描的关键文件（增量于 B1）

| 路径 | B2 读取深度 | 作用判断 | 与 A/B1 判断是否一致 |
|---|---|---|---|
| `migrate_workspace.py` L2167-2226（migrate_workspace 主函数）+ Grep "MIGRATION" 全文件 | 主函数入口、版本检测、能力检测 | 存量迁移真正引擎 | **不一致——A§9 与 B1 两轮均称"MIGRATIONS 分派表"，实测无此结构**（见 B2-问题1） |
| `migrate_workspace.py` L712/L793（capabilities 列表） | 能力注册机制 | 迁移按能力而非按版本分派 | A/B1 均未识别此机制 |
| `SKILL.md` L1-40（含 §2 工作模式集根逻辑 L19-21） | 入口描述与集根判断 | 单包后集根路由改造点 | **A§7 只说改 description，未覆盖集根逻辑改造**（见 B2-问题2） |
| `audit_release.py` 全文件 Grep "Portfolio"（16 处） | 断言 13 + PORTFOLIO 常量 L51 + 注释 L29-30 | 发布审计 | A 只提断言 13，未提常量与注释清理（见 B2-问题3） |
| `refresh_views.py` L1168-1257（run 全函数） | collect_facts 先于指纹比对、写出逻辑 | 增量改造核心 | A§3 只有概念，无 collect_facts 改造伪代码（见 B2-问题4） |
| `ChronoPM-Portfolio/SKILL.md` L1-20 | "须同时安装"口径 | 迁入口径改写 | A 已列，B2 确认需改 |
| `source-split-skill/CAPABILITY.md` | 能力目录形态范本 | query-skill/portfolio-skill 形态参照 | 一致 |

### B2-2 对需求理解的审核（B2 增量）

B1 两轮已核验需求理解无偏差。B2 补充一点：原始需求 SG-20260923-001 §2.3 诊断"保真机制错位"——把保真成本放在查询侧。A 方案的响应是"保真成本前移到写入/升级时刻"，方向正确。但 A 方案对"写入时刻"的定义不够清晰：是每次写入事实源后自动跑 refresh_views 增量更新？还是仍依赖用户手动触发？如果是后者，查询侧仍可能读到过期视图，"零偏差"目标存在缺口。建议 A 在 §3 明确增量指纹的触发时机与写入钩子。

### B2-3 对需求本身的独立辩论（B2）

维持 B1 两轮结论：**必须加、支持继续实施**。B2 补充独立观察：

1. **查询提速的真实瓶颈已被代码实证**：refresh_views.run() L1178 先 collect_facts（全库读取 200+ 文件），L1184 才比指纹——指纹缓存只省了写，没省读。这是 1 分钟目标不可达的根因，A 方案的增量改造对准了真问题。
2. **零偏差的真实痛点已被数据实证**：全链通词库 11 列无"路径"列，G017"全链通/企业通"等行无法直接定位到目标文件，查询时仍需二次解析。13 列改造对准了真问题。
3. **Portfolio 去双包是用户明确要求**，双包维护成本（版本锁步、双基线、双 zip）确实高，单包+能力目录是合理架构。

**B2 的需求裁决建议：支持继续实施**——但 A 方案在迁移机制、集根逻辑、增量实现细节上有 2 项阻塞缺口，需修订后执行。

### B2-4 B2 发现的问题清单

| 编号 | 问题 | 严重程度 | 是否阻塞执行 | 建议修复方式 |
|---|---|---|---|---|
| B2-1 | **迁移机制假设错误**：A§9 称"在 MIGRATIONS 分派表追加 4.0.0 条目：migrate_v400_glossary + migrate_v400_incremental"，B1 两轮亦称"MIGRATIONS 版本分派"。但实测 migrate_workspace.py **无 MIGRATIONS 字典**，实际机制是 `get_capabilities_since(version)` 返回新增能力列表（L712 capabilities 注册、L2223 调用），按能力执行迁移函数。按 A 的假设写迁移代码将找不到入口，4.0.0 存量合并无法执行 | 阻塞 | 是 | §9 改为：在 `get_capabilities_since()` 中注册 4.0.0 新能力（如 `glossary_merge_13col`、`fact_stamps_init`），编写对应迁移函数；明确能力与版本的映射关系（4.0.0 引入哪些能力） |
| B2-2 | **SKILL.md 集根逻辑改造不完整**：A§7 只说"description 改口径：项目集/跨项目加载 portfolio-skill 能力目录"。但 SKILL.md L19-21 的集根判断是核心行为逻辑——当前集根下"禁止单项目写入，材料投喂/日报/入库/混报/进度表/xlsx/csv 交 ChronoPM-Portfolio，跨项目查询同样交 Portfolio，未加载则提示安装"。迁入 portfolio-skill 后，这里需要改为"加载 portfolio-skill/references/portfolio-rules.md，按集层规则处理"，包括：集根检测后如何触发 portfolio-skill 加载、"未加载则提示安装"改为"未加载则提示启用能力目录"、P-HANDOFF-WRITE/ACCEPT 调用关系是否变化。A 方案未明确这些改造细节 | 阻塞 | 是 | §7 SKILL.md 行补"集根逻辑改写"：L19-21 的 ChronoPM-Portfolio 引用全部改为 portfolio-skill 能力目录加载；明确集根下的写入/查询路由；P-HANDOFF 系列调用关系保持不变（仍由 portfolio-skill 规则定义） |
| B2-3 | **audit_release.py Portfolio 引用清理不全面**：A§10 说"断言 13 从双包一致性改为单包自洽"。但 audit_release.py 有 16 处 Portfolio 引用，包括 L51 `PORTFOLIO = ROOT / "ChronoPM-Portfolio"` 常量定义、L29-30 模块注释。删除断言 13 双包检查后，PORTFOLIO 常量和注释也需清理。更重要的是，baselines/{version}/ 目录是否还需要 ChronoPM-Portfolio 子目录——4.0.0 基线只需要 Project 树，但基线生成流程可能仍在生成双基线 | 非阻塞 | 否 | §10 补：audit_release.py 同步删除 PORTFOLIO 常量（L51）与模块注释（L29-30）；确认基线生成流程 4.0.0 起只生成 Project 单树 |
| B2-4 | **增量指纹改造缺少 collect_facts 关键逻辑**：A§3 说"collect_facts 改为先读 .state.json 的 facts 指纹，只对变化文件重新 hash 和读取"。这是本次升级最核心的性能改造，但 A 只有概念描述，无改造伪代码。关键未决点：①如何检测新增/删除文件（遍历目录 vs 旧指纹对比）；②.state.json 不存在或损坏时的 fallback（全库扫描）；③指纹对比用 mtime 快速判断还是直接 hash（若直接 hash 仍要读文件内容，提速有限）；④增量模式下 facts_fingerprint 如何重新计算 | 非阻塞 | 否 | §3 补 collect_facts 增量改造伪代码或关键逻辑说明，至少覆盖：新增/删除检测、损坏 fallback、mtime 快速路径、facts_fingerprint 重算策略 |
| B2-5 | **13 列词库迁移的"路径"列旧行处理**：A§8.2 说旧 11 列→新 13 列，"路径"列旧行默认空。但"路径"是说法的关键属性（文件/对话/系统），实测全链通词库 G001-G022 来源为 manual/contract，若路径全空，这些行在 4.0.0 查询路由中无法定位目标文件，与"零偏差"目标矛盾 | 非阻塞 | 否 | §8.2 补：迁移时根据"来源"列推断路径——source=manual→对话，source=contract/分册→文件，source=system→系统；无法推断的标"待补"并在首次命中时由 --fill-path 回填 |
| B2-6 | **只读模式命名与场景不清晰**：A§4 说"--read-only 模式：不写 .state.json、不写 views、不写词库"。但 refresh_views 的核心价值就是生成 views 和 .state.json，只读模式下不写这些则下次运行仍全库扫描。需明确此模式的使用场景——若为查询热路径专用，应命名为 `--query-fast-path` 并明确不替代正常 refresh_views | 仅建议 | 否 | §4 明确只读模式的使用场景与命名；若为查询热路径专用，建议改名并写清与正常 refresh_views 的分工 |

### B2-5 严重度映射表

| B2 问题编号 | 严重度 | 判定依据 | 对照放行门槛 |
|---|---|---|---|
| B2-1 | 阻塞 | A 的实施路径与项目实际不符（16 号审核包第 4 条）；迁移代码找不到入口 → 存量合并不执行 → 工作区无法升 4.0.0 | 放行门槛"无新的阻塞问题"不满足 |
| B2-2 | 阻塞 | 集根逻辑是核心行为，未改造则集根工作区仍引用已删除的 ChronoPM-Portfolio → 跨项目功能失效 | 放行门槛不满足；影响现有能力正确性 |
| B2-3 | 非阻塞 | 常量/注释残留不影响断言执行，但代码整洁度与基线生成需确认 | 不触发修订-需再审 |
| B2-4 | 非阻塞 | 核心性能改造无伪代码，实现时可能走偏，但机制方向已明确 | 不触发 |
| B2-5 | 非阻塞 | 旧行路径空可通过 --fill-path 后续回填，但首次查询体验受损 | 不触发 |
| B2-6 | 仅建议 | 命名与场景澄清，不影响机制 | 不触发 |

### B2-6 B2 给 A 的修订建议

1. **§9（B2-1）**：删除"MIGRATIONS 分派表"表述，改为"在 `get_capabilities_since()` 能力注册机制中追加 4.0.0 新能力"；列出 4.0.0 引入的能力名称（如 `glossary_merge_13col`、`fact_stamps_init`）及对应迁移函数；明确能力与版本的映射。
2. **§7（B2-2）**：SKILL.md 修改描述从"description 改口径"扩展为"description + §2 集根逻辑全量改写"；写明集根检测后 portfolio-skill 的加载方式、"未加载"提示语变更、P-HANDOFF 调用关系。
3. **§10（B2-3）**：audit_release.py 修改项补"删除 PORTFOLIO 常量与模块注释"；确认基线生成流程 4.0.0 起单树。
4. **§3（B2-4）**：补 collect_facts 增量改造伪代码，覆盖新增/删除检测、损坏 fallback、mtime 快速路径、facts_fingerprint 重算。
5. **§8.2（B2-5）**：补旧行路径推断规则（manual→对话、contract→文件、system→系统）。
6. **§4（B2-6）**：明确只读模式场景与命名。

### B2-7 B2 最终结论

**逐条复核结论**：B1 两轮审核的 17 项问题（B1-1～B1-11 + R2-1～R2-6）A 均已实质落盘，B2 独立重验未发现 B1 误判（除迁移机制表述外——B1 两轮均沿用了 A 的"MIGRATIONS 分派"表述，未独立核实代码实际机制）。12.6 表内 9 条关键断言 B2 重验仍未被证伪。

**判级**：B2 新发现 2 项阻塞问题（B2-1 迁移机制假设错误、B2-2 集根逻辑改造不完整），均属"A 的实施路径与项目实际不符"或"影响现有能力正确性"，按 16 号判级标准与 A 自设放行门槛"无新的阻塞问题"，不满足"通过"条件。

**B2 审核结论：修订-需再审。** A 按 B2-6 修订后须再次提交 B 复审，重点复核 B2-1（迁移机制）与 B2-2（集根逻辑）两项的落盘文本。B2-3～B2-6 为非阻塞/建议项，可与阻塞项一并修订，无需单独再审。

需求层面裁决建议（供用户决策，不等同于方案结语）：

**B2 的需求裁决建议：支持继续实施**——需求真实、方向正确、与既有红线零冲突；2 项阻塞均为实施机制细节（迁移注册方式、集根路由改写），修订后可收敛，无重做必要。

---

## B2 第二轮复审（V0.4，2026-09-23）

> 复审对象：本文件 V0.4（A 按 B2 第一轮六项意见修订）。本轮重新扫描仓库代码与方案落盘文本，未采信 A 修订记录自述，亦未改 B2 第一轮正文。

### R2B-0 工作空间与版本核对

| 核对项 | A 的快照值 | B2 实测值 | 是否一致 |
|---|---|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` | 同 | 是 |
| Skill 版本 | 3.30.3 / schema 0.17.0 | 同（未动技能文件） | 是 |
| 方案版本 | V0.4，状态待 B2 复审 | 文件头 ap_version=V0.4，L23 状态声明一致 | 是 |
| B2 第一轮节 | 应未被删改 | L1048-1174 完整在文，第一轮结论原文未动 | 是 |

### R2B-1 阻塞项复核（重点）

#### B2-1（迁移机制）——已正确修订 ✅

A 在 §7.2（L188-198）全面改写迁移入口描述，B2 逐条对回代码：

| §7.2 断言 | B2 代码实测 | 是否一致 |
|---|---|---|
| 无 MIGRATIONS 字典；版本表是 VERSION_CAPABILITIES | `VERSION_CAPABILITIES` 定义于 L124 | 是 |
| get_capabilities_since() 从当前 skillVersion 之后截表，供打印和缺目录检查 | `get_capabilities_since` 定义于 L912，L916 遍历 VERSION_CAPABILITIES | 是 |
| 真正干活的是 migrate_workspace() 里 needs_v390 这类判断 | `needs_v380` L2330、`needs_v390` L2342，均在 stamp_skill_version 之前 | 是 |
| 4.0.0 在 VERSION_CAPABILITIES 末尾加一条（capabilities=speech_table_merge/fact_stamps_init，new_dirs/new_files 为空） | 结构与现有条目格式兼容，仅检测打印 | 是，设计可行 |
| 加 needs_v400 判断（版本/13列/fact_stamps 覆盖三条件） | 与 needs_v380/v390 同款模式 | 是 |
| 成员根调用合并+戳初始化，失败 return 不盖戳；集根只重写 glossary-index 指针 | 与 §8.2 集根/成员分工一致 | 是 |
| 版本已匹配时存量检查须含同一套条件 | 对应现有 L2215-2220 分支 | 是 |

**结论：B2-1 阻塞已消除。** §7.2 与代码实际机制完全一致，实现入口明确，无残留 MIGRATIONS 表述。

#### B2-2（集根逻辑）——已正确修订 ✅

A 在 §7.1（L174-186）补全集根改写，B2 逐条对回 B2 第一轮要求：

| B2 第一轮要求 | §7.1 落盘内容 | 是否覆盖 |
|---|---|---|
| description 去 Portfolio 引用 | L180 front matter description 去掉「请安装并调用 ChronoPM-Portfolio」，集层触发词留在本技能 | 是 |
| 全面清理 Portfolio 引用（不止 description） | L181 列出 §1 v3.0.0 句、§2（1）（2）（3）、§5.3、路由表、§15 指针、底线 12——凡「另装/调用 Portfolio」都改为加载 portfolio-skill/references/ | 是，覆盖面完整 |
| 集根检测后如何触发 portfolio-skill 加载 | L183 集根投喂/日报/入库/混报/进度表/xlsx/csv/跨项目查询加载 portfolio-skill 已迁入原规则（含原 01 §2.1、§2.2），包内缺文件报规则缺失 | 是 |
| 「未加载则提示安装」改为「提示启用能力目录」 | L183「不提示另装一个技能」 | 是 |
| P-HANDOFF 调用关系是否变化 | L184 P-HANDOFF 调用关系不变：集层规则发起、写过程进 Project、--project-root 仍是成员根、只读五条不放宽 | 是 |
| 集根检测本身保留 | L182 集根检测不变，仍禁止集根当单项目写入 | 是 |

**结论：B2-2 阻塞已消除。** §7.1 覆盖集根逻辑全部改造点，无残留「另装 Portfolio」口径。

### R2B-2 非阻塞/建议项复核

#### B2-3（audit 常量/注释/基线）——已采纳并落盘 ✅

L160 与 L629（AP-4）均明确：断言 13 改单包，删除 PORTFOLIO 常量（约 L51）与文件头双包注释（约 L29-30），4.0.0 基线只含 Project 树。落盘文本与 B2 第一轮建议一致。

#### B2-4（collect_facts 增量伪代码）——A 不采纳，B2 认同理由 ✅

A 理由：方案不把 collect_facts 改成按变化文件重算；提问不调用 refresh_views；先遍历目录再决定读谁是已否决的慢路径。

B2 独立复核后**收回第一轮建议**：我重新梳理了方案架构——查询提速完全由 `query_locate.py` 只哈希命中文件实现，refresh_views 仅在写入后与显式重建时运行，不在查询热路径上。collect_facts 的全库扫描不影响查询速度，无需改造。我第一轮建议基于「方案要改 collect_facts」的误解，实际方案从未以此为提速手段。L93 已写明损坏 fallback 仍只哈希命中文件、不走全库。**A 不采纳成立。**

#### B2-5（路径列旧行推断）——A 不采纳，B2 认同理由 ✅

A 理由：路径列是 ai/ 下具体文件相对路径；旧词库行是「原词→标准词」无文件指针，留空正确；按来源写「对话/文件/系统」会让脚本尝试打开不存在的路径。

B2 独立复核后**收回第一轮建议**：我第一轮把「路径」列误解为来源渠道分类（文件/对话/系统），实际该列承载的是 `wps/WP-017.md`、`todos/{date}/{owner}.md` 这类可直接打开的相对路径。旧词库行确实无此信息——manual 行无对应文件，contract 行指向的拆解产物也不是说法直接绑定的目标。留空后由 `--fill-path` 在首次命中实际文件时回填，是正确机制。我建议的 manual→对话/contract→文件推断确实会产生无法打开的伪路径。**A 不采纳成立。**

#### B2-6（只读模式）——A 不采纳，B2 认同理由 ✅

A 理由：方案不设 --read-only；查询统一走 query_locate.py；refresh_views 只在写入后重建视图。

B2 独立复核：L93 已明确「不给 refresh_views.py 增加 --read-only 或 --query-fast-path」。V0.4 方案中无只读模式设计，第一轮所指表述已不存在。**A 不采纳成立。**

### R2B-3 B2 第二轮新发现问题

无。本轮未发现新的阻塞或非阻塞问题，未发现 A 借修订夹带新能力、改联邦目录或新建 wiki。

### R2B-4 B2 第二轮最终结论

**逐条复核结论**：

- 第一轮 2 项阻塞（B2-1 迁移机制、B2-2 集根逻辑）均已实质落盘，B2 代码级实测确认修订与仓库实际机制一致，阻塞消除。
- B2-3 已采纳落盘（常量/注释/基线清理）。
- B2-4/5/6 A 不采纳，B2 独立复核后认同 A 的理由，并收回第一轮建议（三项均源于 B2 第一轮对方案架构的误解：误判 collect_facts 为改造对象、误解路径列语义、基于已不存在的只读模式表述）。
- 12.6 表内 9 条关键断言本轮重验仍未被证伪。

**判级**：无阻塞级问题，无新增非阻塞问题。按 16 号判级标准，达「通过」条件。

**B2 审核结论：通过。** 无需再审。方案可在用户说「同意执行」后进入实施；执行阶段首个 CR 须按 §7.1/§7.2 落盘文本实施，不得回退到 MIGRATIONS 表述或仅改 description 的旧方案。

需求层面裁决建议（供用户决策，不等同于方案结语）：

**B2 的需求裁决建议：支持继续实施**——维持两轮一致结论；V0.4 已把全部已裁决需求落成与仓库实际一致、可闭环的方案，无阻塞、无重做项。

---

## 升级结果审核（B2，2026-09-23）

> 审核对象：A 自称「升级完了」的 4.0.0 实际产物（技能包 + 实际业务工作区）。B2 独立扫描、独立执行迁移验证，未采信 A 的完成声明。审核覆盖「技能包文件」与「工作区存量迁移」两部分。

### R-0 审核方法与关键动作

1. 扫描开发仓目录结构、skill.json、两个能力目录、SKILL.md、migrate/audit/sync/pack 脚本、模板。
2. 跑 `audit_release.py 4.0.0`：**17/17 PASS**。
3. 扫描实际业务工作区四个版本戳（集根 + 全链通/企业通/信用监管三成员）、词库列结构、.state.json。
4. 对全链通成员实际执行 `migrate_workspace.py --target-version 4.0.0`（先 dry-run 后实跑），验证迁移闭环。

### R-1 技能包（开发仓）侧——已完成且正确 ✅

| 验收项 | 实测结果 |
|---|---|
| skill.json | version=4.0.0；description 改为「单项目读写，跨项目只读归集都在这一个技能里。项目集规则在 portfolio-skill，查询在 query-skill」；modes=single；versionHistory/blueprint 4.0.0 条目齐 |
| ChronoPM-Portfolio 整树 | 已删除，根目录无残留 |
| query-skill | CAPABILITY.md（禁 SKILL.md）+ references/query-rules.md + scripts/query_locate.py + glossary_table.py；子命令 --register/--correct/--flush-heat/--fill-path 齐；fact_stamps 读写逻辑在 |
| portfolio-skill | CAPABILITY.md + 6 规则（01-readonly-boundary～06-version-health）+ 11 模板；无 SKILL.md |
| SKILL.md 集根逻辑 | L19/21 改为加载 portfolio-skill 的 01-readonly/02-aggregation 规则，「目录里没有就报规则缺失，不提示另装技能」；集根禁写保留；P-HANDOFF 关系不变 |
| migrate_workspace.py | VERSION_CAPABILITIES 4.0.0 条目（speech_table_merge/fact_stamps_init，L912）；needs_v400（L2372）；apply_member 接线（L70-73） |
| audit_release.py | 断言 13 改单包（L370-380）；PORTFOLIO 常量已删；双包注释已改 |
| sync_version.py | L106-107 加 isdir+isfile 守卫，Portfolio 缺失即跳过不报错 |
| pack.py | L320-321 companion=None，不打第二包 |
| domain-glossary-template | 13 列；第 2/3 表标注「已并入第 1 表，禁止再追加」 |
| references/05 | 已变指针页，正文在 query-skill |
| 发布审计 | audit 17/17 PASS；回归 1041；baselines/4.0.0 存在；模拟 pack 158 文件 |

**结论：技能包文件侧达到可打 4.0.0 分发包的状态。**

### R-2 实际业务工作区侧——迁移失败，升级未完成 ❌（核心问题）

B2 实测四个版本戳与数据：

| 工作区 | .skill-version.json | 词库 | .state.json |
|---|---|---|---|
| 集根（市监重构/ai） | **3.30.2**，skill=chrono-pm-portfolio | — | — |
| 全链通重构 | **3.30.2**，mode=single | **旧 11 列** | **无 fact_stamps** |
| 企业通重构 | **3.30.2** | 未迁移 | — |
| 信用监管登记注册重构 | **3.30.2** | 未迁移 | — |

B2 实际执行全链通成员迁移，结果：

```
v4.0.0 (schema 0.17.0): speech_table_merge, fact_stamps_init
... compile_source_digests ...
GAP SRC-046 外商投资企业我要变更 没有可确定的需求
GAP SRC-047 ... （共 76 条）
done wrote=0 skip=96 fail=76
存量未完成，不得更新 skillVersion，不得称升级成功
```

**失败根因链**：

1. `ensure_stock_compiled()`（migrate_workspace.py L50-75）在成员根先跑 `compile_workspace()`，**compile 通过后才调用 `apply_member()`（说法表 13 列合并 + fact_stamps + 盖 4.0.0 戳）**。
2. 76 个政务事项源（目录名形如 `SRC-046 外商投资企业我要变更`，2026-08-29 批量投喂）已完成模块级 ATOM 拆解（_index 显示「ATOM 28 + FACT 9」），但 ATOM **未归集到 canonical/REQ 需求**，compile 判「没有可确定的需求」，返回非 0。
3. compile 闸门拦截 → `apply_member` 根本未执行 → 词库仍 11 列、无 fact_stamps、版本戳仍 3.30.2。

**影响**：用户工作区无法在 4.0.0 查询新路径下工作——query_locate 依赖 fact_stamps 与 13 列说法表，两者均未建立。三个成员 + 集根全部未升级。

### R-3 次要残留（代码整洁，不阻塞打包）

| 编号 | 位置 | 问题 |
|---|---|---|
| R3-1 | SKILL.md L205 | 「09 号已退役，内容在 **ChronoPM-Portfolio**（保留退役页…）」——Portfolio 已删，应改为「内容在 portfolio-skill/references/」 |
| R3-2 | pack.ps1 L14-15、L118-120 | 文件头双包注释、excludeDirs 中「ChronoPM-Portfolio」未清理（目录已删故无害，但文本过时） |
| R3-3 | pack.py L15-18、L92、L104-110、L152、L221 | find_companion 已成死代码（L321 直接 None），文件头/函数双包注释未清理 |
| R3-4 | sync_version.py L8 | 注释「Portfolio 版本锁步」已过时（4.0.0 起不锁步） |

### R-4 B2 审核结论

**不通过——升级未完成，不得称升级成功。**

- 技能包文件侧：**通过**（audit 17/17，可打 4.0.0 分发包）。
- 实际工作区侧：**不通过**（4 个版本戳全部 3.30.2、词库 11 列、无 fact_stamps；迁移实跑 fail=76 被闸门拦截）。这是本次升级的核心交付物（让用户工作区跑在 4.0.0 上），未完成即整体不通过。

### R-5 放行前必须完成的动作

1. **处理 76 个 GAP 源（关键决策，需 PM 拍板）**，三选一：
   - **A. 完成需求归集**：把 76 源的 ATOM 归集到 canonical/REQ（业务工作量最大）；
   - **B. 登记薄源/不归集（推荐先评估）**：由 PM 确认这些源按 3.26「薄源」或 source_digest_status 标记为不归集，使 compile 放行；
   - **C. 解耦闸门**：修改 `ensure_stock_compiled`，让说法表 13 列合并（纯词库结构改造，与源归集无因果）先执行、源 GAP 仅 P2 提示——但此改动改变 3.30.2 以来「存量不过不盖戳」原则，**必须先走 B 审核，不得施工时自行解耦**。
2. GAP 处理后，对三个成员根依次重跑迁移（确认词库变 13 列、fact_stamps 初始化、盖 4.0.0 戳），再对集根跑（刷新 glossary-index 指针、盖戳）。
3. 清理 R3-1～R3-4 四处残留文本。
4. 复验：四个版本戳均 4.0.0；各词库 13 列；.state.json 含 fact_stamps；抽测一次 query_locate 实际提问，验证只哈希命中文件、N>0。

### R-6 给用户的裁决提示

技能包本身做得完整、审计全绿；卡住升级的是 2026-08-29 批量投喂的 76 份政务事项报告「拆了但没归集需求」这个**历史数据状态**，不是 4.0.0 新引入的 bug（compile 脚本 4.0.0 未改动）。建议先在 R-5 的 A/B/C 中决策 GAP 处理口径——其中 B（登记薄源）若 PM 认可可最快放行，C（解耦闸门）需补一轮审核。在 GAP 处理完并复验通过前，本次 4.0.0 升级应保持「未完成」状态。

---

## 技能包专项审核（B2，2026-09-25）

> 应用户要求，本轮**只审技能包（Skill）本身是否升级完**，不审实际业务工作区。重新逐项扫描技能包文件并实跑脚本/审计，未采信此前结论。

### S-1 核心改动落盘核对

| # | 验收项 | 实测结果 |
|---|---|---|
| 1 | skill.json | version=4.0.0；description「单项目读写，跨项目只读归集都在这一个技能里。项目集规则在 portfolio-skill，查询在 query-skill」；modes=single；versionHistory/blueprint 4.0.0 齐 |
| 2 | ChronoPM-Portfolio 整树 | 已删除，根目录无残留 |
| 3 | query-skill | CAPABILITY.md（禁 SKILL.md）+ references/query-rules.md + scripts/query_locate.py + glossary_table.py；--register/--correct/--flush-heat/--fill-path 子命令齐；fact_stamps 读写在 |
| 4 | portfolio-skill | CAPABILITY.md + 6 规则（01-readonly-boundary～06-version-health）+ 11 模板；无 SKILL.md |
| 5 | SKILL.md | description + §2 集根逻辑（L19/21）改为加载 portfolio-skill 的 01/02 规则、「不提示另装」；此前 L205「内容在 ChronoPM-Portfolio」残留**已清理** |
| 6 | migrate_workspace.py | VERSION_CAPABILITIES 4.0.0 条目（speech_table_merge/fact_stamps_init）；needs_v400；apply_member 接线 |
| 7 | audit_release.py | 断言 13 改单包；PORTFOLIO 常量与双包注释已删 |
| 8 | sync_version.py | isdir+isfile 守卫，缺失即跳过；过时注释已清 |
| 9 | pack.py | companion=None 不打第二包；find_companion 死代码已删 |
| 10 | references/05 | 已变指针页 |
| 11 | references/06 | scope-register 已入 §2.1 权威清单（L135）；index 标注「不是存在性判据」（L335） |
| 12 | references/17 | 说法表口径已更新（7+7，登记/纠正/补路径/加热度只经 query_locate） |
| 13 | 发布审计 | **audit 17/17 PASS**；回归 1041；baselines/4.0.0 在；模拟 pack 158 文件 |

### S-2 发现的问题

| 编号 | 问题 | 严重度 | 是否阻塞 |
|---|---|---|---|
| S2-1 | **词库模板与规则/脚本列形态不一致**：`assets/templates/domain-glossary-template.md` 第 1 表是**一张 13 列单表**；但 17 规则 L243 明确「第 1 表固定 7 列 + 第 1b 表 7 列，**禁止并成超过 7 列的表**」，glossary_table.py 的 MAIN/META 与 render_table 也输出 **7+7**。B2 实测：脚本能容错读取 13 列模板（load_rows 正确解析 5 行），merge_glossary 会经 _rewrite 自动收敛为 7+7，**不报错、不丢数据，功能闭环成立**；但新工作区 init 从模板复制出的词库初始即 13 列（违规形态），需等首次 merge 才合规。模板作为初始权威范本应直接是最终 7+7 形态 | 非阻塞 | 否 |
| S2-2 | pack.ps1 L116 注释、L118 excludeDirs「ChronoPM-Portfolio」未清；pack.py L137/L206 两处 companion 注释残留 | 仅整洁 | 否 |

### S-3 结论

**技能包已升级完成，可发布。** 13 项核心改动全部实质落盘且内部自洽，发布审计 17/17 PASS，无阻塞问题。

- S2-1（模板 13 列 vs 规则/脚本 7+7）为**非阻塞规范不一致**：脚本已具备容错与自动收敛能力，不影响功能；建议收尾时把模板直接改为 7+7 两表，使新工作区初始化即合规，并消除与 17 规则的字面矛盾。
- S2-2 为注释/排除项整洁问题，Portfolio 目录已删故无害，顺手清理即可。

**B2 判级：通过。** 技能包侧 4.0.0 升级完成；S2-1/S2-2 作为建议项，不构成发布阻塞，是否在本次收尾修理由用户决定。
