# Contract Register（合同登记册）

> RI 检索入口事实源（v1.16.0，CR-20260813-002）。项目集模式唯一登记册在 `portfolio/requirements/contract-register.md`；单项目模式在 `requirements/contract-register.md`。所有主合同与补充协议统一登记，不分子项目复制。
> 写入遵循 SKILL.md 底线 #2（待确认 + pending-changes）：主动变更写入时标记 `Confirmed By: 待确认` 并登记，PM 确认后方视为生效。
> 结构规则见 `references/07-requirement-rules.md` §8.9。

## 合同登记表

| Contract ID | 合同名称 | 合同类型 | scope_level | parent_contract_id | coverage 覆盖对象 | 关联招投标 | 关联立项 | 关联密评 | status | superseded_by | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CON-001 | （示例）XX信息化建设合同 | 主合同 | portfolio | - | PRJ-001, PRJ-002 | BID-001 | INIT-001 | COMP-001 | active | - | 合同V1.2首页 |
| CON-002 | （示例）A子项目补充协议 | 补充协议 | supplement | CON-001 | PRJ-001 | - | - | - | active | - | 补充协议V1.0 |

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| Contract ID | 是 | CON-NNN（唯一编码） |
| 合同名称 | 是 | 合同全称 |
| 合同类型 | 是 | 主合同 / 补充协议 / 分包合同 等 |
| scope_level | 是 | `portfolio`（跨子项目/整体）/ `project`（单个子项目或单项目整体）/ `supplement`（补充协议） |
| parent_contract_id | 补充协议必填（其他填 `-`） | 指向被补充合同 CON-NNN；用于 supplement 存储层级回溯（D7） |
| coverage 覆盖对象 | 是 | 受此合同约束的 PRJ-NNN 列表（单项目模式填"整体"） |
| 关联招投标 / 关联立项 / 关联密评 | 否 | 成套文档簇关联（BID-NNN / INIT-NNN / COMP-NNN） |
| status | 是 | `active` / `superseded` |
| superseded_by | 否 | 合同拆分/替代时的血缘（D8） |
| Source | 是 | 来源合同/文档，可追溯 |

## RI 关联

- **存储归属**：ATOM/Canonical 按 scope_level 决定所在层级（portfolio 级合同→`portfolio/requirements/`；project 级→对应子项目；supplement→**跟随父合同 scope_level**）。
- **检索路由**：RI 范围判定先读本登记册（Step0），依据 scope_level 与 parent_contract_id 定位目标层级 canonical。
- **文档簇**：CON-NNN 通过关联招投标/立项/密评字段形成文档簇，跨源检索时先定位合同再路由。
- **合同变更**：合同拆分/范围调整时维护 status/superseded_by 血缘，并联动 ATOM/Canonical（见 07 号 §8.9.4）。
