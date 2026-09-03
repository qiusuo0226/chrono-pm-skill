# 升级到 3.24.0

> 从 3.23.1 升级到 3.24.0  
> 发布日期：2026-09-03  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260903-001  
> IA：IA-20260903-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.23.1 → 3.24.0。  
> 用户拍板：开始执行升级；每节点 annotated tag 并推远程；直到完全升级完。  
> contract_change：是（Portfolio SKILL.md 路由+默认句）。  
> 施工只认回归套件合计 **877**（基线 867 + Module 80 的 10 条）。

## 变更摘要

集层材料投喂默认：识别 → 无条件落 `portfolio/reports/ingest/{batch}/`（原件+抽出行）→ 写集层日志 → 按已有 V-14 / 05+04 / V-4 / V-8 / V-11 分类。仅成员项目实体走 V-9 白话拍板。禁止问要不要落库。不新增 V-15，不升 schema，不代写 `projects/*/ai`。Project 01 收下句扩人员/资源，人员类仍走 00 确认级。双包同号 3.24.0。

## 施工禁区

- 禁止升 workspace schema；禁止新建规则文件 / V-15 / 新目录
- 禁止集层写 `projects/*/ai`；禁止 `portfolio/cache`
- 禁止把 ingest rows 当花名册查询源
- 禁止改 00 确认矩阵；人员事实确认级不降
- 禁止放宽 02 §12 V-14 硬闸（禁回溯旧 ingest/旧分发稿）
- 禁止新建 Portfolio `SKILL_BLUEPRINT.md`
- 禁止改 `daily-dispatch-template.md` 文件名
- 禁止缺口自动落盘（只提示，点头才落）
- 禁止把纯查询做成强制 ingest
- 禁止写入市监业务库
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260903-001.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260903-001.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.24.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.24.0.md` | 锁步指针 |

### A2. 协议（节点2）

**Portfolio 01 §2.1 投喂统一入口**

- 首段：本条为 V-14 / 04 / 05 / V-8 / V-11 的前置；落原件+rows 后，表类仍走 02 §13，散文仍走 V-14 打分或 05；不重新打分、不替代 §13 槽位、不替代 V-14 打分与硬闸
- 判定：材料投喂走本条；纯查询 / `1A；2B` / 收编选项不 ingest
- 步骤：原件 → rows → 日志 → 分类 → 需改成员才 V-9
- 可写≠拍板：portfolio ingest/分发稿/日志默认写；成员实体才拍板
- 同会话同一原文 → 指向已有 batch，不复制
- 写盘失败如实报已写入部分，禁止谎报已存
- 回执：先报已存路径；再报 N 件事回编号；禁止「要不要落库 / 要不要记住」
- §3：portfolio 落库不进 V-9 待确认

**Portfolio SKILL.md**

- §2 补投喂默认句
- §7：新增「材料投喂」行 `01（先 §2.1）`；「共享人力/流转/资源漂移」→ `01（先 §2.1）+05`；「混报分发/弱结构投喂/进度表入库」→ `01（先 §2.1）+02`；「共享文件拆分」→ `01（先 §2.1）+02`；意图变更行不重复改加载集
- §9「另」补禁止问落库
- §10：01 加载说明含投喂入口

**Portfolio 02 / 04 / 05**

- 02 §12：拆分前先 01 §2.1；分发稿本轮可写（待收下）；低置信只问归属；硬闸一字不放宽
- 02 §11：发现缺口主动提示记升级需求；点头才落盘
- 04 §5 首句：投喂类资源变动先 01 §2.1
- 05：人员/排期投喂先 01 §2.1，禁止只摘要；index 仍禁排期数值；**§2a 外部工时表显式挂先 01 §2.1**

**模板**

- `daily-dispatch-template.md`：注释改为全投喂分发；「日报」措辞改「投喂分发」；`doc_type` 与文件名不改；落点列允许 `_index` / §0.5

**Project 01**

- 落点回执（约 L315）：集层分发稿含人员/资源；点名本项目则收下；人员类分发仍走 00 确认级；不问要不要记住；禁止写入稿里他项目段落

**示例**

- `examples/13-项目集总览.md`：增一轮人员排期投喂（先存 ingest+日志，再白话拍板，无「要不要落库」）
- `examples/05-一份材料拆到多个项目.md`：助手第一句补「原件已存集层 ingest/{batch}」，再问分法；不要加「要不要落库」问答

无引擎/脚本行为变更（版本源在 A4）。

### A3. 回归（节点3）

`ChronoPM-Project/tests/regression-suite.md` Module 80：ING-010～017、DSP-008、EX-013。合计 **877**。

阻断：ING-010、ING-012、ING-013、ING-015、DSP-002、DSP-004、DSP-006、UG-001、UG-002、UG-005、UG-006。

既有 ING-001～009、FED-001、DSP-001 期望不回退；DSP-001 / FE-008 加强为必须有 ingest。

### A4. 版本触点（节点4）

`_version.py` 3.24.0 schema 0.16.0；`sync_version.py`；CHANGELOG 双包须显式 `Blueprint Impact: full`；Project `SKILL_BLUEPRINT.md` Minor 必更（投喂入口一句+版本）；不新建 Portfolio Blueprint。根 README×2 若写死用例数则 877。Portfolio 锁步。

### A5. 基线与发布（节点5）

`baselines/3.24.0/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。禁止对市监跑 migrate。

## C. 节点完成勾选

- [x] A1 治理（`v3.24.0-step1`）
- [x] A2 协议（`v3.24.0-step2`）
- [x] A3 回归（`v3.24.0-step3`）
- [x] A4 版本（`v3.24.0-step4`）
- [x] A5 基线（`v3.24.0-step5` / `v3.24.0`）
- [x] 分发包（Downloads；Grok 安装区不代更）
- [x] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [x] 双包 3.24.0；schema 0.16.0
