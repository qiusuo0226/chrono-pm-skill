# Source Type Registry（源类型登记册）

> 项目级可扩展配置（CR-20260813-001）。用于声明本项目遇到的**所有源文档类型**及其权威层级，
> 支撑跨源需求归集（07 号 §8）。`source_category` 固定 6 类不可改；`source_type` 可随项目追加。
> **追加时须同步**：更新本表 + 受影响 ATOM 的 source_type/category/authority + L1/L2 索引（原子操作，任一失败整体回退并标记 stale）。

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

| source_type | source_category | 说明 | authority | 覆盖默认？ | 示例/备注 |
|---|---|---|---|---|---|
| contract | contractual | 合同正文 | L1 | 否 | 含主合同 |
| supplement | contractual | 补充协议 | L1 | 否 | 合同变更 |
| tender_doc | procurement | 招标文件 | L2 | 否 | 含补遗/答疑 |
| bid_doc | procurement | 投标文件 | L2 | 否 | 投标承诺 |
| tender-source | procurement | 投标文件拆解产物目录 | L2 | 否 | `requirements/tender-source/` |
| initiation | approval | 立项批复 | L3 | 否 | 可研/建议书 |
| security_req | compliance | 密评/等保 | L4 | 否 | 强制门禁 |
| security-assessment-source | compliance | 密评拆解产物目录 | L4 | 否 | `requirements/security-assessment-source/` |
| expert_review | technical | 专家评审意见 | L3 | 否 | - |
| design_spec | technical | 需求规格说明书 | L3 | 否 | 甲方侧需求规格；与开发侧 design_doc 语义不同（07 号 §8.10.2） |
| dev_prd | technical | 开发需求文档/PRD | L3 | 否 | 开发侧，不参与 scope_scope（07 号 §8.5） |
| design_doc | technical | 概要/详细设计文档 | L3 | 否 | 开发侧"怎么做"，区别于甲方侧 design_spec |
| api_spec | technical | 接口文档/API 说明 | L3 | 否 | 开发侧 |
| prototype | technical | 交互原型/线框图 | L3 | 否 | 非文本载体，存指针（07 号 §8.10.3） |
| ui_spec | technical | UI 标注稿/视觉规范 | L3 | 否 | 开发侧 |
| meeting_directive | operational | 甲方指令性纪要 | L3 | 是（→L2） | 甲方高层签发 |
| milestone_clause | operational | 工期/里程碑条款 | L5 | 否 | 权威 L5 |

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
