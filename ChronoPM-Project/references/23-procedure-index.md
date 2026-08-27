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
| P-WF8-CARD | 基数恰好 1 | 00 §8b | WP 已规划且 effect=正常 | — | WP Ref=一个存在的 WP-NNN | 空/`待绑定`/none/多值落盘；绑废弃 WP |
| P-BOX | 时间盒 | 00 WF-8 时间盒门禁 | — | — | 不自动改日期；结束越界问 A/B/C | 静默改期 |
| P-WP-BOX-CHK | WP 窗变检查 | 00 §8c.1 | — | 越界才 P-BOX | pm-decisions（选 C） | 在窗内仍改待办时间 |
| P-PLAN-SYNC | 计划→WP | 00 §4b | — | — | WP 时间盒+计划投影 | 灌 todos |
| P-CARRY | 结转 | 22 | — | 有 Python 则先 `carryover_step0.py`；再 P-CARRY-WPREF（脚本已高置信回填则跳过） | 当日文件 | 改编号、改历史行；exit 0 后手搓全员 |
| P-CARRY-WPREF | 结转 WP Ref | 22 §5 | — | P-WF8-CARD | 仅空值高置信回填 | 猜填；改已有合法归属；无 WP 结转到今天核心表 |
| P-SPLIT | 源文档拆解 | `source-split-skill/references/split-rules.md` | 指纹查重 | 07 REQ 上提（不落待办） | `requirements/sources/{编号}/` 六件套 | 用 outputs HTML 替代；二次拆解 |
| P-DOC-INGEST | 拆文件分发 | 10 源文档信号 + SKILL 路由 | 读 project-brief | **必须 CALL P-SPLIT**；若还要报告再 P-OUTPUT | sources/ | 只出报告不入库 |
| P-REQ-DECOMP | 需求拆解 | 07 §3 | — | — | 需求清单 | 落待办；与 P-SPLIT 混淆 |
| P-REQ-WP | REQ↔WP | 07 | — | — | 登记册工作包列 / WP §2 | 需求正文抄进 WP |
| P-OUTPUT | 生成物 | 11 | P-ALWAYS 三路 | — | `ai/outputs/{批次}/` | 当事实源；替代 P-SPLIT |
| P-RI | 跨源范围判定 | 07 §8 | — | 可读 sources 索引 | 不新建源目录 | 把范围判定当成拆文件 |
| P-WP-SCAN | 待办聚人期 | 00 §8d | effect=正常 | 投影正常计划 §3 行+§4 该 WP 段；同回合 §8b | WP §8 (AI聚合)+§8b | 覆盖点名；全库扫；改 WP 整包窗；清空已冻结 ✅ 人期；改人期不写 8b |
| P-WP-ADVANCE | 建议推进链 | 00 §8d | PM 确认 | SCAN 可选 | §7 只追加 | 改旧链行；自动写链；effect=废弃仍推 |
| P-WP-RETIRE | 废弃 WP | 00 §8e | PM 确认+superseded_by | 移出正常计划 | YAML effect+§6+index | §7 到状态=废弃；删文件；自动改待办 |
| P-SKILL-GAP | 技能缺口笔录 | skill-gap-skill/references/gap-capture-rules.md | 闸 1=B；已载 11 | **必须 CALL P-OUTPUT**（skill_gap **不建 manifest**）；写主文件后、登记 index 前对照当前模板逐必选节自检 | outputs/需求-*.md | 写事实源；写/提议 pm-decisions；问要不要记；简单查询瞎记；省 〇·五；以历史批次为范本 |
| P-WP-STAMP | 待办结论盖章 | 00 WF-1 18.8 | 正式待办 WP Ref=1 | — | WP §4b 一行 | 多文件复制正文；漏盖称办结完成；猜相关包 |
| P-WP-CHART | 派生总览图 | 11 §17 | effect=正常 且 头≠已完成 | 先 index | `wps/_wp-chart.md` | P-OUTPUT；编造边；指纹未变仍重写；废弃/已完成入默认图 |
| P-WP-ALIGN | 功能点全齐推进 | 00 §8d | 功能点 ≥1 行且阶段全同且非 — | — | WP §8 + §7 追加 + §6 来源 AUTO-全齐 | 问准不准；进 pm-decisions；改旧链行；无表仍推 |

调用（无环）：

```
P-ROUTE
 ├─ 派活/加待办 → P-WF8 → P-CARRY → P-CARRY-WPREF → P-WF8-DEDUP → (P-WF8-SPLIT) → P-WF8-CARD → P-BOX
 ├─ 改计划排期 → P-PLAN-SYNC →（WP 窗变）P-WP-BOX-CHK →（越界）P-BOX
 ├─ 拆文件/拆文档/入库源文档 → P-DOC-INGEST → P-SPLIT → P-REQ-WP
 │                              └─（仅当还要对外文件）P-OUTPUT
 ├─ 拆解需求（无源文件） → P-REQ-DECOMP
 ├─ 跨源范围判定 → P-RI
 ├─ 出 HTML/xlsx（无拆文件） → P-OUTPUT
 ├─ 废弃 WP → P-WP-RETIRE
 ├─ 扫 WP 人期 → P-WP-SCAN →（若待确认）P-WP-ADVANCE
 ├─ 待办办结/敲定 → P-WP-STAMP
 ├─ 新建/改/完成归档/废弃 WP → P-WP-CHART
 ├─ 功能点阶段全齐 → P-WP-ALIGN
 └─ 技能缺口 → P-SKILL-GAP → P-OUTPUT
```

P-ALWAYS 第 4 步只检测是否 CALL 本树「技能缺口」分支，不写文件。