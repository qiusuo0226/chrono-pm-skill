# 升级到 3.16.0

> 从 3.15.0 升级到 3.16.0  
> 发布日期：2026-08-26  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260826-001  
> IA：IA-20260826-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.15.0 → 3.16.0。  
> 用户拍板：可以执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V0.3.1（B 通过-可执行）。

## 变更摘要

格式硬约束（日期 YYYY-MM-DD、WP §8 执行人/排期边界、计划 §4 由 verify_projection.py 分通道校验）；版本模板权威源 + skill_gap 禁 manifest；WP↔WP 可选 `related_wps`（YAML SSOT，index 末尾加两列）；Mermaid 派生图仅对话（11 号 §17）。双包同号 3.16.0。workspace schema 保持 0.16.0。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径（含市监重构项目管理）
- **禁止** 19 号 §1.2 默认 P0 命令加上 `--check-plan-section4`（存量压缩计划会 P0 失败）
- 禁止把画图当生成物落盘（含 `ai/outputs/`）；禁止改 23 号
- 禁止用 `STAGE13` 当 §4 必满 13 项白名单（比较对象=该 WP §8 实际行）
- 禁止 index 在中间插列（只允许末尾追加上游/下游）；verify 继续用 `ic[2]`/`ic[3]`
- 禁止把「生效」写成独立列
- 正式文档不得引用 upgrade-plan 草稿路径
- 禁止升 workspace schema

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260826-001.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260826-001.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.16.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.16.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.16.0.md` | 指针文件 |

### A2. 格式硬约束（节点2，SG-006/005）

| # | 文件 | 动作 |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | 新增 §5.1b 日期字段/区间两端完整 `YYYY-MM-DD`，排除 ID/`updated`/周号 |
| A2.2 | `wp-template.md` | §8 字段边界：执行人仅人名/分工，放行 `(点名)`/`(AI聚合)`/`⚠️待安排人`，禁日期；排期仅区间 |
| A2.3 | `plan-template.md` | 多人分隔符 `/`→`、` |
| A2.4 | `19-info-completeness-rules.md` | 新增日期格式/字段边界扫描（P2）；**§1.2 命令不加开关** |
| A2.5 | `14-self-check-rules.md` | 写入场景引用 19 号格式扫描 |

### A3. 版本权威源（节点3，SG-001-版本）

| # | 文件 | 动作 |
|---|---|---|
| A3.1 | `00-pm-main-rules.md` | 改写 §4a.1：禁止手写版本号；模板只读 Skill 包 `assets/templates/` |
| A3.2 | `gap-capture-rules.md` | 版本号只抄事实源；skill_gap 出现 manifest = 级联失败 |

### A4. WP↔WP（节点4，SG-001-责任链）

| # | 文件 | 动作 |
|---|---|---|
| A4.1 | `wp-template.md` | YAML `related_wps`；§2b 投影表；建链待确认 |
| A4.2 | `wp-index-template.md` | 末尾追加上游/下游 → 10 列 |
| A4.3 | `06-file-rules.md` | 8 列→10 列；L308 改写「生效不成列；第 9/10 列=上游/下游」 |
| A4.4 | `00-pm-main-rules.md` | §5a 同句；§8c.1 双向互指+D20；§8e 废弃清对端 |

### A5. §4 确定性校验（节点5，SG-002）

| # | 文件 | 动作 |
|---|---|---|
| A5.1 | `scripts/verify_projection.py` | `--check-plan-section4`；有开关 exit 1；无开关 §4 问题 UNJUDGED exit 2；比较=§8 实际行 |
| A5.2 | `00-pm-main-rules.md` | 闸 2：写入落盘前带开关；无 Python 则两步人工清单 |

### A6. Mermaid（节点6，SG-002-Mermaid）

| # | 文件 | 动作 |
|---|---|---|
| A6.1 | `11-output-artifact-rules.md` | 新增 §17；仅对话；禁止任何落盘 |
| A6.2 | `05-query-rules.md` | 画图路由到 11 §17 |
| A6.3 | `10-update-trigger-rules.md` | 画图不是更新意图 |
| A6.4 | `00-pm-main-rules.md` | §2.7 画图/责任链图/排布图/Mermaid = 查询 |
| A6.5 | 不改 `23-procedure-index.md` | — |

### A7. 版本触点（节点7）

| # | 文件 | 动作 |
|---|---|---|
| A7.1 | `_version.py` | SKILL_VERSION 3.16.0（schema 仍 0.16.0） |
| A7.2 | `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | Project SKILL.md | version；description 触发词「画图/责任链图」；路由行必须 `05+11` |
| A7.4 | 双包 skill.json / CHANGELOG / BLUEPRINT / 根 README×2 | 3.16.0；回归 620 |
| A7.5 | `tests/regression-suite.md` | Module 70（FMT-001～019） |
| A7.6 | `migrate_workspace.py` VERSION_CAPABILITIES | 追加 3.16.0 schema 0.16.0 |
| A7.7 | Portfolio VERSION/SKILL.md/skill.json/CHANGELOG | 同号对齐 |

### A8. 基线与发布（节点8）

| # | 动作 |
|---|---|
| A8.1 | `baselines/3.16.0/` 双子树快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每节点 annotated tag（中文）推 origin 与 github |
| A8.4 | 终 tag `v3.16.0` |
| A8.5 | 删除本版 AP 草稿（基线拍完后）；全部完成后再请用户核验 |

## B. 存量工作区

- 不强制批改。下次打开 WP/计划时按新约束标记 `⚠️`，PM 确认后纠正。
- 示例纠正路径：企业通 `WP-新设名称申报`（执行人栏拆日期、省年补全）。
- `related_wps` 缺省空。`wps/_index.md` 下次更新时末尾增列。
- `--project-root` 无业务 ai/（开发仓）→ skip

## C. 验证检查

- [x] `_version.py` 3.16.0 / schema 0.16.0
- [x] wp-template §8 五列 + 字段边界 + related_wps
- [x] wp-index 10 列，只追加末尾
- [x] 11 号 §9 仍是事实源边界；§17 为 Mermaid
- [x] 19 号 §1.2 无 `--check-plan-section4`
- [x] SKILL 路由画图行 = 05+11
- [x] 不改 23 号
- [x] audit 退出码 0
- [x] 无业务仓路径写入
- [x] 正式文档不引用 upgrade-plan 路径
- [x] 双包 3.16.0
