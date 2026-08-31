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
- [ ] A6 基线 + audit + 删 AP（`v3.22.0-step6` / `v3.22.0`）
