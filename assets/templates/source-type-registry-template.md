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
| initiation | approval | 立项批复 | L3 | 否 | 可研/建议书 |
| security_req | compliance | 密评/等保 | L4 | 否 | 强制门禁 |
| expert_review | technical | 专家评审意见 | L3 | 否 | - |
| design_spec | technical | 需求规格说明书 | L3 | 否 | - |
| meeting_directive | operational | 甲方指令性纪要 | L3 | 是（→L2） | 甲方高层签发 |
| milestone_clause | operational | 工期/里程碑条款 | L5 | 否 | 权威 L5 |

## 使用规则

1. 新源文档类型：向本表追加一行（source_type→source_category→authority），并同步受影响 ATOM 与索引。
2. 未知 source_type：输入时触发"未登记"提示（给出候选类别），不静默归类。
3. source_type 必须归入一个固定 source_category，继承默认 authority；`覆盖默认？` 为显式覆盖。
4. Change Log：本表变更记录于底部（追加/修改/删除）。

## Change Log

| 日期 | 操作 | source_type | 变更说明 | 关联 CR |
|---|---|---|---|---|
| - | - | - | - | - |
