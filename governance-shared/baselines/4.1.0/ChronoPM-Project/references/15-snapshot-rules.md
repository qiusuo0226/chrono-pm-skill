# 快照与历史计划导入规则（V2.10 精简版）

本规则仅保留两项能力：①历史计划批量导入（external_import）；②快照/实际执行摘要的读取规则。待办体系已替代原索引机制，快照仅用于历史回查。

---

## 1. 核心原则

1. **快照 = 冻结的历史记录**（"那天计划是什么"），用于计划 vs 实际对比。
2. 当前待办查询走 `todos/{date}/` 目录，不走快照索引。
3. 历史计划批量导入（external_import）生成的快照冻结、不可静默覆盖。
4. 实际执行摘要在处理目标日期日报后自动生成。

---

## 2. 目录结构

```
todos/
├── snapshots/                      # 计划快照：当时计划做什么（冻结）
│   ├── daily/
│   │   ├── {YYYYMMDD}.md           # AI 前向生成
│   │   └── imported-{YYYYMMDD}.md  # 历史计划批量导入（source_type=external_import）
│   └── weekly/
│       └── {YYYY}-W{WW}.md
└── actuals/                        # 实际执行摘要：当天/当周实际做了什么（可追加）
    ├── daily/
    │   └── {YYYYMMDD}.md
    └── weekly/
        └── {YYYY}-W{WW}.md
```

---

## 3. 快照读取规则

当用户查询历史计划或计划偏差时：

1. 读取对应计划快照 `snapshots/daily/{snapshot_date}.md`（导入计划为 `imported-{date}.md`）
2. 读取对应实际执行 `actuals/daily/{target_date}.md`
3. 输出对比表

### 3.1 常见查询路由

| 用户问题 | 读取路径 |
|---|---|
| 某日大家原计划做什么 | `snapshots/daily/{前一日}.md` |
| 某日实际做了什么 | `actuals/daily/{当日}.md` |
| 某日计划完成了吗 | 快照 + 实际摘要对比 |
| 上周计划偏差 | `snapshots/weekly/` + `actuals/weekly/` |
| 导入的那批计划 | `snapshots/daily/imported-{date}.md` |

### 3.2 归档日报读取协议（V2.6 B3）

升级前日期的日报读取 archive 旧日报格式，升级后日期读取待办文件。拼接时标注数据源切换点。

### 3.3 Change Log 月归档读取（v3.8.0）

change-log 月归档属活历史，**索引受控可读**：优先查活跃区 → `change-log/index.md` 导航 → 按指向读 `change-log/archive/YYYYMM-change-log.md`。禁止遍历 archive 目录。`backup/` 与 migration-log「视为 backup」目录不是本协议范围，禁读。

---

## 4. 快照冻结规则

1. 快照生成后默认冻结，不得静默覆盖（含 external_import 导入快照）。
2. 如发现抽取错误，在快照末尾追加 `Revision Log`。

---

## 5. 历史计划批量导入（external_import）

### 5.1 触发与目的

用户提供历史计划文件（`.pod` OmniPlan / Excel 计划表）并要"导入历史计划 / 同步进计划体系"时触发。目的是把一次性回溯灌入的历史计划落为快照，供回查与后续计划变更追踪。

### 5.2 数据源与确认

1. 读取 `.pod`/Excel，解析计划字段（Task/Owner/Due Date）。
2. 生成导入候选，输出"建议导入清单"。
3. **人工确认后**才落库（事实源确认原则）。

### 5.3 生成文件与命名

- 文件：`snapshots/daily/imported-{date}.md`（date 为计划目标日期）
- 命名用 `imported-` 前缀，与 AI 前向生成的 `{date}.md` 区分，不互相覆盖
- frontmatter 字段：`source_type: external_import` + `import_source`（原始文件路径）+ `import_date`（导入动作日期）+ `status: frozen`

### 5.4 冻结与修订

- 导入快照同样默认冻结；修订通过追加 `Revision Log`，不静默覆盖。

---

## 6. 与其他规则的关系

| 规则 | 职责 |
|---|---|
| `05-query-rules.md` | 历史查询路由、聚合计数 |
| `01-daily-report-rules.md` | 日报处理时生成 snapshot 和 actuals |
| `06-file-rules.md` | 快照冻结规则、external_import 命名 |
| `13-continuity-rules.md` | 与 external_import 划界（13 管结转，本规则管计划数据导入） |
