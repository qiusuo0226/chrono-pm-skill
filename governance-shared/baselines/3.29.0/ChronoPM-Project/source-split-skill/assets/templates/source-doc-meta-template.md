---
doc_type: source-doc-meta
source_id: SRC-NNN
source_type: [registry 中的类型]
lifecycle_stage: [立项/招投标/合同签约/规划启动/需求设计/开发实施/测试/上线试运行/验收/售后结项/贯穿/监理]
version: v1.0
shared_from: —
coverage: 本项目
---

# SRC-NNN — {源文档名称}

> 一个源文档 = 本目录。落点：`requirements/sources/{编号}/`。
> 原始文档不入库，只存指针 + 指纹。跨项目共享须用簇固定号，禁止 SRC-NNN 作互认键。

## meta

| 字段 | 值 |
|---|---|
| 编号 | SRC-NNN |
| 源文档名称 | [名称] |
| 版本 | v1.0 |
| source_type | [类型] |
| 生命周期阶段 | [阶段] |
| 指针（source_doc） | [外部路径/文件名，不入库] |
| 指纹 | [MD5（可得时）；不可得回退 大小+mtime] |
| file_type | pdf/docx/xlsx/md/其他 |
| size_kb | [工具可得时填；否则 —] |
| file_created | [不可得填 —，不猜测] |
| 登记指针 | contract-register / sources/_index |
| 拆解状态 | 未拆 / 部分 / 完成 |
| 已拆章节 | [渐进导入断点] |
| 待拆章节 | [清单] |
| shared_from | — / {首次拆解项目} |
| local_only | false（副本项目专属 facts 标 true，不回流） |

## _digest（AI 专用索引，L2）

> 读本段即可理解全文语义，不读原文。单次加载预算 ≤400 行（沿用 RI-003）。

- 全文摘要：
- 章节导航：

## atoms.md（需求类 ATOM）

> kind ∈ requirement / requirement_directive / agreement / constraint。走 ATOM→Canonical→REQ。
> 监理/验收中的服务承诺/质保条款：kind=agreement/constraint，source_type 归 operational。

## facts.md（非需求类事实）

> kind ∈ background / baseline / hardware / spec / term / milestone_fact。
> **不进** Canonical / scope_scope 聚合。可供检索并 SUGGEST 填充 project-context，禁止与 project-context 双写（facts 为证据，context 为确认后摘要）。

## ledger.md（拆解台账，9 列）

> 必填最小集：source_id / file / file_type / source_fingerprint / source_version / parse_history。
> 选填：size_kb（工具可得时填）、file_created / description（不可得默认 —）。
> parsed_by / parsed_at 记在 parse-log.md，ledger 不双写。

| source_id | file | file_type | size_kb | source_fingerprint | file_created | source_version | description | parse_history |
|---|---|---|---|---|---|---|---|---|
| SRC-NNN | [文件名] | pdf/docx/xlsx/md/其他 | — | [MD5 或 大小+mtime] | — | v1.0 / 版本未知-指纹{8位} | — | 1 轮；最近 YYYY-MM-DD → parse-log.md |

## parse-log.md

见 `source-parse-log-template.md`。每轮拆解一行。
