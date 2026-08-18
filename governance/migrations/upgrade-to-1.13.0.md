# 升级到 1.13.0

> 从 1.12.0 升级到 1.13.0
> 发布日期：2026-08-12
> Schema 变更：无
> CR 编号：CR-20260812-001

## 变更摘要

架构精简改造(CR-20260812-001, Minor)：A 线实体级联嵌入(6 实体规则文件新增§级联传播规则 AUTO/CHECK/SUGGEST + 00 号§8 级联冲突处理)；B 线文件膨胀治理(06 号§9 通用归档表操作化 + decision-log/transfer-log/issue-register 拆分行 + 02/09 号归档规则 + 15 号§15 与 11 号§16 存储生命周期 + 01 号§5.8 通用归档检查)；C 线索引派生分级(14 号§2.4 完全派生/增量维护/独立累积 + D13/M8/R7)；D 线版本同步收口(新增 scripts/sync_version.py 自 _version.py 同步四触点)；E 线 Blueprint 瘦身(§5.3/§9.1/§11.3 指针化+1.13.0 行)；新增 assets/templates/decision-log-template.md；回归套件新增 Module 29(CP-001~006)/Module 30(AG-001~006)，总计 179 用例

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.13.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.13.0）


## CHANGELOG 摘录

## 1.13.0 — 2026-08-12（已发布 · released）

> 发布归档：CR-20260812-001（架构精简改造）。覆盖 5 条改造线：实体级联嵌入、文件膨胀治理、索引派生分级、版本同步收口、Blueprint 瘦身。基线快照见 `governance/baselines/1.13.0/`，回归见 `governance/regression-reports/rr-20260812-1.13.0.md`。

### Added
- **A 线 · 实体级联嵌入**：6 个实体规则文件新增 `§级联传播规则`（03 §8、04 §9、07 §7、08 §9、09 §8、02 §6），声明实体状态变更后 AUTO（写派生视图）/CHECK（只读校验）/SUGGEST（写事实源待确认）三类下游动作；00 号新增 §8 级联冲突处理；AUTO 作用域限定非事实源的派生视图（受 `skill-contract.md` 第 5 条约束）。
- **B 线 · 文件膨胀治理**：06 号 §6.2 新增 decision-log/issue-register/transfer-log 拆分行，§6.3 新增持续拆分模式，§9 归档规则操作化为通用归档表（实体/触发/目标/索引）；02 号新增 decision-log 归档规则；08 号归档粒度改为纯条数触发+归档索引；09 号新增 transfer-log 归档 + resource 生命周期；01 号 §5.8 扩展为通用归档检查；15 号新增 §15 存储生命周期；11 号新增 §16 存储生命周期。
- **C 线 · 索引派生分级**：14 号新增 §2.4 索引派生分级（完全派生 AUTO / 增量维护 / 独立累积）；§2.2 加"实体级联完成后"维护项；D13/M8/R7 级联完整性自查项。
- **D 线 · 版本同步收口**：新增 `scripts/sync_version.py`（自 `_version.py` 单一源同步 VERSION/SKILL.md/skill.json）；release-checklist 新增运行检查。
- **E 线 · Blueprint 瘦身**：§1 版本行、§5.3 分布、§9.1 稳定能力、§11.3 结构变更改为指向单一事实源或 CHANGELOG；§7.2 补充级联依赖声明说明。
- 新增模板 `assets/templates/decision-log-template.md`（决策日志此前无模板）。

### Changed
- 版本 1.12.0 → 1.13.0（Minor）；Workspace Schema 保持 0.6.0（无迁移）。
- SKILL.md §15 规则索引为 6 个实体文件补充级联传播说明。

### Regression
- 回归套件新增级联传播场景用例；全量回归见 rr-20260812-1.13.0.md。

### Risk
- **contract_change**：00-pm-main-rules.md 新增 §8 级联冲突处理（检测 CHECK/SUGGEST 结果与上下文矛盾，标记 ⚠ 级联异常交 PM 决策，不自动解决）。
- **AUTO 作用域约束**：所有 §级联传播规则声明 AUTO 仅作用于非事实源的派生视图（todo 索引/各类派生 index），事实源写入一律受 `skill-contract.md` 第 5 条约束。

---
