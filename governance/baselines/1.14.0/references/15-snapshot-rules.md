# 计划快照与实际执行规则

本规则用于支持历史计划回查、计划 vs 实际偏差对比、历史计划批量导入。当前待办查询用索引，历史计划回查用快照，执行结果用 actuals。

---

## 1. 核心原则

1. **当前待办用索引，历史计划用快照，执行结果用 actuals。**
2. 快照在每日生成 PM 待办时自动创建，冻结不可静默覆盖；历史计划批量导入生成的快照同样冻结、与 AI 快照不互相覆盖。
3. 实际执行摘要在处理目标日期日报后自动生成。
4. 热数据（近 7 天 + 未来 14 天）在 `daily-todo-index.md`，冷数据在 `snapshots/` 和 `actuals/`。
5. 历史计划查询不得默认全量扫描日报，必须优先读取快照和实际摘要。

---

## 2. 目录结构

```
ai/portfolio/todos/
├── personal-todo-index.md          # 当前按人待办索引（热数据，可变）
├── daily-todo-index.md             # 当前按日期待办索引（热数据，可变）
├── weekly-todo-index.md            # 当前按周待办索引（热数据，可变）
├── history-index.md                # 历史快照索引（可变，追加）
├── snapshots/                      # 计划快照：当时计划做什么（冻结）
│   ├── daily/
│   │   ├── {YYYYMMDD}.md           # AI 前向生成
│   │   └── imported-{YYYYMMDD}.md  # 历史计划批量导入（source_type=external_import）
│   ├── weekly/
│   │   └── {YYYY}-W{WW}.md
│   └── monthly/
│       └── {YYYYMM}.md
└── actuals/                        # 实际执行摘要：当天/当周实际做了什么（可追加）
    ├── daily/
    │   └── {YYYYMMDD}.md
    └── weekly/
        └── {YYYY}-W{WW}.md
```

---

## 3. 文件性质对比

| 文件 | 性质 | 是否可变 | 用途 |
|---|---|---|---|
| `daily-todo-index.md` | 当前待办索引 | 可变 | 快速查询今天/明天/近期待办 |
| `snapshots/daily/{date}.md` | 历史计划快照 | 原则冻结 | 回查某日形成的次日计划 |
| `snapshots/daily/imported-{date}.md` | 导入计划快照 | 原则冻结 | 回查批量导入的历史计划（external_import） |
| `actuals/daily/{date}.md` | 实际执行摘要 | 可追加 | 对比某日实际完成情况 |
| `history-index.md` | 历史快照目录 | 可变（追加） | 快速定位历史计划/实际文件 |
| `snapshots/weekly/{week}.md` | 周计划快照 | 原则冻结 | 回查某周原计划 |
| `actuals/weekly/{week}.md` | 周实际执行 | 可追加 | 对比某周实际完成 |

---

## 4. 热数据与冷数据分离

`daily-todo-index.md` 只保存近期热数据：

- 过去 7 天 + 未来 14 天

更早历史查询转向：

```
history-index.md → snapshots/ + actuals/
```

---

## 5. 快照生成时机

| 触发动作 | 生成文件 |
|---|---|
| 生成 PM 明日待办 | `snapshots/daily/{today}.md` + 更新 `history-index.md` |
| 处理个人日报中的明日计划 | 更新 `personal-todo-index.md` + `daily-todo-index.md` |
| 生成周计划 | `snapshots/weekly/{week}.md` + 更新 `history-index.md` |
| 历史计划批量导入（R1） | `snapshots/daily/imported-{date}.md` + 更新 `history-index.md`（见 §8a） |

---

## 6. 实际执行摘要生成时机

| 触发动作 | 生成文件 |
|---|---|
| 处理当天日报实际完成 | `actuals/daily/{today}.md` |
| 生成周报 | `actuals/weekly/{week}.md` |
| 任务状态变更 | 更新 `personal-todo-index.md`，必要时追加 `actuals` |

---

## 7. 快照内容规范

### 7.1 日快照字段

| 字段 | 说明 |
|---|---|
| snapshot_date | 快照生成日期（当天） |
| target_date | 计划目标日期（通常为次日；导入快照可为任意历史/未来日期） |
| created_at | 生成时间 |
| source_type | 来源类型（personal_daily_reports / pm_todo / meeting / external_import） |
| status | frozen（冻结） |

**source_type 语义（统一）**：
- `personal_daily_reports`：从**个人日报**明日计划提取生成。
- `pm_todo`：生成 PM 待办时生成。
- `meeting`：从会议纪要提取生成的计划。
- `external_import`：从 `.pod`/Excel 等外部文件**批量导入**生成（见 §8a），`daily_reports` 已并入上述语义，历史文件中的 `daily_reports` 按 `personal_daily_reports` 兼容解读。

### 7.2 快照章节

1. PM 直接任务
2. 全团队目标日期计划（按子项目分组）
3. 需跟进风险
4. 需跟进问题
5. 里程碑关注
6. 资源提醒
7. 无计划项目

---

## 8. 实际执行摘要内容规范

### 8.1 字段

| 字段 | 说明 |
|---|---|
| actual_date | 实际执行日期 |
| created_at | 生成时间 |
| source_type | 来源类型（personal_daily_reports；沿用历史 `daily_reports` 亦兼容） |
| status | draft / final |

### 8.2 章节

1. **完成汇总**：原计划完成情况（Todo ID / 计划任务 / 实际结果 / 完成状态 / 证据来源）
2. **计划外工作**：未在计划中但实际完成的工作
3. **延期/结转**：原计划未完成，延期到何时，原因

### 8.3 完成状态取值

| 状态 | 说明 |
|---|---|
| planned_done | 原计划且已完成 |
| planned_not_done | 原计划但未完成 |
| blocked | 原计划但被阻塞 |
| cancelled | 原计划取消 |
| carried_forward | 原计划延期/结转 |
| unplanned_done | 未计划但实际完成 |
| no_evidence | 缺少实际证据 |

---

## 8a. 历史计划批量导入快照（external_import，R1）

### 8a.1 触发与目的

用户提供历史计划文件（`.pod` OmniPlan / Excel 计划表）并要"导入历史计划 / 同步进计划体系"时触发。目的是把**一次性回溯灌入**的历史计划落为快照，供回查与后续计划变更追踪，**而非逐日前向生成**。

### 8a.2 数据源与确认

1. 读取 `.pod`/Excel，解析计划字段（Task/Owner/Due Date，如文件含历史任务级别用 `一级/二级` 映射到 Task）。
2. 生成**导入候选**（含 Original Due Date 映射），输出"建议导入清单"。
3. **人工确认后**才落库（事实源确认原则）。
4. 与 `references/13-continuity-rules.md` 划界：13 号管风险/问题/需求等过程记录的结转；R1（本小节）**只**管任务计划数据的批量导入为快照，二者并行不重叠。

### 8a.3 生成文件与命名

- 文件：`snapshots/daily/imported-{date}.md`（date 为计划目标日期）或按周 `snapshots/weekly/imported-{week}.md`。
- 命名用 `imported-` 前缀，**与 AI 前向生成的 `{date}.md` 区分，不互相覆盖**。
- frontmatter 字段：`source_type: external_import` + `import_source`（原始文件路径）+ `import_date`（导入动作日期）+ `status: frozen`。

### 8a.4 冻结与修订

- 导入快照同样**默认冻结**；修订通过追加 `Revision Log`（见 §11），不静默覆盖。
- 导入后同步登记 `history-index.md`（标注 source_type=external_import）。

### 8a.5 与 board 联动

导入的计划若需进入任务看板追踪变更/延期（R2/R3），将解析结果回填 `tasks/board.md`（Original Due Date / Due Date / Plan Change Count / Delay Count），规则见 `references/03-task-board-rules.md`。

---

## 9. 计划 vs 实际对比规则

当用户查询计划完成情况或计划偏差时，AI 必须同时读取：

1. 对应计划快照 `snapshots/daily/{snapshot_date}.md`（导入计划为 `imported-{date}.md`）
2. 对应实际执行 `actuals/daily/{target_date}.md`

输出对比表：

```markdown
## 计划 vs 实际对比 - {target_date}

| Todo ID | Owner | Planned Task | Actual Result | Completion Status | Evidence |
|---|---|---|---|---|---|
| TODO-20260810-001 | 陈佳菁 | 接口联调 | 已完成联调 | planned_done | 日报 |
| TODO-20260810-002 | 胡康利 | 修复认证问题 | 等待接口文档 | blocked | 日报 |

### 偏差汇总
- 原计划：5 项
- 已完成：3 项（60%）
- 未完成：1 项（阻塞）
- 延期：1 项
- 计划外完成：2 项
```

---

## 10. 历史查询路由

### 10.1 触发词

往日计划、历史计划、过去某天、之前某天、某月某日原计划、某月某日实际完成、计划完成情况、计划偏差、计划有没有完成、上周计划对照、上周二大家原来要做什么、某人上周每天计划、导入的历史计划、同步进来的计划

### 10.2 查询顺序

1. 读取 `history-index.md`
2. 定位 `snapshots/daily/{date}.md` 或 `snapshots/weekly/{week}.md`（导入计划定位 `imported-{date}.md`）
3. 如查询实际完成，读取 `actuals/daily/{date}.md` 或 `actuals/weekly/{week}.md`
4. 如快照/实际摘要不存在，读取对应月份日报索引
5. 用户确认后才允许扫描具体日报明细

### 10.3 常见查询路由

| 用户问题 | 读取路径 |
|---|---|
| 8月10日大家原计划做什么 | `history-index.md` → `snapshots/daily/20260809.md`（snapshot_date=08-09, target_date=08-10） |
| 8月10日实际做了什么 | `actuals/daily/20260810.md` |
| 8月10日计划完成了吗 | `snapshots/daily/20260809.md` + `actuals/daily/20260810.md` |
| 上周计划偏差 | `snapshots/weekly/{week}.md` + `actuals/weekly/{week}.md` |
| 某人过去一周每天计划 | `history-index.md` → 多个 daily snapshots |
| 导入的那批计划 | `history-index.md` → `snapshots/daily/imported-{date}.md`（source_type=external_import） |

---

## 11. 快照冻结规则

1. 快照生成后默认冻结，不得静默覆盖（含 external_import 导入快照）。
2. 如发现抽取错误，在快照末尾追加 `Revision Log`。
3. 修订记录格式：

```markdown
## Revision Log
| Time | Change | Reason | Operator |
|---|---|---|---|
| 2026-08-09 22:10 | 补充陈佳菁计划项 | 原日报补录 | AI |
```

---

## 12. Todo ID 规则

格式：`TODO-{target_date}-{NNN}`

示例：`TODO-20260810-001`

- target_date：计划目标日期
- NNN：当日序号（001~999）

如果任务进入后续多日滚动，保持同一个 Todo ID，在 actuals 中引用。

---

## 13. 周快照与周实际

### 13.1 周快照

每周一或生成周计划时创建 `snapshots/weekly/{YYYY}-W{WW}.md`：

- 本周各子项目重点计划
- 关键里程碑
- 重点风险
- 资源安排
- 跨项目协调事项

### 13.2 周实际

周末或生成周报时创建 `actuals/weekly/{YYYY}-W{WW}.md`：

- 本周实际完成
- 本周偏差
- 未完成原因
- 下周结转

---

## 14. 与其他规则的关系

| 规则 | 职责 |
|---|---|
| `05-query-rules.md` | 历史查询路由、热/冷数据分离、聚合计数秒答 |
| `01-daily-report-rules.md` | 日报处理时生成 snapshot 和 actuals |
| `10-update-trigger-rules.md` | 触发 snapshot/actuals 更新 |
| `06-file-rules.md` | 快照冻结规则、热/冷数据边界、external_import 命名 |
| `14-self-check-rules.md` | 快照完整性校验 |
| `03-task-board-rules.md` | 计划变更计数、延期计数、超期判定（B 类） |
| `13-continuity-rules.md` | 与 R1 划界（13 管结转，R1 管计划数据导入） |

## 15. 存储生命周期

热数据（当前索引中引用的快照/实际）：保留在原位。
温数据（90 天内的快照/实际文件）：保留在原位。
冷数据（>90 天的快照/实际文件）：
- 触发：每周检查一次（在周报生成时顺带检查）
- 动作：将 >90 天的文件移动到 `snapshots/archive/YYYY/` 和 `actuals/archive/YYYY/`
- 更新 `history-index.md`：归档条目标记为 `[已归档]`，不删除文件

`history-index.md` 自身瘦身：
- >200 行时，将 >180 天的已完成条目移至 `history-index-archive.md`
