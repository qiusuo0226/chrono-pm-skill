---
doc_type: source-atoms-index
source_id: SRC-NNN
---

# atoms/ 分片索引

> 当 atoms 或 facts **>300 条或 >1500 行**（06 号可配置软阈值）时转目录。
> 按章节分片，一条 ATOM 不跨片。查询先读本索引，单次只载 1 片。

| 分片 | 编号区间 | 章节 | 条数 | 摘要 |
|---|---|---|---|---|
| part-01-{章节}.md | ATOM-001 ~ ATOM-0nn | [章节] | n | ≤50 字 |
