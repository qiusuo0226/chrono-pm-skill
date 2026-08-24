# 升级到 3.12.0

> 从 3.11.0 升级到 3.12.0  
> 发布日期：2026-08-24  
> Schema 变更：**不升**，workspace schema 保持 **0.14.0**  
> CR：CR-20260824-002 / 003 / 004  
> 施工依据：三份 CR + 本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.11.0 → 3.12.0。  
> 用户拍板：可以执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再审核。

## 变更摘要

过程调用索引 + 简单查询仅 05（迁走 Qoder 轻量能力后删除宿主特例文件）；正式待办必须恰好绑定 1 个已规划 WP；派活先查重再建/改、禁止问要不要建；待办结束不得超 WP（开始可早，轻提示）；「拆文件」强制走 source-split 入库 `ai/requirements/sources/`。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径
- 禁止升 schema
- 禁止把过程正文抄进 SKILL.md（净增 ≤20 非空行）
- 禁止重写 07 正文搬家
- 禁止自动改待办日期
- 禁止全库扫 WP Ref
- 禁止留 `QODER_RULES.md` 空文件
- 禁止在 ST-001/004/005/006 未通过口径下删除 QODER_RULES.md
- Portfolio 不代写成员项目

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260824-002.md` | 节点 A 结构 |
| A1.2 | `governance-shared/change-requests/CR-20260824-003.md` | 节点 B 待办 |
| A1.3 | `governance-shared/change-requests/CR-20260824-004.md` | 节点 C 拆文件 |
| A1.4 | 本文件 | 本施工清单 |
| A1.5 | `governance-shared/impact-analysis/IA-20260824-002.md` | 本 IA（覆盖三 CR） |
| A1.6 | `governance-shared/migrations-history/upgrade-to-3.12.0.md` | 拷贝本文件 |
| A1.7 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.12.0.md |
| A1.8 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.12.0.md` | 指针文件 |

### A2. 节点 A 结构（节点2）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `references/23-procedure-index.md` | **新增**：过程签名（Trigger/Pre/Calls/Writes/Forbidden），摘要≤200 字，不抄规则正文 |
| A2.2 | `SKILL.md` | **拆分**「本项目查询」为「简单查询=仅 05」+「复杂查询=00+05+17」。写入/派活/拆文件行 +23。§15：00 改为写入与复杂必须；21 改为写入与复杂自动加载；新增 23 行。前言 21 自动加载收窄。拆文件命中改走源文档拆解行。净增≤20 非空行 |
| A2.3 | `05-query-rules.md` | §6.3 补「今天谁没交日报」。新增「安全升级」：最小读取不得用于写入；改口写入立即加载 §7。不删不缩最小读取正文 |
| A2.4 | `16-skill-governance-rules.md` §18 | 白名单删除 QODER_RULES.md 行 |
| A2.5 | `SKILL_BLUEPRINT.md` Limitations | Qoder 行改为：简单查询仅 05；SKILL.md 体积预算；写入才加载 00 |
| A2.6 | `QODER_RULES.md` | **最后删除**（A2.1–A2.5 完成后） |

### A3. 节点 B 待办（节点3）

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `00-pm-main-rules.md` | 派活分词；WF-8 入口⑦+查重步；S1 多 WP 主题可分则自动拆；S4 按行号：L742 废可暂填待绑定；落位废独立任务 none/待绑定；默认归属不得无 WP 落盘；§8b 基数恰好 1、无匹配不落盘；§8c.1 窗变检查（在窗不改、结束越界问 A/B/C）；禁止问「要不要建待办」 |
| A3.2 | `01-daily-report-rules.md` | 够正式但绑不上 WP → 不自动建，进 pm-decisions 并问绑哪个 |
| A3.3 | `22-carried-over-rules.md` | 空 WP Ref 高置信回填恰好 1；低置信不把无 WP 行结转到今天核心表；编号不变；多值拦截 |
| A3.4 | `14-self-check-rules.md` | D15/D21：多值 WP Ref 为异常；空值触碰须问绑；仍禁止全库扫 |
| A3.5 | `personal-daily-todo-template.md` | WP Ref 单元格注释：必填恰好一个 WP-NNN；不加列 |

### A4. 节点 C 拆文件（节点4）

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | `10-update-trigger-rules.md` | Level 1 增加拆文件/拆文档；源文档信号扩词；命中不先问要不要解析；分词：拆解需求≠拆文件；一句两意先 P-SPLIT 再可选 P-OUTPUT |
| A4.2 | `07-requirement-rules.md` | 文首改为 P-DOC-INGEST 必须 CALL P-SPLIT；§3 与拆文件分词一句。**不重排章节** |
| A4.3 | `source-split-skill/references/split-rules.md` | 首句改为由 P-DOC-INGEST/P-SPLIT 加载。不改六件套/指纹/不落待办 |
| A4.4 | `source-split-skill/CAPABILITY.md` | 何时加载与 23 对齐 |
| A4.5 | `00-pm-main-rules.md` 意图表 | 「文件解析入库」拆：过程记录走 10；源文件拆解走 P-DOC-INGEST |

### A5. 示例 / 流程图 / README（节点5）

| # | 文件 | 动作（写死） |
|---|---|---|
| A5.1 | `examples/04-投喂合同和立项.md` | 助手产物写明 `sources/{编号}/` 六件套，不是 HTML 替代入库 |
| A5.2 | `examples/05-确认需求和工作包.md` | 拆待办必须已规划 WP；「只认包不拆人」合法（WP 可 0 待办） |
| A5.3 | `examples/19-派活与拆文件入库.md` | **新增**：派活查重/禁问要不要建；拆文件进 sources |
| A5.4 | `examples/README.md` | 加 19；阅读顺序补「派活/拆文件」 |
| A5.5 | `SKILL_MODULE_MAP.md` | G4 待办必须绑 WP；新增 G18 派活、G19 拆文件调用 |
| A5.6 | 仓库根 `README.md` `README.en.md` | 版本 3.12.0；回归用例数；开口表补拆文件入库 |

### A6. 回归（节点6）

| # | 动作（写死） |
|---|---|
| A6.1 | 模块 65 派活/基数/时间盒（DS/CO） |
| A6.2 | 模块 66 拆文件（SF） |
| A6.3 | 模块 67 结构/Q4（ST，含 ST-006 删 QODER 前置） |
| A6.4 | 改 BS-018 / WP-002 / DF-019 口径：无 WP 不得落正式待办 |
| A6.5 | 合计 **525→约 553**（以实际写入为准） |

### A7. 版本触点（节点7）

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | `scripts/_version.py` | SKILL_VERSION=3.12.0；schema 0.14.0 |
| A7.2 | 跑 `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | CHANGELOG 双包 | 3.12.0 段 |
| A7.4 | BLUEPRINT 演进表 | 3.12.0 行 |
| A7.5 | Portfolio `02-aggregation-query-rules.md` | 待办 WP Ref 按单值；缺/多值当脏数据不双计 |
| A7.6 | Portfolio 锁步版本 | 能力除 A7.5 一句外零改 |

### A8. 基线与发布（节点8）

| # | 动作（写死） |
|---|---|
| A8.1 | `baselines/3.12.0/` 双子树全量快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每完成一个节点：annotated tag（中文说明）推 origin 与 github |
| A8.4 | AP 草稿：基线拍完后删除（`planning/` 仅 README） |
| A8.5 | 全部完成后请用户审核；不提前打断 |

---

## B. 业务工作区

**本发布不代做任何业务仓。**

通用算法（执行时对当时打开的工作区，禁路径常量）：不扫全库回填 WP Ref；仅结转/触碰时处理空值。

## C. 验证检查

- [x] `_version.py` 3.12.0 / 0.14.0
- [ ] SKILL.md 相对 3.11.0 净增非空行 ≤20
- [ ] 包内无 `QODER_RULES.md`；16 白名单无该行
- [ ] 简单查询路由仅 05
- [ ] 回归模块 65–67 已写入
- [ ] audit_release 退出码 0
- [ ] 正式文档不引用 upgrade-plan 路径
