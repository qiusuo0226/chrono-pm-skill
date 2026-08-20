# 升级到 3.0.0

> 从 2.1.0 升级到 3.0.0
> 发布日期：2026-08-19
> Schema 变更：skill schemaVersion 0.6.0 → 0.7.0（契约）；workspace schema 0.8.0 → 0.9.0（联邦挂载协议）。两概念分离，禁止绑死。
> CR 编号：—（未走独立 CR，参照 2.1.0 先例；升级方案 V0.9.2a 定稿经双 Agent 审核放行，结论通过-可执行。实质固化于本文件 + baselines/3.0.0/ + CHANGELOG 3.0.0 段）
> 本次执行范围（用户 2026-08-19）：**只升级 Skill 包**，不处理业务工作区（市监重构项目管理）。工作区迁移步骤保留在本文，供日后执行。

## 变更摘要

双包拆分 + 单项目回归（Major/architecture_change）：ChronoPM-Project 3.0.0（纯单项目录入）+ ChronoPM-Portfolio 3.0.0（只读归集）。废弃旧 portfolio 作为日常录入口；录入归属强制判定；禁止跨项目待办镜像；删除委派→PM 跟进条；pending 查重；结转共享人力提示；DF-007~016 内置 + DF 删除保护；进出组多行 + 人员能耗滚存；登记册时间戳编号；RI 下沉到项目级；Token 分级确认（仍登记 pending-changes）；待办查询默认未办结且未确认终态仍可见。旧 portfolio 工作区默认不拆，日后按 D-13/D-21 原地升级 + 补建自足性最小文件集。

## 新增目录（Skill 仓库）

- `ChronoPM-Project/` — 单项目 Skill 包（现仓库主体迁入）
- `ChronoPM-Portfolio/` — 只读项目集 Skill 包（新建）
- `ChronoPM-Portfolio/references/` — F-3~F-8 六份规则
- `ChronoPM-Portfolio/assets/templates/` — 集层模板
- `governance/baselines/3.0.0/` — 双包基线快照

## 新增文件（Skill 包）

- `ChronoPM-Portfolio/SKILL.md`、`skill.json`、`VERSION`、`CHANGELOG.md`
- `ChronoPM-Portfolio/references/01-readonly-boundary-rules.md`
- `ChronoPM-Portfolio/references/02-aggregation-query-rules.md`
- `ChronoPM-Portfolio/references/03-mount-awareness-rules.md`
- `ChronoPM-Portfolio/references/04-portfolio-report-rules.md`
- `ChronoPM-Portfolio/references/05-resource-shared-rules.md`
- `ChronoPM-Portfolio/references/06-version-health-rules.md`
- `ChronoPM-Portfolio/assets/templates/suggested-update-list-template.md`
- `ChronoPM-Portfolio/assets/templates/portfolio-weekly-template.md`（自 Project 迁入）
- `ChronoPM-Portfolio/assets/templates/project-index-template.md`（自 Project 迁入并改成员挂载字段）
- `governance/migrations/upgrade-to-3.0.0.md`（本文件）

**F-10**：V1 **不建** Portfolio init 脚本。联邦骨架由 AI 按 F-9 模板创建。

## 删除文件/目录（Skill 包）

- `references/09-portfolio-rules.md` 规则实体退役迁出（查询/聚合/汇总周报 → Portfolio；单项目资源条款 → 06 号）；Project 包仅保留**退役指针页**（不加载、无任何规则条款，仅指向 ChronoPM-Portfolio，避免历史路径 404）——P-10「删除」口径于收尾时正式化为「退役迁出 + 保留指针页」（2026-08-19；SKILL.md §15 索引与 audit 断言 6 要求 references/ 全文件名覆盖，指针页在覆盖集内）
- 草稿 `governance/upgrade-plan-v3.0.0.md` 已按 R10 于发布验证通过后删除（2026-08-19，删除登记见 CHANGELOG 3.0.0 段；实质固化于本文件 + baselines/3.0.0/ + CHANGELOG）

## 规则变更（Project 包）

见方案 P-1~P-30。摘要：

- `00`：删 WF-1 18.6；红线禁镜像；新增操作确认分级表（三类写入仍登记 pending-changes）；WF-8 默认归属；P-30 清集层路径（跨项目概念合法保留）
- `01`：§1.0 录入归属判定；迁出集周报/资源变动检测；保留单项目周报；D-23 双轨仲裁（日报 100% 可自动完成 + pending）；能耗投喂入口
- `05`：§2.0a 改指针；新「待办清单查询输出规范」（未办结/已办结；未确认终态默认可见）；RI Step0 读本项目 contract-register
- `06`：删集层路径；并入单项目资源条款（自 09）
- `07`：RI 全部下沉，scope_level=portfolio 不再存集层
- `09`：退役迁出
- `14`：pending 写入查重；DF 行完整性；操作×规则匹配校验
- `16`：AP 生命周期显式化
- `18`：成本核算方式必填；删项目集分支
- `20`：Skill < 工作区版本 → 只读降级；双层 .skill-version.json；skillName 兼容
- `21`：DF-007~016；禁物理删除 DF；disabled 枚举；§5.1b 一次问完协议
- `22`：Step 0.5 共享人力提示；能耗滚存/停链；空窗不占位
- `02/04/08/10/11/12/13/17/19`：P-30 集层路径清理 + 编号时间戳（04/08/17/21 登记册类）

## 模板变更

- `personal-daily-todo-template.md`：§0 进组/离组降级为摘要；新增 §0.5 进出组记录、§0.6 能耗记录
- `pm-profile-template.md`：DF-007~016 预填；引导语改「可覆盖或禁用，不可删除」；状态增 disabled
- `resource-register-template.md`：删 portfolio front-matter 与按子项目分组视图；所属项目列保留他项目名
- `project-context-template.md`：新增「兄弟项目」段、「成本核算方式」段
- 登记册模板编号列：`{前缀}-{YYYYMMDD}-{HHmmss}`（R/I/D/CON/IMP/BID/INIT/COMP/PF/G）
- contract-register / source-type-registry：拆解指针、tender-source、security-assessment-source；ledger 增 source_fingerprint + parsed_by
- `portfolio-weekly-template.md`、集级 `project-index-template.md` 迁 Portfolio

## 工作流变更

- 录入只发生在单项目 ai；混报先拆后写，禁代写他项目
- 分级只决定问不问：直接落库/先写后告知/DF-013 仍登记 pending；未确认完成不进统计不参超期，**默认查询仍可见**
- 委派不再给 PM 生成跟进条
- WF-8 未指定归属时默认当前计划/独立待办
- 结转：有未办结 **或** 当日能耗投喂；滚存源=该人最新文件
- 工作区 Skill 版本反向校验

## 09 号条款 → 目标（P-10 逐条处置）

| 09 原条款 | 目标 | 处置 |
|---|---|---|
| 文头零数据源原则 | Portfolio F-2 / F-3 | 迁；强化「零事实源、禁止落盘聚合」 |
| §1.1 业务目录不侵入 | Project 06 号（已有） | 保留 Project，不迁 |
| §1.2 层级职责 | Portfolio F-2 + F-3 | 迁；改为联邦 `projects/{名}/ai/` |
| §1.3 数据流 + 人员双层 | 双层身份：00 §4d 保留；集层聚合 → F-7 | 拆 |
| §2 汇总周报 | F-6 | 迁；硬约束从项目周报摘；缺周报降级路径 |
| §3 跨项目风险 | F-4 V-4 | 迁；主归属仍在项目 risk-register |
| §4 整体 P&L | F-4 V-7 | 迁 |
| §5 人员资源（跨项目索引） | F-7 | 迁聚合；单项目 register/transfer-log 生命周期 → 06 号 |
| §5.4 动态视图不落盘 | F-3 / F-7 | 迁 |
| §6 里程碑总览 / 门禁最小值 | F-4 V-6 | 迁 |
| §7 项目索引 / 禁扫描代索引 | F-5 | 修订：扫描只发现候选，登记仍需确认 |
| §8 Resource 级联 | 单项目段 → 06；跨项目提示 → F-7 | 拆 |
| §8.1/8.2 归档 | 06 号单项目资源条款 | 迁入 Project |

## P-30 集层路径处置（Project 包）

两类标注：**删/迁** = 集层路径或集层职能；**留** = 跨项目概念/历史注释（R5/R8/DF-016）。

| 文件 | 策略 |
|---|---|
| 00（16） | 删 WF 中 portfolio/issues 读取与集周报路径；留「不得镜像他项目」红线 |
| 01 | 迁集周报/资源变动；留单项目周报 + 归属判定 |
| 02（1） | 删集层会议路径，改为本项目 meetings/ |
| 04 | 编号改时间戳；无集层路径则不动路径 |
| 05 | 删 §2.1 项目集路由（改「跨项目查询请用 Portfolio 包」）；改写 §2.0a |
| 06 | 删集层目录树；并入 09 单项目资源段 |
| 07 | 存储改项目级；检索跨项目改「Portfolio 遍历」指针 |
| 08 | 编号；无集层路径则不动 |
| 10（26） | 删 portfolio/context/domain-glossary 等集层默认路径，改本项目 context/ |
| 11/12 | 删归档到 portfolio/reports 的默认；改本项目 reports 或「建议到 Portfolio 对话」 |
| 13 | 删项目集衔接分支 |
| 17 | 词库路径改本项目 context/domain-glossary.md |
| 18（12） | 删项目集向导分支与 portfolio/requirements 登记路径；合同登记只写本项目 |
| 19 | 巡检路径去集层 |
| file_registry.py | 删 is_portfolio 分支（与 P-14 一致） |

回归断言：Project `references/` grep **集层路径**（`portfolio/` 作为存储路径）零命中；「跨项目」字样允许保留。

## 迁移执行步骤

### A. Skill 仓库（本次执行）

1. 落盘本文件 + 回归用例（本步已完成）
2. 改 Project 规则/模板/脚本/契约/版本触点
3. 新建 Portfolio 包（无 init 脚本）
4. 仓库重组：主体迁入 `ChronoPM-Project/`；根保留 git / README / LICENSE / VERSION / governance / tests / tools
5. 打基线 `governance/baselines/3.0.0/`
6. **不**对业务工作区跑 migrate

### B. 业务工作区（本次不执行；日后按此）

**单项目 2.1.0**：轻量——`.skill-version.json` 升 3.0.0 + skillName `chrono-pm-project` + 补 DF-007~016（已有同义 PF 不覆盖）+ 待办文件补 §0.5/§0.6 + 补成本核算方式（缺则标待登记）。

**集工作区 2.1.0（如市监）**：默认不拆。五步：

1. **内容级升级先行**（原路径）：pm-profile 补 DF；pending 三截按 Change Log 重建。
2. **文件级迁移**：`projects/{子项目}/*` → `projects/{子项目}/ai/*`；补建最小文件集（resources/、reports/、pending-changes.md、contract-register、pm-profile、templates/、.skill-version.json）；兄弟项目名录写入各 project-context；配置型文件每子项目一份；需求库按 coverage 下沉（AI 出清单 → PM 确认 → 复制/移动）。单簇 `{type}-source/` 暂不平铺（ledger 记 source_id，簇 ID 在登记册）；多簇再 `{type}-source/{簇 ID}/`。禁止第三套目录。
3. **prompts/**：主路径 = 出归属清单 → PM 确认后下沉，验证后再删。不得以「v1 遗留直删」为主路径。
4. **portfolio/** 剥离录入口，只留索引/派生产物。
5. 验证（数量核对 + 抽样）后旧路径直删。根级 `todos/` 空→直删；非空→停下询问。

指纹失配：提示版本差异，严禁静默覆盖。140 个 RI 文件的逐文件映射在**工作区升级当时**按实盘生成，不预写死市监清单（Skill 包通用）。

存量 todos：旧进组/离组 → §0.5 首行；待补全不猜。能耗单位待登记直至补录成本核算方式。旧编号不重编，查询双格式兼容。

PF 冲突对照：升级时输出工作区 PF × R17 × 内置 DF，PM 三选一；AI 不单方面删 PF。

失败回退：验证前不删源；失败保留旧结构。

## 验证检查（Skill 包）

收尾回填（2026-08-19，audit_release.py 13/13 PASS 后逐项核实）：

- [x] Project 包 `modes=["single"]`，无 `defaultMode: portfolio`
- [x] Project 无 09 规则实体（仅退役指针页，见删除文件段口径注）
- [x] Project references 无集层存储路径 `portfolio/xxx`（06 号否定式警示句属 P-30 豁免）
- [x] 00 号无步骤 18.6
- [x] IR-006 为反向用例（模块 35）
- [x] DF-007~016 在 21 号与模板
- [x] 待办模板含 §0.5 / §0.6
- [x] 分级表三类仍登记 pending-changes
- [x] P-28：未确认终态默认可见
- [x] Portfolio 只读契约五条 + V-1~V-10
- [x] 双包 version 均为 3.0.0（audit 断言 13）
- [x] `_version.py` SKILL_VERSION=3.0.0，WORKSPACE_SCHEMA_VERSION=0.9.0
- [x] skill schemaVersion=0.7.0
- [x] 无 F-10 init 脚本（Portfolio 包无 scripts/）
- [x] 未改业务工作区任何文件（用户定界）

**遗留偏差（不在本次收尾范围）**：仓库形态未改成三目录（G-5：ChronoPM-Project/ 子目录化），见下方偏差记录。

## 偏差记录（G-5 三目录重组延后，2026-08-19）

- **偏差内容**：迁移执行步骤 A.4「主体迁入 `ChronoPM-Project/`」未执行；Project 包文件仍在仓库根，形成「根 = Project + `ChronoPM-Portfolio/` 伴生目录 + governance/tests/tools」形态（非方案的严格三目录）。
- **延后理由**：① 动面大——audit_release.py 全部断言按「根 = Project」实现，重组需改包根/仓根双根定位，sync_version.py、README 目录树、baselines 快照结构、migrate/pack 路径联动；② 当前形态功能等价——双包版本/内容/基线均已就位，打包已按排除模型正确隔离双包（G-3 已落地），audit 13/13 保障发布质量；③ 不影响业务工作区升级与伴生包使用。
- **后续路径**：如执行，需同步改造 audit（双根）、pack、sync_version、README×2 目录树、baselines/<v>/ChronoPM-Project 快照结构；建议随下一个 Major 版本一并执行，不单独起 Patch。
- **登记**：本偏差随 CHANGELOG 3.0.0 段收尾补记登记，不另起 CR。
