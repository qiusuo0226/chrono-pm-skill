# 跨源需求归集与判定方案（Requirement Intelligence, RI）— V0.4

> 版本：V0.4（Agent A 修订版，已处理 B 三次审核意见，待 B 四次复核）
> 上一版：V0.3
> 目标：为 ChronoPM 设计"AI 存储、拆词、合并、检索"的跨源需求管理方案，解决
> "需求是否在合同/招投标/立项范围内"的取证扯皮问题。
> 本版修订：新增三级索引 + 分级加载 + 覆盖索引（解决索引效率）；P1 语义兜底三层机制；
> scope_scope 归属修正到 Canonical 层；L5 authority 默认值声明；ATOM 提取触发时机；registry 变更迁移。

---

## 一、B 三次审核意见处理清单（V0.3 → V0.4）

| B 编号 | 级别 | 问题 | 采纳 | 修订动作 |
|--------|------|------|------|----------|
| H-I1 | 高 | 索引规模管理 + AI 分级加载缺失 | ✅ | 新增 §7.1 三级索引 + 分级加载 + 覆盖索引 |
| M-I2 | 中 | P1 语义检索兜底缺失 | ✅ | §7.1 三层兜底（词库扩展→norm_text 扫读→降级提示） |
| M-I3 | 中 | scope_scope 不应在 ATOM 层 | ✅ | §5 从 ATOM 移除 scope_scope，仅 Canonical 层保留 |
| M-I4 | 中 | L5 authority 默认值缺失 | ✅ | §3 source_category 声明 L5 归属（operational 工期/里程碑条款默认 L5） |
| L-I5 | 低 | ATOM 提取触发时机未声明 | ✅ | §9 主/辅助/增量三触发 |
| L-N3 | 低 | file_registry.py 未单列清单 | ✅ | §10 补齐 |
| L-N4 | 低 | registry 变更后已建 ATOM 迁移规则缺失 | ✅ | §8 新增 source_type 更名/类型变更的迁移一致性规则 |

---

## 二、原始需求照抄

> 规划一个新需求：在规划大型项目的时候，总是会遇到，'需求在不在合同范围内'，'需求在不在招投标文件内'，'需求在不在立项需求范围内'，总是容易出现扯皮的情况。这涉及到多个文件的需求合并，归档以及整理。帮我想一想，包括合同项目要求，如何存储记录调用。比如密评要求，以及各种时间里程碑节点的重要规划。帮我设计一个 ai存储、拆词、合并、检索的方案。

## 三、可扩展的源文档类型体系（修订 M-I4）

**双层分类**：`source_category`（固定 6 类）+ `source_type`（项目级可扩展，`source-type-registry.md` 声明）。

| source_category | 语义 | 默认 authority | 覆盖的典型文档 |
|----------------|------|---------------|----------------|
| `contractual` | 合同/协议类 | L1 | 合同正文、附件/补充协议、变更签证、采购订单 |
| `procurement` | 招投标类 | L2 | 招标文件、补遗/答疑、投标文件、评标报告 |
| `approval` | 立项审批类 | L3 | 可研、立项批复、项目建议书、初步设计 |
| `compliance` | 合规标准类 | L4 | 密评/等保、国标/行标、政策法规、审计整改 |
| `technical` | 技术文件类 | L3（基线化后） | 需求规格说明、总体/详细设计、接口规范、专家评审意见、验收标准、数据迁移方案 |
| `operational` | 运维约定类 | L2-L3（工期/里程碑条款默认 **L5**） | 运维SLA、培训要求、监理通知、甲方指令性纪要、工作联系单、备忘录、**工期/里程碑条款** |

**L5 归属声明（修订 M-I4，方案 A）**：authority 保持 L1~L5。`L5`（工期/里程碑）默认归属 `operational` 类别中的"工期条款/里程碑约定"条目；一个 source_type 若主要为工期约束，可在 registry 中声明 `authority: L5`，否则默认 L3。设计上保留 L5 独立层级，因工期条款的效力源于合同且影响验收门禁，值得单独标记。

**设计原则**：
- `source_category` 固定 6 类 → authority 推断与跨项目对比稳定。
- `source_type` 项目级可扩展 → 新类型只需 registry 声明，不改规则文件。
- 每个 `source_type` 归入一个 `source_category`，继承默认 authority，可用 `覆盖默认？` 列显式覆盖。
- ATOM `source_type` 引用 registry；未知类型触发"未登记"提示。

### 目录结构（扁平 + 索引分组）
```
requirements/
├── requirement-register.md        # REQ 管理层（现有）
├── source-type-registry.md       # 源类型登记（项目级可扩展）
├── canonical/                    # Canonical 归并层
│   ├── canonical-index.md
│   └── {canonical_id}.md
├── atoms/                        # ATOM 证据层（三级索引，见 §7.1）
│   ├── atom-index.md             # L1 主索引（路由，~6 行）
│   ├── contractual-index.md      # L2 类别倒排索引（6 个）
│   ├── contractual.md            # L3 ATOM 全文（6 个 category 文件）
│   ├── procurement-index.md / procurement.md
│   ├── approval-index.md / approval.md
│   ├── compliance-index.md / compliance.md
│   ├── technical-index.md / technical.md
│   └── operational-index.md / operational.md
└── change-log.md                 # 需求变更（现有）
```
单个 ATOM 类别文件超 300 行时按 06 号 §6.1 拆分（Level 2 索引按 source_type 分片，如 `technical-design_spec-index.md`）。

---

## 四、双层来源分类

| 层 | 字段 | 粒度 | 取值 | 用途 |
|----|------|------|------|------|
| REQ（现有） | `来源` | 粗粒度 | contract / document / meeting / implied（07 号 §1.3，不变） | 管理级来源说明 |
| ATOM（新增） | `source_type` | 细粒度 | registry 中的值 | 证据层按来源检索、分组 |

REQ 通过 `canonical_id` 间接关联 Canonical，Canonical 聚合 ATOM 的细粒度 source_type。07 号声明双层关系不合并。

---

## 五、三层数据模型 + ATOM 字段（修订 M-I3）

```
源文档（任意 source_type，registry 可扩展）
  → AI 切块抽取 ATOM（证据层，只读，raw_text≤500字 + 指针）
  → 语义归并 Canonical（归并层，evidence 证据链 + scope_scope + conflict）
  → REQ 登记册（管理层，关联任务/里程碑/变更/验收，不变）
```
- `Canonical 1:N ATOM`；`REQ 1:1 Canonical`（默认）+ `Canonical 1:N REQ`（canonical_id 回指）。
- `来源/Source` 升级为 Canonical ID 指针（旧工作区仍为自由文本，向后兼容）。

### ATOM 字段定义（修订 M-I3：移除 scope_scope）

```
ATOM_ID         : ATOM-<source_type>-NNN
kind            : requirement / requirement_directive / agreement / constraint
source_doc      : 文档名
source_version  : 源文档版本号（stale 检测基准）
source_ref      : 条款号 / 章节 / 页码
source_type     : registry 细粒度类型
source_category : contractual / procurement / approval / compliance / technical / operational
authority       : L1~L5（由 source_category 默认值推断，可覆盖）
raw_text        : 条款级原文（≤500 字；超长拆分为多条 ATOM）
supersedes      : 长条款拆分时，指向同一条款的拆分前/后 ATOM_ID（锚定拆分血缘）
norm_text       : 语义归一后的标准表述（AI 生成，confidence 记录，人工确认）
keywords        : 拆词四元组 [对象][动作][约束][指标]
confidence      : AI 归一/匹配置信度
milestone       : 关联里程碑 M-NN（若有）
hash            : 防篡改摘要
updated         : 时间戳
```

> **scope_scope 归属修正（M-I3）**：scope_scope 是**跨源聚合结论**，只属于 Canonical 层（其 evidence 聚合了多条 ATOM 后才能判定范围）。单个 ATOM 只需 `authority` + `source_category` 表达单条证据效力，**不设 scope_scope**。

### Canonical 字段定义
```
CAN_ID          : CAN-NNN
evidence        : ATOM_ID 证据链（1:N）+ 各自 source_type/authority
scope_scope     : in_contract / in_bid_only / in_initiation_only / not_in_scope / conflict
consistency     : consistent / conflict（来源互斥转人工裁决）
milestone       : 关联里程碑、合规门禁
status          : active / evidence_stale（见 §8）
```

---

## 六、全链路需求/要求/约定/约束的跟踪拆解

| 内容类型 | 来源示例 | 处理 |
|---------|---------|------|
| 需求（Requirement） | 合同条款、需求规格、竞标承诺 | ATOM → Canonical → REQ，scope_scope 判定 |
| 要求（Requirement directive） | 立项批复要求、甲方指令性纪要 | 同上，source_type 记录 |
| 约定（Agreement） | 接口约定、数据格式约定、乙方承诺 | 同上，kind=agreement |
| 约束（Constraint） | 密评/等保、国标行标、技术选型、工期约束 | ATOM 落 compliance/technical，密评带强制门禁，工期关联里程碑 |

统一用 ATOM schema（`kind` 字段），同一套拆词→归一→归并→检索链路。

---

## 七、拆词与归一的 ES 分析链（继承 V0.3）

Character Filter(17纠错) → Tokenizer(AI原子化) → Token Filter(17归一+四元组) → 同义词(domain-glossary) → 倒排索引(atom-index)。术语级归一(17 状态机，keywords) 与 句子级归一(LLM 生成 norm_text，不入 17 状态机，confidence 记于 ATOM，人工确认) 边界在 17 号 §6.4 声明。

## 七.1 三级索引 + 分级加载（修订 H-I1 + M-I2）

**三级索引结构（解决索引效率）**：

| 级别 | 文件 | 内容 | 加载时机 | 典型大小 |
|------|------|------|---------|---------|
| L1 主索引 | `atom-index.md` | 路由表：category / ATOM 总数 / 文件位置 / 最近更新 | 查询起点 | ~6 行 |
| L2 类别倒排 | `{category}-index.md` | keyword / ATOM ID / **norm_text 摘要** / source_type | 定位目标类别后 | 50-200 行 |
| L3 ATOM 全文 | `{category}.md`（可分片） | raw_text + evidence 细节 | 仅在 L2 命中后 | 逐条 1-3 行 |

**分级加载策略（与 05 号 §6.1 最小读取对齐）**：
1. 加载 L1 `atom-index.md` → 判断搜索哪些 category（~6 行）
2. 加载目标 `{category}-index.md` → keyword + norm_text 摘要定位候选（50-200 行）
3. 仅加载命中的 ATOM 全文（3-5 条）→ 看 raw_text + evidence
4. 关联 Canonical → scope_scope + 证据链

总加载 200-400 行，而非全量扫描所有 category 文件。

**覆盖索引（Covering Index）关键**：Level 2 索引含 `norm_text` 摘要列，**AI 读索引即可理解每条 ATOM 语义，无需加载全文做初步筛选**——这是效率提升的核心，也是语义兜底的基础。

**P1 语义兜底三层机制（修订 M-I2，解决"AI 检索不全"）**：
1. **词库同义词扩展**：查询前查 17 号 domain-glossary，把查询术语扩展到所有 confirmed 同义词再匹配（如"身份认证"→"用户登录/登录认证"）。
2. **norm_text 语义扫读**：用 L2 索引的 norm_text 摘要做语义理解定位（非精确关键词），AI 读摘要即判相关性。
3. **降级提示**：均未命中时输出"当前关键词索引未命中，建议：①换关键词 ②检查词库同义词 ③P2 向量检索增强"，不臆造结果。

---

## 八、workspace schema 0.7.0 与联动一致性（修订 L-N4）

**workspace schema 升级**：
- `skill.json`：`current` 0.6.0→0.7.0；`migrations` 追加 0.6.0→0.7.0 条目（canonical/atoms/source-type-registry 目录）。
- `scripts/_version.py`：`WORKSPACE_SCHEMA_VERSION` → 0.7.0。
- `scripts/migrate_workspace.py`：新增 0.7.0 迁移（创建 canonical/、atoms/ 6 类别文件 + 6 个 L2 索引 + L1 主索引 + source-type-registry.md，单/项目集模式）。
- `scripts/chronopm_init/`：`config.py`/`file_registry.py` 初始化新增这些目录。

**联动一致（原子性）**：
- ATOM 变更 → 同一操作内重建其 Canonical 证据链 + 更新对应 L1/L2 索引；失败整体回退标记 stale。
- stale 检测：ATOM `source_version` + 索引 `last_source_version` 比对；源文档新版本触发。
- `evidence_stale`：Canonical 的所有 ATOM 均 stale 时，Canonical 标记 `evidence_stale`，提示 PM 重新评估证据基础。

**registry 变更迁移（修订 L-N4）**：当 `source-type-registry.md` 中某 source_type 被更名/改归 category/改 authority 时，必须在一同操作内：
1. 更新 registry 条目；
2. 重写受影响 ATOM 的 `source_type`/`source_category`/`authority` 字段并重算 hash；
3. 同步刷新 L1/L2 索引；
4. 若分类变化跨 category，迁移该 ATOM 到目标 category 全文文件；
5. 任一失败整体回退并标记 stale。禁止"只改 registry 不同步 ATOM"的延迟模式。

---

## 九、PM 随笔双入口 + ATOM 提取触发时机（修订 L-I5）

**PM 随笔**：`ai/projects/{子项目}/context/project-notes.md`（项目集 `ai/portfolio/context/project-notes.md`），只追加时间线，每条 `日期 / 标签 / 内容 / 来源`，标签 `#方法论 #干系人 #洞察 #策略 #风险直觉`。
- 入口 1 PM 主动要求：直接追加。
- 入口 2 AI 主动感知：四类信号（方法论/干系人/洞察/策略）→ 附加"💡 检测到 N 条候选备忘，是否记入 project-notes？"→ 确认写入、否定不记录、不阻塞主流程。
- 与 project-context（结构化背景）/ decision-log（正式决策）/ lessons-learned（复盘产出）边界清晰。

**ATOM 提取触发时机（修订 L-I5，写入 07 号新增章节）**：
- 主触发：PM 主动提供源文档（上传/粘贴/指定路径）并要求"提取需求/拆解/归集"。
- 辅助触发：初始化向导（18 号）Step 1（合同层）引导 PM 录入合同时同步提取；Step 2 起允许登记 registry 各 source_type。
- 增量触发：PM 告知"合同出了补充协议 / 招投标补遗 / 新增某文档"时，仅对新版本增量提取 ATOM 并触发 stale 判定。

---

## 十、文件级改动清单（修订 L-N3，完整版）

| 文件路径 | 操作 | 内容 |
|---------|------|------|
| `references/07-requirement-rules.md` | 修改 | 新增 §8 跨源证据链+ATOM schema、§9 提取触发+归并流程、§10 范围判定+双层来源分类、§10a ATOM 提取触发时机 |
| `references/17-domain-glossary-rules.md` | 修改 | §6.4 术语级 vs 句子级归一边界 |
| `references/05-query-rules.md` | 修改 | §2/Quick Query 新增"跨源范围判定、需求归集"查询行 + 分级加载对齐说明 |
| `references/00-pm-main-rules.md` | 修改 | §2.7 意图检测新增 RI 意图 + 备忘建议输出点 |
| `references/06-file-rules.md` | 修改 | §2.1 事实源清单新增 canonical/atoms(L1+L2+L3)/source-type-registry；§9 归档表新增 ATOM/Canonical；§6 拆分阈值适配 |
| `assets/templates/requirement-register-template.md` | 修改 | 新增 `Canonical ID` + `scope_scope` 列（与优先级解耦） |
| `assets/templates/milestone-board-template.md` | 修改 | 里程碑总览表新增"合规门禁"列 |
| `assets/templates/index-formats.md` | 修改 | 新增 L1 主索引/L2 类别倒排/L3 全文 + Canonical 索引 + source-type-registry 格式 |
| `assets/templates/domain-glossary-template.md` | 修改 | 补充密评/等保/招投标初始词条 |
| `assets/templates/source-type-registry-template.md` | 新增 | 源类型登记模板 |
| `assets/templates/project-notes-template.md` | 新增 | 项目备忘录模板 |
| `SKILL.md` | 修改 | 路由表新增 RI 查询/归集行 |
| `skill.json` | 修改 | schema 0.7.0 + migrations；versionHistory；CAP 更新 |
| `SKILL_BLUEPRINT.md` | 修改 | §5.2 CAP 更新 + §8 数据流 + §11.3 版本行 |
| `governance/contracts/skill-contract.md` | 修改 | 事实源清单新增目录；Protected Capabilities 增补 |
| `CHANGELOG.md` | 修改 | 版本记录 |
| `tests/regression-suite.md` | 修改 | 新增 Module 32 RI(RI-001~RI-012，含索引分级) + Module 33 Project Notes(PN-001~PN-004) |
| `scripts/_version.py` | 修改 | WORKSPACE_SCHEMA_VERSION → 0.7.0 |
| `scripts/migrate_workspace.py` | 修改 | 新增 0.7.0 迁移步骤（含 L1/L2 索引初始化） |
| `scripts/chronopm_init/config.py` | 修改 | 初始化 canonical/atoms/registry 目录 |
| `scripts/chronopm_init/file_registry.py` | 修改 | 文件注册表登记 canonical/atoms 各文件与索引 |（修订 L-N3）

**不新增**：独立规则文件、独立 CAP、独立状态机（scope_scope `/evidence_stale` 作字段值）。

## 十一、复杂度、风险与边界

- 复杂度：Minor + schema 变更（含迁移脚本），需 CR 工单 + 全量回归。
- 风险：AI 归一误合并→冲突仲裁保人工确认；scope 结论仅辅助，以合同原文/法务为准；证据链依赖来源版本登记；**索引一致性依赖 L1/L2 与 ATOM 原子更新**。
- 边界：原始文档不入库；P2 向量检索按需；source_type 未知走"未登记提示"。

## 十二、待 B 四次复核事项

| 编号 | 内容 | 建议默认 |
|------|------|---------|
| R4-Q1 | 三级索引（L1 路由/L2 类别倒排含 norm_text 摘要/L3 全文）是否符合 05 号最小读取 | 是 |
| R4-Q2 | scope_scope 移到 Canonical 层、ATOM 仅 authority+source_category 是否一致 | 是 |
| R4-Q3 | L5 默认归属 operational 方案 A 是否可接受 | 是 |
| R4-Q4 | P1 三层语义兜底（词库扩展→norm_text 扫读→降级提示）是否足够 | 是 |
| R4-Q5 | registry 变更迁移规则是否与 06/skill-contract 一致 | 是 |

## 十三、给 B 的四次复核输入包

```
你现在是 Skill 升级独立审核 Agent B。请独立扫描 c:\Users\qiusuo\Downloads\ChronoPM Skill（skill.json v1.14.0 / schema 0.6.0→目标 0.7.0），
不基于 A 的缓存或结论。请复核 V0.4：
1. 三级索引（L1/L2 覆盖索引含 norm_text 摘要/L3）+ 分级加载是否满足 05 号最小读取与索引效率（H-I1）；
2. P1 三层语义兜底（词库扩展/norm_text 扫读/降级提示）是否解决"AI 检索不全"（M-I2）；
3. scope_scope 移至 Canonical 层、ATOM 仅 authority+source_category 是否自洽（M-I3）；
4. L5 默认归属 operational（方案 A）是否合理（M-I4）；
5. ATOM 提取触发时机（主/辅助/增量）与 18 号初始化向导衔接是否顺畅（L-I5）；
6. registry 变更迁移规则 + 三级索引原子更新是否与 06 号/ skill-contract 一致（L-N4/L-N3）；
7. 文件级改动清单（21 项）是否完整、复杂度与 schema 变更合规。
输出：B 审核结论 A/B/C/D + 问题清单 + 修订建议。
```

## 十四、当前共识状态

- 已确认：三级索引 + 分级加载 + 覆盖索引；scope 归属 Canonical；L5 归属 operational；双层来源分类；三层数据模型；大文档只存指针；P1 Markdown 索引 + 语义兜底；milestone 复用；随笔双入口；schema 0.7.0 治理。
- 暂定：R4-Q1~R4-Q5。
- 不纳入本次：向量检索部署、原始文档入库。

## 十五、是否偏离目标自检

是否偏离目标：否。
说明：V0.4 补齐索引效率与检索完整性两处短板，16 项用户需求全部有落点，仍遵守 ChronoPM 治理流程，无目标漂移，建议进入 CR 工单阶段。
