# 合同作用域与跨源需求归集扩展方案（Contract Scope for RI）— V0.4

> 版本：V0.4（终审版，B 四轮审核 A 通过）
> 关联：CR-20260813-002（基于 CR-20260813-001 RI 能力的二次扩展）
> 目标：补齐 RI 方案中"合同与子项目多对多映射"架构缺口，新增项目集级 `portfolio/requirements/` RI 存储、`contract-register.md` 合同登记册、按 scope_level 的 ATOM/Canonical 归属、带合同维度的 scope 判定（contract_refs）、四步检索路由、文档簇关联与合同变更三级联动，并修复 CR-001 脚本层遗留缺口。

---

## 一、需求背景与场景枚举

用户原始需求（节选）：当前 RI 方案把 ATOM/Canonical/索引全部放在子项目级 `projects/{子项目}/requirements/`，隐含"合同与子项目 1:1"假设，但现实中是**多对多**关系。关键场景除 1:1 外还包括：合同跨子项目（A/B）、单项目 1 合同覆盖 3 子部分（D）、联合体合同+独立补充协议+跨项目运维合同（E）、主合同+多补充协议变更（F）、子项目被多合同覆盖不同建设内容（G）、单项目多合同分期（H）。招投标/立项/密评等文档与合同成套出现，继承同样的多对多关系。

**4 个盲区**：
1. 合同跨子项目时 ATOM 无处安放（存 A 还是 B？）。
2. 合同覆盖整个项目集时缺 `portfolio/requirements/` 目录。
3. 子项目被多合同覆盖时 scope 判定混乱（场景 G）。
4. 用户以合同为视角提问时 AI 不知去哪个子项目搜。

**CR-001 遗留脚本缺口**（独立复核确认）：
- 项目集模式初始化/迁移不建子项目级 RI 骨架（config SUB_PROJECT_DIRS 无 canonical/atoms、SUB_PROJECT_FACT_SOURCE_FILES 无 source-type-registry）。
- portfolio/ 级无 RI 目录（PORTFOLIO_DIRS 无 requirements）。
- 0.7.0 迁移条目 `new_dirs`/`new_files` 全为单项目路径，迁移框架无子项目遍历机制。
- SKILL.md §4 事实源表缺 RI 文件；description 无"合同"触发词。

## 二、设计决策（V0.4 定稿）

| 编号 | 决策 | 内容 |
|---|---|---|
| D1 | scope_scope 5 值枚举 + contract_refs | 保留既有 5 值（in_contract/in_bid_only/in_initiation_only/not_in_scope/conflict），新增伴随字段 `contract_refs`（Canonical 层），旧 Canonical 缺字段→"未关联合同"降级标注，向后兼容 |
| D2 | Canonical storage_level | evidence 全部同层→归该层；跨层/跨子项目→归 portfolio 级（portfolio 优先） |
| D3 | 单项目多合同 | 不引入 portfolio 目录，复用 `requirements/contract-register.md` + coverage 列 |
| D4 | 项目集登记册唯一性 | 唯一登记册在 `portfolio/requirements/`，子项目不复制，避免双写漂移 |
| D5 | 冷启动 | 空登记册不阻塞但触发补录引导（最小字段：ID/名称/scope_level/覆盖/status），不臆造结论 |
| D7 | supplement 跟随父合同 | supplement 的 ATOM/Canonical 存储与检索跟随**父合同 scope_level**；contract-register 新增 `parent_contract_id` 列（补充协议必填）实现回溯 |
| D8 | 合同变更不改 08 号 | 合同范围变更复用既有 `scope`/`cost`/`requirement` 类型，contract-register 维护 status/superseded_by 血缘，不修改 08 号概念域 B 枚举 |
| D9 | 迁移前向修复 | 0.8.0 条目承载 `sub_project_dirs`/`sub_project_files` 键 + 子项目遍历，不修改 0.7.0 历史条目 |
| D10 | 子项目遍历守卫 | 仅对已存在 `requirements/` 目录的子项目补齐 RI 骨架，避免强建与误扫 |

## 三、contract-register.md 模板（V0.4 定稿）

```
# Contract Register（合同登记册）

> RI 检索入口事实源（v1.16.0）。项目集模式唯一登记册在 portfolio/requirements/；
> 单项目模式在 requirements/。所有主合同与补充协议统一登记。
> 写入遵循 SKILL.md 底线 #2（待确认 + pending-changes）。

## 合同登记表

| Contract ID | 合同名称 | 合同类型 | scope_level | parent_contract_id | coverage 覆盖对象 | 关联招投标 | 关联立项 | 关联密评 | status | superseded_by | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CON-001 | XX信息化建设合同 | 主合同 | portfolio | - | PRJ-001, PRJ-002 | BID-001 | INIT-001 | COMP-001 | active | - | 合同V1.2首页 |
| CON-002 | A子项目补充协议 | 补充协议 | supplement | CON-001 | PRJ-001 | - | - | - | active | - | 补充协议V1.0 |

## 字段说明
- scope_level：portfolio(跨子项目/整体) / project(单个子项目或单项目整体) / supplement(补充协议)
- parent_contract_id：补充协议必填，指向被补充合同；主合同填「-」（D7）
- coverage：受此合同约束的 PRJ-NNN（或单项目整体）列表
- status：active / superseded；superseded_by 记录血缘（合同拆分/替代时）(D8)

## RI 关联
- supplement 的 ATOM/Canonical 存储与检索跟随父合同 scope_level
- Canonical 依据 evidence 的 storage_level 与 contract_refs 判定归属与范围结论
```

## 四、RI 四步检索路由（05 号新增）

```
Step 0  读 contract-register（空 → 触发补录引导：ID/名称/scope_level/覆盖/status）
Step 1  解析合同指向
        ├─ 指定合同（CON-XXX/名称）→
        │     scope_level=portfolio   → 查 portfolio/requirements/canonical
        │     scope_level=project     → 查对应子项目 canonical
        │     scope_level=supplement  → 经 parent_contract_id 回溯父合同 scope_level → 按父合同层级路由（D7）
        ├─ 未指定 → 列合同候选供选择；或"全部范围"→ 逐合同检索合并（N11）
        └─ 登记册空/无匹配 → 提示补录，不臆造（N9）
Step 2  目标 canonical 走 L1→L2→L3 三级索引（单次 200-400 行最小读取）
Step 3  输出 scope_scope(result) + contract_refs + 证据链
        scope_level=supplement 时 → contract_refs 含 supplement 与父合同双 ID
        场景 G 多合同覆盖 → 逐合同列结论
```

## 五、ATOM/Canonical 存储归属矩阵

| 合同 scope_level | ATOM 存在哪 | Canonical 存在哪 |
|---|---|---|
| portfolio（跨子项目） | `portfolio/requirements/atoms/` | `portfolio/requirements/canonical/` |
| project（单个子项目或单项目） | `projects/{子项目}/requirements/atoms/`（单项目 `requirements/atoms/`） | `projects/{子项目}/requirements/canonical/`（单项目 `requirements/canonical/`） |
| supplement（补充协议） | **跟随父合同 scope_level**（D7） | **跟随父合同 scope_level**（D7） |

Canonical storage_level 补充规则（D2）：
- evidence 全部来自同层级合同 → 归该层级；
- evidence 跨 portfolio/project 或多子项目 → 归 portfolio 级，`storage_level=portfolio`；
- Canonical 层新增 `contract_refs`（关联合同 ID 列表），用于带合同维度的 scope 结论输出。

## 六、合同变更三级联动（N14，D8）

| 类别 | ATOM | Canonical | contract-register | 08 号 |
|---|---|---|---|---|
| 合同范围扩大（含补充协议） | 增量提取新增 ATOM(supplement) | 新 ATOM 归并后 scope 重判 | 补充协议登记（parent_contract_id） | 变更走 08 号 `scope`+`requirement` |
| 合同拆分为两份 | 原 ATOM 按新合同归属迁移 | 相关 Canonical 重判 | 旧条 status=superseded、superseded_by=新条；新增 2 条 | 08 号 `scope`+`cost` |
| 合同范围缩小 | 相关 ATOM 标 stale/剔除 | 原 in_contract 的 Canonical 可能变 not_in_scope | 维护 status/血缘 | 08 号 `scope` |

全程遵守 SKILL.md 底线 #2（待确认 + pending-changes）；contract-register 写入走主动变更模式标记待确认，PM 确认后方视为生效。

## 七、脚本层扩展（E 闭合）

- `config.py`：
  - P2：`PORTFOLIO_DIRS` 加 `requirements/canonical`、`requirements/atoms`；`PORTFOLIO_FACT_SOURCE_FILES` 加 `requirements/contract-register.md`（→contract-register-template）与 `requirements/source-type-registry.md`。
  - P1：`SUB_PROJECT_FACT_SOURCE_FILES` 加 `requirements/source-type-registry.md`。
  - P3：`ALL_TEMPLATE_FILES` 加 `contract-register-template.md`。
  - `SUB_PROJECT_DIRS` 加 `requirements/canonical`、`requirements/atoms`。
- `workspace_builder.py`：portfolio 模式对 `portfolio/` 级调用 `create_ri_skeleton`（参数化基路径）+ 创建 contract-register。
- `file_registry.py`：`create_ri_skeleton(ai_dir, base_path="requirements")` 参数化支持 portfolio 目标；新增 `create_contract_register()`；`generate_single_readme`/`generate_portfolio_readme` 目录树与事实源清单补 RI 与 contract-register（P5）。
- `migrate_workspace.py`：
  - 新增 `sub_project_dirs`/`sub_project_files` 键与遍历逻辑（D10 守卫：`_sub_projects()` 仅返回含 `requirements/` 的子项目）。
  - `create_missing_files` 子项目路径剥前缀后查 `template_map`（H1）；`template_map` 补 `portfolio/requirements/contract-register.md` 与 `portfolio/requirements/source-type-registry.md`（H2）。
  - 新增 0.8.0 条目：`new_dirs`（portfolio/requirements/{canonical,atoms}）、`new_files`（portfolio/requirements/contract-register.md、source-type-registry.md）、`sub_project_dirs`（requirements/canonical、requirements/atoms）、`sub_project_files`（requirements/source-type-registry.md）。
- `_version.py`：`SKILL_VERSION`→1.16.0；`WORKSPACE_SCHEMA_VERSION`→0.8.0。

## 八、契约层更新

- `SKILL.md`：§6 RI 路由行更新为四步路由；§8 ID 编码新增 `CON-` 前缀；§4 事实源表补 `portfolio/requirements/` 与 `contract-register.md`（两级）；description 补"合同登记/合同变更"触发词（G）。
- `skill.json`：schema current→0.8.0 + migrations 0.7.0→0.8.0；versionHistory + CAP（新增 contract_scope_ri 能力语义，扩展 cross_source_requirement_intelligence）。
- `skill-contract.md`：Fact Source 补 `portfolio/requirements/contract-register.md`、`portfolio/requirements/` 目录、`source-type-registry`（两级）；Protected Capabilities 的 RI 描述扩展合同作用域。
- `SKILL_BLUEPRINT.md`：§5.2 CAP 更新 + §7/§8 数据流 + §11.3 版本行（Blueprint Impact: full）。
- `CHANGELOG.md`：1.16.0 版本记录（含 Blueprint Impact: full）。

## 九、回归测试（Module 34 Contract Scope）

CS-001~017（见 CR-20260813-002 Test Cases）。既有用例影响：RI-012 复核（contract_refs 同步）、SK-1E（规则索引计数）、BP-003/008、VR-001（版本号）。阻断项：核心契约改动→全量既有 198 + 新增用例全通过。

## 十、边界与风险

- 边界：原始文档不入库；不引入向量检索；不动 08 号概念域 B；scope 结论仅辅助，以合同原文/法务为准。
- 风险：schema 迁移（低概高影，structure-only 缓解）；contract_refs 兼容（旧记录降级）；supplement 回溯依赖 parent_contract_id（必填校验）；子项目遍历误伤（D10 守卫）；冷启动空壳（最小字段+待确认）。
- 回滚：从 1.15.0 基线恢复 + schema 回 0.7.0 + 移除 0.8.0 迁移与新增目录。
