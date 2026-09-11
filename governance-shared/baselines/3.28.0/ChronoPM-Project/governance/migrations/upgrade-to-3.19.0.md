# 升级到 3.19.0

> 从 3.18.0 升级到 3.19.0  
> 发布日期：2026-08-27  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260827-006～009  
> IA：IA-20260827-006～009  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.18.0 → 3.19.0。  
> 用户拍板：执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V0.3（B1 通过-可执行 / B2 通过-待修订，A 已消化至 V0.3）。  
> 按 16 §4 拆 **4** 个 CR。施工只认回归 **729**（706+23；以 Module 73 落地统计为准）。

## 变更摘要

工作包图按 `related_wps` 有无分横排/竖排，超长链 `graph TD` + 行子图 `direction LR` + 子图级跨行边；skill-gap 废 `rev-NNN`、单文档原位迭代与废弃；WP 删「阶段明细」，§3b 改名为 WP §3（功能点）并加阶段留痕；确认落地后不回放已裁定、开放项 N=0 不横幅。双包同号 3.19.0。schema 0.16.0。

## 施工禁区

- 禁止升 workspace schema；禁止搬 `wps/WP-*.md`
- 禁止新建 `references/NN-*.md`
- 禁止图走 P-OUTPUT / `ai/outputs/`
- 禁止给 WP 功能点**当前表**加执行人列（S6）
- 禁止 skill_gap 再写 `revisions/rev-NNN.md`；禁止误删周报 revisions
- 运行时禁止裸写「§3」指功能点，必须写「WP §3（功能点）」
- 历史 upgrade-to / 旧 CHANGELOG 段的 §3b **不改**
- 正式文档不得引用 upgrade-plan 草稿路径
- 禁止写入业务工作区（开发仓无 `ai/wps/` 则 B 节 skip）
- 00 的 CR-C 与 CR-D 改动同一波次写完再测，禁止先发一半 00

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260827-006.md`～`009.md` | 四 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260827-006.md`～`009.md` | 四 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.19.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.19.0.md` | 指针 |

### A2. 图排列（节点2，CR-006）

见 CR-006。11 §17.2 / §17.2.1 A～F；`wp-chart-template` 四形态；05 画图行指针；23 P-WP-CHART 红线；8c.2 结构闸。指纹不变。子图级边不计指纹。

### A3. skill-gap 原位与废弃（节点3，CR-007）

见 CR-007。废 skill_gap 的 rev-NNN；原位+迭代记录；定向扫描；废弃状态；11 §5.3/§5.4/L31 仅非 skill_gap；10 去 7 日窗。周报 revisions 保留。

### A4. WP §3（功能点）+ 确认后不回放（节点4，CR-008+009）

见 CR-008 / CR-009。**00 本节点一次写完。** 删阶段明细与 L24 头注；§3b→WP §3（功能点）+ 留痕（含来源 TD）；全库运行时用词；D9：落地后不回放、不混节、横幅整轮一份、N=0 无横幅。

### A5. 回归（节点5）

`tests/regression-suite.md` Module 73。改写 WPC-008/WPR-004/SKG-005/WPR-014/PU-001；新增 WPC-012～019、SKG-013～018、WPS-013～016、RN-005～009。合计 **729**。

### A6. 版本触点（节点6）

| # | 文件 | 动作 |
|---|---|---|
| A6.1 | `_version.py` | 3.19.0；schema 0.16.0 |
| A6.2 | `sync_version.py` | 双包触点 |
| A6.3 | CHANGELOG 双包 + BLUEPRINT + 根 README×2 | 3.19.0；回归 **729**；历史段 §3b 不改 |
| A6.4 | `migrate_workspace.py` VERSION_CAPABILITIES | 3.19.0 schema 0.16.0 |
| A6.5 | Portfolio：`assets/templates/skill-gap-demand-template.md` 字段锁步 + 02/06 用词。**禁止**建 `ChronoPM-Portfolio/skill-gap-skill/`（有意省略：集层只拷模板，规则权威在 Project） |

### A7. 基线与发布（节点7）

| # | 动作 |
|---|---|
| A7.1 | `baselines/3.19.0/` 双子树 |
| A7.2 | `audit_release.py` 退出 0 |
| A7.3 | 每节点 annotated tag 推 origin 与 github |
| A7.4 | 终 tag `v3.19.0` |
| A7.5 | 删除 AP 草稿；分发包；全部完成后再请用户核验 |

---

## B. 存量工作区

开发仓无 `ai/wps/` → **skip**。

有 `ai/wps/` 的业务仓（升级对话中执行，不在本开发仓写业务文件）：

1. 扫描 `## 3b.` → 改标题为 `## 3. 实体/功能点行`（WP §3（功能点））。运行时两种标题都认，直到改完。
2. 原 `## 3. 阶段明细`：无数据则删；有正文则改名为「历史阶段明细」，不删内容。
3. 存量 skill_gap：`revisions/rev-NNN.md` 合并入主文档「八、迭代记录」后删除修订文件；证据迁 `assets/`。
4. 可选：扫描需求池，Skill 已包含的标 `status=deprecated` + index「已废弃」。找不到或用户已删 → 不动作。
5. 下次 P-WP-CHART 按新排列覆盖 `_wp-chart.md`。

验证：改标题数量核对 + 抽样；rev 合并后批次内无 `revisions/rev-NNN.md`。

---

## C. 验证检查

- [x] `_version.py` 3.19.0 / schema 0.16.0
- [x] 11 §17.2 横/竖 + §17.2.1 A～F；§5.3 skill_gap 例外
- [x] gap-capture 无 rev-NNN；有原位/废弃/定向扫描
- [x] wp-template 无阶段明细；`## 3.` 为功能点+留痕
- [x] 运行时「WP §3（功能点）」；历史 CHANGELOG 段保留 §3b
- [x] 00 §5.0 D9；N=0 无横幅
- [x] 回归 729；audit 17/17 退出 0
- [x] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [x] 双包 3.19.0
- [x] planning/ 仅留 README；本版 AP 已删
- [x] 分发包已写入 Downloads（用户核验通过后同步 Grok 安装区）
