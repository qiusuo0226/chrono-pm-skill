# 任务看板约束规则

本规则适用于任务看板的字段定义、状态流转和关联管理。

---

## 1. 任务看板字段

`tasks/board.md` 是任务管理的核心事实源，字段定义如下：

| 字段 | 说明 | 必填 | 取值 |
|------|------|------|------|
| Task ID | 唯一标识 | 是 | T-YYYYMMDD-NNN |
| Title | 任务标题 | 是 | 自由文本 |
| Owner | 负责人 | 是 | 姓名 |
| Status | 当前状态 | 是 | todo / in_progress / blocked / review / done / cancelled |
| Priority | 执行优先级 | 是 | P0 / P1 / P2 / P3 |
| Plan Ref | 关联计划项 | 否 | P-NN |
| Milestone Ref | 关联里程碑 | 否 | M-NN |
| Requirement Ref | 关联需求 | 否 | REQ-XXX-NNN |
| Risk Ref | 关联风险 | 否 | R-YYYYMMDD-NNN |
| Issue Ref | 关联问题 | 否 | I-YYYYMMDD-NNN |
| Due Date | 预计完成日期 | 是 | YYYY-MM-DD |
| Actual Date | 实际完成日期 | 否 | YYYY-MM-DD |
| Source | 来源 | 是 | meeting / daily / manual / requirement |
| Source Ref | 来源文件 | 是 | 文件路径或会议 ID |
| Notes | 备注 | 否 | 自由文本 |

## 2. 任务状态流转

```
todo → in_progress → review → done
                ↓          ↑
             blocked ───────┘

任何状态 → cancelled
```

### 2.1 状态定义

| 状态 | 说明 | 进入条件 |
|------|------|----------|
| todo | 已分配但未开始 | 任务已创建，负责人已确认 |
| in_progress | 正在进行 | 负责人已开始执行 |
| blocked | 被阻塞 | 存在依赖未满足或外部问题 |
| review | 待评审 | 开发完成，等待代码审查或测试 |
| done | 已完成 | 评审通过，交付物已提交 |
| cancelled | 已取消 | 任务不再需要 |

### 2.2 流转规则

1. `todo → in_progress`：必须有负责人确认。
2. `in_progress → blocked`：必须记录阻塞原因和关联的 Issue ID。
3. `blocked → in_progress`：必须记录解除阻塞的条件和时间。
4. `in_progress → review`：必须有交付物或完成标准可验证。
5. `review → done`：必须通过评审，评审人需记录。
6. 任何状态 → `cancelled`：必须记录取消原因和决策人。

## 3. 任务与需求的关联

1. 需求描述"要实现什么"，任务描述"如何实现或交付"。
2. AI 不得将需求直接登记为任务，除非已明确拆解为可执行事项。
3. 每个任务必须能追溯到来源需求或来源会议/日报。
4. 一个需求可拆解为多个任务，但一个任务原则上只关联一个主需求。

## 4. 任务优先级

| 优先级 | 含义 | 判定标准 |
|--------|------|----------|
| P0 | 紧急且重要 | 阻断里程碑、影响验收、生产事故 |
| P1 | 重要不紧急 | 核心功能、关键路径任务 |
| P2 | 一般 | 辅助功能、优化类任务 |
| P3 | 低 | 非紧急、可延后 |

优先级不代表执行顺序，执行顺序由依赖关系和负责人安排决定。

## 5. 任务依赖

在 Notes 字段中记录依赖关系：

```markdown
depends_on: T-20260809-001
blocks: T-20260809-003, T-20260809-005
```

- `depends_on`：本任务依赖的前置任务。
- `blocks`：本任务阻塞的后续任务。

依赖关系变更时，必须在 Change Log 中记录。

## 6. Backlog 管理

`tasks/backlog.md` 用于存放：
- 尚未排期的任务。
- 需求拆解后尚未分配到迭代的任务。
- 会议中提出的待确认事项。

Backlog 中的任务字段简化：

| 字段 | 说明 |
|------|------|
| Task ID | T-YYYYMMDD-NNN |
| Title | 任务标题 |
| Source | 来源 |
| Priority | P0-P3 |
| Status | backlog |
| Notes | 备注 |

从 backlog 移入 board 时，状态改为 `todo`，并补全完整字段。

## 7. Change Log

`tasks/board.md` 底部必须维护 Change Log：

```markdown
## Change Log

| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
| 2026-08-09 | add | 新增 T-20260809-001 | MTG-20260809-001 | 张三 |
| 2026-08-09 | status | T-20260808-005: review → done | 日报 2026-08-09 | 李四 |
```

Change Log 超过 100 行时，拆分为独立的 `tasks/task-change-log.md`。
