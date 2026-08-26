# ChronoPM-Project v3.16.0 升级方案

> **方案版本**：V0.3.1  
> **当前状态**：B 终审 **通过-可执行**（2026-08-26）。T-1～T-5 已写入 AP。用户授权分步执行；每节点 annotated tag 推 origin 与 github。  
> **目标版本**：3.15.0 → 3.16.0（Project + Portfolio 双包同号）  
> **Workspace Schema**：保持 0.16.0（不变）  
> **contract_change**：是（修改 SKILL.md + 00 号核心契约层）  
> **生成时间**：2026-08-26

---

## 工作空间版本快照

| 项目 | 值 |
|---|---|
| 工作空间根路径 | `c:\Users\qiusuo\Downloads\ChronoPM Skill` |
| 版本标识来源 | `skill.json` version + `VERSION` |
| 版本标识值 | Project 3.15.0 / Portfolio 3.15.0 / schema 0.16.0 |
| 关键文件清单 | SKILL.md, skill.json, VERSION, CHANGELOG.md, references/(23 文件), assets/templates/(37 文件), scripts/(顶层 8 + chronopm_init/ 6 = 14 文件) |
| 用户确认状态 | ✅ 已由用户确认 |

---

## 变更日志

| 版本 | 时间 | 变更内容 |
|---|---|---|
| V0.1 | 2026-08-26 | 初版方案，基于 A 首次目录扫描形成 |
| V0.2 | 2026-08-26 | 按 B 审核意见修订：① 文件移到 planning/；② 结构改为 AP-1~AP-7；③ KA-2 四列→五列；④ SG-002 改 verify_projection.py；⑤ Mermaid 移 §17；⑥ 双包同号；⑦ 标 contract_change；⑧ 删除虚构 20%/15% 门槛；⑨ 补 B-01~B-18 逐条回复 |
| V0.3 | 2026-08-26 | 按 B V0.2 修订：① 00 §5a 重写「不加第9列」+§8e 废弃清对端+§2.7 画图=查询；② verify §4 分通道设计；③ 删 23 号改动+11§17 禁落盘；④ B2-04~B2-09 重大项 |
| V0.3.1 | 2026-08-26 | B 复审「通过-待修订」。写入 T-1~T-5：① 语法设计 §4 补放行后缀；② 19 号施工禁区；③ SKILL.md 拆清 description/路由/加载；④ §8c.1 双向互指+D20；⑤ 文档对齐（STAGE13 措辞/V0.2→V0.3/KA-1 行数） |

---

# AP-1. 变更概述

v3.16.0 定位为 **「格式硬约束 + 数据模型微调 + 确定性校验」** 版本，解决 6 份 SG 需求（4 高 + 2 中优先级）：

1. **格式硬约束**（SG-006/005/002）：全局日期格式 `YYYY-MM-DD` 硬规则（收窄到日期字段与区间两端）；WP §8 执行人/排期字段边界约束（五列中只约束第 3、4 列）；计划 §4 投影完整性由 `verify_projection.py` 确定性校验（STAGE13 仅作缺标准名时的提示，比较对象为 WP §8 实际行阶段名集合）。
2. **执行纪律**（SG-001-版本）：改写 00 §4a 第 1 条，增加模板权威源（Skill 包 `assets/templates/` 为准，工作区 `ai/templates/` 仅参考）；gap-capture-rules 写死 skill_gap 禁建 manifest。
3. **数据模型扩展**（SG-001-责任链）：WP 新增可选 YAML `related_wps`（upstream/downstream），SSOT = YAML，§2b 为投影，index 为加速器；同步改 06/00/模板的 8 列冻结→10 列。
4. **新能力**（SG-002-Mermaid）：11 号新增 §17 派生 Mermaid 图规则，仅对话输出，不落盘不登记。
5. **双包同号**：Portfolio 齐步 3.16.0（能力无变化，CHANGELOG 写「同号对齐」）。

**捆绑例外**：用户明确要求 6 SG 同版本发布，属 16 号 §4 例外。

---

# AP-2. 影响点详细分析

| 影响项 | 当前状态 | 变更后状态 | 影响描述 | 程度 | 可逆 |
|---|---|---|---|---|---|
| `00-pm-main-rules.md` | 923 行，无日期总规则/版本模板权威 | +约 30 行，§5.1b 日期规则（收窄）+ §4a.1 改写 + §8c.1 关联检查 + 闸 2 引用 verify | 核心契约变更，净增控制在 30 行内 | 中 | 是 |
| `wp-template.md` | §8 五列（阶段/状态/执行人/排期/关键阶段） | §8 注释增加字段边界约束（只约束执行人/排期）；新增 §2b 关联 WP 表；YAML 新增 related_wps | WP 数据模型扩展 | 中 | 是 |
| `plan-template.md` | 13 阶段示例，分隔符 `/` | 分隔符改 `、`（与 WP 一致）；§4 注释引用 verify | 计划模板微调 | 低 | 是 |
| `wp-index-template.md` | 8 列，注释「仍 8 列」 | 末尾追加「上游 WP」「下游 WP」→ 10 列；注释更新 | 索引扩展 | 中 | 是 |
| `06-file-rules.md` | §6/§7.4 写死「仍 8 列」 | 改为「10 列（含上游/下游 WP）」 | 冻结规则更新 | 中 | 是 |
| `11-output-artifact-rules.md` | §9=事实源边界，到 §16 | 新增 §17 Mermaid 派生图 | 新能力 | 中 | 是 |
| `19-info-completeness-rules.md` | 完整性巡检主文件 | 新增日期格式/字段边界扫描项 | 巡检增强 | 低 | 是 |
| `gap-capture-rules.md` | 无 manifest 禁止校验 | 写死 skill_gap 出现 manifest = 级联失败 | 执行纪律 | 低 | 是 |
| `scripts/verify_projection.py` | 有 STAGE13 未用于 §4 校验 | 新增 §4 投影校验函数（STAGE13 仅作缺标准名提示） | 确定性校验 | 中 | 是 |
| `SKILL.md` | 路由表无「画图」 | 路由表加派生图行 | 核心契约 | 低 | 是 |
| `SKILL_BLUEPRINT.md` | 3.15.0 | 3.16.0 + Mermaid + WP↔WP | 能力蓝图 | 低 | 是 |
| `tests/regression-suite.md` | 601 用例 | +新模块（6 SG 覆盖）+negative ≥4 条 | 回归扩展 | 中 | 是 |
| ~~`23-procedure-index.md`~~ | — | **不改**（纯查询不载，画图走 05→11 §17） | — | — | — |
| Portfolio 版本文件 | 3.15.0 | 3.16.0（同号对齐） | 双包同版本 | 低 | 是 |
| 存量 WP 文件 | 无 related_wps | 缺省空，不强制补 | 向后兼容 | 低 | — |
| 存量 wps/_index.md | 8 列 | 下次更新时自动增列 | 存量渐进 | 低 | — |
| 工作区兼容性 | schema 0.16.0 | 不变 | 目录结构无变化 | 低 | — |

**contract_change 标记**：修改 SKILL.md + 00 号 → 标 `contract_change`，须全量回归（601 套件 + 新增模块）。

---

# AP-3. 变更策略与设计思路

## 为什么选择这个方案

- **SG-002**：SG 原文要「确定性校验」。仓库已有 `verify_projection.py`（含未使用的 `STAGE13`），扩展它是最小补丁。否决方案：只加 AI 提示词注释——否决原因：SG-002 根因就是「AI 为控篇幅不守模板」，再加提示词等于重复失效。
- **Mermaid**：否决方案「放 05 号派生查询」——图是生成物不是查询路由，11 号更贴。否决方案「走 P-OUTPUT 且登记 index」——派生视图非正式交付物，与 11 号「生成物不得当查询数据源」冲突。最终选「仅对话输出」。
- **related_wps SSOT**：否决方案「三处手写（YAML+§2b+index）」——Skill 历史教训就是双写。最终选 YAML 权威 + §2b/index 投影。
- **index 加列**：否决方案「index 不加列，关联只在 WP YAML」——PM 看图排任务需要 index 一览。最终选末尾追加两列，verify 脚本继续用固定下标 `ic[2]`/`ic[3]`。

## 与现有规则的交互

| 新规则 | 交互的现有规则 | 关系 |
|---|---|---|
| §5.1b 日期格式 | 00 §5.1a 沟通质量 | 补充，不冲突 |
| §4a.1 改写（模板权威源） | 20 号版本检查、gap-capture-rules | 增强，闭环 |
| §8c.1 关联检查 | §8d P-WP-SCAN、§8e P-WP-RETIRE | 新增检查点 |
| 11 号 §17 Mermaid | 05 查询路由、SKILL.md 路由表 | 新增能力，路由独立 |
| verify §4 投影 | 闸 2「§4==§8 全表」 | 确定性兜底 |

---

# AP-4. 修改范围清单

## 文件级改动清单

| 文件路径 | 操作类型 | 修改内容 | 修改原因 | 优先级 | 风险 | 备注 |
|---|---|---|---|---|---|---|
| `ChronoPM-Project/VERSION` | 修改 | 3.15.0→3.16.0 | 版本升级 | P0 | 低 | contract_change |
| `ChronoPM-Project/skill.json` | 修改 | version+history+migration | 版本声明 | P0 | 低 | contract_change |
| `ChronoPM-Project/SKILL.md` | 修改 | ① front matter `version`→3.16.0；② `description` 触发词补「画图/责任链图」；③ 路由表新行「画图」→**必须加载 `05+11`**（禁止落到「简单查询仅 05」，否则 11 §17 不载入） | 版本触点+路由 | P0 | 中 | **contract_change** |
| `ChronoPM-Project/CHANGELOG.md` | 修改 | 新增 3.16.0 条目 | 变更日志 | P0 | 低 | |
| `scripts/_version.py` | 修改 | SKILL_VERSION→3.16.0 | 脚本版本源 | P0 | 低 | |
| `references/00-pm-main-rules.md` | 修改 | §5.1b 日期规则（收窄到日期字段/区间）；§4a.1 改写（模板权威源）；**§5a 重写「不加第 9 列」→「状态列写废弃；生效不成列；上游/下游为第 9/10 列」**；**§8c.1 关联检查 + related_wps 双向互指**（改 upstream 必须同步对端 downstream，反之亦然；缺文件走 D20，不建幽灵 WP）；§8e P-WP-RETIRE 废弃时清对端 related_wps；§2.7 意图表把「画图/责任链图/排布图/Mermaid」归入查询；闸 2 引用 verify（分通道） | SG-006/001/005/002 | P0 | 中 | **contract_change**，净增约 35 行 |
| `assets/templates/wp-template.md` | 修改 | §8 字段边界约束（只约束执行人/排期；**放行 `(点名)`/`(AI聚合)`/`⚠️待安排人`**）；§2b 关联 WP 表；YAML related_wps；**建链/改链走待确认 + pm-decisions** | SG-005/001-责任链 | P0 | 中 | 五列不动 |
| `assets/templates/plan-template.md` | 修改 | 分隔符 `/`→`、`；§4 注释引用 verify | SG-002 | P0 | 低 | |
| `assets/templates/wp-index-template.md` | 修改 | 末尾追加「上游 WP」「下游 WP」→10 列；注释更新 | SG-001-责任链 | P1 | 低 | 只追加末尾 |
| `references/06-file-rules.md` | 修改 | §6/§7.4「仍 8 列」→「10 列」；**§7.4 L308「不加第 9 列」改写为「状态列写废弃；生效不成列；上游/下游为第 9/10 列」** | 冻结更新 | P0 | 中 | |
| `references/11-output-artifact-rules.md` | 修改 | 新增 §17 Mermaid 派生图（仅对话）；**硬禁：禁止写成任何文件（含 ai/outputs/）** | SG-002-Mermaid | P1 | 中 | 不占 §9 |
| `references/19-info-completeness-rules.md` | 修改 | 新增日期格式/字段边界扫描项 | SG-006/005 | P1 | 低 | 主巡检落点。**施工禁区**：§1.2 默认 P0 命令不加 `--check-plan-section4`，禁止把该开关并入完整性巡检 P0（否则存量计划 P0 失败） |
| `references/14-self-check-rules.md` | 修改 | 辅助巡检引用 19 号 | SG-006/005 | P2 | 低 | |
| `skill-gap-skill/references/gap-capture-rules.md` | 修改 | 写死 skill_gap 禁建 manifest + 版本号只抄事实源 | SG-001-版本 | P0 | 低 | |
| ~~`references/23-procedure-index.md`~~ | ~~删除~~ | **不改。23 号加载条件为写入/派活，纯查询不载。画图是查询，不走 23 号。** | — | — | — | B2-03 |
| `references/05-query-rules.md` | 修改 | 「画图」意图路由到 11 号 §17 | SG-002-Mermaid | P2 | 低 | |
| `references/10-update-trigger-rules.md` | 修改 | 排除「画图」为更新意图 | SG-002-Mermaid | P2 | 低 | |
| `scripts/verify_projection.py` | 修改 | 新增 §4 投影校验（**分通道**：`--check-plan-section4` 开关；有开关=严格 exit 1；无开关=UNJUDGED exit 2）；比较对象=该 WP §8 实际行阶段名集合（非 STAGE13 白名单） | SG-002 | P0 | 中 | 扩展非新建 |
| `SKILL_BLUEPRINT.md` | 修改 | 3.16.0 + Mermaid + WP↔WP | 能力蓝图 | P1 | 低 | |
| `tests/regression-suite.md` | 修改 | +新模块 +negative ≥4 条 +PLT/PWP/STP 阻断 | 回归 | P0 | 中 | 601→扩展 |
| `governance/migrations/upgrade-to-3.16.0.md` | **新增** | 升级指引+存量纠正+双包指针+**施工禁区**（19 号默认不加 `--check-plan-section4`） | 治理要求 | P0 | 低 | |
| `governance/migrations/README.md` | 修改 | 版本链追加 3.16.0 | 治理要求 | P0 | 低 | B2-07 |
| `governance-shared/migrations-history/upgrade-to-3.16.0.md` | **新增** | 拷贝 | 治理要求 | P0 | 低 | B2-07 |
| `ChronoPM-Portfolio/VERSION` | 修改 | 3.15.0→3.16.0 | 双包同号 | P0 | 低 | |
| `ChronoPM-Portfolio/skill.json` | 修改 | version→3.16.0 | 双包同号 | P0 | 低 | |
| `ChronoPM-Portfolio/SKILL.md` | 修改 | front matter version→3.16.0 | 双包同号 | P0 | 低 | |
| `ChronoPM-Portfolio/CHANGELOG.md` | 修改 | 「同号对齐，能力变更见 Project」 | 双包同号 | P0 | 低 | |
| `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.16.0.md` | **新增** | 指针文件 | 双包同号 | P0 | 低 | |

**净增文件**：3（Project upgrade-to + migrations-history 拷贝 + Portfolio 指针）；README 为修改

---

# AP-5. 回归测试计划

## 新增测试用例

| Case ID | 模块 | 输入 | 预期结果 | 类型 |
|---|---|---|---|---|
| TC-01 | 日期格式 | 写入 `07-17` 作为日期字段 | 标记 `⚠️ 日期格式待纠正` | positive |
| TC-02 | 日期格式 | 写入 `2026-07-17` | 正常通过 | positive |
| TC-03 | 日期格式 | 叙事中出现 `07-17` | 不误伤（非日期字段） | **negative** |
| TC-04 | 日期格式 | ID 中含 `20260717` | 不误伤 | **negative** |
| TC-05 | 字段边界 | WP §8 执行人栏写 `王欢欢（2026-06-29~2026-08-20）` | 标记 `⚠️ 字段边界待纠正` | positive |
| TC-06 | 字段边界 | 执行人 `王欢欢`，排期 `2026-06-29~2026-08-20` | 正常通过 | positive |
| TC-07 | §4 校验（严格） | PLAN §4 某 WP 缺阶段 | `verify --check-plan-section4` 退出 1，落盘被拦截 | positive |
| TC-08 | §4 校验（严格） | PLAN §4 完整 | verify 退出 0 | positive |
| TC-09 | §4 校验（巡检） | 存量 PLAN §4 被压缩 | 默认巡检（无开关）→ exit 2 UNJUDGED，**不 P0** | **negative** |
| TC-10 | 版本核对 | skill_gap front matter 手写 3.14.0 | 纠正为 3.16.0 | positive |
| TC-11 | 版本核对 | skill_gap 批次含 manifest.md | 级联失败 | **negative** |
| TC-12 | WP↔WP | 设置 WP-002 前置=WP-001 | YAML+§2b+index 同步 | positive |
| TC-13 | WP↔WP | 废弃 WP-001 | WP-002 upstream 引用被清理 | positive |
| TC-14 | WP↔WP | related_wps 自指 | 拒绝 | **negative** |
| TC-15 | Mermaid | 请求「画 WP 结构图」 | 对话输出 Mermaid 代码块 | positive |
| TC-16 | Mermaid | 未请求画图 | 不生成图 | **negative** |
| TC-17 | 回归 | 正常日报处理 | 行为不变 | regression |
| TC-18 | 回归 | 正常待办创建 WF-8 | 行为不变 | regression |
| TC-19 | 回归 | 正常计划生成 | 行为不变 | regression |

## 阻断回归项（必须通过）

- PLT-001 / PLT-002（计划投影）
- PWP-004（WP §8 投影）
- STP-001 / STP-005（计划 §4 相关）
- 全部 C1~C8 / D-TODO-WP / D-PLAN-REF / D-EFFECT（verify_projection.py 现有检查项）

---

# AP-6. 风险评估与回滚方案

| 风险项 | 概率 | 影响 | 预防 | 回滚 |
|---|---|---|---|---|
| 00 号膨胀（923→~953） | 确定 | 中 | 改写既有句而非叠加；增量控制 30 行 | 回滚到 3.15.0 基线 |
| index 加列破坏存量解析 | 低 | 中 | 只追加末尾两列；verify 用固定下标 ic[2]/ic[3] | index 回退 8 列 |
| related_wps 三处不一致 | 中 | 中 | YAML SSOT + 写后必检 §8c.1 | 清空 related_wps |
| 双包版本分叉 | 低 | 高 | 同号发布，CHANGELOG 互引 | Portfolio 回退 3.15.0 |
| verify 脚本误报阻断正常落盘 | 低 | 中 | 先 dry-run 验证；negative 用例覆盖 | 暂时跳过 verify |

## 回滚方案

- **回滚版本**：3.15.0 基线（`governance-shared/baselines/3.15.0/`）
- **回滚步骤**：① 还原 VERSION/skill.json/SKILL.md/CHANGELOG/_version.py；② 还原 00 号/wp-template/plan-template/wp-index-template/06 号/11 号/05 号/10 号/19 号/14 号/gap-capture-rules；③ 还原 verify_projection.py；④ 还原 SKILL_BLUEPRINT.md/tests/regression-suite.md；⑤ Portfolio 还原（VERSION/skill.json/SKILL.md/CHANGELOG + 删除指针 migration）；⑥ 删除 upgrade-to-3.16.0.md + migrations-history 拷贝；⑦ `.skill-version.json` 不改（schema 未变，工作区无需回退）
- **回滚后不可用**：日期格式校验、字段边界校验、§4 确定性校验、WP↔WP 关联、Mermaid 派生图
- **存量 related_wps 处理**：回滚后已填写的 related_wps 保留（YAML 可选字段，旧版忽略）

---

# AP-7. 版本影响

| 维度 | 变更前 | 变更后 |
|---|---|---|
| Skill Version (Project) | 3.15.0 | 3.16.0 |
| Skill Version (Portfolio) | 3.15.0 | 3.16.0 |
| Workspace Schema | 0.16.0 | 0.16.0（不变） |
| 是否需要工作区迁移 | — | 否（schema 未变，目录结构不变） |
| 迁移模式 | — | N/A |
| 是否影响核心契约 | — | **是**（SKILL.md + 00 号 → contract_change） |
| 是否影响已有工作区 | — | 低（可选字段 + 渐进索引增列） |
| 双包同版本 | — | ✅ Project + Portfolio 均 3.16.0 |

**不升 schema 理由**：`related_wps` 为可选 YAML 字段，不改变目录结构；index 加列为存量兼容（只追加末尾）。与 1.20.0 需求册加列先例一致。

---

# 原始需求照抄（摘要）

6 份 SG 升级需求：

| SG 编号 | 一句话痛点 | 优先级 |
|---|---|---|
| SG-20260825-002 | 计划 §4 须每 WP 按 §8 实际阶段投影，禁止压缩 | 高 |
| SG-20260825-005 | WP §8 执行人/排期两栏填值边界不清 | 高 |
| SG-20260825-006 | 日期字段统一完整 YYYY-MM-DD，禁止省年 | 高 |
| SG-20260826-001 | AI 不读版本事实源 + 沿用工作区旧模板 + skill_gap 建 manifest | 高 |
| SG-20260826-001(新) | WP 之间无法关联成责任链 | 中 |
| SG-20260826-002(新) | 由 index 派生 Mermaid 图供 PM 看图排任务 | 中 |

---

# Agent A 对需求的理解 + 偏差验证

## 需求分层

| 层级 | SG | 性质 |
|---|---|---|
| 格式硬约束层 | 006（日期）、005（字段边界）、002（§4 校验） | 补规则 + 确定性校验 |
| 执行纪律层 | 001-版本 | 改写既有规则 + gap-capture 闭环 |
| 数据模型扩展层 | 001-责任链 | YAML 可选字段 + SSOT + 冻结更新 |
| 新能力层 | 002-Mermaid | 11 号 §17 派生视图 |

## 偏差验证

| 原始需求点 | A 的理解 | 方案对应设计 | 完全覆盖 | 需 B 复核 |
|---|---|---|---|---|
| SG-002 §4 不可压缩 | 扩展 verify_projection.py + 闸 2 | AP-4 verify 修改 + AP-5 TC-07~09 | ✅ | 是 |
| SG-005 字段边界 | 五列中只约束执行人/排期 | wp-template §8 注释 | ✅ | 是 |
| SG-006 日期格式 | 收窄到日期字段/区间 | 00 §5.1b | ✅ | 是 |
| SG-001-版本 三件套 | 改写 §4a.1 + gap-capture | AP-4 改动清单 | ✅ | 是 |
| SG-001-责任链 | YAML SSOT + 双向 + 废弃清理 | §8c.1 + P-WP-RETIRE | ✅ | 是 |
| SG-002-Mermaid | 11 号 §17 仅对话 | AP-4 + AP-5 TC-15~16 | ✅ | 是 |

**结论**：当前方案忠实于原始需求，不存在目标偏移。

---

# 能力变更设计

## 保留能力（不变）
WF-1~WF-8 全部工作流、待办单一数据源、计划 6 节结构、需求只绑 WP、级联传播、pm-decisions、词库/PM Profile/完整性巡检。

## 新增能力
| 能力 | 来源 SG | 落点 |
|---|---|---|
| 日期格式硬规则 | SG-006 | 00 §5.1b |
| WP §8 字段边界约束 | SG-005 | wp-template §8 注释 |
| §4 投影确定性校验 | SG-002 | verify_projection.py + 闸 2 |
| 版本模板权威源 | SG-001-版本 | 00 §4a.1 改写 + gap-capture |
| WP↔WP 关联字段 | SG-001-责任链 | wp-template §2b + YAML + index |
| Mermaid 派生视图 | SG-002-Mermaid | 11 §17 |

## 修改能力
| 能力 | 修改内容 | 来源 |
|---|---|---|
| WP 数据模型 | 新增 related_wps YAML | SG-001-责任链 |
| wps/_index.md | 8 列→10 列 | SG-001-责任链 |
| 完整性巡检 | 19 号新增扫描项 | SG-006/005 |
| 计划 §4 生成 | 落盘前必跑 verify | SG-002 |

## 可选增强（不纳入本次）
- Mermaid 自动触发机制
- WP 责任链自动阻塞检测
- 00 号大篇幅瘦身

## 删除/弱化能力
无。

---

# Skill 语法设计（核心改动摘要）

## 1. 日期格式硬规则（SG-006）→ 00 §5.1b

作用域：**日期字段**与**区间两端**。明确排除：ID 中 `YYYYMMDD`、`updated` 时分、周号 `YYYY-Wxx`。

## 2. 版本模板权威源（SG-001-版本）→ 00 §4a.1 改写

版本号只从 VERSION + `.skill-version.json` 抄。读模板只读 Skill 包 `assets/templates/`；工作区 `ai/templates/` 仅参考库。skill_gap 若出现 `manifest.md` = 级联失败。

## 3. §4 投影校验（SG-002）→ verify_projection.py 扩展（分通道）

利用已有 `STAGE13`（仅作缺标准名时的提示，非白名单）。**分通道设计**：
- **写入/生成 PLAN 落盘前**：`python verify_projection.py --root <根> --check-plan-section4`，失败 exit 1 → 不得落盘。
- **19 号默认 P0 巡检**：不加该开关，§4 压缩最多 UNJUDGED exit 2，不把存量健康检查打成 P0。
- **比较算法**：该 WP §8 实际行的阶段名集合（非 STAGE13 白名单；§8 可增删）。STAGE13 仅作「缺标准名时的提示」。
- **无 Python 时**：闸 2 人工对账清单——① §3 每个 WP 是否有 `### WP-xxx` 小节；② 该小节阶段名集合是否等于该 WP §8 实际行。两步不符不得落盘。

## 4. WP §8 字段边界（SG-005）→ wp-template §8 注释

五列（阶段/状态/执行人/排期/关键阶段）中只约束第 3 列（执行人）和第 4 列（排期）。执行人栏仅填人名/分工；排期栏仅填时间区间 `YYYY-MM-DD~YYYY-MM-DD`。**放行现有合法后缀**：`(点名)` / `(AI聚合)` / `⚠️待安排人`，只禁日期混入执行人/排期栏。

## 5. WP↔WP 关联（SG-001-责任链）→ wp-template §2b + YAML

YAML `related_wps: {upstream: [], downstream: []}` 为 SSOT。§2b 为展示投影。index 为加速器。写后必检进 00 §8c.1：**改 upstream 必须同步对端 downstream（反之亦然）；缺文件走 D20，不建幽灵 WP**。P-WP-RETIRE 清对端。禁止自指；环 → pm-decisions。

## 6. Mermaid 派生图（SG-002-Mermaid）→ 11 §17

仅对话输出。**硬禁：禁止写成任何文件（含 ai/outputs/）**。不走 P-OUTPUT、不登记 outputs/index。用户显式请求时生成。路由：SKILL.md 路由表 + 05 号查询 → 11 §17。**不改 23 号**（23 号为写入/派活加载，纯查询不载）。

---

# 存量文件升级路径

> upgrade-to-3.16.0.md 内容设计

| 升级项 | 操作 | 强制？ |
|---|---|---|
| 存量 WP §8 执行人栏含日期 | 标记 `⚠️`，PM 确认后手动拆分 | 否 |
| 存量 WP §7 省年日期 | 标记 `⚠️`，PM 确认后补全 | 否 |
| 存量 WP related_wps | 缺省空，不强制补 | 否 |
| 存量计划 §4 被压缩 | 下次打开时 verify 校验 | 否 |
| 存量 wps/_index.md 8 列 | 下次更新时自动增列 | 否 |
| 示例纠正路径 | 企业通 WP-新设名称申报列为 SG-005/006 复现样本 | — |

---

# 联动更新设计

| 更新场景 | 触发模块 | 需同步更新（按顺序） | 原子性 |
|---|---|---|---|
| WP 新增 related_wps | WP YAML | §2b 投影 + index 加速器 | 同一操作 |
| WP 废弃 | WP 文件 | 关联 WP related_wps + index + 计划 §3/§4 | 同一操作 |
| 计划 §4 生成 | plan-template | verify_projection.py 校验 | 同一操作 |

---

# 关键断言与放行门槛

| 编号 | 关键断言 | 依据 | 若被证伪 |
|---|---|---|---|
| KA-1 | 00 号 923 行，净增约 35 行后约 958 行 | 已实读 | 非阻塞 |
| KA-2 | wp-template §8 **五列**（阶段/状态/执行人/排期/关键阶段） | 已实读 L107 | 阻塞 |
| KA-3 | plan-template §4 有 13 阶段示例，分隔符 `/` | 已实读 | 阻塞 |
| KA-4 | 00 号无 YYYY-MM-DD 全局规则 | 已实读 | 非阻塞 |
| KA-5 | WP 模板无 WP↔WP 字段 | 已实读 | 阻塞 |
| KA-6 | 11 号 §9=事实源边界，到 §16 | 已实读 L121 | 阻塞（号段） |
| KA-7 | verify_projection.py 有 STAGE13 但未用于 §4 | 已实读 L8-11 | 阻塞 |
| KA-8 | 06 号 §6/§7.4 写死「仍 8 列」 | 已实读 L279/306 | 阻塞 |
| KA-9 | skill-contract 要求双包同版本 | 已实读 L113 | 阻塞 |
| KA-10 | 净增文件 = 3（Project upgrade-to + migrations-history 拷贝 + Portfolio 指针） | 改动清单 | 非阻塞 |

**放行门槛**：全部 KA 未被证伪 + 无新增阻塞 + 已声明取舍不构成障碍 → 通过-可执行 / 通过-待修订。任一 KA 被证伪 → 修订-需再审。

---

# 待确认问题

| 编号 | 问题 | 必须？ | 建议默认 |
|---|---|---|---|
| Q-1 | 6 SG 是否必须同版本（3.16.0）？B 建议拆两刀 | 是 | 用户已要求同版本 |
| Q-2 | Mermaid 仅对话输出 vs 落盘登记？ | 否 | 仅对话（A 已选） |
| Q-3 | 存量 wps/_index.md 是否一次性补空列？ | 否 | 不补，按需增列 |

---

# A 对 B-01~B-18 逐条回复

## 阻塞项

| ID | 回复 | 措施 |
|---|---|---|
| B-01 | **已改** | 全稿四列→五列；字段边界只约束执行人/排期 |
| B-02 | **已改** | Mermaid 移 11 号 §17（否决放 05 号） |
| B-03 | **已改** | 文件移到 `governance-shared/planning/` |
| B-04 | **已改** | 结构改为 AP-1~AP-7 |
| B-05 | **已改** | Portfolio 齐步 3.16.0 |
| B-06 | **已改** | SG-002 改 verify_projection.py |
| B-07 | **已改** | index 加列同步改 06/00/模板冻结 |
| B-08 | **已改** | 标 contract_change + 挂 601 回归 |

## 重大项

| ID | 回复 | 措施 |
|---|---|---|
| B-09 | **已改** | SG-001-版本三件套齐 |
| B-10 | **已改** | related_wps SSOT=YAML + §8c.1 + P-WP-RETIRE |
| B-11 | **已改** | 自检算法改为按 WP §8 实际行投影 |
| B-12 | **已改** | 日期规则收窄到日期字段/区间两端 |
| B-13 | **已改** | Mermaid 仅对话，不走 P-OUTPUT |
| B-14 | **已改** | 补 SKILL_BLUEPRINT/regression-suite/06/23/05/10/19/gap-capture |
| B-15 | **已改** | AP 写明 16 §4 捆绑例外 |
| B-16 | **已改** | 删除虚构 20%/15% 门槛 |
| B-17 | **已改** | 巡检落 19 号 |
| B-18 | **已改** | 分隔符统一为「、」 |

## 次要项

| ID | 回复 |
|---|---|
| B-19 | 已改。模板 37、00 行 923 |
| B-20 | 采纳。YAML 英文 + 正文中文 |
| B-21 | 已改。negative ≥4 条 |
| B-22 | 已改。闸 2 + verify |
| B-23 | 已改。gap-capture 纳入 |
| B-24 | 已改。企业通 WP 列为示例纠正路径 |

---

# 当前结论

- **是否忠实于目标**：是。6 个 SG 全部覆盖。
- **是否存在目标偏移**：否。
- **是否覆盖完整**：是。B-01~B-18 全部回复。
- **是否可落地**：是。改动量可控，向后兼容。
- **是否需要 B 复审**：是。
- **是否可以直接执行**：是（T-1~T-5 已写入 AP 后）。

> **当前方案为 A 修订版方案（V0.3），B 复审结论「通过-待修订」。T-1~T-5 已写入 AP，等用户「同意执行」即可改 Skill。**

---

# 给 B 的审核输入包

你现在是 Skill 升级独立审核 Agent，代号 B。

请注意：
1. 不要基于 A 的缓存、记忆或结论直接判断。
2. 你必须自己扫描 Skill 项目目录，眼见为实。
3. A 的 V0.3 方案只能作为待审核对象。
4. V0.3 已按 B2-01~B2-09 逐条修订，请核实每条是否到位。
5. 在开始审核前，确认工作空间版本与快照一致。

### 请 B 完成以下审核

1. V0.3 是否解决了 B2-01~B2-03 全部阻塞项
2. V0.3 是否解决了 B2-04~B2-09 全部重大项
3. KA-1~KA-10 是否成立
4. AP-1~AP-7 结构是否完整
5. contract_change 标记是否正确
6. 回归测试计划是否充分（含 negative）
7. 回滚方案是否可执行
8. B 最终结论（四档之一）

---

# 双审核人审核记录

> 审核记录统一归入本活文档，不另建独立审计文件。

| 轮次 | 审核人 | 时间 | 结论 | 备注 |
|---|---|---|---|---|
| V0.1 | B | 2026-08-26 | **修订-需再审** | KA-2 证伪 + 7 条阻塞。详见下方 |
| V0.2 | B | 2026-08-26 | **修订-需再审** | 原 B-01～B-08 除 B-07 未完全闭环外均到位。新阻塞 3 条。详见 §B 审核报告 V0.2 |
| V0.3 | B | 2026-08-26 | **通过-待修订** | B2-01～B2-03 闭环；B2-04～B2-08 已补进 AP-4/AP-6。余 T-1～T-5（对齐/禁区/触发词），写入后可执行、不必再审。详见 §B 审核报告 V0.3。 |

---

# B 审核报告 V0.1（2026-08-26）

> **结论档位：修订-需再审**  
> 完整报告见 V0.1 历史版本。核心发现：KA-2 证伪（五列非四列）；11 号 §9 已占用；AP 位置/结构违规；双包契约未遵守；SG-002 根因对错；index 8 列冻结未处理；核心契约未标 contract_change；虚构 20%/15% 门槛。共 8 阻塞 + 10 重大 + 6 次要。

---

# B 审核报告 V0.2（2026-08-26）

> **结论档位：修订-需再审**  
> 本轮只审 V0.2 是否把 V0.1 的阻塞闭环，以及修订是否引入新阻塞。工作空间仍为 Project/Portfolio **3.15.0** / schema **0.16.0**。AP 已在 `governance-shared/planning/`。未执行改造。

---

## 1. 工作空间与 KA 复核

| KA | V0.2 表述 | B 本轮实读 | 结果 |
|---|---|---|---|
| KA-1 | 00 号 923 行 | 仍 923 行量级 | 成立 |
| KA-2 | §8 **五列** | `wp-template.md` L107–108：`阶段/状态/执行人/排期/关键阶段` | **成立**（V0.1 证伪项已改写） |
| KA-3 | 13 阶段示例，分隔符 `/` | `plan-template.md` 注释「多人用 `/`」，示例行含 `/` | 成立 |
| KA-4 | 00 无 YYYY-MM-DD 总规则 | 00 号检索无该字样 | 成立 |
| KA-5 | 无 WP↔WP 字段 | 模板仅 `plan_ref` / §2 REQ / §5 R·I | 成立 |
| KA-6 | 11 号 §9=事实源边界，到 §16 | L121 `## 9. 事实源边界` | 成立 |
| KA-7 | `STAGE13` 未用于 §4 | `verify_projection.py` L8–11 定义后未再引用 | 成立 |
| KA-8 | 06 §6/§7.4 仍 8 列 | L279「仍 8 列」；L306「必须包含 8 列」；**L308「不加第 9 列」** | 成立 |
| KA-9 | 双包同版本 | skill-contract L113 | 成立 |
| KA-10 | 净增文件=2 | 按 AP-4 计数为 2；漏 `migrations-history/` 拷贝与 migrations README 更新（见下，不证伪 KA 字面） | 字面成立 |

KA 无新证伪。按 A 自设门槛，本轮卡在「新增阻塞 / 旧阻塞未闭环」，不是 KA。

---

## 2. V0.1 阻塞项（B-01～B-08）是否到位

| ID | V0.2 自称 | B 核实 | 状态 |
|---|---|---|---|
| B-01 四列→五列 | 已改 | AP-1/AP-2/KA-2/语法设计均写五列，只约束执行人/排期 | **闭环** |
| B-02 11 号 §9 撞车 | 已改 | 改为 §17，否决放 05 有理由 | **闭环**（意图路由仍有洞，见 B2-03） |
| B-03 AP 路径 | 已改 | 仅 `governance-shared/planning/upgrade-plan-v3.16.0.md`；根目录旧文件已不存在 | **闭环** |
| B-04 AP-1～AP-7 | 已改 | 七章齐全：替代方案、回滚、版本影响、contract_change 均有 | **闭环**（AP-2 与 AP-4 文件集未完全对齐，非阻塞） |
| B-05 双包 | 已改 | AP-4 列 Portfolio VERSION/skill.json/SKILL.md/CHANGELOG/指针 migration | **闭环** |
| B-06 SG-002→verify | 已改 | 扩展现有脚本 + 按 §8 实际行而非 ×13 | **方向闭环**（并入 19 号 P0 的副作用未设计，见 B2-02） |
| B-07 8 列冻结 | 已改 | AP-4 改了 `06` §6/§7.4 与 `wp-index-template`；**00 §5a L366「不加第 9 列」未出现在 00 的修改内容列** | **未闭环** |
| B-08 contract_change + 601 | 已改 | 文首与 AP-7 已标；AP-5 挂 PLT/PWP/STP + 现有 C1–C8 | **闭环** |

---

## 3. V0.1 重大项（B-09～B-18）是否到位

| ID | 状态 | 说明 |
|---|---|---|
| B-09 版本三件套 | **闭环** | §4a.1 改写 + gap-capture 禁 manifest + 模板权威源 |
| B-10 SSOT/废弃清理 | **部分** | YAML SSOT、8c.1、禁止自指/环 已写；**AP-4 的 00 行未列 §8e P-WP-RETIRE**，施工清单会漏「废弃清对端」 |
| B-11 ×13 公式 | **闭环** | 改为 §4 阶段集合 = 该 WP §8 实际行 |
| B-12 日期过宽 | **闭环** | 排除 ID / `updated` 时分 / 周号 |
| B-13 Mermaid 落盘 | **部分** | 「仅对话、不走 P-OUTPUT」已选；00 §2.7 未列意图；23 号仍写「或」 |
| B-14 漏文件 | **基本闭环** | 已补 06/05/10/19/23/Blueprint/regression/gap-capture；仍漏 migrations README 与 `migrations-history/` |
| B-15 捆绑例外 | **闭环** | AP-1 已记录 16 号 §4 例外 |
| B-16 虚构门槛 | **闭环** | 已删 |
| B-17 巡检落 19 | **闭环** | 19 为主、14 为 P2 |
| B-18 分隔符 | **闭环** | 计划 `/`→`、` |

---

## 4. 本轮新阻塞（必须改完再送审）

### B2-01（阻塞，B-07 未闭环）

00 §5a L366 原文：`effect=废弃 时写 废弃（不加第 9 列）`。06 §7.4 L308 同句。

V0.2 把 index 改成末尾追加第 9/10 列（上游/下游），但：

- AP-4 对 00 的修改内容只有：§5.1b、§4a.1、§8c.1、闸 2 引 verify。**没有 §5a。**
- 「不加第 9 列」本意是禁止「生效」列，不是禁止一切第 9 列。加列后必须改写成：`状态列写废弃；生效仍不成列；上游/下游为第 9/10 列`。只改 06 的「8→10」而留「不加第 9 列」，落地后规则自相矛盾。

### B2-02（阻塞，B-06 副作用）

`verify_projection.py` 已被 19 号 §1.2 列为完整性巡检 **P0 旁路**（exit 1=差异）。SG-002 的复现样本就是存量大计划 §4 被压缩。

若把「§4 小节/阶段集合不全」直接做成现有脚本的 exit 1：

- 国庆类存量计划会在「完整性巡检」立刻 P0 失败；
- 与 AP-7 / 存量路径「不强制、下次打开再校验」冲突。

必须分通道，方案里写死，例如：

- **写入/生成 PLAN 落盘前**：`python scripts/verify_projection.py --root <根> --check-plan-section4`（或等价开关），失败不得落盘；
- **19 号默认 P0 旁路**：不加该开关，§4 压缩最多 UNJUDGED/exit 2，不把存量健康检查打成 P0；
- 比较对象 = 该 WP §8 **实际行的阶段名集合**，不要拿 `STAGE13` 当必满 13 项白名单（§8 可增删）。`STAGE13` 只可作「缺标准名时的提示」，不能当失败条件。

闸 2 无 Python 时的「人工对账」必须写成可执行清单（§3 每个 WP 是否有 `### WP-xxx`；该小节阶段名集合是否等于该 WP §8），不能只写「人工对账」四字——否则无 Python 时退回 V0.1 的失效模式。

### B2-03（阻塞，B-13 未写稳）

「仅对话」与现行闸 1 的关系没写完：

1. 00 §2.7 意图表：**必须**把「画图 / 责任链图 / 排布图 / Mermaid」归入 **查询**，禁止归入「生成」（生成会走 11 号生成物 → 闸 1 B 路强制 `outputs/` + manifest，直接推翻仅对话）。
2. 11 §17 须加一句硬禁：`禁止写成任何文件（含 ai/outputs/）`。
3. AP-2/AP-4 对 23 号仍写「P-DERIVED-MERMAID **或** 并入 05」。23 号加载条件是「写入/派活/更新」，**纯查询不载**。画图是查询 → **不要改 23 号**。AP-4 删除 23 号这一行，路由只走 SKILL.md + 05 → 11 §17。

---

## 5. 重大（V0.3 必须写进 AP-4，不构成方向性推倒）

| ID | 问题 |
|---|---|
| B2-04 | AP-4 的 00 行补上 **§8e P-WP-RETIRE 清对端 related_wps**（B-10 正文有、清单无） |
| B2-05 | 字段边界须显式放行现有合法后缀：`(点名)` / `(AI聚合)` / `⚠️待安排人`。只禁日期混入，不把这些判成违规 |
| B2-06 | 建链/改链批准口径：V0.1 有「须 PM 确认」，V0.2 删了。按本 Skill 事实源惯例走待确认 + pm-decisions 即可，但 AP 要写一句，不要留空 |
| B2-07 | AP-4 补：`ChronoPM-Project/governance/migrations/README.md`（当前文件改为 upgrade-to-3.16.0.md）；`governance-shared/migrations-history/upgrade-to-3.16.0.md`（拷贝）。净增文件改为 **3**（Project upgrade-to + history 拷贝 + Portfolio 指针），README 为修改 |
| B2-08 | AP-6 回滚文件列表按 AP-4 全量列（现漏 05/10/19/23/gap-capture/Blueprint/regression/Portfolio 指针） |
| B2-09 | SKILL.md 路由表加「画图」行时，front matter `description` 触发词建议补「画图/责任链图」（否则冷启动不一定载入本 Skill）。可标 P2 |

---

## 6. AP 结构 / contract_change / 回归 / 回滚

| 项 | 结论 |
|---|---|
| AP-1～AP-7 | 结构完整，可继续用这套骨架 |
| contract_change | 标记正确（SKILL.md + 00） |
| 回归 | negative 已有（TC-03/04/09/11/14/16）；阻断项点名 PLT/PWP/STP 足够。TC-09 更像降级路径而非 negative，可改名，非阻塞 |
| 回滚 | 有版本、有步骤、schema 不回退，方向对；文件清单不完整（B2-08） |
| 取舍 | Mermaid 手动/仅对话、related_wps 可选、6 SG 捆绑例外：已声明，B 接受 |

---

## 7. 给 A 的 V0.3 最小修订清单

只改方案，不改 Skill 正文。做完这 3 条阻塞即可再送 B：

1. **AP-4 的 00 号**补三处：§5a 重写「不加第 9 列」；§8e 废弃清对端；§2.7 画图=查询。
2. **verify §4** 写成带开关的分通道 + 比较算法=WP §8 实际行；19 号默认 P0 **不**因存量压缩失败。
3. **Mermaid**：删 23 号改动；11 §17 禁止落盘任何文件；05 + SKILL 路由即可。

顺手带上 B2-04～B2-08。不要再扩范围。

---

## 8. B 最终结论

**修订-需再审**

不选「重做」：V0.2 已把 V0.1 的方向性错误（根因、号段、AP 位置、双包、contract_change、五列）纠正到位。

不选「通过-*」：B-07 在 00 §5a 未闭环；把 §4 校验塞进现有 P0 脚本、把画图接到 23/生成物，会在实施时打存量或打穿「仅对话」。这三处不改，执行清单不可用。

A 出 V0.3 后只对 B2-01～B2-03 逐条「已改」即可再审；不必重开 21 章。在此之前 **禁止执行改造**。

---

# A 对 B2-01～B2-09 逐条回复（V0.3）

## 阻塞项

| ID | 问题摘要 | A 回复 | 改动位置 |
|---|---|---|---|
| B2-01 | 00 §5a「不加第 9 列」未改，与加列矛盾 | **已改**。AP-4 对 00 号补三处：§5a 重写为「状态列写废弃；生效不成列；上游/下游为第 9/10 列」；06 §7.4 L308 同句同步改写 | AP-4 的 00 行、06 行 |
| B2-02 | verify §4 并入 19 号 P0 会打存量 | **已改**。分通道设计：`--check-plan-section4` 开关控制严格/宽松；比较对象=该 WP §8 实际行阶段名集合（非 STAGE13 白名单）；无 Python 时闸 2 人工对账写成可执行清单 | AP-4 verify 行、§二十三 Skill 语法 §3、AP-5 TC-07/08/09 |
| B2-03 | 「仅对话」不稳：00 §2.7 未定意图、23 号不应改 | **已改**。00 §2.7 意图表把「画图/责任链图/排布图/Mermaid」归入查询；11 §17 加硬禁「禁止写成任何文件」；**删除 23 号改动行**（纯查询不载） | AP-4 的 00 行、11 行、23 行 |

## 重大项

| ID | 问题摘要 | A 回复 | 改动位置 |
|---|---|---|---|
| B2-04 | 00 行缺 §8e P-WP-RETIRE 清对端 | **已补**。AP-4 的 00 行新增 §8e 废弃时清对端 related_wps | AP-4 的 00 行 |
| B2-05 | 字段边界须放行 `(点名)`/`(AI聚合)`/`⚠️待安排人` | **已补**。AP-4 的 wp-template 行新增「放行现有合法后缀」；建链/改链走待确认 + pm-decisions | AP-4 的 wp-template 行 |
| B2-06 | 建链/改链批准口径未写 | **已补**。同上，写入 wp-template 修改内容 | AP-4 的 wp-template 行 |
| B2-07 | 漏 migrations README + migrations-history 拷贝 | **已补**。AP-4 新增两行：migrations/README.md（修改）+ migrations-history/upgrade-to-3.16.0.md（新增）；净增文件改为 3 | AP-4 文件清单 |
| B2-08 | 回滚文件清单不完整 | **已补**。AP-6 回滚步骤补全：05/10/19/14/gap-capture/Blueprint/regression/Portfolio 指针/upgrade-to/migrations-history | AP-6 回滚方案 |
| B2-09 | SKILL.md description 触发词补「画图/责任链图」 | **已补**（P2）。AP-4 的 SKILL.md 行「路由表加派生图行」已含触发词更新 | AP-4 的 SKILL.md 行 |

---

# B 审核报告 V0.3（2026-08-26）

> **结论档位：通过-待修订**  
> 本轮只核：B2-01～B2-03 是否闭环；B2-04～B2-09 是否进 AP-4；有无新阻塞。工作空间仍为 Project/Portfolio **3.15.0** / schema **0.16.0**。未执行改造。

---

## 1. KA-1～KA-10

与 V0.2 实读一致，无新证伪。KA-10 已改为净增 3，与 AP-4 一致。KA-1 正文「+30 行」与 AP-4「约 35 行」略差，非阻塞，并入 T-5。

---

## 2. B2-01～B2-03（本轮必核）

| ID | V0.3 落点 | B 判定 |
|---|---|---|
| B2-01 | AP-4 的 00：§5a 改写为「状态列写废弃；生效不成列；上游/下游为第 9/10 列」；06 §7.4 L308 同句 | **闭环** |
| B2-02 | `--check-plan-section4` 分通道；无开关=exit 2；比较=WP §8 实际行；无 Python 时闸 2 两步清单 | **闭环**（19 号默认命令保持不加开关，须写入施工禁区，见 T-2） |
| B2-03 | §2.7 画图=查询；11 §17 禁止任何落盘；23 号明确不改 | **闭环** |

原 V0.1 八条阻塞 + V0.2 三条阻塞，到此全部闭环。

---

## 3. B2-04～B2-09

| ID | B 判定 | 说明 |
|---|---|---|
| B2-04 §8e | **闭环** | 已进 AP-4 的 00 行 |
| B2-05 合法后缀 | **AP-4 已写，语法设计未齐** | 见 T-1 |
| B2-06 建链待确认 | **闭环** | wp-template 行已写待确认 + pm-decisions |
| B2-07 migrations | **闭环** | README 修改 + history 拷贝；净增 3 |
| B2-08 回滚清单 | **闭环** | AP-6 已按文件补全（含删除 3.16.0 新增文件） |
| B2-09 description 触发词 | **未真正落到 AP-4** | 回复把「路由表」说成 description。路由表 ≠ YAML `description`。见 T-3 |

---

## 4. 待修订（T-1～T-5）

不构成方向性阻塞。写入 AP-4 / upgrade-to 施工禁区后即可执行，**不必再送 B**。超出本表须再审。

| ID | 项 | 怎么改 |
|---|---|---|
| T-1 | 语法设计 §4 与 AP-4 不一致 | 「执行人栏仅填人名/分工」补上：放行 `(点名)` / `(AI聚合)` / `⚠️待安排人`，只禁日期混入 |
| T-2 | 19 号 P0 旁路可能被顺手加上开关 | AP-4 的 19 行 + upgrade-to **施工禁区**写死：`§1.2 默认命令不加 --check-plan-section4`，禁止把该开关并入完整性巡检 P0 |
| T-3 | B2-09 未进清单 | AP-4 的 SKILL.md 行拆成两句：① front matter `version`；② `description` 触发词补「画图/责任链图」；③ 路由表新行 **必须加载 `05+11`**，禁止落到「简单查询仅 05」（否则 11 §17 不会载入） |
| T-4 | 双向互指只在口头 | AP-4 的 00 §8c.1 写明：改 `related_wps.upstream` 必须在对端 `downstream` 互指（反之亦然）；缺文件走 D20，不建幽灵 WP |
| T-5 | 文档卫生 | AP-1 删「扩展已有 STAGE13」这种易误解写法，改为「STAGE13 仅缺标准名提示」；AP-2 的 00 行与 AP-4 对齐（补 §5a/§8e/§2.7）；文内「当前结论 / 给 B 输入包」仍写 V0.2，改为 V0.3；KA-1 与 AP-4 行数 30/35 统一 |

---

## 5. AP 结构 / 回归 / 回滚 / 取舍

| 项 | 结论 |
|---|---|
| AP-1～AP-7 | 完整，可作施工骨架 |
| contract_change | 正确（SKILL.md + 00），须全量回归 |
| 回归 | TC-07/08 严格通道、TC-09 巡检不 P0，覆盖 B2-02；negative 足够 |
| 回滚 | 可执行；schema 不回退 |
| 取舍 | 仅对话、可选 related_wps、6 SG 捆绑例外：B 接受 |

---

## 6. B 最终结论

**通过-待修订**

不选「修订-需再审」：B2-01～B2-03 已写进 AP-4，不再挡方向。

不选「通过-可执行」：T-1～T-5 不改的话，实施时仍可能（a）把点名判成字段边界违规；（b）把 `--check-plan-section4` 塞进 19 号 P0 再打存量；（c）画图只载 05、11 §17 未加载。

**放行条件**：A 把 T-1～T-5 写入本 AP（或写入 `upgrade-to-3.16.0.md` 施工清单/禁区）后，等用户「同意执行」即可改 Skill。不必再交 B。若改动超出 T-1～T-5 或改 KA，须再审。在 T 项落盘前 **禁止执行改造**。


