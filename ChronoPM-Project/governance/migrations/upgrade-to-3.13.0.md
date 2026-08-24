# 升级到 3.13.0

> 从 3.12.0 升级到 3.13.0  
> 发布日期：2026-08-24  
> Schema 变更：**不升**，workspace schema 保持 **0.14.0**  
> CR：CR-20260824-005  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.12.0 → 3.13.0。  
> 用户拍板：可以执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。

## 变更摘要

WP 双向联动（SCAN 人期、ADVANCE 半自动推进、计划 6 列节点子行、D38）；WP `effect: 正常|废弃`；项目集 V-13 按时间窗归集正常计划中的正常 WP；`skill-gap-skill/` 技能缺口笔录进 `ai/outputs/`。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径
- 禁止升 schema
- 禁止新增 `references/24-*.md`
- 禁止 `status: 废弃`（生效用 `effect`）
- 禁止 index 第 9 列；PLAN §3 禁止第 7 列
- 禁止 `skill-gap-skill/SKILL.md`
- 禁止全库扫；禁止脚本批量改存量 PLAN/WP
- 禁止自动改链尾；禁止覆盖点名
- 禁止缺口文写入 requirements/wps/plans
- Portfolio 不代写成员项目；不建第二份 skill-gap 目录
- 00 合计净增 ≤100 非空行（§8d+§8e ≤90；P-ALWAYS 第 4 步 ≤8）
- 禁止 P-ALWAYS 第 4 步出现「目标未达成」；该步不写文件

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260824-005.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260824-003.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.13.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.13.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.13.0.md` | 指针文件 |

### A2. 核心规则（节点2）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | P-ALWAYS 第 4 步（V0.4 口径，无「目标未达成」）；闸 2 含子行/废弃/缺文件先 D20；§5a 生效与进度分离、同义词收紧、`(AI聚合)`；§8c 增废弃行与子行验证；新增 §8d 联动、§8e 生效；WF-7 纳入须建议离开待确认；WF-8 仅已规划且 effect=正常；净增≤100 |
| A2.2 | `23-procedure-index.md` | 增 P-WP-SCAN / P-WP-ADVANCE / P-WP-RETIRE / P-SKILL-GAP；调用树补 P-CARRY-WPREF、P-RI 与四新过程；ProcID 16→20 |
| A2.3 | `06-file-rules.md` | PLAN §3 父+子行仍 6 列；WP `effect`；index 状态可写废弃；预览护栏 |
| A2.4 | `14-self-check-rules.md` | D38；D20 与闸 2 缺文件分工 |

### A3. 模板（节点3）

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `wp-template.md` | YAML `effect`/`superseded_by`；§1 生效行；§8 排期/(AI聚合)/点名/空岗/包级覆盖 |
| A3.2 | `plan-template.md` | §3 父+子行示例（6 列）；只纳入正常 WP；禁止加列 |
| A3.3 | `wp-index-template.md` | 状态列注释含废弃；仍 8 列 |

### A4. 辅助规则与能力目录（节点4）

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | `skill-gap-skill/` | 新增 CAPABILITY + capability-boundary + gap-capture-rules（V0.4 骨架）+ 模板；无 SKILL.md |
| A4.2 | `10-update-trigger-rules.md` | Level 1 一行 + Level 3「技能缺口信号」 |
| A4.3 | `05-query-rules.md` | 计划查询含子行/空岗；默认只列正常 WP |
| A4.4 | `11-output-artifact-rules.md` | Type=skill_gap；主文件 `需求-*.md`；禁归档事实源 |
| A4.5 | `04-risk-issue-rules.md` | Issue 关闭 SUGGEST：关联 WP 若未废弃可提示推进 |
| A4.6 | `07-requirement-rules.md` | 推进已规划时 CHECK 未确认需求（一句交叉引用） |
| A4.7 | `19-info-completeness-rules.md` | 指针到 D38 |

### A5. Portfolio 与文档三角（节点5）

| # | 文件 | 动作（写死） |
|---|---|---|
| A5.1 | Portfolio `SKILL.md` + `02-aggregation-query-rules.md` | V-13；集层缺口最小落盘 |
| A5.2 | Portfolio 拷贝 `skill-gap-demand-template.md` | 不建 skill-gap-skill 目录 |
| A5.3 | Project `SKILL.md` | 路由：WP 查询可选 14；技能缺口行 |
| A5.4 | `SKILL_MODULE_MAP.md` | G4/G5/G18 扫描推进；G20 缺口；G5 子行 |
| A5.5 | `examples/09,11,14` + **新增 20** + examples/README | 节点空岗、时间窗、D38、缺口 |
| A5.6 | 仓库根 README.md / README.en.md | 开口两行（节点/空岗；归纳日期前计划；记技能缺口） |

### A6. 回归与审计脚本（节点6）

| # | 动作（写死） |
|---|---|
| A6.1 | 模块 68：WPL / PFA / SG（含 V0.4 SG-007~010、WPL-021） |
| A6.2 | `audit_release.py` 第 15 条必含 gap-capture-rules + 模板 |
| A6.3 | PLT-006 / PWP-006 保持 |

### A7. 版本触点（节点7）

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | `scripts/_version.py` | SKILL_VERSION=3.13.0；schema 0.14.0 |
| A7.2 | 跑 `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A7.3 | CHANGELOG 双包 | 3.13.0 段 |
| A7.4 | BLUEPRINT 演进表 | 3.13.0 行 |

### A8. 基线与发布（节点8）

| # | 动作（写死） |
|---|---|
| A8.1 | `baselines/3.13.0/` 双子树全量快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每完成一个节点：annotated tag（中文）推 origin 与 github |
| A8.4 | AP 草稿：基线拍完后删除（`planning/` 仅 README） |
| A8.5 | 全部完成后请用户核验；不提前打断 |

---

## B. 业务工作区

**本发布不代做任何业务仓。**

| 对象 | 方式 |
|---|---|
| PLAN 无子行 | 闸 2 懒补默认范围（链尾及之后） |
| WP 无 `effect` | 触碰懒补 `effect: 正常` |
| WP 无 §8 排期 | 第一次 SCAN 写列表行 |
| 待确认已入计划 | D38 建议 ADVANCE |
| 用户认为该废弃但 effect=正常 | 问是否 RETIRE，不自动废弃 |
| §3 引用失踪 WP 文件 | 先 D20，确认无法恢复才移出 |

## C. 验证检查

- [ ] `_version.py` 3.13.0 / 0.14.0
- [ ] 00 净增非空行 ≤100；无「目标未达成」
- [ ] 23 ProcID=20；调用树含 P-CARRY-WPREF、P-RI、四新过程
- [ ] plan-template §3 仍 6 列；wp-index 仍 8 列
- [ ] wp-template 有 `effect`，`status` 仅四枚举
- [ ] skill-gap-skill 无 SKILL.md；audit 含其规则+模板
- [ ] 模块 68 已写入；PLT-006 / PWP-006 仍在
- [ ] README / examples 09·11·14·20 / MAP 已改
- [ ] 正式文档不引用 upgrade-plan 路径
- [ ] audit_release 退出码 0
- [ ] 无业务仓路径写入
