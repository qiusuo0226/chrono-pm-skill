# 升级到 3.23.0

> 从 3.22.0 升级到 3.23.0  
> 发布日期：2026-08-31  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260831-005  
> IA：IA-20260831-005  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.22.0 → 3.23.0。  
> 用户拍板：执行升级；每节点 annotated tag；全部完成后再请用户核验。  
> contract_change：是（SKILL.md + 00 + skill-contract #5）。单一目标一张 CR。施工只认回归套件合计行（基线 **830** + Module 78）。

## 变更摘要

堵住 3.21/3.22 已建层的消费洞：确认分级驱动生效与横幅（低/中风险 `Confirmed By: auto`，不进块 8 子节「已经写了等点头」）；主路径不阻断；查询默认不灌 entities 全文；决策/需求标题进现有 alias；brain 投影 ops 摘要；Portfolio 汇总带 as-of。不新建平行索引/快照/缓存/会话事实源。schema 0.16.0。双包同号 3.23.0。

## 施工禁区

- 禁止升 workspace schema；禁止新建 Project `references/NN-*.md`
- 禁止 `query-index.md` / 场景 memo / `active-entities-hot|cold` / `session-log` / `portfolio/cache`
- 禁止确认级别改名 L0–L3；禁止 24h 沉默生效；禁止 `sweep_pending()` 进 refresh_views
- 禁止切 `update_mode: passive`；禁止把历史日能耗回写一并 auto 化
- 禁止改 22 号（无旧口径）
- 禁止写入市监业务库；禁止 `reply-norm-skill/SKILL.md`
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）
- 禁止 Portfolio 写 `projects/*/ai`

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260831-005.md` | 一 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260831-005.md` | 一 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.23.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.23.0.md` | 锁步指针 |

### A2. 引擎（节点2）

- `scripts/refresh_views.py`：entities 紧凑写出 + count；parse 决策标题/需求标题进 alias；brain 最近过程 + 别名短表排序；ops `_index` 进指纹；TDs 编号序截 80
- `scripts/view-spec.json`：`brain_fact_globs` 增 `logs/ops/_index.md`

### A3. 协议（节点3）

00 §3.1/§3.3/L342/§8b.3/WF-1 五行/L204；SKILL description/§4/底线#2/§5.3；skill-contract #5；05 §0/§1a/§2/B-18；01/06/07/10/14/19/21；相关模板；Portfolio 02 as-of + L16/L21。口径 SSOT = 00 §3.3。

### A4. 回归（节点4）

`tests/regression-suite.md` Module 78 + 改 PW-001/002、V3-021、V3-019、UT-001。examples/03 横幅。

### A5. 版本触点（节点5）

`_version.py` 3.23.0 schema 0.16.0；`sync_version.py`；CHANGELOG 双包 + BLUEPRINT + 根 README×2；Portfolio 锁步。

### A6. 基线与发布（节点6）

`baselines/3.23.0/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。禁止对市监跑 migrate。存量块 8 不自动清。

## C. 节点完成勾选

- [x] A1 治理（`v3.23.0-step1`）
- [x] A2 引擎（`v3.23.0-step2`）
- [x] A3 协议（`v3.23.0-step3`）
- [x] A4 回归（`v3.23.0-step4`）
- [x] A5 版本（`v3.23.0-step5`）
- [x] A6 基线（`v3.23.0-step6`）
