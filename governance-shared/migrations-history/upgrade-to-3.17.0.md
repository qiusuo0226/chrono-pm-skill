# 升级到 3.17.0

> 从 3.16.0 升级到 3.17.0  
> 发布日期：2026-08-26  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260826-002  
> IA：IA-20260826-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.16.0 → 3.17.0。  
> 用户拍板：执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V0.3（B1/B2 通过-待修订，A 已核实修订）。  
> 16 号 §4 例外：本版 8 条一 CR 多节点，经用户裁决；后续不得当常态。  
> 3.16 A6 反转：Mermaid 仅对话禁落盘 → 唯一例外懒建 `wps/_wp-chart.md` 派生视图。

## 变更摘要

工作包关联记录盖章；图默认全包竖排总览、连线只认前后置、派生落盘；WP 查询摘要+原件链接；skill-gap 不进 pm-decisions 且强制示例图节；功能点列「阶段」、全齐 AUTO。双包同号 3.17.0。workspace schema 保持 0.16.0。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径
- 禁止升 workspace schema
- 禁止新建规则文件、禁止新建结论索引
- 禁止把图当生成物写入 `ai/outputs/` 或走 P-OUTPUT
- 禁止一条待办多个 WP Ref
- 禁止全齐以外的 WP 推进自动写状态链
- 禁止把存量「已评审」静默填成某一十三阶段名
- 正式文档不得引用 upgrade-plan 草稿路径

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260826-002.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260826-002.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.17.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.17.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.17.0.md` | 指针文件 |

### A2. skill-gap（节点2，D4/D5）

| # | 文件 | 动作 |
|---|---|---|
| A2.1 | `skill-gap-skill/references/gap-capture-rules.md` | Forbidden：不进 pm-decisions、不问 PM 确认；§6 强制 〇·五；落盘前撞号=级联失败 |
| A2.2 | `skill-gap-skill/assets/templates/skill-gap-demand-template.md` | 开场后加 〇·五 示例图 |
| A2.3 | `examples/20-技能缺口.md` | 不进 pm-decisions；含示例图节说明 |

### A3. 图形态与派生落盘（节点3，D2/D3）

| # | 文件 | 动作 |
|---|---|---|
| A3.1 | `11-output-artifact-rules.md` §17 | 默认全包竖排三行节点；边只认 related_wps；懒建 `wps/_wp-chart.md`；指纹字段集 |
| A3.2 | `05-query-rules.md` 画图行 | 默认总览规格；可链盘上图；禁止编造边 |
| A3.3 | `skill-contract.md` #1/#2 | 例外：`wps/_wp-chart.md` 派生视图 |
| A3.4 | `SKILL.md` 底线 13 | 同例外 |
| A3.5 | `assets/templates/wp-chart-template.md` | 新模板 |
| A3.6 | `06-file-rules.md` WP 行 | 允许懒建 `_wp-chart.md`，不进 index 行 |
| A3.7 | `00` §8c.1 | 影响图字段 → 指纹 → 重画 |

### A4. WP 查询（节点4，D6）

| # | 文件 | 动作 |
|---|---|---|
| A4.1 | `05-query-rules.md` §6.7 WP 行 | 摘要+原件链接；「贴原文」才全文；旧「评审状态」列原样展示 |

### A5. 盖章（节点5，D1）

| # | 文件 | 动作 |
|---|---|---|
| A5.1 | `wp-template.md` | §4b 关联记录 |
| A5.2 | `personal-daily-todo-template.md` | §1.3 决策 Ref |
| A5.3 | `00` WF-1 | 办结/敲定盖章步；缺行=级联未完成 |
| A5.4 | `23-procedure-index.md` | P-WP-STAMP / P-WP-CHART / P-WP-ALIGN |

### A6. 功能点阶段（节点6，D7/D8）

| # | 文件 | 动作 |
|---|---|---|
| A6.1 | `wp-template.md` §3b | 删阶段归属；评审状态→阶段；固定说明 |
| A6.2 | `00` §5a/§10.1 | 去阶段归属；全齐 AUTO 白名单；来源 AUTO-全齐 |
| A6.3 | 本文件 B 节 | 存量三值映射 |

### A7. 版本触点（节点7）

| # | 文件 | 动作 |
|---|---|---|
| A7.1 | `_version.py` | SKILL_VERSION 3.17.0（schema 仍 0.16.0） |
| A7.2 | `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | CHANGELOG 双包 + BLUEPRINT + 根 README×2 | 3.17.0；写明 A6 反转与 §4 例外；回归 642 |
| A7.4 | `tests/regression-suite.md` | Module 71（WPR-001～022） |
| A7.5 | `migrate_workspace.py` VERSION_CAPABILITIES | 追加 3.17.0 schema 0.16.0 |
| A7.6 | Portfolio VERSION/SKILL.md/skill.json/CHANGELOG | 同号对齐 |

### A8. 基线与发布（节点8）

| # | 动作 |
|---|---|
| A8.1 | `baselines/3.17.0/` 双子树快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每节点 annotated tag（中文）推 origin 与 github |
| A8.4 | 终 tag `v3.17.0` |
| A8.5 | 删除本版 AP 草稿；全部完成后再请用户核验 |

## B. 存量工作区

默认 **不写** 业务 WP。`--migrate-business` 须 PM 确认：

| 旧「评审状态」 | 新「阶段」 | 其它 |
|---|---|---|
| `—` | `—` | dry-run 记「原空」 |
| `未评审` | `—` | 标注「原未评审，阶段未知」 |
| `待评审`（脏） | `—` | 同未评审 |
| `已评审` | **不写阶段名** | pm-decisions「已评审待落位」 |

删「阶段归属」列。查询未迁移文件时原样展示旧列，禁止翻译成十三阶段。

`--project-root` 无业务 ai/（开发仓）→ skip。

## C. 验证检查

- [ ] `_version.py` 3.17.0 / schema 0.16.0
- [ ] 11 §17 默认总览 + `_wp-chart.md` 派生例外
- [ ] 05 WP 查询摘要+链接
- [ ] wp-template 无阶段归属、有 §4b、「阶段」列
- [ ] gap-capture 禁 pm-decisions；有 〇·五
- [ ] 待办恰好 1 个 WP 未改
- [ ] audit 退出码 0
- [ ] 无业务仓路径写入
- [ ] 正式文档不引用 upgrade-plan 路径
- [ ] 双包 3.17.0
