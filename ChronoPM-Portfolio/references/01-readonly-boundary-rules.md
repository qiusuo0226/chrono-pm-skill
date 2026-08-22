# 只读边界与写禁（V-9 / 落盘）

本规则是 ChronoPM-Portfolio 的硬契约。与 `SKILL.md` §4 / §9 只读五条同文，细则在此。

## 1. 写禁范围

| 路径 | 权限 | 说明 |
|------|------|------|
| `ai/projects/*/ai/**` | **只读** | 成员项目事实源。禁止创建、修改、删除、重命名、移动 |
| 业务目录（project-index「业务路径」） | **只读引用** | 不侵入，不建 `ai/` |
| `ai/portfolio/**` | 可写 | 仅索引指针与派生产物 |
| `ai/.skill-version.json` | 可写（集级） | 不得改成员项目 `.skill-version.json` |
| `ai/projects/` 一级目录名 | 不由本包创建 | 挂载由集经理解压完成；本包只发现与提示登记 |

禁止行为（发现即停止该动作并改输出内部 V-9；对外白话，不对用户说「建议更新清单」）：

1. 改成员项目 todos（含 `_index.md` / 个人待办）/ PLAN / risk-register / issue-register / resource-register / transfer-log / contract-register / pm-decisions / 日报周报原文。
2. 在成员项目 `ai/` 内建文件「方便汇总」。
3. 把集层聚合结果写回成员项目。
4. 代写他项目待办（含镜像、抄送、同步完成状态）。
5. 静默同步 pm-profile / domain-glossary 跨项目副本（entity-registry 已于 v3.7.0 废弃，无此项）。

AUTO 级联在本包**不存在**。任何本应写入成员项目的动作一律 SUGGEST → 内部 V-9。V-11 同样只写 `portfolio/` 建议产物，永不写成员项目。

## 2. 可写清单（仅 portfolio/）

| 文件 | 性质 | 约束 |
|------|------|------|
| `portfolio/context/project-index.md` | 指针索引 | 登记须确认；不含进度/成本/待办实体 |
| `portfolio/context/glossary-index.md` | 指针索引 | V-12：只存术语指针，不存全文/释义 |
| `portfolio/reports/**` | 派生产物 | 必须 `generated_from` + `updated` + stale；不得当后续查询数据源 |
| `portfolio/resources/shared-resource-index.md` | 指针索引 | 仅姓名 + 参与项目指针 + 共享状态导航字段；禁止落盘排期/可用性数值 |
| `portfolio/resources/transfer-index.md` | 指针索引 | 仅 Transfer ID + 方向 + 日期指针 |
| `portfolio/logs/` | 集层操作日志 | 本包自身动作，不写成员项目 Change Log |
| 建议更新清单落盘（内部 V-9） | 派生产物 | 建议本身不是事实源。对外白话，不对用户说「建议更新清单」 |
| V-11 共享文件拆分产物 | 派生产物 | **只写 `portfolio/` 建议产物**（拆分方案 / 内部 V-9 清单），**永不写成员项目**。用户要求「直接写入」仍拒绝，提示换对应项目 ChronoPM-Project 对话 |

禁止在 `portfolio/` 建 todos / plans / risks / issues / requirements 事实源目录。集层 `requirements/` 若存量遗留，只读指针，不新增实体。

## 3. 建议更新清单（V-9，内部能力名）

当集经理意图变更成员项目实体（改待办、关风险、调人、改预算、补登记等），本包：

1. 停止写入。
2. 按 `assets/templates/suggested-update-list-template.md` 输出：对外「白话摘要」，对内表留痕。
3. 对外告知到对应项目对话执行（白话，不念路径/内部编号）。禁止对用户说「建议更新清单」六字。

V-11 拆分方案确认后，也走本条：只把建议产物写在 `portfolio/`，不写成员项目。

每条必填：

| 字段 | 要求 |
|------|------|
| 目标项目 | project-index 的项目名称或 PRJ-NNN |
| 目标文件 | 相对该项目 `ai/` 的路径，如 `todos/2026-08-19/张三.md` |
| 建议内容 | 可执行的具体改动（字段/行/状态），禁止空泛「请关注」 |
| 理由与来源 | 触发证据（查询结果、周报摘录、漂移比对） |
| 优先级 | P0 / P1 / P2 |

同一流程多条 SUGGEST 合并为一份清单，流程末尾一次输出。清单可只对话输出，或经确认后写入 `portfolio/reports/suggested-updates/YYYYMMDD.md`（仍是派生产物）。

**禁止**：清单输出后「顺手改一下」成员项目；禁止把清单当已执行。

## 4. 聚合产物落盘规则

| 产物类型 | 可否落盘 | 规则 |
|----------|----------|------|
| 人的视图、进度总览、门禁、P&L、风险聚合、合同全景、待办矩阵 | **禁止** | 查询时现算 |
| 集周报、专项报告快照 | 允许 | 仅当期报告 |
| project-index / 指针索引 | 允许 | 不含聚合数值 |

落盘报告 YAML 头或文首必须含：

```yaml
generated_from:
  - ai/projects/{名}/ai/reports/weekly/YYYY/YYYY-Wxx.md
  - ...
updated: YYYY-MM-DDTHH:MM
stale_after: YYYY-MM-DD   # 或规则名，见下
```

**stale 判定**（命中任一即过期）：

1. 任一 `generated_from` 源文件修改时间晚于 `updated`。
2. 周报：所属 ISO 周结束后满 7 天。
3. 其他快照：超过 24 小时，或本次会话集经理要求「刷新」。

过期报告：查询不得当数据源；必须重算或标注「过期快照，以下为实时聚合」。禁止用过期快照更新索引数值。

## 5. 零事实源强化

- 共享人力可用性、排期冲突、人力配置率 = 动态视图，禁止写入 shared-resource-index。
- 跨项目风险完整实体在主归属项目 risk-register；集层不存风险实体。
- 合同/招投标/立项拆解产物在各项目 `requirements/sources/{编号}/`（未迁完可读 `{type}-source/`）；集层不另存登记册事实源。
- 里程碑 = 各项目 PLAN 中 `is_milestone: true` 的 WP；集层不存里程碑板。
