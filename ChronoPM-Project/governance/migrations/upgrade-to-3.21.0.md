# 升级到 3.21.0

> 从 3.20.0 升级到 3.21.0  
> 发布日期：2026-08-30  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260830-001～003  
> IA：IA-20260830-001～003  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.20.0 → 3.21.0。  
> 用户拍板：执行升级；每节点 annotated tag 推 origin 与 github；全部完成后再请用户核验。  
> 方案：`upgrade-plan-v3.21.0.md` **V0.6**（B4 通过-可施工；B3/B2 待修订已闭合）。  
> contract_change：是（SKILL.md + 00）。按 16 §4 拆 **3** 个 CR。施工只认回归 **807**（基线 777 + Module 75 新增 30）。

## 变更摘要

单项目百科叠层：懒建 `logs/journal/`、`context/brain.md`、`context/active-entities.json`、`ai/.state.json`。`refresh_views.py` 读 `view-spec.json` 生成全部派生视图（脚本优先，无 Python 则 AUTO 兜底）。纠偏只写事实/词库；查询 L0–L3；日报默认更新活实体。跳版本不升 schema。双包同号 3.21.0。

## 施工禁区

- 禁止升 workspace schema；禁止改 `wps/_index` 列数与 WP 模板列
- 禁止新建 Project `references/NN-*.md`
- 禁止改 pm-decisions 八块；禁止改 `skill-contract.md` 正文
- 禁止引入 git 到业务工作区
- 禁止写入市监业务库（ALI-001 只读抽查）
- 禁止清空 00 §8a 实体级联
- 禁止 JSON 可写 `corrections`；口径家=词库 §2
- 禁止 brain 含待拍板节
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）
- 禁止 Portfolio 写 `projects/*/ai`；本包 Portfolio 仅版本锁步

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260830-001.md`～`003.md` | 三 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260830-001.md`～`003.md` | 三 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.21.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.21.0.md` | 仅锁步指针 |

### A2. 引擎（节点2，CR-001）

`scripts/view-spec.json`；`scripts/refresh_views.py`（`--check-spec`、原子 replace、分视图 status、先 parse WP 再写 index/json）；`assets/templates/journal-entry-template.md`；`tests/fixtures/qlt-wp-20260827-001-fp.md`；`ALL_TEMPLATE_FILES` 增 journal 模板。

### A3. 协议（节点3，CR-002）

SKILL.md §3 懒建名单、§5.1b P-VIEWS、§7 铁律；00 脚本优先+P-CORRECT+P-RESOLVE；05 brain/L0–L3；10 默认更新；23 三过程；06/11/17/20/14 短改。

### A4. 回归（节点4，CR-003 测试段）

`tests/regression-suite.md` Module 75。合计 **807**。阻断：SK-002、TW-003、SP-001、ALI-003、UPD-002、COR-001/004/005、SCH-001、BRN-003。

### A5. 版本触点（节点5，CR-003 版本段）

`_version.py` 3.21.0 schema 0.16.0；`sync_version.py`；CHANGELOG 双包 + BLUEPRINT AD-10 + 根 README×2 回归 807；`migrate_workspace.py` VERSION_CAPABILITIES 一条 encyclopedia_overlay、new_dirs=[]。

### A6. 基线与发布（节点6）

`baselines/3.21.0/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。市监只读核 ALI-001 fixture，不写盘。
