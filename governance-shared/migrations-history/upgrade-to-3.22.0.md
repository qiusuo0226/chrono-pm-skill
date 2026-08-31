# 升级到 3.22.0

> 从 3.21.1 升级到 3.22.0  
> 发布日期：2026-08-31  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260831-001～004  
> IA：IA-20260831-001～004  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.21.1 → 3.22.0。  
> 用户拍板：执行升级；每节点 annotated tag 推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是（SKILL.md + 00）。按 16 §4 拆 **4** 个 CR。施工只认回归套件合计行（基线 807 + Module 76/77）。

## 变更摘要

会议转写走 WF-3 快路径（先纪要后结转，禁止误入源文档拆解）；结转脚本用技能包路径并对空花名册回退；查询每次比指纹、SRC 进 alias、只读不 C'/Step 0；查询轮不自动写词库 pending，升格只认命题。问答残差：提问带对象、宿主假执行门拆穿。跳版本不升 schema。双包同号 3.22.0。

## 施工禁区

- 禁止升 workspace schema；禁止改 `wps/_index` 列数与 WP 模板列
- 禁止新建 Project `references/NN-*.md`
- 禁止改 pm-decisions 八块；禁止改 `skill-contract.md` 正文
- 禁止引入 git 到业务工作区
- 禁止写入市监业务库
- 禁止 `reply-norm-skill/SKILL.md`
- 禁止把会议登记为源文档类型；禁止重写 P-SPLIT 引擎
- 禁止把 22 HARD BLOCK 改成「无 Python 可跳过结转」
- 禁止新建会话记忆 / 答案缓存 / 手写「主题→文件」进 `_index` 或 brain
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）
- 禁止 Portfolio 写 `projects/*/ai`；本包 Portfolio 仅版本锁步

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260831-001.md`～`004.md` | 四 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260831-001.md`～`004.md` | 四 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.22.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.22.0.md` | 仅锁步指针 |

### A2. 引擎（节点2，CR-002 脚本段 + CR-003 引擎）

- `scripts/carryover_step0.py`：`main()` 对合法日倒序找 `names>0`；stdout `ROSTER_FALLBACK`；都空 `FAIL:ROSTER_EMPTY` + exit 2
- `scripts/view-spec.json`：`brain_fact_globs` 增 sources `_index` 与 `meta.md`
- `scripts/refresh_views.py`：parse SRC meta 进 alias；brain 别名短表；collect_facts 含 sources
- `scripts/migrate_workspace.py`：3.22.0 能力条 + 会议误拆 dry-run 检测器

### A3. 协议（节点3，CR-001/002/003/004 规则）

SKILL §5/§6 会议排除、脚本包内路径、查询先 P-VIEWS；00 §2.7 排除句、WF-3 顺序、CQ-5；02 快路径；05 文首 if-else + §1b/§2.5a/§6.3/§1.5；10 信号；17 查询闸；22 脚本路径；23 会议支；split-rules 排除；reply-rules 残差；examples/08 去 T-A4 可选化。

### A4. 回归（节点4）

`tests/regression-suite.md` Module 76 + 77。阻断见套件。

### A5. 版本触点（节点5）

`_version.py` 3.22.0 schema 0.16.0；`sync_version.py`；CHANGELOG 双包 + BLUEPRINT + 根 README×2；Portfolio 锁步。

### A6. 基线与发布（节点6）

`baselines/3.22.0/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。禁止对市监跑 migrate。

## C. 节点完成勾选

- [x] A1 治理（`v3.22.0-step1`）
- [x] A2 引擎（`v3.22.0-step2`）
- [x] A3 协议（`v3.22.0-step3`）
- [x] A4 回归（`v3.22.0-step4`）
- [x] A5 版本锁步（`v3.22.0-step5`）
- [x] A6 基线 + audit + 删 AP（`v3.22.0-step6` / `v3.22.0`）
- [x] 分发包已写入 Downloads：`ChronoPM-Project-Skill-v3.22.0.zip` + `ChronoPM-Portfolio-Skill-v3.22.0.zip`
- [x] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [x] 双包 3.22.0；schema 0.16.0；audit 17/17
- [x] planning/ 仅留 README

### 收尾补记（2026-08-31，不另起版本）

- 用户核验通过并指示收尾。Grok 安装区**不代更**。
- B2 验收漏改已补：22 §3 第 3 步、SKILL §5.1b 包内路径；05 源文档行加主题/取证边界。
- 施工收尾核对：`governance-shared/review-checklists/review-20260831-3.22.0.md`，结论 **通过-升级成功**。
- 四 CR Status=completed；planning/ 仅 README。
- 业务仓未代迁（B 节 skip）。

---

## D. B2 升级验收审核（2026-08-31）

> 本章节由 Agent B2 在 A 宣称「升级完成」后进行独立验收。复审/复盘时**重写覆盖**本章节，不改动 A 的施工记录正文。审核对象 = 3.22.0 实际落地 vs 本清单 A2–A6 + AP §19 闭合表。

### D.1 验收方式

- 独立扫描开发仓（`git log` 6 节点 + 工作树）、基线 `baselines/3.22.0/`、分发包 zip、回归套件统计、audit_release.py 实跑。
- 不读不写市监业务库；工作空间 = `C:\Users\qiusuo\Downloads\ChronoPM Skill`。

### D.2 已核验通过项（B2 亲验）

| # | 验收点 | 实测 | 结果 |
|---|---|---|---|
| 1 | 版本六触点 3.22.0 | VERSION×2、`_version.py` SKILL_VERSION、skill.json、CHANGELOG×2 均 3.22.0；schema 保持 0.16.0；Portfolio 锁步 | ✅ |
| 2 | audit_release.py 独立实跑 | 17/17 PASS（含版本、幽灵引用、基线、双包、模拟 pack、残留 AP） | ✅ |
| 3 | 分发包 | Downloads 含 `ChronoPM-Project-Skill-v3.22.0.zip`(500884B) + `ChronoPM-Portfolio-Skill-v3.22.0.zip`(56471B) | ✅ |
| 4 | 施工治理 | CR-001～004、IA-001～004、upgrade-to 落地；planning/ 仅留 README（AP 已删） | ✅ |
| 5 | R1：reply-rules 残差 | 硬规则 7（推断标推测/80%≠确认）+ 正反例 4 行（宿主误弹/中途确认/已裁定/80%）；capability-boundary RN-001～011；examples/08 删 T-A4 A/B/C 可选化（改「已记下请认」） | ✅ |
| 6 | R2：会议快路径 | 02 号 §0 快路径（先 meetings/ 不碰 todos 不触发 22）；00 §2.7 排除句；WF-3 顺序；10 号信号；23 号会议支（禁 P-SPLIT）；split-rules 首段排除；migrate `_detect_meeting_sources` dry-run | ✅ |
| 7 | R2：结转脚本 | `carryover_step0.py` `resolve_roster` 倒序回退 + `ROSTER_FALLBACK`/section3 + `FAIL:ROSTER_EMPTY` exit 2；22 号 L20 与 23 号 P-CARRY 包内路径 | ✅ |
| 8 | R3：查询派生定位 | 05 §0 if-else（有/无 Python）+ §1b/§2.5a/§6.3 三处收口；SKILL §5.3 每次查询先 P-VIEWS；CQ-5 澄清；refresh_views parse SRC meta → alias（type=src）；view-spec globs 增 sources；brain 别名短表 80 行 | ✅ |
| 9 | R4：口低证高 | 17 §8.1 查询禁自动 pending、SUGGEST ≤7、T1/T2 才 confirmed；05 §1.5 同步 | ✅ |
| 10 | 回归 | Module 76（MTG/CO-S）+ Module 77（QL/TG/RN/MIG）落地；合计 830（489 positive / 341 negative）；阻断/非阻断清单齐全 | ✅ |
| 11 | 施工禁区 | references/ 仍 21 个 NN 文件（无新增）；无 reply-norm SKILL.md；未升 schema；未写市监；无会话记忆文件 | ✅ |

### D.3 B2 发现的遗漏与不一致（不阻塞发布，建议跟踪）

| # | 问题 | 严重度 | 说明与建议 |
|---|---|---|---|
| ① | 22 号 §3 执行流程第 3 步（L81）仍是相对路径 `python scripts/carryover_step0.py --root <项目根>`，未随 L20 改为包内路径 | 中 | §9.4 要求「22 / 23 P-CARRY / SKILL §5 同义」。L20（时机 0）已改包内，但 L81（Step 0.5 流程段）漏改，且同病存在于**基线 3.22.0 与分发包**。AI 若按 L81 执行仍可能踩业务 cwd 坑。**建议**：补丁统一为 `python "<Skill包根>/scripts/carryover_step0.py" --root "<项目根>"`，与 L20 同文 |
| ② | SKILL.md §5.1b（L86）P-VIEWS 仍是相对路径 `python scripts/refresh_views.py` | 中 | 已在 AP §17.5-① 指出过；§5.3（L90）已改包内，但 §5.1b 漏改，基线/分发包同病。**建议**：补丁统一包内路径 |
| ③ | 回归套件 Module 77 用例 ID 用 `QL-xxx`/`TG-xxx`，而 AP/CR/upgrade-to 用 `QLOC-xxx`/`TERM-xxx` | 低 | 功能与阻断判定不受影响（合计/阻断/非阻断均一致），但正式文档与套件编号口径不一致，后续引用易错位。**建议**：套件或 AP 二选一统一编号 |
| ④ | 05 号 L108「源文档 / 拆解产物」查询行仍是旧路径（`sources/_index.md` → `_digest.md`），与 §0 新的 alias 一跳（SRC 标题）机制并存 | 低 | 功能可回退（`sources/_index.md` 已入 globs 会被索引），但描述与新定位主路径不统一。**建议**：将该行改为「alias 一跳（SRC 标题）→ meta 命中 → 实读 `_digest.md`/facts」 |

### D.4 结论

- **升级主体验收通过**：A 的施工声明（audit 17/17、回归 830、双包 3.22.0、schema 不变、AP 已删、分发包已产）经 B2 独立复核全部属实；四个 CR 的规则/脚本/回归/版本触点均落地，施工禁区未越界。
- **存在 2 项中严重度路径残留（D.3 ①②）与 2 项低严重度口径不一致（D.3 ③④）**，均在 3.22.0 功能主体外，属同版本内可顺带修正的细节，**不构成重新发布的阻塞**。建议下一 Patch 补丁统一，不必重发 3.22.0。
- 用户核验：功能验收以回归 830 与日常使用为准；若采纳 D.3 ①②，建议并入下一版本补丁统一处理。

### D.5 收尾闭合（2026-08-31，用户指示不升版本）

用户核验通过并指示收尾。下列 D.3 项在本版收尾补丁闭合，不另起 PATCH：

| # | 处置 |
|---|---|
| ① | 已补：22 §3 第 3 步改为包内路径，与 L20 同义；stdout 含 `ROSTER_FALLBACK` / `FAIL:ROSTER_EMPTY` |
| ② | 已补：SKILL §5.1b 改为包内路径，与 §5.3 同义 |
| ③ | 不改：现行套件/CR 已用 QL/TG；QLOC/TERM 仅历史 AP 草稿（已删） |
| ④ | 已补边界：05 源文档行仅 SRC 编号/拆没拆走 `_digest`；主题定位先 alias |

施工收尾核对 `review-20260831-3.22.0.md`：**通过-升级成功**。Grok 安装区不代更。基线 3.22.0 已同步本补丁。
