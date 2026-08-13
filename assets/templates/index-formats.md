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

> **概念域说明**：本条 Change Type 为**概念域 A（记录操作）**。它与 `references/08-change-control-rules.md` / change-log-template.md 的**概念域 B（变更影响分类）**（`requirement/scope/schedule/cost/resource/plan_change`）是不同维度，二者不合并。各事实源 Change Log 用概念域 A；需求/变更登记用概念域 B。

## 6. RI 三级索引（CR-20260813-001）

### 6.1 L1 主索引 `requirements/atoms/atom-index.md`（路由表）

```
| source_category | ATOM 数 | L2 索引文件 | L3 全文文件 | last_source_version | last_updated |
|---|---|---|---|---|---|
| contractual | 12 | atoms/contractual-index.md | atoms/contractual.md | v1.2 | 2026-08-13 |
| procurement | 8 | atoms/procurement-index.md | atoms/procurement.md | v1.0 | 2026-08-13 |
| approval | 3 | atoms/approval-index.md | atoms/approval.md | v1.0 | 2026-08-13 |
| compliance | 2 | atoms/compliance-index.md | atoms/compliance.md | v1.0 | 2026-08-13 |
| technical | 0 | atoms/technical-index.md | atoms/technical.md | - | - |
| operational | 0 | atoms/operational-index.md | atoms/operational.md | - | - |
```

### 6.2 L2 类别倒排索引 `atoms/{category}-index.md`（覆盖索引，含 norm_text 摘要）

```
| keyword | ATOM ID | norm_text 摘要 | source_type | authority |
|---|---|---|---|---|
| 等保三级 | ATOM-contract-003 | 系统应满足等保三级 | contract | L4 |
| 身份认证 | ATOM-bid_doc-012 | 提供用户身份认证/登录 | bid_doc | L2 |
```

### 6.3 L3 ATOM 全文 `atoms/{category}.md`

```
- ATOM-contract-003 | kind=constraint | source_doc=合同V1.2 | source_ref=第8.2条 | authority=L4
  raw_text: 系统应满足网络安全等级保护三级要求。
  norm_text: 系统应满足等保三级。
  keywords: [系统][满足][等保三级]
  supersedes: -
  hash: <sha256> | updated: 2026-08-13
```

### 6.4 Canonical 索引 `requirements/canonical/canonical-index.md`

```
| CAN_ID | norm_text 摘要 | scope_scope | evidence 数 | status | 文件 |
|---|---|---|---|---|---|
| CAN-001 | 满足等保三级 | in_contract | 2 | active | canonical/CAN-001.md |
```

> 范围判定查询先读 canonical-index（含 scope_scope 摘要），命中后再打开 Canonical 全文，避免逐个打开文件（对齐覆盖索引理念）。

### 6.5 Source Type Registry `requirements/source-type-registry.md`

见 `assets/templates/source-type-registry-template.md`（source_category 固定 6 类 + source_type 项目级可扩展 + 默认 authority + 覆盖默认列）。
