# 项目初始化向导规则

本文件定义 ChronoPM 的项目初始化向导机制。当用户首次进入工作区或主动请求初始化时，AI 通过分步引导方式录入项目基线信息，替代传统"创建空白模板后手动填写"的流程。

---

## 1. 触发条件

AI 在以下任一情况下启动初始化向导：

1. **新工作区检测**：检测到 `ai/.skill-version.json` 的 `initializedAt` 为当天，或 `project-brief.md` 的 `status: 草稿` 且关键字段（项目名称、合同总额等）为空。
2. **用户主动触发**：用户说"初始化项目""录入项目信息""设置项目基线""补全项目基础信息"等。
3. **脚本完成引导**：`init_workspace.py` 执行完成后提示"对 AI 说：初始化项目"。

### 触发检查流程

```
AI 进入工作区
  → 读取 ai/.skill-version.json（如存在）
  → 读取 context/project-brief.md
  → 检查 brief status 是否为"草稿"且关键字段为空
  → 是 → 主动提示："检测到项目尚未完成基线信息录入，是否开始初始化向导？"
  → 否 → 不触发
```

---

## 2. 六步向导流程

### Step 1: 合同层（必填）

**提示词**：

```
【Step 1/6 合同信息】
请提供以下信息（*为必填）：
* 合同名称：
* 合同总额（万元）：
* 立项时间（YYYY-MM）：
* 启动时间（YYYY-MM-DD）：
  合同类型：
  合同范围摘要（一段话概括）：
  计划完工时间（YYYY-MM-DD）：

你也可以上传合同文档，我来解析提取。
```

**录入字段**：

| 字段 | 必填 | 目标文件 |
|------|------|----------|
| 合同名称 | 是 | project-context.md, project-brief.md |
| 合同总额 | 是 | project-context.md |
| 立项时间 | 是 | project-context.md, project-brief.md |
| 启动时间 | 是 | project-context.md, project-brief.md |
| 合同类型 | 否 | project-context.md |
| 合同范围摘要 | 否 | project-context.md |
| 计划完工时间 | 否 | project-context.md, project-brief.md |

**文件上传支持**：如用户上传合同文档，AI 先解析提取上述字段，再补充询问缺失项。

**多合同循环登记（CR-20260813-002）**：合同与子项目为多对多关系（可能有多份主合同、主合同+补充协议）。Step1 录入完一份合同后询问"是否还有其他合同/补充协议？"，是则循环录入下一份，直到用户确认无更多合同。每份合同分配 `CON-NNN` ID，并登记到 `contract-register.md`（项目集 `portfolio/requirements/contract-register.md`；单项目 `requirements/contract-register.md`）：

| 补充登记字段 | 必填 | 说明 |
|---|---|---|
| scope_level | 是 | portfolio（跨子项目/整体）/ project（单子项目或单项目整体）/ supplement（补充协议） |
| parent_contract_id | supplement 必填 | 指向被补充合同 CON-NNN |
| coverage 覆盖对象 | 是 | 该合同约束的 PRJ-NNN 列表（Step2 确认映射，若 Step2 尚未录入子项目则先按合同范围摘要登记、Step2 后回填） |
| 关联招投标/立项/密评 | 否 | 成套文档簇关联 |

> 多合同登记与 Step2 的项目清单相互校验：Step2 确认"该合同分几个项目"时，若存在多份合同，须分别确认每份合同的覆盖子项目（场景 A-H 全覆盖）。合同登记册结构见 `07-requirement-rules.md` §8.9。

### Step 2: 项目层（必填）

**提示词**：

```
【Step 2/6 项目清单】
该合同分为了几个项目？请列出每个项目名称和一句话描述。
（如已从合同范围识别，请确认是否正确）
```

**目标文件**：`project-index.md`, `project-brief.md`

**项目集模式**：录入多个子项目。
**单项目模式**：确认项目名称。

### Step 3: 计划层（选填）

**提示词**：

```
【Step 3/6 计划规划】
现在为每个项目登记计划信息。先从"[项目名]"开始：
该项目规划分几个阶段？请列出阶段名称和计划时间段。
（如暂未规划可回答"跳过"）
```

**目标文件**：`context/project-brief.md`（计划概览段）

**录入字段**：阶段名称、计划开始时间、计划结束时间。

**规则**：
- 初始化阶段只记录计划概览；PLAN 文件（`plans/PLAN-NNN-{name}.md`）由 AI 在正式排计划时按需创建，向导不预建。
- 关联里程碑字段选填（可后置）。
- 计划阶段与里程碑是并存关系，可选关联（Q1=C）。

### Step 4: 需求层（选填）

**提示词**：

```
【Step 4/6 需求规划】
阶段"[阶段名]"预计包含多少需求？
（如已有需求文档可上传，我来解析。如暂未拆解可回答"跳过"）
```

**目标文件**：`requirements/requirement-register.md`（需求数量、需求ID列表字段）

**规则**：
- 初始化阶段允许只登记需求数量（Q4=C）。
- 需求 ID 列表默认为"待补充"，后续可补充。
- 如已有需求登记册，可补充完整需求 ID 列表。

### Step 5: 资源层（选填）

**提示词**：

```
【Step 5/6 资源分配】
阶段"[阶段名]"的开发资源有谁？请列出姓名和角色。
（如暂未确定可回答"跳过"）
```

**目标文件**：`projects/{子项目}/resources/resource-register.md`（项目集模式：各子项目分别创建，v2.0.0 零数据源，项目集层只维护 shared-resource-index 只读索引；单项目模式人员从待办/日报推导，不单独维护）

**规则**：
- project-brief.md 计划概览中记录资源摘要（姓名(角色)）。
- 资源登记册中记录资源详细信息（RES-NNN/角色/所属项目/状态/分配方式等）。
- 资源登记册的"计划分配视图"小节记录每个资源在各阶段的投入。
- **v2.1.0 新增：待办文件 §0 人员信息段引导**。初始化向导不直接创建待办文件；但向导完成后，某人首次出现于待办文件（`todos/{date}/{姓名}.md`）时，因无前一天文件可 T+1 拷贝，AI 必须引导 PM 填写 §0 人员信息段（岗位/姓名/联系方式/负责模块/进组日期/离组日期，见 personal-daily-todo-template §0），后续按 T+1 拷贝沿用（见 `00-pm-main-rules.md` §4d）。§0 与 resource-register 冲突时以 resource-register 为权威源。

### Step 6: 里程碑层（选填）

**提示词**：

```
【Step 6/6 里程碑时间】
除默认 M01-M12 里程碑体系外，是否有其他关键里程碑时间需要登记？
（如暂无可回答"跳过"）
```

**目标文件**：`plans/progress-plan.md`

**规则**：
- M01-M12 默认体系已预置，用户只需补充计划日期。
- 如有额外里程碑，后续在 PLAN 文件中追加里程碑型 WP（is_milestone=true）。

---

## 3. 跳过机制

- 每步标注必填/选填。
- 选填步骤用户可回答"跳过"，该步标记为"待补充"。
- 必填步骤不可跳过，但允许用户回答"稍后补充"，写入 brief 草稿区域。
- 跳过的步骤在确认摘要中标注"待补充"。

---

## 4. 进度记忆

### 记录位置

向导进度记录在 `project-brief.md` 的 front matter 中：

```yaml
---
doc_type: project-brief
project: "[项目名]"
version: v1.0
date: "YYYY-MM-DD"
status: 草稿
init_wizard_progress: "step3"  # 当前完成到第几步
init_wizard_started: "YYYY-MM-DD HH:MM:SS"
---
```

### 断点续接

- 向导中断后，下次进入时检测 `init_wizard_progress` 字段。
- 如检测到未完成的向导，提示用户："检测到未完成的初始化向导（已完成到 Step X），是否继续？"
- 用户确认后从断点步骤继续。

### 完成标记

向导全部完成且用户确认后：

```yaml
status: 已确认
init_wizard_progress: "completed"
init_wizard_completed: "YYYY-MM-DD HH:MM:SS"
```

---

## 5. 确认写入流程

### 5.1 生成确认摘要

向导完成后，AI 输出"初始化确认摘要"：

```markdown
# 项目初始化确认摘要

## 合同信息
- 合同名称：XXX
- 合同总额：XXX 万元
- 立项时间：YYYY-MM-DD
- 启动时间：YYYY-MM-DD
- 计划完工时间：YYYY-MM-DD

## 项目清单
| 项目ID | 项目名称 | 计划阶段数 | 需求总数 | 资源数 |
|---|---|---|---|---|

## 计划概览
| 项目 | 阶段名称 | 时间段 | 需求数 | 资源 |
|---|---|---|---|---|

## 里程碑
| 里程碑 | 计划日期 | 状态 |
|---|---|---|

## 待补充项
- [列出所有跳过或未完成的步骤]

## 将更新的文件
| 文件 | 更新内容 |
|---|---|

请确认以上信息是否正确，确认后我将写入对应文件。
```

### 5.2 写入规则

- 用户确认后才写入事实源文件。
- 所有写入的文件 `status` 从"草稿"改为"已确认"。
- 写入操作遵循 `06-file-rules.md` 的文件操作规则。
- 写入完成后输出确认清单，列出所有已更新的文件。

### 5.3 写入范围

| 步骤 | 目标文件 | 写入内容 |
|------|----------|----------|
| Step 1 合同层 | `context/project-context.md` | 合同信息表 |
| Step 1 合同层 | `context/project-brief.md` | 基本信息（立项时间/启动日期/计划完成） |
| Step 1 合同层 | `portfolio/requirements/contract-register.md`（项目集）/ `requirements/contract-register.md`（单项目） | 合同登记册：每份合同（CON-NNN）的 scope_level/parent_contract_id/coverage/文档簇关联（CR-20260813-002） |
| Step 2 项目层 | `context/project-index.md` | 子项目清单 |
| Step 2 项目层 | `context/project-brief.md` | 子项目清单 |
| Step 3 计划层 | `context/project-brief.md` | 计划概览（阶段名称/时间段）+ 一行摘要 |
| Step 3 计划层 | `context/project-index.md` | 子项目清单的计划阶段数列 |
| Step 4 需求层 | `requirements/requirement-register.md` | 需求数量、需求ID列表字段 |
| Step 5 资源层 | `projects/{子项目}/resources/resource-register.md`（项目集模式按子项目分建） | 资源清单 + 计划分配视图 |
| Step 5 资源层 | 待办文件 §0 人员信息段（首次出现时引导填写，v2.1.0） | 岗位/联系方式/负责模块/进出组日期（身份快照，T+1 拷贝） |
| Step 6 里程碑层 | `plans/progress-plan.md` | 计划日期 |

---

## 6. 异常处理

| 场景 | 处理方式 |
|------|----------|
| 用户中途退出 | 保存已录入信息到 `project-brief.md` 草稿区域，更新 `init_wizard_progress` |
| 用户提供的信息与已有文件冲突 | 提示冲突项，询问以哪个为准 |
| 用户上传文件解析失败 | 提示解析失败原因，改为对话式录入 |
| 项目集模式下某子项目信息暂时不可用 | 该子项目的计划/需求/资源步骤标记为"待补充"，不阻塞其他子项目 |
| 计划阶段数为 0 | 允许，跳过计划相关步骤 |
| 重复触发向导 | 检测到 `status: 已确认` 时提示"项目已完成初始化，是否需要修改？" |

---

## 7. 文件上传解析规则

当用户在向导过程中上传文件时：

1. AI 先读取 `context/project-brief.md` 判断项目归属（即使 brief 是草稿也读取）。
2. 按文件类型选择解析方式：
   - 合同文档 → 提取合同名称/总额/类型/范围/时间
   - 需求清单 → 提取需求数量/需求ID/功能模块
   - 计划表 → 提取阶段名称/时间段/人员/任务
3. 解析结果结构化展示，请用户确认。
4. 确认后填入对应向导步骤。
5. 解析失败时降级为对话式录入。

---

## 7a. 可选步骤：推导基线（entity-registry）

> 仅当项目存在多模块/多阶段/多市场主体时提示，单模块简单项目可跳过。

**触发条件**：向导 Step 3（计划层）完成后，若检测到项目含 ≥2 个模块或 ≥3 个计划阶段，AI 主动提示：

```
【可选步骤 推导基线】
检测到项目含多个模块/阶段，建议创建实体登记册（entity-registry），
用于周报生成时的实体枚举校验和生命周期状态推导。
是否现在创建？（可稍后通过完整性巡检触发）
```

**创建流程**：
1. 从 `assets/templates/entity-registry-template.md` 创建 `context/entity-registry.md`
2. 引导用户填入已知实体清单（可从已录入的计划/需求信息推断）
3. 引导用户确认项目级推导链覆盖（如"预演"等特有阶段）
4. 写入后标注 `status: 草稿`，待用户确认后改为 `已确认`

**与其他规则的关系**：
- 创建后触发 `00-pm-main-rules.md` §10 推导基线机制
- 完整性巡检（`19-info-completeness-rules.md` §3.3a）检查其存在性和完整性

---

## 8. 与其他规则的关联

| 关联规则 | 关系 |
|----------|------|
| `00-pm-main-rules.md` §2.7 | 默认意图检测新增"初始化"意图，路由到本规则 |
| `06-file-rules.md` | 文件写入操作遵循文件规则 |
| `10-update-trigger-rules.md` | 向导写入属于高风险操作（基线信息），必须用户确认 |
| `19-info-completeness-rules.md` | 向导完成后，日常巡检接管信息完整性持续检查 |
