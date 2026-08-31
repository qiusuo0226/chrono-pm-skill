---
CR ID: CR-20260831-001, CR-20260831-002, CR-20260831-003, CR-20260831-004
AP Version: 0.5
Status: pending_review
Target Skill Version: 3.22.0
Workspace Schema: 0.16.0（不升）
Created At: 2026-08-31
Updated At: 2026-08-31
Author: Agent A
---

# 升级方案审查文档（3.22.0）

> 设计阶段只改本文件。每周期限 1 个 AP，禁止拆文件、禁止附加后缀。  
> CR / IA 仅在用户准许执行后创建（16 号 §2.1a）。本文件不是施工清单；落地进 `upgrade-to-3.22.0.md` 后删除本草稿。  
> **禁止操作**业务示例空间 `C:\Users\qiusuo\Downloads\市监重构项目管理`。

请审查以上方案。B 审核通过且用户回复「同意执行」后，再按最小修改方案实施。

---

## 0. 工作空间版本快照（已由用户确认）

| 项目 | 值 |
|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` |
| 版本标识来源 | `ChronoPM-Project/skill.json` version + git HEAD |
| 版本标识值 | Skill **3.21.1**；workspace schema **0.16.0**；HEAD `e6954e1`（2026-08-30 17:56:57 +0800） |
| 快照生成时间 | 2026-08-31 |
| 工作树 | 写本 AP 前干净；本文件为设计阶段唯一新增 |
| 双包 | Project / Portfolio 均为 3.21.1 |
| 用户确认状态 | ✅ 路径与 R1/R2/Q1–Q5 已确认。2026-08-31 增量：用户要求把「换对话查询仍慢 / 不要会过期的记忆」写入本 AP（R3） |

明确不读不写：`C:\Users\qiusuo\Downloads\市监重构项目管理`。

---

## 0.1 原始需求照抄

1. 优化 AI 间断性提问：突然问「是否执行此方案」，用户不知道要执行什么。这一类属于提示优化，加到 Project 下专门强化人机交互的假 skill。须核对该问题是否已在前序版本处理。截图：`C:\Users\qiusuo\Downloads\2026-08-27_094722.png`。
2. 一份拆解/整理记录做了几十分钟，怀疑链路有问题。整理对象：`C:\Users\qiusuo\Downloads\仇索发起的视频会议(1)\仇索发起的视频会议.docx`（内容不多）。截图：`C:\Users\qiusuo\Downloads\2026-08-31_101335.png`。
3. 按《Agent双向Skill升级提示词-需求辩论版》由 Agent A 出升级方案。代码空间为本仓库；方案不得操作业务示例空间；升级方案须考虑在升级执行脚本中处理历史版本老数据。
4. （2026-08-31 增量）查询链路实际问题：历史问题换个对话还是会加载很慢，没有记忆；但加了记忆又怕更新不及时。要求想清楚处理方式并加进本方案。截图：TraeWork「住所核验国庆上线包含哪些地市」，首次约 4 分 25 秒，模型自述扫了 100+ 文件、无检索路径存档，并提议把定位关系手写进项目索引。
5. （2026-08-31 增量）推导约 80% 靠当前聊天上下文，Skill 不会把对话存本地；下次不投喂就会偏。记多了无结构则链路变长、回复变慢；过于结构化又不便于 PM 随便说都能记。截图：`C:\Users\qiusuo\Downloads\2026-08-31_135523.png`（`/epoint-gateway/zwww/sds` 是否干废；模型承认「江苏一体化网关」是上一轮推断不是检索命中）。

---

## 0.2 需求基线（用户已裁决，辩论终止）

| 项 | 裁决 |
|---|---|
| 总体 | **继续实施**：R1 残差 + R2 会议链 + R3 派生定位 + **R4 口低闸证高闸（术语/推断落盘节流）** |
| Q1 R1 | **仅残差**：不把 3.18.0 已落地的假执行门当新能力重做；只补提问对象化 + 宿主误弹拆穿 |
| Q2 T-A4 | **维持强制落待办**（写完纪要之后）；改 `examples/08`，禁止再问「要不要建待办」 |
| Q3 无 Python | **不跳过结转**；先落纪要，再手工结转并告知会较慢 |
| Q4 版本 | **3.22.0 Minor**；schema **保持 0.16.0** |
| Q5 老数据 | 疑似会议误拆 SRC：**只出清单，不自动搬**；写回必须 `--migrate-business` |
| R3 查询慢 | **采用指纹派生定位，禁止会话记忆，禁止手写「主题→文件」进 index**。每一次查询先比指纹；过期则重建再答。 |
| R4 口低证高 | **PM 随便说可以进 pending；AI 自推默认不落盘；升 confirmed 必须认命题不是认「推得还行」。查询轮禁止自动写词库。** 截图 `2026-08-31_135523.png`：sds/zwww 属术语不是事实；「80%」不是 T1。 |

A 原辩论：R1 不建议当新能力；R2 必须加。用户确认按上表执行。R3 为用户增量要求，辩论见 §0.4，结论纳入基线。此后 A/B 只忠实执行本基线，不得以合理性为由再推翻。

---

## 0.3 Agent A 对需求的理解（已对齐基线）

| 点 | 理解 |
|---|---|
| R1 | 对外中途提问必须带对象（已做 / 请你选什么 / 选了会怎样）。空壳「是否执行此方案」属假执行门。落点只能是 `ChronoPM-Project/reply-norm-skill/`（能力目录，禁止 `SKILL.md`）。3.18.0 `CR-20260827-005` 已收主体（截图 1 即 `RN-003` 反例）；本次只补残差，不改 SKILL 底线 14–16 与 05 短条的同文结构。 |
| R2 | 「整理/拆解」腾讯会议导出耗时过长，根因是过程链串台，不是文档体积。附件约 56KB / 2.8 万字，后半已有结构化纪要。须切开会议 vs 源文档，先写 `meetings/` 再结转，脚本走技能包路径，花名册空表回退。 |
| 老数据 | `migrate_workspace.py` 默认 dry-run 列出疑似会议误拆；`carryover_step0.py` 运行时回退空花名册。升级执行不对市监跑 migrate。 |
| R3 | 换对话慢不是因为缺聊天记忆，而是 3.21 快路径没被走、SRC 没进 alias、CQ-5 被理解成必须全库实扫。方案：派生定位 + 指纹失效，不是记忆。 |

---

## 0.4 R3 需求辩论（查询链路 / 记忆过期）

现场（TraeWork，约 4 分 25 秒）：问「住所核验国庆上线哪些地市」。模型说（1）本会话第一次加载技能；（2）关键词出现在 100+ 文件，排除企业通/信用监管后还要对 todos、WP、风险、SRC 再对一遍；（3）没有检索路径存档；（4）建议把「住所核验→关键文件」手写进 `wps/_index`。

**(1) 合理性**

| 论证项 | 结论 | 论据 |
|---|---|---|
| 是否符合定位 | 符合 | 查询是核心读路径；SKILL §5.3 / 05 / P-VIEWS / P-RESOLVE 已规定「brain + 指纹 + 最多 1～3 个事实文件」 |
| 是否有真实场景 | 有 | 截图：换对话仍全库扫；用户明确怕记忆过期 |
| 是否与现有能力重复 | **机制已有、缺口是没被执行 + 覆盖不全** | 3.21.0 已有 `brain.md`、`active-entities.json` `alias_index`、`.state.json` 指纹、BRN-003、ALI-001、CQ-5 实读禁缓存、底线 17 禁止只改 brain/index。`refresh_views.py` **零处**解析 `requirements/sources/`，SRC-055「住所核验」进不了 alias。brain「## 别名跳转」只写「见 json」，05 简单查询又不加载 00，P-VIEWS 命令不在 05 文首 |
| 支持（≥2） | ① 对话记忆换会话必丢，这是对的，不该当项目记忆。② 手写「主题→文件」进 index 正是用户害怕的过期记忆，且违反底线 17。③ 指纹派生：事实变 → 指纹变 → 新会话入口重建 → 再答，更新及时且可检测 | |
| 反对（≥2） | ① 宿主第一次加载 SKILL.md 的耗时本包消不掉。② 把查询答案缓进 brain 会过期，比没记忆更危险。③ 05 §1b 查询遇到 inbox 非空还 AUTO C'，可能把只读问句拖进写入/结转 | |

**(2) 必要性**：**必须加（硬化 3.21 快路径 + 补 SRC 别名）**。不新建「记忆层」。

**(3) 扩展风险**

| 风险维度 | 说明 | 严重程度 | 缓解 |
|---|---|---|---|
| 记忆过期 | 手写定位、会话缓存、答案缓存都会过期 | 高 | 只派生；禁止手改 brain/json/index；CQ-5 仍要求实读命中的 1～3 个事实文件 |
| 膨胀 | 新规则文件 / 新记忆目录 | 中 | 扩展 05/view-spec/refresh_views；不新建 NN |
| 破坏 CQ-5 | 被理解成可以凭 brain 直接答、不再读事实 | 高 | brain/alias 只指路；结论必须来自实读事实文件 |
| SRC 别名过大 | 把 atoms 全文灌进 alias | 中 | 只收 `sources/_index` 与各 `meta.md` 标题/编号，不收 atoms |
| 宿主冷启动 | 新对话加载技能正文 | 低（不可消） | 对外声明：本包只约束项目内读文件数 |

**(4) A 建议（已按用户「加到方案里」纳入基线）**：继续实施 R3。名称必须叫 **派生定位**，禁止叫记忆/缓存/会话存档。

用户说「把定位关系写进索引」时的正确落点：**词库 alias（待确认）**，确认后 P-VIEWS 重建 alias_index；禁止改 `wps/_index` 当地图。

### 0.4.1 过期 / 更新 / 及时 / 有效（R3 时效模型）

本包 **不保存「记忆」**。保存的是三样不同寿命的东西，禁止混用：

| 东西 | 是什么 | 寿命 | 过期判定 | 更新动作 |
|---|---|---|---|---|
| 事实源 | todos / WP / SRC / 风险等 | 以文件为准，无时钟 TTL | 被写入即变 | 人确认后的写入；查询只读 |
| 派生定位（alias_index / brain 指路段） | 从事实源算出来的「词→文件」地图 | 与 `facts_fingerprint` 同寿 | 磁盘事实哈希 ≠ `.state.json` 里记下的哈希 | **每一次查询**先 `refresh_views`：未变 0 写盘，变了整表重建 |
| 对话正文 / 模型上下文 | 上一句答过什么 | 本会话内有效，跨会话作废 | **永远不能当证据** | 不更新、不落盘。CQ-5：本轮未打开的文件不得引用 |

**过期**：不是「放久了」，是「地图和事实对不上」。项目事实不按日历过期，按文件是否被改过期。因此不设 5 分钟缓存、不设会话记忆文件。

**更新**：只有两条合法更新链。

1. 事实变了 → 指纹变 → 下次（或当次）查询重建地图。  
2. 用户要补别名（「住所核验就是 SRC-055」）→ 写词库待确认 → 确认后重建地图。禁止第三条链：把查询结论或手写路径表写进 `_index`/brain。

**及时性**（窗口要短到「下一次开口之前」）：

| 场景 | 窗口 | 规则 |
|---|---|---|
| 本会话刚写完事实再问 | 写成功后 P-VIEWS，下一句查询已是新指纹 | 3.21 已有；保持 |
| **每一次查询**（含同一会话第 2、3 问） | 开口先比指纹，不是只在新会话开头比一次 | **R3 硬化**：05 文首每问必跑脚本（未变则秒级返回） |
| 另一个对话刚改了文件，本对话还开着 | 本对话下一问跑脚本即发现指纹变，重建后再答 | 不靠「记得关窗口」 |
| 无 Python | 不用过期 brain 当真理；定向读事实并声明 as-of | BRN-004 |
| 脚本失败 | 同无 Python，不拿旧 brain 硬答 | 查询失败降级，不是用记忆顶上 |

同一会话里模型已经「记住」刚才的结论：仍须实读命中文件。刚才的结论只是话，不是事实。这是 CQ-5 的本意，R3 写明：**禁的是把对话当证据，不是禁止用指纹地图找路。**

**有效性**（什么可以写进对外结论）：

| 来源 | 有效？ | 条件 |
|---|---|---|
| 本轮打开的事实文件 | 是 | 路径可指回 |
| 指纹一致的 alias 指出的 path，且本轮已打开 | 是 | 地图只指路，打开后才算数 |
| `pm-decisions.md` 开放行 | 横幅有效 | **实时读**，禁止从 brain 抄待拍板 |
| 词库 `confirmed` 别名 | 仅用于找路 | 不把释义当进度 |
| 词库 `pending` | 否（静默路由） | 可提示「按候选理解」 |
| 上一对话 / 本会话更早一句未再实读 | **否** | 过期记忆 |
| 过期 brain（指纹不一致） | **否** | 先重建或 as-of 降级 |
| 手写进 `_index` 的主题清单 | **否** | 当不存在 |

双保险：地图过期 → 重建；即使地图偶发漏指，结论仍来自本轮实读的 ≤3 个文件，不会把旧摘要当答案缓存。

换对话慢的合法剩余：宿主加载 SKILL 正文。项目侧目标：指纹未变时脚本秒级 + json/brain + 1～3 个文件。

---

## 0.5 R4 需求辩论（随便说 vs 记太多 vs 下次没上下文）

现场（`2026-08-31_135523.png`）：问 `/epoint-gateway/zwww/sds` 干不干。模型把「江苏一体化对外网关」说成结论；用户追问怎么知道。模型承认：**本地没有这条完整 URL，上轮是根据投标书 02 里 zwww=政务外网等线索推断的，不是检索命中。** 用户随后提出取舍：80% 靠聊天上下文，不落盘则下次偏；落盘太多链路变长变慢；过结构则 PM 不能随口记。

对家模型建议：事实/过程/知识分层；zwww 等进词库；把用户说「80% 成立」升为「用户已确认」。后两句里 **升格那句不成立**（见下）。

**(1) 合理性**

| 论证项 | 结论 | 论据 |
|---|---|---|
| 是否符合定位 | 符合 | 词库 17 已是「辅助理解不是事实源」+ pending→confirmed；journal 只追加原文；project-notes 随笔要问；05 §6.3a 最小读取不得用来写入 |
| 是否有真实场景 | 有 | 截图；用户本轮原话即取舍 |
| 是否重复 | 机制在、闸反了 | 17 §6.1 查询也会「自动推断高 → 写入 pending」，查询轮每遇生词就写盘，正是「记越多越慢」。00 备忘要 ASK。缺的是：**查询默认不写；升格认命题不认推导质量** |
| 支持（≥2） | ① 下次要准，只需可复用的 **词→一句释义**，不需要整段推导。② PM 随口「记一下 / X 就是 Y」已有 T1 和 10 号，不必新表。③ 把 80% 评价当成确认，会把推测写进 confirmed，下次当静默真理，比没记忆更危险 | |
| 反对（≥2） | ① 再做一套「知识库/记忆层」必膨胀。② journal 每轮推断都追加 = 查询链更长。③ 完全不记生词，下次仍要靠聊天 | |

**(2) 必要性**：**必须加（闸，不是新库）**。不新建记忆文件。

**(3) 取舍（口低闸 / 证高闸 / 过程不落盘 / 图派生）**

| 谁在说 | 记什么 | 记到哪 | 何时 | 下次查询怎么用 |
|---|---|---|---|---|
| PM 随口「记一下」「X 就是 Y」 | 他认的那句 | T1→词库 confirmed；否则 pending 或 10 号待确认事实 | 当场 | alias 一跳 |
| PM 随口进度/待办 | 事项 | 原 10/WF-8，待确认 | 当场 | 事实源 |
| AI 自己从网页/上下文推出的 80% | **默认不记** | 本轮标注「推测」 | 不写盘 | 无。丢了就对了 |
| 用户点名「这几个进词库」 | 词 + 一句候选释义 | 词库 **pending** | 攒成一批，一轮一次 | 找路时标「待确认」，不静默当事实 |
| 推导过程、旁证链接、怎么想到的 | **永不记进事实/词库** | 不要 journal 灌推断 | — | — |

**什么值得升 confirmed（截图第三问）**

同时满足才升：

1. **可复用**：下轮还可能用这个词找路（平台名、路径段、模块名），不是一次性「这接口干不干」的猜测。  
2. **认的是命题**：用户说「zwww 就是政务外网」「对，就是这个」。  
3. **不是认推导质量**：「你推得 80% 对」「有道理」**不等于**确认「sds 属于江苏一体化网关」。

**截图三条词的落点**

- `zwww` / `epoint-gateway` / `sds`：适合当 **术语**（接口路径段），不是需求、不是 WP、不是「已干废」。  
- 投标书 02 已写 zwww=政务外网 → 有源，可 pending，用户 T1 后 confirmed。  
- 「属于江苏省一体化…对外网关」：本地未命中完整 URL → **保持推测**，禁止因「80%」升 confirmed。  
- 「接口干不干」：查对接文档/待办；查不到就说查不到，不把推断写成废接口事实。

查询轮（05）：**禁止** 17 §6.1 自动写 pending。只允许输出一批 SUGGEST（≤7 个词，一轮一次）。用户说「写这几个」才写 pending。日报/会议/拆解仍可按 17 攒批自动 pending（已有节流）。

**(4) A 建议**：纳入本 AP 为 CR-004，扩展 17+05，不新建文件。禁止把截图对家方案里「80%→用户已确认」写进规则。本轮 **不写市监词库**。

---

## AP-1. 变更概述

3.22.0 修三类现场失败，都不升 schema、不新建 `references/NN-*.md`、不抽独立 Skill、不引入会话记忆。

**R1（残差）**：在既有 `reply-norm-skill` 上补「提问必须带对象」和「宿主弹出假执行门时拆穿」；3.18.0 的语种 / 禁 CoT / 禁假执行门保持不动。

**R2（会议链）**：会议转写/纪要/例会导出默认走 WF-3，禁止因「整理/拆解」误入 `P-SPLIT`。先归档纪要（不碰 todos、不触发 Step 0），有正式行动项再跑技能包内 `carryover_step0.py`。脚本在业务 cwd 找不到时不得手搓全员；`_index` §1 有标题无表时回退上一合法日花名册。存量 `sources/` 里像会议的 SRC 由 migrate 默认 dry-run 列清单，不自动搬。开发仓与执行过程不写市监业务库。

**R3（查询定位闸）**：换对话慢按「3.21 快路径未执行 + SRC 未进 alias + 只读查询被拖成写入」修，不按「加记忆」修。05 文首写死：先跑包内 `refresh_views.py` 比指纹 → 读 `alias_index`/`brain` → 最多 1～3 个事实文件。全库扫、扫 backup、为求稳再对一遍 = 本轮查询失败。`refresh_views` 把 SRC 标题/编号纳入 alias（不收 atoms）。只读查询禁止 AUTO C'、禁止因此 Step 0。brain/json 禁止手改；过期只通过指纹重建。

**R4（口低证高）**：PM 随口能记，记的是薄入口（词 pending / 待确认事项），不是把 AI 推导链存下来。查询轮默认不写词库；升 confirmed 只认命题（T1/T2/点名），不认「推得 80%」。推导过程不落盘。下次靠 alias 找词，不靠重放聊天。

---

## AP-2. 影响点详细分析

| 影响项 | 当前状态 | 变更后状态 | 影响描述 | 影响程度 | 是否可逆 |
|---|---|---|---|---|---|
| `SKILL.md` §6 会议行 | 「整理/拆文件」可改走源文档拆解 | 会议转写/纪要/例会导出禁止改走拆解 | 契约路由；合同「拆文件」不变 | 中 | 是 |
| `SKILL.md` §5 / 22 脚本示例 | `python scripts/carryover_step0.py --root <项目根>`，易在业务 cwd 找 | 明确脚本=本 Skill 包 `scripts/carryover_step0.py`，`--root` 才是项目根 | 避免「脚本不存在」后手搓 36 人 | 高 | 是 |
| `00` §2.7 | 「源文档拆解入库」行触发词含拆文件/拆文档，无会议排除 | 该行追加排除句：`会议转写/纪要/例会导出除外（走 WF-3）`；明示「拆进 sources」仍走 P-SPLIT | 意图分发阶段就切开，避免只改 10/split-rules 仍误路由 | 中 | 是 |
| `00` WF-3 行动项列 | 写成 SUGGEST | 与 02 对齐：T-A4 MANDATORY；**顺序**先归档纪要，再 P-CARRY，再 inbox | 修三套口径冲突 | 中 | 是 |
| `00` §5.0 | 真确认形状已在；假执行门指针到 reply-norm | 不改形状；R1 细则仍只在 reply-rules | 避免再复制底线 | 低 | 是 |
| `02-meeting-rules.md` | T-A4 强制落待办，无「不碰 todos 则不结转」 | 增加快路径：写 `meetings/` 不触发 22；ASR 不作源文档；禁止为「可能有倒排」加载 WF-7 | 会议投喂变快 | 高 | 是 |
| `10-update-trigger-rules.md` | L1「整理记录」=投喂入库；「拆解这份」=源文档；「整理成会议纪要」=会议；重叠 | 宾语/文件类型是会议时改 WF-3；源文档「不是本信号」加会议转写/纪要/腾讯会议导出 | 信号过宽会伤合同拆解 | 高 | 是 |
| `23-procedure-index.md` | 会议无独立支；P-DOC-INGEST 必须 CALL P-SPLIT；P-WF8 Pre=P-CARRY | 会议支：P-ROUTE→WF-3；会议禁止 CALL P-SPLIT。P-CARRY 脚本定位=包内路径 | 过程树与现场一致 | 中 | 是 |
| `source-split-skill/references/split-rules.md` | 无会议排除 | 首段排除会议转写/纪要/例会导出，除非用户明示拆进 sources | 防误拆 | 中 | 是 |
| `reply-norm-skill/references/reply-rules.md` | 硬规则 3–5 已禁假执行门；正反例第一行即截图 1 | 补：提问必须带已做/对象/后果；宿主误弹须拆穿 | 残差，不重写 3–5 | 低 | 是 |
| `reply-norm-skill/references/capability-boundary.md` | 回归仍写 RN-001～004 | 改为 RN-001～009，并加 RN-010/011 | 陈旧索引 | 低 | 是 |
| `22-carried-over-rules.md` | HARD BLOCK 仍正确；脚本路径含糊；无空表回退 | 不放松 HARD BLOCK；写明包内路径；空花名册回退规则 | 行为修正 | 中 | 是 |
| `scripts/carryover_step0.py` | `parse_index` 只吃单个 index；`main` 只取 `dates[-1]`；表空仍 exit 0 | `main` 对合法日倒序找第一个 `names>0`；stdout `ROSTER_FALLBACK`；两日都空 `FAIL:ROSTER_EMPTY` 且 exit 2 | 修 0 人后手搓；实现落在 main 倒序而非只改 parse_index | 高 | 是 |
| `scripts/migrate_workspace.py` | 3.21.1 条无会议误拆检测 | 增 3.22.0 能力条 `meeting_ingest_guard`；dry-run 列疑似会议 SRC | 老数据；默认不写盘 | 中 | 是 |
| `examples/08-记会议纪要.md` | 第 1 轮把 T-A4 做成 A 落待办 / B 只写纪要 / C 先放着（可选化，违反 02 §2.2 MANDATORY） | 正式行动项改为「我记下了，请你认不认」；删除 A/B/C 可选化；缺负责人仍问 | 示例与规则对齐 | 中 | 是 |
| `tests/regression-suite.md` | 807 例；无会议≠拆解、无脚本包内路径、无查询定位闸 | Module 76+77；合计约 826 | 验收 | 低 | 是 |
| 模板 / 目录结构 | 39 模板；schema 0.16.0 | 不改模板、不新建目录 | 无结构迁移义务 | 无 | — |
| 核心契约 | SKILL.md + 00 将改路由与 WF-3 表 | 标记 `contract_change`，全量回归 | 发布门槛 | 中 | 是 |
| 已有工作区兼容 | schema 0.16.0 | 仍 0.16.0；结转解析更稳；不改历史文件除非 `--migrate-business` | 可跳版本升 Skill | 低 | 是 |
| 合同拆文件 P-SPLIT | 「拆文件」+ 规格 → 六件套 | **保持**（SF-001 阻断回归） | 不得误伤 | 高（若排除过宽） | 是 |
| 查询假执行门 | RN-003 已存在 | 保持失败即失败；另加 RN-010/011 | 不回退 3.18 | 低 | 是 |
| T-A4 / 全员结转 | 正式行动项强制落待办 → 周一 36 人 Step 0 | 仍强制，但**先有纪要**；脚本秒级；禁止手搓 | 有行动项时仍会结转 | 中 | 是 |
| Portfolio | 3.21.1 只读 | 仅版本锁步到 3.22.0，无行为 | 双包同号 | 低 | 是 |
| 市监业务库 | 3.21 已禁写 | 本轮继续禁读禁写、不跑 migrate | 用户硬约束 | — | — |
| 宿主「是否执行此方案」按钮 | 产品层弹出，Skill 拆不掉 | 对话拆穿；不补假方案迎合按钮 | 体验部分改善 | 低 | 是 |
| `05-query-rules.md` §1 | 流程无每问比指纹；无 Python 降级不在文首 | 文首 if-else：有 Python 跑包内 refresh_views；无 Python/失败 → 四加速器+as-of（BRN-004），不报错 | 每问必比，无 Python 不卡死 | 高 | 是 |
| `05-query-rules.md` §1b | inbox 非空 AUTO C' | 只读查询 → HINT 一行，禁止 C' | 查询不变写入 | 高 | 是 |
| `05-query-rules.md` §2.5a / §6.3 | 待办文件不存在 → 触发 Step 0 | 只读查询不 Step 0、不建今天 todos；HINT「今日待办未结转」 | 与 §1b 同时收口，避免只改一处 | 高 | 是 |
| `05-query-rules.md` §1.5 | 查询术语归一化会走到 17 自动 pending | 查询轮只允许 SUGGEST ≤7，禁止触发 17 §8.1 自动写盘 | 与 R4 对齐 | 中 | 是 |
| `SKILL.md` §5.3 | 「有 brain 且指纹一致先读 brain」 | 补：简单查询也先 P-VIEWS（命令在 05，不加载 00） | 与 5.1b 对齐 | 中 | 是 |
| `00` P-RESOLVE / CQ-5 | alias_index 已有；CQ-5 禁对话缓存，易被理解成必须全库实扫 | CQ-5 澄清：禁的是对话记忆当证据；指纹一致的 alias 必须用来找路，然后实读命中文件 | 防两种相反误读 | 中 | 是 |
| `scripts/view-spec.json` `brain_fact_globs` | 无 `requirements/sources/` | 增加 `requirements/sources/_index.md` 与各 `meta.md`（标题/编号） | SRC-055 类主题能一跳命中 | 中 | 是 |
| `scripts/refresh_views.py` | 不解析 sources；brain 别名节只指针 json | 解析 SRC meta 进 alias_index 与 entities；brain「别名跳转」改为短表（WP 名+词库 confirmed+SRC 标题，上限，详见 §9.6） | 现场「住所核验」可定位 | 高 | 是 |
| `17-domain-glossary-rules.md` | 词库是 alias 家 | 用户说「把定位写进索引」→ 写词库 alias 待确认，再 P-VIEWS；禁止手改 `_index`/brain/json | 防过期手账 | 中 | 是 |
| `23` P-RESOLVE | 写入查重用 | 查询同样必须走 alias；05 短条复述（简单查询不载 23） | 过程树一致 | 低 | 是 |
| 会话记忆 / 答案缓存 | 无（换对话丢失） | **保持无**。不建 chat-memory 文件 | 避免过期记忆 | — | — |

**能力行为变化（摘要）**

- 会议整理：从「可能同时拆解 + 全员结转 + 倒排」变为「纪要优先，必要时再结转」。
- 源文档拆解：仅当用户明示把会议当需求源，或文件本就是合同/招标/立项/规格。
- 对外提问：查询/只读后不准空壳执行门；真确认仍只走 00 §5.0。
- 结转：有 Python 必须跑包内脚本；空花名册不再解析成 0 人后手搓全员。
- 查询：换对话不靠聊天记忆；靠指纹派生的 alias 找路，再实读 1～3 个文件。手写主题地图和答案缓存都不做。

**回归可能受影响**：RN-001～009（应仍过）、BS-022（顺序改为纪要之后，结果仍落待办）、CO-S10（仍禁止手搓）、SF-001～004、CO-S01～19、SC-002。须把 `examples/08` 从「先问再建」改掉，否则与 BS-022 继续对打。

---

## AP-3. 变更策略与设计思路

### 3.1 为什么选这个方案

现场有三张截图、一份会议 docx、一条已完成 CR。R1 的主体已经在 3.18.0 用假 skill 收过，再做一遍是复杂度空涨。R2 是 3.12 强制拆文件、3.18 结转脚本、3.20 无感知入库叠出来的串台。R3 是 3.21 百科快路径没被走、SRC 不进 alias、CQ-5 被读成全库扫，再叠加「手写定位进 index」这种会过期的假记忆。全部扩展现有文件，符合 16 号「现有能力扩展优先」。

### 3.2 设计思路

不新增一级能力名。在 `P-ROUTE` 增加会议快路径；WF-3 写成可执行的阶段序；P-CARRY 的脚本定位从「相对 scripts/」改为「与 SKILL.md 同级的包内 scripts/」。`reply-norm` 只加残差句，底线 14–16 三处同文不动。migrate 只检测、默认不搬，避免把真源文档当会议清掉。

修好后的会议链：

```
上传腾讯会议 docx / 「整理纪要」 / 「拆解这份会议记录」
  → P-ROUTE：会议转写或纪要 → 只加载 00+02+06+17（写入时 +23）
  → 禁止加载 split-rules
  → 优先用文档后部已有纪要/行动项；ASR 只核对，不 ATOM
  → 写 meetings/YYYY/MM/… 草稿 + index    ← 不碰 todos，不 Step 0
  → 对外：纪要结论 + 行动项（白话）
  → 无 T-A4：结束（风险/决策 SUGGEST，不加载倒排）
  → 有 T-A4：P-CARRY（包内脚本）→ inbox→C' 只写点名的人
  → P-REPLY：00 §5.0「我记下了这些」；宿主假执行门则拆穿
```

R3 新会话只读查询：

```
问进度 / 某主题现在怎样 / 国庆上线哪些地市
  → 只载 05
  → python "<Skill包根>/scripts/refresh_views.py" --project-root "<项目根>" --all
  → 用提问词查 alias_index（编号 / WP名 / 词库 / SRC 标题）一跳
  → 命中：打开 path，最多再补 2 个事实文件后作答
  → 未命中：只读 wps/_index、sources/_index、todos/{最新合法日}/_index、risk-register；仍无则说缺什么
  → 禁止 glob ai/、禁止 backup/、禁止第 4 个事实文件、禁止上轮对话当证据
  → inbox 非空只 HINT，不 C'、不 Step 0
```

### 3.3 关键决策点

| 决策 | 选择 | 理由 |
|---|---|---|
| R1 范围 | 残差，不重做 3.18 | 截图 1 = RN-003 反例；用户已确认 |
| T-A4 | 仍强制，放在纪要之后 | 用户确认 Q2；不丢行动项；改示例 |
| 22 HARD BLOCK | 不跳过 | 用户确认 Q3；丢未办结比慢更糟 |
| 排除词 | 绑会议类型/文件名/宾语，不绑光秃「拆解」 | 合同「拆文件」必须仍进 sources |
| schema | 不升 | 无新必填目录/字段 |
| 误拆 SRC | dry-run 清单 | 用户确认 Q5 |
| 市监 | 不读不写、不 migrate | 用户硬约束 |
| R3 记忆 | 不用会话记忆、不缓存答案、不手写主题地图 | 过期可检测的只有指纹派生 |
| R3 只读查询 | 禁止因 inbox 非空 AUTO C' | 查询不得变成结转/写入 |
| CR 拆分 | 三 CR：001 问答残差；002 会议链+结转脚本+migrate；003 查询派生定位 | 16 号单一目标；同 AP |

### 3.4 与现有规则的交互

| 模块 | 交互 |
|---|---|
| 00 §2.7 / §4c / §5.0 / WF-3 / WF-8 | 意图分发、结转闸、确认形状、会议顺序、T-A4→WF-8 |
| 02 | 快路径正文；T-A4 口径唯一家 |
| 10 | 信号表排除；「整理记录」遇会议不当工时投喂 |
| 22 | 时机 0 不变（读或写今天 todos 才全员）；脚本路径与空表回退 |
| 23 | 调用树会议支；P-SPLIT Forbidden 加会议；P-CARRY 包内路径 |
| split-rules | 首段排除；引擎与六件套不改 |
| reply-rules | 提问对象化；确认形状仍只认 00 §5.0 |
| 05 / SKILL 底线 14–16 | **不改同文**（R1 不重写假执行门） |
| 07 | 需求拆解仍不落待办；与会议快路径无关 |
| migrate / carryover 脚本 | 老数据检测 + 运行时回退 |
| 16 / 契约 | SKILL+00 为 contract_change；全量回归 |

### 3.5 被否决的替代方案

| 方案 | 否决原因 |
|---|---|
| A. 重写拆解引擎 / 把会议登记为 source_type | 过重；会议不是需求源文档；与 R2 诊断相反 |
| B. 无 Python 或脚本找不到就跳过 Step 0 | 丢未办结；违反 22 HARD BLOCK；用户否决（Q3） |
| C. 把 R1 再做成独立模块或重写底线 14–16 | 与 3.18.0 / RN-003 重复；用户否决（Q1） |
| D. 改 T-A4 为先问「要不要建待办」 | 违反 P-WF8 / BS-022；用户否决（Q2） |
| E. migrate 自动把会议 SRC 搬进 meetings/ | 可能误伤真源文档；用户否决（Q5） |
| F. 新建 `24-meeting-ingest-rules.md` | 违反扩展优先与「禁止新建 NN」禁区 |
| G. 会话记忆 / 把查询答案写入 brain | 必过期；违反「brain 禁止待拍板」与 CQ-5 |
| H. 按截图建议把「住所核验→文件清单」手写进 `wps/_index` | 索引不是地图；事实一变即撒谎；违反底线 17 |

---

## AP-4. 修改范围清单

修改类型：`new_file` / `edit_section` / `edit_full` / `delete` / `rename`。行数为实施时预估，以最小补丁为准。

| 文件 | 修改类型 | 修改内容摘要 | 新增/修改行数（估） | 是否核心契约 |
|---|---|---|---|---|
| `governance-shared/planning/upgrade-plan-v3.22.0.md` | new_file | 本 AP | — | 否（设计草稿，发布后删） |
| `ChronoPM-Project/SKILL.md` | edit_section | §6 会议行排除拆解；§5 脚本包内路径；版本 3.22.0 | 15–30 | **是** |
| `ChronoPM-Project/references/00-pm-main-rules.md` | edit_section | §2.7「源文档拆解入库」行加排除句「会议转写/纪要/例会导出除外（走 WF-3）」；WF-3 顺序与 T-A4；CQ-5 澄清 | 50–90 | **是** |
| `ChronoPM-Project/references/02-meeting-rules.md` | edit_section | 快路径：不碰 todos 不结转；ASR 非源文档；禁预加载倒排 | 40–70 | 否 |
| `ChronoPM-Project/references/10-update-trigger-rules.md` | edit_section | L1 整理/拆解遇会议改 WF-3；源文档「不是本信号」 | 20–40 | 否 |
| `ChronoPM-Project/references/23-procedure-index.md` | edit_section | 会议支；P-SPLIT Forbidden；P-CARRY 包内路径 | 15–30 | 否 |
| `ChronoPM-Project/source-split-skill/references/split-rules.md` | edit_section | 首段会议排除 | 8–15 | 否 |
| `ChronoPM-Project/source-split-skill/references/capability-boundary.md` | edit_section | 触点 + 回归 ID | 5–10 | 否 |
| `ChronoPM-Project/reply-norm-skill/references/reply-rules.md` | edit_section | 提问对象化 + 宿主误弹；正反例各 1 行 | 15–25 | 否 |
| `ChronoPM-Project/reply-norm-skill/references/capability-boundary.md` | edit_section | RN-001～009 + 010/011 | 4–8 | 否 |
| `ChronoPM-Project/references/22-carried-over-rules.md` | edit_section | 包内脚本路径；空花名册回退；不改 HARD BLOCK | 20–40 | 否 |
| `ChronoPM-Project/scripts/carryover_step0.py` | edit_section | `main` 对合法日倒序找 `names>0`；stdout `ROSTER_FALLBACK`；都空则 `FAIL:ROSTER_EMPTY` + exit 2 | 40–80 | 否 |
| `ChronoPM-Project/scripts/migrate_workspace.py` | edit_section | VERSION_CAPABILITIES 3.22.0；误拆检测 dry-run | 40–80 | 否 |
| `ChronoPM-Project/scripts/_version.py` | edit_section | `SKILL_VERSION = "3.22.0"` | 1 | 否（版本源） |
| `ChronoPM-Project/skill.json` `VERSION` `CHANGELOG.md` | edit_section | 3.22.0 触点（准许执行后） | 版本同步 | **skill.json 是** |
| `ChronoPM-Project/SKILL_BLUEPRINT.md` | edit_section | 能力/版本行（Minor 必更） | 元数据+会议快路径+查询派生定位 | 否 |
| `ChronoPM-Project/examples/08-记会议纪要.md` | edit_section | 删除 T-A4 的 A/B/C 可选化；改为「已记下请认」；缺负责人仍问 | 20–40 | 否 |
| `ChronoPM-Project/references/05-query-rules.md` §1 | edit_section | 文首 if-else：有 Python 跑包内 refresh_views；无 Python/失败 → BRN-004 四加速器+as-of | 15–25 | 否 |
| `ChronoPM-Project/references/05-query-rules.md` §1b | edit_section | 只读查询 inbox 非空 → HINT，禁止 AUTO C' | 8–15 | 否 |
| `ChronoPM-Project/references/05-query-rules.md` §2.5a 与 §6.3 | edit_section | 只读查询待办文件不存在 → 不 Step 0、不建档；HINT | 10–20 | 否 |
| `ChronoPM-Project/references/05-query-rules.md` §1.5 | edit_section | 查询术语归一化禁止触发 17 §8.1 自动 pending；仅 SUGGEST ≤7 | 8–15 | 否 |
| `ChronoPM-Project/references/17-domain-glossary-rules.md` | edit_section | 查询轮禁止自动 pending；升格认命题；SUGGEST 一批 ≤7；「写进索引」→ 词库 | 25–50 | 否 |
| `ChronoPM-Project/scripts/view-spec.json` | edit_section | brain_fact_globs 增 sources/_index 与 meta.md | 5–10 | 否 |
| `ChronoPM-Project/scripts/refresh_views.py` | edit_section | parse SRC meta；alias_index；brain 短定位表 | 80–140 | 否 |
| `ChronoPM-Project/tests/regression-suite.md` | edit_section | Module 76（会议）+ Module 77（查询定位） | 60–100 | 否 |
| `ChronoPM-Portfolio/VERSION` `skill.json` `SKILL.md` `CHANGELOG.md` | edit_section | 仅锁步 3.22.0 | 版本 | 否（无行为） |
| `ChronoPM-Project/governance/migrations/upgrade-to-3.22.0.md` | new_file | 施工清单（准许执行后） | — | 否 |
| `ChronoPM-Project/SKILL.md` §5.3 | edit_section | 简单查询也先跑包内 refresh_views（不加载 00）；无 Python 不阻断 | 8–15 | **是** |
| `governance-shared/change-requests/CR-20260831-001.md`～`004.md` | new_file | **准许执行后才建** | — | 否 |
| `governance-shared/impact-analysis/IA-20260831-001.md`～`004.md` | new_file | **准许执行后才建** | — | 否 |

**不改**：`skill-contract.md` 正文、pm-decisions 八块、WP/计划模板列、`wps/_index` 列数、拆解六件套字段、`reply-norm-skill` 不得出现 `SKILL.md`。

**施工禁区（写入 upgrade-to 时原样保留）**

- 禁止读写 `C:\Users\qiusuo\Downloads\市监重构项目管理`
- 禁止升 workspace schema
- 禁止新建 `references/NN-*.md`
- 禁止 `reply-norm-skill/SKILL.md`
- 禁止把会议登记为源文档类型；禁止重写 P-SPLIT 引擎
- 禁止把 22 HARD BLOCK 改成「无 Python 可跳过结转」
- 禁止新建会话记忆 / 答案缓存 / 手写「主题→文件」进 `_index` 或 brain
- 正式文档不得引用本 upgrade-plan 路径（发布后删 AP）

---

## AP-5. 回归测试计划

施工只认发布时 `regression-suite.md` 合计行。基线 **807**；本版新增 Module 76（会议）+ Module 77（查询定位），预估合计 **826**（实施时以套件为准）。

### 5.1 新增用例

| Case ID | 模块 | 输入 | 预期结果 | 类型 | 说明 |
|---|---|---|---|---|---|
| MTG-001 | 会议路由 | 腾讯会议 docx +「整理/拆解记录」 | 走 WF-3；不加载 split-rules；不写 `sources/` | positive | 阻断 |
| MTG-002 | 会议路由 | 合同/需求规格 +「拆文件」 | 仍 P-SPLIT 六件套 | regression | 阻断 |
| MTG-003 | 顺序 | 会议含 T-A4，今天未结转 | 先有 `meetings/` 文件，再跑**包内**脚本，再 inbox | positive | 阻断 |
| MTG-004 | 顺序 | 会议无正式行动项 | 不 Step 0、不建今天 todos | negative | 阻断 |
| MTG-005 | ASR | 2 万字转写 + 文末结构化纪要 | 用文末结构；不建 atoms 六件套 | positive | |
| CO-S20 | 脚本路径 | cwd=项目根，技能包在别处 | 调用包内 `carryover_step0.py`；不手搓 | positive | 阻断 |
| CO-S21 | 花名册 | §1 标题在、表空，上一日有表 | 回退上一日；人数>0；stdout 有 `ROSTER_FALLBACK` | positive | 阻断 |
| CO-S22 | 花名册 | 两日都无表 | `FAIL:ROSTER_EMPTY`；不造全员空文件 | negative | 阻断 |
| RN-010 | 问答残差 | 查询后宿主弹「执行此方案」 | 正文拆穿误弹 + 已有中文结论 | positive | |
| RN-011 | 问答残差 | 中途确认 | 必须带已做/对象/后果；禁止空洞「是否执行」 | positive | |
| MIG-001 | 老数据 | dry-run 遇到会议类 SRC | 只打印清单，不搬不删 | positive | 阻断 |
| MIG-002 | 老数据 | 无 `--migrate-business` | 零写盘 | regression | 阻断 |
| QLOC-001 | 查询定位 | 新会话问「住所核验国庆上线哪些地市」类主题（fixture 有 SRC meta 标题+对应 WP） | 先 refresh_views；alias 命中；打开事实文件 ≤3；不 glob 100+；不读 backup/ | positive | 阻断 |
| QLOC-002 | 指纹 | 事实已变、brain 仍旧 | 必须先重建再答；禁止用旧 brain 结论 | negative | 阻断 |
| QLOC-003 | 禁手账 | 用户说「把定位关系写进 wps/_index」 | 写词库 alias 待确认或拒绝手改 index；随后 P-VIEWS | negative | 阻断 |
| QLOC-004 | CQ-5 | 上一对话已答过同一句，本轮未实读 | 不得用上轮正文当证据；须走 alias+实读 | negative | 阻断 |
| QLOC-005 | 只读 | 查询日 inbox 非空 | 不 C'、不 Step 0；可 HINT 一行 | negative | 阻断 |
| QLOC-007 | 及时性 | 同一会话已答过；磁盘事实已改（指纹变） | 第二问必须发现 stale、重建后再答，不得复述第一问结论 | negative | 阻断 |
| TERM-001 | 口低证高 | 只读问「sds 干不干」，模型自推网关 | 本轮标推测；**不写**词库/journal；可 SUGGEST 一批 | negative | 阻断 |
| TERM-002 | 口低证高 | 用户说「80% 有道理」 | 不升 confirmed | negative | 阻断 |
| TERM-003 | 口低证高 | 「zwww 就是政务外网，写进词库」 | T1 → confirmed 或先 pending 再确认；有 Source | positive | 阻断 |
| TERM-004 | 口低证高 | 查询轮一次冒出 10 个缩写 | 只一张 SUGGEST ≤7，不自动 pending 10 条 | negative | |
| QLOC-006 | SRC | 仅 sources/meta 有标题「住所核验」，WP 名不同 | alias 仍能指到 SRC + 关联 WP（若登记册/WP 有编号） | positive | |
| BRN-003 | 回归 | 「注销国庆包现在怎样」 | 仍先 brain；不载 00 | regression | 阻断 |
| ALI-001 | 回归 | 农专注销 term 两跳 | 仍命中正确 WP | regression | 阻断 |

### 5.2 必须仍通过的旧用例（阻断）

| Case ID | 说明 |
|---|---|
| RN-003 | 「电子签名和实名进度」仍不准问是否执行方案 |
| CO-S10 | 有 Python 仍手搓全员 = 级联失败 |
| CO-S19 | 脚本部分失败只 E5 失败人 |
| SF-001 | 「拆文件」+ 需求规格 → sources 六件套 |
| BS-022 | T-A4 有负责人仍落待办（在纪要之后） |
| SC-002 | 处理会议纪要后仍有自查清单 |

### 5.3 影响的已有用例

- `examples/08` 与 BS-022 / P-WF8 对打 → **改示例**，不改 BS-022 预期。
- CO-S01～19 预期不变；CO-S21/22 是空花名册新分支。
- RN-001～009 不改预期；RN-010/011 只加残差。

### 5.4 阻断项汇总

**阻断（任一失败不得发布）**：MTG-001、MTG-002、MTG-003、MTG-004、CO-S20、CO-S21、CO-S22、CO-S10、RN-003、SF-001、MIG-001、MIG-002、BS-022、QLOC-001、QLOC-002、QLOC-003、QLOC-004、QLOC-005、QLOC-007、BRN-003、ALI-001、TERM-001、TERM-002、TERM-003。

**非阻断（须实现、失败不挡发布）**：QLOC-006（SRC 标题定位）、TERM-004（SUGGEST ≤7）、RN-010/011、MTG-005。

---

## AP-6. 风险评估与回滚方案

| 风险项 | 发生概率 | 影响程度 | 预防措施 | 回滚方案 |
|---|---|---|---|---|
| 会议排除词过宽，合同拆文件走偏 | 中 | 高 | 排除条件绑会议类型/文件名/宾语；MTG-002 / SF-001 阻断 | 回滚 10/00/23/split-rules 排除段 |
| 周一有 T-A4 仍全员结转，用户觉得还是慢 | 高（有行动项时必然） | 中 | 先落纪要让用户看见结果；脚本秒级；禁止手搓 | 不回滚强制 T-A4（基线） |
| 空花名册回退读错日/错人 | 低 | 高 | 只回退 `date≤今天` 的上一合法日 §1；仍 0 人则 FAIL 不写 | 回滚 `parse_index` |
| 把真源文档标成会议误拆 | 低 | 中 | 检测用文件名/标题关键词；只清单；搬迁要 `--migrate-business` | dry-run 无写盘可回 |
| 宿主按钮仍弹出 | 高 | 低 | RN-010 拆穿；不承诺拆 UI | 无需回滚 Skill |
| 改 00/SKILL 引入契约回归 | 中 | 高 | 全量回归；contract_change | 回滚到 3.21.1 基线 |
| 执行时误写市监 | 低 | 高 | 施工禁区；工具参数出现该路径则拒绝 | 本方案执行不含该路径 |
| 把 brain 当答案缓存，事实变了仍用旧结论 | 中 | 高 | 查询准入只认当前 facts_fingerprint；QLOC-002 阻断 | 回滚 05 文首步骤 |
| alias 收录 atoms 全文导致 json 膨胀 | 中 | 中 | 只收 SRC 编号+标题+meta 路径 | 回滚 parse SRC 段 |
| CQ-5 被改成可以不实读 | 低 | 高 | 定位表只指路，结论必须来自打开的事实文件 | 回滚 CQ-5 澄清句 |

### 6.1 回滚步骤

1. 回滚目标：Skill **3.21.1** 基线 `governance-shared/baselines/3.21.1/`（及 git tag `v3.21.1`，若已打）。
2. 操作：弃用 3.22.0 工作树改动；恢复 VERSION / skill.json / 规则 / 脚本；Portfolio 锁步回 3.21.1。
3. 回滚后不可用：会议快路径、提问对象化残差、花名册回退、误拆检测。行为回到串台前。
4. 工作区：**不需要** schema 回迁。未加 `--migrate-business` 则业务文件未被本版改写。若有人已对某项目跑了 `--migrate-business` 搬 SRC，用该次 `backup/migration-snapshot-*` 回滚该项目（本轮升级执行不对市监做这一步）。

---

## AP-7. 版本影响

| 维度 | 变更前 | 变更后 |
|---|---|---|
| Skill Version | 3.21.1 | 3.22.0 |
| Workspace Schema | 0.16.0 | 0.16.0 |
| 是否需要工作区迁移 | — | **否**（无新必填目录/字段） |
| 迁移模式 | — | N/A。可选：既有 `migrate_workspace.py` 上挂检测器，默认 dry-run |
| 是否影响核心契约 | — | **是**（SKILL.md 路由 + 00 意图/WF-3） |
| 是否影响已有工作区 | — | 结转解析更稳（运行时）；历史文件默认不动 |
| Blueprint Impact | — | full（Minor + 能力行为） |
| 双包 | 3.21.1 | 同号 3.22.0；Portfolio 无行为变更 |
| Python | ≥3.9 | 不变 |

---

## 8. 老数据：升级执行脚本怎么处理

本版 **不升 schema**，但按用户要求把历史数据处理写进脚本，而不是只写在提示词里。

| 老数据 | 谁处理 | 默认 | `--migrate-business` | 升级执行时 |
|---|---|---|---|---|
| `requirements/sources/*/meta.md` 文件名/标题/描述含 会议、纪要、腾讯会议，或 docx 且像会议导出 | `migrate_workspace.py` 检测器 | dry-run 打印「疑似会议误拆」清单，**不搬不删** | 仅对 PM 确认过的条目：复制到 `meetings/` 并在该 SRC `parse-log` 追加「误拆迁出」；**不删** fingerprint 目录 | 开发仓无 `ai/wps/` → B 节 skip；**禁止对市监跑** |
| `_index.md` §1 有「花名册」标题、无表（指针或空） | `carryover_step0.py` 运行时 | 回退上一合法日 §1；再空用 §3 姓名 | 不改历史 `_index` 文件 | 所有工作区下次结转自动受益 |
| 两日花名册都空 | 同上 | exit ≠ 0，`FAIL:ROSTER_EMPTY`，AI 只 E5 | — | 禁止手搓全员 |
| 3.18 前无结转脚本的仓 | 22 号已有无 Python 路径 | 不补历史空日目录 | 不补 | — |
| `VERSION_CAPABILITIES` | migrate 增 3.22.0 条 | `schema: 0.16.0`，`new_dirs/new_files: []`，`capabilities: ["meeting_ingest_guard","query_locator"]` | — | 跳版本升 Skill 能命中本条 |
| 无 SRC alias 的旧 brain / active-entities | 下次 `refresh_views.py --all` | 懒建重建；指纹变才写盘 | 不改历史事实文件 | 开发仓 B 节 skip；**禁止对市监跑**。用户自己项目升 Skill 后第一次查询会跑脚本 |
| 手写进 `_index` 的「主题→文件」行 | **不自动删** | dry-run 不处理 | 不处理 | 规则侧禁止再写；旧手账不扫、不迁 |

检测关键词（实施时写死在脚本，避免模型发挥）：`会议纪要` `会议记录` `视频会议` `腾讯会议` `例会` `转写`；文件名匹配优先于正文扫描。误伤合同里「会议」二字：必须 **文件名或 meta.title/description** 命中，禁止全库扫 atoms。

---

## 9. 规则补丁要点（实施时按此写，禁止发挥）

### 9.1 reply-rules.md（CR-001）

在硬规则 4 后追加（不改 1–3、不改 SKILL/05 同文三句）：

- 任何中途提问必须同时写清：已经做完什么、请你决定什么、选 A 或 B 之后会怎样。禁止只问「是否执行此方案 / 是否基于文档继续」。
- 宿主若自行弹出「文档已生成是否继续 / 执行此方案」，且本轮是查询、汇报或已给出结论：对话里写明这是宿主误弹，没有待执行方案，请忽略按钮。

正反例各加一行，指向「空壳执行门」与「宿主误弹」。

### 9.2 会议排除（CR-002，多文件同义一句）

**是会议（走 WF-3）**：腾讯/视频会议导出、会议纪要、例会记录、会议转写；用户说整理/拆解/记录 **且** 宾语或文件是上述类型。

**仍是源文档（走 P-SPLIT）**：合同/招标/立项/需求规格 + 拆文件；用户明示「把这份会议拆进 `sources/` / 当需求源文档」。

**00 §2.7 意图表必须同步**（B1 ③）：「源文档拆解入库」行追加  
`会议转写/纪要/例会导出除外（走 WF-3）`  
只改 10 号和 split-rules、不改此行 = 级联失败。

10 号 L1「整理记录」遇到会议文件 → 会议纪要，不是工时投喂。

### 9.3 WF-3 阶段序（00 表 + 02 快路径）

1. 解析（优先文末结构，不整篇 ATOM）  
2. 写 `meetings/` + index（不读不写 `todos/{今天}`）  
3. 对外结论 + 行动项清单  
4. 仅当存在 T-A4：P-CARRY → inbox→C'  
5. 其余风险/决策/变更 SUGGEST  
6. 级联验证  

02 写明：步骤 2 完成前禁止 Step 0。ASR 不是源文档。禁止因「里面可能有倒排」加载 WF-7。

### 9.4 结转脚本定位与空花名册回退（B1 ⑥）

22 / 23 P-CARRY / SKILL §5 同义：

```
python "<Skill包根>/scripts/carryover_step0.py" --root "<项目根>"
```

Skill 包根 = 与 `SKILL.md` 同级的目录（安装区或开发仓）。禁止在 `ai/`、业务项目根、cwd 的 `scripts/` 判断「脚本不存在」后手搓全员。找到包内脚本仍手搓 = 级联失败（沿用 CO-S10）。

`carryover_step0.py` 实现路径（写进 upgrade-to 原样施工）：

1. `parse_index(index_md)` 保持单文件解析，表空返回 `names=[]`。  
2. **回退在 `main()`**：对 `date≤今天` 的合法日目录倒序，调用 `parse_index`，取第一个 `len(names)>0` 的日期作为花名册源。  
3. 用了非「今天 index」的源日：stdout 含 `ROSTER_FALLBACK=<源日>`（CO-S21）。仍可用该日 §3 姓名作第二回退，stdout `ROSTER_FALLBACK=section3`。  
4. 倒序后仍 `names==[]`：`print("FAIL:ROSTER_EMPTY")`，`return 2`（exit ≠ 0，触发 22 §6 E5，**禁止** AI 手搓全员）。  
5. 禁止把「今天 index 存在但表空」当成 0 人成功（现行为 exit 0）。

### 9.5 examples/08

第 1 轮现状：把已有负责人的正式行动项做成 A 落到待办 / B 只写纪要 / C 先放着（**T-A4 可选化**，不是字面「要不要建待办」五字）。

施工：删除该 A/B/C。有负责人的正式行动项改为 00 §5.0「我已经记下了，请你认不认」。缺负责人仍问，不造无主待办。不改 BS-022 预期。

### 9.6 查询派生定位（CR-003）

05 文首（简单查询不载 00，所以 **if-else 必须写在 05 同一段**，B1 ④ / B2 ②）：

```
每一次查询（同一会话第 2 问也一样，禁止「本会话刷过就不再比」）：
  IF 有 Python ≥3.9：
      python "<Skill包根>/scripts/refresh_views.py" --project-root "<项目根>" --all
      指纹未变不得 --force 重写
      读 ai/.state.json 的 facts_fingerprint 须与本次脚本结果一致
      不一致 = stale，禁止用旧 brain 作答
  ELSE（无 Python 或脚本失败）：
      不阻断、不报错当失败门
      不读过期 brain 当真理
      按四个加速器定向读事实文件，声明 as-of（BRN-004）
```

随后：
3. 定位：`context/active-entities.json` 的 `alias_index`（以及 brain「## 别名跳转」短表）。一跳：精确编号 → WP/TD 名 → 词库 canonical → SRC 标题。
4. 命中后实读该 `path`，总数 ≤3 个事实文件。第 4 个起 = 本轮查询失败。
5. 未命中：只打开四个加速器（`wps/_index.md`、`requirements/sources/_index.md`、最新合法日 `todos/_index.md`、`risks/risk-register.md`），仍无则声明缺什么。
6. 禁止：`backup/`、`archive/`、兄弟项目、`**/atoms/**` 全文、上一对话正文当证据、「为求稳再对一遍」。
7. 只读查询三处同时收口（B2 ③ / B1 ②）：  
   - §1b inbox 非空 → HINT，禁止 AUTO C'  
   - §2.5a 待办文件不存在 → 不 Step 0、不建今天目录  
   - §6.3 快捷「待办查询」行：文件不存在时 HINT，不触发结转生成  
8. CQ-5：禁的是对话记忆/未打开文件的内容；指纹一致的派生定位表必须用来找路。定位表不是答案。
9. 用户说「把定位写进索引」：写 `domain-glossary` alias（待确认）→ 确认后 P-VIEWS。禁止手改 `wps/_index`、`brain.md`、`active-entities.json`。
10. §1.5 查询术语归一化：禁止触发 17 §8.1 自动 pending（B2 ⑤）。只允许 §9.7 的 SUGGEST ≤7。

`refresh_views.py`：

- 解析 `requirements/sources/*/meta.md`：`source_id`、title/description（≤40 字）、path。写入 entities `type=src` 与 alias_index。不读 atoms/facts 正文。
- `brain_fact_globs` 增加 `requirements/sources/_index.md`、`requirements/sources/*/meta.md`。
- `render_brain`「## 别名跳转」改为短表：词库 confirmed + 进行中 WP 名称 + SRC 标题，单表上限 80 行；全文仍以 json 为准。禁止把待办标题全量灌进 brain 短表（json 可保留 TD alias）。

### 9.7 口低闸证高闸（CR-004）

17 号查询路径改闸（日报/会议/拆解的攒批 pending **保持**）：

- 简单查询 / 只读分析：**禁止** §6.1 第 6 步自动写入 pending。本轮可用「按候选理解」标注，不写盘。
- 同一轮最多一张 SUGGEST：≤7 个词，每词一行「原词 → 候选标准词（一句）」。禁止每个缩写弹一次。
- 用户说「写这几个 / 进词库」→ 只把点名的词写入 **pending**（不是 confirmed）。
- T1「X 就是 Y」/ T2 对当前术语追问答「对」→ **confirmed**（沿用 17 §6.3）。
- 「有道理 / 80% / 差不多」**不是** T1/T2，不得升 confirmed。
- 推导过程、网页旁证、置信度独白：不写词库、不写 journal、不写 project-notes。
- pending 释义 ≤40 字；来源=本轮用户点名或投喂，禁止来源=「模型推断」。
- 查询命中 pending：可用来找路，对外必须带「待确认」，禁止静默当政务外网/网关事实。

05：只读轮发现生词 → 走上面 SUGGEST，不 CALL 写词库。与 §6.3a「最小读取不得写入」对齐。§1.5 查询术语归一化必须写明：查询轮禁止触发 17 §8.1 自动 pending（B2 ⑤）。

reply-rules（可并入 CR-001 残差，避免第四处同文）：对外推断必须标推测；用户夸推导质量 ≠ 确认命题。

---

## 10. 拟拆 CR（准许执行后才落盘）

| CR | 目标 | 主文件 | 类型 |
|---|---|---|---|
| CR-20260831-001 | 对外提问必须带对象；宿主假执行门须拆穿。不重做 3.18 假执行门主体 | `reply-norm-skill/references/reply-rules.md` 及 boundary | contract_change 否；capability_change 弱（残差） |
| CR-20260831-002 | 会议投喂快路径；结转脚本包内定位；花名册空表回退；migrate 误拆检测 | SKILL/00/02/10/23/22/split-rules/脚本/示例/回归 | contract_change + capability_change |
| CR-20260831-003 | 查询用指纹派生定位，不用会话记忆；SRC 进 alias；只读查询不 C' | 05/SKILL §5.3/00 CQ-5/17/view-spec/refresh_views/回归 | contract_change（SKILL+00）+ capability_change |
| CR-20260831-004 | 查询不自动写词库；升格认命题不认 80%；PM 随口仍可 T1/点名写入 | 17 §6.1 查询闸 + 05 SUGGEST 一批 + 回归 | capability_change |

验收：001 → RN-010/011 + RN-003 仍过。002 → Module 76 阻断项 + SF-001/BS-022/CO-S10。003 → QLOC-001～005/007 + BRN-003 + ALI-001。004 → TERM-001～004。

---

## 11. 复杂度与扩展优先

全部需求均扩展现有能力，**0 个新规则文件**。

| 指标 | 升级前 | 本次新增 | 本次简化 | 升级后 | 是否超阈值 |
|---|---|---|---|---|---|
| 规则文件数 | 21 + 3 能力目录 | 0 | 0 | 同 | 否 |
| 模板数 | 39 | 0 | 0 | 39 | 否 |
| 回归用例 | 807 | ~19 | 0 | ~826 | 否（<15%） |
| 提示词 | 重 | 会议排除 + 提问对象 + 查询硬步骤约 +1–1.5k 字 | 删 00 WF-3 过时 SUGGEST；示例去违规问句 | 净增小 | 否 |

简化项：00 WF-3 与 02 并口径；`examples/08` 去掉违规「要不要建待办」。R3 不新增记忆文件，只硬化已有 brain/alias。

---

## 12. 联动更新（实施同节点）

| 场景 | 顺序 | 失败 |
|---|---|---|
| 改会议路由 | 10 → 00 §2.7 → SKILL §6 → 23 → split-rules 排除 → MTG-001/002 | 回滚该节点全部 |
| 改结转脚本 | carryover_step0.py → 22 说明 → SKILL §5 → 23 P-CARRY → CO-S20/21/22 | 回滚脚本+说明 |
| 改提问 | 只 reply-rules（不改底线 14–16）→ RN-010/011 | 回滚该文件 |
| 改查询定位 | view-spec globs → refresh_views parse SRC → 05 文首 → SKILL 5.3 → CQ-5 澄清 → QLOC-* | 回滚该节点 |

禁止先改路由、过几天再改 23（否则过程树与 SKILL 不一致）。

---

## 13. 方案关键断言（B 证伪则阻塞）

| 关键断言 | 依据 | 若被证伪 |
|---|---|---|
| R1 主体已在 3.18.0 / RN-003 落地 | `CR-20260827-005`、`reply-rules.md` 硬规则 3–5 与正反例第 1 行 | 阻塞（则必须当新能力重做，与本基线冲突） |
| 截图 2 主因是链路串台不是 docx 体积 | 路由重叠 + 脚本 cwd + 花名册 0 人 + 先结转后纪要；docx 56KB | 阻塞 |
| 写 `meetings/` 不触发 22 | 22 时机 0 = 读或写 `todos/{今天}` | 阻塞 |
| 会议排除不会改合同 P-SPLIT | 排除绑会议类型；MTG-002 / SF-001 | 阻塞 |
| 升级执行不写市监 | 用户硬约束 | 阻塞 |
| schema 不升仍能处理老数据 | 检测器 + 运行时回退，无新必填目录 | 阻塞 |
| 不新建 NN 规则文件 | 16 号 + 本 AP-4 | 阻塞 |
| R3 不引入会话记忆/答案缓存 | §0.4 / §9.6；brain 仍禁止待拍板 | 阻塞 |
| 查询结论必须来自实读事实文件 | CQ-5 + QLOC-004 | 阻塞 |
| SRC atoms 不进 alias | 只 meta 标题/编号 | 阻塞 |
| 只读查询不触发 Step 0 / C' | QLOC-005；05 §1b 收口 | 阻塞 |
| 「80% 有道理」不等于确认命题 | 17 T1/T2；TERM-002 | 阻塞 |
| 只读查询不自动写词库 pending | 17 §6.1 查询闸；TERM-001 | 阻塞 |

**放行门槛**：全部断言未被证伪且无新阻塞 → 通过-可执行 / 通过-待修订。断言被证伪 → 修订-需再审。

**非阻塞取舍**：不拆除宿主按钮；T-A4 周一仍全员结转（先纪要）；误拆 SRC 不自动搬；R1 按残差而非新能力（用户已裁决）；宿主冷启动加载 SKILL 正文本包消不掉。

---

## 14. 需求实现偏差验证

| 原始需求点 | 方案对应 | 是否完全覆盖 | 是否扩展 |
|---|---|---|---|
| 间断提问落到假 skill | CR-001 只改 `reply-norm-skill` | 是（残差；主体 3.18 已有） | 无新目录 |
| 先查是否处理过 | §0.2 / 断言 1 | 是 | 否 |
| 拆解记录太久 / 查链路 | CR-002 路由+顺序+脚本+花名册 | 是 | 否 |
| 不操作市监 | 施工禁区 | 是 | 否 |
| 升级脚本处理老数据 | §8 migrate + parse_index + 下次 P-VIEWS 重建 alias | 是 | 不自动搬（已裁决） |
| 换对话查询慢 / 怕记忆过期 | CR-003 指纹派生定位，禁止会话记忆与手写主题地图 | 是 | 不缓存答案 |
| 随便说能记 vs 记多变慢 vs 下次没上下文 | CR-004 口低证高：PM 投喂/T1 才落盘；AI 自推不记过程；查询不自动 pending | 是 | 不新建知识库 |

忠实于已裁决基线：**是**。目标偏移：**否**（R3 按用户增量纳入，明确拒绝「加记忆」）。

---

## 15. 给 B 的审核要点

B 须自行扫描本仓库（3.21.1 / `e6954e1` / 本 AP 已入 `planning/`）。不得把 A 的结论当事实。须独立辩论需求（R1 残差是否足够、R2 排除词是否过宽、R3 用派生定位而非记忆是否足够，以及 `refresh_views.py` 是否确实未索引 sources）。

B 审核前向用户确认工作空间仍是 `C:\Users\qiusuo\Downloads\ChronoPM Skill`，并声明不读不写市监。

结语四档：通过-可执行 / 通过-待修订 / 修订-需再审 / 重做-需再审。  
需求裁决建议与方案结语分开写。用户已裁决继续实施，B 不得以「需求不该做」为由改写基线；若认为需求不应做，只能建议用户重新裁决，方案结语不得「通过-可执行」。

---

## 16. 当前结论

- 方案版本：AP **0.5**。B1 **通过-可执行**（第二轮 6/6 闭合）；B2 **通过-待修订**（尚未复审）。§19 已闭合 A 的修订项。
- 尚未准许执行：不得改 Skill 规则/脚本（本 AP 除外）、不得建 CR/IA、不得跑市监 migrate。
- B2 复审通过 + 用户回复「同意执行」后，A 按 §9.2/§9.4/§9.6/§9.7 与 AP-4 分条写 CR + `upgrade-to-3.22.0.md` 并最小补丁施工。

---

## 17. B2 审核结果

> 本章节由 Agent B2 独立审核后写入。复审时**重写覆盖**本章节全部内容，不改动文档中其他 Agent 的内容。章节号固定为 `17`。

### 17.1 审核范围与声明

- 审核对象：本 AP **v0.5**（CR-20260831-001/002/003/004，Target 3.22.0），含 A 修订闭合（§19）后的回写落点。
- 独立核验：未采信 A / B1 的结论。直接扫描仓库 3.21.1 / `e6954e1`（`git log -1` = `e6954e1 2026-08-30 17:56:57 +0800`）与当前工作树。
- 声明：不读不写 `C:\Users\qiusuo\Downloads\市监重构项目管理`；工作空间确认为 `C:\Users\qiusuo\Downloads\ChronoPM Skill`。
- 审核日期：2026-08-31（第二轮复审）。B2 历史结论：AP 0.4 曾为「通过-待修订」（修订项①–⑤）；本轮核验 §19 是否闭合。

### 17.2 §19 闭合核验（B2 上轮 ①–⑤ 修订项逐项复核）

| B2 上轮项 | 闭合方式（A 声明） | B2 复核实测 | 结果 |
|---|---|---|---|
| ① examples/08 措辞精确化 | AP-2 / §9.5 / AP-4 改称「T-A4 可选化为 A/B/C」 | AP-2 L235 已改为「做成 A 落待办 / B 只写纪要 / C 先放着（可选化，违反 02 §2.2 MANDATORY）」；§9.5 L576 已写明「不是字面『要不要建待办』五字」；AP-4 L375 改为「删除 T-A4 的 A/B/C 可选化」 | ✅ 闭合 |
| ② 无 Python 降级同段 if-else | §9.6 改为 05 文首 if-else 一块 | §9.6 L582–595：if-else 代码块同段写明「有 Python → 跑包内 refresh_views」「ELSE（无 Python 或脚本失败）→ 不阻断、BRN-004 定向读 + as-of」；AP-4 L376 对应「文首 if-else」 | ✅ 闭合 |
| ③ 只读查询三处收口 | AP-4 拆三条 edit_section | AP-4 L377–379：§1b（inbox→HINT 禁 C'）、§2.5a+§6.3（不 Step 0、不建档）、§1.5（禁自动 pending）三条独立列出；§9.6 L602–605 第 7 步同步列三处 | ✅ 闭合 |
| ④ QLOC-006 列入 5.4 | 5.4 增「非阻断」清单 | §5.4 L460 新增「非阻断（须实现、失败不挡发布）：QLOC-006（SRC 标题定位）、TERM-004、RN-010/011、MTG-005」 | ✅ 闭合 |
| ⑤ 查询归一化禁自动 pending | 05 §1.5 单独一条 + §9.6 第 10 步 + §9.7 | AP-4 L379 有 05 §1.5 行；§9.6 L608 第 10 步明写「禁止触发 17 §8.1 自动 pending（B2 ⑤）」；§9.7 L629 05 段落末重申 | ✅ 闭合 |

结论：B2 上轮 5 项修订**全部闭合**，无漏项、无半闭合（条件句/落点/引用编号均落到具体条款）。

### 17.3 B1 修订项的 B2 交叉复核（不替代 B1，仅验证 A 回写是否到位）

| B1 项 | B2 复核落点 | 结果 |
|---|---|---|
| B1② 05 三处显式列出 | AP-4 L377–379 三条独立行 | ✅（与 B2③ 同步闭合） |
| B1③ 00 §2.7 会议排除句 | AP-2 L223 + §9.2 L539–541 + AP-4 L361 三处均含「会议转写/纪要/例会导出除外（走 WF-3）」；§9.2 明写「只改 10 号和 split-rules、不改此行 = 级联失败」 | ✅ |
| B1④ if-else 同段 | §9.6 L582–595 + AP-4 L376 | ✅ |
| B1⑥ 回退实现路径 | §9.4 L566–572：`main()` 倒序合法日、`ROSTER_FALLBACK=<源日>` / `ROSTER_FALLBACK=section3`、都空 `FAIL:ROSTER_EMPTY` + exit 2；AP-4 L370 同步 | ✅ |

B1 独立发现项（①⑤）与 B2 上轮项重合或属 AP 文字级，B2 不再重复核验，以 §18 原文为准。

### 17.4 对 §13 关键断言的证伪结论（本轮维持）

B2 上轮已核 19 项断言全部通过（含版本快照、22 号时机 0、refresh_views 无 sources、05 AUTO C'/Step 0、17 自动 pending、回归基线 807、`reply-norm-skill` 无 SKILL.md 等）。本轮抽查新增引用的真实性：

| 新增引用 | B2 实测 | 结果 |
|---|---|---|
| 22 §6 E5 兜底（exit ≠ 0 只对 FAIL 人兜底） | `22-carried-over-rules.md` L190–198 错误处理表 E5 在位；L20/L81 明写「脚本 exit ≠ 0 只对 FAIL 的人按 §6 E5 兜底，不算手搓全员」 | ✅ |
| `ai/.state.json` 键名 `facts_fingerprint` | `refresh_views.py` L363/602/671/727 四处读写该键 | ✅ |
| BRN-003 / BRN-004 用例存在 | `regression-suite.md` L1197 BRN-003「先 brain；不载 00」、L1198 BRN-004「无 Python / 脚本失败 → 读 WP 原文；声明可能过期」 | ✅ |
| 花名册回退第二源（§3 姓名作第二回退） | 22 号/todos `_index` 结构中 §3 = 当日参与，回退用该日 §3 属同源扩展，方案 §9.4 已自洽 | ✅ |
| §13 全部 13 条断言 | 本轮无新证据证伪任何一条；「不新建 NN 规则文件」「schema 不升」「不写市监」与 AP-4 施工禁区一致 | ✅ |

### 17.5 本轮 B2 新发现（轻微，不阻塞）

| # | 问题 | 严重度 | 说明与建议 |
|---|---|---|---|
| ① | SKILL.md §5.1b 的 P-VIEWS 命令（L86 `python scripts/refresh_views.py --project-root <根> --all`）仍是相对 cwd 写法，AP-4 只列了 SKILL.md §5.3 行改包内路径，未显式列 §5.1b 行 | 低 | 与 carryover 同病（22/SKILL §5），修法相同。**建议**：upgrade-to 施工时 SKILL.md 的脚本路径统一改为 `"<Skill包根>/scripts/…"`，§5.1b 一并覆盖，不必回写 AP |
| ② | §9.6 refresh_views 新增「parse SRC meta 写 entities type=src」与 view-spec.json 新增 globs，但 AP-4 未列 `context/active-entities.json` 模板或 05 对 `src` 类型的读法说明 | 低 | entities 结构由脚本自派生，无需模板；05 定位步骤已含「SRC 标题」一跳。**建议**：施工时在 05 §1 定位句把 SRC 标题一跳写完整即可，无需改 AP |
| ③ | MTG-003 用例「再跑**包内**脚本」的预期，隐含 CO-S20 已先行存在；两用例独立运行时 fixtures 需共享同一技能包路径配置 | 低 | 回归实施细节。**建议**：套件施工时在 Module 76 头部注明依赖 `CO-S20` 的包内路径 fixture |

三项均为实施细节级，可在 `upgrade-to-3.22.0.md` 施工清单中顺带处理，不要求回写本 AP。

### 17.6 需求裁决建议（与方案结语分开）

- R1（残差）：维持同意。残差句（RN-010/011）落 reply-rules，不重写 3.18 主体。
- R2（会议链）：维持同意。会议排除句、WF-3 阶段序、脚本包内定位、空花名册回退（含第二回退源）在 AP-2/AP-4/§9.2–§9.4 均已可施工。
- R3（查询派生定位）：维持同意。05 文首 if-else + 三处收口 + alias 扩 SRC 后，查询链路自洽；明确拒绝会话记忆与手写主题地图。
- R4（口低闸证高闸）：维持同意。查询轮禁自动 pending、SUGGEST ≤7、升格只认 T1/T2 命题，与 17 号现状诊断闭合。
- 用户已裁决继续实施；B2 无「需求不应做」的反建议，无重新裁决诉求。

### 17.7 方案结语（四档之一必选）

**通过-可执行。**

理由：AP 0.4 的全部关键断言经 B2 两轮独立核验未被证伪；B1/B2 的全部修订建议（B2 ①–⑤、B1 ①–⑥）已在 §19 闭合并回写到 AP-2/AP-4/§5.4/§9.2/§9.4/§9.5/§9.6/§9.7 对应落点，B2 逐项复核确认无漏项；本轮新发现仅 3 项轻微实施细节（§17.5），可在施工清单顺带处理，不构成阻塞。方案忠实于已裁决基线（R1–R4），无目标偏移。

**前置条件**（用户回复「同意执行」后 A 才可动工）：
1. A 建 CR-20260831-001～004 + IA-001～004 + `upgrade-to-3.22.0.md` 施工清单（按 §19 落点分条，含 §17.5 三项顺带处理）。
2. 施工最小补丁，全量回归：阻断项（MTG-001～004、CO-S10/S20/S21/S22、RN-003、SF-001、MIG-001/002、BS-022、QLOC-001～005/007、BRN-003、ALI-001、TERM-001～003）全过 + 非阻断项（QLOC-006、TERM-004、RN-010/011、MTG-005）须实现；合计以发布时套件为准（预估 826）。
3. 禁止写市监、禁止升 schema、禁止新建 NN 规则文件（施工禁区照抄）。

**复审机制**：若 A 施工中偏离 §19 落点或回归失败，B2 下一轮复审降档为「修订-需再审」并重写本章节。

---

## 18. B1 审核结果（第二轮，AP 0.5 复审）

> 本章节由 Agent B1 复审后**重写覆盖**。不改动文档中其他章节（含 §17 B2 审核结果、§19 A 修订闭合）。章节号固定为 `18`。

### 18.1 复审范围

- 审核对象：AP **0.5**（CR-20260831-001/002/003/004，Target 3.22.0）。
- 复审焦点：B1 第一轮（AP 0.4）提出的 6 条修订建议（§18.4 ①–⑥）是否已回写 AP 正文。
- 不重复第一轮已核验的 17 项事实断言（仍有效）；本节只核验修订落点。

### 18.2 六条修订逐项核验

| B1 编号 | 严重度 | 原要求 | A 落点 | B1 核验 | 结论 |
|---|---|---|---|---|---|
| ① | 低 | examples/08 措辞精确化：不是字面「要不要建待办」，而是 T-A4 可选化为 A/B/C | AP-2 L235「把 T-A4 做成 A 落待办/B 只写纪要/C 先放着（可选化）」；§9.5 L576「**T-A4 可选化**，不是字面『要不要建待办』五字」；AP-4 L375 同义 | 措辞已精确，三处一致 | ✅ 闭合 |
| ② | 中 | 05 修改点三处显式列出（§1b / §2.5a+§6.3 / §1.5） | AP-4 拆成 4 条 edit_section：05 §1（L376）、05 §1b（L377）、05 §2.5a 与 §6.3（L378）、05 §1.5（L379）；§9.6 第 7 步列三处收口（L602–605） | 三处（实际四处含 §1.5）均已显式列出 | ✅ 闭合 |
| ③ | 中 | 00 §2.7 意图检测表加会议排除句 | AP-2 L223 显式列出排除句；§9.2 L539–541「**00 §2.7 意图表必须同步**」+ 排除句原文 + 「只改 10 号和 split-rules、不改此行 = 级联失败」；AP-4 L361 对应 edit_section | 三处（AP-2/§9.2/AP-4）一致，排除句原文可抄 | ✅ 闭合 |
| ④ | 中 | 05 文首 if-else 块（有/无 Python 同段） | §9.6 L582「05 文首（…if-else 必须写在 05 同一段）」；L584–595 给出完整 if-else 代码块；AP-4 L376 对应 edit_section | if-else 块完整，含 Python 路径 / ELSE 降级 / BRN-004 as-of | ✅ 闭合 |
| ⑤ | 低 | QLOC-006 列入 §5.4 或注明非阻断 | §5.4 L460「非阻断（须实现、失败不挡发布）：QLOC-006（SRC 标题定位）…」 | 已列入非阻断清单 | ✅ 闭合 |
| ⑥ | 中 | `carryover_step0.py` 回退实现路径写清 | §9.4 L566–572 五步实现路径（parse_index 保持单文件 → main 倒序 → ROSTER_FALLBACK → ROSTER_EMPTY exit 2 → 禁止 exit 0）；AP-2 L233 对应行；AP-4 L370 对应 edit_section；CO-S21/CO-S22 用例已在 §5.1 | 实现路径完整，exit code / stdout 标记 / 回退逻辑均可施工 | ✅ 闭合 |

**结论：6/6 全部闭合。**

### 18.3 §19 修订闭合表核验

| §19 行 | B1 核验 |
|---|---|
| B2①/B1① → AP-2、§9.5、AP-4 | ✅ 三落点均在 |
| B2②/B1④ → §9.6、AP-4 `05` §1 | ✅ |
| B2③/B1② → AP-4 拆三条 edit_section；§9.6 第 7 步列三处 | ✅（实际拆成四条含 §1.5，更细） |
| B2④/B1⑤ → §5.4 增非阻断清单 | ✅ |
| B2⑤ → AP-4、§9.6 第 10 步、§9.7 | ✅ |
| B1③ → AP-2、§9.2、AP-4 00 | ✅ |
| B1⑥ → §9.4、AP-4 脚本 | ✅ |
| 「未采纳：无」 | ✅ 同意，无遗漏 |

§19 闭合表与 B1 实际落点完全一致，无遗漏、无错位。

### 18.4 修订引入的新问题检查

逐项检查 AP 0.5 修订内容是否引入新的不一致：

| 检查项 | 结果 |
|---|---|
| §9.2 排除句 vs AP-2 L223 vs AP-4 L361 三处文字是否一致 | ✅ 均为「会议转写/纪要/例会导出除外（走 WF-3）」 |
| §9.6 if-else 代码块 vs AP-4 L376 行数估计（15–25） | ✅ 代码块约 12 行 + 说明文字，在估计范围内 |
| §9.4 五步实现 vs AP-4 L370 行数估计（40–80） | ✅ 五步约 20 行改动，在估计范围内 |
| §5.4 非阻断清单新增 QLOC-006 等 4 项 vs §5.1 用例表 | ✅ QLOC-006/TERM-004/RN-010/011/MTG-005 均在 §5.1 有对应用例 |
| §16 结论「AP 0.5；§19 已闭合其修订项」 | ✅ 与事实一致 |
| §9.6 第 10 步「§1.5 查询术语归一化禁止触发 17 §8.1」 vs §9.7 对应段 | ✅ 两处同义 |

未发现新不一致。

### 18.5 方案结语

**通过-可执行。**

理由：
1. 第一轮 6 条修订建议（4 中 + 2 低）已全部正确回写 AP 0.5 正文（AP-2 / AP-4 / §5.4 / §9.2 / §9.4 / §9.5 / §9.6）。
2. §19 修订闭合表与 B1 实际落点核验一致，无遗漏。
3. 修订未引入新的不一致。
4. 全部 17 项事实断言（第一轮核验）仍有效，无断言被证伪。
5. 需求基线 R1–R4 不变。

用户回复「同意执行」后，A 可按 §9.2/§9.4/§9.6/§9.7 与 AP-4 分条写 CR + `upgrade-to-3.22.0.md` 并最小补丁施工。禁止写市监。

---

## 19. A 修订闭合（AP 0.5，不改写 §17/§18 原文）

B1/B2 结语均为 **通过-待修订**。下列条目已回写本 AP（AP-2 / AP-4 / §5.4 / §9.2 / §9.4 / §9.5 / §9.6 / §9.7），施工时 `upgrade-to-3.22.0.md` 按这些落点抄，不再另发明。

| 来源 | 项 | 严重度 | 闭合方式 | 落点 |
|---|---|---|---|---|
| B2① / B1① | examples/08 不是字面「要不要建待办」 | 低 | 改称「T-A4 可选化为 A/B/C」；施工删该三选项，改为已记下请认 | AP-2、§9.5、AP-4 |
| B2② / B1④ | 无 Python 降级须与「每问跑脚本」同段 | 中 | §9.6 改为 05 文首 if-else 一块 | §9.6、AP-4 `05` §1 |
| B2③ / B1② | 只读查询须同时收口 §1b / §2.5a / §6.3 | 中 | AP-4 拆成三条 edit_section；§9.6 第 7 步列三处 | AP-4、§9.6 |
| B2④ / B1⑤ | QLOC-006 未进 5.4 | 低 | 5.4 增「非阻断」清单，含 QLOC-006 | §5.4 |
| B2⑤ | 查询归一化仍可能走 17 §8.1 | 低 | 05 §1.5 单独一条：禁止自动 pending | AP-4、§9.6 第 10 步、§9.7 |
| B1③ | 00 §2.7 意图表缺会议排除句 | 中 | 「源文档拆解入库」行必须加「会议转写/纪要/例会导出除外（走 WF-3）」 | AP-2、§9.2、AP-4 00 |
| B1⑥ | 花名册回退实现写清 | 中 | 回退在 `main()` 倒序合法日；`ROSTER_FALLBACK`；都空 `FAIL:ROSTER_EMPTY` + exit 2 | §9.4、AP-4 脚本 |

未采纳：无。未把任何 B 项升为阻塞。需求基线 R1–R4 不变。

用户回复「同意执行」后：建 CR-001～004 + IA + `upgrade-to-3.22.0.md`（施工清单按上表分条），再最小补丁。禁止写市监。
