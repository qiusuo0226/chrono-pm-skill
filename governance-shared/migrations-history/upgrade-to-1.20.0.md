# 升级到 1.20.0

> 从 1.19.1 升级到 1.20.0
> 发布日期：2026-08-15
> Schema 变更：无
> CR 编号：—

## 变更摘要

需求双视图与开发文档关联(Minor/capability_change)：双 Agent 四轮审核收敛（V0.1→V0.4）。解决合同需求（业务视角）⇄开发需求（实现视角）语义断层：07号新增 §8.10 双视图机制（view_business=business 类 ATOM norm_text 派生聚合不新增字段；view_dev 实现视图+原型/文档链接挂 REQ 层新增 2 可选列，摘要级≤100字）；§8.5 scope_scope 聚合排除硬约束（technical 类 ATOM 不参与范围判定，数据正确性红线）+§8.7 级联 CHECK；§8.6 新增触发 D 开发侧文档提取（模块/接口/页面维度切块，norm_text 保留技术术语）+大文档渐进导入（分批 2000-5000 字断点续导）。source-type-registry 新增 dev_prd/design_doc/api_spec/prototype/ui_spec 五个 technical 类 source_type（L3），design_doc 与 design_spec 边界显式区分。WF-2 需求上下文加载（00/05号，Task→REQ 链路，单次≤10条 REQ 降级不阻塞）+05号需求详情/双视图路由（与范围判定路由显式区分）；17号词库开发侧分类标签示例+分类预筛/懒加载（§5.1a，复用 §12.2 拆分不新增索引）+§6.3a 开发侧术语归一；12号 §1.3 Excel 扩展列 U/V（方案 α，与 O-T 连续）；19号双视图存在性巡检（confirmed REQ 覆盖率 P3 提示，Requirement Ref 存在性 P2，不变相强制必填）；个人/项目日报模板新增关联原型/文档可选节。回归套件新增 Module 37 Dual View（DV-001~010，总计 259，DV-001 为红线用例）。零新增规则文件，requirement-register 23→25 列（均可选），workspace schema 保持 0.8.0 无需迁移。Blueprint Impact full。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.20.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 见下方 CHANGELOG 摘录中工作流相关条目

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.20.0）


## CHANGELOG 摘录

## 1.20.0 — 2026-08-15（已发布 · released）

> 发布归档：Minor（需求双视图与开发文档关联）。双 Agent 审核四轮收敛（V0.1→V0.4，B1/B2 终审放行）。核心升级：解决"合同需求（业务视角）⇄ 开发需求（实现视角）"语义断层——业务视图为 business 类 ATOM norm_text 派生聚合（不新增字段），实现视图与原型/文档链接为 REQ 层新增可选列；WF-2 日报处理按 Task→REQ 链路加载需求上下文，使 AI 能同时理解日报中的业务语言与实现语言。technical 类 ATOM 硬约束排除出 scope_scope 聚合（数据正确性红线）。无 workspace schema 变更（仍 0.8.0），无需工作区迁移；新增字段均为可选，存量工作区向后兼容。

Blueprint Impact: full（WF-2 数据路径 + 双视图能力 + 版本演进表）

### Added
- **需求双视图机制（07 号 §8.10）**：view_business = business 类（contractual/procurement/approval/compliance/operational）ATOM norm_text 派生聚合，查时现算不新增字段；view_dev = 登记册"实现视图"列（摘要级 ≤100 字，挂 REQ 层与 Task→REQ 日报链路对齐）；"原型/文档链接"列存指针，原文档不入库。
- **开发侧 source_type 扩展（source-type-registry）**：dev_prd / design_doc / api_spec / prototype / ui_spec 五个 technical 类类型（authority L3）；design_doc（开发侧）与 design_spec（甲方侧）语义边界显式区分。
- **WF-2 需求上下文加载（00 号/05 号）**：Task 带 Requirement Ref 时读对应 REQ 的功能描述+实现视图+原型链接；单次最多 10 条 REQ，字段缺失降级不阻塞（05 号 §2.5 需求上下文加载规范）。
- **Quick Query 需求详情路由（05 号）**："某需求具体做什么/怎么实现/原型在哪"走 requirement-register，与既有范围判定路由（contract-register）显式区分。
- **词库开发侧支持（17 号）**：类别自由文本补充"模块名/接口名/技术组件"标签示例（§3.1）；分类预筛 + 懒加载性能策略（§5.1a，复用 §12.2 拆分不新增索引）；开发侧术语归一规则（§6.3a）。
- **日报模板可选段**：个人日报/项目日报新增"关联原型/文档（可选）"节，原文档不入库仅记指针。
- **Excel 扩展列 U/V（12 号 §1.3）**：实现视图 + 原型/文档链接，与既有 O-T 扩展列连续。

### Changed
- **07 号 §8.5 scope_scope 聚合排除硬约束**：判定仅由五类 business ATOM evidence 参与，technical 类 ATOM 不参与范围判定，仅填充 REQ 实现视图/原型链接；§8.7 级联新增对应 CHECK 红线。
- **07 号 §8.6 提取流程扩展**：新增触发 D（开发侧文档提取）；technical 类 ATOM 按模块/接口/页面维度原子化切块，norm_text 保留技术术语原样；命中 Canonical 时 SUGGEST 填充实现视图；新增大文档渐进导入（分批 2000-5000 字，source_ref 到章节号支持断点续导）。
- **19 号双视图巡检（存在性校验非强制必填）**：confirmed REQ 的实现视图/原型链接覆盖率作 P3 提示；已填 Requirement Ref 的 Task 校验 REQ 存在性（P2）；Requirement Ref 为可选字段不得变相强制。

### Notes
- 回归套件新增 Module 37 Dual View（DV-001~010，10 用例，总计 259）；DV-001（dev_prd 不污染 scope_scope）为数据正确性红线用例。
- 零新增规则文件；requirement-register 新增 2 个可选列（总览表 23→25 列），旧数据无此列不影响既有功能；workspace schema 保持 0.8.0。
- 方案经四轮 B 审核收敛：V0.1→V0.4；关键决策链：双视图挂 REQ 层（非 Canonical）、view_business 派生不加字段、technical 隔离红线、12 号扩展列方案 α（追加 U/V）。

---
