# 23 过程调用索引

签名层，不是第二套规则。冲突时以 Home 节原文为准。本文件只约束「禁止跳过 callee」。

**何时加载**：写入 / 派活 / 拆文件 / 更新意图。纯查询不加载。

每条摘要 ≤200 字。改 Home 时同轮改本表 Calls。

| ProcID | 名称 | Home | Pre | Calls | Writes | Forbidden |
|---|---|---|---|---|---|---|
| P-ROUTE | 场景分发 | SKILL.md §6 | — | 命中行必须加载 | — | 用其他 Skill 替代本包过程 |
| P-WF8 | 待办创建 | 00 §9 WF-8 | P-CARRY | P-WF8-DEDUP → P-WF8-SPLIT? → P-WF8-CARD → P-BOX | inbox→`todos/{date}/{owner}.md` | 问「要不要建待办」；无 WP 落核心表；直写个人文件 |
| P-WF8-DEDUP | 查重 | 00 WF-8 查重步 | — | — | 不新建同主题 | 不查重就建第二条 |
| P-WF8-SPLIT | 多 WP 拆 | 00 归属④ | — | 每条 P-WF8-CARD | 多条待办 | 一条待办多个 WP Ref |
| P-WF8-CARD | 基数恰好 1 | 00 §8b | WP 已规划 | — | WP Ref=一个存在的 WP-NNN | 空/`待绑定`/none/多值落盘 |
| P-BOX | 时间盒 | 00 WF-8 时间盒门禁 | — | — | 不自动改日期；结束越界问 A/B/C | 静默改期 |
| P-WP-BOX-CHK | WP 窗变检查 | 00 §8c.1 | — | 越界才 P-BOX | pm-decisions（选 C） | 在窗内仍改待办时间 |
| P-PLAN-SYNC | 计划→WP | 00 §4b | — | — | WP 时间盒+计划投影 | 灌 todos |
| P-CARRY | 结转 | 22 | — | P-CARRY-WPREF | 当日文件 | 改编号、改历史行 |
| P-CARRY-WPREF | 结转 WP Ref | 22 §5 | — | P-WF8-CARD | 仅空值高置信回填 | 猜填；改已有合法归属；无 WP 结转到今天核心表 |
| P-SPLIT | 源文档拆解 | `source-split-skill/references/split-rules.md` | 指纹查重 | 07 REQ 上提（不落待办） | `requirements/sources/{编号}/` 六件套 | 用 outputs HTML 替代；二次拆解 |
| P-DOC-INGEST | 拆文件分发 | 10 源文档信号 + SKILL 路由 | 读 project-brief | **必须 CALL P-SPLIT**；若还要报告再 P-OUTPUT | sources/ | 只出报告不入库 |
| P-REQ-DECOMP | 需求拆解 | 07 §3 | — | — | 需求清单 | 落待办；与 P-SPLIT 混淆 |
| P-REQ-WP | REQ↔WP | 07 | — | — | 登记册工作包列 / WP §2 | 需求正文抄进 WP |
| P-OUTPUT | 生成物 | 11 | P-ALWAYS 三路 | — | `ai/outputs/{批次}/` | 当事实源；替代 P-SPLIT |
| P-RI | 跨源范围判定 | 07 §8 | — | 可读 sources 索引 | 不新建源目录 | 把范围判定当成拆文件 |

调用（无环）：

```
P-ROUTE
 ├─ 派活/加待办 → P-WF8 → P-CARRY → P-WF8-DEDUP → (P-WF8-SPLIT) → P-WF8-CARD → P-BOX
 ├─ 改计划排期 → P-PLAN-SYNC →（WP 窗变）P-WP-BOX-CHK →（越界）P-BOX
 ├─ 拆文件/拆文档/入库源文档 → P-DOC-INGEST → P-SPLIT → P-REQ-WP
 │                              └─（仅当还要对外文件）P-OUTPUT
 ├─ 拆解需求（无源文件） → P-REQ-DECOMP
 └─ 出 HTML/xlsx（无拆文件） → P-OUTPUT
```
