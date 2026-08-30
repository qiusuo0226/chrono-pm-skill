# source-split-skill — 能力目录（不是独立 Skill）

当前版是 ChronoPM-Project 内的能力目录，**禁止**命名为 `SKILL.md`。宿主不得把本目录扫成第二个 Skill。

- **何时加载**：命中拆文件/拆文档/入库源文档，或 SKILL.md「源文档拆解」行。由 P-DOC-INGEST 强制 CALL，加载 `references/split-rules.md`。日报/待办/简单查询默认不加载。
- **产出**：`requirements/sources/{编号}/` 六件套。工人只写 `atoms/part-NN-*.md`，不写 ledger/_index。
- **交叉点**：只允许 REQ/WP 编号与术语入流。不反向依赖日报/待办。
- **将来抽包**：补 `SKILL.md` 作入口 → 抽出独立发行包 → 主 SKILL 改加载外部包。

规则权威：拆文件正文在本目录 `references/split-rules.md`；需求/工作包绑定仍在 Project `references/07-requirement-rules.md`。
