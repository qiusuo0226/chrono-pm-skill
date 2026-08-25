# 源文档拆解规则（能力目录正文）

由 P-DOC-INGEST / P-SPLIT 加载本文件（SKILL.md「源文档拆解」行）。禁止未加载本文件就声称已拆解入库。需求/工作包绑定见 Project `07-requirement-rules.md`。

**工人只写** `requirements/sources/{编号}/atoms/part-NN-*.md`（或 facts 分片）。ledger、`sources/_index.md`、parse-log 收尾由协调者写。禁止工人写 `_index`。

拆解只产需求清单条目（默认未确认），**不落待办**。

过程日志：每步结束立刻写 `logs/ops/` 一行（模型/token/耗时；无接口写「未知」）。字段抽空记表 B。

pending-changes 已退役，待确认进 `ai/pm-decisions.md`。

---

#### ledger.md 字段规范（sources/ 拆解台账）

每个 `requirements/sources/{编号}/` 配一份 `ledger.md`。存量 `{type}-source/` 未迁完时仍可读其 ledger。

| 字段 | 必填 | 说明 |
|---|---|---|
| source_id | 是 | 目录编号（SRC-NNN 或簇固定号） |
| file | 是 | 相对本目录的文件名（或外部指针名） |
| file_type | 是 | pdf/docx/xlsx/md/其他 |
| size_kb | 否 | 工具可得时填；否则 — |
| source_fingerprint | 是 | **优先 MD5**；不可得回退「大小+mtime」 |
| file_created | 否 | 不可得填 —，不猜测 |
| source_version | 是 | PM 登记；未知标「版本未知-指纹{8位}」 |
| description | 否 | ≤30 字；不可得 — |
| parse_history | 是 | 轮次计数 + 最近日期，明细见 parse-log.md |

必填最小集：source_id / file / file_type / source_fingerprint / source_version / parse_history。parsed_by / parsed_at 只在 parse-log。

跨项目：簇固定号 + source_fingerprint 去重。指纹相同视为同一文档副本，**禁止二次拆解**。

#### 编号

| 用途 | 格式 |
|---|---|
| 项目内任意源文档 | `SRC-NNN` |
| 跨项目共享 / 文档簇 | CON-/BID-/INIT-/COMP-/SUP-/TRN- + `{YYYYMMDD}-{HHmmss}` |

SRC-NNN **不得**作跨项目互认键。

#### 目录与加载

`requirements/sources/{编号}/`：meta.md、_digest.md、atoms.md（或 `atoms/` 分片）、facts.md（或 `facts/`）、ledger.md、parse-log.md。查询先读 `sources/_index.md` → `_digest.md` → 取证才读 atoms/facts。存在性以 `sources/*/meta.md` 为准。

#### 同源判定与接收侧对账 WF-SD-1

同源只看输入侧：`(簇固定号 OR source_doc 指针名+版本) + source_fingerprint` 相同即为同源。

```
Step 1 扫描新纳入项目 sources/*/ledger.md（+meta 指纹）
Step 2 与其余项目比对互认键
Step 3 ├─ 指纹相同 → 同源副本：已有则跳过；没有则复制首拆并标 shared_from
       ├─ 簇 ID 同、指纹不同 → SUGGEST 重拆
       ├─ 文件名相似但指纹不同 → 待裁决写入 pm-decisions，禁止擅自归并
       └─ 无匹配 → 新建
Step 4 更新 _index.md；输出对账报告
```

#### atoms/facts 分片

>300 条或 >1500 行 → 转 `atoms/` 或 `facts/`：按章节分片 `part-NN-{章节}.md` + `_index.md`。禁止按行数硬切条款。工人只写 part 文件。

#### REQ 自动编号

拆解产 REQ 自动取号 `REQ-[模块代号]-NNN`。模块代号：CON→CONTRACT、BID→BID、INIT→INIT、COMP→COMP、SUP→SUPPLEMENT、TRN→TRANSFER、SRC→登记册既有或文档缩写。NNN 在该代号下接续。**只写入需求清单，不落待办。** WP 绑定见 07。

#### 共享复制

首个登记项目拆解一次，`sources/{簇 ID}/` 复制到各覆盖项目（meta.`shared_from`）。禁止二次拆解。本包不写 `portfolio/`。
