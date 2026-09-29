# 升级到 3.15.0

> 从 3.14.0 升级到 3.15.0  
> 发布日期：2026-08-25  
> Schema 变更：workspace schema **0.15.0 → 0.16.0**（pm-profile 增 `current_operator`；升级契约含存量数据受控迁移）  
> CR：CR-20260825-002  
> IA：IA-20260825-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.14.0 → 3.15.0。  
> 用户拍板：分步执行；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V0.11。

## 变更摘要

存量受控迁移（dry-run/回滚/幂等/只投影）；计划 §4 模板含执行人排期；skill_gap 单文件（仅该 Type 不建 manifest）；current_operator（空则 ASK）；AP/examples/收尾治理；Python ≥3.9 引导；四套 verify（P0 挂 19 号）；日报路由载 22 + 投喂全员结转（人人一份 §1 可空）；init README `{编号}` 转义。双包 3.15.0。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径（含市监重构项目管理）
- 禁止 11 号 §3 默认结构删除 manifest（仅 skill_gap 例外）
- 禁止 current_operator 空时回退 pm_name
- 禁止 Portfolio AUTO 写子项目 pm-profile
- 禁止用 verify 脚本代替 22 号 Step 0；无 Python 仍必须结转
- 禁止削弱 22 号人人一份（§1 可空）
- 禁止追溯改 20 个 examples 对话正文（只重编号+跨引用）
- 禁止再复制一份 WF-8 Step 0
- 禁止改待办核心表 8 列
- 正式文档不得引用 upgrade-plan 草稿路径

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260825-002.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260825-002.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.15.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.15.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.15.0.md` | 指针文件 |

### A2. 身份拆分（节点2，SG-004）

| # | 文件 | 动作 |
|---|---|---|
| A2.1 | `21-pm-profile-rules.md` | §2.4 重写：pm_name 1～2 位项目基本信息；current_operator 单值；空则 ASK；禁岗位升格；禁回退 |
| A2.2 | `pm-profile-template.md` | 增 current_operator；pm_name 注释 `A / B`；删「用 pm_name 推导我」 |
| A2.3 | `05-query-rules.md` | 「我的待办」Owner=current_operator；空则 ASK |
| A2.4 | Project `SKILL.md` | §4 事实源表加 current_operator |
| A2.5 | Portfolio `SKILL.md` | 「我是张三」走 V-9，对外白话，不写子项目 |

### A3. 模板与缺口（节点3，SG-002/003）

| # | 文件 | 动作 |
|---|---|---|
| A3.1 | `plan-template.md` | §4 每行 `- 阶段 → 图标｜执行人｜排期`；空岗 `⚠️待安排人` / `— 待排期` |
| A3.2 | `gap-capture-rules.md` | Calls/§7 去掉必须建 manifest |
| A3.3 | `skill-gap-skill/CAPABILITY.md` | 产出去掉 "+ manifest" |
| A3.4 | `11-output-artifact-rules.md` | **§3 保留 manifest**；§5/§8 skill_gap 例外不建 |
| A3.5 | `outputs-index-template.md` | Type=skill_gap 主文件=需求-*.md |
| A3.6 | 双包 `skill-gap-demand-template.md` | YAML 可含 batch_id/source_files（正文 〇～七不变） |
| A3.7 | `23-procedure-index.md` | P-SKILL-GAP：skill_gap 不要求 manifest |

### A4. 日报结转与 Python（节点4，SG-008/010）

| # | 文件 | 动作 |
|---|---|---|
| A4.1 | Project `SKILL.md` | 新增 §5.0 环境检测（Python ≥3.9）；日报路由 `00+01+06+17+22` |
| A4.2 | `01-daily-report-rules.md` | 投喂入口硬阻断：先 22 时机 0；不调 verify 脚本 |
| A4.3 | `22-carried-over-rules.md` | 时机 0 触发列举含日报投喂；不改人人一份 / L93 |
| A4.4 | `00-pm-main-rules.md` | WF-8 Step 0 **只对齐、不新造** |

### A5. 治理与 examples（节点5，SG-005/006/007）

| # | 文件 | 动作 |
|---|---|---|
| A5.1 | `16-skill-governance-rules.md` | 新增 §21 AP 约束；§22 examples 质量（不追溯）；§14 路径改 governance-shared；§2.1a L111 写死 planning 路径 |
| A5.2 | `governance-shared/planning/README.md` | L7 必须本目录、每周期 1 个 |
| A5.3 | `examples/` | 按方案重编号 20 个文件 + 两处跨引用 |
| A5.4 | `examples/README.md` | mermaid/表格新编号 |
| A5.5 | `governance-shared/review-checklists/release-checklist.md` | 追加 C-1～C-4；C-4 存量豁免场景/mermaid |

### A6. 脚本（节点6，SG-001/009/011）

| # | 动作 |
|---|---|
| A6.1 | `file_registry.py`：`{编号}` → `{{编号}}` |
| A6.2 | `workspace_builder.py`：README 已存在 skip |
| A6.3 | `migrate_workspace.py`：VERSION_CAPABILITIES 3.15.0 schema 0.16.0；`migrate_business_data` dry-run 默认、快照、幂等、只投影；pm-profile 补空 current_operator |
| A6.4 | 新建 `verify_projection.py`（C1–C8 + D-TODO-WP + D-PLAN-REF + D-EFFECT）；只读 |
| A6.5 | 新建 `verify_todo_continuity.py`（D-TODO-01/02/03）；只读 |
| A6.6 | 新建 `verify_requirement_wp.py`（D-REQ-WP + D-SOURCE）；只读；19 号不自动跑 |
| A6.7 | 新建 `verify_contract_ri.py`（D-CONTRACT）；只读；19 号不自动跑 |
| A6.8 | `19-info-completeness-rules.md`：巡检旁路跑 P0 两脚本 |

### A7. 版本触点（节点7）

| # | 文件 | 动作 |
|---|---|---|
| A7.1 | `_version.py` | 3.15.0 / 0.16.0 |
| A7.2 | `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | 双包 skill.json | current=0.16.0；migrations 0.15.0→0.16.0；versionHistory |
| A7.4 | 双包 CHANGELOG | 3.15.0 段 |
| A7.5 | BLUEPRINT / MODULE_MAP / 根 README×2 | 版本；Python ≥3.9 |
| A7.6 | 20 号 / skill-contract | schema 0.16.0 |

### A8. 基线与发布（节点8）

| # | 动作 |
|---|---|
| A8.1 | `baselines/3.15.0/` 双子树快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每节点 annotated tag（中文）推 origin 与 github |
| A8.4 | 终 tag `v3.15.0` |

## B. 存量工作区（脚本提供，不代跑业务仓）

- dry-run 默认；写回需 PM 确认 + `ai/backup/migration-snapshot-{timestamp}/`
- WP §7/§8 阶段名：先剥 `（完成）` `（当前）`；已是 13 标准名 skip；无法映射保留+⚠️待校准
- 计划 §3/§4 从 WP §8 投影；不重算点名人期
- budget/progress-plan 仍在 plans/ → 清单后移 project-info/
- pm-profile 补 `current_operator:` 空字段
- `--project-root` 无业务 ai/（开发仓）→ skip 存量迁移

阶段名映射沿用 upgrade-to-3.14.0.md B 节表。

## C. 验证检查

- [x] `_version.py` 3.15.0 / 0.16.0
- [x] plan-template §4 含 `｜`
- [x] 11 号 §3 仍有 manifest.md；skill_gap 例外
- [x] 21 号空则 ASK；模板无「用 pm_name 推导我」
- [x] SKILL 日报行含 22
- [x] init 临时目录 README 含字面 `{编号}/`
- [x] examples 01=初始化工作区
- [x] 16 号 §14 指向 governance-shared/review-checklists/
- [x] audit 退出码 0
- [x] 无业务仓路径写入
- [x] 正式文档不引用 upgrade-plan 路径（本文件除外的禁引用）
- [x] planning/ 仅留 README；本版 AP 已删
- [x] 分发包已写入 Downloads（未替换安装区，待用户核验）
