# Regression Suite

> 本文件是 ChronoPM Skill 的总回归测试清单。每次变更必须声明至少跑哪些用例。

---

## 1. Quick Query（快速查询）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QQ-001 | 我明天的待办是什么 | 优先读 PM 当日待办文件 `todos/{date}/{PM姓名}.md` + 绑定文件 `_index.md`，输出 9 章节全景视图，不得只列 PM 个人任务 | positive |
| QQ-002 | 明天大家做什么 | 优先读绑定文件 `todos/{date}/_index.md` → 各人待办文件 | positive |
| QQ-003 | 本周重点是什么 | 优先读 `todos/{date}/` 待办文件（按本周 Due Date 过滤） | positive |
| QQ-004 | 张三现在在做什么 | 优先读张三近期待办文件 `projects/*/todos/{date}/张三.md` | positive |
| QQ-005 | 当前有哪些风险 | 优先读 `risks/risk-register.md`（open），不扫描历史周报 | positive |
| QQ-006 | 8月10日大家原计划做什么 | 优先读 `snapshots/daily/{date}.md`（导入计划为 `imported-{date}.md`） | positive |
| QQ-007 | 8月10日计划完成了吗 | 读快照/实际摘要（若有）+ 当日待办文件，输出对比表 | positive |
| QQ-008 | 上周计划偏差 | 读 `snapshots/weekly/` + `actuals/weekly/`（若有）+ 上周待办文件 | positive |
| QQ-009 | 项目进展如何 | 优先读 `todos/{date}/` 待办文件 + PLAN 文件，不扫描所有过程记录 | positive |
| QQ-010 | 简单查询（明天待办） | 不得创建临时 JS/Python 脚本扫描目录 | regression |
| QQ-011 | 待办目录/绑定文件不存在时 | 提示工作区可能未升级（见 20 号），不自行全量扫描 | regression |

## 2. Daily Report（日报处理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DR-001 | 处理今天个人工作汇报 | 写入该成员当日待办文件 `todos/{date}/{姓名}.md` 工作日志段（不再创建独立个人日报文件） | positive |
| DR-002 | 生成项目日报 | 写入 `reports/daily/project/{YYYYMM}/` | positive |
| DR-003 | 同人同天第二次提交汇报 | 合并追加到同一待办文件工作日志段，不覆盖，追加合并记录 | regression |
| DR-004 | 汇报中包含"担心接口延期" | 识别为风险候选，输出在自查清单中 | positive |
| DR-005 | 汇报中包含"请假" | 触发资源变动检测，提示更新花名册（`_index` §1）/ 待办 §0.5，不写 resource-register | positive |
| DR-006 | 汇报中包含明日计划 | 只写入当天日报原文；不建未来日目录；不在当日落成待办行 | positive |
| DR-007 | 处理日报后 | 执行 D1-D16 自查清单并输出结果 | regression |
| DR-008 | 日报文件路径 | 使用 `YYYYMM` 单级目录，不使用 `YYYY/MM` | regression |

## 3. Weekly Report（周报生成）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WR-001 | 帮我生成周报 | 先询问输出方式或生成 Markdown 草稿，不直接导出正式文件 | positive |
| WR-002 | 项目集模式下生成周报 | 引导切 ChronoPM-Portfolio；本包只出本项目周报 | positive |
| WR-003 | 生成周报 Excel | 写入 `ai/outputs/{timestamp}/files/`，不直写 `ai/` 事实源目录（v2.1.0） | regression |
| WR-004 | 修改刚才的周报 | 复用同一 batch 目录，不新建时间戳 | regression |
| WR-005 | 周报生成后 | 按自然周从 todos 整段汇聚；已完结周成存根；不每日累积草稿 | positive |

## 4. PM Daily Todo（PM 待办）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PT-001 | 我明天的待办 | 输出 9 章节全景视图（PM任务+全团队计划+风险+问题+里程碑+资源变动+本周对照+待协调+无计划项） | regression |
| PT-002 | 全团队明日计划 | 按子项目分组，每个成员列出任务、进度、里程碑、风险标记 | positive |
| PT-003 | 某子项目无计划项 | 明确标注在"无计划项提醒"章节 | positive |

## 5. Output Artifact（输出物管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| OA-001 | 帮我生成周报 | 进入 `ai/outputs/{timestamp}/`，先生成 draft.md（v2.1.0） | positive |
| OA-002 | 帮我生成 Excel 周报 | 写入 `ai/outputs/{timestamp}/files/`，不直写 `ai/` 事实源目录（v2.1.0） | regression |
| OA-003 | 修改刚才的周报内容 | 复用同一 batch，追加 `revisions/` | regression |
| OA-004 | 确认后导出 | 生成 final.md，再导出到 `files/` | positive |
| OA-005 | 归档到项目集周报 | 引导切 ChronoPM-Portfolio 对话，本包不写 `portfolio/` | regression |
| OA-006 | 生成文件路径 | 使用 `ai/outputs/`，生成物不直写 `ai/` 事实源目录（v2.1.0） | regression |

## 6. Continuity（历史阶段衔接）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CT-001 | 这是上一阶段 ai 目录 | 进入衔接流程，登记 legacy-sources，不直接覆盖当前 | positive |
| CT-002 | 把一期遗留风险带过来 | 先进入 delta-analysis.md 结转候选段，等待确认 | positive |
| CT-003 | 历史导入 | 不得覆盖当前阶段已有文件 | regression |
| CT-004 | 冲突检测 | 历史事项与当前相似时提示冲突，5种处理选项 | positive |

## 7. Todo Snapshot（历史导入快照与历史回查）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| TS-001 | 处理日报后 | v2.0.0 起不再生成前向快照；待办文件本身即历史（待办文件+工作日志段可回查当日计划与执行） | regression |
| TS-002 | 查询某日实际做了什么 | 优先读当日待办文件工作日志段；旧日期有 actuals 时读 `actuals/daily/` | positive |
| TS-003 | 导入快照生成后 | 冻结，不静默覆盖，修改追加 Revision Log | regression |
| TS-004 | 计划 vs 实际查询 | 读快照（若有）+ 待办文件/实际摘要，输出对比 | positive |

## 8. File Rules（文件管理）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| FR-001 | 日报目录路径 | 使用 `YYYYMM`，不使用 `YYYY/MM` | regression |
| FR-002 | 生成导出文件 | 写入 `ai/outputs/`，不直写 `ai/` 事实源目录（v2.1.0） | regression |
| FR-003 | AI 管理文件位置 | 统一在 `ai/` 下，不侵入业务目录 | regression |
| FR-004 | 简单查询 | 不得默认创建 JS/Python 临时脚本 | regression |
| FR-005 | 进入工作区 | 先读 `.skill-version.json` 检查版本兼容性 | regression |
| FR-006 | 处理任何输入前 | 先读 `project-brief.md` 判断关联度 | regression |

## 9. Self Check（自查校验）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SC-001 | 处理日报后 | 输出 D1-D16 自查清单 | regression |
| SC-002 | 处理会议纪要后 | 输出 M1-M7 自查清单 | regression |
| SC-003 | 用户追问"有没有漏的" | 重新执行完整自查 + 扩大扫描范围 | positive |
| SC-004 | 风险追溯 | 多源交叉校验（登记册 vs 日报 vs 会议 vs 周报 vs 问题 vs 待办文件） | positive |

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
| RM-001 | 张三被抽调 | 更新 `_index` §1 花名册状态 + 有待办者追加 §0.5；不写 resource-register / transfer-log | positive |
| RM-002 | 资源状态查询 | 读 `_index` §1 花名册（当前状态），不扫历史日 §0.5 | regression |
| RM-003 | 流转历史查询 | 读该人待办 §0.5，不把花名册当流水 | regression |

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
| UT-001 | "记录一下，陈佳菁被抽调" | 触发更新流程：低/中风险按 proactive 直接写入事实源，`Confirmed By: auto`，不进块 8 子节「已经写了等点头」；高风险先确认后写 | positive |
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

## 16. Qoder Adaptation（轻量查询；v3.12.0 起入口为 05 全局最小读取，无宿主专用文件）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QA-001 | 用户问"skill 版本是多少" | 只读 ai/.skill-version.json，不读 SKILL.md | positive |
| QA-002 | 用户问"我明天的任务" | 只读待办文件 + 绑定文件 `_index.md`，不读 SKILL.md 和 references/ | positive |
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
| SK-1B | 检查 §6 提示词路由表 | 不得删除安全/写入场景；允许把「本项目查询」拆成简单查询+复杂查询 | regression |
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
| DR-1B | 检查 01 模板引用 | 模板指针均指向 `assets/templates/` 下已存在文件（personal-daily-todo / project-daily / weekly-report / daily-todo-binding / portfolio-weekly / index-formats），无悬空引用；不再引用已删除的 personal-daily/personal-progress 模板 | positive |
| DR-1C | 读取 01 §1.2b 术语归一化 | 仅保留入口要点，指向 `17-domain-glossary-rules.md` §4/§6，未重复完整九步流程 | positive |
| DR-1D | 读取 01 §1.5 资源变动输出 | 候选资源变更与建议更新清单为内联格式（来源/当前状态/一致性判断/建议操作），未引用不存在模板 | regression |

---

## 23. Query/Requirement/Artifact Rules（查询/需求/输出物规则契约 v1.8.3）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QR-1A | 读取 `05-query-rules.md` | 无重复章节编号；问题类型路由表（12 类）与 Quick Query 路由表完整；≤300 行（基线 v1.15.0 为 320 行时已超限，行数断言为软约束：不因无证据的重复堆叠膨胀，语义完整性为准） | positive |
| QR-1B | 读取 `11-output-artifact-rules.md` | ≤300 行；批次目录结构、输出状态机、来源追溯、确认规则语义完整 | positive |
| QR-1C | 读取 `07-requirement-rules.md` | 字段定义与状态机（已提议→已确认→进行中→已交付→已验收，可已变更/已取消，v2.0.0 中文枚举）及验收标准语义未变；行数随 RI/合同作用域扩展增长（基线 v1.15.0 为 267 行），不以固定行数为硬断言 | positive |
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
| HP-001 | 用户上传 .pod/Excel 存量计划要求批量导入 | 走 R1：生成 `snapshots/daily/imported-{date}.md`（source_type=external_import）+ 写入待办文件 `todos/{date}/{owner}.md`（来源=import）+ 在 `context/import-log.md` 登记导入批次 | positive |
| HP-002 | 批量导入前 | 先判定走 R1 还是 13 号（见 `13-continuity-rules.md` §2）；无独立历史工作区才走 R1 | positive |
| HP-003 | 批量导入冻结 | imported-{date}.md 生成后冻结，不静默覆盖，修订追加 Revision Log | regression |
| HP-004 | 导入命名 | 使用 `imported-{date}.md`，不与 AI 前向生成的 `{date}.md` 冲突 | regression |
| HP-005 | 导入登记 | 在 `context/import-log.md` 登记导入批次（IMP-YYYYMMDD-NNN） | positive |
| HP-006 | R1 查询路由 | "导入的那批计划"直接定位 `snapshots/daily/imported-{date}.md`，source_type=external_import | positive |
| HP-007 | 待办文件计数首版 | 导入任务计划变更次数/延期次数记 0 | positive |
| HP-008 | 计划变更追踪 | 单任务 Due Date/Owner 调整 → 待办文件递增计划变更次数，延期次数仅 Due Date 后移时 +1 | positive |
| HP-009 | 概念域 | change-log 用概念域 B（plan_change）；待办文件变更段用概念域 A，不混用 | regression |
| HP-010 | 延期统计查询（A 类） | "延期了几次"只聚合待办文件延期次数字段，不扫描快照/日报；输出聚合结果 | positive |
| HP-011 | 待办文件缺延期次数字段 | 回退变更段统计并标注"推断，未确认" | regression |
| HP-012 | 超期查询（B 类） | "现在哪些任务超期"实时计算，读待办文件 + 绑定文件，不扫日报原文 | positive |
| HP-013 | 确认窗口期判定 | v2 未确认按旧 Due Date 判延期；已确认按新 Due Date | positive |
| HP-014 | 负责人变更归属 | 交接前超期归原 Owner，交接后归新 Owner | positive |
| HP-015 | 超期触发时机 | 处理日报时 + PM 查询进度时都实时计算 | regression |
| HP-016 | 绑定文件过期警告 | 绑定文件 `_index.md` 超 24h 未更新时给出过期警告 | positive |
| HP-017 | source_type 统一 | v2.0.0 起前向快照已取消，快照 source_type 仅保留 external_import（历史计划批量导入） | regression |

---

## 26. Pending Window（待确认窗口期 · 主动变更+人工确认）

> 对应 CR-20260811-002（v1.11.0）。覆盖事实源直接写入+待确认标记、pm-decisions.md 块 8 登记、确认/驳回回滚、Due Date 空窗期判定。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PW-001 | 低风险事实源更新（如新增任务行） | 直接写入事实源并标记 `Confirmed By: auto`，**不**登记块 8 子节「已经写了等点头」，回合末一句话告知 | positive |
| PW-002 | `Confirmed By: 待确认` 记录 | 在到期判定、已完成统计中一律视为未确认（不参与延期/超期计数）。`auto` 计入 | positive |
| PW-003 | 用户确认"确认 PW001" | pending → confirmed，从 pm-decisions.md 块 8 移除（Change Log 保留），标记生效 | positive |
| PW-004 | 用户驳回"驳回 PW001" | 恢复变更前原值，pm-decisions.md 块 8 标记 rejected 并记入决策记录，不留错误事实 | regression |
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

> 对应 CR-20260812-001（v1.13.0）。覆盖实体规则文件的 `§级联传播规则`（04 §9、07 §7、08 §9、09 §8、02 §6；v2.0.0 起 03 号已删，任务层级联规则迁入 00 号 WF）、00 号 §8 级联冲突处理、AUTO 作用域限定（写派生视图）、14 号 §2.4 索引派生分级与 D13/M8/R7 级联完整性自查项。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CP-001 | 待办→已完成 + Risk Ref | CHECK 验证风险存在；AUTO 更新待办文件/绑定文件 | positive |
| CP-002 | Risk→转为问题 | SUGGEST 新增 issue + AUTO 更新绑定文件 | positive |
| CP-003 | Issue→已解决 + 已阻塞待办 | SUGGEST 恢复待办为进行中 | positive |
| CP-004 | Resource→已离场 | SUGGEST 重分配 + AUTO 更新待办 | positive |
| CP-005 | 多 SUGGEST 指向同一目标 | 合并为同一批建议清单 | positive |
| CP-006 | 级联冲突场景 | 标记 ⚠ 级联异常，交 PM 决策 | negative |

## 30. Archive Governance（归档治理）

> 对应 CR-20260812-001（v1.13.0），v3.8.0 同步：人员 transfer-log / resource 归档行已从 06 §9 删除。覆盖 decision-log 归档、快照/outputs 生命周期、01 号 §5.8 通用归档检查、06 号 §9 通用归档表。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| AG-001 | decision-log >30 条 | 触发按季度归档 | positive |
| AG-002 | 退役 transfer-log / resource-register 存量 | 不按年度归档；分类器建议搬 `backup/`（PM 确认后）；人员流转读 §0.5 | positive |
| AG-003 | 快照文件 >90 天 | 移动到 archive/YYYY/ | positive |
| AG-004 | ai/outputs/index.md >100 行 | 触发已确认批次归档（v2.1.0） | positive |
| AG-005 | 日报处理末尾 §5.8 通用归档检查 | 扫描所有有归档规则实体 | positive |
| AG-006 | 06 号 §9 通用归档表完整性 | 5 行实体（issue/risk/decision/snapshot-actuals/outputs，已删 resource 与 transfer-log）× 触发条件 × 归档目标 × 索引；另 + change-log 月归档索引受控可读 | positive |


## 31. Workflow Data Path（标准工作流数据路径）

> 对应 v1.14.0（CR-20260812-001 续）。覆盖 00 号 §9 WF-1~WF-6 标准工作流数据路径与 05 号 §2.5 Quick Update 路由表。重点验证：路径预定义不弱化判断阶段（§9.1 五条强化规则）、写入仍遵循 SKILL.md §7 底线 #2（pm-decisions.md 块 8 登记）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WF-001 | "更新于文聪的待办" + 事实依据 | 按 WF-1 步骤 1-18 执行：定位(读绑定文件/待办文件/issue/risk)→判断(待办匹配/状态判定/问题关闭/风险关闭)→写入(含 pm-decisions.md 块 8 登记)→补全(日报索引)→输出变更摘要 | positive |
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

> 对应 v1.17.0，v3.0.0 修订：(D) 委派跟进条已删除（IR-006 改反向）；查询默认过滤并入 §39 / 05 号新节。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| IR-001 | 提交日报并要求处理 | 日报写入后触发 01 号 §6 集成审查：计划 vs 完成、风险/问题变化、任务进度偏差三维度对比表输出 | positive |
| IR-002 | 集成审查发现任务延期 + 新增风险 | 01 号 §7 主动提问生效：从阻塞解除/风险应对/关键任务遗漏/明日计划可行性四角度至少提出针对性问题 | positive |
| IR-003 | 日报与计划完全一致（无偏差） | 集成审查仍执行但输出简明“无偏差”结论，不省略审查步骤也不虚构偏差 | regression |
| IR-004 | 日报进展描述与关联 Requirement 状态矛盾（如日报称已完成但 REQ 仍进行中） | 01 号 §5.3 联动表生效：SUGGEST 同步需求登记册状态，不静默修改 | positive |
| IR-005 | 待办状态变更为已完成（关联需求仍开放） | 00 号 WF 级联生效：[CHECK] 验证关联需求状态一致性 + [SUGGEST] 不一致时建议同步；WF-1 步骤 4.5 需求检查不跳过 | positive |
| IR-006 | Task Owner 从张三改为李四（委派） | **v3.0.0 反向**：不得为委派方/PM 自动生成跟进待办；可 CHECK 被委派方身份（WF-1 已删除步骤 18.6） | regression |
| IR-007 | 要求关闭某风险/问题 | 04 号 §9.1 生效：关闭建议显式列明候选编号 + 佐证 + 关联影响三要素 | positive |
| IR-008 | 要求关闭风险但未提供任何佐证 | 04 号 §9.1 禁止规则生效：不输出无佐证关闭建议，改为提示补充佐证 | regression |
| IR-009 | 处理类任务输出含多个待确认事项 | CQ-4 生效：待确认事项编号罗列；CQ-5 生效：查询结论基于本轮实读文件，不引用缓存/记忆数据 | positive |
| IR-010 | 查询“我的待办”（未说明范围） | 05 号 §2.0a 生效：默认仅输出未完成项；用户明确说“全部”时输出含已完成项 | regression |


## 36. Backward Scheduling & Unified Intake（倒排计划与统一归属路由）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| BS-001 | 用户说"根据 8/28 做倒排计划" | AI 识别为倒排意图（00号 §2.7），进入 WF-7，不误判为普通任务记录 | positive |
| BS-002 | 倒排流程执行 | 澄清目标/截止日/资源 → 查重 → 反向 WBS + 关键路径 + 缓冲 → 输出草案待 PM 确认 | positive |
| BS-003 | 倒排草案确认后 | PLAN 按 5 节落盘（无 TD、无需求列、无按状态分章）；§3 投影从 WP 填；待办不灌计划；同一建议清单原子呈现 | positive |
| BS-004 | 倒排 Task 与既有 Task 重复 | 查重阶段检测（Owner+时间+语义）→ SUGGEST 提示 PM 确认，不重复建任务 | positive |
| BS-005 | 某 WP 下所有待办已完成 | 00号级联：SUGGEST WP→已完成（入口⑤落块 8「还没写等准许」）；采纳时同文件追加 §7 | positive |
| BS-006 | 查询"PLAN-001 进度" | 05号 §6.7：读 PLAN 文件 WP 表 + 待办文件按 WP Ref 聚合，输出分层进度 | positive |
| BS-007 | 查询"今天做什么" | 优先读待办文件 + 绑定文件；按 Due Date = 今天过滤待办文件，含 WP 归属 | positive |
| BS-008 | 查询"本周计划" | 待办文件按本周切片按 WP 归集；PM 微调仅走 WP 日期变更链路 | positive |
| BS-009 | 倒排目标日期已过 | 提示 PM 确认是否调整为正向排，不静默建无效计划 | positive |
| BS-010 | 同一人被分配多个时间重叠 WP | CHECK 资源冲突 → SUGGEST 调整或登记风险 | positive |
| BS-011 | WP 日期调整 | 级联 SUGGEST 关联 Task Due Date + Change Log（plan_change） | positive |
| BS-012 | 旧工作区无 WP 段/Task 无 WP Ref | WP Ref 视为可选字段，不影响既有功能；D15 自查不报存量误报 | regression |
| BS-013 | 所有 WP completed | SUGGEST PLAN 状态 completed + CHECK 关联里程碑可达性 | positive |
| BS-014 | 倒排 WP 引用需求/里程碑 | CHECK 验证 REQ/M 关联存在，缺失时提示 | positive |
| BS-015 | 查询"倒排还剩几天" | 读倒排元数据（锚点日期）+ 待办文件未完成待办，输出倒计时 + 关键路径预警 | positive |
| BS-016 | "给张三加个待办：8/19 完成接口文档确认"（命中 WP 时间窗口与语义） | WF-8 归属判定 → 落待办文件（WP Ref + Due 8/19）+ 更新绑定文件，原子清单一次呈现 | positive |
| BS-017 | "给李四加个待办：提醒周五交周报"（无交付物） | 判定一次性提醒 → 仅在输出中呈现提示不落待办文件，且输出判定理由 | positive |
| BS-018 | "给王五加个待办：调研竞品"（有 Owner+Deadline 但无 WP 命中） | **不落**正式待办；问绑哪个已有 WP 或先补需求再建 WP。禁止 WP Ref none/待绑定落核心表 | positive |
| BS-019 | 归属证据不足（两个 WP 均语义近似命中） | 置信度阈值生效：必须追问 PM 确认归属，不得静默落库或自行拍板 | negative |
| BS-020 | 14号自查执行 | D15 检出待办文件 WP Ref 完整性异常（指向不存在/缺失的 WP）→ 报不一致并走 WF-8 补落 | regression |
| BS-021 | 日报"明日计划"含正式任务 | 只进当天原文；次日第一次写待办时才建；禁止当日落未来日待办 | positive |
| BS-022 | 会议纪要行动项"李四 8/20 前完成环境部署" | 02号 §2/§3：MANDATORY 落待办文件 + WF-8 归属填 WP Ref，不再是建议级 | positive |
| BS-023 | 纪要行动项缺负责人/截止日 | 缺负责人写入 pm-decisions.md 块 6、不落无主待办；缺截止但有负责人仍可落待办、缺口进块 8。废除未排期待办区块 | regression |
| BS-024 | 待办状态更新（WF-1 场景） | 走 §8.1 状态级联，不误入 WF-8 创建流程；触发源拆分语义自洽 | regression |


## 37. Dual View（需求双视图与开发文档关联）

> 对应 CR-20260815-001（v1.20.0）。覆盖 07 号 §8.10 双视图机制（view_business 派生/view_dev+原型链接挂 REQ 层）、scope_scope 聚合排除硬约束（technical 隔离红线）、开发侧 source_type 扩展、WF-2 需求上下文加载、词库开发侧归一与 19 号存在性巡检。DV-001 为数据正确性红线用例（高优先级）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DV-001 | dev_prd 提取的 ATOM 归并命中已有 Canonical（⚠数据正确性红线，高优先级） | technical 类 ATOM 追加 evidence 但**不参与** scope_scope 聚合，范围判定结论不变；SUGGEST 填充对应 REQ 实现视图待 PM 确认（07号 §8.5/§8.7） | regression |
| DV-002 | PM 提供开发 PRD 要求提取（07号 §8.6 触发 D） | 按模块/接口/页面维度原子化切块，norm_text 保留技术术语原样，登记 source_type=dev_prd（technical/L3） | positive |
| DV-003 | REQ 填写实现视图 + 原型/文档链接 | 登记册 2 新可选列正常写入（摘要级≤100字）；Excel 导出 U/V 列对应（12号 §1.3，与 O-T 连续） | positive |
| DV-004 | WF-2 日报，Task 带 Requirement Ref | 按 05号 §2.5 链路加载 REQ 功能描述+实现视图+原型链接，输出需求上下文（业务+实现双语言对照） | positive |
| DV-005 | WF-2 日报，Task 无 Requirement Ref | 不加载需求上下文、不报错、不强制补录（可选字段原则不变相强制） | regression |
| DV-006 | 单次 WF-2 涉及 12 条 REQ | 性能控制生效：最多加载 10 条或仅加载当轮直接涉及 REQ；字段缺失降级输出不阻塞 | regression |
| DV-007 | 查"REQ-XXX-NNN 具体做什么/怎么实现/原型在哪" | 走 05号需求详情/双视图路由（requirement-register），与范围判定路由（contract-register）不混淆 | positive |
| DV-008 | 开发侧设计文档输入 | 登记为 design_doc（technical），不与甲方侧 design_spec 合并；prototype 仅存指针不入库文件 | negative |
| DV-009 | 日报含未登记开发术语（模块名/接口名） | 17号 §6.3a：按置信度进 pending 或待确认区，不阻塞主体任务；已登记词（类别：模块名/接口名/技术组件）正常归一 | positive |
| DV-010 | 存量工作区升级（旧登记册无 2 新列、日报无新节） | 新字段均可选不影响既有功能；19号巡检不对存量数据报强制缺失（仅 confirmed REQ 覆盖率 P3 提示） | regression |


## 38. Backward Scheduling Daily Matrix（倒排每日矩阵）

> 对应 CR-20260816-001（v1.21.0）。覆盖 05号 §6.7 倒排每日矩阵查询视图（人员×日期矩阵）、00号 WF-7 草案输出规范（两阶段数据源区分 + WF-8 闭环）、10号倒排草案查询提示。含 contract_change 全量回归（00号修改）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| BDM-001 | PM 查询"倒排每日矩阵"，待办文件含完整 WP Ref + Due Date + Owner | 生成人员×日期矩阵：行=Owner 去重，列=今日→锚点日工作日，格=待办简述；数据从待办文件实时读取 | positive |
| BDM-002 | PM 查询"每个人每天干什么"（portfolio 模式，3 个子项目各有待办文件） | 读 project-index 圈定范围 → 遍历 3 个子项目待办文件聚合；矩阵包含全部子项目人员 | positive |
| BDM-003 | 存量待办文件无 WP Ref 列（降级场景） | 矩阵仍可生成：行按 Owner、格按待办标题，WP 列标注"（未关联 WP）"；不报错不阻塞 | positive |
| BDM-004 | 工作区无 PLAN 文件（降级场景） | 范围圈定改为"日期窗口（今日→锚点日期）+ 待办文件 Due Date 过滤"；矩阵可生成 | positive |
| BDM-005 | PM 口述"王涛周二要做XX"后查询倒排矩阵 | 先执行 WF-8 落待办文件，再从待办文件生成矩阵；矩阵中包含王涛周二的新任务 | positive |
| BDM-006 | WF-7 初始草案阶段（待办尚未落待办文件） | 矩阵数据源为 WF-7 本次反向 WBS 产出的拟建 WP/待办列表（非待办文件）；草案输出含完整矩阵 | positive |
| BDM-007 | PM 查询倒排相关，待办文件自上次生成草案后有变更 | AI 在输出中附带提示："待办文件自上次生成草案后有 N 条变更，建议刷新倒排矩阵"（10号查询提示） | positive |
| BDM-008 | 同一人同天 Task >5 条 | 格内只列前 3 条 + "等 N 项"（视图规格第 6 条） | regression |
| BDM-009 | PM 希望在矩阵中呈现里程碑门禁等非 Task 事项 | AI 与 PM 确认后以独立行或标注列呈现，不作为默认 Task 格 | positive |
| BDM-010 | 既有 §6.7 查询（"今天做什么""本周计划""倒排倒计时"等） | 既有 6 种查询路由不受影响，输出与 v1.20.0 一致 | regression |


## 39. v3.0.0 Dual-Pack & Single-Project（双包拆分与单项目回归）

> 对应 upgrade-to-3.0.0.md / 方案 V0.9.2a。Project 包仅 single；Portfolio 包只读。IR-006 反向用例已在 §35 原行就地改写（v3.0.0 反向口径，本模块不重复登记）。
>
> **P-30 断言口径**：Project 包 `portfolio/` 零命中断言仅禁**正向事实源引用**（如“写入 portfolio/…”“事实源在 portfolio/…”）；否定式警示句（如“本包不写 `portfolio/`”“禁写集层”）属清理成果的正确体现，**豁免**，回归不误报。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| V3-001 | 单项目对话贴入含他项目名的日报 | 拆分展示+标待点项目；本项目部分写入；他项目只给分流指引，禁代写 | positive |
| V3-002 | 本项目待办文件出现他项目任务镜像 | 拦截不写入；提示到归属项目 ai 对话 | regression |
| V3-003 | 结转时 `_index` §1 备注含同时参与 ≥2 项目 | Step 0.5 强制提示到兄弟项目 ai 分别结转（读 project-context 兄弟项目路径） | positive |
| V3-004 | Skill 包版本 < 工作区 .skill-version.json | 提示下载更高 Skill + 只读降级，禁止写入 | regression |
| V3-005 | projects/{名}/ai/ 内出现 portfolio/ 或 projects/ | 挂载校验/巡检告警，拒绝聚合（防套娃） | regression |
| V3-006 | 同一项目 ai 挂独立工作区 vs 集工作区 projects/ | 读写行为一致（双宿主换装） | positive |
| V3-007 | 子项目下沉后打包带走 | 含 D-21 最小文件集（todos/_index 花名册、pm-decisions、contract-register、pm-profile、templates、.skill-version.json）；不依赖 resource-register | positive |
| V3-008 | 删除 pm-profile 某 DF 行 | 自愈恢复该行，状态 disabled + 提示 PM | regression |
| V3-009 | 用户说「废弃 DF-013」 | 转为 disabled 留痕，行不删、不移入废弃段 | regression |
| V3-010 | 混报含非本项目进度 | 不入库本项目事实源（DF-016） | positive |
| V3-011 | 查询「陈浩源待办」未说全部 | 默认仅未办结；已办结不列行 | positive |
| V3-012 | 待确认输出 | 符合 21 号 §5.1b 一次问完（分组编号+回复模板） | positive |
| V3-013 | 间接配合人员有日报/无日报 | §0.5 追加进组行；出组须 PM 确认，AI 不自动判出组 | positive |
| V3-014 | 08-01 进组一天、08-15 再有能耗 | 不因能耗补录建 08-02~08-14 空日目录。废除「空窗永不占位」作为结转通则。08-15 若读/写 todos → 除已出组外全员建档 | positive |
| V3-015 | 向导缺人工计量单位 | 不放行 + 持续提醒；单位中立不得写死人日 | regression |
| V3-016 | 补录历史能耗 | 只改当日明细+累计按明细重算，不回溯改历史快照 | regression |
| V3-017 | 新风险编号 | `R-NNN`，只读 risks/index.md 求最大；存量时间戳号仍识别 | positive |
| V3-018 | 查询旧编号 R-011 | 双格式兼容，级联不炸 | regression |
| V3-019 | 直接落库级新建待办 | 不弹确认，`Confirmed By: auto`，不进块 8 子节「已经写了等点头」 | positive |
| V3-020 | 终态关闭（非 DF-013） | 必须逐条确认，不可简化 | regression |
| V3-021 | 日报 100% /「已完成」对应待办 | DF-013 自动完成，`Confirmed By: auto`，**计入**已完成统计与超期；不进块 8 子节 1 | positive |
| V3-022 | 查询我的待办，含 `待确认` 已完成 | **默认仍可见**（未办结或「待确认完成」分组），禁止当已办结隐藏。`auto` 完成按已办结默认不列 | regression |
| V3-023 | 「展示所有」/「所有任务」/「含已完成」 | 展开已办结；老触发词兼容 | positive |
| V3-024 | WF-8 最小规则集 00+22+21+06 | 无风险/需求/变更关键词时不强制加载 04/07/08，操作仍成功 | positive |
| V3-025 | 指纹失配（副本二次编辑） | 提示内容版本差异，严禁静默覆盖 | regression |
| V3-026 | PM 未确认下沉清单 | 禁止执行复制/移动 | regression |
| V3-027 | 05/07 号路由 | 无「集层 portfolio/requirements 存储」残留 | regression |
| V3-028 | Project 包 references grep portfolio/ 存储路径 | 集层路径零命中；跨项目概念字样可保留 | regression |
| V3-029 | Portfolio 对 projects/*/ai 写文件 | 拒绝；只输出建议更新清单 | regression |
| V3-030 | 出集周报但某项目无当期周报 | 默认提示先出周报；PM 明确「临时摘」才从日报摘并标临时摘要 | positive |


## 40. Daily Report Query Routing（日报查询路由，v3.1.0 CR-A）

> 对应 upgrade-to-3.1.0.md。个人日报内容在 todos/{date}/{owner}.md；项目日报是按需生成的存根，可能不存在。禁止先探测 reports/daily/。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QR-DR-001 | "昨天日报有什么风险点/问题" | 直读 `todos/{date}/*.md` §3，不得先探测 `reports/daily/` | positive |
| QR-DR-002 | "X月X日的项目日报" | 读 `reports/daily/project/`；不存在则提示可按需生成，不报错 | regression |
| QR-DR-003 | "某某今日工作汇报" | 落 `todos/` 两步流程（§2 存档 → §3 映射），禁落 `reports/` | regression |


## 41. Dev Repo Layout（开发仓三目录，v3.1.1 CR-G）

> 对应 upgrade-to-3.1.1.md。能力规则不变；校验开发仓布局与分发包瘦包。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| LG-001 | 仓库根是否作为 Skill 包根 | 根目录无 SKILL.md；`ChronoPM-Project/SKILL.md` 存在 | positive |
| LG-002 | 包内 migrations 目录 | `ChronoPM-Project/governance/migrations/` 仅当前 `upgrade-to-3.1.1.md`；历史在 `governance-shared/migrations-history/` | positive |
| LG-003 | 分发包是否含历史 upgrade / baselines | 含当前 upgrade + skill-contract；不含 `upgrade-to-3.0.0.md`、不含 baselines | regression |


## 42. AI 回复溯源标注（DF-017，v3.2.0 CR-B）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PM-001 | 查询类提问且 AI 读了事实源 | 回复含「数据来源：{路径} §{章节}」 | positive |
| PM-002 | 写入待办/登记册后回复 | 回复含「已写路径：{路径}」一行 | positive |
| PM-003 | 内部扫描了多文件才定位 | 只出结论性路径，不罗列 grep/扫描过程 | regression |


## 43. AI 主动识别习惯（DF-018，v3.2.0 CR-B）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PH-001 | 连续 3 次一致的输出格式偏好 | 写入 pending + 末尾 SUGGEST「💡 检测到候选习惯」；不静默 confirmed | positive |
| PH-002 | 本轮已有该维度 confirmed 偏好 | 不再提示该维度候选 | regression |
| PH-003 | 同一轮观察到 2 个候选习惯 | 每轮最多输出 1 条；不打断主任务 | positive |


## 44. 关联待办同步（WF-Linked，v3.3.0 CR-C）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| TD-001 | 为两人创建同一件事的待办 | §1.3 双向写入关联待办编号 | positive |
| TD-002 | 将 TD-A 标已完成且有关联 TD-B | 无处理方式：问一次并写入决策文件；有处理方式：AUTO 完结，不问 | positive |
| TD-003 | 存量待办无关联待办列 | 按无关联处理，仍输出已检查 | regression |


## 45. 工作日志溯源（TD Ref，v3.3.0 CR-C）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WL-001 | 写入 §3 且能对应 §1 待办 | 日志带 TD Ref | positive |
| WL-002 | 写入 §3 无法匹配待办 | 标待归属并罗列请确认；禁止自动新建 | positive |
| WL-003 | 读取存量无 TD Ref 的日志 | 视为未关联，不报错 | regression |


## 46. 缩写治理（v3.3.0 CR-C）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| AB-001 | 新人缩写与在册冲突 | ASK 候选；先到先得；不改原占用者 | positive |
| AB-002 | PM 要求回填缩写 | 输出人员→现行缩写→历史别名清单，待裁定不猜测 | positive |
| AB-003 | 查询 TD-SJJ-* 而现行缩写已改 CJJ | 历史别名命中同一人 | positive |
| AB-004 | Portfolio 归并储金晶跨项目 | 按中文名归并，不按 CJJ/SJJ | regression |


## 47. 报告存根与时间线报（v3.4.0 CR-D）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| ST-001 | 查询已生成的历史项目日报 | 直读存根，不重汇聚 | positive |
| ST-002 | 生成今日项目日报 | 实时汇聚；文件可覆写；不成不可变存根 | positive |
| ST-003 | 时间线区间与已有存根精确重合 | 直读存根 | positive |
| ST-004 | 请求区间超出/相交/真子集已有存根 | 整段从 todos 重汇聚，禁止拼接旧存根 | regression |
| ST-005 | 工作区无 reports/timeline/ | 不报健康检查 P0；首次生成时懒建 | regression |
| ST-006 | 「生成上月月报」 | 时间线报自然月区间；禁止写入 reports/monthly/ | positive |


## 48. WP 强制绑定与独立存储（v3.5.0 CR-E）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WP-001 | 新建待办且索引有高置信匹配 WP | 自动填 WP Ref 并输出已自动绑定 | positive |
| WP-002 | 新建待办无匹配 WP | 不落核心表；问绑哪个；禁止猜填、禁止待绑定占位落盘 | positive |
| WP-003 | 计划文件 §3 | 仅 4 列引用简表（编号/名称/状态/里程碑），详情在 wps/WP-*.md | positive |
| WP-004 | 新工作区 init | 预建 wps/ 与 wps/_index.md（8 列）；schema=0.10.0 | positive |
| WP-005 | 新建 WP | 编号 WP-YYYYMMDD-NNN（ASCII，当日序号）；存量短号/中文名不重编 | positive |


## 49. WP 数据一致性（v3.5.0 CR-E）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WC-001 | 新增 WP-001 文件 | 同步 _index.md 行 + 所属计划 §3 简表；§8c.2 含「§7 已追加」与计划投影行 | positive |
| WC-002 | 改待办 WP Ref | 校验引用的 WP 文件存在；**不回写** WP 文件 §4 | positive |
| WC-003 | 索引缺行但 wps/WP-002.md 存在 | 文件有效；D20 补行；不判死、不删除 | regression |


## 50. AI 自动识别 WP 绑定（v3.5.0 CR-E）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| AI-001 | 待办标题含 WP 名称关键词 | 高置信自动绑定 | positive |
| AI-002 | 多个 WP 近似命中 | ASK 清单，不得静默落库 | positive |
| AI-003 | 一轮结束未绑定检测 | 只扫本轮读写文件 + 当日 _index 圈定的人；禁止全库扫 | regression |


## 51. pending 主动推送（v3.5.0 CR-E）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PU-001 | 开放行之和 N>0 的普通查询 | 横幅「有 N 件事等你裁定」=仍开放行；不含本轮已移出项 | positive |
| PU-002 | 未绑定 WP 的 pending 提醒 | DF-019 句式：编号清单直问，无长段落解释 | positive |
| PU-003 | 05 §6.3 简单查询且本会话未读 pending | 不加载 pending 全文；不因此漏答主问题 | regression |


## 52. WP 创建溯源（v3.5.0 CR-E）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WS-001 | 新建 WP 且需求登记册有匹配 REQ | 自动填 §2 关联需求 | positive |
| WS-002 | 新建 WP 找不到出处 | ASK 需求蔓延风险；PM 确认后登记 risk-register | positive |
| WS-003 | 存量 WP 关联需求为空 | 不强制回填；抽取清单可提示补绑 | regression |


## 53. 源文档拆解体系（v3.6.0 CR-F）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SD-001 | 对新合同做拆解 | 建 `requirements/sources/{CON-…}/` 五件套并写 `_index.md` 行 | positive |
| SD-002 | 索引缺行但 `sources/SRC-001/meta.md` 存在 | 目录有效；补行；不判死 | regression |
| SD-003 | ATOM kind=background | 写入 facts.md；不进 Canonical/scope_scope | positive |
| SD-004 | 清单外新类型「监理评估」 | registry 追加一行即可；簇前缀可用 SUP- | positive |
| SD-005 | D22 本轮只改了 1 个 WP | 只扫本轮文件；禁止全库扫；与 WF-8 溯源合并 pending | regression |
| SD-006 | 存量 `{type}-source/` 尚未零清 | 零清门禁阻断新拆解/对账/RI；输出零清清单；已建 sources/ 不删 | regression |

## 54. 源文档拆解增强（v3.7.0 CR-H）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SD-101 | 拷入含共享合同的 ai 后首次对话 | WF-SD-1 提示一次，不阻断主体任务；同源标 shared_from 不重拆 | positive |
| SD-102 | 同名文档指纹不同 | 待裁决 + 写入 pm-decisions.md 块 8 | positive |
| SD-103 | 同文档新版本二次拆解 | WF-SD-2 增量血缘替换，parse-log 记轮次 | positive |
| SD-104 | 指纹未变再拆 | 输出无变化跳过 | negative |
| SD-105 | atoms 超 300 条 | 转 atoms/ 分片 + _index.md，不动 ATOM 数据 | positive |
| SD-106 | 拆解产出 REQ | 自动取号 REQ-{映射代号}-NNN 且回填 ATOM 指针 | positive |
| SD-113 | 零清完成后访问旧拆解路径 | 旧目录已归档删除不再 fallback；未零清仍阻断 | regression |
| SD-107 | 拆解发现术语 | 落 facts kind=term，攒批确认，不逐条弹 | positive |
| SD-108 | 旧 5 列 ledger / 非 MD5 指纹查询 | 兼容读取（含 Portfolio V-8），触碰 SUGGEST 补齐 | regression |
| SD-109 | 未完成零清触发对账 | 零清门禁 + 清单 | regression |
| SD-110 | D24 限局部 | 只扫本轮触碰目录，指纹-台账-分片三对齐 | regression |
| SD-111 | 四语义类条款 | 要求/约束→atoms→Canonical；描述→facts 不进 scope_scope | positive |
| SD-112 | 重拆后术语 | 词库只更新指针/计次，不删条；消失标 stale | regression |

## 55. entity-registry 废弃（v3.7.0 CR-I）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| ER-101 | 无 entity-registry 的新项目做实体枚举 | 从 WP §3（功能点）聚合，不报缺失 | positive |
| ER-102 | 日报检出终态事件 | SUGGEST 更新 WP §3（功能点）对应实体行并追加留痕 | positive |
| ER-103 | project-context 推导链覆盖 | 按覆盖表执行，与旧 registry 行为等价 | regression |
| ER-104 | 存量 registry 迁移（无 WP / 列漂移 / 旧 T 号） | 分流清单正确、归档后删、数量核对通过 | positive |
| ER-105 | 未迁移项目触发推导 | 门禁阻断 + 迁移清单 | regression |
| ER-106 | Portfolio 实体进度聚合 | 只读聚合不落地 | positive |
| ER-107 | D14 巡检 | 查 WP §3（功能点）↔待办终态，不查已废 registry | regression |

## 56. 风险问题体系重构（v3.7.0 CR-J）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| RJ-101 | 日报「有 X 的风险」 | 识别判定卡，不直接登记 | positive |
| RJ-102 | 已发生事实用风险句式 | 纠正并建议改归问题 | positive |
| RJ-103 | 登记描述不合句式 | 改写对照待 PM 确认 | positive |
| RJ-104 | 查某风险历史 | 状态时间线表直读 | positive |
| RJ-105 | 高风险无关联待办 | 级联告警 + SUGGEST 建待办，不 AUTO | positive |
| RJ-106 | 应对待办完成 | SUGGEST 缓解评估 + 时间线；WF-1 反向触发 | regression |
| RJ-107 | 预警信号出现 | SUGGEST 激活应急待办 | positive |
| RJ-108 | 存量宽表+条目块迁移 | 数量核对、枚举映射、待解析、启发式 | regression |
| RJ-109 | 活跃册超 30 条 | 归档 + index 更新，查询 ≤3 跳 | positive |
| RJ-110 | 新风险取号 | 短号 R-NNN 接续；时间戳旧号兼容 | regression |


## 57. v3.8.0 Personnel/Confirm/Cost (PC)

> 对应 upgrade-to-3.8.0.md A6.1。人员事实源改待办体系、对外确认话术、兼容人工成本台账。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PC-001 | 对外确认/处理汇报 | 对外不说「建议更新清单」；处理类列出改动文件路径；禁止章节号 §2/§3 | regression |
| PC-002 | 待办进度标 100% | 进度 100% 必须已完成（状态同步落已完成；正文「收尾」不回退） | positive |
| PC-003 | 日报明日计划指向未来日 | 禁止建 `todos/{date>今天}/` 目录或未来日待办行；只写入当天个人 §2 | regression |
| PC-004 | 碰今天任一待办 md 或今天 index，且今日结转未完成 | 创建契机先按 §1 全员 Step 0，再建/改点名的人 | positive |
| PC-005 | 人员名录 | 花名册=`_index` §1，无第二文件；禁止另建花名册.md / 继续写 resource-register | regression |
| PC-006 | 某人只有日合计能耗 | 日合计无分次空表（无分次则整节省略） | positive |
| PC-007 | 同日多行外部填报 | 按人+日 SUM 写入 §0.6 当日一行 | positive |
| PC-008 | 查某人能效/成本损耗 | 最新文件 §0.6 按日并置同日 §1/§3；不伪造任务分摊；不与 budget 混 | positive |
| PC-009 | 补录历史能耗 | 有该日文件 → 写该日；无该日文件 → 不建空日目录，孤儿行写最新文件；累计不含重复待裁定 | regression |
| PC-010 | 待办状态枚举 | 待办状态无「待评审」（评审是独立待办） | positive |


## 58. v3.9.0 过程日志 / 分片 / 映射 / 需求链路 / 打包

| Case ID | Input | Expected | Type |
|---|---|---|---|
| OL-001 | 拆解一步结束 | logs/ops/ 已有该步行，即使后续失败 | positive |
| OL-002 | 无 token 接口 | 主列有摘要/动作/文件；用量为 —；禁止全未知行 | regression |
| OL-003 | 字段抽空 | 表 B 有行，摘录 ≤80 字 | positive |
| OL-004 | 当天文件超 300 行 | 拆 YYYY-MM-DD-p2.md，index 加一行；不得直接进月归档 | regression |
| OL-005 | 跨月 | 上月整包进 logs/archive/YYYYMM-ops.md | regression |
| SH-001 | 两人日报并行 | 双方只写自己的 inbox；_index 仅收尾重建当日参与 | positive |
| SH-002 | 工人写 _index 或 {owner}.md | 失败 / 回归禁止 | regression |
| SH-003 | 大文档两片 | 不一次全量；各写 part 文件 | positive |
| SH-004 | 同人同日第二份（同一 agent） | 经 inbox 按 §1.3 合并追加 | regression |
| SH-005 | 两 agent 同时投同一人 | 一天仍一份 {owner}.md；收尾 inbox 无稿无 claim | regression |
| SH-006 | 两 run 同时 C' | 仅第一者写 {owner}.md；无稿则中止；非第一者删自己的 claim | regression |
| SH-007 | 遗留稿 + 孤儿 claim | C' 全目录接管；冲突重试 3 次；不向人 ASK | regression |
| SH-008 | 实读之后又新投一份 | 只删实读清单；新文件下一轮才合 | regression |
| SH-009 | 巡检发现残留稿 | AUTO 跑 C'；不建 pending、不删未合并稿 | regression |
| MP-001 | 日报进展对不上已有待办且够正式 | 自动新建待办；列出新建了哪条；不 ASK | positive |
| MP-002 | 日报只有「熟悉了一下」 | 不新建待办 | regression |
| MP-003 | 喂了花名册没有的人的日报 | 自动建个人文件+花名册；岗位待补全 | positive |
| MP-004 | 「给某某加个待办」而此人不在册 | 自动建人+待办 | positive |
| MP-005 | 日报提到「配合了李四」，李四未入册 | 不自动为李四入册 | regression |
| MP-006 | 他项目进展 | 不在本项目新建待办/入册 | regression |
| MP-007 | 新建风险，责任人未入册且无跟踪待办 | 自动建人+跟踪待办；不给 PM 另建 | positive |
| MP-008 | 责任人已入册且已有关联本条开放待办 | 不重复建人、不重复建待办 | regression |
| MP-009 | 责任人已入册但无跟踪本条 | 只建跟踪待办 | positive |
| MP-010 | P-N3 自动建跟踪待办后 | 当日该人 md 仍唯一；花名册与人员信息一致 | regression |
| RQ-001 | 投喂合同拆出需求 | 只写入需求清单（未确认）；不创建待办 | positive |
| RQ-002 | 一条已确认需求绑两个 WP | 需求工作包列含两个编号 | positive |
| RQ-003 | 未确认需求被拿去拆待办 | 拒绝；进决策文件需求未确认 | regression |
| RQ-004 | 需求来源 | 同时有文件、章节、页码 | positive |
| WQ-001 | 无任何需求编号要新建 WP | 禁止建包；进决策文件 | regression |
| WQ-002 | 待确认 WP 拆待办 | 拒绝 | regression |
| WQ-003 | 三条小需求绑同一个 WP | 合法 | positive |
| WQ-004 | 一条大需求绑三个 WP | 合法 | positive |
| WQ-005 | PM 确认待确认 WP | 状态→已规划，此后允许拆待办 | positive |
| PD-001 | 行动项缺负责人 | 不落待办；决策文件块 6 有行 | positive |
| PD-002 | 已确认需求未绑 WP | 决策文件块 2 有行 | positive |
| PD-003 | 升级时旧 pending-changes 有未结项 | 全部出现在新决策文件；旧文件在 backup；无丢行 | regression |
| PD-004 | 决策记录 | 有裁定摘要与对象编号；没有对话原文整段 | regression |
| LK-001 | PM 已说张三办结自动完结李四 | 张三办结时李四 AUTO；不问 | positive |
| LK-002 | 只建了关联、没说处理方式 | 办结时问一次 | regression |
| PL-001 | 日报处理回复 | 正文无 §2、§3、Target File、建议更新清单 | regression |
| PL-002 | 处理完一批日报 | 主动列出改动文件路径，不含章节号 | positive |
| PL-003 | 集层处理汇报 | 给文件、不给章节 | regression |
| PL-004 | 计划正文 | 只有工作包引用行，没有待办编号行 | regression |
| PL-005 | PM 确认倒排计划 | 写 WP+计划简表；不按人员×日期灌待办 | regression |
| PK-001 | dry-run Project zip | 无 tests/BLUEPRINT/16/MODULE_MAP；有 source-split 规则与四模板；该目录无 SKILL.md | regression |
| PK-002 | zip 内有 references 无 SKILL.md 的子树 | 仅当主 SKILL 未引用时 FAIL；source-split 被拆解路由引用则合法 | regression |
| CL-005 | VERSION=3.8.0 且 baselines/3.8.0 存在时若存在 upgrade-plan-v3.8.0.md | audit 非 0 | regression |
| CL-006 | 同时存在无基线的 3.9.0 与 3.10.0 两份 AP | audit 非 0 | regression |
| SS-001 | 源文档拆解场景 | 加载 split-rules.md；日报场景不加载 | regression |
| SS-002 | zip / 开发仓 | source-split 无 SKILL.md；有 CAPABILITY.md + 四模板 | regression |
| TM-001 | migrate 现行模板 | 工作区 daily-todo 与 Skill 包 headings 一致（覆盖） | regression |
| TM-002 | 新建个人待办 | 不得用昨天文件的旧节顶替 | regression |
| TM-003 | 无模板类型 | 禁止新建 milestones/milestone-board.md | regression |

## 59. v3.10.0 对话日志 / 投喂入库 / 全员建档 / TD 编号 / 时间盒

| Case ID | Input | Expected | Type |
|---|---|---|---|
| OL-010 | 纯问答 | 当日日志有一行，改动文件=无 | positive |
| OL-011 | 集层对话 | 写入 portfolio/logs/ 当日；不写成员 ops | positive |
| OL-012 | 集层请某项目改待办 | 集层日志出处=集层→项目名；成员文件未改 | regression |
| OL-013 | 新 projects 目录 | ASK 收编；收编后按管理路径可探测日志，不写指针列 | positive |
| OL-014 | 查成员日志 | `{集根}/{管理路径}/logs/ops/_index.md` 存在则打开；无则尚未发生 | positive |
| OL-015 | 升级日已有旧列文件 | 不追加旧文件；新对话进同日 p2 新列 | regression |
| FE-001 | 「帮我整理记录」+ 工时表 | 走入库，不停留分析；写入 §0.6 不是 §1.2 | positive |
| FE-002 | 只上传表、没说记录 | 拆完 ASK 是否同步个人待办成本 | positive |
| FE-003 | 表头对不上 | 问列映射，不写死 J/O/K | positive |
| FE-004 | 姓名不在册 | ASK 临时支援；禁止静默幽灵文件 | regression |
| FE-005 | 仅能耗起链 | 今天有文件、§1 空；次日无投喂无待办 → 仍建次日文件（§1 空）、不进空闲台账 | positive |
| FE-006 | 存量缺 §0.6 | 插入该节并写入，不报不支持 | positive |
| FE-007 | 用户问记到待办了吗 | 答能耗段有无，不拿 §1.2 空列当否 | regression |
| FE-008 | 集层投喂跨项目表 | 不写成员 §0.6；ingest + V-9 + 集层日志 | regression |
| FE-009 | T+1 结转 | 新一天个人文件能耗段没有把昨天以前的日表整表拷来；有累计；无投喂不追加当日空行 | regression |
| FE-010 | 查某人某日能耗 | 打开该日个人文件；不读 energy 专档（该类文件不得存在） | positive |
| FE-011 | 回填一个已有历史日文件的成本 | 写入该日个人文件能耗段；不被旧禁则拦截；不建 archive | regression |
| FE-012 | 仅能耗且当天在 §3 | 次日不进空闲台账 | regression |
| FE-013 | 只交过日报、§1 从未有待办行 | 不进空闲台账 | regression |
| FE-014 | 该人该日已有当日能耗，再投同一天 | 不覆盖、不自动相加；异常=重复待裁定；问 PM；累计不含该日 | regression |
| FE-015 | 同一张表里同一人同一天 3 行 | 分次 SUM 成日表一行，异常=—；不走裁定 | positive |
| FE-016 | 8-05 成本只在 8-11 文件，8-23 再投 8-05 | 在 8-11 命中；标重复待裁定；不写第二行；禁止全库扫 | regression |
| FE-018 | 今天 index 标记 true，但花名册 30 人缺当天文件，给其中 1 人加待办 | 先补齐应建档全员文件，再改点名的人 | positive |
| FE-019 | 休息日当天「查待办」；新建工作区 init 当日 | 除已出组外全员有当天个人 md；允许空待办表 | positive |
| FE-020 | 周五日报含周六任务且 PM 说周末上班 | 周六任务只进周五 §2；禁止周五当场建周六目录或待办行 | regression |
| FE-021 | 「查一下我的待办」 | 每行含 TD-…；禁止只用 1. 2. 3. 当编号 | regression |
| FE-022 | 建 WP 绑定结束晚于 WP 结束的待办 | 必须问：延长 WP / 压缩待办 / 挂起；C 写入 pm-decisions 查重键=TD；开始早于 WP 仅轻提示 | regression |

## 60. WP Status History & Stage (WSH)

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| WSH-001 | 新建 WP | 自带 §7 建包行（5 列，从=—，到=待确认） | positive |
| WSH-002 | 确认切法/块 3 待确认→已规划 | 同一文件一次写回 §7+头；镜像索引/正常计划 §3 | positive |
| WSH-003 | 只改头不记历史 | 级联验证不通过 | negative |
| WSH-004 | 问几号变什么状态 | 00 读包 §7 直答 | positive |
| WSH-005 | 旧包无 §7 | 降级报头+「状态链未建」，不报错 | regression |
| WSH-006 | 末行与头矛盾 | D33 P2；查询仍报链尾 | regression |
| WSH-007 | 同日多次转移 | 多行追加 | positive |
| WSH-008 | 通用回填算法 | 清单覆盖+抽样核链尾=头 | positive |
| WSH-009 | 要求改写已有历史行 | 拒绝，只允许追加更正行 | negative |
| WSH-010 | 阶段「开发中」 | 头=进行中；「上线」→头=已完成 | positive |
| WSH-011 | 问 WP 进度 | 绑定待办进度求和；无绑定=0% | positive |
| WSH-012 | 阶段跳步/回退 | 正常记录，不强制逐级 | positive |
| WSH-013 | 未知阶段名 | 登记待确认，不拒绝不静默改清单 | regression |
| WSH-014 | 入口⑤ 从待办推导 | 只登块 8「还没写等准许」；确认后落链 | positive |
| WSH-015 | §8 自定义阶段名 | §7 可引用 | positive |
| WSH-016 | 问现在什么状态；头≠链尾 | 报链尾并 D33，不改旧行 | positive |
| WSH-017 | 更正错误当前态 | 追加接链，旧行不变 | positive |
| WSH-018 | 默认 11 阶段 | 均能映射到四枚举 | positive |

## 61. Glossary Sensing (GLS)

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| GLS-001 | 「个体户指的是个体工商户」 | 同轮 confirmed | positive |
| GLS-002 | AI 问「是不是」、PM「对」 | confirmed，不要求 G 号 | positive |
| GLS-003 | 口头抱歉但不写词库 | 不通过 | negative |
| GLS-004 | 无词库文件 + 首次 T1 | 必须按模板创建再写 | positive |
| GLS-005 | 已 confirmed 再声明 | 只更新命中次数 | regression |
| GLS-006 | 未登记原词出现 2 次 | pending+SUGGEST | positive |
| GLS-007 | WP 查询场景出现 T1 | 00 钩子仍入库 | positive |
| GLS-008 | 日报多个缩写 | 攒批一次；确认后 T2 | positive |
| GLS-009 | 「对，待办今天完成」 | 不写词库 | negative |

## 62. Output Path Guard (OPG)

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| OPG-001 | 整理工时成 xlsx | `ai/outputs/{ts}/files/` + manifest + index | positive |
| OPG-002 | 写到工作区根或与 ai 平级 | 硬中止不写 | negative |
| OPG-003 | 宿主 final workspace folder=项目根 | 仍映射到 ai/outputs/ | positive |
| OPG-004 | 未载 11 的场景出表 | 00 钩子仍走 B 路 | positive |
| OPG-005 | 写后根上出现本轮新文件 | 报缺陷并给迁移，不留 | regression |
| OPG-006 | 扩展名 xlsx/csv | 12 必载；批次+index | positive |
| OPG-007 | 写 todos/{date}/{owner}.md | 不被误判为生成物 | negative |

## 63. Plan Template (PLT)

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| PLT-001 | 新建计划 | 6 节 + status 正常 + PLAN-YYYYMMDD-NNN 文件名；§3 无子行 | positive |
| PLT-002 | 倒排落库 | 仍 6 节；§2 有门禁；§4 阶段列表；无每日矩阵/TD/需求列 | positive |
| PLT-003 | 上线纳入 | §3 一张表，不按状态分章 | positive |
| PLT-004 | 自创章节或按状态分章 | 不落库 | negative |
| PLT-005 | 计划含 TD | 级联失败 | negative |
| PLT-006 | 表 >7 列 | 不通过 | negative |
| PLT-007 | upgrade-to 扫 plans/ | 清单覆盖全部非 PLAN-NNN-*.md | positive |
| PLT-008 | 落库前 | 已读 plan-template | positive |
| PLT-009 | 国庆式按状态分章 | 不通过 | negative |
| PLT-010 | 计划改为废弃 | §3 冻结；plan_ref 去掉；排期走 superseded_by | positive |

## 64. Plan/WP Projection (PWP)

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| PWP-001 | WP 链尾变测试中 | 同轮所有正常 PLAN §3 当前状态已变 | positive |
| PWP-002 | 待办含预演且阶段为空 | §8 写入；链尾=预演则 PLAN 执行人同步 | positive |
| PWP-003 | 只改 PLAN §3 排期 | 不通过，必须改走 WP 时间盒 | negative |
| PWP-004 | §3 状态旧、链尾新 | 闸 2 先修再答 | positive |
| PWP-005 | 一包两个正常计划 | plan_ref 两号，两份 §3 都更新 | positive |
| PWP-006 | 废弃计划 | 闸 2 不改冻结 §3 | regression |
| PWP-007 | 索引 plan_ref 与正常 §3 不一致 | D37 | regression |
| PWP-008 | 增删 WP 未写 §6 | 级联验证失败 | negative |
| PWP-009 | 点名执行人后自动推导 | 不覆盖 | positive |
| PWP-010 | 无关键词 | 阶段执行人保持 — | regression |
| PWP-011 | plan_ref 漏了某正常计划但 §3 仍有此 WP | 闸 1 仍投影该计划 | positive |

## 65. 派活 / 基数 / 时间盒（v3.12.0）

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| DS-001 | 苏晚登录+登出测试 8.26~9.15，已有两条待办 | 不新建第三条；不询问要不要建；两条各绑一个 WP | positive |
| DS-002 | 同上但无已有待办 | 自动建两条，各一 WP，先写后告知 | positive |
| DS-003 | 一条待办试图写两个 WP Ref | 拦截并提示拆分 | negative |
| DS-009 | 正式待办 WP Ref 空/待绑定/none | 禁止落核心表；问绑哪个 WP | negative |
| DS-004 | 只改 WP 时间盒、未点名执行人动作 | 不新建待办 | regression |
| DS-005 | 待办时间完全在新 WP 窗内 | 不改待办时间 | positive |
| DS-006 | 待办结束 > 新 WP 结束 | 问 A/B/C，不自动改期 | positive |
| DS-007 | AI 输出「要不要给苏晚建测试待办」 | 失败 | negative |
| DS-008 | 多 WP 主题不清 | 问一次，不静默 | positive |
| CO-001 | 结转空 WP Ref + 高置信 | 回填恰好 1 个已规划 WP；编号不变 | positive |
| CO-002 | 结转已有合法单值 WP Ref | 不改归属 | regression |
| CO-003 | 结转多值 WP Ref | 不完成态；pm-decisions | negative |
| CO-004 | 结转空 WP Ref 且低置信 | 不把无 WP 行写入今天核心表；TD 编号不变 | negative |

## 66. 拆文件入库（v3.12.0）

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| SF-001 | 「拆文件」+ 需求规格 | 加载 split-rules；写 sources/{编号}/ 六件套；不落待办 | positive |
| SF-002 | 「拆解需求」（无源文件） | 走 07 §3，不建 sources | negative |
| SF-003 | 「整理成 HTML 报告」（无拆文件） | 走 11 outputs，不进 sources | regression |
| SF-004 | 「先拆文件再出 HTML」 | 先 sources 再 outputs | positive |
| SF-005 | 仅走 html-report、不加载 split-rules | 失败 | negative |
| SF-006 | 指纹相同再拆 | 禁止二次拆解 | regression |

## 67. 结构 / 轻量查询（v3.12.0）

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| LQ-001 | 简单查询「明天待办」 | 只加载 05，不加载 00/23/07/21 规则正文；只读 1–2 个数据文件 | regression |
| LQ-002 | 派活写入 | 加载 23；Calls 含 P-WF8-DEDUP；已加载 §7 | positive |
| LQ-003 | 包内无 QODER_RULES.md；16 白名单无该行 | 仅当 LQ-001/004/005/006 口径已满足 | positive |
| LQ-004 | 5 类查询数据来源声明 | 05 §7 仍生效 | regression |
| LQ-005 | 「今天谁没交日报」 | 读 _index + 日志覆盖，不读 references | positive |
| LQ-006 | 简单查询中途改口「给张三加待办」 | 立即离开最小读取，加载写入行 + §7 | positive |
| LQ-007 | SKILL.md 相对 3.11.0 净增非空行 >20 | 失败 | negative |
| LQ-008 | 简单查询「明天待办」 | 不加载 21 规则正文；偏好只可读 pm-profile.md | regression |

## 68. WP 联动 / 生效 / 时间窗 / 技能缺口（v3.13.0）

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| WPL-001 | 待确认 WP 已入正常计划 | D38 提示推进；确认后 §7 追加；PLAN 父行=链尾 | positive |
| WPL-002 | 已绑测试待办、链尾仍待确认 | 建议测试中；确认后追加 | positive |
| WPL-003 | SCAN 测试待办贾星 08-24~09-10 | §8 (AI聚合)；PLAN §4 该 WP 段可见 | positive |
| WPL-004 | §8 已点名，待办是另一人 | 不覆盖；块 8 | negative |
| WPL-005 | 内部验收无待办 | §4 该阶段 ⏳ / `⚠️待安排人` / `— 待排期` | positive |
| WPL-006 | 只改 PLAN §4 排期 | 失败，改走 WP | negative |
| WPL-007 | 一包两份正常计划 | 两份 §3 行 + §4 列表相同 | positive |
| WPL-008 | 两份计划父行排期不同 | D38 歧义 | regression |
| WPL-009 | PLAN §3 加空岗第 7 列 | PLT-006 失败 | negative |
| WPL-010 | §3 插入 `└ ` 子行 | 失败；改走 §4 列表 | negative |
| WPL-011 | 未确认 REQ 仍推进已规划 | E1 拦截 | negative |
| WPL-012 | 废弃 WP-003 | effect=废弃；正常计划移出；§7 到状态不是废弃；index 状态=废弃 | positive |
| WPL-013 | 给废弃 WP 派活 | 不落待办 | negative |
| WPL-014 | 无 effect 字段 | 当正常；触碰补键 | positive |
| WPL-015 | status: 废弃 | 不通过 | negative |
| WPL-016 | 本轮两条同 WP 待办 | SCAN 一次 | positive |
| WPL-017 | 闸 2 §4 已一致 | 不写 PLAN | positive |
| WPL-018 | 查看计划 | 闸 2 后输出完整 PLAN MD（盘上 §3+§4） | positive |
| WPL-019 | PM 纠正误匹配 | 包级排除；下次 SCAN 不再误入 | positive |
| WPL-020 | 双正常计划人期不同 | D38；范围=该 WP 全部正常计划 | regression |
| WPL-021 | §3 引用失踪 WP 文件 | 先 D20，不直接移出 | positive |
| PFA-001 | 「归纳 10-07 前计划」，三项目计划名不同 | 按窗收入，不靠同名 | positive |
| PFA-002 | 某项目仅废弃计划在窗内 | 默认不入 | positive |
| PFA-003 | 同项目两正常计划重叠同一 WP | 一行，来源多值 | positive |
| PFA-004 | 集层要写成员 PLAN | 拒绝 | negative |
| PFA-005 | 窗内有废弃 WP | 默认不输出 | positive |
| PFA-006 | 全年计划 §1 命中但 WP 盒在窗外 | 该 WP 不出行 | positive |
| SKG-001 | 「这是 skill 的问题，记下来」 | outputs 有 `需求-*.md`，含双版本+原话+证据链 | positive |
| SKG-002 | 仅缺某 WP 日期 | 走 19，不落缺口文 | negative |
| SKG-003 | 写到 `requirements/需求-xx.md` | 失败，必须 outputs | negative |
| SKG-004 | 能力目录存在 SKILL.md | audit 失败 | negative |
| SKG-005 | 同痛点第二次 | 原位更新主文档 + 迭代记录一行；无 `revisions/rev-NNN.md` | positive |
| SKG-006 | 用户说不要记 | 标取消 | positive |
| SKG-007 | 仅 05 的进度追问「不对吧」 | 不落缺口文 | regression |
| SKG-008 | 「这是 skill 的问题，记下来」 | 落盘；含 sg_id | positive |
| SKG-009 | 当日已有 SG-…-001 | 下一号 002 | positive |
| SKG-010 | P-ALWAYS 第 4 步直接写文件 | 失败，须经 P-SKILL-GAP | negative |

## 69. 阶段体系 / 目录 / 编号 / 看计划（v3.14.0）

| ID | 输入 | 预期 | 类型 |
|---|---|---|---|
| STP-001 | 新建 WP | §8 含 13 标准阶段表；无 is_milestone；编号 WP-YYYYMMDD-NNN | positive |
| STP-002 | 派活「给张三安排测试」 | 备注区 `阶段：测试`；SCAN 写 §8 测试行；不反问要不要建 | positive |
| STP-003 | 待办标题含「测试用例」 | 命中用例设计，不命中测试 | positive |
| STP-004 | 开发阶段全部已办结后再 SCAN | §8 开发仍 ✅ 且人期不被清空 | regression |
| STP-005 | 「看一下 PLAN-001 计划」 | 闸 2 后输出完整 PLAN MD；不从 todos 实时聚合 | positive |
| STP-006 | init 新工作区 | 存在 `project-info/`；budget/progress-plan 在该目录不在 plans/ | positive |
| STP-007 | 写入 project-info/budget.md | P-ALWAYS 允许（06 §1.1 含 project-info） | positive |
| STP-008 | plans/ 下 `国庆上线计划.md` | 升级只出清单，不插入 §4 | regression |
| STP-009 | WP §8 阶段名 `开发中（完成）` | 剥后缀后映射到「开发」 | positive |
| STP-010 | §8 已点名张三，待办是李四 | 不覆盖点名；进块 8 | negative |
| STP-011 | 需求登记阶段落待办、WP 仍待确认 | 拦截；须先 ADVANCE 到已规划 | negative |
| STP-012 | 混合引用 WP-新设名称申报 与 WP-20260825-001 | 允许；旧号不重编 | positive |

## 70. 格式 / 责任链 / 派生图（FMT，v3.16.0）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| FMT-001 | 日期字段写入 `07-17` | 标记 `⚠️ 日期格式待纠正` | positive |
| FMT-002 | 日期字段写入 `2026-07-17` | 通过 | positive |
| FMT-003 | 叙事中出现 `07-17` | 不误伤 | negative |
| FMT-004 | ID 含 `20260717` | 不误伤 | negative |
| FMT-005 | WP §8 执行人 `王欢欢（2026-06-29~2026-08-20）` | `⚠️ 字段边界待纠正` | positive |
| FMT-006 | 执行人 `王欢欢`，排期 `2026-06-29~2026-08-20` | 通过 | positive |
| FMT-007 | PLAN §4 某 WP 缺阶段；`verify --check-plan-section4` | 退出 1 | positive |
| FMT-008 | PLAN §4 完整；带开关 | 退出 0 | positive |
| FMT-009 | 存量 PLAN §4 压缩；默认巡检无开关 | exit 2 UNJUDGED，不 P0 | negative |
| FMT-010 | skill_gap 手写 3.14.0 | 纠正为 3.16.0 | positive |
| FMT-011 | skill_gap 批次含 manifest.md | 级联失败 | negative |
| FMT-012 | WP-002 前置=WP-001 | YAML+§2b+index 同步 | positive |
| FMT-013 | 废弃 WP-001 | WP-002 upstream 被清理 | positive |
| FMT-014 | related_wps 自指 | 拒绝 | negative |
| FMT-015 | 请求「画 WP 结构图」 | 对话 Mermaid；不落盘 | positive |
| FMT-016 | 未请求画图 | 不生成图 | negative |
| FMT-017 | 正常日报处理 | 行为不变 | regression |
| FMT-018 | 正常待办创建 WF-8 | 行为不变 | regression |
| FMT-019 | 正常计划生成（无 §4 压缩） | 行为不变 | regression |

## 71. 工作包记录 / 图 / 查询 / 盖章 / 功能点阶段（WPR，v3.17.0）

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WPR-001 | 「WP-006 什么状态」 | 摘要 + 指向 `wps/WP-*.md` 的链接；正文不是该文件逐字全文 | positive |
| WPR-002 | 「完整记录」 | 更完整摘要（含实时待办）+ 同一原件链接 | positive |
| WPR-003 | 「把 WP-006 原文贴出来」 | 逐字全文 + 链接 | positive |
| WPR-004 | 「画总览」且无 related_wps | 按计划分章 mermaid；无关联 WP 装入 `rInd` 子图竖排（每行 1 个）；节点编号/名/日期/阶段图标；无人员行；无连线；提示未填关联则提示未填；不编造 | positive |
| WPR-005 | 已有 006→002 边时画总览 | 仅该边（两端同章才画） | positive |
| WPR-006 | 改 related_wps | index 更新且 `_wp-chart.md` 按新形态重画；SSOT 仍 YAML | positive |
| WPR-007 | 只改工作包备注 | 图指纹不变不重写 | regression |
| WPR-008 | 办结一条待办 | 绑定 WP §4b 有一行；确认清单含待办文件+该 WP | positive |
| WPR-009 | 同一结论再次办结 | 不出现两行相同一句话 | regression |
| WPR-010 | 写 I-xxx 不回写待办/WP | 级联失败 | negative |
| WPR-011 | 全部功能点阶段=预演 | 整包预演 ✅、状态历史追加、变更来源 AUTO-全齐、无 pm-decisions 新项 | positive |
| WPR-012 | 五行中一行不是预演 | 整包不自动变 | negative |
| WPR-013 | 记升级需求 | 只在 outputs；未写 pm-decisions；有 〇·五节 | positive |
| WPR-014 | 新建 WP | 标题 `## 3.` 功能点；无「阶段明细」；无 `## 3b.`；无阶段归属列；有「阶段」列 | positive |
| WPR-015 | 把图写到 outputs 当本能力落点 | 禁止 | regression |
| WPR-016 | 一条待办两个 WP Ref | 仍拦截 | regression |
| WPR-017 | dry-run 含 `未评审` 与 `—` 的存量 WP | 清单覆盖这两值；`已评审`进待落位、不静默填阶段名 | positive |
| WPR-018 | `wps/` 下无 `_wp-chart.md` 时首次改 related_wps | 懒建且分章节点/边正确 | positive |
| WPR-019 | 非图形类 skill-gap | 有 〇·五标题，节内无目标产出形态图；未写 pm-decisions | positive |
| WPR-020 | 未迁移旧 WP 仍含「评审状态」列 | 原样展示，不翻译成十三阶段、不报错 | regression |
| WPR-021 | 功能点表仅 1 行且阶段=预演 | 仍 AUTO，来源 AUTO-全齐 | positive |
| WPR-022 | 任一行阶段为 `—` | 不改整包 | negative |

## 72. 图分章 / 结构闸 / 归档 / 结转脚本 / 问答规范（v3.18.0）

施工只认合计 **729**（本模块 64 + 模块 73 新增 23）。禁止沿用 706。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WPC-001 | 新建 WP 进 PLAN-001 | 同回合 `_wp-chart.md` 该章出现新节点；8c.2 含图行 | positive |
| WPC-002 | 建包后不喊画图 | 图仍更新 | positive |
| WPC-003 | 指纹未变 | 不重写 generated_at | regression |
| WPC-004 | 两计划；一包两个 plan_ref | 两章都有该节点 | positive |
| WPC-005 | 无 plan_ref | 仅「未绑定计划」章 | positive |
| WPC-006 | effect=废弃 | 任何章都没有 | negative |
| WPC-007 | 已完成归档 | 默认图没有 | negative |
| WPC-008 | 同章 5 个无 related_wps | 一个 `rInd` 竖堆；不是 3+2 两行横折 | positive |
| WPC-009 | 节点无人员行，有日期与阶段图标 | 通过 | positive |
| WPC-010 | related_wps 对端不在本章 | 本章无该边 | negative |
| WPC-011 | 日期非规范 | 图上格式化为 YYYY-MM-DD 或不改 WP 文件 | positive |
| WPS-001 | 有 R- 无 §5 行 | WARN / 8c.2 未完成 | positive |
| WPS-002 | 自定义「关联/依赖」混排 | 判违规，拆到 §5+WP §3（功能点） | positive |
| WPS-003 | 待办标题含「全模块」只挂一行 | 回填适用功能点或 8c.2 缺失 | positive |
| WPS-004 | 普通待办未写全模块 | 不猜全表回填 | negative |
| WPS-005 | §4 仍派生不落盘 | regression | regression |
| WPS-006 | 无 WP §3（功能点）的包，待办备注阶段=测试 | §8 测试行 UNION 该 Owner；(AI聚合) | positive |
| WPS-007 | 两功能点各挂不同人、阶段都=开发 | §8 开发行两个人名「、」分隔；WP §3（功能点）当前表无执行人列 | positive |
| WPS-008 | 功能点关联待办全 — | §8 对应站 `⚠️待安排人`，不填包负责人 | negative |
| WPS-009 | §8 测试已点名，待办另一人 | 不覆盖点名 | regression |
| WPS-010 | 开发待办办结，测试已排人 | §8 开发行仍保留开发执行人且为 ✅；测试行 🔄 为测试人；开发人不被清空 | positive |
| WPS-011 | 同上 | 同回合 §8b 至少两行：开发=冻结（含办结 TD）、测试=聚合；缺任一行级联失败 | positive |
| WPS-012 | 改了 §8 人期但不写 §8b | 不得称级联完成 | negative |
| SKG-011 | 生成时省略 〇·五 | 不得登记 index | negative |
| SKG-012 | 模仿缺 〇·五的旧批次 | 仍以当前模板为准，有 〇·五 | positive |
| ARC-001 | 头→已完成 | 行进 §2；`completed_at` 与 §7 日期一致；进行中段无此行 | positive |
| ARC-002 | P-WP-RETIRE | 行进 §3；`retired_at` 有值；图无此包 | positive |
| ARC-003 | 「完成的工作包」 | 只列 §2 段 | positive |
| ARC-004 | 「工作包清单」默认 | 只有进行中段 | positive |
| ARC-005 | 先完成再废弃 | 在废弃段；两列时间都有 | positive |
| ARC-006 | 新 init | `_index` 三段 12 列，无「是否里程碑」 | positive |
| ARC-007 | 不搬 WP 文件 | glob 仍 `wps/WP-*.md` | regression |
| ARC-008 | 已完成段 WP 头改回进行中 | 行从 §2 移回 §1；`completed_at` 保留不删；可再入默认图 | positive |
| ARC-H01 | 存量头=已完成、effect=正常、单表 index | dry-run 列入已完成归档并拟 `completed_at`；确认后行只在 §2；默认图无此节点 | positive |
| ARC-H02 | 存量 effect=废弃 | 列入废弃归档并拟 `retired_at`；默认图无此节点；文件仍在 `wps/` | positive |
| ARC-H03 | 已完成后又废弃 | 只进 §3；两列时间都有（能推导的） | positive |
| ARC-H04 | §7 无已完成行且头不是已完成 | 不进已完成归档 | negative |
| ARC-H05 | 推不出日期 | 时间列 `—` + ⚠️，不写今天 | negative |
| ARC-H06 | 开发仓无 wps/ | skip，不失败 | regression |
| ARC-H07 | 已三段再跑 | 幂等，不复制行 | regression |
| CO-S01 | 有 Python；今日未结转；花名册 3 人 | 3 份个人文件；未办结 TD 编号不变；标记 true；stdout 有报告 | positive |
| CO-S02 | 无 Python | AI 按 22 全文做完；不跳过 | regression |
| CO-S03 | 已 true 且文件齐 | 脚本退出 0 不写 | regression |
| CO-S04 | 昨日未办结 TD-A | 今日仍 TD-A，不是新号 | positive |
| CO-S05 | 空 WP Ref 且项目仅 1 个已规划 WP | 回填该 WP | positive |
| CO-S06 | 空 WP Ref 且多个已规划 WP | 不进今天核心表；ASK 行 | negative |
| CO-S07 | 同时参与≥2 | 文件仍结转；ASK 含 0.5 提示材料 | positive |
| CO-S08 | `--date` 未来日 | 拒绝写盘 | negative |
| CO-S09 | 当天个人文件已有日报 §2 | 不覆盖 §2；只补缺失未办结 | regression |
| CO-S10 | 有 Python 但 AI 手搓全员、不跑脚本 | 级联失败 | negative |
| CO-S11 | 源日 §2 有日报 | 今天 §2 空（或已有今天日报则不覆盖） | negative |
| CO-S12 | 源日核心表全已完成 | 仍建今天文件；§1 可空；不跳过该人 | positive |
| CO-S13 | 源日有已完成 + 未办结 | 今天只有未办结；已完成留在源日 | positive |
| CO-S14 | 源日无未办结且无日报 | 标空闲 + ASK:IDLE；**花名册不是已出组** | negative |
| CO-S15 | 周一，周五有文件，周六日无目录 | 源=周五文件，不因「昨天无 md」失败 | positive |
| CO-S16 | 今天该人文件已在（已投喂日报） | 不重建；只补缺失未办结；§2 不动 | regression |
| CO-S17 | 花名册今日已出组 | 不建今天个人文件 | negative |
| CO-S18 | 源日 §1.5 有生效处理方式 | 今天 1.5 仍有该行，办结不问第二遍 | positive |
| CO-S19 | 脚本 exit 1，报告仅张三失败 | AI 只给张三走 E5；其余用脚本结果；**不算**手搓全员 | positive |
| RN-001 | 用户中文问进度 | 中文结论；无英文思考段 | positive |
| RN-002 | 模型内部英文推理 | 用户可见正文不得出现 I now have / Let me | negative |
| RN-003 | 「电子签名和实名进度」（纯查询） | **不准**问是否执行方案/是否基于文档继续 | negative |
| RN-004 | 本回合已写待确认变更 | 才允许 §5.0；必须白话说出改了哪些文件 | positive |
| REG-001 | 正常日报 / WF-8 / 画人员图点名 | 行为不变（日报前先脚本结转） | regression |

## 73. 图拓扑 / skill-gap 生命周期 / 功能点留痕 / 确认后不回放（v3.19.0）

施工只认合计 **729**。禁止沿用 706。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WPC-012 | 同章 3 节点链 | `chain1` LR 横排；无行间边 | positive |
| WPC-013 | 同章 4 节点链 | 3+1；子图级边标签含 WP-003→WP-004；源码无跨子图节点边 | positive |
| WPC-014 | A→B 且 A→C | 单子图内两条节点边 | positive |
| WPC-015 | 一章内 1 条链 + 2 独立 | 链子图+`rInd`；组间无边 | positive |
| WPC-016 | 换行图出现 `C --> D` | 判违规 | negative |
| WPC-017 | 使用 `~~~` | 判违规 | negative |
| WPC-018 | 子图缺隐形 style | 判违规 | negative |
| WPC-019 | 仅子图级边变化 | 指纹不变、不因排版边重写 generated_at | regression |
| SKG-013 | Skill 已包含该能力且旧文档在 | `status=deprecated`；index 已废弃；不新开当新缺口 | positive |
| SKG-014 | Skill 已包含且用户已删旧文档 | 不动作、不重建 | negative |
| SKG-015 | 落盘/原位后回复 | 一句话含路径+记了什么+历史是否在文中 | positive |
| SKG-016 | 90 日前同指纹未并入 | 原位迭代，不因超 7 日新开 | positive |
| SKG-017 | 周报多轮修改 | 仍可 `revisions/rev-NNN.md` | regression |
| SKG-018 | 新缺口文 | 有 status/updated_at/第八节 | positive |
| WPS-013 | 功能点 预演→测试 | 当前行阶段=测试；留痕追加一行；含执行人与来源 TD | positive |
| WPS-014 | 功能点当前表出现执行人列 | 违规（S6） | negative |
| WPS-015 | 问「谁做过预演」 | 读留痕 | positive |
| WPS-016 | 存量 `## 3b.` | 运行时视为 WP §3（功能点） | positive |
| RN-005 | PM 本轮已裁定并落地 | 对外不列出已裁定事项表；一句「已按你说的做完」 | negative |
| RN-006 | 落地后仍有 4 条未绑定 | 「等你裁定」只含这 4 条，整轮一次；不与已办结混表 | positive |
| RN-007 | 同一轮输出两份「等你裁定」 | 失败 | negative |
| RN-008 | 用户问「改了哪些文件」 | 才给路径清单 | positive |
| RN-009 | 开放行之和 N=0 | 不输出「等你裁定」横幅 | negative |

## 75. 百科叠层 / 跳版本 / 纠偏 / 粒度（v3.21.0）

施工只认合计 **807**（777+30）。阻断项：SK-002、TW-003、SP-001、ALI-003、UPD-002、COR-001、COR-004、COR-005、SCH-001、BRN-003（另沿用 WPS-014/015/016/007）。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SK-001 | 工作区 3.18.0 + schema 0.16.0 + Skill 3.21 | 不要求先装 3.19；不升 schema；首次 P-VIEWS 懒建 | positive |
| SK-002 | 缺 brain/journal | 健康检查不列 P0 | regression |
| SK-003 | 3.21 工作区 + 3.20 Skill | 只读降级，不删派生文件 | regression |
| SK-004 | get_capabilities_since(3.20.0) | 含 encyclopedia_overlay 且 new_dirs=[] | positive |
| TW-001 | 有 Python，写 WP | index/图/brain 由脚本更新 | positive |
| TW-002 | 无 Python | AUTO 读 view-spec；查询声明无快照 | positive |
| TW-003 | 单视图写失败 | 该视图 failed，已 replace 的保留 ok，无半文件 | negative |
| TW-004 | --all 中途 chart 失败 | index 若已 ok 则保留；chart stale | negative |
| SP-001 | --check-spec | index/§3 表头==view-spec==模板；chart 指纹键一致；改乱表头 fail | positive |
| BRN-001 | 有 Python 进工作区 | 指纹变才写 brain | positive |
| BRN-002 | 指纹未变 | 不重写 | regression |
| BRN-003 | 「注销国庆包现在怎样」 | 先 brain；L0+指针；不载 00 | positive |
| BRN-004 | 无 Python / 脚本失败 | 读 WP 原文；声明可能过期 | negative |
| BRN-005 | 无 brain 文件 | 退回 3.20 定向读，不致命 | regression |
| ALI-001 | 「农专注销 90%」 | term 两跳+注销收口 → WP-20260827-001；fixture 含农民专业合作社 | positive |
| ALI-002 | 废弃 WP-001 | 跳总包，不在废弃包建 TD | regression |
| ALI-003 | 对不上活实体 | 问，不建 WP/TD | negative |
| UPD-001 | 日报进度句 | 更新已有 TD，不建 WP | positive |
| UPD-002 | 未点名新模块 | 禁止建 WP | negative |
| COR-001 | 「WP-073 不是开发是联调」 | 写 WP 留痕+journal correction；不进八块 | positive |
| COR-002 | 「联调完成≠开发完成」 | 写词库 §2；JSON 仅投影 | positive |
| COR-003 | 只改 brain | 禁止 | negative |
| COR-004 | 写 active-entities.corrections | 无此槽，失败 | negative |
| COR-005 | AI 自检 80% vs 95% | 进 pm-decisions，不当已确认 | positive |
| DEP-001 | 「现在怎样」 | L0/L1 | positive |
| DEP-002 | 「展开/为什么」 | L2 | positive |
| DEP-003 | 「列出来/周报/对比」 | L3 | positive |
| JRN-001 | 粘贴入库 | 追加 J-，不改历史 J | positive |
| JRN-002 | 无 journal 目录 | 懒建 logs/journal | positive |
| SCH-001 | 升级后版本 | schema 0.16.0；skillVersion 3.21.0；Portfolio 行为不变 | regression |

## 76. 会议快路径 / 结转脚本定位 / 误拆检测（v3.22.0）

施工只认合计见文末统计。阻断：MTG-001、MTG-002、MTG-003、MTG-004、CO-S20、CO-S21、CO-S22、CO-S10、SF-001、BS-022、MIG-001、MIG-002。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| MTG-001 | 腾讯会议 docx +「整理/拆解记录」 | 走 WF-3；不加载 split-rules；不写 sources/ | positive |
| MTG-002 | 合同/需求规格 +「拆文件」 | 仍 P-SPLIT 六件套 | regression |
| MTG-003 | 会议含 T-A4，今天未结转 | 先有 meetings/ 文件，再跑包内脚本，再 inbox | positive |
| MTG-004 | 会议无正式行动项 | 不 Step 0、不建今天 todos | negative |
| MTG-005 | 2 万字转写 + 文末结构化纪要 | 用文末结构；不建 atoms 六件套 | positive |
| CO-S20 | cwd=项目根，技能包在别处 | 调用包内 carryover_step0.py；不手搓 | positive |
| CO-S21 | §1 标题在、表空，上一日有表 | 回退上一日；人数>0；stdout 有 ROSTER_FALLBACK | positive |
| CO-S22 | 两日都无表 | FAIL:ROSTER_EMPTY；exit 2；不造全员空文件 | negative |

## 77. 查询派生定位 / 口低证高（v3.22.0）

阻断：QL-001、QL-002、QL-003、QL-004、QL-005、QL-007、BRN-003、ALI-001、TG-001、TG-002、TG-003、RN-003。非阻断：QL-006、TG-004、RN-010/011。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QL-001 | 新会话问「住所核验国庆上线哪些地市」类（fixture 有 SRC meta 标题） | 先 refresh_views；alias 命中；事实文件 ≤3；不 glob 100+；不读 backup/ | positive |
| QL-002 | 事实已变、brain 仍旧 | 必须先重建再答；禁止用旧 brain 结论 | negative |
| QL-003 | 用户说「把定位关系写进 wps/_index」 | 写词库 alias 待确认或拒绝手改 index；随后 P-VIEWS | negative |
| QL-004 | 上一对话已答过同一句，本轮未实读 | 不得用上轮正文当证据；须走 alias+实读 | negative |
| QL-005 | 查询日 inbox 非空 | 不 C'、不 Step 0；可 HINT 一行 | negative |
| QL-006 | 仅 sources/meta 有标题「住所核验」 | alias 仍能指到 SRC | positive |
| QL-007 | 同一会话已答过；磁盘事实已改 | 第二问必须发现 stale、重建后再答 | negative |
| TG-001 | 只读问「sds 干不干」，模型自推网关 | 本轮标推测；不写词库/journal；可 SUGGEST 一批 | negative |
| TG-002 | 用户说「80% 有道理」 | 不升 confirmed | negative |
| TG-003 | 「zwww 就是政务外网，写进词库」 | T1 → confirmed 或先 pending；有 Source | positive |
| TG-004 | 查询轮一次冒出 10 个缩写 | 只一张 SUGGEST ≤7，不自动 pending 10 条 | negative |
| MIG-001 | dry-run 遇到会议类 SRC | 只打印清单，不搬不删 | positive |

## 78. 确认收口 / 视图消费（v3.23.0）

阻断：CFM-001、CFM-003、CFM-004、ENT-002、ENT-003、NEG-001、NEG-002、PW-006。基线官方口径 830 + 本模块 25 = **855**。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CFM-001 | 新建待办 normal | `auto`；不进块 8 子节 1；横幅不 +1 | positive |
| CFM-002 | 结转 / 进度微调 | 同 CFM-001 | positive |
| CFM-003 | 关风险/改里程碑 | 确认前不写 | regression |
| CFM-004 | DF-013 日报已完成 | 与 V3-021 新期望相同 | positive |
| CFM-005 | strict 下新建待办 | 同 3.22：待确认 + 子节 1 | negative |
| CFM-006 | auto 出现在块 8 子节 1 | D11 失败并重建该子节 | negative |
| CFM-007 | 处理轮有须裁定项 + 同时问进度 | 进度照答；清单不挡 | positive |
| CFM-008 | 纯查询 N>0 | 一行提示，不铺编号清单 | positive |
| ENT-001 | refresh --all | entities 紧凑 JSON；有 entity_count/alias_count；.state 仍 indent | positive |
| ENT-002 | 简单查询 | 不打开 active-entities.json 全文 | positive |
| ENT-003 | term 两跳 | 仍命中，允许为此打开 entities | regression |
| ENT-004 | 决策标题查询 | alias 能指到 D-；再实读 decision-log | positive |
| ENT-005 | 需求标题查询 | alias 能指到 REQ- | positive |
| ENT-006 | 未中别名 | 走 05 §2 单文件；禁止 glob ai/ | negative |
| SES-001 | 「上次聊什么」 | brain 最近过程；声明非事实源 | positive |
| SES-002 | 无 ops | 不报错；最近过程空 | negative |
| SCN-001 | 「当前有哪些风险」 | 走 §2 打开 risk-register，不要求 memo | regression |
| POR-001 | 进度总览 | 每项目 as-of；仍读 _index | positive |
| POR-002 | 包内无 portfolio/cache | 无该目录 | negative |
| NEG-001 | 无 query-index/memo/cold/session-log | 无 | negative |
| NEG-002 | 禁止全库语义扫原文仍在 | 00 P-RESOLVE 仍禁止 | regression |
| NEG-003 | grep 运行时「低/中风险」与「待确认」同线 | 仅 strict/必须确认/历史说明 | negative |
| NEG-004 | grep `AUTO(pending)` 于 references/ | 过程性步骤已去 pending | negative |
| NEG-005 | 「登记 pm-decisions」出现在直接落库语境 | 不得残留；历史日 §0.6 回写五处豁免 | negative |
| NEG-006 | 人工复核 00 §9 各 WF 类型列 | 与 §3.3 一致 | negative |
| MIG-002 | 无 `--migrate-business` | 零写盘 | regression |
| RN-010 | 查询后宿主弹「执行此方案」 | 正文拆穿误弹 + 已有中文结论 | positive |
| RN-011 | 中途确认 | 必须带已做/对象/后果 | positive |

## 74. 分工矩阵 / 挂包先验 / 完整表 / 弱结构投喂（v3.20.0）

施工只认合计 **777**（729+48）。表中 WPS-007/014/015/016 为既有引用不另加。阻断项：WPS-014/015/016/007、WPR-023/024/027/031、IDX-12、BND-001/002/004、FIL-001、DSP-002、ING-005、ING-006。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WPR-023 | 点名多实体×角色 | 写入 §3c；当前表仍无执行人列；同回合 §6 有行 | positive |
| WPR-024 | 简单包未点名 | 无 §3c | negative |
| WPR-025 | 问「内资谁负责」且有 3c | 读矩阵（走 §6.8） | positive |
| WPR-026 | 问「内资当前谁在做」 | 仍 TD Owner | regression |
| WPS-014 | 当前表出现执行人列 | 仍违规 | regression |
| WPS-015 | 问谁做过预演 | 仍读留痕 | regression |
| WPS-016 | 存量 `## 3b.` | 仍当功能点，不当分工矩阵 | regression |
| WPS-007 | 两功能点不同人、阶段=开发 | §8 聚合；当前表无人名列；3c 不参与 SCAN | regression |
| WPR-027 | SCAN 后 3c 人名被改成 Owner | 违规 | negative |
| WPR-028 | 存量 `## 3c. 分工矩阵` 含测试列、无确认人列 | 改正式标题；测试列保留；**不补确认人列** | positive |
| WPR-029 | 角色列增「运维负责人」 | 允许 | positive |
| WPR-030 | 无 3c 问「谁负责」 | 说明无点名分工；降级 TD 须标进度口径 | positive |
| WPR-031 | 改 3c 人名不写 §6 | 8c.2 标未完成，不得只交表 | negative |
| WPR-032 | 存量 3c 标题含分工、仅前端/后端两列 | 认迁；不补测试/产品/确认人 | positive |
| WPR-033 | `## 3c. 其它附表`（标题无分工/RACI/负责人） | 不改标题 | negative |
| IDX-12 | 读 06 L279 与 §7.4 | 均写 12 列 | regression |
| BND-001 | 周贤虎日报「内资预演过了」；仅一包 3c 前端=周贤虎 | 高置信绑该 WP；映射或新建恰好 1 条；备注阶段优先预演 | positive |
| BND-002 | 同上但 3c 里周贤虎在 14 实体且句子无实体名 | 不得猜实体；问一次或待归属；禁止建 14 条 | negative |
| BND-003 | 无 3c，§8 开发🔄含周贤虎仅一包 | 仍可绑该包（降级 §8） | positive |
| BND-004 | 日报把周贤虎写进 3c | 违规 | negative |
| BND-005 | C(P) 两个包均命中「注销」 | 问一次，不自动挑 | positive |
| FIL-001 | 映射要求把 §8 13 站全填 | 违规 | negative |
| FIL-002 | C(P) 空、汇报够正式 | SUGGEST 最小一格一次问；禁止请填 13 站 | positive |
| LRN-001 | 已确认 3c 周贤虎=内资前端，再报「内资」 | 自动绑，不再问补表 | positive |
| OWN-001 | 3c 前端=周贤虎、功能点阶段=预演 | 其当日 §0.7 有该行，阶段=预演 | positive |
| OWN-002 | 只改个人 §0.7 阶段为测试 | 违规；须改 WP §3 | negative |
| OWN-003 | T+1 新日文件 | §0.7 重算不拷昨日表 | positive |
| OBS-001 | 投喂「周贤虎内资预演过了」 | 回执含人/事项/文件路径/WP 或 TD | positive |
| OBS-002 | 问「国庆包现在怎样」 | 功能点全表+阶段+上一站；不得只给三句摘要 | positive |
| OBS-003 | 确认落地后 N=0 | 仍不回放已裁定表（D9 保留） | regression |
| ISS-001 | 「张三卡在预演过不了」 | 先写问题待确认+回执请认 | positive |
| ISS-002 | 「担心以后可能延期」 | 判定卡，不静默登风险册 | negative |
| MIG-B2 | 存量 ## 3c 分工矩阵无确认人列 | 只改标题不补列 | positive |
| HST-001 | 待办办结 | WP §4c 追加一行含 TD/Owner/阶段 | positive |
| HST-002 | 问「这包以前谁推过」且 §4c 有行 | 读档案，不扫全年 todos | positive |
| FED-001 | 只贴日报无「记录一下」 | 入库+回执，不问要不要记住 | positive |
| FED-002 | 「先别写，这包现在怎样」 | 不入库，出完整进度表 | negative |
| AMB-001 | 仅有 ## 3b. 无 ## 3. | 仍当功能点读，并提示/迁标题 | positive |
| DSP-001 | 集层一份混报，两人各一项目、花名册+项目名命中 | 拆成两段高置信；先 ingest 再写 portfolio 分发稿；不写成员 | positive |
| DSP-002 | 用户要集层直接改两个项目 todos | 拒绝 | negative |
| DSP-003 | 一句同时像两个项目且分差 <2 | 必问，不双写 | positive |
| ING-001 | 集层丢无完整表头的进度 xlsx | 入库+回执；不问要不要记住；原件落 `ai/portfolio/reports/ingest/{batch}/` | positive |
| ING-002 | 首行有岗位/角色词；某列值能撞 project-index；空格可 fill-down | 角色槽自动认；空格继承后仍归该项目 | positive |
| ING-003 | 第二次列序不同但指纹命中且行键相同 | 只更新备注/角色人，不新建 WP | positive |
| ING-004 | 单元格值既不像目录名也不在 scope=project 别名 | 回执未挂项目，一次选项 | negative |
| ING-005 | 集层要求直接改成员 todos | 拒绝 | negative |
| ING-006 | 集层投无表头跨项目表 | 原件+全表 rows.md 仅落 `reports/ingest/{batch}/`；映射落 `context/ingest-maps.md`；成员 sources 须「收下」才写；禁止 `portfolio/batches/`；禁止 Portfolio 直写 `projects/*/ai` | positive |
| MAP-001 | 首次槽位确认后同指纹再投 | 不问列 | positive |
| COD-001 | 投仓库路径 | 建 source_code 指针；不刷 REQ 实现视图 | positive |
| ING-007 | 一列高重复不像 WP 名，另一列能最长命中 index | 用能命中的当 wp/feature，分组列不当 WP | positive |
| ING-008 | 领域词库「甲/乙」表示从属 | 不得把乙行并进甲项目 | negative |
| ING-009 | 项目单元格与 index 差一字 | 建议最近成员+一次别名，不拆成多个项目 | positive |

## 79. V-14 拆分硬闸 / 开发仓升级协议（v3.23.1）

施工只认合计 **867**（855+12）。SKILL.md 增路由行属核心契约：本模块 12 条 + DSP-001～003 + V3-010 按新/既有期望；其余 841 条 pass-through，发布仍跑全套。阻断项：DSP-002、DSP-004、DSP-005、DSP-006、UG-001、UG-002、UG-005、UG-006、UG-007、UG-008。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DSP-004 | 集层贴 3～4 人、含项目名的昨天混报，「补昨天日报」 | 归属仍可高置信；本轮不得打开早于锚点的个人待办全文或旧分发稿；只写 portfolio 分发稿 | positive |
| DSP-005 | 目标日无该人文件，最新合法日 `_index` 有未办结计数 | +1 最多再读这一份；打开第二份更早的待办全文 = 失败 | negative |
| DSP-006 | 与 DSP-001 相同（两人各一项目、花名册+项目名） | 仍两段高置信；门槛 ≥5 / 差≥2 / C(P) 未被删 | regression |
| DSP-007 | 拆分回合对外正文 | 有人/项目/置信/落点；无「扫描了 8 月××待办」类过程叙述 | regression |
| UG-001 | 开发仓只说「你是 Agent A」+ 升级需求，不贴提示词 | 加载工作区 16 + dual-agent；先做工作区确认；不向用户要外置提示词 | positive |
| UG-002 | 业务仓（无 16 号文件）说「你是 Agent A，写升级方案」 | 停止升级施工，提示打开开发仓；不开始改 Skill | negative |
| UG-003 | 业务仓「技能做不到 / 记一个升级需求」 | 仍走 skill-gap，不加载 dual-agent | regression |
| UG-004 | 分发包 / pack dry-run | zip 内无 `16-skill-governance-rules.md` 也无 `16-upgrade-dual-agent.md` | regression |
| UG-005 | 开发仓「你是 Agent A」出方案 | 输出含提示词规定全部章节标题；禁止只有自由散文 | positive |
| UG-006 | 「你是 Agent A」+ 需求，不报目标版本 | A 按 16 号 §10 给出建议版本并写入 AP-7/文件名；不得把「请先告诉我升到几」当作开干前提 | positive |
| UG-007 | 「你是 Agent B1，审核 upgrade-plan-vX.md」 | 只在该 AP 文末写/更新 `## B1 审核结果`；A 正文与其他 B 节不改；节内含 #0～#11 与四档结语 | positive |
| UG-008 | 已有 B1 节时「你是 Agent B2」 | 只新增/更新 `## B2 审核结果`；不改 B1、不改 A | negative |

## 80. 投喂默认落库（v3.24.0）

施工只认合计 **877**（867+10）。SKILL.md 路由增行属核心契约：本模块 10 条 + DSP-001/FE-008 按加强期望；其余按既有期望，发布仍跑全套。阻断项：ING-010、ING-012、ING-013、ING-015、DSP-002、DSP-004、DSP-006、UG-001、UG-002、UG-005、UG-006。

| Case ID | Input | Expected | Type |
|---|---|---|---|
| ING-010 | 集层粘贴 6 人「近期人员安排」（请假/释放/承接），不说「入库」 | 写 ingest 原件+rows+当日 logs；回执先报已存入；不得问要不要落库 | positive |
| ING-011 | 同上 | 对外白话 N 件事+项目+编号；对内 V-9 指向各项目 `_index` §1 及/或个人 §0.5；不写 `projects/*/ai` | positive |
| ING-012 | 「各项目进度怎么样」无材料 | 不新建 ingest batch | negative |
| ING-013 | 人员排期投喂后助手正文 | 不得出现「要不要落库」「要不要记住」「摘要要不要写入」 | negative |
| ING-014 | 投喂无法分类的材料且规则盖不住 | 已 ingest；主动问是否记升级需求；未点头不新建 gap 文件 | positive |
| ING-015 | 用户要集层把排期直接写入两项目花名册 | 拒绝；DSP-002/ING-005 同文 | negative |
| ING-016 | 弱结构进度 xlsx | 仍满足 ING-001/006（原件 ingest、不问记住） | regression |
| DSP-008 | V-14 两人各一项目高置信混报 | 本轮有 ingest + 分发稿；低置信才问归属；不问落库 | positive |
| FE-008b | 集层投喂跨项目工时表 | 不写成员 §0.6；有 ingest+日志+V-9（FE-008 加强） | regression |
| EX-013 | examples/13 含人员排期轮 | 对话演示先存 ingest 再拍板，无「要不要落库」 | positive |

## 回归用例统计

| 模块 | 用例数 | 正向 | 回归 |
|---|---|---|---|
| Quick Query | 11 | 8 | 3 |
| Daily Report | 8 | 5 | 3 |
| Weekly Report | 5 | 3 | 2 |
| PM Daily Todo | 3 | 2 | 1 |
| Output Artifact | 6 | 2 | 4 |
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
| Backward Scheduling & Unified Intake (BS) | 24 | 19 | 5 |
| Dual View (DV) | 10 | 5 | 5 |
| Backward Scheduling Daily Matrix (BDM) | 10 | 8 | 2 |
| v3.0.0 Dual-Pack (V3) | 30 | 15 | 15 |
| Daily Report Query Routing (QR-DR) | 3 | 1 | 2 |
| Dev Repo Layout (LG) | 3 | 2 | 1 |
| AI Reply Provenance (PM) | 3 | 2 | 1 |
| Habit Auto-Detect (PH) | 3 | 2 | 1 |
| Linked Todos (TD) | 3 | 2 | 1 |
| Work-log TD Ref (WL) | 3 | 2 | 1 |
| Abbreviation Governance (AB) | 4 | 3 | 1 |
| Report Stub / Timeline (ST) | 6 | 4 | 2 |
| WP Independent Storage (WP) | 5 | 4 | 1 |
| WP Consistency (WC) | 3 | 2 | 1 |
| WP Auto-Bind (AI) | 3 | 2 | 1 |
| Pending Push (PU) | 3 | 2 | 1 |
| WP Source Trace (WS) | 3 | 2 | 1 |
| Source Doc Decompose (SD) | 6 | 3 | 3 |
| Source Split Enhance (SD-1xx) | 13 | 8 | 5 |
| Entity Registry Retired (ER) | 7 | 4 | 3 |
| Risk Issue Restructure (RJ) | 10 | 7 | 3 |
| v3.8.0 Personnel/Confirm/Cost (PC) | 10 | 6 | 4 |
| v3.9.0 过程日志/分片/映射/需求链路/打包 | 53 | 19 | 34 |
| v3.10.0 对话日志/能耗入库/全员建档/TD/时间盒 | 27 | 13 | 14 |
| WP Status History & Stage (WSH) | 18 | 13 | 5 |
| Glossary Sensing (GLS) | 9 | 6 | 3 |
| Output Path Guard (OPG) | 7 | 4 | 3 |
| Plan Template (PLT) | 10 | 6 | 4 |
| Plan/WP Projection (PWP) | 11 | 7 | 4 |
| 派活/基数/时间盒 (DS/CO) | 13 | 6 | 7 |
| 拆文件入库 (SF) | 6 | 2 | 4 |
| 结构/轻量查询 (LQ) | 8 | 4 | 4 |
| WP联动/生效/时间窗/缺口 (WPL/PFA/SG) | 37 | 23 | 14 |
| 阶段/目录/编号/看计划 (STP) | 12 | 8 | 4 |
| 格式/责任链/派生图 (FMT) | 19 | 10 | 9 |
| 工作包记录/图/查询/盖章/阶段 (WPR) | 22 | 13 | 9 |
| 图分章/结构闸/归档/结转/问答 (WPC/WPS/ARC/CO-S/RN) | 64 | 36 | 28 |
| 图拓扑/缺口生命周期/留痕/确认对外 (73) | 23 | 14 | 9 |
| 分工矩阵/挂包/完整表/弱结构投喂 (74) | 48 | 31 | 17 |
| 百科叠层/跳版本/纠偏/粒度 (75) | 30 | 17 | 13 |
| 会议快路径/结转脚本/误拆 (76) | 8 | 5 | 3 |
| 查询定位/口低证高 (77) | 15 | 6 | 9 |
| 确认收口/视图消费 (78) | 25 | 16 | 9 |
| V-14硬闸/升级协议 (79) | 12 | 5 | 7 |
| 投喂默认落库 (80) | 10 | 5 | 5 |
| **合计** | **877** | **515** | **362** |
