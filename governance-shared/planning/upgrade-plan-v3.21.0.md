# 升级方案审查文档 AP — ChronoPM 3.21.0

> 治理位置：`governance-shared/planning/upgrade-plan-v3.21.0.md`（16 号：每周期限 1 个，本文件原地修订）。  
> 本轮状态：**V0.6**。B4「通过-可施工」低优先四条已写入正文。未授权执行。禁止写市监、禁止改 Skill 正文。  
> git：不引入。schema：**保持 0.16.0**。

---

# 0. 修订记录

## V0.1 → V0.2（用户裁决）

V0.1 把视图脚本化留给 3.22。用户否决版本切架构。V0.2：协议一次给全；激活靠探测；不升 schema。

## V0.2 → V0.3（消化 B1）

B1 结论「修订-需再审」**成立**。六条放行条件全部采纳，不改架构、不升 schema、不碰市监：

| B1 | 采纳 | V0.3 落点 |
|---|---|---|
| 1 一处定义物理载体 | 是 | 新增 `scripts/view-spec.json`；脚本与 AUTO 都读它；11/00 禁止另列指纹/投影列 |
| 2 原子写 | 是 | 每视图写临时文件再 `os.replace`；`.state.json` 分视图指纹；失败标 stale 不回滚已成功视图的事实 |
| 3 活表含 TD | 是 | entities[] = 进行中 WP + 未办结 TD + 开放 R/I + 在册人员 |
| 4 journal 入指纹 | 是 | `.state.json.journal` 独立段 |
| 5 纠偏确认边界 | 是 | 仅用户发起的 P-CORRECT 视为已确认；AI 自检冲突仍进 pm-decisions |
| 6 回归 30 条可枚举 | 是 | Module 75 固定 30 个 ID，合计 807 |

另采 B1 非阻塞建议：20 号 / `_version.py` 写死 schema 判别式（必填目录或迁移义务才升 schema；懒建派生物不升）。

## V0.3 → V0.4（消化 B2）

B2 结论「通过-待修订」接受。四处全部写入正文，不留「施工时再补」：

| B2 | 采纳 | V0.4 落点 |
|---|---|---|
| 1 SPEC-002 JSON↔模板 | 是 | `--check-spec`：index/§3 表头必须 == view-spec；不一致 fail。SPEC-001 含此检查（不另增 ID，合计仍 807） |
| 2 alias 派生源 | 是 | §5 `alias_index` 源表：词库 §1 confirmed + §2 纠错原词 + WP 名称 + 废弃 WP/`supersedes` + 花名册名 + `_index` §6 缩写 |
| 3 facts glob | 是 | `.state.facts` 覆盖清单写死 |
| 4 指纹命名 | 是 | 统一 `facts_fingerprint` / `journal_fingerprint` / `views.*.view_fingerprint` |

## V0.4 → V0.5（消化 B3）

B3「通过-待修订」接受。B3-1 选 **删 brain 待拍板节**（不复制实时确认面）。四处均写入正文：

| B3 | 采纳 | V0.5 落点 |
|---|---|---|
| 1 brain vs pm-decisions 双源 | 是：brain **禁止**待拍板节 | §5 brain 节清单；05 横幅仍实时读 `pm-decisions.md` |
| 2 term 两跳链 | 是 | §5 P-RESOLVE：alias → term.canonical → wp.name/aliases → wp.id |
| 3 最新合法日 | 是 | 改引 22 号原文：`date≤今天` 且存在 `_index.md` 的最大日期 |
| 4 无 .state 降级 | 是 | C2 缺 `.state.json` = 全部 stale，走 05 第 2 条 |

## V0.5 → V0.6（消化 B4 + 收口）

B4「通过-可施工」接受。低优先三条写入正文；B4-4 写成施工/回归必检。顺手修两处会让 ALI-001 在全链通失败的缺口：

| B4 / 自检 | 采纳 | V0.6 落点 |
|---|---|---|
| 1 派生读派生 | 是 | `type=wp` **只读** `wps/WP-*.md` frontmatter；`_index` 由同一次 parse 写出，禁止用 §1 当收录判据 |
| 2 多条 alias 优先级 | 是 | P-RESOLVE 类型序：精确 ID → wp/td → term 第二跳 → person（仅指人）；同类型再用原文里的 开办/变更/注销 收口 |
| 3 探测 vs 重建 | 是 | C2：查询准入只比 `facts_fingerprint`；P-VIEWS 写盘时 facts **或** journal 变了都重建 |
| 4 ALI-001 真实库 | 是 | 回归 fixture 摘 WP-20260827-001 §3「农民专业合作社」；施工只读抽查市监该文件，**禁止写入** |
| 自检 | 第二跳多总包 | 「农专」功能点同时在开办/变更/注销总包；必须用「注销」等词过滤后再问 |

# 1. 原始需求照抄

## 1.a 第一轮

```
我总会担心视图的时效性……纠偏……回复粒度。
口径纠偏、四级深度、指纹重建。
边界：叠层不改宗教；brain/json 脚本重建；不写 wiki；不动市监；不用 git。
字段清单 + 00/05/10/23 最小规则集。
JSON 是否预留 aliases 和 corrections？倾向预留。
全部回退，先写方案。Agent A。能改的都优化掉。小版本号。
```

## 1.b 第二轮（本轮裁决 + 新约束）

```
按你的想法来，但是你要考虑，skill实际使用过程中，很多人会存在跳版本升级的情况，后面如果要升，还是会发生步子迈得太大的问题。所以最好的处理方式，不是按版本切割升级的步骤，而是想一套能够完整兼容的有效方案。
```

---

# 2. Agent A 对需求的理解

用户裁决 = **按 V0.1 的技术收敛**（不做 git、不把 JSON 当口径家、不升 schema、不迁 3700 文件、不清空实体级联 8a），**但推翻「架构按版本切片」**。

正确目标不是「3.21 做 40%、3.22 做 60%」，而是：

> 一套从 3.21 起就完整的百科协议；旧工作区不搬家也能用；跳过若干 Skill 版本只表现为「同一协议的脚本/规则更完整」，不表现为「还缺一层必须先升级才能用的结构」。

跳版本今天已经痛在 schema 链（0.10 wps、0.14 pm-decisions、0.15 project-info）。百科协议 **禁止再加一节 schema**，否则 3.20→3.25 仍要迈结构大步。

---

# 2.5 工作空间版本快照

| 项目 | 值 |
|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` |
| 版本标识 | Skill 3.20.0；schema 0.16.0；HEAD `c2b6831` |
| 本轮磁盘相对 c2b6831 | 仅本 AP（现 V0.6） |
| 快照时间 | 2026-08-30 |
| 用户确认 | 路径沿用此前指定；本轮请再确认一次 |
| 业务库 | 市监 **零写入** |

---

# 1.6 需求裁决记录（辩论终止）

| 项 | 结果 |
|---|---|
| 收敛（git / JSON 可写 corrections / 升 schema / 迁存量 / 清空 8a 实体级联） | **按 A** |
| 架构按 3.21/3.22 切片 | **否决** |
| 替代 | **3.21 一次给出完整兼容协议** |
| 辩论 | 终止。下文只忠实执行本基线 |

---

# AP-1. 变更概述

3.21.0 交付 **完整百科叠层**（不是半套）：

1. 证据只追加：`ai/logs/journal/` 懒建（旧日报/纪要不回迁）。
2. 事实不搬家：`wps/` `todos/` 登记册照旧。
3. 派生视图 **全部** 有脚本生成器：brain、active-entities、.state、WP `_index`、`_wp-chart`、PLAN §3§4 投影。
4. 运行时双轨：**有 Python → 脚本是视图权威；无 Python → 现有 AUTO 兜底。** 同一套语义，不是两个架构。
5. 纠偏只写事实或词库；L0–L3；日报默认更新活实体。
6. schema 仍 0.16.0。migrate **不**建必填新目录、**不**改业务 md。跳版本 = 换 Skill 包 + 首次会话脚本懒建。

PM 无新套话、不学 git。

---

# AP-2. 影响点

| 影响项 | 当前 | 变更后 | 程度 | 可逆 |
|---|---|---|---|---|
| 查询主路径 | 定向读待办/_index | 先 P-VIEWS（能跑则跑）再读 brain；无脚本则 3.20 路径 | 中 | 是 |
| 视图写入 | 00 AUTO 手写 index/图/PLAN 投影 | **脚本优先，AUTO 仅兜底** | 高 | 是 |
| 00 §8a 实体级联 | 待办↔风险↔问题 CHECK/SUGGEST | **保留**（不是视图保姆） | 无删 | — |
| 对齐 | WF-8 语义搜待办 | 先活实体表 | 中 | 是 |
| 纠偏 | 易进八块 / 易只改派生 | 写事实+词库，视为已确认 | 中 | 是 |
| 05 粒度 | 待办有展开词；进度完整表 | L0–L3 覆盖；清单/周报仍 L3 | 中 | 是 |
| migrate | VERSION_CAPABILITIES 到 3.20 | 增 3.21 一条：`encyclopedia_overlay`，new_dirs=[] | 低 | 是 |
| 20 号健康检查 | 缺目录常当缺失能力 | **缺 brain/journal 不致命**（同 3.4 timeline） | 低 | 是 |
| 市监 | — | 零写 | — | — |
| Portfolio | V-1～14 | 仅同号 3.21.0 | 无行为 | 是 |
| 契约 #4 #8 | 禁临时脚本；改目录升 schema | 打包脚本；懒建不升 schema | 断言 | — |

---

# AP-3. 策略

**为什么不切片：** `get_capabilities_since(from)` 会累加从旧版到当前的每一档。若 3.21 只交 brain、3.22 才交视图脚本，从 3.20 跳到 3.25 的人会一次面对「新目录 + 新脚本 + 删 AUTO + 新对齐」——正是用户要避免的。

**完整协议 + 双轨运行：** 结构一次定义死。运行时用能力探测（Python? 指纹? 文件在否?），不用「你是不是经过了 3.21」。

**否决：** 顶层 `journal/`、升 0.17.0、JSON 可写 corrections、git、迁存量、把 8a 实体级联当视图一起删。

**先例：** 3.4.0 timeline 懒建不升 schema；3.17 `_wp-chart.md` 写入 VERSION_CAPABILITIES.new_files 但 schema 不变；3.10–3.20 连续 Minor 保持 0.14/0.16。

---

# 兼容合同（本方案核心，跳版本只认这一节）

## C0. 一条协议，终身不加第二套

以后改百科，只允许：修脚本、加投影列的派生、收紧 AUTO 兜底。禁止：再起 `facts/` 树、再起第二套 ID、再起「v4 journal 才是真入口」的平行语义。

## C1. 三层与路径（3.21 一次写死）

| 层 | 路径 | 谁写 | 缺了怎么办 |
|---|---|---|---|
| 证据 | 已有 `meetings/`、todos §2、`sources/`；新投喂 `logs/journal/J-*.md` | 只追加 | 无 journal 则证据仍在日报/纪要，功能降级不阻断 |
| 事实 | `wps/` `todos/` `requirements/` `risks/` `issues/` `decisions/` `context/domain-glossary.md` | 确认后写；纠偏视为已确认 | 与 3.20 相同，跳版本零搬家 |
| 派生 | `context/brain.md`、`context/active-entities.json`、`ai/.state.json`、`wps/_index.md`、`wps/_wp-chart.md`、PLAN §3§4 投影列、当日 `_index` 可派生格 | **脚本覆盖**；无 Python 则 AUTO | 缺文件不致命；会话或写后生成 |

口径家永远是词库 §2，不是 JSON。JSON 只有派生 `aliases` 与只读 `term_corrections`。用户发起的纠偏才视为已确认。

## C2. 能力探测（禁止用 Skill 版本号当 if）

规则与脚本只问（名称与 `.state.json` 同文，B2-4）：

0. **无 `ai/.state.json`**（B3-4）：视为全部视图 stale，**禁止**假装有指纹。走 05 第 2 条（读事实原文 + 声明 as-of）。有 Python 则可先 P-VIEWS 懒建再问第 1 条。
1. 能否执行包内 `scripts/refresh_views.py`？
2. **查询准入**只比 `.state.json` 的 **`facts_fingerprint`** 与当前 facts glob 聚合哈希（WP 进度问句不因新 journal 作废 brain）。
3. `views.brain.status == ok` 且 `active-entities.json` 存在？过期则重建，不把 stale 当真理。

**与 §7 的不对称（B4-3，写死避免施工误把查询当重建）：** P-VIEWS / `--all` **写盘**条件 = `facts_fingerprint` **或** `journal_fingerprint` 任一变化。新投喂只改 journal 时：查询仍可用旧 brain 答进度，但本轮若走入库必须先重建（活表/别名可能变）。禁止把 C2 第 2 条理解成「journal 变了查询也必须重跑」。

禁止：`if skillVersion >= 3.22` 才重建图；禁止：`if 工作区经历过 3.21` 才允许 journal。

## C3. 跳版本矩阵

| 从 → 到 | 工作区发生什么 | PM 要做什么 |
|---|---|---|
| 3.20 schema 0.16.0 → 3.21 同 schema | 换 Skill 包。首次会话脚本懒建派生文件。事实 md 不动 | 无。不跑迁存量 |
| 3.18 schema 0.16.0 → 3.21 | 同上。3.19/3.20 的规则增量随新包生效，不要求先装 3.19 | 无结构迁移 |
| 3.14 schema 0.15.0 → 3.21 | **先走已有** 0.15→0.16（project-info / current_operator），再叠层懒建。百科不另加 0.17 | 仅确认已有 schema 迁移（本来就要） |
| 更旧且缺 wps/ | 已有 3.5 抽取门禁，与百科无关 | 旧债，不绑进百科 |
| 3.21 工作区 + 3.20 Skill（反向） | 20 号只读降级。多出来的 brain/json/journal **当普通文件忽略**，低版本不得删 | 提示升级 Skill |
| 无 Python 的 3.21 | 不建/不刷新派生；问答读事实原文；写入走 AUTO 视图 | 无 |
| 有派生文件但事实已改、脚本没跑 | as_of/指纹不一致 → 回答声明可能过期并打开事实文件 | 无 |

## C4. migrate 义务（防跳版本踩空）

`VERSION_CAPABILITIES` 增加 **一条** 3.21.0：

```
schema: 0.16.0
capabilities: ["encyclopedia_overlay"]
new_dirs: []
new_files: []    # 懒建，禁止 migrate 预建并当缺失失败
note: 完整百科叠层；缺 brain/journal 不致命
```

`get_capabilities_since("3.18.0")` 会包含 3.19、3.20、3.21 三档能力名，但 **3.21 档不得带必须落地的 new_dirs**。跳版本健康检查：缺 brain ≠ 缺失能力表里的 P0。

20 号增加一行 **3.21.0+**：与 3.4.0 timeline 同句式——不要把缺 `context/brain.md` / `logs/journal/` 当健康失败。

## C5. 双轨同一语义（物理载体，V0.3 闭合）

派生列与指纹 **只有一份机器可读定义**：`ChronoPM-Project/scripts/view-spec.json`。

| 键 | 内容 | 与现模板对齐 |
|---|---|---|
| `wp_index_columns` | 12 列 | `wp-index-template.md` 表头 |
| `wp_chart_fingerprint` | 编号、名称、plan_ref、开始日、结束日、当前阶段名、upstream、downstream、effect | 今 11 §17.3 |
| `plan_s3_columns` | 6 列 | `plan-template.md` §3 |
| `plan_s4_format` | 阶段列表行格式 | 同模板 §4 |
| `brain_fact_globs` | 进入 facts 指纹的路径模式 | 与本节 `.state.facts` glob 同文 |

约束：

1. `refresh_views.py` **只读**该 JSON 写列，禁止在 py 里另写一份列名常量。
2. 无 Python 走 AUTO 时，规则写「列与指纹以 `view-spec.json` 为准」，**11 §17.3 / 00 §8c 删除复述表，改指针**。
3. 启动先 `--check-spec`（B2-1）：`wp-index-template.md` 表头 == `wp_index_columns`；`plan-template.md` §3 表头 == `plan_s3_columns`；不一致 **exit 2 不写盘**。chart 指纹无模板表头，只认 JSON（11 号指针）。
4. 改列：先改模板表头与 `view-spec.json` 两处（`--check-spec` 卡住漏改）；禁止只改 11 号正文。
5. 回归 SPEC-001：脚本产出表头 == view-spec **且** view-spec == 对应模板表头。

运行时：

| 运行时 | 谁写派生 | 谁禁止 |
|---|---|---|
| 主轨：Python | `refresh_views.py --all` 读 view-spec | 手改派生文件 |
| 兜底：无 Python | AUTO，同样读 view-spec（模型打开 JSON） | 把投影列当事实；只改 brain 当纠偏 |

以后删 AUTO 只改规则一句，工作区不迁。

## C6. 旧文件即证据，不回迁

跳到 3.21 的库：历史 todos/纪要/sources 保持原位当证据。journal 只收 **新**投喂。禁止 migrate 把 1225 份待办改写成 J-0001。

---

# AP-4. 修改范围

| 文件 | 类型 | 摘要 | 契约 |
|---|---|---|---|
| 本 AP | 本文件 | V0.6 | 否 |
| `scripts/view-spec.json` | new_file | 投影列与指纹唯一事实源 | 否 |
| `scripts/refresh_views.py` | new_file | 读 view-spec；原子 replace；分视图 status | 否 |
| `assets/templates/journal-entry-template.md` | new_file | J- 头 | 否 |
| `tests/fixtures/qlt-wp-20260827-001-fp.md` | new_file | 全链通注销总包 §3 功能点摘录（只读 fixture） | 否 |
| `SKILL.md` | edit_section | §3 懒建名单；§5.1b P-VIEWS；§7 铁律；跳版本不致命 | 否 |
| `00` | edit_section | 视图=脚本优先 AUTO 兜底；P-CORRECT；WF-8 先活表；**8a 实体级联保留** | 否 |
| `05` | edit_section | 先 brain；L0–L3；证据指针；横幅不报结构债 | 否 |
| `10` | edit_section | 日报默认更新；禁进展建 WP；纠偏信号 | 否 |
| `23` | edit_section | P-VIEWS / P-INGEST-DELTA / P-CORRECT | 否 |
| `06` | edit_section | 懒建路径；派生可覆盖 | 否 |
| `11` §17.3 | edit_section | 指纹改为指针指向 view-spec；有脚本 CALL --chart；无则 AUTO 仍读 JSON | 否 |
| `17` | edit_section | 口径→纠错表；禁写 JSON | 否 |
| `20` / `_version.py` 注释 | edit_section | 3.21+ 缺 brain 不致命；判别式：必填/迁移义务才升 schema，懒建派生不升 | 否 |
| `14` | edit_section | 写后指纹检测 | 否 |
| `migrate_workspace.py` VERSION_CAPABILITIES | edit_section | 3.21 一条，空 dirs | 否 |
| `_version.py` 等版本触点 | edit_section | 3.21.0 / schema 0.16.0 | 否 |
| BLUEPRINT | edit_section | AD-10 完整协议 + 修订 AD-05 | 文档层 |
| 回归 Module 75 | edit_section | 含跳版本/无 Python/反向 Skill | 否 |
| Portfolio | 版本触点 | 无 V-x | 否 |
| 市监 | 只读 | 禁止 | — |

禁止：新 NN 规则；改 WP 模板列；改八块；改 skill-contract 正文；git；`--migrate-business` 默默改市监。

`verify_projection.py` 保持只读校验；`refresh_views.py` 负责写投影。写后仍可跑 verify。

---

# AP-5. 回归（基线 777 → 施工只认 **807** = 777+30）

Module 75 固定这 30 个新 ID（B1-4）。旧 QQ-010 / WPS-014 仍跑，不计入 +30。

| ID | 预期 |
|---|---|
| SKIP-001 | 工作区 3.18.0 + schema 0.16.0 + Skill 3.21：不要求先装 3.19；不升 schema；首次 P-VIEWS 懒建 |
| SKIP-002 | 缺 brain/journal：健康检查不列 P0 |
| SKIP-003 | 3.21 工作区 + 3.20 Skill：只读降级，不删派生文件 |
| SKIP-004 | get_capabilities_since(3.20.0) 含 encyclopedia_overlay 且 new_dirs=[] |
| DUAL-001 | 有 Python：写 WP 后 index/图/brain 由脚本更新 |
| DUAL-002 | 无 Python：AUTO 读 view-spec 更新图/index；查询声明无快照 |
| DUAL-003 | 单视图写失败：该视图 failed，已 replace 的其它视图保留 ok，不出现截断半文件 |
| DUAL-004 | `--all` 中途 chart 失败：index 若已 ok 则保留；chart stale；brain 未跑标 stale |
| SPEC-001 | ① 脚本产出 index 表头 == view-spec.wp_index_columns 且 == `wp-index-template` 表头；② plan §3 同理；③ chart 指纹键 == wp_chart_fingerprint。`--check-spec` 人为改乱表头必须 fail |
| BRN-001 | 有 Python 进工作区：指纹变才写 brain |
| BRN-002 | 指纹未变：不重写 |
| BRN-003 | 「注销国庆包现在怎样」：先 brain；L0+指针；不载 00 |
| BRN-004 | 无 Python / 脚本失败：读 WP 原文；声明可能过期 |
| BRN-005 | 无 brain 文件：退回 3.20 定向读，不致命 |
| ALI-001 | 「农专注销 90%」：term 两跳 + 「注销」收口 → `WP-20260827-001`（§3 功能点「农民专业合作社」）。fixture：`tests/fixtures/qlt-wp-20260827-001-fp.md`（摘自全链通该 WP §3，含农民专业合作社行）。施工必检：只读打开市监 `全链通重构/ai/wps/WP-20260827-001.md` 核对 fixture 未过期，**禁止写市监**（B4-4） |
| ALI-002 | 废弃 WP-001：跳总包，不在废弃包建 TD |
| ALI-003 | 对不上活实体：问，不建 WP/TD |
| UPD-001 | 日报进度句：更新已有 TD，不建 WP |
| UPD-002 | 未点名新模块：禁止建 WP |
| COR-001 | 用户说 WP-073 不是开发是联调：写 WP 留痕 + journal correction + 重建；不进八块 |
| COR-002 | 「联调完成≠开发完成」：写词库 §2；JSON 仅投影 |
| COR-003 | 只改 brain：禁止 |
| COR-004 | 写入 active-entities.corrections：无此槽，失败 |
| COR-005 | AI 自检发现 80% vs 95%：进 pm-decisions，**不**当已确认 |
| DEP-001 | 「现在怎样」→ L0/L1 |
| DEP-002 | 「展开/为什么」→ L2 |
| DEP-003 | 「列出来/周报/对比」→ L3 |
| JRN-001 | 粘贴入库：追加 J-，不改历史 J |
| JRN-002 | 无 journal 目录：懒建 logs/journal |
| SCH-001 | 升级后 schema 仍 0.16.0；skillVersion 3.21.0；Portfolio 行为不变 |

阻断：SKIP-002、DUAL-003、SPEC-001、ALI-003、UPD-002、COR-001、COR-004、COR-005、SCH-001、BRN-003。

---

# AP-6. 风险与回滚

| 风险 | 缓解 | 回滚 |
|---|---|---|
| 脚本覆盖手改过的 index 空列 | 只覆盖派生列；存在性以 WP 文件为准；PLAN 只写 §3§4 投影，不动叙事节 | 停用脚本，AUTO 兜底仍在 |
| PLAN 投影写错 | 先 verify 再写；失败不写盘 | 同 |
| 跳版本用户以为要迁 3700 文件 | 20 号明文：规则升级无需迁移；健康检查不把缺 brain 当 P0 | — |
| 双轨两套结果 | view-spec 唯一载体 + `--check-spec` 卡住模板漂移 | — |
| 无 Python 长期不重建 brain | 每次查询打开事实文件+as-of；不装假新鲜 | — |

回滚 Skill 到 `baselines/3.20.0/`。派生文件可留可删。事实 md 不自动回滚。

---

# AP-7. 版本影响

| 维度 | 后 |
|---|---|
| Skill | **3.21.0** |
| Schema | **0.16.0 不变** |
| 工作区迁移 | **否**（跳到 3.21 若旧 schema<0.16.0，只走 **已有** schema 链，百科不增环节） |
| 核心契约正文 | 不改 |
| Blueprint | full（AD-10） |
| 双包 | 同号，Portfolio 无行为 |

---

# 5. 字段清单（完整协议，以后不加平行字段）

## journal `logs/journal/J-YYYYMMDD-NNN.md`

`id` `at` `kind: daily|meeting|chat|file|oral|correction` `who` `source` + 原文。只追加。

## brain.md

头：`doc_type: brain` `as_of` **`facts_fingerprint`**（与 `.state.facts_fingerprint` 同值）`generated_by: refresh_views.py`。

节（仅这些）：活 WP、未办结 TD、开放 R/I、别名跳转、近 7 日证据指针。硬顶 50KB。

**禁止「待拍板 / 等你裁定」节**（B3-1）。`pm-decisions.md` 是实时确认面，不进 facts 指纹，派生层不准复制。横幅只走 05 §1a 当场读该文件。脚本若写出待拍板节 = 失败。

## active-entities.json

`as_of` **`facts_fingerprint`**（同 `.state`）`generated_by`

`entities[]` **必须覆盖四类**（B1-1）：

| type | 收录 | 源（禁止派生读派生） |
|---|---|---|
| `wp` | YAML `effect!=废弃` 且头 `status`∈{待确认,已规划,进行中,已完成} 的活文件；`effect=废弃` 只进 alias 跳转 | **只读** `wps/WP-*.md` frontmatter + 标题 + §3 功能点表。**禁止**用 `_index` §1 当收录判据（B4-1） |
| `td` | **未办结**（待处理/进行中/已阻塞；含待确认终态） | 最新合法日 `todos/{date}/{owner}.md` 核心表（事实文件，不是 `_index` 派生格） |
| `risk` / `issue` | 开放或监控中 | 登记册正文 |
| `person` | 在册 | 最新合法日 `_index.md` §1（3.8 起花名册事实源，不是 WP index） |

每条：`id` `type` `name` `status` `path` `aliases`（派生，**WP 必须纳入**：包名、废弃旧名、`supersedes` 旧编号、**§3 功能点名**）`owner`（TD/人）`supersedes`（仅 WP）。

`alias_index` 派生。`term_corrections[]` 只读投影自词库 §2。**无 corrections 可写槽。**

**`alias_index` 聚合源（B2-2，脚本必须全扫这些，禁止猜）：**

| 源 | glob / 位置 | 写入 alias_index 的键 → 值 |
|---|---|---|
| 词库 §1 confirmed | `context/domain-glossary.md` 术语映射表 | 原词 → `{id: Gxxx, type: term, canonical: 标准词}` |
| 词库 §2 纠错 | 同文件纠错映射表 | 错误写法 → `{id: Gxxx 或 canonical, type: term}` |
| WP 名称 | `wps/WP-*.md` 标题与 YAML，**不读** `_index` 名称列 | 名称 → `{id: WP-…, type: wp}` |
| WP §3 功能点 | 同文件「实体或功能点」列（全链通注销总包含「农民专业合作社」） | 功能点名 → `{id: WP-…, type: wp}` |
| 废弃 WP / supersedes | WP YAML `supersedes` / `superseded_by` | 旧编号与旧名称 → 现总包 |
| 花名册 | 最新合法日 `todos/{date}/_index.md` §1 | 姓名 → `{id: 姓名, type: person}` |
| TD 缩写 | 同文件 §6 | 缩写 → `{id: 姓名, type: person}` |

ALI-001「农专」只允许命中词库 §1 confirmed，不得靠语义近似。

### P-RESOLVE（B3-2 + B4-2，禁止跳过 term 直接猜 WP）

WF-8 / P-INGEST-DELTA 对齐时必须走本链。

**同表面词命中多条 alias 时的类型优先级（B4-2）：**

1. 精确编号（`WP-` / `TD-` / `G-` / `R-` / `I-`）
2. `type=wp` 或 `type=td`（业务对象优先于人、优先于纯术语）
3. `type=term` → 必须第二跳到 WP，停在 term 不算对齐完成
4. `type=person` **仅当**原文在指人（谁/花名册/他/她/「我的待办」+ current_operator）。「农专注销」即使缩写碰巧撞人名，也不走 person

**term 第二跳：**

1. 取 `canonical`（农专 → 农民专业合作社）。
2. 在 `entities[type=wp]` 找 `name` 或 `aliases` 含 canonical 的包。`aliases` 必须已含 §3 功能点名与废弃旧名（全链通 `WP-20260827-001` §3 有「农民专业合作社」，包名本身没有）。
3. **>1 条时先用原文其余词收口**（开办 / 变更 / 注销 / 国庆 / 国庆后）。「农专注销」应落到注销国庆总包，不得停在「问用户选开办还是注销」之前不做过滤。
4. 收口后 0 条 → 问，不建。
5. 收口后 1 条 → 该 WP。
6. 收口后仍 >1 → WF-8 归属④，问一次。
7. alias_index 未命中 → 问，禁止全库语义扫。

WF-8 查重：P-RESOLVE 得到 WP/TD 后，只在该人未办结 `type=td` 查同 WP+主题。

## .state.json

命名统一（B2-4）：聚合哈希叫 `facts_fingerprint` / `journal_fingerprint`；每视图叫 `view_fingerprint`。禁止再用无前缀的 `fingerprint` 或只写 `facts` 当探测字段。

```json
{
  "facts_fingerprint": "<sha256 over canonical facts map>",
  "journal_fingerprint": "<sha256 over journal map>",
  "facts": {
    "wps/WP-073.md": "<hash>"
  },
  "journal": {
    "logs/journal/J-20260830-001.md": "<hash>"
  },
  "views": {
    "brain": {"as_of": "", "view_fingerprint": "", "status": "ok|stale|failed"},
    "active_entities": {},
    "wp_index": {},
    "wp_chart": {},
    "plan_proj": {}
  }
}
```

**`facts` 覆盖 glob（B2-3）。相对 `ai/`。最新合法日 = 22 号原文：`date≤今天` 且存在 `_index.md` 的最大日期（B3-3）。非法未来日不参与。**

| glob | 说明 |
|---|---|
| `wps/WP-*.md` | 全部 WP 文件（含废弃，供 supersedes） |
| `todos/{最新合法日}/*.md` | 当日个人待办 + 当日 `_index.md` |
| `risks/risk-register.md` | 若存在 |
| `issues/issue-register.md` | 若存在 |
| `decisions/decision-log.md` | 若存在 |
| `requirements/requirement-register.md` | 若存在 |
| `requirements/_index.md` | 若存在 |
| `context/domain-glossary.md` | 词库 |
| `plans/PLAN-*.md` | 仅 `status` 正常或未标废弃的计划 |

不含：`outputs/`、`logs/ops/`、`backup/`、`archive/`、共享盘、`pm-decisions.md`（确认面不是进度事实）。journal 不进 `facts`，只进 `journal` 段。

查询只信任 `views.*.status == ok`。探测用 `facts_fingerprint` 比较，不用扫 `facts` 对象本身来口头命名。

## 其它派生

`_index` / `_wp-chart` / PLAN §3§4：列与指纹 **只认 `view-spec.json`**，与模板表头对齐，不在 00/11 再抄一份。

---

# 6. 00 / 05 / 10 / 23 / 11 最小规则（完整语义）

### 00

1. 进工作区：版本检查 → **P-VIEWS**（能跑则跑，指纹未变不写）。
2. 写事实成功后同回合 P-VIEWS。无 Python → 走现有 §8c / P-WP-CHART AUTO。
3. WF-8 查重：先 **P-RESOLVE** 两跳，再只在该人未办结 `type=td` 查同 WP；禁止全库扫。
4. P-CORRECT：**仅用户发起的纠正**（「不对」「你说错了」「纠正」）视为已确认，写 WP/TD/风险留痕或词库 §2，不进八块。**AI 自检发现的冲突/歧义**仍登记 `pm-decisions` 待确认，禁止当已确认写入。禁止只改派生。
5. §8a **实体**级联保留。视图相关 AUTO 改为「脚本失败才 AUTO」。
6. 禁止对 PM 朗读 AUTO/CHECK。

### 05

1. 有 brain 且 **`facts_fingerprint` 一致**且 `views.brain.status=ok`：先读 brain，再最多 1～3 个事实文件。新 journal 单独不使进度问答失效（C2/B4-3）。**仍须按 §1a 实时读 pm-decisions 做横幅，不读 brain 待拍板（该节已禁止存在）。**
2. 无 brain / 无 `.state.json` / 指纹不一致 / 无脚本 / 视图 stale：读事实原文并声明 as-of。禁止在缺 `.state` 时当作指纹一致。
3. L0 默认；展开/为什么 → L2；列出来/对比/周报/巡检 → L3。与现有待办展开词合并，本节 ≤40 行。
4. 证据指针；冲突亮出。简单查询不载 00。
5. 横幅只报业务待裁定，**只实时读 `pm-decisions.md`**，禁止从 brain 抄待拍板。

### 10

1. 日报/口播默认更新活实体。
2. 禁止从一句进展建 WP/REQ。
3. 对不上就问。
4. 「不对/纠正」→ P-CORRECT。
5. 不新增长触发词表。

### 23

| ProcID | 作用 | Forbidden |
|---|---|---|
| P-VIEWS | CALL `refresh_views.py`（或无 Python 时 AUTO 等价物） | 手改派生；查询现场写临时脚本 |
| P-INGEST-DELTA | 追加 journal + **P-RESOLVE** 活表对齐 | 改历史 J；全库扫；跳过 term 直接猜 WP |
| P-CORRECT | 纠偏闭环 + P-VIEWS | JSON/brain 当家；八块 |

### 11 §17.3 / 00 §8c

删除复述的指纹字段表与投影列清单，改为：「以 `scripts/view-spec.json` 为准」。有脚本 CALL `--chart`/`--plan`；无 Python 则 AUTO，模型必须先打开该 JSON。SPEC-001 卡住漂移。

---

# 7. `refresh_views.py` 行为（完整生成器 + 原子写）

```
python scripts/refresh_views.py --project-root <根> [--all|--brain|--index|--chart|--plan]
```

- 列与指纹只读 `view-spec.json`。启动先 `--check-spec`（可并入 `--all` 第一步），失败 exit 2。
- 默认会话：`--all`。`facts_fingerprint` **与** `journal_fingerprint` **都**未变才 exit 0 不写盘（B4-3：重建看两枚指纹；查询准入只看 facts，见 C2）。
- `--all` 顺序：先 **parse 全部 `wps/WP-*.md`** 到内存 → 写 `_index` → chart → plan → `active-entities` / brain / `.state`。json 与 index 共用同一次 WP 解析，禁止 json 再去读刚写出的 `_index`（B4-1）。
- **原子写（B1 条件 2）**：每个目标文件先写同目录 `.{name}.tmp`，成功后再 `os.replace` 到正式路径（单文件替换在同卷上是原子的）。禁止先截断正式文件再写。
- **分视图提交**：`--all` 按 index → chart → plan → brain/json 顺序；某一视图失败则该视图 `status=failed`，**已成功替换的视图保留**，未开始的标 `stale`。exit 非 0。查询不把 failed/stale 当真理。这不是「半个 index 文件」，是「整文件要么新要么旧」。
- 解析失败的行/段：标记 skip+日志，**禁止猜值写入**。写盘前对 PLAN 调用现有 `verify_projection.py`，失败则该视图不 replace。
- `--plan` 只改 §3§4 投影，不动 §1§2§5§6。
- `--index` 存在性以 WP 文件为准。
- 不扫描共享盘、`backup/`、`archive/`。

不是契约 #4 的临时脚本。

---

# 8. 用户交互（无新套话）

问「现在怎样」→ L0+指针。扔日报 → 更新活实体 + 回执。说「你说错了」→ 当场改事实 + 重建派生 + 旧 vs 新。跳版本换包后第一次对话：不提问「是否按 3.21 迁移」，直接 P-VIEWS 懒建。

---

# 12.5 影响与必要性

跳版本约束使「完整协议进 3.21」成为必须，而不是膨胀。成本是多一个写视图的脚本、00 视图 AUTO 改优先顺序。收益：3.20→3.25 不必再消化半套架构。

必要性：**必须升级（收敛后的完整协议）**。不升级则失忆/错建/纠偏不持久；切成 3.22 则跳版本仍踩大步。

体验：增强（更短、更可纠）。削弱：无 Python 时多一句可能过期——可接受。

---

# 12.6 关键断言

| 断言 | 证伪则 |
|---|---|
| schema 仍 0.16.0，百科不新增 schema 台阶 | 阻塞 |
| 3.21 含全部派生生成器，不把图/index/PLAN 投影留给「下个版本才有的架构」 | 阻塞 |
| 缺 brain/journal 不致命；migrate new_dirs 为空 | 阻塞 |
| 规则用能力探测，不用 `skillVersion>=3.22` | 阻塞 |
| 口径家=词库 §2；JSON 无写 corrections | 阻塞 |
| 8a 实体级联仍在；只把视图 AUTO 降为兜底 | 阻塞 |
| refresh_views.py 非临时脚本 | 阻塞 |
| 市监零写 | 阻塞 |
| 简单查询不载 00 | 阻塞 |
| 反向：低版本 Skill 不删高版本派生文件 | 阻塞 |
| 双轨同一语义以 `view-spec.json` 为唯一载体；00/11 不复述列 | 阻塞 |
| 每视图原子 replace；失败不留半文件；分视图 status | 阻塞 |
| entities[] 含未办结 TD；WF-8 只查本表 | 阻塞 |
| `.state.journal` 独立段；增量不扫全量 todos | 阻塞 |
| 仅用户发起的纠偏视为已确认；AI 自检仍进 pm-decisions | 阻塞 |
| 20 号写死：必填/迁移义务才升 schema，懒建派生不升 | 阻塞 |

| 取舍 | 阻塞 |
|---|---|
| 无 git | 否 |
| 无 Python 时 AUTO 兜底长期存在 | 否（这是兼容，不是债） |
| 结构债不进每日横幅 | 否 |
| 历史 todos 不回迁 journal | 否 |

**不再把「视图脚本化」列为 3.22 遗留。** 3.22+ 允许的只剩：改善脚本精度、在 AUTO 已无用户依赖时删除兜底条文。

---

# 15. 偏差验证

| 需求点 | V0.3 | 覆盖 |
|---|---|---|
| 时效/纠偏/深度/口径 | 同 V0.1 闭环 | 是 |
| 按 A 收敛 | 是 | 是 |
| 跳版本不大步 | 完整协议+懒建+双轨+不升 schema | 是 |
| 不按版本切架构 | 取消 3.22 架构债 | 是 |
| JSON 可写 corrections | 仍不做 | 有意 |
| 全优化/清空 8a | 仍不做 | 有意 |

忠实：**部分是**（执行用户第二轮调整；仍拒绝 JSON 当家与清空实体级联）。

---

# 16. 复杂度

| 指标 | 前 | 本版 | 后 | 超？ |
|---|---|---|---|---|
| 规则文件 | 23 | 0 | 23 | 否 |
| 脚本 py | 15 | +1 | 16 | 否 |
| view-spec.json | 0 | +1 | 1 | 否 |
| 模板 | 36 | +1 | 37 | 否 |
| 回归 | 777 | +30 | 807 | 否 |
| 05 L0–L3 | — | ≤40 行 | — | 精神预算 |

补偿：视图手养规则改为「CALL 脚本」，00 视图段应净减字数，禁止又抄一遍列定义。

---

# 18. 联动（底层→上层）

1. 事实文件（WP/TD/词库）  
2. `refresh_views.py`：index → chart → PLAN 投影 → brain/json/.state  
3. 对外回答只读 brain + 必要时事实原文  

禁止先改 brain。失败不写一半派生。

---

# 19. 待确认（V0.2 仅剩非阻塞默认）

用户已裁技术收敛 + 完整兼容。下列 **默认采用**，B 可反对：

| 默认 | 内容 |
|---|---|
| D1 | 单一脚本 `refresh_views.py`，不拆成 brain/index 两个入口 |
| D2 | PLAN 脚本只写 §3§4 投影 |
| D3 | Portfolio 仅同号 |
| D4 | 无 Python 降级不阻断 |

无新的用户阻塞题。若你反对 D1–D4，回一句即可。

---

# 20. A 自审

| 项 | V0.6 |
|---|---|
| B4-1 | wp 只读 WP 文件，不读 _index |
| B4-2 | alias 多命中类型序 + 开办/注销收口 |
| B4-3 | 查询比 facts；重建比 facts 或 journal |
| B4-4 | fixture + 市监只读抽查 |
| 适合施工 | **待用户授权**。B4 已可施工，V0.6 只收低优先 |

---

# 21. 当前结论

V0.6 消化 B4。仍 **不可自行执行**。你点头后再按 AP-4 改 Skill（市监只读验证 ALI-001，不写回）。

---

# 给 B 的审核输入包

你现在是 Skill 升级独立审核 Agent，代号 B。

注意：自行扫仓；A 方案不是事实；不执行改造；先与用户确认工作空间；独立辩论需求；四档结语。

【用户原始需求】见 #1.a 与 #1.b。

【A 的需求理解】完整百科协议一次进 3.21；激活靠探测；跳版本不新增 schema 台阶；技术收敛（无 git、JSON 非口径家、8a 实体级联保留）。

【A 的需求辩论结论】第一轮建议调整后实施。用户已裁决：按 A 收敛，且否决按版本切架构。辩论已终止。B 仍须独立辩论第二轮约束是否合理。

【A 已扫描文件摘要】Skill 3.20.0 / schema 0.16.0 / HEAD c2b6831 / 回归 777 / migrate VERSION_CAPABILITIES 至 3.20 且 3.10–3.20 多档 schema 不变 / 20 号 3.4.0 懒建不致命先例。

【A 工作空间版本快照】

| 项目 | 值 |
|---|---|
| 工作空间根路径 | C:\Users\qiusuo\Downloads\ChronoPM Skill |
| 版本标识值 | 3.20.0 / schema 0.16.0 / c2b6831 |
| 快照生成时间 | 2026-08-30 |
| 本轮仅有 | governance-shared/planning/upgrade-plan-v3.21.0.md（V0.4） |

【A 升级方案】本文件 **V0.4**。B2 四处已写入：`--check-spec`/SPEC-001 含模板表头、alias 六源、facts glob、指纹三名。请核这四处是否仍口头。历史 B1/B2 章节勿当当前正文。

请重点证伪：① 完整视图生成器进 3.21 是否仍属 Minor+schema 不变；② 双轨是否会造成两套投影语义；③ migrate 空 new_dirs 是否真能让 3.18→3.21 跳版本不踩 P0；④ 是否又把大步藏进「一个脚本里」而无法落地。

---

# B1 审核结果

> 治理约定：本文件的 B 审核意见**一律只写在本章节**，不得改动方案正文其他部分。后续轮次在本节追加"第 N 轮"子段或就地更新，A 修订须同步在 #0 标注"相对上版改了什么"以便 B 复核。
> 审核轮次：B1 第一轮，对象 V0.2。审核方法：独立扫仓（A 方案不是事实），版本/断言全量实测核验，未执行任何改造，未写市监。

## 0. 版本与事实核验（眼见为实）

| 项 | A 声称 | 实测 | 结论 |
|---|---|---|---|
| Skill 版本 | 3.20.0 | `ChronoPM-Project/VERSION`=3.20.0、`_version.py SKILL_VERSION`=3.20.0 | ✅ |
| Schema | 0.16.0 | `_version.py WORKSPACE_SCHEMA_VERSION`=0.16.0（注释 0.16.0=pm-profile current_operator） | ✅ |
| git HEAD | c2b6831 | `git log -1`=c2b6831「docs: add GitHub and Gitee repo links in README」；工作区仅本 AP 未跟踪 | ✅ |
| 规则文件 | 23 | `references/*.md`=23 | ✅ |
| 脚本 | 15→16 | `scripts/*.py`（含 chronopm_init 包）=15，+refresh_views=16 | ✅ |
| 模板 | 36→37 | `assets/templates/*.md`=36 | ✅ |
| 回归基线 | 777 | 统计表合计 777（正向 461+回归 316），模块 1~74 | ✅ |
| 3.18/3.19/3.20 migrate 档 | schema 0.16.0 且 new_dirs 空 | 实测三档 `new_dirs:[] new_files:[]`，仅 capabilities 名称不同 | ✅ |
| get_capabilities_since | 从指定版本后累加 | 实现：found 后 append 其后所有档 | ✅ |

## 1. 对 A 四个重点证伪的结论

### ① 完整视图生成器进 3.21 是否仍属 Minor+schema 不变 —— **未被证伪，可行，但需补一条显式边界**

- 成立依据（实测）：3.18/3.19/3.20 三档 migrate 均为空 `new_dirs`，且 3.17 `_wp-chart` 也是"新增文件但不升 schema"先例；20 号已有 3.4.0 timeline 懒建不致命先例（实测 line 88）。
- **未明确点**：方案靠"懒建、缺了不致命、migrate 不承载"来论证"不加 schema 台阶"，但没有把"什么算 schema 变更"的边界规则写死。历史 schema 注释里 0.10=新增 wps/、0.14=新增 pm-decisions 都是"新增目录/文件即升 schema"，本次却允许新增 `logs/journal/`、`context/brain.md`、`context/active-entities.json`、`ai/.state.json` 而不升——依据是"可选/派生/懒建"。这条边界若不固化，下一次升级会滥用"懒建"规避 schema。**建议**：在 `_version.py` schema 注释或 20 号补一句判别式："新增必填目录/必填文件/迁移义务 → 升 schema；新增懒建可选派生物（缺了能降级运行、不参与迁移校验）→ 不升。"（非阻塞，施工作业补即可）

### ② 双轨是否会造成两套投影语义 —— **部分成立，但"一处定义"的机制缺口未闭合（修订项）**

- 方案 C5 断言"指纹字段集合与 11 §17.3 / index 列定义**同一份**（一处定义，脚本与 AUTO 都引用）"——这是防漂移的唯一防线，但**只是断言，没有设计"这一处"是什么**：
  - Python 脚本不可能"引用 00/11 原文"，它必须在代码里写死列名/指纹字段；
  - 规则文件（00/11）里是另一份文本化定义；
  - 两处没有任何机器可读的共享载体，`DUAL-001`（脚本更新视图）与现有 AUTO 路径天然会各写各的。
- **判定**：关键断言"不会两套语义"**当前未被机制支撑**，属修订项，不是重做。**最小补齐**：给"一处定义"指定物理载体，例如 `refresh_views.py` 直接读取 `wp-template.md`/`_index` 模板的表头作为列定义源（模板即定义），或新增一个 `scripts/view-columns.json` 由脚本与 11 §17.3 共同引用；并加一条回归：脚本生成列名集合 == 模板表头集合。

### ③ migrate 空 new_dirs 是否真能让 3.18→3.21 跳版本不踩 P0 —— **未被证伪，成立**

- 实测：3.18/3.19/3.20 三档 migrate 的 `new_dirs:[] new_files:[]`；`get_capabilities_since("3.18.0")` 返回 3.19+3.20+3.21 三档，`check_missing_dirs/files` 仅按 `new_dirs/new_files` 检查，全部为空 → 不会产生缺失 P0。3.21 档 `capabilities` 里多一个 `encyclopedia_overlay` 名称，但检查逻辑只看 new_dirs，不看能力名，不触发缺失。✅ 断言成立，`SKIP-001/004` 可行。

### ④ 是否又把大步藏进"一个脚本里"而无法落地 —— **方向可落地，但两个落地机制缺口（修订项）**

- 单入口 `refresh_views.py --all` 承担 brain+json+.state+index+chart+PLAN 六类生成，**可行**（已有 11 §17.3 / 00 §8c 的 AUTO 语义可移植成脚本），不是"藏大步"。
- **缺口 A（原子性）**：方案反复说"失败不写一半 / 不留半更新"，但没设计原子机制。多文件生成若写一半失败，`.state.json` 指纹如何标记哪些视图已新哪些已旧？**建议**：先写临时文件再统一替换，或每类视图单独原子提交并在 `.state.json` 记 per-view 指纹，查询侧据 as_of 声明陈旧。
- **缺口 B（解析健壮性）**：脚本要解析 WP frontmatter + §3b/§3 表格、`todos/{date}/{owner}.md` 多节、登记册/词库，纯 md 表格解析易碎。**建议**：规定"解析失败的行/段标记 stale 或跳过并记录，禁止猜测补值"，与 `verify_projection.py` 只读校验衔接（写前先 verify、失败不写盘）。

## 2. 新增发现（A 未覆盖，施工前须明确）

| # | 发现 | 级别 | 建议 |
|---|---|---|---|
| B1-1 | **active-entities.json 是否含"未办结 TD"未定义**：00 改"WF-8 先活表"，但 §5 字段清单 entities[] 未说明是否收录 todos 级实体。若 WF-8 查活表却无 TD，对齐退回语义扫描，方案核心收益落空 | 修订 | 字段清单补一句：entities[] 覆盖 WP + 未办结 TD + 开放 R/I + 在册人员；未办结 TD 从最新合法日 todos 聚合 |
| B1-2 | **journal 是否进 .state.json 指纹未定义**：P-INGEST-DELTA 靠"上次会话后新出现的 journal"触发，但 §5 .state.json 范围写的是"事实层"，未含 journal。若 journal 不进指纹，"新投喂检测"又退回扫目录 | 修订 | .state.json 范围补 `logs/journal/` 子目录指纹（journal 属证据层，单独指纹段） |
| B1-3 | **P-CORRECT 视为已确认的边界未定义**：用户主动"纠正"= 权威人工输入，视为已确认合理；但 AI 自查发现的冲突（非用户发起）不应自动确认 | 澄清 | 补一句：仅用户发起的纠偏视为已确认；AI 自检发现的歧义仍进 pm-decisions 待确认 |
| B1-4 | **回归 +30 不可枚举**：SKIP-001~004(4)+DUAL-001~003(3)+COR-004+QQ-010+BRN/ALI/UPD/COR/DEP/JRN/SCH(7) 粗数约 16，与"777→807(+30)"对不上（V0.1 用例未在本文件列出） | 低 | 模块 75 施工时给出完整用例 ID 清单，使 807 可回溯 |
| B1-5 | **零数据源原则遵守**：3.21 属单项目包，未在项目集层落盘聚合，与既有"项目集=纯聚合层"哲学一致，无新增违规 | 通过 | — |

## 3. 关键断言判定

| 断言 | 结论 |
|---|---|
| schema 仍 0.16.0，百科不新增 schema 台阶 | 未证伪（补边界判别式） |
| 3.21 含全部派生生成器 | 未证伪 |
| 缺 brain/journal 不致命；migrate new_dirs 为空 | 未证伪（实测 3.18~3.20 全空） |
| 规则用能力探测不用 skillVersion | 未证伪 |
| 口径家=词库 §2；JSON 无写 corrections | 未证伪（词库模板 §2 纠错映射表实测存在） |
| 8a 实体级联仍在；视图 AUTO 降为兜底 | 未证伪 |
| refresh_views.py 非临时脚本 | 未证伪（打包脚本，同类 carryover_step0） |
| 市监零写 | 未证伪（本 AP 未执行任何写入） |
| 简单查询不载 00 | 未证伪 |
| 反向低版本不删派生文件 | 未证伪 |
| **双轨不会两套语义** | **机制缺口（未闭合，修订）** |
| **单脚本不留半更新** | **机制缺口（未闭合，修订）** |

## 4. 四档结论

**方向正确，无方向性错误，无重做项；核心断言 ①③⑤ 等未被证伪；但存在 2 项关键机制缺口（双轨"一处定义"物理载体缺失、单脚本原子性缺失）+ 2 项施工前须明确的修订项（B1-1 活表含 TD、B1-2 journal 入指纹）。**

按审查红线"任一关键断言被证伪 → 修订-需再审"：② 的关键断言"不会两套语义"当前**未被机制支撑**，判定为——

### 结论：修订-需再审（B1）

放行条件（施工前必须闭合，闭合后回 B 复核即放行）：
1. 给"一处定义"指定物理载体（模板即定义 或 共享 view-columns.json），并加列名一致性回归；
2. 明确 refresh_views.py 原子写机制（临时文件替换 或 per-view 指纹），支撑"不留半更新"；
3. 明确 active-entities.json 收录 TD/人员/开放 R/I（B1-1）；
4. 明确 .state.json 对 journal 的指纹范围（B1-2）；
5. 补 P-CORRECT 用户纠偏 vs AI 自检的确认边界（B1-3）；
6. 模块 75 回归用例 ID 清单可回溯到 807（B1-4）。

以上均非架构调整、不碰市监、不升 schema、不改事实层。闭合后本方案可进入施工。

---

## 5. 第二轮审核（B2，对象 V0.3）——六条放行条件全部闭合，判定**通过-待修订**

> 复核方法：独立重扫 A 修订的 V0.3 正文 + 对照现存模板/规则/脚本实证，不采信闭合声明自述。

### 5.1 六条放行条件逐条复核（全部闭合）

| 条件 | V0.3 落点 | 复核结论 |
|---|---|---|
| 1 一处定义物理载体 | C5 + `scripts/view-spec.json`（new_file）；11/00 改指针；SPEC-001 | 闭合。实测 11 §17.3 现有指纹=9 字段（编号/名称/plan_ref/开始日/结束日/当前阶段名/upstream/downstream/effect），与 view-spec.wp_chart_fingerprint 逐项一致，**未另造指纹**；`wp-index-template` 表头实测 12 列、`plan-template` §3 实测 6 列，与 view-spec 声明列数一致 |
| 2 原子写 | §7 tmp+`os.replace`+`.state.views.*` 分视图 status；DUAL-003/004 | 闭合。整文件要么新要么旧，不出现截断半文件；分视图提交语义清晰 |
| 3 活表含 TD | §5 entities 四类（wp/td/risk+issue/person）；WF-8 只查本表 | 闭合。td 含未办结+待确认终态，源=最新合法日 todos 核心表；WF-8 禁止退回全库扫 |
| 4 journal 入指纹 | `.state.json.journal` 独立段 | 闭合。P-INGEST-DELTA 用该段 diff，不扫 1225 待办 |
| 5 纠偏确认边界 | 00 第 4 条 + COR-005 | 闭合。仅用户发起视为已确认；AI 自检冲突仍进 pm-decisions |
| 6 回归 30 ID 可枚举 | AP-5 固定 SKIP…SCH 30 个 | 闭合。实测计数 4+4+1+5+3+2+5+3+2+1=30，777+30=807 可回溯 |

另：B1 非阻塞建议（20 号/`_version.py` 写死 schema 判别式）已在 AP-4 落为 `20 / _version.py 注释 edit_section`。✅

### 5.2 实证一致性核验（B2 独立扫仓）

- `_version.py` WORKSPACE_SCHEMA_VERSION=0.16.0；VERSION=3.20.0；git HEAD=c2b6831 —— 与方案快照一致，未施工。
- `view-spec.json` / `refresh_views.py` **当前不存在**，AP-4 已标 new_file（施工交付物），不构成缺口。
- 00 第 5 条「§8a 实体级联保留」——实测 00 号 §8a.1/.2/.3 仍在，未误删。
- `verify_projection.py` 实测为只读（C1–C8 投影 + D-TODO-WP 等），与「refresh_views 负责写、verify 只读把关」职责分离一致。
- C6「旧文件即证据不回迁」与 C1 三层路径一致；schema 判别式（必填/迁移义务才升 schema）在 AP-4 有明确落点。

### 5.3 B2 新增发现（非阻塞，施工时补定义即可，不构成否决）

| # | 发现 | 级别 | 建议 |
|---|---|---|---|
| B2-1 | **SPEC-001 只校验「脚本产出 == view-spec」**，未校验「view-spec == 模板表头」。C5 约束 4「改列=只改 JSON+模板表头（须一致）」靠人工保证，JSON 与模板表头仍可能漂移（改了一处漏另一处） | 中（加固） | 增加 SPEC-002：脚本启动时读模板表头与 view-spec 列定义比对，不一致即 fail；或 view-spec 由脚本从模板表头生成，消除人工同步 |
| B2-2 | **alias_index 的派生来源未定义**：方案只说「别名跳转/派生」，但 `农专→农民专业合作社` 这类别名到底来自词库 §1 confirmed、词库 §2、还是 WP 名称？ALI-001 依赖 alias 命中，源不定义脚本无从生成 | 中（澄清） | 明确 alias 聚合源 = 词库 §1 confirmed 术语 + WP 名称 + 花名册人名；并在 §5 alias_index 注明来源文件 glob |
| B2-3 | **`.state.facts` 覆盖的「最新合法日待办」glob 未写明**：`.state.json` 示例只有 `wps/WP-073.md`，待办/登记册/词库的具体路径模式未列全，脚本实现时可能漏指纹 | 低 | §5 .state 补一份 `facts` 覆盖的路径 glob 清单（todos/{最新日}/*.md、risks/issue/decisions/requirements/*.md、context/domain-glossary.md、plans/PLAN-*.md） |
| B2-4 | **C2 能力探测第 2 条「facts_fingerprint 是否等于当前事实文件」与 `.state` 分视图指纹命名不一致**（brain 头用 facts_fingerprint，.state 用 facts hash + views.*） | 低（术语） | 统一命名为 facts_fingerprint（聚合）+ view_fingerprint（每视图），避免探测规则与存储结构各说各话 |

### 5.4 四档结论（B2）

**六条放行条件全部闭合；实证核验未发现断言被证伪；无方向性错误、无架构级问题。**

### 结论：通过-待修订（B2）

- 施工时补 B2-1（SPEC-002 JSON↔模板一致性）、B2-2（alias 派生源）、B2-3（facts glob 清单）、B2-4（指纹命名统一）四处定义/加固；其中 B2-2 影响 ALI-001 实现、B2-1 影响「一处定义」落地强度，建议在 Module 75 施工前完成。
- 施工仍禁碰市监、禁升 schema、禁改模板列、禁改八块、禁 git。
- 上述补定义不涉及架构调整，无需再审即可随施工闭合；若施工中出现对 C0–C6 契约的改动，回本节追加第三轮复核。

---

## 6. 第三轮审核（B3，对象 V0.4）——B2 四处全部闭合，但新发现 1 项内部矛盾 + 1 项落地缺口，判定**通过-待修订**

> 复核方法：独立重扫 V0.4 正文 + 对照现存模板/22 号/词库模板实证，不采信闭合声明自述。

### 6.1 B2 四处复核（全部闭合）

| B2 | V0.4 落点 | 复核 |
|---|---|---|
| 1 SPEC-002 JSON↔模板 | C5 约束 3 `--check-spec`（index/§3 表头==view-spec，不一致 exit 2）；SPEC-001 已并入模板表头比对 | 闭合 |
| 2 alias 派生源 | §5 alias_index 六源表（词库 §1/§2、WP 名、废弃 WP/supersedes、花名册、§6 缩写） | 闭合（但见 B3-2） |
| 3 facts glob | `.state.facts` 覆盖清单写死，含「最新合法日=22 号定义」 | 闭合（22 号实测：最新合法日=`date≤今天 且存在 _index.md 的最大日期`，与方案引用一致） |
| 4 指纹命名 | `facts_fingerprint` / `journal_fingerprint` / `views.*.view_fingerprint` 统一 | 闭合 |

### 6.2 B3 新增发现

| # | 发现 | 级别 | 说明 |
|---|---|---|---|
| **B3-1** | **内部矛盾：brain 含「业务待拍板≤10」，但 `.state.facts` 明确排除 `pm-decisions.md`**。pm-decisions 变化 → `facts_fingerprint` 不变 → refresh_views 不重建 brain → 待拍板节永久旧值。而 05 第 5 条又要求「横幅只报业务待裁定」（实时读）——同一条信息，brain 放一份（会旧）、横幅实时读一份，双源且可能打架 | **中（功能矛盾）** | 二选一：① 把 `pm-decisions.md` 加入 `.state.facts` glob（确认面变化也触发重建）；② 从 brain 删掉「业务待拍板」节，全部走实时读 pm-decisions（05 横幅已实时）。倾向 ②（派生层不复制实时面，避免双源） |
| **B3-2** | **ALI 两跳链路未定义**：alias_index 词库 §1 confirmed 条目为 `type: term`（如 农专→农民专业合作社），但 WF-8 只查 `type=td + type=wp`；ALI-001 要求「农专注销 90%」落到 WP。term 条目被 WF-8 跳过，「农专」如何跳到 `注销-农民专业合作社` WP 未定义两跳链 | **中（落地缺口）** | 补一句：命中 term 条目后，用 canonical 名称对 `wp.name` 做次轮匹配生成 wp 别名；WF-8 对齐链 = alias→term.canonical→wp.name→wp.id |
| B3-3 | 「有结转完成标记的最近 todos 日」表述与 22 号「存在 _index.md 的最大日期」措辞略有出入 | 低 | 引用处改为「按 22 号最新合法日定义」，避免两处口径漂移 |
| B3-4 | C2 探测依赖 `.state.json`，但 `.state.json` 本身在 C1 属「缺了不致命」派生物——缺它时探测/降级路径未写 | 低 | 补一句：无 `.state` 时视为全部 stale，走 05 规则第 2 条降级（读事实原文+声明 as-of） |

### 6.3 四档结论（B3）

**B2 四处全部闭合，无断言证伪，无方向性错误；但 B3-1（pm-decisions 与 brain 待拍板双源矛盾）会在施工后直接造成「待拍板视图时效失效」，B3-2（ALI 两跳链缺失）会让 ALI-001 落地悬空。**

### 结论：通过-待修订（B3）

- 施工前把 B3-1（二选一写死）与 B3-2（两跳链）补进正文；B3-3/B3-4 随手修正。均不涉及架构、不升 schema、不碰市监。
- 补完后无需整轮再审，Module 75 施工时以正文为准即可；若施工出现对 C0–C6 的改动，回本节追加第四轮复核。

---

## 7. 第四轮审核（B4，对象 V0.5）——B3 四处全部闭合，无断言证伪、无阻塞，判定**通过-可施工（附低优先建议）**

> 复核方法：独立重扫 V0.5 正文 + 对照现存 05 号规则/22 号/模板实证，不采信闭合声明自述。

### 7.1 B3 四处复核（全部闭合）

| B3 | V0.5 落点 | 复核 |
|---|---|---|
| 1 brain vs pm-decisions | §5 brain 节清单改为「仅这些：活 WP、未办结 TD、开放 R/I、别名跳转、近 7 日证据指针」+ 显式「**禁止待拍板/等你裁定节**」；05 第 1 条「仍须按 §1a 实时读 pm-decisions 做横幅」 | 闭合。实测现存 05-query-rules.md §1a 确实实时读 pm-decisions 八块开放行之和做横幅，引用有效 |
| 2 term 两跳链 | §5 P-RESOLVE 七步（alias→term.canonical→entities[wp] 含 canonical→0/1/>1 分支 + 未命中问）；ALI-001 已升级为两跳语义 | 闭合。第二跳依赖 wp.aliases 含 §3 功能点名（如「注销-农民专业合作社」作为功能点落在总包 aliases），V0.5 已把「§3 功能点名」纳入 wp aliases 派生 |
| 3 最新合法日 | `.state.facts` 改为 22 号原文「`date≤今天` 且存在 `_index.md` 的最大日期」 | 闭合。实测 22-carried-over-rules.md 第 75 行定义一致 |
| 4 无 .state 降级 | C2 第 0 条「无 .state.json → 全部 stale → 走 05 第 2 条」；05 第 2 条已含「无 .state.json」 | 闭合 |

### 7.2 回归与一致性（未动）

- Module 75 仍 30 ID（SKIP/DUAL/SPEC/BRN/ALI/UPD/COR/DEP/JRN/SCH），777+30=807 可回溯；ALI-001 升级为两跳语义未新增 ID。✅
- `--check-spec` 已并入 SPEC-001（表头==view-spec==模板），未另增 ID，计数一致。✅
- 阻断清单未新增。✅

### 7.3 B4 新增建议（均为低优先，不构成阻塞，可施工时顺手收口）

| # | 建议 | 级别 | 说明 |
|---|---|---|---|
| B4-1 | **active-entities 的 wp 源依赖 `_index` §1「进行中」派生列**——派生读派生，靠刷新顺序（index→…→json）保证新鲜。更稳的做法：wp 直接以 `wps/WP-*.md` frontmatter `status/effect` 判进行中/废弃，不依赖 `_index` 镜像 | 低 | 非阻塞。现状顺序正确（index 先于 json），若施工嫌脆可改；不改也成立 |
| B4-2 | **P-RESOLVE 未定义「原文命中多条 alias」的优先级**：如「农专」同时命中词库 §1 term 与花名册缩写时未定取舍 | 低 | 建议补一句：wp/td 命中优先；无 wp/td 才走 term 第二跳；person 仅在明确指人时用 |
| B4-3 | **C2 探测第 2 条只比 `facts_fingerprint`，但 §7 重建条件是 facts+journal 两者都查**——探测与重建不对称（非矛盾，探测是准入、重建是写入） | 低 | 建议 C2 第 2 条补一句「探测以 facts 为准；重建时 journal 变化也触发写盘」，避免施工误解 |
| B4-4 | **ALI-001 正确性依赖「§3 功能点名被脚本解析进 wp.aliases」**——若施工时脚本漏解析功能点名，第二跳即失效 | 施工关注 | 非文本缺口；Module 75 施工须用真实项目数据（全链通 85 WP）验证 ALI-001 能由「农专注销」落到注销总包 |

### 7.4 四档结论（B4）

**B3 四处全部闭合，回归 30 ID 与阻断清单未变，无断言证伪、无方向性错误、无新增阻塞。** 方案自 V0.3 起架构已稳定，V0.4/V0.5 均为消化审核意见的收敛，正文口径与现存规则/模板/实测数据一致。

### 结论：通过-可施工（B4）

- B4-1~B4-3 为低优先建议，采纳与否不影响放行；B4-4 作为施工必检项（用真实全链通库验证 ALI-001 两跳）。
- 施工范围以 AP-4 为限：禁碰市监、禁升 schema、禁改模板列、禁改八块、禁 git。
- 施工后如有对 C0–C6 契约的改动，回本节追加复核；未改动则本方案定稿。

---

# A 对 B1 的闭合声明（V0.3，供 B 第二轮）

B1 结语「修订-需再审」接受。六条放行条件在方案正文的落点：

| 条件 | 落点 |
|---|---|
| 1 一处定义 | C5 + `scripts/view-spec.json`；11/00 改指针；SPEC-001 |
| 2 原子写 | §7 tmp+`os.replace` + `.state.views.*` 分视图 status；DUAL-003/004 |
| 3 活表含 TD | §5 entities 四类表；WF-8 只查本表 |
| 4 journal 指纹 | `.state.journal` 独立段 |
| 5 纠偏边界 | 00 第 4 条 + COR-005 |
| 6 回归 30 ID | AP-5 枚举 SKIP…SCH 共 30，777+30=807 |

请 B 只核这六条是否仍缺口。未授权施工。

---

# A 对 B2 的闭合声明（V0.4）

B2「通过-待修订」接受。四处不留施工口头债：

| 条件 | 落点 |
|---|---|
| B2-1 | C5 `--check-spec` + SPEC-001 含模板表头 |
| B2-2 | §5 alias_index 六源表 |
| B2-3 | `.state.facts` glob 清单 |
| B2-4 | `facts_fingerprint` / `journal_fingerprint` / `view_fingerprint` |

未授权施工。用户授权后按 AP-4 执行。

---

# A 对 B3 的闭合声明（V0.5）

B3「通过-待修订」接受。选 **删 brain 待拍板**（不把实时确认面做成派生快照）。

| 条件 | 落点 |
|---|---|
| B3-1 | §5 brain 禁止该节；05 横幅只读 `pm-decisions.md` |
| B3-2 | P-RESOLVE：alias → term.canonical → wp.name/aliases → wp.id；功能点名写入 wp.aliases |
| B3-3 | 最新合法日 = 22 号「存在 `_index.md` 的最大日期且 date≤今天」 |
| B3-4 | C2 第 0 步 + 05 第 2 条 |

未授权施工。

---

# A 对 B4 的闭合声明（V0.6）

B4「通过-可施工」接受。低优先写入正文。

| 条件 | 落点 |
|---|---|
| B4-1 | `type=wp` 只读 `wps/WP-*.md`；`--all` 先 parse WP 再写 index 与 json |
| B4-2 | 多命中：ID → wp/td → term 第二跳 → person（仅指人） |
| B4-3 | 查询比 facts；重建比 facts **或** journal |
| B4-4 | fixture + 市监该 WP **只读**抽查，禁止写回 |
| 自检 | 第二跳用 开办/变更/注销 收口 |

未授权施工。
