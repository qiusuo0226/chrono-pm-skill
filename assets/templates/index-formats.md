# 索引格式模板

本模板提供各类索引文件的完整 markdown 代码块。06-file-rules.md §7 只声明各索引**必须包含的列**，完整格式以此处为准。

## 1. 日报索引

```
| Date | Type | File | Owner | Summary | Task Sync | Risk Sync | Issue Sync | Weekly Sync |
|---|---|---|---|---|---|---|---|---|
```

## 2. 会议索引

```
| Date | Meeting ID | Title | Key Decisions | Action Items | File |
|---|---|---|---|---|---|
```

## 3. 周报索引

```
| Week | Date Range | File | Status | Key Highlights |
|---|---|---|---|---|
```

## 4. 复盘索引

```
| Date | Event | Milestone | File | Key Lessons |
|---|---|---|---|---|
```

## 5. Change Log

```
| Date | Change Type | Description | Source | Confirmed By |
|---|---|---|---|---|
```

- Change Type：`add` / `update` / `remove` / `status` / `archive`
- Source：来源文件或会议 ID
- Confirmed By：确认人姓名（AI 建议的记录为"待确认"）

> **概念域说明**：本条 Change Type 为**概念域 A（记录操作）**。它与 `references/08-change-control-rules.md` / change-log-template.md 的**概念域 B（变更影响分类）**（`requirement/scope/schedule/cost/resource/plan_change`）是不同维度，二者不合并。各事实源 Change Log 用概念域 A；需求/计划变更登记用概念域 B。
