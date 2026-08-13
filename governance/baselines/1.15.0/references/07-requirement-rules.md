# 需求管理约束规则

本规则适用于需求的收集、分类、拆解、评审和追踪矩阵维护。需求变更管理见 `08-change-control-rules.md`。

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

注意：需求优先级（MoSCoW）代表业务价值，任务优先级（P0-P3）代表执行紧急度，两者不完全等同。一个 Must 需求拆出的任务不一定都是 P0。

### 1.3 按来源分类

| 来源 | 需要确认的事项 |
|------|----------------|
| 合同/招标文件 | 逐条核对，不可遗漏，具法律效力 |
| 需求规格说明书 | 确认是否已评审通过 |
| 用户口述/会议 | 确认是否有书面记录或纪要 |
| 隐含需求 | 与干系人确认后纳入 |

## 2. 需求登记册

`requirements/requirement-register.md` 是需求管理的核心事实源，同时承载需求清单和追踪矩阵。

### 2.1 字段定义

| 字段 | 说明 | 必填 |
|------|------|------|
| Req ID | REQ-[模块代号]-NNN | 是 |
| 标题 | 需求标题 | 是 |
| 类型 | FR / NFR / CR / IR / DR | 是 |
| 优先级 | Must / Should / Could / Won't | 是 |
| 来源 | contract / document / meeting / implied | 是 |
| 来源引用 | 合同条款号或文档章节 | 是 |
| 验收标准 | 可验证的验收条件 | 是 |
| 关联任务 | Task ID 列表 | 否（拆解后填） |
| 关联里程碑 | M-NN | 否 |
| 验收状态 | pending / in_progress / accepted / rejected | 是 |
| 状态 | proposed / confirmed / in_progress / delivered / accepted / changed / cancelled | 是 |
| 变更记录 | CR-YYYYMMDD-NNN | 否 |
| Source | 来源说明 | 是 |

### 2.2 追踪矩阵

追踪矩阵内嵌在需求登记册中，通过字段关联实现全链路追溯：

```
合同条款 → 需求(REQ) → 任务(T) → 测试用例 → 验收
```

每条需求必须能追溯到来源（合同条款或需求文档），并能向下追踪到任务和验收。

## 3. 需求拆解

### 3.1 拆解层级

```
需求（Requirement）
  └── Epic（业务史诗）
       └── Feature（功能特性）
            └── Task（开发任务）
```

### 3.2 拆解原则

1. 每层拆解必须符合 MECE 原则（相互独立、完全穷尽）。
2. 拆解为 Task 时必须满足可分配、可估算、可测试。
3. 一个需求拆解为多个任务时，所有任务必须关联到该需求 ID。
4. 拆解后必须更新需求登记册的"关联任务"字段。

### 3.3 需求描述规范

```markdown
### REQ-[模块代号]-NNN：[需求标题]

**类型**：FR
**优先级**：Must
**来源**：合同附件3 第2.1条
**验收标准**：
1. [条件1] 时，系统应 [行为1]
2. [条件2] 时，系统应 [行为2]
3. 异常情况：[异常场景] 时，系统应 [异常处理]

**关联任务**：
- T-YYYYMMDD-001
- T-YYYYMMDD-002

**状态**：confirmed
```

## 4. 需求评审

### 4.1 评审检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 完整性 | 角色、功能、目的、验收标准齐全 |
| 清晰性 | 无歧义，无主观形容词（如"快速""友好"） |
| 一致性 | 与其他需求无矛盾 |
| 可验证性 | 验收标准明确且可执行 |
| 可追溯性 | 可追溯到合同条款或需求文档 |
| 可行性 | 有技术可行性分析 |
| 必要性 | 与项目目标相关，非镀金 |

### 4.2 评审结论

- **通过**：纳入基线，状态改为 `confirmed`。
- **有条件通过**：列出待补充项，状态保持 `proposed`。
- **不通过**：说明原因，状态改为 `cancelled`。
- **暂缓**：记录到需求池，状态保持 `proposed`，标注暂缓原因。

## 5. 需求与变更的边界

1. 需求登记册只记录当前有效的需求状态。
2. 任何变更（新增、修改、删除、优先级调整）必须先进入 `requirements/change-log.md`。
3. 变更批准后才能更新需求登记册。
4. 需求登记册中的"变更记录"字段关联到对应的 Change ID。

## 6. Change Log

需求登记册底部维护 Change Log，格式同其他事实源。Change Log 活跃区上限 50 行或超过 30 天时触发按月归档到 `change-log/archive/YYYYMM-change-log.md`，并维护 `change-log/index.md` 月份导航（与 06/03 号归档规则一致）。

## 7. 级联传播规则

本实体（Requirement）状态变更时，按以下规则触发下游动作。动作分三类：
- [AUTO] 写派生视图（索引），低风险，直接执行
- [CHECK] 只读校验，检查关联是否存在/一致
- [SUGGEST] 写事实源或影响其他实体，加入建议更新清单待 PM 确认

> **AUTO 作用域声明**：AUTO 仅作用于非事实源的派生视图，不触碰任何事实源文件。事实源写入（含 pending 登记）一律受 `skill-contract.md` 第 5 条约束。

执行顺序：先 AUTO → 再 CHECK → 最后 SUGGEST。
同一处理流程内，级联动作只执行一次；多个 SUGGEST 汇总为同一批建议清单，流程末尾统一输出。
执行完毕后，14 号自查清单验证完整性。

Requirement 状态变更 →
  [CHECK] 检查关联 task 的状态一致性（追踪矩阵）
  [AUTO] 更新 requirement-register 衍生索引

Requirement 优先级变更 →
  [CHECK] 检查关联 task 是否需要调整优先级

## 8. 跨源需求归集与范围判定（RI）(CR-20260813-001)

当同一批需求分散在**合同、招投标、立项、密评/等保、里程碑**等多来源文档时，用三层数据模型把"需求在不在某范围"从扯皮变成**可取证**。本能力在 §1.3 来源分类与 §2 追踪矩阵之上扩展，不改变既有 REQ 层字段。

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

`Canonical 1:N ATOM`；`REQ 1:1 Canonical`（默认）+ `Canonical 1:N REQ`（canonical_id 回指）。REQ 的 `来源/Source` 字段升级为指向 Canonical ID 的指针（旧工作区仍为自由文本，向后兼容）。

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
kind            : requirement / requirement_directive / agreement / constraint
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
milestone       : 关联里程碑 M-NN（若有）
hash            : 防篡改摘要
updated         : 时间戳
```

> scope_scope 是**跨源聚合结论**，只属 Canonical 层；单个 ATOM 用 authority + source_category 表达单条证据效力，不设 scope_scope。

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

### 8.6 提取与归并流程

1. **触发**：A) PM 主动提供源文档并要求提取/拆解；B) 初始化向导 Step1 合同层同步提取；C) 源文档出新版本（补充协议/补遗）时增量提取 + 源版本 stale 判定。
2. **拆词归一**：按 ES 分析链，AI 原子化切块 → 17 号语义归一生成 norm_text（术语级走词库状态机，句子级 confidence 记于 ATOM、人工确认）。
3. **归并**：基于 norm_text + keywords 双路匹配，命中已有 Canonical 则追加 evidence；未命中则新建 Canonical；归并/新建结果须 PM 确认。
4. **范围判定**：Canonical 聚合 all evidence 判定 scope_scope；来源互斥标 conflict 转人工裁决；密评等 compliance 类带强制门禁（不过密评不得进入验收）。
5. **索引**：更新对应类别 L1/L2 索引与 ATOM 全文（见 05 号三级索引）；任何失败整体回退并标记 stale。

### 8.7 级联传播规则（RI 扩展）

ATOM 归并/变更 →
  [AUTO] 更新 canonical evidence 链 + L1/L2 索引（派生视图）
  [CHECK] 校验 source_version 与索引 last_source_version 一致性
  [SUGGEST] 新 Canonical 或 scope 判定结果 → 待 PM 确认；evidence 全 stale → 提示重新评估

### 8.8 Project Notes 随笔准则 (CR-20260813-001)

PM 方法论、干系人沟通备忘、项目洞察、交付策略等**低结构化、追加式**内容，统一存入 `ai/projects/{子项目}/context/project-notes.md`（项目集为 `ai/portfolio/context/project-notes.md`）。**只追加**，不修改历史条目。

每条格式：`- YYYY-MM-DD [#标签] 内容（来源：PM主动/AI感知-<信号>）`

标签：`#方法论` `#干系人` `#洞察` `#策略` `#风险直觉`

**双入口**：
1. PM 主动要求（"记一下/备忘/这个经验记下"）→ 直接追加。
2. AI 主动感知（仿 17 号 §8.1 自动发现 + pending→confirmed）：对话命中方法论/干系人/洞察/策略信号 → 附加"💡 检测到 N 条候选备忘，是否记入 project-notes？" → PM 确认写入、否定不记录、不阻塞主体任务。

**更新权限**：project-notes 为低结构化追加式记录，属**低/中风险更新**（proactive 模式可直接追加并标 `Confirmed By: 待确认`，与 AI 感知"建议保存→确认"一致），不涉及事实源状态变更。

**与既有文件边界**：`project-context`=结构化背景；`decision-log`=正式决策；`lessons-learned`=复盘产出；`project-notes`=非正式随笔/备忘。

**归档**：project-notes 超过 100 条或 6 个月时，按季度归档到 `context/project-notes-archive/`（沿用 06 号归档规则）。
