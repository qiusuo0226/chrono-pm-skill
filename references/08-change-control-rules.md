# 变更管理约束规则

本规则适用于需求变更、范围变更、进度变更、成本变更的识别、影响分析、审批和执行。需求管理基础规则见 `07-requirement-rules.md`。

---

## 1. 变更范围

本规则覆盖以下变更类型：

| 变更类型 | 说明 | 常见触发场景 |
|----------|------|--------------|
| 需求变更 | 新增、修改、删除需求 | 客户提出新需求、需求理解偏差 |
| 范围变更 | 项目交付范围调整 | 模块裁剪、交付物增减 |
| 进度变更 | 里程碑或交付时间调整 | 工期压缩、延期、提前交付 |
| 成本变更 | 预算调整 | 人力增减、外采变更 |
| 资源变更 | 人员或设备调整 | 人员变动、资源冲突 |

## 2. 变更流程

所有变更必须走以下流程，不可跳过任何环节：

```
变更请求提出 → 登记到 change-log.md（submitted）
  → 影响分析（assessing）
  → CCB/项目经理评审
  → 决策：批准 / 拒绝 / 延期
  → 若批准：执行变更 → 更新事实源
  → 若拒绝：记录原因，关闭变更
  → 通知相关干系人
```

### 2.1 关键规则

1. 任何疑似变更，不得直接更新事实源文件。
2. 必须先进入 `requirements/change-log.md`，状态为 `submitted`。
3. 变更未经审批前，相关事实源文件保持不变。
4. 客户口头需求不得直接进入需求登记册，只能进入 change-log 的 submitted 状态。

## 3. 变更登记

### 3.1 change-log.md 字段

| 字段 | 说明 | 必填 |
|------|------|------|
| Change ID | CR-YYYYMMDD-NNN | 是 |
| 变更类型 | requirement / scope / schedule / cost / resource | 是 |
| 描述 | 变更内容描述 | 是 |
| 变更前内容 | 原始状态 | 是 |
| 变更后内容 | 目标状态 | 是 |
| 提出人 | 提出者 | 是 |
| 提出日期 | YYYY-MM-DD | 是 |
| 变更原因 | 为什么变更 | 是 |
| 影响分析 | 见第 4 节 | 是（assessing 阶段） |
| 变更级别 | micro / normal / major | 是 |
| 审批结果 | approved / rejected / deferred | 否（审批后填） |
| 审批人 | 决策者 | 否 |
| 审批日期 | YYYY-MM-DD | 否 |
| 执行状态 | pending / implemented / cancelled | 否 |
| 关联需求 | REQ-XXX-NNN | 否 |
| 关联任务 | T-YYYYMMDD-NNN | 否 |
| 关联决策 | D-YYYYMMDD-NNN | 否 |
| Source | 来源 | 是 |

### 3.2 变更状态流转

```
submitted → assessing → approved → implemented
                     → rejected（关闭）
                     → deferred（暂缓，后续可重新评估）

任何状态 → cancelled
```

## 4. 影响分析

每次变更必须进行以下维度的影响分析：

| 维度 | 分析内容 | 输出 |
|------|----------|------|
| 范围影响 | 涉及哪些模块、哪些需求 | 受影响需求清单 |
| 进度影响 | 对里程碑和交付时间的影响 | 天数偏差、里程碑风险 |
| 成本影响 | 增加的工作量和人力成本 | 人天增量、成本增量 |
| 质量影响 | 对测试范围和质量风险的影响 | 测试范围变化、质量风险 |
| 风险影响 | 引入的新风险 | 新增风险项 |
| 依赖影响 | 对上下游模块的影响 | 依赖关系变化 |
| 验收影响 | 对验收标准和验收进度的影响 | 验收范围变化 |

### 4.1 影响分析输出模板

```markdown
## 变更影响分析

### 变更概述
- Change ID: CR-YYYYMMDD-NNN
- 变更类型: [类型]
- 描述: [描述]

### 范围影响
- 受影响需求: [REQ-XXX-NNN 列表]
- 受影响模块: [模块列表]

### 进度影响
- 工作量增量: [X] 人天
- 里程碑影响: [M-NN 是否延期]
- 预计进度偏差: [X]%

### 成本影响
- 人力成本增量: [X] 万元
- 预算偏差: [X]%

### 质量影响
- 测试范围变化: [说明]
- 质量风险: [说明]

### 风险影响
- 新增风险: [R-YYYYMMDD-NNN 或描述]

### 依赖影响
- 上下游影响: [说明]

### 验收影响
- 验收标准变化: [说明]
- 验收进度影响: [说明]
```

## 5. 变更分级

| 变更级别 | 判定标准 | 审批权限 |
|----------|----------|----------|
| 微变更(micro) | 工作量增量 ≤ 2人天，无里程碑影响，无成本基线影响 | 项目经理审批 |
| 一般变更(normal) | 工作量增量 2-10人天，可能有进度偏差，不涉及成本基线 | CCB 评审 |
| 重大变更(major) | 工作量增量 > 10人天，或影响里程碑，或影响成本基线，或影响合同范围 | CCB 评审 + 发起方确认 |

CCB（变更控制委员会）组成：项目经理、技术负责人、客户代表（如需）、发起方代表（重大变更时）。

## 6. 变更执行

### 6.1 批准后执行步骤

1. 更新 `requirements/change-log.md`：状态改为 `implemented`。
2. 更新 `requirements/requirement-register.md`：新增/修改/标记对应需求。
3. 更新 `tasks/board.md` 或 `tasks/backlog.md`：新增/调整对应任务。
4. 更新 `plans/progress-plan.md`：调整进度计划（如需）。
5. 更新 `plans/budget.md`：调整预算（如需）。
6. 更新 `milestones/milestone-board.md`：调整里程碑（如需）。
7. 更新 `risks/risk-register.md`：新增变更引入的风险（如有）。
8. 更新 `decisions/decision-log.md`：记录审批决策。
9. 通知相关干系人。

### 6.2 执行输出

```markdown
## 变更执行清单

| Target File | Update Type | Suggested Change | Confirmed |
|---|---|---|---|
| requirements/requirement-register.md | update | REQ-XXX-001 状态改为 changed | 待确认 |
| tasks/board.md | add | 新增 T-YYYYMMDD-NNN | 待确认 |
| ... | | | |
```

所有更新必须通过"建议更新清单"输出，人工确认后执行。

## 7. 变更记录独立性

1. `requirements/change-log.md` 是独立文件，不可将变更记录长期追加到 `requirement-register.md` 中。
2. 变更记录按时间顺序排列，最新的在最上面。
3. 已关闭的变更（rejected、cancelled、implemented）保留记录，不可删除。
4. 变更记录超过 100 条时，按季度归档到 `requirements/archive/`。

## 8. Change Log

change-log.md 本身不需要底部 Change Log（它本身就是变更记录）。但 requirement-register.md 底部需维护 Change Log，记录因变更导致的需求状态变化。
