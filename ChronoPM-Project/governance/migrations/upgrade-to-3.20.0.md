# 升级到 3.20.0

> 从 3.19.0 升级到 3.20.0  
> 发布日期：2026-08-29  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260829-001～003  
> IA：IA-20260829-001～003  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.19.0 → 3.20.0。  
> 用户拍板：执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V0.12（B1 通过-可执行；B2 V0.11 通过-待修订，A 已消化 R1–R5 至 V0.12；用户 2026-08-29 开始执行）。  
> 按 16 §4 拆 **3** 个 CR。施工只认回归 **777**（基线 729 + Module 74 新增 48）。

## 变更摘要

WP 增加可选 **§3c 分工矩阵**（点名责任，不是进度人）；C(P)/E(P) 作日报/WF-8 挂包先验；个人待办派生 **§0.7**；办结追加 **§4c**；投喂无感知入库+落点回执；卡点高置信先记问题待确认。集层 **V-14** 混报拆分 + **弱结构投喂**（槽位+映射档，乙案落盘）。读侧进度默认**完整表**，撤销 v3.17 摘要当正文。代码源本版只注册指针。双包同号 3.20.0。schema 0.16.0。

## 施工禁区

- 禁止升 workspace schema；禁止改 `wps/_index` 列数
- 禁止新建 Project `references/NN-*.md`
- 禁止给 WP §3（功能点）**当前表**加执行人列（S6 / WPS-014）
- 禁止占用 `## 3b.`（WPS-016 功能点别名）；正式节号仅 `## 3c. 分工矩阵（可选）`
- 禁止 SCAN / ALIGN / CHART / 日报回写 §3c
- 禁止 Portfolio 写 `projects/*/ai`
- 禁止新开 `portfolio/batches/` 或 `portfolio/ingest-maps/` 顶层目录
- 禁止把业务 Excel 列号写进规则
- 禁止本版 source_code 指纹刷新链（劈 3.21）
- 禁止 13 站全填 / 功能点×阶段负责人表
- 历史 CHANGELOG / 旧 upgrade-to 的 §3b **不改**
- 正式文档不得引用 upgrade-plan 草稿路径
- 禁止写入业务工作区（开发仓无 `ai/wps/` 则 B 节 skip）
- 00 的 CR-A 与 05 的 CR-C 可分节点，但 8c 闸与 §6.8 口径必须同文

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260829-001.md`～`003.md` | 三 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260829-001.md`～`003.md` | 三 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.20.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.20.0.md` | 施工含 V-14 + 弱结构投喂，不只指针 |

### A2. 写侧（节点2，CR-001）

见 CR-001。模板 §3c + §4c；00 C(P)/8c/§5.0 回执 vs D9；01 §1.5 + 完备闸；04 卡点高置信先记；06 L279 12 列 + sources `original.*`/`rows.md`；10 L2/L3 默认入库；22/个人模板 §0.7；23 SCAN 禁写 3c、P-WF8 补 C(P)、P-WP-STAMP Writes=§4b+§4c；registry 增 `source_code` + `weak_ingest`。

### A3. 集层（节点3，CR-002）

见 CR-002。Portfolio 01 L11/§2 乙案例外；02 V-14 + 弱结构投喂；SKILL V-1～V-14；分发稿模板；ingest-map 模板。禁止代写成员。

### A4. 读侧（节点4，CR-003）

见 CR-003。05 新建 §6.8 人查询；§6.7/§6.9 进度默认完整表，显式撤销 v3.17 摘要当唯一正文。

### A5. 回归（节点5）

`tests/regression-suite.md` Module 74。既有 WPS-007/014/015/016 保持阻断。合计 **777**。

### A6. 版本触点（节点6）

| # | 文件 | 动作 |
|---|---|---|
| A6.1 | `_version.py` | 3.20.0；schema 0.16.0 |
| A6.2 | `sync_version.py` | 双包触点 |
| A6.3 | CHANGELOG 双包 + BLUEPRINT + 根 README×2 | 3.20.0；回归 **777** |
| A6.4 | `migrate_workspace.py` VERSION_CAPABILITIES | 3.20.0 schema 0.16.0 |

### A7. 基线与发布（节点7）

| # | 动作 |
|---|---|
| A7.1 | `baselines/3.20.0/` 双子树 |
| A7.2 | `audit_release.py` 退出 0 |
| A7.3 | 每节点 annotated tag 推 origin 与 github |
| A7.4 | 终 tag `v3.20.0` |
| A7.5 | 删除 AP 草稿；分发包；全部完成后再请用户核验 |

---

## B. 存量工作区

开发仓无 `ai/wps/` → **skip**。

有 `ai/wps/` 的业务仓（升级对话中执行，不在本开发仓写业务文件）。无 Python 批量脚本。

| # | 动作 | 不做 |
|---|---|---|
| B1 | 存量 `## 3b.` → `## 3. 实体/功能点行`（未迁完仍认两种标题） | 不改历史 CHANGELOG 的 §3b 用词 |
| B2 | `## 3c` 且标题含分工/RACI/负责人 → 正式标题，表体不动 | 不补确认人列、不补缺角色列 |
| B3 | 无匹配 3c → 不新建节 | 不按 Owner 猜填 3c |
| B4 | 最新合法日个人文件：有则重算 §0.7；无则不建空日 | 不拷昨日 §0.7 |
| B5 | 进行中 WP：§8 🔄 空岗列入升级报告，不编人 | 不填满 13 站 |
| B6 | 升级回执：改标题数、§0.7 数、空岗清单、**根级散落目录清单（只列不删）** | Portfolio 升级不写成员项目；不删散落目录 |
| B7 | 不回填全部历史进 §4c；点名刷新某 WP 才扫该包历史 TD | 禁止升级全库扫 todos |

验证：B2 标题数；抽样 §0.7 阶段=对应 WP §3；WPS-016 仍成立。

---

## C. 验证检查

- [ ] `_version.py` 3.20.0 / schema 0.16.0
- [ ] 正式标题 `## 3c. 分工矩阵（可选）`；当前表仍 5 列无人名
- [ ] 改 3c 同回合 §6；8c.2 能拦住漏写；ING 写 3c 同闸
- [ ] 05 §6.8 人查询；进度默认完整表
- [ ] V-14 不写 `projects/*/ai`；弱结构投喂乙案路径
- [ ] 回归 777；audit 退出 0
- [ ] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [ ] 双包 3.20.0
- [ ] planning/ 仅留 README；本版 AP 已删
- [ ] 分发包已写入 Downloads（用户核验通过后同步 Grok 安装区）
