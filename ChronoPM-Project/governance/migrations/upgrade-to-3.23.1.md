# 升级到 3.23.1

> 从 3.23.0 升级到 3.23.1  
> 发布日期：2026-09-01  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260901-001  
> IA：IA-20260901-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.23.0 → 3.23.1。  
> 用户拍板：可以执行升级；每节点 annotated tag 并推远程；全部完成后再请用户核验。  
> contract_change：是（仅 Project SKILL.md §6 增升级路由行）。  
> **16 号 §4 豁免**：用户要求同一版本实施两件事——① V-14 拆分读取硬闸；② 双向升级提示词全文嵌入 16 家族。一张 CR。  
> 施工只认回归套件合计 **867**（基线 855 + Module 79 的 12 条）。

## 变更摘要

① Portfolio V-14 混报拆分：允许清单补禁止集与失败条件；+1 双锚点（目标日 → 最新合法日一份）；高置信 ≥5 / 差≥2 / C(P) 不降；拆分回执短；不改 Project 写入。  
② 开发仓：提示词全文嵌入 `references/16-upgrade-dual-agent.md`（源 2008 行）；SKILL.md §6 升级路由从工作区整份加载；用户开口不必报版本号（A 按 16 号 §10 拟定）；B 只在 AP 文末写 `## B{N} 审核结果`。分发包仍排除 16 家族。schema 0.16.0。双包同号 3.23.1。

## 施工禁区

- 禁止升 workspace schema；禁止新建 `references/24-*.md`
- 禁止抽独立升级 Skill；禁止 dual-agent 进分发包；禁止把 2008 行写进 SKILL.md
- 禁止改 Project `01`/`05`/`00`/`22`、skill-contract 正文、reply-norm
- 禁止降 V-14 高置信三项；禁止改打分权重
- 禁止 `portfolio/cache`；禁止集层写 `projects/*/ai`
- 禁止写入市监业务库
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）
- 迁入 dual-agent 禁止摘要化；禁止删辩论/四档结语/给 B 的包/共识状态/执行格式

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260901-001.md` | 一 CR（含 §4 豁免） |
| A1.2 | `governance-shared/impact-analysis/IA-20260901-001.md` | 一 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.23.1.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.23.1.md` | 锁步指针 |

### A2. 协议（节点2）

**① V-14**

- `ChronoPM-Portfolio/references/02-aggregation-query-rules.md` §12：允许集 + 禁止集 + 失败条件 + +1 双锚点 + 回执 + 不改 Project；禁止用 §1 读法凑打分
- `ChronoPM-Portfolio/SKILL.md`：V-14 实时读列与最小读取集补硬闸指针

**② 16 家族**

- 新建 `ChronoPM-Project/references/16-upgrade-dual-agent.md`：Downloads 提示词全文复制 + 允许补丁（加载声明、16 号路径、版本由 A 拟定、B 落盘 `## B{N} 审核结果`）
- `ChronoPM-Project/references/16-skill-governance-rules.md`：指针 + B 只写自己的节
- `ChronoPM-Project/SKILL.md` §6/§15：升级路由；整份加载；缺节失败；开发仓探测；与 skill-gap 分界；触发词不含「项目升级/系统升级」
- `tools/pack-skill/scripts/pack.ps1`：排除 `16-upgrade-dual-agent.md`

无引擎/脚本行为变更（版本源在 A4）。

### A3. 回归（节点3）

`ChronoPM-Project/tests/regression-suite.md` Module 79：DSP-004～007、UG-001～008。合计 **867**。  
核心契约声明：SKILL.md 增行不改已有业务用例期望；855 中 16 条按新期望，841 pass-through，发布跑全套。

阻断：DSP-002、DSP-004、DSP-005、DSP-006、UG-001、UG-002、UG-005、UG-006、UG-007、UG-008。

### A4. 版本触点（节点4）

`_version.py` 3.23.1 schema 0.16.0；`sync_version.py`；CHANGELOG 双包 + BLUEPRINT + 根 README×2（若写死用例数则 867）；Portfolio 锁步。`SKILL_MODULE_MAP.md` 无版本号，不改。

### A5. 基线与发布（节点5）

`baselines/3.23.1/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。禁止对市监跑 migrate。

## C. 节点完成勾选

- [x] A1 治理（`v3.23.1-step1`）
- [x] A2 协议（`v3.23.1-step2`）
- [ ] A3 回归（`v3.23.1-step3`）
- [ ] A4 版本（`v3.23.1-step4`）
- [ ] A5 基线（`v3.23.1-step5` / `v3.23.1`）
- [ ] 分发包（用户核验后再打；本节点不代装 Grok）
- [ ] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [ ] 双包 3.23.1；schema 0.16.0
