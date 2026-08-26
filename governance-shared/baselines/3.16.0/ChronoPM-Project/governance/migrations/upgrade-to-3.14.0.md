# 升级到 3.14.0

> 从 3.13.0 升级到 3.14.0  
> 发布日期：2026-08-25  
> Schema 变更：workspace schema **0.14.0 → 0.15.0**（新增 `ai/project-info/`）  
> CR：CR-20260825-001  
> IA：IA-20260825-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.13.0 → 3.14.0。  
> 用户拍板：终版可执行；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。B 审核：V0.4 **通过-待修订**（E-01～E-09 已写入本文件，施工时执行）。

## 变更摘要

计划 §3 去子行、新增 §4 阶段列表（6 节）；WP §8 改为 13 标准阶段表；新 PLAN/WP 编号 `PLAN/WP-YYYYMMDD-NNN`（存量不重编）；`budget.md`/`progress-plan.md` 迁到 `project-info/`；删除 `is_milestone`，改为 §8 关键阶段；P-WP-SCAN 增量+冻结；查看计划=闸 2 写回后输出完整 MD。双包同版本 3.14.0。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径（含市监重构项目管理）
- 禁止改待办核心表 8 列（阶段只写备注区）
- 禁止 WP §8 回写待办 Owner/日期（P-BOX 询问除外）
- 禁止用关键阶段自动生成计划 §2
- 禁止改 WP §2 关联需求 / §3 阶段明细 / §3b / §5 / §6 现网含义
- 禁止 07「关联里程碑」改成填阶段名（仍存 WP 编号）
- 禁止计划第 7 列；禁止 index 第 9 列
- 禁止 `status: 废弃`（生效用 `effect`）
- 禁止全库扫（日常 SCAN 只增量）；升级全量按 WP Ref，不按计划时间窗
- 禁止把非 `PLAN-*.md` 当正式计划插入 §4
- 禁止按 §12 旧短表施工（**只认本文件 + AP 的 §25**）

## E 项（B3 施工必改，写入本文件即闭环）

| # | 项 | 落点 |
|---|---|---|
| E-01 | WP §8 阶段名映射前先剥 `（完成）` `（当前）` | 本文件 B 节 + 00 §8d |
| E-02 | A2/A3 重算以冻结表为准：日常读范围内无未办结 → ✅ 并冻结 | 00 §8d |
| E-03 | 文件清单以本文件 A 节为准 | — |
| E-04 | 07 关联里程碑仍存 WP 编号 | 07 号 |
| E-05 | 改计划 §2 不回写 WP 关键阶段 | 00 §8c |
| E-06 | 23 号必须改 P-WP-SCAN（投影 §4，备注阶段） | 23 号 |
| E-07 | D-NEW-2：🔄 必须有人；⏳ 显式待安排 | 14 号 |
| E-08 | 未映射清单交 PM，不用 80% 门槛 | 本文件 B |
| E-09 | 看计划=盘上全文，禁止「展开」代替文件 | 05 §6.7 |

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260825-001.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260825-001.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.14.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.14.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.14.0.md` | 指针文件 |

### A2. 核心规则（节点2）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | 闸 2 对账 §3/§4 与 WP §8，移出 §3+§4+§6，先写回再答，查看=全文；§4b 6 节无子行；§5a 13 阶段+映射+同义词最长匹配+剥后缀+点名；§5b 里程碑=关键阶段，M01-M12 仍为项目框架；§8b.0 新号 YYYYMMDD-NNN、存量不重编；§8c/8c.2 子行→§4、§5→§6；§8d SCAN 增量+冻结/解冻/重算表，删子行规则；WF-7 6 节无子行；WF-8 备注区 `阶段：` |
| A2.2 | `23-procedure-index.md` | P-WP-SCAN：Writes 含备注阶段+§8 冻结；投影正常计划 §4；Forbidden 覆盖点名/全库扫；删「子行」 |
| A2.3 | `06-file-rules.md` | **§1.1 允许目录加 project-info**；§1.3 树加 project-info、计划 6 节；§2.1 `project-info/budget.md` `project-info/progress-plan.md`；§6.2 PLAN 6 节无子行、WP 编号新格式、index 是否里程碑→关键阶段仍 8 列 |
| A2.4 | `14-self-check-rules.md` | D35 6 节；D38 父行+§4 列表；D-NEW-1～4（D-NEW-2=🔄 必须有人，⏳ 显式待安排） |

### A3. 模板（节点3）

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `plan-template.md` | §3 无子行 6 列（关键阶段）；新增 §4 阶段列表；原 §4 风险→§5；原 §5 变更→§6；6 节；编号 PLAN-YYYYMMDD-NNN |
| A3.2 | `wp-template.md` | 删 is_milestone；§1 删是否里程碑；§8 13 阶段 5 列表（点名写执行人格）；§4 口径含已办结（查看/谁参与过）；不改 §2/§3/§3b/§5/§6 |
| A3.3 | `wp-index-template.md` | 「是否里程碑」→「关键阶段」；仍 8 列；新号注释 |
| A3.4 | `personal-daily-todo-template.md` | §1.4 备注区加 `阶段：{名} / —` |
| A3.5 | `project-brief-template.md` | budget→project-info/budget.md；里程碑路由改关键阶段 WP |

### A4. 辅助规则与契约（节点4）

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | `SKILL.md` | 目录加 project-info；事实源路径；ID 编码新 PLAN/WP；§9–14 里程碑=关键阶段 |
| A4.2 | `05-query-rules.md` | §6.7 看计划=闸 2 写回后全文；还差谁读盘上 §4；budget 路径；is_milestone 查询改关键阶段 |
| A4.3 | `01/02/08/10/11/12/13/18/19` | `plans/budget.md`→`project-info/budget.md`；`plans/progress-plan.md`→`project-info/progress-plan.md`；里程碑口径 |
| A4.4 | `07-requirement-rules.md` | 「关联里程碑」**仍存 WP 编号**，语义=含关键阶段的 WP |
| A4.5 | `20-workspace-version-rules.md` | schema 0.15.0 健康检查：存在 `project-info/` |
| A4.6 | `skill-contract.md` | 事实源路径；现行 schema 0.15.0 |
| A4.7 | `index-formats.md` | 关联里程碑列注释（仍 WP 编号） |

### A5. Portfolio（节点5）

| # | 文件 | 动作（写死） |
|---|---|---|
| A5.1 | Portfolio `SKILL.md` | V-7 路径 project-info/budget.md |
| A5.2 | `01-readonly-boundary-rules.md` | 里程碑=WP §8 关键阶段=是 |
| A5.3 | `02-aggregation-query-rules.md` | is_milestone→关键阶段；budget 路径 |
| A5.4 | `05-resource-shared-rules.md` | plans/budget.md→project-info/budget.md |
| A5.5 | `portfolio-weekly-template.md` | budget 路径 |

### A6. 脚本与回归（节点6）

| # | 动作（写死） |
|---|---|
| A6.1 | `config.py`：SINGLE_PROJECT_DIRS 加 project-info；FACT_SOURCE 两文件改路径 |
| A6.2 | `file_registry.py`：树与 brief 路由 |
| A6.3 | `workspace_builder.py`：提示文案 |
| A6.4 | `migrate_workspace.py`：VERSION_CAPABILITIES 补 3.13.0 + 3.14.0（new_dirs=project-info）；脚本只建空目录，不搬业务文件；打印迁文件指引 |
| A6.5 | 回归：WP-005 翻盘；PLT-001/002 6 节；PWP-008 §6；WPL 子行→§4；新增模块 69（STP 阶段/目录/编号/看计划） |

### A7. 版本触点（节点7）

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | `scripts/_version.py` | SKILL_VERSION=3.14.0；WORKSPACE_SCHEMA_VERSION=0.15.0 |
| A7.2 | 跑 `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | skill.json | supportedWorkspaceSchema.current=0.15.0；migrations 0.14.0→0.15.0；versionHistory |
| A7.4 | CHANGELOG 双包 | 3.14.0 段 |
| A7.5 | BLUEPRINT 演进表 + MODULE_MAP | 3.14.0 行；子行改 §4 |
| A7.6 | README.md / README.en.md | 版本与用例数 |
| A7.7 | examples 09/10（若含旧路径/子行/5 节） | 对齐 |

### A8. 基线与发布（节点8）

| # | 动作（写死） |
|---|---|
| A8.1 | `baselines/3.14.0/` 双子树全量快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每完成一个节点：annotated tag（中文）推 origin 与 github |
| A8.4 | 删除 `output/upgrade-plan-v3.14.0.md` 及 B 审核草稿（基线拍完后） |
| A8.5 | 全部完成后请用户核验；不提前替换 Grok skills / 不提前打分发包 |

---

## B. 业务工作区

**本发布不代做任何业务仓。** 存量由该项目对话按下列规则懒迁/触碰。

| 对象 | 方式 |
|---|---|
| 计划升级 | **只处理**文件名 `PLAN-*.md` 且头 `doc_type: plan`。`国庆上线计划.md` / `dev-freeze-plan.md` 只出清单 |
| PLAN §3 子行 | 闸 2 / 升级程序：删子行，从 WP §8 生成 §4；原 §4 风险→§5；原 §5 变更→§6 |
| WP §8 旧阶段名 | 先剥 `（完成）` `（当前）`，再按下表映射；未映射保留原名+⚠️待校准，清单交 PM，禁止猜 |
| 无 is_milestone | 不当关键阶段 |
| is_milestone=true | 链尾或「上线」标关键阶段=是；删字段 |
| 无 effect | 触碰补 `effect: 正常` |
| 中文/短号 | 不重编 |
| budget/progress-plan | 工作区 migrate：建 `project-info/`；有旧文件则 AI 清单→PM 确认后移动（脚本不自动搬） |
| 查看 WP 谁参与过 | 含已办结；优先读 §8 已落盘人期 |

### 存量阶段名映射

| 旧 | 新 |
|---|---|
| 待确认 | 需求登记 |
| 需求已规划 | 需求规划 |
| 已需求评审 | 需求评审 |
| 已设计评审 | 方案设计 |
| 已测试用例评审 | 用例设计 |
| 开发中 | 开发 |
| 预演 | 预演 |
| 测试中 | 测试 |
| 内部验收中 | 内部验收 |
| 试运行 | 试运行 |
| 上线 | 上线 |
| （无） | 插入 需求调研、需求确认为 ⏳ |

插入「需求调研」「需求确认」为 ⏳ 待安排。

## C. 验证检查

- [x] `_version.py` 3.14.0 / 0.15.0
- [x] 06 §1.1 允许目录含 project-info
- [x] plan-template 6 节、§3 无子行、§4 阶段列表
- [x] wp-template 无 is_milestone；§2 仍为关联需求；§8 13 阶段
- [x] wp-index 仍 8 列，关键阶段列
- [x] 待办模板备注含 `阶段：`
- [x] 23 P-WP-SCAN 无「子行」
- [x] grep `plans/budget.md` 双包 = 0（升级文档除外）
- [x] grep `is_milestone` 规则/模板 = 0（升级文档除外）
- [x] WP-005 预期=新号合法
- [x] PLT-001 预期=6 节
- [x] audit_release 退出码 0
- [x] 无业务仓路径写入
- [x] 正式文档不引用 upgrade-plan 路径

## 发布收尾（强制）

- [ ] 删除本版 AP 草稿 `output/upgrade-plan-v3.14.0.md` 与 B 审核草稿（须用户核验通过后）
- [ ] CHANGELOG 登记
