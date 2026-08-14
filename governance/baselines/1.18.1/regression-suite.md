# Regression Suite

> 本文件是 ChronoPM Skill 的总回归测试清单。每次变更必须声明至少跑哪些用例。

---

## 1. Quick Query（快速查询）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QQ-001 | 我明天的待办是什么 | 优先读 `portfolio/todos/personal-todo-index.md`，输出 9 章节全景视图，不得只列 PM 个人任务 | positive |
| QQ-002 | 明天大家做什么 | 优先读 `daily-todo-index.md` | positive |
| QQ-003 | 本周重点是什么 | 优先读 `weekly-todo-index.md` | positive |
| QQ-004 | 张三现在在做什么 | 优先读 `summaries/张三-progress.md` | positive |
| QQ-005 | 当前有哪些风险 | 优先读 `risks/risk-register.md`（open），不扫描历史周报 | positive |
| QQ-006 | 8月10日大家原计划做什么 | 优先读 `history-index.md` → `snapshots/daily/` | positive |
| QQ-007 | 8月10日计划完成了吗 | 同时读 `snapshots/` + `actuals/`，输出对比表 | positive |
| QQ-008 | 上周计划偏差 | 同时读 `snapshots/weekly/` + `actuals/weekly/` | positive |
| QQ-009 | 项目进展如何 | 优先读 `tasks/board.md` + `milestones/`，不扫描所有过程记录 | positive |
| QQ-010 | 简单查询（明天待办） | 不得创建临时 JS/Python 脚本扫描目录 | regression |
| QQ-011 | 索引不存在时 | 提示用户重建索引，不自行全量扫描 | regression |

## 2. Daily Report（日报处理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DR-001 | 处理今天个人日报 | 写入 `reports/daily/personal/{YYYYMM}/YYYY-MM-DD-{name}.md` | positive |
| DR-002 | 生成项目日报 | 写入 `reports/daily/project/{YYYYMM}/` | positive |
| DR-003 | 同人同天第二次提交日报 | 合并追加，不覆盖，追加更新记录 | regression |
| DR-004 | 日报中包含"担心接口延期" | 识别为风险候选，输出在自查清单中 | positive |
| DR-005 | 日报中包含"请假" | 触发资源变动检测，提示更新 resource-register | positive |
| DR-006 | 日报中包含明日计划 | 提取为 TODO，更新 todos index + 生成 snapshot | positive |
| DR-007 | 处理日报后 | 执行 D1-D10 自查清单并输出结果 | regression |
| DR-008 | 日报文件路径 | 使用 `YYYYMM` 单级目录，不使用 `YYYY/MM` | regression |

## 3. Weekly Report（周报生成）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WR-001 | 帮我生成周报 | 先询问输出方式或生成 Markdown 草稿，不直接导出正式文件 | positive |
| WR-002 | 项目集模式下生成周报 | 同时生成子项目周报和项目集汇总周报 | positive |
| WR-003 | 生成周报 Excel | 写入 `outputs/{timestamp}/files/`，不写入 `ai/` | regression |
| WR-004 | 修改刚才的周报 | 复用同一 batch 目录，不新建时间戳 | regression |
| WR-005 | 周报生成后 | 自动生成 `actuals/weekly/` 实际执行摘要 | positive |

## 4. PM Daily Todo（PM 待办）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PT-001 | 我明天的待办 | 输出 9 章节全景视图（PM任务+全团队计划+风险+问题+里程碑+资源变动+本周对照+待协调+无计划项） | regression |
| PT-002 | 全团队明日计划 | 按子项目分组，每个成员列出任务、进度、里程碑、风险标记 | positive |
| PT-003 | 某子项目无计划项 | 明确标注在"无计划项提醒"章节 | positive |

## 5. Output Artifact（输出物管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| OA-001 | 帮我生成周报 | 进入 `outputs/{timestamp}/`，先生成 draft.md | positive |
| OA-002 | 帮我生成 Excel 周报 | 写入 `outputs/{timestamp}/files/`，不写入 `ai/` | regression |
| OA-003 | 修改刚才的周报内容 | 复用同一 batch，追加 `revisions/` | regression |
| OA-004 | 确认后导出 | 生成 final.md，再导出到 `files/` | positive |
| OA-005 | 归档到项目集周报 | 询问确认后写入 `ai/portfolio/reports/weekly/` | positive |
| OA-006 | 生成文件路径 | 使用 `outputs/`，不使用 `ai/` | regression |

## 6. Continuity（历史阶段衔接）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CT-001 | 这是上一阶段 ai 目录 | 进入衔接流程，登记 legacy-sources，不直接覆盖当前 | positive |
| CT-002 | 把一期遗留风险带过来 | 先进入 carryover-register，等待确认 | positive |
| CT-003 | 历史导入 | 不得覆盖当前阶段已有文件 | regression |
| CT-004 | 冲突检测 | 历史事项与当前相似时提示冲突，5种处理选项 | positive |

## 7. Todo Snapshot（计划快照）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| TS-001 | 处理日报后 | 自动生成 `snapshots/daily/{date}.md` + 更新 `history-index.md` | positive |
| TS-002 | 处理日报后 | 自动生成 `actuals/daily/{date}.md` | positive |
| TS-003 | 快照生成后 | 冻结，不静默覆盖，修改追加 Revision Log | regression |
| TS-004 | 计划 vs 实际查询 | 同时读 snapshot + actuals，输出 7 种完成状态 | positive |

## 8. File Rules（文件管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| FR-001 | 日报目录路径 | 使用 `YYYYMM`，不使用 `YYYY/MM` | regression |
| FR-002 | 生成导出文件 | 写入 `outputs/`，不写入 `ai/` | regression |
| FR-003 | AI 管理文件位置 | 统一在 `ai/` 下，不侵入业务目录 | regression |
| FR-004 | 简单查询 | 不得默认创建 JS/Python 临时脚本 | regression |
| FR-005 | 进入工作区 | 先读 `.skill-version.json` 检查版本兼容性 | regression |
| FR-006 | 处理任何输入前 | 先读 `project-brief.md` 判断关联度 | regression |

## 9. Self Check（自查校验）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SC-001 | 处理日报后 | 输出 D1-D10 自查清单 | regression |
| SC-002 | 处理会议纪要后 | 输出 M1-M7 自查清单 | regression |
| SC-003 | 用户追问"有没有漏的" | 重新执行完整自查 + 扩大扫描范围 | positive |
| SC-004 | 风险追溯 | 多源交叉校验（登记册 vs 日报 vs 会议 vs 周报 vs 问题 vs 看板） | positive |

## 10. Versioning（版本管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| VG-001 | 修改目录结构 | 必须提升 workspace schema | regression |
| VG-002 | 修改核心契约 | 必须走 contract_change + 全量回归 | regression |
| VG-003 | 小模板修复 | 只提升 patch 版本 | regression |
| VG-004 | 版本不匹配 | 提示版本差异，不自行迁移 | regression |

## 11. Resource Management（资源管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| RM-001 | 张三被抽调 | 更新 resource-register + 生成 transfer-log | positive |
| RM-002 | 资源状态查询 | 读 resource-register（当前状态），不读 transfer-log | regression |
| RM-003 | 流转历史查询 | 读 transfer-log，不读 resource-register | regression |

## 12. Excel Generation（Excel 生成）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| EG-001 | 生成需求跟踪矩阵 Excel | 14 列精确列头 + 数据验证下拉框 + 冻结首行 | positive |
| EG-002 | 生成风险登记册 Excel | 15 列 + 条件格式（高=红/中=黄/低=绿） | positive |
| EG-003 | 生成成本测算表 | 询问"按角色汇总还是按个人明细" | positive |
| EG-004 | 生成问题跟踪表 | "是否延期"列使用公式 | positive |

## 13. Update Trigger（更新触发）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| UT-001 | "记录一下，陈佳菁被抽调" | 触发更新流程：低/中风险按 proactive 直接写入事实源并标记待确认（登记 pending-changes），高风险先确认后写 | positive |
| UT-002 | 上传评审材料 | 识别文件类型，主动询问是否入库 | positive |
| UT-003 | 日报中包含"决定""确认" | 识别为决策信号，提示更新 decision-log | positive |
| UT-004 | 纯查询"现在有哪些风险" | 不触发更新清单 | regression |

## 14. Skill Governance（变更治理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SG-001 | "帮我优化一下 Skill" | 先输出变更工单草案，标记 contract_change（若涉核心契约），不直接改文件 | regression |
| SG-002 | 用户确认变更工单后 | 执行最小变更 + 跑全量回归测试（contract_change 必须全量） | positive |
| SG-003 | 回归测试失败 | 建议回滚，不叠加临时修复 | regression |
| SG-004 | 修改核心契约 | 标记为 contract_change + 全量回归 | regression |

## 15. Blueprint（架构蓝图与外部审查）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| BP-001 | 外部 AI 只读取 SKILL_BLUEPRINT.md | 能理解 Skill 目标、能力、边界和待补充项 | positive |
| BP-002 | 对比 skill.json.version 与 Blueprint §1 版本 | 版本一致（均为 1.12.0） | positive |
| BP-003 | 对比规则文件清单(00-21)与 Capability Map | 22 个规则文件对应的能力无遗漏 | positive |
| BP-004 | 模拟 Patch 级模板小修 | Blueprint 可不更新正文，CHANGELOG 标注 "Blueprint Impact: none" | positive |
| BP-005 | 模拟 Minor 新增能力 | Blueprint 必须更新 Capability Map 和 Roadmap | positive |
| BP-006 | 对比 SKILL.md 与 Blueprint 正文 | 不存在大段重复的目录树或规则全文 | regression |
| BP-007 | 检查 release-checklist.md | Documentation 章节包含 Blueprint 检查项 | positive |
| BP-008 | 检查 16-skill-governance-rules.md | 包含 §17 Blueprint 更新规则 | positive |
| BP-009 | 检查 skill-contract.md 规则分层表 | 包含文档层分类 | positive |
| BP-010 | 检查 skill.json blueprint 字段 | 包含完整触发条件数组 | positive |

---

## 16. Qoder Adaptation（Qoder 环境适配）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QA-001 | 用户问"skill 版本是多少" | 只读 ai/.skill-version.json，不读 SKILL.md | positive |
| QA-002 | 用户问"我明天的任务" | 只读 todo-index，不读 SKILL.md 和 references/ | positive |
| QA-003 | 简单查询超过 3 个文件 | 先说明原因再继续 | positive |
| QA-004 | 版本查询回答末尾 | 包含"数据来源："标注 | positive |
| QA-005 | 文件修改时间无法获取 | 显示"当前环境未提供，无法确认"，不编造时间 | regression |
| QA-006 | 用户要求修改风险登记册 | 触发安全升级，先加载完整 SKILL.md §7 | regression |
| QA-007 | 复杂任务（日报处理） | 可读多文件但需列出文件清单 | positive |

## 17. Initialization Wizard（初始化向导）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| IW-001 | 用户说"初始化项目" | 启动六步向导，进入 Step 1 合同信息 | positive |
| IW-002 | 新工作区 project-brief status=草稿 | 自动提示"是否开始初始化向导" | positive |
| IW-003 | 向导 Step 3 用户说"跳过" | 标记为待补充，继续 Step 4 | positive |
| IW-004 | 向导中断后再次进入 | 检测到 init_wizard_progress，提示从断点继续 | positive |
| IW-005 | 向导完成后 | 生成初始化确认摘要，用户确认后写入所有文件，brief status 改为"已确认" | positive |

## 18. Information Completeness（信息完整性巡检）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| IC-001 | 用户说"生成周报" | 执行强触发检查，若发现 P0/P1 缺失项则主动提醒 | positive |
| IC-002 | 用户说"查询张三的任务" | 执行弱触发检查，仅检查与张三任务直接相关的字段 | positive |
| IC-003 | 用户说"进入静默模式" | 后续不再主动提醒，P0 级缺失仍必须提示 | regression |
| IC-004 | 用户说"给我做一次完整性巡检" | 输出完整性巡检报告（总体结论+缺失清单+优先补充建议） | positive |
| IC-005 | 用户说"本次不要提醒" | 本次任务跳过完整性检查，下次恢复 | regression |

## 19. Script Contract（脚本契约）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SC-1A | `python init_workspace.py --help` | 参数列表一致（--project-root/--mode/--project-name/--portfolio-name/--sub-projects/--glossary） | regression |
| SC-1B | `--mode portfolio --sub-projects A B C` 在临时目录运行 | 生成 `ai/` 完整目录树，与基线结构一致（忽略当月月份值） | positive |
| SC-1C | `--mode single --project-name X` 在临时目录运行 | 生成单项目 `ai/` 结构与基线一致 | positive |
| SC-1D | 运行生成 `.skill-version.json` | `initializedAt` 为运行当天；月份目录为运行当月 `%Y%m`（非固定值） | positive |
| SC-1E | 重复运行 | 模板防覆盖逻辑仍生效（不覆盖已有文件） | regression |
| SC-1F | portfolio 模式缺参 | 缺 --portfolio-name / --sub-projects 时打印对应错误并 exit(1) | negative |
| SC-1G | `migrate_workspace.py --project-root <tmp> --target-version 1.9.0`（非 dry-run，工作区旧版本 1.0.0） | 读取 `<tmp>/ai/.skill-version.json` 断言 `skillVersion == "1.9.0"`（证明 --target-version 实际写入，而非单一版本源或旧硬编码值） | positive |
| SC-1H | `python -c "from _version import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION"`（sys.path 含 `scripts/`） | 输出 `SKILL_VERSION == 当前发布版本`（如 1.12.0）、`WORKSPACE_SCHEMA_VERSION == "0.6.0"`（单一版本源生效） | positive |
| SC-1I | `init_workspace.py --mode single` 在临时目录运行后读取 `.skill-version.json` | 断言 `skillVersion` 等于单一版本源（如 1.12.0），且与 `_version.SKILL_VERSION` 一致（init 链路端到端） | positive |
| SC-1J | 读取 `migrate_workspace.VERSION_CAPABILITIES` | 断言最大 `version` 字段 == 当前发布版本（如 1.12.0），且包含 1.9.0 条目（能力表补全） | regression |
| SC-1K | 运行既有 SC-1A~1F | 全部通过（脚本 CLI 与行为不回归） | regression |

## 20. SKILL Navigation（SKILL.md 导航与下沉完整性）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SK-1A | 读取 `SKILL.md` | 行数 ≤ 300 | regression |
| SK-1B | 检查 §6 提示词路由表 | 场景条目与修改前一致（一条不删） | regression |
| SK-1C | 检查 §7 安全底线 | 底线条目完整保留 | regression |
| SK-1D | 检查 §8 ID 编码 | 编码体系完整保留 | regression |
| SK-1E | 检查 §15 规则索引 | 00-21 共 22 条 + 版本控制文件完整 | regression |
| SK-1F | 检查下沉落点 | 状态枚举(§5a)/输出规范(§5.4/5.5)/容忍度(§5c)/里程碑(§5b)均存在于 `00-pm-main-rules.md` | positive |
| SK-1G | 模拟"查任务状态" | 通过 §6 路由表能定位到对应 rule（导航可用） | positive |

## 21. File Contract（文件管理契约 v1.8.1）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| FC-1A | 读取 `06-file-rules.md` | 无 §0/§0c 内容；章节编号连续无重复；行数随文件瘦身/RI 目录增长合理（基线 v1.15.0 为 334 行） | positive |
| FC-1B | 读取 `20-workspace-version-rules.md` | 包含版本检查/健康检查/兼容模式/兜底逻辑/升级提醒/触发词/迁移模式全部内容 | positive |
| FC-1C | 读取 `17-domain-glossary-rules.md` 末尾 | 包含 §17 词库文件规范（文件规格/创建边界/拆分规则） | positive |
| FC-1D | 检查 `SKILL.md` §6 路由表 + §5.1b | §6 含 20 号条目；§5.1b 指向 `20-workspace-version-rules.md` 而非 06 | regression |

## 22. Daily Report Rules（日报规则契约 v1.8.2）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DR-1A | 读取 `01-daily-report-rules.md` | 无重复 §2.3 块；章节编号连续无重复；≤300 行 | positive |
| DR-1B | 检查 01 模板引用 | 6 处模板指针均指向 `assets/templates/` 下已存在文件（personal-daily / project-daily / weekly-report / personal-progress / portfolio-weekly / index-formats），无悬空引用 | positive |
| DR-1C | 读取 01 §1.2b 术语归一化 | 仅保留入口要点，指向 `17-domain-glossary-rules.md` §4/§6，未重复完整九步流程 | positive |
| DR-1D | 读取 01 §1.5 资源变动输出 | 候选资源变更与建议更新清单为内联格式（来源/当前状态/一致性判断/建议操作），未引用不存在模板 | regression |

---

## 23. Query/Requirement/Artifact Rules（查询/需求/输出物规则契约 v1.8.3）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QR-1A | 读取 `05-query-rules.md` | 无重复章节编号；问题类型路由表（12 类）与 Quick Query 路由表完整；≤300 行（基线 v1.15.0 为 320 行时已超限，行数断言为软约束：不因无证据的重复堆叠膨胀，语义完整性为准） | positive |
| QR-1B | 读取 `11-output-artifact-rules.md` | ≤300 行；批次目录结构、输出状态机、来源追溯、确认规则语义完整 | positive |
| QR-1C | 读取 `07-requirement-rules.md` | 字段定义与状态机（proposed→confirmed→in_progress→delivered→accepted→changed→cancelled）及验收标准未变；行数随 RI/合同作用域扩展增长（基线 v1.15.0 为 267 行），不以固定行数为硬断言 | positive |
| QR-1D | 模拟一次进度查询 + 一次需求登记 | 查询按 05 §2/§2.5 路由表正确路由读取索引；需求按 07 字段定义与状态机正确登记，规范化后语义完整保留 | regression |

---

## 24. PM Profile（用户偏好学习）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PP-001 | pm-profile.md 存在且有 confirmed 偏好"回复长度=简洁" | AI 输出采用简洁格式 | positive |
| PP-002 | pm-profile.md 不存在 | 跳过偏好加载，按默认格式输出，不报错 | regression |
| PP-003 | 用户说"以后先给结论再分析" | 直接写入 confirmed，本轮生效 | positive |
| PP-004 | 用户连续 3 次未纠正简洁格式 | 写入 pending，末尾输出偏好学习提示 | positive |
| PP-005 | 用户说"确认 PF001" | pending → confirmed，更新 Change Log | positive |
| PP-006 | 用户说"否定 PF001" | pending → rejected，不再自动建议 | positive |
| PP-007 | 用户说"我的偏好" | 输出当前 Profile 全貌（confirmed + pending + rejected） | positive |
| PP-008 | confirmed 偏好"回复长度=简洁" vs project-rules.md 指定"详细格式" | project-rules 优先，输出详细格式 | regression |
| PP-009 | 处理日报时 PM Profile 加载 | confirmed 偏好应用于日报输出格式，pending 不直接应用 | positive |
| PP-010 | pm-profile.md 中 pending 偏好 | pending 不直接改变 AI 输出行为，仅标注候选 | regression |

---

## 25. Historical Plan Import & Change Tracking（R1-R4 历史计划全量同步与变更追溯）

> 对应 CR-20260810-008（v1.10.0）。覆盖需求规格 R1（批量导入）、R2（计划变更追踪）、R3（延期计数）、R4（聚合查询路由）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| HP-001 | 用户上传 .pod/Excel 存量计划要求批量导入 | 走 R1：生成 `snapshots/daily/imported-{date}.md`（source_type=external_import）+ 登记 history-index + 写 board(Source=import) | positive |
| HP-002 | 批量导入前 | 先判定走 R1 还是 13 号（见 `13-continuity-rules.md` §2）；无独立历史工作区才走 R1 | positive |
| HP-003 | 批量导入冻结 | imported-{date}.md 生成后冻结，不静默覆盖，修订追加 Revision Log | regression |
| HP-004 | 导入命名 | 使用 `imported-{date}.md`，不与 AI 前向生成的 `{date}.md` 冲突 | regression |
| HP-005 | 导入登记 | 在 `todo-history-index-template` 外部导入登记追加一行（IMP-*） | positive |
| HP-006 | R1 查询路由 | "导入的那批计划"经 history-index → imported-{date}.md 定位，source_type=external_import | positive |
| HP-007 | board 计数首版 | 导入任务 Plan Change Count / Delay Count 记 0 | positive |
| HP-008 | 计划变更追踪 | 单任务 Due Date/Owner 调整 → board 递增 Plan Change Count，Delay 仅 Due Date 后移时 +1 | positive |
| HP-009 | 概念域 | change-log 用概念域 B（plan_change）；board Change Log 用概念域 A，不混用 | regression |
| HP-010 | 延期统计查询（A 类） | "延期了几次"只读 board.md 单文件，不扫描快照/日报；输出 delay-stats | positive |
| HP-011 | board 缺计数字段 | 回退 Change Log 统计并标注"推断，未确认" | regression |
| HP-012 | 超期查询（B 类） | "现在哪些任务超期"实时计算，读 board + 预建索引，不扫日报原文 | positive |
| HP-013 | 确认窗口期判定 | v2 未确认按旧 Due Date 判延期；已确认按新 Due Date | positive |
| HP-014 | 负责人变更归属 | 交接前超期归原 Owner，交接后归新 Owner | positive |
| HP-015 | 超期触发时机 | 处理日报时 + PM 查询进度时都实时计算 | regression |
| HP-016 | 索引过期警告 | 索引超 24h 未更新时给出过期警告 | positive |
| HP-017 | source_type 统一 | snapshot source_type 取 personal_daily_reports/pm_todo/meeting/external_import 四值之一 | regression |

---

## 26. Pending Window（待确认窗口期 · 主动变更+人工确认）

> 对应 CR-20260811-002（v1.11.0）。覆盖事实源直接写入+待确认标记、pending-changes 登记、确认/驳回回滚、Due Date 空窗期判定。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PW-001 | 低风险事实源更新（如新增任务行） | 直接写入事实源并标记 `Confirmed By: 待确认`，同时登记 `pending-changes.md`，末尾提示待人工确认 | positive |
| PW-002 | 待确认记录 | 在到期判定、已完成统计中一律视为未确认（不参与延期/超期计数） | positive |
| PW-003 | 用户确认"确认 PW001" | pending → confirmed，从 pending-changes 移除（Change Log 保留），标记生效 | positive |
| PW-004 | 用户驳回"驳回 PW001" | 恢复变更前原值，pending-changes 标记 rejected，不留错误事实 | regression |
| PW-005 | 待确认记录超 7/14 天未确认 | 触发催办升级提示，不静默丢弃 | regression |
| PW-006 | 高风险变更（如删任务/改里程碑基线） | 必须先确认后写，不适用主动写入待确认模式 | regression |

---

## 27. Change Log Archive（变更日志分层归档）

> 对应 CR-20260811-002（v1.11.0）。覆盖活跃区 50 行/30 天触发、月度归档文件、月份导航索引。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CLA-001 | 活跃区 Change Log 达 50 行 | 触发按月归档至 `change-log/archive/YYYYMM-change-log.md` | positive |
| CLA-002 | 活跃区最旧记录超 30 天 | 触发归档，更新 `change-log/index.md` 月份导航 | positive |
| CLA-003 | 查询历史变更 | 经 `change-log/index.md` 定位到对应归档月份文件，不扫活跃区 | regression |

---

## 28. Workspace Cleanliness（工作空间清洁度）

> 对应 CR-20260811-003（v1.12.0）。覆盖根目录白名单合规、幽灵引用扫描、版本号一致性、构建缓存清理。规则来源：`references/16-skill-governance-rules.md` §18/§19/§20。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CL-001 | 扫描根目录所有文件和目录 | 仅包含白名单（§18）内的条目，无非标准文件 | positive |
| CL-002 | 扫描 CR/IA/RR/基线 README/CHANGELOG 中的文件引用 | 所有被引用的文件路径必须实际存在，无幽灵引用 | positive |
| CL-003 | 检查 SKILL.md 版本控制表中的版本号 | 与 VERSION 文件一致，无陈旧版本号 | regression |
| CL-004 | 扫描 scripts/ 目录 | 无 `__pycache__/` 等构建缓存残留 | positive |

---

## 29. Cascade Propagation（级联传播）

> 对应 CR-20260812-001（v1.13.0）。覆盖 6 个实体规则文件新增的 `§级联传播规则`（03 §8、04 §9、07 §7、08 §9、09 §8、02 §6）、00 号 §8 级联冲突处理、AUTO 作用域限定（写派生视图）、14 号 §2.4 索引派生分级与 D13/M8/R7 级联完整性自查项。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CP-001 | Task→done + Risk Ref | CHECK 验证风险存在；AUTO 更新 todo 索引 | positive |
| CP-002 | Risk→converted_to_issue | SUGGEST 新增 issue + AUTO 更新索引 | positive |
| CP-003 | Issue→resolved + blocked task | SUGGEST 恢复 task | positive |
| CP-004 | Resource→offboard | SUGGEST 重分配 + AUTO 更新 todo | positive |
| CP-005 | 多 SUGGEST 指向同一目标 | 合并为同一批建议清单 | positive |
| CP-006 | 级联冲突场景 | 标记 ⚠ 级联异常，交 PM 决策 | negative |

## 30. Archive Governance（归档治理）

> 对应 CR-20260812-001（v1.13.0）。覆盖 B 线文件膨胀治理的归档触发规则：02 号 decision-log 归档、09 号 transfer-log 归档、15 号快照存储生命周期、11 号 outputs 存储生命周期、01 号 §5.8 通用归档检查、06 号 §9 通用归档表。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| AG-001 | decision-log >30 条 | 触发按季度归档 | positive |
| AG-002 | transfer-log >100 条 | 触发按年度归档 | positive |
| AG-003 | 快照文件 >90 天 | 移动到 archive/YYYY/ | positive |
| AG-004 | outputs/index.md >100 行 | 触发已确认批次归档 | positive |
| AG-005 | 日报处理末尾 §5.8 通用归档检查 | 扫描所有有归档规则实体 | positive |
| AG-006 | 06 号 §9 通用归档表完整性 | 8 行实体 × 触发条件 × 归档目标 × 索引 | positive |


## 31. Workflow Data Path（标准工作流数据路径）

> 对应 v1.14.0（CR-20260812-001 续）。覆盖 00 号 §9 WF-1~WF-6 标准工作流数据路径与 05 号 §2.5 Quick Update 路由表。重点验证：路径预定义不弱化判断阶段（§9.1 五条强化规则）、写入仍遵循 SKILL.md §7 底线 #2（pending-changes 登记）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WF-001 | "更新于文聪的待办" + 事实依据 | 按 WF-1 步骤 1-18 执行：定位(读 todo-index/board/issue/risk)→判断(待办匹配/状态判定/问题关闭/风险关闭)→写入(含 pending-changes 登记)→补全(日报索引)→输出变更摘要 | positive |
| WF-002 | WF-1 步骤 6 待办匹配：用户用别名/缩写描述 | §9.1 规则1 生效：语义匹配考虑别名缩写，不因路径预定义简化判断 | positive |
| WF-003 | WF-1 步骤 8/9 关联问题/风险仅"部分缓解" | §9.1 规则3/4 生效：不自动关闭，列入建议清单待 PM 确认 | regression |
| WF-004 | WF-1 步骤 16：单纯状态更新指令（无工作进展描述） | §9.1 规则5 生效：不触发 PF006 日报补全，仅更新待办状态 | regression |
| WF-005 | 05 号 Quick Update 路由表 6 条场景 | 每条场景指向正确 WF 编号，且写入动作含 SKILL.md §7 底线 #2 引用（不绕过确认） | positive |


## 32. Requirement Intelligence（需求情报 RI）

> 对应 CR-20260813-001（v1.15.0）。覆盖跨源需求拆词、归并、范围判定与三级索引检索（requirements/atoms + canonical + source-type-registry）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| RI-001 | 合同条款文本 | 拆分为 ATOM，含 source_type/authority/raw_text/norm_text | positive |
| RI-002 | 合同+招标对同一需求的不同表述 | 归并到同一 Canonical，evidence 含 2 个来源 | positive |
| RI-003 | 查"XX 在不在合同范围内" | 返回 scope + 证据链，本次加载 ≤400 行 | positive |
| RI-004 | 未登记 source_type 的需求 | 触发未登记提示，不静默归类 | negative |
| RI-005 | 合同出新版本 | 相关 ATOM 标记 stale、Canonical evidence_stale | regression |
| RI-006 | 查"身份认证" | 命中"用户登录"ATOM（词库同义词扩展） | regression |
| RI-007 | 合同条款 raw_text > 500 字 | 拆分为多个 ATOM，supersedes 链指向首条 | negative |
| RI-008 | 合同(L1)与技术文档(L3)对同一需求表述冲突 | Canonical 取 L1 authority，evidence 保留两来源 | regression |
| RI-009 | L2 类别索引 norm_text 摘要 | AI 仅读 L2 即可理解 ATOM 语义，无需加载 L3 全文 | positive |
| RI-010 | 关键词匹配失败 | P1 语义兜底：norm_text 扫读 → 降级提示，不返回空 | regression |
| RI-011 | source-type-registry 新增类型后迁移 | 5 步原子操作（更新 registry → 重写 ATOM → 刷新索引 → 迁移文件 → 失败回退） | regression |
| RI-012 | Canonical scope_scope 变更 | 级联传播至所有关联 REQ 的 scope_scope 字段 | regression |

## 33. Project Notes（项目备忘）

> 对应 CR-20260813-001（v1.15.0）。覆盖项目经验备忘的追加与 AI 检测候选备忘。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PN-001 | PM 说"记一下这个经验" | 追加 project-notes 条目 | positive |
| PN-002 | AI 检测到方法论/干系人信号 | 输出候选备忘建议，PM 确认后写入 | positive |


## 34. Contract Scope（合同作用域 RI）

> 对应 CR-20260813-002（v1.16.0）。覆盖合同与子项目多对多映射、contract-register 合同登记册、scope_level 归属（supplement 跟随父合同）、四步检索路由、合同变更联动与 0.8.0 迁移。设计决策见 governance/planning/contract-scope-ri-scheme.md（D1-D10）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CS-001 | 项目集 + CON-001(portfolio，覆盖 PRJ-001+PRJ-002) | contract-register 登记成功；ATOM/Canonical 存 portfolio/requirements | positive |
| CS-002 | 问"X 在不在合同1 范围"（portfolio 合同） | 路由 portfolio 级 canonical；返回 scope_scope=in_contract + contract_refs={CON-001} + 证据链 | positive |
| CS-003 | 项目集 3 合同，未指定合同 | 列合同候选→选择/全检索→按合同标注各 scope 结论 | positive |
| CS-004 | 场景 G：子项目 A 被 CON-001+CON-002 覆盖（不同建设内容） | 逐合同列结论（in_contract(CON-001)+in_contract(CON-002)），contract_refs 显式双 ID，不混淆 | regression |
| CS-005 | 单项目 2 合同分期（场景 H） | requirements/contract-register 区分 CON-001/CON-002；路由正确（不引入 portfolio） | positive |
| CS-006 | Canonical evidence 跨 portfolio+子项目 | 归 portfolio 级，storage_level=portfolio，contract_refs 含双合同 | positive |
| CS-007 | 已有工作区升级后 contract-register 为空 | RI 查询触发补录引导（最小字段），不返回错误结论 | negative |
| CS-008 | 补充协议扩大范围 | 新增 ATOM(supplement)→归并→scope 重判→索引刷新（supplement 归父合同层级） | regression |
| CS-009 | 合同拆分（CON-001 → CON-001a/CON-001b） | 旧条 status=superseded、superseded_by=新条；ATOM 归属迁移；Canonical 重判 | regression |
| CS-010 | 子项目 A 的 CON-002 + 子项目 B 的 CON-003 对同一需求有证据 | Canonical 归 portfolio，storage_level=portfolio | regression |
| CS-011 | RI-012 复核：Canonical scope_scope 变更 + contract_refs | contract_refs 随 Canonical 变更同步更新 | regression |
| CS-012 | 0.8.0 迁移后 portfolio/requirements 骨架完整 | canonical/atoms/contract-register/source-type-registry 齐全且格式正确 | positive |
| CS-013 | 项目集 0.7.0→0.8.0 迁移（CR-001 遗留修复） | 子项目级 requirements/canonical+atoms+source-type-registry 自动补齐 | positive |
| CS-014 | PM 说"新签了一份合同" | 触发合同登记意图→补入 contract-register→路由可查 | positive |
| CS-015 | supplement of portfolio 级父合同（CON-002 补充 CON-001） | parent_contract_id 回溯→portfolio 级 canonical→in_contract 含双 ID | positive |
| CS-016 | 0.8.0 迁移 sub_project_dirs/files 遍历 | 各 projects/*/requirements/{canonical,atoms}+source-type-registry 补齐；无 requirements/ 的子项目不强建（D10） | positive |
| CS-017 | 合同范围缩小变更 | 走 08 号 scope 类型（不新增枚举）；superseded 血缘更新 | regression |

## 35. PM Preference Generalization（PM 偏好通用化能力）

> 对应 v1.17.0。覆盖五个能力模块：(A) 日报集成审查（01 号 §6）+ 主动提问（01 号 §7）；(B) 跨实体联动同步（01 号 §5.3 + 03 号 §8 + 00 号 WF-1 步骤 4.5）；(C) 关闭确认佐证（04 号 §9.1）；(D) 委派跟踪级联（03 号 §8 + WF-1 步骤 18.6）；(E) 沟通质量规则（00 号 §5.1a CQ-4/CQ-5）+ 可选查询默认过滤（05 号 §2.0a）。沟通风格类偏好（CQ-1/2/3）留在 PM Profile 层，不属于本模块验证范围。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| IR-001 | 提交日报并要求处理 | 日报写入后触发 01 号 §6 集成审查：计划 vs 完成、风险/问题变化、任务进度偏差三维度对比表输出 | positive |
| IR-002 | 集成审查发现任务延期 + 新增风险 | 01 号 §7 主动提问生效：从阻塞解除/风险应对/关键任务遗漏/明日计划可行性四角度至少提出针对性问题 | positive |
| IR-003 | 日报与计划完全一致（无偏差） | 集成审查仍执行但输出简明“无偏差”结论，不省略审查步骤也不虚构偏差 | regression |
| IR-004 | 日报进展描述与关联 Requirement 状态矛盾（如日报称已完成但 REQ 仍 in_progress） | 01 号 §5.3 联动表生效：SUGGEST 同步需求登记册状态，不静默修改 | positive |
| IR-005 | Task 状态变更为 done（关联需求仍 open） | 03 号 §8 生效：[CHECK] 验证关联需求状态一致性 + [SUGGEST] 不一致时建议同步；WF-1 步骤 4.5 需求检查不跳过 | positive |
| IR-006 | Task Owner 从张三改为李四（委派） | 03 号 §8 委派级联生效：[CHECK] 被委派方身份 + [SUGGEST] 为委派方生成跟进待办；WF-1 步骤 18.6 引导不遗漏 | regression |
| IR-007 | 要求关闭某风险/问题 | 04 号 §9.1 生效：关闭建议显式列明候选编号 + 佐证 + 关联影响三要素 | positive |
| IR-008 | 要求关闭风险但未提供任何佐证 | 04 号 §9.1 禁止规则生效：不输出无佐证关闭建议，改为提示补充佐证 | regression |
| IR-009 | 处理类任务输出含多个待确认事项 | CQ-4 生效：待确认事项编号罗列；CQ-5 生效：查询结论基于本轮实读文件，不引用缓存/记忆数据 | positive |
| IR-010 | 查询“我的待办”（未说明范围） | 05 号 §2.0a 生效：默认仅输出未完成项；用户明确说“全部”时输出含已完成项 | regression |


## 回归用例统计

| 模块 | 用例数 | 正向 | 回归 |
|---|---|---|---|
| Quick Query | 11 | 8 | 3 |
| Daily Report | 8 | 5 | 3 |
| Weekly Report | 5 | 3 | 2 |
| PM Daily Todo | 3 | 2 | 1 |
| Output Artifact | 6 | 3 | 3 |
| Continuity | 4 | 3 | 1 |
| Todo Snapshot | 4 | 3 | 1 |
| File Rules | 6 | 0 | 6 |
| Self Check | 4 | 3 | 1 |
| Versioning | 4 | 0 | 4 |
| Resource Management | 3 | 1 | 2 |
| Excel Generation | 4 | 4 | 0 |
| Update Trigger | 4 | 3 | 1 |
| Skill Governance | 4 | 1 | 3 |
| Blueprint | 10 | 8 | 2 |
| Qoder Adaptation | 7 | 5 | 2 |
| Initialization Wizard | 5 | 4 | 1 |
| Information Completeness | 5 | 3 | 2 |
| Script Contract | 11 | 6 | 5 |
| SKILL Navigation | 7 | 2 | 5 |
| File Contract | 4 | 3 | 1 |
| Daily Report Rules | 4 | 3 | 1 |
| Query/Requirement/Artifact Rules | 4 | 3 | 1 |
| PM Profile | 10 | 7 | 3 |
| Historical Plan Import & Change Tracking | 17 | 11 | 6 |
| Pending Window (PW) | 6 | 3 | 3 |
| Change Log Archive (CLA) | 3 | 2 | 1 |
| Workspace Cleanliness (CL) | 4 | 3 | 1 |
| Cascade Propagation (CP) | 6 | 6 | 0 |
| Archive Governance (AG) | 6 | 6 | 0 |
| Workflow Data Path (WF) | 5 | 3 | 2 |
| Requirement Intelligence (RI) | 12 | 4 | 8 |
| Project Notes (PN) | 2 | 2 | 0 |
| Contract Scope (CS) | 17 | 10 | 7 |
| PM Preference Generalization (IR) | 10 | 6 | 4 |
| **合计** | **225** | **142** | **83** |
