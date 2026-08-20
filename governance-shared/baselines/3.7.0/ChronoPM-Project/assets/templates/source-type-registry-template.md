# Source Type Registry（源类型登记册）

> 项目级可扩展配置（CR-20260813-001）。用于声明本项目遇到的**所有源文档类型**及其权威层级，
> 支撑跨源需求归集（07 号 §8）。`source_category` 固定 6 类不可改；`source_type` 可随项目追加。
> **追加时须同步**：更新本表 + 受影响 ATOM 的 source_type/category/authority + L1/L2 索引（原子操作，任一失败整体回退并标记 stale）。
> **v3.6.0**：下表为全生命周期基线包。新工作区 Step1 多选启用；存量升级**按需启用、不预灌**。清单外类型追加一行即可。拆解产物落 `requirements/sources/{编号}/`，禁止新建 `{type}-source/`。

## Source Category（固定 6 类，不可扩展）

| source_category | 语义 | 默认 authority |
|---|---|---|
| contractual | 合同/协议类 | L1 |
| procurement | 招投标类 | L2 |
| approval | 立项审批类 | L3 |
| compliance | 合规标准类 | L4 |
| technical | 技术文件类 | L3（基线化后） |
| operational | 运维约定类 | L2-L3（工期/里程碑条款默认 L5） |

## Registry（项目级可扩展，初始化向导 Step1/Step2 引导建立）

| source_type | source_category | 说明 | authority | 启用？ | 示例/备注 |
|---|---|---|---|---|---|
| contract | contractual | 合同正文 | L1 | 是 | 簇前缀 CON- |
| supplement | contractual | 补充协议 | L1 | 是 | 合同变更 |
| nda | contractual | 保密协议 | L1 | 否 | 按需启用 |
| integrity_pact | contractual | 廉政协议 | L1 | 否 | 按需启用 |
| performance_bond | contractual | 履约保函 | L1 | 否 | 按需启用 |
| tender_doc | procurement | 招标文件 | L2 | 否 | 含补遗/答疑 |
| bid_doc | procurement | 投标文件 | L2 | 否 | 投标承诺 |
| award_notice | procurement | 中标通知 | L2 | 否 | 按需启用 |
| clarification | procurement | 澄清函 | L2 | 否 | 按需启用 |
| addendum | procurement | 补遗 | L2 | 否 | 按需启用 |
| initiation | approval | 立项批复 | L3 | 否 | 可研/建议书 |
| feasibility | approval | 可研报告 | L3 | 否 | 立项前期 |
| proposal | approval | 项目建议书 | L3 | 否 | 立项前期 |
| quotation | approval | 报价单 | L3 | 否 | 立项前期 |
| charter | approval | 项目章程 | L3 | 否 | 规划启动 |
| mgmt_plan | approval | 管理计划 | L3 | 否 | 规划启动 |
| security_req | compliance | 密评/等保 | L4 | 否 | 强制门禁 |
| expert_review | technical | 专家评审意见 | L3 | 否 | - |
| design_spec | technical | 需求规格说明书 | L3 | 否 | 甲方侧；与 design_doc 不同（§8.10.2） |
| srs | technical | SRS | L3 | 否 | 需求设计 |
| db_dict | technical | 数据库字典 | L3 | 否 | 需求设计 |
| dev_prd | technical | 开发需求文档/PRD | L3 | 否 | 不参与 scope_scope（§8.5） |
| design_doc | technical | 概要/详细设计 | L3 | 否 | 开发侧 |
| api_spec | technical | 接口文档 | L3 | 否 | 开发侧 |
| prototype | technical | 交互原型 | L3 | 否 | 存指针（§8.10.3） |
| ui_spec | technical | UI 标注/视觉规范 | L3 | 否 | 开发侧 |
| meeting_directive | operational | 甲方指令性纪要 | L3 | 是（→L2） | 甲方高层签发 |
| milestone_clause | operational | 工期/里程碑条款 | L5 | 否 | 权威 L5 |
| wbs | operational | WBS | L3 | 否 | 开发实施 |
| deploy_manual | operational | 部署手册 | L3 | 否 | 开发实施 |
| oss_compliance | compliance | 开源合规清单 | L4 | 否 | 开发实施 |
| test_report | operational | 测试报告 | L3 | 否 | 测试 |
| defect_list | operational | 缺陷清单 | L3 | 否 | 测试 |
| cutover | operational | 上线割接 | L3 | 否 | 上线试运行 |
| trial_run | operational | 试运行报告 | L3 | 否 | 上线试运行 |
| training_material | operational | 培训材料 | L3 | 否 | 簇前缀 TRN- |
| ops_manual | operational | 操作手册 | L3 | 否 | 上线试运行 |
| acceptance_app | operational | 验收申请 | L2 | 否 | 验收 |
| prelim_accept | operational | 初验报告 | L2 | 否 | 验收 |
| final_accept | operational | 终验报告 | L2 | 否 | 验收 |
| asset_handover | operational | 资产移交 | L2 | 否 | 验收 |
| ops_plan | operational | 运维方案 | L3 | 否 | 售后结项 |
| settlement | operational | 结算书 | L2 | 否 | 售后结项 |
| review_report | operational | 复盘报告 | L3 | 否 | 售后结项 |
| archive_list | operational | 归档清单 | L3 | 否 | 售后结项 |
| change_order | contractual | 变更单 | L1 | 否 | 贯穿全周期 |
| correspondence | operational | 函件 | L3 | 否 | 贯穿全周期 |
| signoff | operational | 签字单 | L3 | 否 | 贯穿全周期 |
| supervision_plan | operational | 监理规划 | L3 | 否 | 簇前缀 SUP- |
| supervision_monthly | operational | 监理月报 | L3 | 否 | 监理 |
| witness | operational | 旁站记录 | L3 | 否 | 监理 |
| evaluation | operational | 监理评估报告 | L3 | 否 | 监理 |
| supervision_log | operational | 监理日志 | L3 | 否 | 监理 |
| supervision_rule | operational | 监理实施细则 | L3 | 否 | 监理 |
| meeting_minutes | operational | 会议纪要类源文档 | L3 | 否 | 与 MTG 过程记录区分：本行仅当作为拆解源 |
| ip_agreement | contractual | 知识产权协议 | L1 | 否 | 按需启用 |
| tender-source | procurement | **存量目录别名**（勿新建） | L2 | 否 | 旧 `requirements/tender-source/`，迁入 sources/ |
| security-assessment-source | compliance | **存量目录别名**（勿新建） | L4 | 否 | 旧路径，迁入 sources/ |

## 使用规则

1. 新源文档类型：向本表追加一行（source_type→source_category→authority），并同步受影响 ATOM 与索引。
2. 未知 source_type：输入时触发"未登记"提示（给出候选类别），不静默归类。
3. source_type 必须归入一个固定 source_category，继承默认 authority；`覆盖默认？` 为显式覆盖。
4. **technical 类开发侧文档**（dev_prd/design_doc/api_spec/prototype/ui_spec）：其 ATOM 不参与 scope_scope 范围判定聚合，仅用于填充对应 REQ 的"实现视图"与"原型/文档链接"字段（07 号 §8.5 硬约束 + §8.10 双视图）。
5. Change Log：本表变更记录于底部（追加/修改/删除）。

## Change Log

| 日期 | 操作 | source_type | 变更说明 | 关联 CR |
|---|---|---|---|---|
| - | - | - | - | - |
