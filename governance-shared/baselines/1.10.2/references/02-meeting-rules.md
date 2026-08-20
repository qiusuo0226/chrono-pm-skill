# 会议纪要约束规则

本规则适用于会议纪要的生成、行动项提取和事实源同步。

---

## 0b. 评审记录术语归一化预处理

在提取评审结论、行动项、遗留问题、需求变更前，执行术语归一化：

1. 读取 `ai/portfolio/context/domain-glossary.md`（如不存在，跳过，按现有逻辑处理）
2. confirmed 术语可静默归一化
3. pending 术语仅作为候选理解，并在评审整理结果中标注待确认
4. low/conflict 术语保留原文，进入待确认问题
5. 不得基于 pending/low/conflict 直接写入确定事实源
6. 输出评审整理结果时保留原文片段和归一化记录
7. 无术语变化时不输出归一化记录

**禁止规则：**

- pending 条目不得静默替换
- 涉及该术语的事实源更新只写草稿，不进入正式事实源
- 原文片段必须保留

---

## 1. 会议纪要模板

```markdown
---
doc_type: meeting
project: [项目名]
meeting_id: MTG-YYYYMMDD-NNN
title: [会议主题]
date: YYYY-MM-DD
time: HH:MM ~ HH:MM
location: [地点/线上]
participants: [参会人员列表]
organizer: [组织者]
status: 草稿
---

# 会议纪要 - [会议主题] - YYYY-MM-DD

## 1. 会议目的
（1-2 句话说明为何开会）

## 2. 参会人员
| 姓名 | 角色 | 部门/单位 |
|---|---|---|

## 3. 议题与讨论
### 3.1 [议题1]
- 讨论：[讨论内容摘要]
- 结论：[结论，如无结论标注"待确认"]

### 3.2 [议题2]
- 讨论：[讨论内容摘要]
- 结论：[结论]

## 4. 行动项
| Action ID | 描述 | 负责人 | 截止日期 | 关联任务 | 关联需求 | 状态 |
|---|---|---|---|---|---|---|
| A-001 | [行动项描述] | [姓名] | YYYY-MM-DD | T-YYYYMMDD-NNN | REQ-XXX-NNN | todo |

## 5. 决策
| Decision ID | 描述 | 决策人 | 关联事项 |
|---|---|---|---|
| D-YYYYMMDD-NNN | [决策描述] | [决策人] | [关联] |

## 6. 风险与问题
### 6.1 新增风险
| Risk ID | 描述 | 类别 |
|---|---|---|

### 6.2 新增问题
| Issue ID | 描述 | 影响范围 |
|---|---|---|

## 7. 需求变更（如有）
| Change ID | 描述 | 提出人 | 当前状态 |
|---|---|---|---|

## 8. 下次会议（如有）
- 时间：
- 议题：

## 建议更新清单
| Target File | Update Type | Suggested Change | Reason | Need Confirmation |
|---|---|---|---|---|

## 信息来源
- 会议形式：[现场/线上/口述]
- 记录人：[姓名]
```

## 2. 行动项提取规则

1. 会议纪要中的行动项必须提取为任务候选。
2. 如果缺少负责人、截止时间或完成标准，进入 `tasks/backlog.md` 或标记为"待确认"，不得直接进入正式进行中任务。
3. 行动项必须有 Action ID（格式：`A-NNN`），后续同步到任务看板时分配 Task ID。
4. 行动项必须标注来源会议 ID。

## 3. 事实源同步规则

会议纪要生成后，AI 必须识别以下同步项：

| 会议内容类型 | 目标文件 | 处理方式 |
|---|---|---|
| 明确行动项 | `tasks/board.md` 或 `tasks/backlog.md` | 建议新增任务 |
| 暂未排期事项 | `tasks/backlog.md` | 建议新增到 backlog |
| 潜在风险 | `risks/risk-register.md` | 建议新增风险 |
| 已发生问题 | `issues/issue-register.md` | 建议新增问题 |
| 关键决策 | `decisions/decision-log.md` | 建议新增决策记录 |
| 需求变更 | `requirements/change-log.md` | 建议新增变更请求（submitted 状态） |
| 里程碑调整 | `milestones/milestone-board.md` | 建议更新里程碑状态 |

所有同步项必须通过"建议更新清单"输出，人工确认后执行。

## 4. 会议纪要归档规则

1. 会议纪要按日期存放：`meetings/YYYY/MM/YYYY-MM-DD-topic.md`。
2. `meetings/index.md` 必须维护索引：

```markdown
| Date | Meeting ID | Title | Key Decisions | Action Items | File |
|---|---|---|---|---|---|
| 2026-08-09 | MTG-20260809-001 | 周例会 | D-20260809-001 | A-001~A-003 | meetings/2026/08/... |
```

3. 会议纪要状态流转：`草稿` → `已确认` → `已归档`。
4. 已确认的纪要不可直接修改，如有更正需追加"更正记录"。

## 5. 特殊规则

- 如果会议中讨论了需求范围变更但未正式提出变更请求，AI 必须提示走正式变更流程。
- 如果会议中做出的决策与已有决策记录冲突，必须标注冲突并提示项目经理确认。
- 如果会议纪要来源是口述或非正式沟通，必须在信息来源中标注"口述/非正式"。
