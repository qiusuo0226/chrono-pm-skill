# 升级到 3.25.0

> 从 3.24.0 升级到 3.25.0  
> 发布日期：2026-09-04  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260904-001  
> IA：IA-20260904-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.24.0 → 3.25.0。  
> 用户拍板：开始执行升级；每节点 annotated tag 并推远程；直到完全升级完再交用户审核。  
> contract_change：是（Portfolio 只读五条手递例外；00 §3.3 / skill-contract #5「跨项目镜像」拆口径）。  
> 施工只认回归套件合计 **891**（基线 877 + Module 81 的 14 条）。

## 变更摘要

集层投喂闭环到成员项目事实源：感知 → 拆解 → 落 ingest → 同会话按白名单调用 ChronoPM-Project 写过程（P-HANDOFF-WRITE → P-HANDOFF-ACCEPT）。日报 inbox→C'；当日能耗 01 §1.6；源文档 P-SPLIT；确认后人员走 01 L315；风险走 04 判定卡；合同登记走 07 §8.9。低置信只问归属；高风险仍确认。禁止手递 pm-profile。Portfolio 工人不手搓成员正文。不新增 V-15，不升 schema，不新规则文件。双包同号 3.25.0。

## 施工禁区

- 禁止升 workspace schema；禁止新建规则文件 / V-15 / 新目录
- 禁止 Portfolio 自拟 `{owner}.md` / 登记册格式（可写≠代写）
- 禁止手递 `pm-profile.md` / `current_operator`
- 禁止未确认写花名册 §1 / 进出组 §0.5
- 禁止跳过 04 判定卡静默登风险册
- 禁止放宽 02 §12 V-14 硬闸
- 禁止把人员进出组/里程碑/成本降为直接落库
- 禁止新建 Portfolio `SKILL_BLUEPRINT.md`
- 禁止改 `daily-dispatch-template.md` 文件名
- 禁止缺口自动落盘；禁止纯查询强制 ingest
- 禁止写入市监业务库
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）
- Grok 安装区不代更

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260904-001.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260904-001.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.25.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.25.0.md` | 锁步指针 |

### A2. 协议（节点2）

**Portfolio 01 新 §2.2 P-HANDOFF-WRITE（Home）**

- 前置：§2.1 已完成。不替代 V-14 打分、不替代 §13 槽位、不放宽 §12 硬闸
- 白名单（不在名单=禁止手递）：日报/过程待办→01 inbox；当日能耗→01 §1.6；源文档→P-SPLIT；人员/资源（先 V-9）→01 L315；风险→04 判定卡；合同登记→07 §8.9
- 禁写：pm-profile / current_operator；里程碑/成本/删除覆盖；未登记成员
- 步骤 1–8：已登记成员 → project-root=该成员根 → 加载兄弟包写侧 → 缺日目录则 P-CARRY → 5a–5f 分派 → 幂等 → 分发稿 status 已手递 → 按项目分次或子 agent
- Forbidden：跳过 inbox；写兄弟项目；镜像 A→B；谎报；未确认改花名册；跳过判定卡登册

**Portfolio SKILL.md**

- description：删「禁止写入成员项目事实源」绝对句；改为归集只读 + 投喂感知 + 高置信低/中风险同会话调用 Project；高风险仍确认
- 触发词补：投喂、粘贴、xlsx、csv、日报、进度表、混报、排期、分发、入库、同步到各项目
- §1：投喂由本包发起、成员写盘走 Project 过程
- §2：viewer = 工人不手搓成员正文；该写的段落同会话手递
- §4 / §9 只读五条：工人零写；手递须 CALL Project。**保留** §4 条 3 后半：集层「我是张三」禁止写各子项目 pm-profile
- §6 V-9/V-11/V-14：永不代写；手递须 CALL Project
- §7：投喂/混报/排期/拆分/风险 行追加手递加载集（日报 00+01+06+17+22；人员 00+01+06+22 敏感先 V-9；风险 00+04；拆文件=源文档行；合同 00+07 §8.9）
- 「细则不得跨包引用」→ 禁止复制 Project 规则进本包；手递时加载兄弟包对应路由，root=该成员根
- §8：低/中风险高置信投喂不走 V-9，走 §2.2

**Portfolio 02 / 04 / 05**

- 02 §12 L167：删「直接写进各项目 → 拒绝」；高置信 CALL §2.2；低置信只问归属；status 走新枚举。硬闸一字不放宽
- 02 回执示例：成员路径，禁止「请换对话说收下」完成句
- 02 §13：成员 original 在 §2.2 手递之后
- 05：排期确认后 CALL §2.2 / 01 L315，不换对话；§2a 当日能耗允许手递 01 §1.6
- Portfolio 04：资源投喂先 §2.1，再按 00 分级手递或拍板（指针 §2.2）

**Project**

- SKILL.md description/§2：允许被集层手递调用；仍禁写兄弟项目与 portfolio/
- 01：极短「集层手递入口」+ 幂等（已手递 batch 不重复收下）；人员仍用 L315
- 23：P-HANDOFF-ACCEPT 一行，Calls=5a–5f，摘要 ≤200 字
- 04 / 07 §8.9：各一句 callee 指针，不改确认级
- 10：一句，跨项目材料归 Portfolio 01 §2.1 感知
- 00 §3.3：`跨项目写入` → `跨项目镜像`；直接落库格补集层手递日报/过程待办/当日能耗。人员进出组不降级
- skill-contract #5 与 00 同步

**模板 / 示例**

- `daily-dispatch-template.md`：status 默认 `待归属`；手递后 `已手递`；删「请到对应项目对话说收下」；不改文件名
- `suggested-update-list-template.md`：选项 A = 本对话确认后立刻手递
- examples/05：删 2B「我不会这么干」；分法确定后演示 P-SPLIT 给路径
- examples/13 第 3 轮：`1A；2A` 后同会话手递走 01 L315；查询轮不改

无引擎/脚本行为变更（版本源在 A4）。结转复用既有 `carryover_step0.py`。

### A3. 回归（节点3）

`ChronoPM-Project/tests/regression-suite.md` Module 81：HO-001～014（14 条）。合计 **891**。人员手递正例由 ING-011 翻转承担。

阻断：HO-001、HO-004、HO-006、HO-008、DSP-006、DSP-004、ING-010、ING-012、UG-001、UG-002。

旧期望翻转：DSP-002、ING-005、ING-011、DSP-001/008、DSP-004、ING-006。ING-015 保持拒绝静默写花名册。

既有 ING-010/012/013、DSP-006、UG-001/002/005/006、V-14 门槛、FED-001/002 不回退。

### A4. 版本触点（节点4）

`_version.py` 3.25.0 schema 0.16.0；`sync_version.py`；CHANGELOG 双包须显式 `Blueprint Impact: full`；Project `SKILL_BLUEPRINT.md` Minor 必更（手递一句+版本行）；`SKILL_MODULE_MAP.md` G1/G6/G8/G11/G14/G19 补手递实线。不新建 Portfolio Blueprint。根 README×2 用例数 **891**。Portfolio 锁步。

### A5. 基线与发布（节点5）

`baselines/3.25.0/` 双子树；`audit_release.py` 退出 0；删除 AP 草稿。分发包落 Downloads；Grok 安装区不代更。

---

## B. 业务工作区

开发仓无业务 `ai/wps/` → **B 节 skip**。禁止对市监跑 migrate。

## C. 节点完成勾选

- [x] A1 治理（`v3.25.0-step1`）
- [x] A2 协议（`v3.25.0-step2`）
- [x] A3 回归（`v3.25.0-step3`）
- [x] A4 版本（`v3.25.0-step4`）
- [x] A5 基线（`v3.25.0-step5` / `v3.25.0`）
- [x] 分发包（Downloads；Grok 安装区不代更）
- [x] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [x] 双包 3.25.0；schema 0.16.0
- [x] 收尾（`v3.25.0-close`）：用户核验通过；P2 幽灵编号 EX-014/015 已改为 HO-001～014（14 条）；Grok 不代更；归档施工核对
