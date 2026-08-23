# 需求管理约束规则

本规则适用于需求的收集、分类、拆解、评审和追踪矩阵维护。需求变更管理见 `08-change-control-rules.md`。源文档拆解（提取/归并/台账/分片）正文见 `source-split-skill/references/split-rules.md`，仅拆文件时加载。

**硬分离**：需求 ≠ 工作包 ≠ 待办。三者编号、文件、生命周期均独立。需求只绑工作包；待办只从已规划工作包拆出；禁止把需求正文写入工作包文件。

---

## 1. 需求分类

### 1.1 按类型分类

| 类型 | 代号 | 说明 |
|------|------|------|
| 功能需求 | FR | 系统必须实现的功能行为 |
| 非功能需求 | NFR | 性能、安全、可用性、兼容性等 |
| 约束需求 | CR | 技术选型、合规、标准等强制约束 |
| 接口需求 | IR | 与外部系统的接口对接 |
| 数据需求 | DR | 数据格式、迁移、标准 |

### 1.2 按优先级分类（MoSCoW）

| 优先级 | 说明 | 判定标准 |
|--------|------|----------|
| Must | 必须实现 | 不实现则系统无法验收 |
| Should | 应该实现 | 不实现影响用户体验 |
| Could | 可以实现 | 有价值但非本次必须 |
| Won't | 暂不实现 | 明确排除的范围 |

注意：需求优先级（MoSCoW）代表业务价值，待办优先级（P0-P3）代表执行紧急度，两者不完全等同。一个 Must 需求绑定的工作包，其下待办不一定都是 P0。

### 1.3 按来源分类

| 来源 | 需要确认的事项 |
|------|----------------|
| 合同/招标文件 | 逐条核对，不可遗漏，具法律效力 |
| 需求规格说明书 | 确认是否已评审通过 |
| 用户口述/会议 | 确认是否有书面记录或纪要 |
| 隐含需求 | 与干系人确认后纳入 |

## 2. 需求登记册

`requirements/requirement-register.md`（或按模块分片）是需求管理的核心事实源，同时承载需求清单和追踪矩阵。查询不得默认通读整册，见 §2.3。

### 2.1 字段定义

| 字段 | 说明 | 必填 |
|------|------|------|
| Req ID | REQ-[模块代号]-NNN | 是 |
| 标题 | 需求标题 | 是 |
| 类型 | FR / NFR / CR / IR / DR | 是 |
| 优先级 | Must / Should / Could / Won't | 是 |
| 确认状态 | 未确认 / 已确认 / 已否决（独立于生命周期，见 §2.1.1） | 是 |
| 确认缺口 | 未确认时可多项：做不做 / 效果未对齐 / 方案未对齐；已确认、已否决填 — | 未确认时是 |
| 生命周期 | 已提议 / 进行中 / 已交付 / 已验收 / 已变更 / 已取消（不再用「已确认」占位） | 是 |
| 来源 | contract / document / meeting / implied | 是 |
| 来源指针 | 文件（`sources/SRC-NNN` 或文档名）+ 章节/条款 + 页码；从 ATOM `source_ref` 上提，页码不得只活在证据层 | 是 |
| 工作包 | 可多个 WP-NNN（逗号分隔，如 `WP-001, WP-014`）；空值「—」合法，但必须进 `ai/pm-decisions.md`「需求未绑定工作包」 | 否 |
| 验收标准 | 可验证的验收条件 | 是 |
| 实现视图 | 面向开发的实现摘要（关键模块/接口名 + 一句话要点，≤100 字，见 §8.10 双视图） | 否 |
| 原型/文档链接 | 关联的原型图、设计稿、接口文档的路径或 URL 指针（原文档不入库，见 §8.10） | 否 |
| 关联里程碑 | 里程碑型 WP 编号（WP-NNN） | 否 |
| 验收状态 | 待验收 / 验收中 / 已验收 / 已驳回 | 是 |
| 变更记录 | CR-YYYYMMDD-NNN | 否 |
| Source | 来源说明 | 是 |

禁止字段：

- **关联任务**（TD-xxx）。需求不直接绑待办。存量「关联任务」列停用为只读遗留；触碰该条时改写「工作包」列，不批量回填待办号。
- 需求正文、验收标准、功能描述不得作为工作包字段或抄进 WP 文件。

#### 2.1.1 确认状态与生命周期

确认状态与生命周期是两个独立维度，禁止用生命周期「已确认」占位。

| 确认状态 | 含义 | 约束 |
|----------|------|------|
| 未确认 | 刚入库或评审未齐 | 必须标缺口（可多项）：做不做 / 效果未对齐 / 方案未对齐。三项没齐不得标已确认 |
| 已确认 | 做不做、效果、方案三项均已对齐 | 才允许组**已规划**工作包、才允许从已规划 WP 拆待办 |
| 已否决 | 明确不做 | 不得绑已规划 WP、不得拆待办；生命周期通常为已取消 |

| 生命周期 | 含义 |
|----------|------|
| 已提议 | 刚入库；与确认状态=未确认同时出现 = 还在等项目经理裁定 |
| 进行中 | 已进入已规划工作包并开始执行 |
| 已交付 | 实现侧交付完成，待验收 |
| 已验收 | 验收通过 |
| 已变更 | 基线需求被变更单改写（关联 CR） |
| 已取消 | 不再纳入范围 |

未确认需求可以继续留在清单里（后续文件还会拆出更多条），**不得**拿去组已规划工作包、**不得**拆待办。可暂绑状态=`待确认`的 WP 草案；需求确认与 WP 确认均完成后才允许拆待办。

### 2.2 追踪矩阵

追踪矩阵内嵌在需求登记册中，通过编号关联实现全链路追溯：

```
合同条款 → 需求(REQ) → 工作包(WP) → 待办(TD) → 测试用例 → 验收
```

每条需求必须能追溯到来源指针（文件 + 章节/条款 + 页码），并能向下追踪到工作包。待办经 WP 回指需求，需求清单不维护待办号。REQ↔WP 双向**只存编号**。

### 2.3 查询与分片

查询先读 `requirements/_index.md`（≤7 列：`Req ID | 标题 | 确认状态 | 生命周期 | 工作包 | 来源指针 | 优先级`），再打开命中分片。禁止默认通读整册。正文超 50 条按模块分片，索引保持瘦；Change Log 50 行/30 天按月归档（与 06 号一致）。

## 3. 需求拆解

### 3.1 拆解层级

```
源文件（合同 / 招标 / 立项 / 合规等）
  └── 需求清单（REQ，默认确认状态=未确认）
       └──（确认状态=已确认后）绑定工作包（WP；一需求可多 WP，多小需求可进一个 WP）
            └──（WP 已规划后）拆待办（TD）
```

删除 Epic→Feature→待办。拆解产出写入需求清单，**不落待办**。

### 3.2 拆解原则

1. 需求 ≠ 工作包 ≠ 待办。禁止把三层写成同一条记录。
2. 每层拆解必须符合 MECE 原则（相互独立、完全穷尽）。
3. 拆解只写入需求清单，默认确认状态=`未确认`、生命周期=`已提议`。禁止「拆解出的待办」、禁止回填「关联任务」。
4. 未确认需求不得组已规划工作包、不得拆待办。
5. REQ↔WP 双向只存编号。禁止把需求正文、验收标准、功能描述写入 WP 文件。
6. 一需求可绑定多个 WP；多个小需求可进入同一个 WP。AI **禁止**代切颗粒度。
7. **无需求禁止建 WP**。搜不到需求 → 禁止建包，进 `ai/pm-decisions.md`「工作包无需求」。项目经理坚持要这块活 → 先在需求清单补需求（可仍是未确认），再绑，并记疑似蔓延。
8. 工作包列空值合法，但必须进 `ai/pm-decisions.md`「需求未绑定工作包」。
9. 待办只从已规划工作包拆出（见 `00-pm-main-rules.md` WF-8）。需求拆解不是待办入口。

### 3.3 需求描述规范

```markdown
### REQ-[模块代号]-NNN：[需求标题]

**类型**：FR
**优先级**：Must
**确认状态**：未确认
**确认缺口**：做不做；效果未对齐；方案未对齐
**生命周期**：已提议
**来源指针**：sources/SRC-NNN 第2.1条 第12页
**工作包**：— （空值须进 pm-decisions「需求未绑定工作包」）
**验收标准**：
1. [条件1] 时，系统应 [行为1]
2. [条件2] 时，系统应 [行为2]
3. 异常情况：[异常场景] 时，系统应 [异常处理]

**实现视图**（可选，面向开发的摘要级描述）：[关键模块/接口名 + 一句话实现要点]

**原型/文档链接**（可选）：[原型地址 / PRD 章节 / 接口文档链接 / 无]
```

工作包侧对应段只写 `REQ-[模块代号]-NNN`（及可选来源文件路径指针），不粘贴本段正文。

## 4. 需求评审

### 4.1 评审检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 完整性 | 角色、功能、目的、验收标准齐全 |
| 清晰性 | 无歧义，无主观形容词（如"快速""友好"） |
| 一致性 | 与其他需求无矛盾 |
| 可验证性 | 验收标准明确且可执行 |
| 可追溯性 | 来源指针含文件 + 章节/条款 + 页码 |
| 可行性 | 有技术可行性分析 |
| 必要性 | 与项目目标相关，非镀金 |
| 确认三项 | 做不做、效果、方案均已对齐（缺任一项不得标已确认） |

### 4.2 评审结论

- **通过**：确认状态改为 `已确认`（三项已齐）；生命周期保持 `已提议`，直至进入已规划工作包后改为 `进行中`。
- **有条件通过**：列出待补充项，确认状态保持 `未确认`，标对应缺口。
- **不通过**：说明原因，确认状态改为 `已否决`，生命周期改为 `已取消`。
- **暂缓**：记录到需求池，确认状态保持 `未确认`，标缺口，生命周期保持 `已提议`。

确认/否决写入 `ai/pm-decisions.md` 决策记录（不是对话日志）。未确认项同时留在决策文件「需求未确认」块。

## 5. 需求与变更的边界

1. 需求登记册只记录当前有效的需求状态。
2. 任何变更（新增、修改、删除、优先级调整）必须先进入 `requirements/change-log.md`。
3. 变更批准后才能更新需求登记册，并走工作包绑定/调整；禁止跳过 WP 直接灌待办。
4. 需求登记册中的"变更记录"字段关联到对应的 Change ID；生命周期改为 `已变更`。

## 6. Change Log

需求登记册底部维护 Change Log，格式同其他事实源。Change Log 活跃区上限 50 行或超过 30 天时触发按月归档到 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航（与 06 号归档规则一致）。

## 7. 级联传播规则

本实体（Requirement）状态变更时，按以下规则触发下游动作。动作分三类：
- [AUTO] 写派生视图（索引），低风险，直接执行
- [CHECK] 只读校验，检查关联是否存在/一致
- [SUGGEST] 写事实源或影响其他实体，加入建议更新清单待 PM 确认

> **AUTO 作用域声明**：AUTO 仅作用于非事实源的派生视图，不触碰任何事实源文件。事实源写入（含 pm-decisions 登记）一律受 `skill-contract.md` 第 5 条约束。

执行顺序：先 AUTO → 再 CHECK → 最后 SUGGEST。
同一处理流程内，级联动作只执行一次；多个 SUGGEST 汇总为同一批建议清单，流程末尾统一输出。
执行完毕后，14 号自查清单验证完整性。

> **强制执行要求**（见 `00-pm-main-rules.md` §8a）：以上 AUTO/CHECK/SUGGEST 动作不得静默跳过。SUGGEST 必须呈现给 PM 确认，不得以"用户未要求"为由省略。流程末尾必须输出"级联完整性"结论。

Requirement 确认状态 / 生命周期变更 →
  [CHECK] 检查关联 WP 编号双向一致（需求清单「工作包」列 ↔ WP 关联需求编号）
  [CHECK] 未确认或已否决的需求未进入已规划 WP、未拆待办
  [AUTO] 更新 `requirements/_index.md` 衍生索引

Requirement 优先级变更 →
  [CHECK] 检查关联 WP 是否需要调整优先级（不直接改待办）

Requirement 工作包列变更 →
  [CHECK] 双向只存编号且一致；空值已进 `ai/pm-decisions.md`「需求未绑定工作包」
  [SUGGEST] WP 无关联 REQ → `ai/pm-decisions.md`「工作包无需求」（禁止维持无需求 WP）

## 8. 跨源需求归集与范围判定（RI）(CR-20260813-001)

当同一批需求分散在**合同、招投标、立项、密评/等保、里程碑**等多来源文档时，用三层数据模型把"需求在不在某范围"从扯皮变成**可取证**。本能力在 §1.3 来源分类与 §2 追踪矩阵之上扩展。REQ 层字段以 §2.1 为准；ATOM/Canonical 模型不变。

### 8.1 三层数据模型

```
源文档（任意 source_type）
  → ATOM（证据层，只读）→ Canonical（归并层）→ REQ（管理层，登记册）
```

| 层 | 实体 | 说明 |
|----|------|------|
| 证据层 | ATOM | 从源文档条款提取的原子事实，只读不可改写；`raw_text` 存条款原文（≤500 字），原始文档不入库只存指针（文档名+版本+条款号） |
| 归并层 | Canonical | 跨源语义归并后的规范需求，含 evidence 证据链 + scope_scope 判定；`Canonical 1:N ATOM` |
| 管理层 | REQ | 现有登记册条目；默认 `REQ 1:1 Canonical`，多交付需求时允许多 REQ 以 `canonical_id` 回指同一 Canonical |

`Canonical 1:N ATOM`；`REQ 1:1 Canonical`（默认）+ `Canonical 1:N REQ`（canonical_id 回指）。REQ 的 `来源/Source` 字段升级为指向 Canonical ID 的指针（旧工作区仍为自由文本，向后兼容）。入库 REQ 时必须同时写「来源指针」（文件 + 章节/条款 + 页码），从 ATOM `source_doc` + `source_ref` 上提。

### 8.2 双层来源分类

| 层 | 字段 | 粒度 | 取值 |
|----|------|------|------|
| REQ（现有） | `来源` | 粗 | contract / document / meeting / implied（§1.3，不变） |
| ATOM（新增） | `source_type` | 细 | 见 `requirements/source-type-registry.md` |

source_type 项目级可扩展；每条必须归入 `source_type→source_category`（contractual/procurement/approval/compliance/technical/operational，固定 6 类），继承默认 authority。未知 source_type 触发"未登记"提示，不静默归类。

### 8.3 来源权威层级与默认值

| authority | 层级 | 来源类别默认 |
|---|---|---|
| L1 | 合同/协议 | contractual |
| L2 | 招投标/投标承诺 | procurement |
| L3 | 立项/技术基线 | approval、technical（基线化后） |
| L4 | 合规强制 | compliance（密评/等保） |
| L5 | 工期/里程碑 | operational（工期/里程碑条款默认 L5，其余默认 L3） |

### 8.4 ATOM 字段

```
ATOM_ID         : ATOM-<source_type>-NNN
kind            : requirement / requirement_directive / agreement / constraint / background / baseline / hardware / spec / term / milestone_fact
source_doc      : 文档名
source_version  : 源文档版本号（stale 检测基准）
source_ref      : 条款号 / 章节 / 页码
source_type     : registry 细粒度类型
source_category : 6 类之一
authority       : L1~L5（由 source_category 默认推断，可覆盖）
raw_text        : 条款级原文（≤500 字，超长拆分为多条，用 supersedes 标记血缘）
supersedes      : 长条款拆分时指向同一条款拆分前/后 ATOM_ID（锚定拆分血缘）
norm_text       : 语义归一后的标准表述（AI 生成，confidence 记录，人工确认）
keywords        : 拆词四元组 [对象][动作][约束][指标]
confidence      : AI 归一/匹配置信度
milestone       : 关联里程碑型 WP 编号（WP-NNN，若有）
hash            : 防篡改摘要
updated         : 时间戳
```

> scope_scope 是**跨源聚合结论**，只属 Canonical 层；单个 ATOM 用 authority + source_category 表达单条证据效力，不设 scope_scope。
>
> **kind 落盘（v3.6.0）**：需求类（requirement / requirement_directive / agreement / constraint）写入 `requirements/sources/{编号}/atoms.md`，走 ATOM→Canonical→REQ。非需求类（background / baseline / hardware / spec / term / milestone_fact）写入同目录 `facts.md`，**不进** Canonical / scope_scope。旧 4 类 kind 全部兼容，不强制重标。监理/验收中的服务承诺/质保条款：kind=agreement/constraint，source_type 归 operational（Q10）。
>
> **上提到来源指针**：产 REQ 时把 `source_doc` + `source_ref`（章节/条款 + 页码）写入需求清单「来源指针」，不得只把页码留在 ATOM。

### 8.5 Canonical 字段

```
CAN_ID          : CAN-NNN
evidence        : ATOM_ID 证据链（1:N）+ 各自 source_type/authority
scope_scope     : in_contract / in_bid_only / in_initiation_only / not_in_scope / conflict
consistency     : consistent / conflict（来源互斥转人工裁决，沿用 pending→confirmed）
milestone       : 关联里程碑、合规门禁
status          : active / evidence_stale
```

**scope_scope 与优先级解耦**：`scope_scope`（范围归属）与 §1.2 `优先级`（MoSCoW）是**两个独立维度**。例：`scope_scope=in_contract` + `优先级=Won't`（合同有但双方同意暂不做）；`scope_scope=in_initiation_only` + `优先级=Must`（立项要求但合同未覆盖，需优先推动纳入）。登记册中作为两列独立呈现。

> **scope_scope 聚合排除规则（硬约束）**：`scope_scope` 的判定**仅由** `source_category ∈ {contractual, procurement, approval, compliance, operational}` 的 ATOM evidence 参与。`source_category = technical` 的 ATOM（含 dev_prd/design_doc/api_spec/prototype/ui_spec 等开发侧文档，见 §8.10）**不参与** scope_scope 聚合，仅用于填充对应 REQ 的"实现视图"与"原型/文档链接"字段。此边界防止开发文档的实现细节污染范围判定结论，任何归并/重判流程不得违反。

### 8.6 提取与归并流程

正文见 `source-split-skill/references/split-rules.md`。

### 8.7 级联传播规则（RI 扩展）

ATOM 归并/变更 →
  [AUTO] 更新 canonical evidence 链 + L1/L2 索引（派生视图）
  [CHECK] 校验 source_version 与索引 last_source_version 一致性
  [CHECK] technical 类 ATOM 未参与 scope_scope 聚合（聚合排除红线）
  [SUGGEST] 新 Canonical 或 scope 判定结果 → 待 PM 确认；evidence 全 stale → 提示重新评估；technical 类 ATOM 命中 Canonical → 建议填充对应 REQ 的"实现视图"字段

### 8.8 Project Notes 随笔准则 (CR-20260813-001)

PM 方法论、干系人沟通备忘、项目洞察、交付策略等**低结构化、追加式**内容，统一存入本项目 `context/project-notes.md`。**只追加**，不修改历史条目。

每条格式：`- YYYY-MM-DD [#标签] 内容（来源：PM主动/AI感知-<信号>）`

标签：`#方法论` `#干系人` `#洞察` `#策略` `#风险直觉`

**双入口**：
1. PM 主动要求（"记一下/备忘/这个经验记下"）→ 直接追加。
2. AI 主动感知（仿 17 号 §8.1 自动发现 + pending→confirmed）：对话命中方法论/干系人/洞察/策略信号 → 附加"💡 检测到 N 条候选备忘，是否记入 project-notes？" → PM 确认写入、否定不记录、不阻塞主体任务。

**更新权限**：project-notes 为低结构化追加式记录，属**低/中风险更新**（proactive 模式可直接追加并标 `Confirmed By: 待确认`，与 AI 感知"建议保存→确认"一致），不涉及事实源状态变更。

**与既有文件边界**：`project-context`=结构化背景；`decision-log`=正式决策；`lessons-learned`=复盘产出；`project-notes`=非正式随笔/备忘。

**归档**：project-notes 超过 100 条或 6 个月时，按季度归档到 `context/project-notes-archive/`（沿用 06 号归档规则）。

### 8.9 合同作用域与检索路由（CR-20260813-002）

RI 范围判定隐含"合同↔项目 1:1"假设，但现实中为**多对多**（联合体合同、跨项目合同、主合同+多补充协议、同一项目被多份合同覆盖等）。本小节补齐该缺口：项目级 contract-register 作为拆解发生地，定义 ATOM/Canonical 的存储归属、带合同维度的 scope 判定与检索路由。跨项目检索由 ChronoPM-Portfolio 执行。

#### 8.9.1 contract-register.md 合同登记册（拆解发生地）

**位置**：项目级 `requirements/contract-register.md` 为合同登记与检索入口（每项目一份）。**拆解产物（v3.6.0）**落 `requirements/sources/{编号}/`（一个源文档 = 一个目录，编号即目录名）。文档簇固定号（CON-/BID-/INIT-/COMP-/SUP-/TRN- 等 `{YYYYMMDD}-{HHmmss}`）为跨项目互认键；`SRC-NNN` 仅项目内短号，不得作互认键。

- **现行**：`requirements/sources/{CON-… 或 SRC-NNN}/` 含 meta.md / _digest.md / atoms.md（或 atoms/）/ facts.md（或 facts/）/ ledger.md / parse-log.md。
- **存量**：旧 `{type}-source/` 走零清重建，不走迁移；未零清前禁止新拆解。禁止再新建 `{type}-source/`。Portfolio V-8 读取端仍可兼容旧形态。
- **禁止第三套目录**（不得再使用 `contracts/CON-NNN` 等旧目录名，也不得在 sources/ 与 {type}-source/ 之外再造一套）。

跨项目检索由 ChronoPM-Portfolio 遍历 + 指纹去重，本包不维护集层登记册、不「项目集唯一登记册、子项目不复制」。

**字段**：

| 字段 | 必填 | 说明 |
|---|---|---|
| Contract ID | 是 | CON-NNN |
| 合同名称 | 是 | 合同全称 |
| 合同类型 | 是 | 主合同 / 补充协议 / 分包合同 等 |
| scope_level | 是 | `portfolio`（跨项目语义，存储仍下沉本项目）/ `project`（本项目）/ `supplement`（补充协议） |
| parent_contract_id | 补充协议必填 | 指向被补充合同 CON-NNN（D7）；主合同填「-」 |
| coverage 覆盖对象 | 是 | 受此合同约束的 PRJ-NNN 列表（或单项目整体） |
| 关联招投标 | 否 | 成套文档簇：BID-NNN |
| 关联立项 | 否 | INIT-NNN |
| 关联密评 | 否 | COMP-NNN |
| status | 是 | active / superseded |
| superseded_by | 否 | 合同拆分/替代时的血缘（D8） |
| Source | 是 | 来源合同/文档 |

> 撰写遵循 SKILL.md 底线 #2（待确认 + `ai/pm-decisions.md`）；写入走主动变更模式标记 `Confirmed By: 待确认`。

**文档簇关联（N5）**：招投标/立项/密评等文档与合同成套出现。通过 contract-register 的关联字段形成文档簇：`CON-NNN（合同）← BID-NNN（招标文件）← INIT-NNN（立项批复）← COMP-NNN（密评报告）`。检索"某 PDF 要求 X 在不在合同范围"时，先经文档簇定位对应合同，再走 §8.9.3 路由。

#### 8.9.2 ATOM/Canonical 存储归属（下沉 + 跨项目复制）

| 合同 scope_level | ATOM 存在哪 | Canonical 存在哪 |
|---|---|---|
| `portfolio`（跨项目，语义保留） | 下沉到各覆盖项目 `requirements/atoms/`，跨项目复制（禁止二次拆解） | 下沉到各覆盖项目 `requirements/canonical/`，跨项目复制 |
| `project` | 本项目 `requirements/atoms/` | 本项目 `requirements/canonical/` |
| `supplement`（补充协议） | 跟随父合同，下沉到覆盖项目 | 跟随父合同 |

**Canonical storage_level 判定**：Canonical 是跨源归并产物，一律落项目级：
- evidence 全部来自本项目合同 → 归本项目；
- evidence 跨项目 → 各覆盖项目各存一份副本（同源复制，禁止二次拆解），`storage_level` 可标 `portfolio` 语义但**存储不在集层**；跨项目检索由 ChronoPM-Portfolio 做。
- 多合同覆盖本项目时 Canonical 归 `requirements/canonical/`，用 `contract_refs` 区分合同。

**contract_refs 伴随字段（D1）**：Canonical 层新增 `contract_refs`（关联合同 ID 列表），表达"在哪些合同范围内"。scope_scope 保持既有 5 值枚举不变（向后兼容），`contract_refs` 为伴随字段。旧 Canonical 无该字段 → 视为"未关联合同"降级标注，不报错。

#### 8.9.3 检索路由（配合 05 号 §Quick Query）

```
Step 0  读本项目 requirements/contract-register.md（空 → 触发补录引导，最小字段：ID/名称/scope_level/覆盖/status）
Step 1  解析合同指向
        ├─ 指定合同（CON-XXX/名称）→ 查本项目 requirements/canonical
        │     scope_level=portfolio 语义 → 本项目副本 + 提示跨项目检索用 ChronoPM-Portfolio
        │     scope_level=supplement → 经 parent_contract_id 回溯父合同后仍在本项目路由
        ├─ 未指定 → 列本项目合同候选供选择；或"全部范围"→ 逐合同检索合并
        └─ 登记册空/无匹配 → 提示补录，不臆造（D5）
Step 2  本项目 canonical 走 L1→L2→L3 三级索引（单次 200-400 行最小读取，05 号）
Step 3  输出 scope_scope(result) + contract_refs + 证据链
        多合同覆盖 → 逐合同列结论
        scope_level=supplement → contract_refs 含 supplement 与父合同双 ID
```

#### 8.9.4 合同变更三级联动（N14，D8，引用 08 号）

| 类别 | ATOM | Canonical | contract-register | 08 号变更类型 |
|---|---|---|---|---|
| 合同范围扩大（含补充协议） | 增量提取新增 ATOM(supplement) | 新 ATOM 归并，scope 重判 | 补充协议登记（parent_contract_id） | `scope` + `requirement` |
| 合同拆分为两份 | 原 ATOM 按新合同归属迁移 | 相关 Canonical 重判 | 旧条 status=superseded、superseded_by=新条；新增 2 条 | `scope` + `cost` |
| 合同范围缩小 | 相关 ATOM 标 stale/剔除 | 原 in_contract 的 Canonical 可能变 not_in_scope | 维护 status/血缘 | `scope` |

> 合同范围变更**不修改 08 号概念域 B 枚举**（不新增 `contract_scope`），复用既有 `scope`/`cost`/`requirement` 类型（D8）。级联执行顺序遵循 §8.7（AUTO→CHECK→SUGGEST），事实源写入待 PM 确认。
>
> **contract_refs 同步（CS-011/RI-012 复核口径）**：Canonical 的 scope_scope 重判时，`contract_refs` 必须同步更新——合同扩大/补充协议时在 contract_refs 追加（含 supplement 与父合同双 ID）；合同拆分时旧 Canonical 的 contract_refs 改指向新合同、旧合同条目进入血缘；合同缩小移除对应合同 ID；旧 Canonical 无 contract_refs 时按"未关联合同"处理（D1）。

#### 8.9.5 ledger.md 字段规范（sources/ 拆解台账，v3.6.0）

正文见 `source-split-skill/references/split-rules.md`。

### 8.10 需求双视图与开发文档关联（CR-20260815-001）

解决"合同需求（业务视角）⇄ 开发需求（实现视角）"的语义断层，使 AI 处理开发日报时能对照业务上下文。

#### 8.10.1 双视图定位与挂载

| 视图 | 存储方式 | 挂载层 | 定位 |
|---|---|---|---|
| 业务视图（view_business） | **不新增字段**，为 business 类（contractual/procurement/approval/compliance/operational）ATOM 的 `norm_text` 派生聚合，查时现算 | Canonical（经 evidence 派生） | 面向甲方/PM 的业务表述 |
| 实现视图（view_dev） | **新增字段**，登记册"实现视图"列 | **REQ 层**（日报经 WP 关联需求编号回指 REQ） | 面向开发的**摘要级**实现表述 |

**粒度约束**：实现视图只承载"关键模块/接口名 + 一句话实现要点"（≤100 字）；细粒度开发功能不进实现视图，走 REQ→WP→待办链路（待办自带实现描述）。禁止把需求正文抄进 WP 文件。Canonical 层不新增视图字段，仅通过 evidence 中 ATOM 的 source_category 区分来源。

#### 8.10.2 开发侧 source_type 扩展

`source-type-registry.md` 新增以下 source_type（均归入 `technical` 类别，authority 默认 L3）：

| source_type | 说明 | 与现有类型的边界 |
|---|---|---|
| dev_prd | 开发需求文档/PRD | 面向开发"怎么做"，区别于甲方侧需求规格 |
| design_doc | 概要/详细设计文档 | 与 design_spec（甲方侧需求规格说明书，contractual/approval 类）语义不同，不合并 |
| api_spec | 接口文档/API 说明 | - |
| prototype | 交互原型/线框图 | 非文本载体，见 §8.10.3 存储原则 |
| ui_spec | UI 标注稿/视觉规范 | - |

#### 8.10.3 原型与非文本内容存储原则

1. 原型/截图等文件本身**不放入工作区**（避免体积膨胀），仅在 REQ 的"原型/文档链接"字段存指针（外部路径/URL）。
2. 需要 AI 查看时，可将压缩截图放入 `requirements/artifacts/`，AI 通过读图能力辅助理解；文字化描述由 PM 补充或 AI 基于命名生成（SUGGEST → 待确认）。
3. 原型作为 ATOM 证据来源时，走 `prototype` source_type 提取其文字说明部分。

#### 8.10.4 日报场景数据链路

```
待办.WP Ref (WP-NNN)
  → WP 关联需求编号（只存编号，不存需求正文）
  → 需求清单 REQ.标题 + 验收标准（业务上下文，读需求文件）
  → REQ.实现视图（开发上下文，如存在）
  → REQ.原型/文档链接（如存在）
```

WF-2 日报处理按此链路加载需求上下文（性能控制见 05 号 §2.5）；字段缺失时降级输出已有字段，不阻塞。独立任务（WP Ref=待绑定）无需求上下文时不编造。

#### 8.10.5 字段完整性巡检

双视图链路字段完整性纳入 19 号信息完整性巡检（**存在性校验，非强制必填**）：已填 WP Ref 的待办经 WP 关联需求编号校验其 REQ 存在且未取消；确认状态=已确认的 REQ，其实现视图/原型链接覆盖率作巡检提示（独立任务 WP Ref=待绑定合法，同时进 `ai/pm-decisions.md`「待办未绑定工作包」；不得变相强制每条待办必须另填 Requirement Ref）。

### 8.11 源文档台账、目录化与互认（v3.6.0 / CR-F）

编号、目录与加载、共享复制见 `source-split-skill/references/split-rules.md`。本文件仅保留 REQ↔WP 绑定。

#### 8.11.1 编号

正文见 `source-split-skill/references/split-rules.md`。

#### 8.11.2 目录与加载

正文见 `source-split-skill/references/split-rules.md`。

#### 8.11.3 REQ↔WP 双向绑定

硬规则：

- **需求 ≠ 工作包 ≠ 待办**。双向只存编号（`REQ-XXX-NNN` ↔ `WP-NNN`），禁止把需求正文、验收标准、功能描述写入 WP 文件。
- **无需求禁止建 WP**。搜不到需求 → 禁止建包，进 `ai/pm-decisions.md`「工作包无需求」。项目经理坚持要这块活 → 先在需求清单补需求（可仍是未确认），再绑，并记疑似蔓延。
- 一需求可多个 WP；多个小需求可进一个 WP。工作包列空值「—」合法，但必须进 pm-decisions「需求未绑定工作包」。
- 未确认需求不得组**已规划**工作包、不得拆待办。可暂绑状态=`待确认`的 WP 草案。

正向：新产 REQ 提示归属 WP（可填多个编号）；未分配合法，但登记 `ai/pm-decisions.md`（块=需求未绑定工作包）。
反向：WP 关联需求编号 ↔ 需求清单「工作包」列必须一致（写后必检，复用 00 号 §8c）。
D22（14 号，限局部）：WP 无关联 REQ → pm-decisions「工作包无需求」（疑似需求蔓延）；REQ 无 WP → 登记「需求未绑定工作包」。与同一指针则**合并**决策行，不重复告警。

#### 8.11.4 共享复制

正文见 `source-split-skill/references/split-rules.md`。

### 8.12 同源判定与接收侧对账 WF-SD-1（v3.7.0）

正文见 `source-split-skill/references/split-rules.md`。

### 8.13 atoms/facts 分片（v3.7.0）

正文见 `source-split-skill/references/split-rules.md`。

### 8.14 REQ 自动编号（v3.7.0）

正文见 `source-split-skill/references/split-rules.md`。WP 绑定复用 §8.11.3。
