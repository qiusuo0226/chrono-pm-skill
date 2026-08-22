# Contract Register（合同登记册）

> RI 检索入口事实源（v3.0.0）。本文件为**项目级**合同登记册，位于 `requirements/contract-register.md`。每个项目各一份，不再作为项目集唯一登记册。
> 新建编号：`CON-{YYYYMMDD}-{HHmmss}`；存量旧编号 `CON-NNN` 保留不重编。
> 拆解产物见 `requirements/sources/{编号}/`（本表「拆解文件夹指针」列）；各目录配 `ledger.md`（字段规范见 07 号 §8.9.5）。存量 `{type}-source/` 未迁完时可作 fallback。
> 写入遵循 SKILL.md 底线 #2（待确认 + pm-decisions）：主动变更写入时标记 `Confirmed By: 待确认` 并登记到决策文件，你确认后方视为生效。
> 结构规则见 `references/07-requirement-rules.md` §8.9。

## 合同登记表

| Contract ID | 合同名称 | 合同类型 | scope_level | parent_contract_id | coverage 覆盖对象 | 关联招投标 | 关联立项 | 关联密评 | 拆解文件夹指针 | status | superseded_by | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CON-{YYYYMMDD}-{HHmmss} | （示例）XX信息化建设合同 | 主合同 | project | - | 本项目 | BID-{YYYYMMDD}-{HHmmss} | INIT-{YYYYMMDD}-{HHmmss} | COMP-{YYYYMMDD}-{HHmmss} | requirements/sources/CON-{YYYYMMDD}-{HHmmss}/ | active | - | 合同V1.2首页 |
| CON-{YYYYMMDD}-{HHmmss} | （示例）补充协议 | 补充协议 | supplement | CON-{YYYYMMDD}-{HHmmss} | 本项目 | - | - | - | requirements/sources/CON-{YYYYMMDD}-{HHmmss}/ | active | - | 补充协议V1.0 |

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| Contract ID | 是 | 新建 `CON-{YYYYMMDD}-{HHmmss}`（唯一编码）；存量 `CON-NNN` 保留不重编 |
| 合同名称 | 是 | 合同全称 |
| 合同类型 | 是 | 主合同 / 补充协议 / 分包合同 等 |
| scope_level | 是 | `project`（本项目整体）/ `supplement`（补充协议） |
| parent_contract_id | 补充协议必填（其他填 `-`） | 指向被补充合同；用于 supplement 存储层级回溯（D7） |
| coverage 覆盖对象 | 是 | 本项目；他项目指针见 `project-context` 兄弟项目段 |
| 关联招投标 / 关联立项 / 关联密评 | 否 | 成套文档簇关联（BID- / INIT- / COMP-；新建用 `{YYYYMMDD}-{HHmmss}`） |
| 拆解文件夹指针 | 否 | 本项目 `requirements/sources/{编号}/`（簇固定号或 SRC-NNN） |
| status | 是 | `active` / `superseded` |
| superseded_by | 否 | 合同拆分/替代时的血缘（D8） |
| Source | 是 | 来源合同/文档，可追溯 |

## RI 关联

- **存储归属**：ATOM/Canonical 一律存本项目 `requirements/`（canonical + atoms）；跨项目检索由 ChronoPM-Portfolio 遍历，本 Skill 不在项目 ai 内建 `portfolio/`。
- **检索路由**：RI 范围判定先读本登记册（Step0），依据 scope_level 与 parent_contract_id 定位本项目 canonical。
- **文档簇**：Contract ID 通过关联招投标/立项/密评与拆解文件夹指针形成文档簇，跨源检索时先定位合同再路由。
- **合同变更**：合同拆分/范围调整时维护 status/superseded_by 血缘，并联动 ATOM/Canonical（见 07 号 §8.9.4）。
