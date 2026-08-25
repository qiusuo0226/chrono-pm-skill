# Changelog

本文件记录 ChronoPM-Portfolio 的版本变更。版本号与 ChronoPM-Project 共用同一条版本线。

---

## 3.14.0 — 2026-08-25（版本锁步 · released）

> 与 Project 3.14.0 共用版本线。各项目 `project-info/budget.md`；里程碑口径改为 WP §8 关键阶段。禁止写入成员项目。workspace schema 0.15.0。

## 3.13.0 — 2026-08-24（版本锁步 · released）

> 与 Project 3.13.0 共用版本线。V-13 按时间窗归集各项目正常计划中的正常 WP（不按计划名）。集层技能缺口写入 `portfolio/reports/`。禁止写入成员项目。workspace schema 0.14.0。

## 3.12.0 — 2026-08-24（版本锁步 · released）

> 与 Project 3.12.0 共用版本线。待办 WP Ref 按单值聚合；缺/多值当脏数据不双计。禁止写入成员项目。workspace schema 0.14.0。

## 3.11.0 — 2026-08-24（版本锁步 · released）

> 与 Project 3.11.0 共用版本线。本包能力零改动。workspace schema 0.14.0。

## 3.10.0 — 2026-08-23（版本锁步 · released）

> 与 Project 3.10.0 共用版本线。集层对话日志懒建于 `portfolio/logs/`。查成员日志按管理路径推导，不加指针列。跨项目待办列表每行项目名+TD。外部工时表在集层只分析+V-9。workspace schema 0.14.0。

### Added
- `ops-log-template.md` / `ops-log-index-template.md`（集层路径）

### Changed
- 只读契约：`portfolio/logs/` 可写集层对话，禁止抄成员正文
- V-1 收编后按管理路径探测成员 ops index
- 待办聚合每行必须项目名 + TD 编号

## 3.9.0 — 2026-08-22（版本锁步 · released）

> 与 Project 3.9.0 共用版本线。只读归集各项目过程日志 index 与 pm-decisions 开放计数。禁止读成员 inbox。过程日志不当进度。workspace schema 0.14.0。

### Changed
- 未确认终态改读成员 `pm-decisions` 块 8
- 禁写清单 pending-changes → pm-decisions

## 3.8.0 — 2026-08-22（版本锁步 · released）

> 与 Project 3.8.0 共用版本线。新增 V-11 跨项目共享文件拆分、V-12 术语指针索引。V-3 人员聚合改读各项目待办 §0/§0.5 + `_index`（不再读 resource-register）。对外确认改白话，不对用户说「建议更新清单」（内部能力名 V-9 保留）。进入工作区扫 `projects/` 一级目录，新目录 ASK 收编，确认后自动刷 glossary-index；无后台盯盘。workspace schema 0.13.0（集层结构不加 backup 义务）。

### Added
- V-11 共享文件拆分：分析+归属建议，默认各放一份，不主动建议指针；只写 `portfolio/` 建议产物，永不写成员项目。模板 `shared-file-split-template.md`
- V-12 术语指针索引 `portfolio/context/glossary-index.md`（只存指针不存全文）。模板 `glossary-index-template.md`

### Changed
- V-3 / 05 号 / 集周报人力源改待办体系（`_index` §1 花名册 + 待办 §0.5；缩写读 `_index` §6）
- 待办未办结枚举删除「待评审」
- V-9 模板增加白话摘要段；跨项目能耗只读聚合各项目最新 §0.6

---

## 3.7.0 — 2026-08-21（版本锁步 · released）

> 与 Project 3.7.0 共用版本线。V-8 读 ledger 9 列（缺列 —；新旧指纹兼容）。实体进度从成员 WP §3b 聚合。禁令清单去掉 entity-registry。workspace schema 0.12.0。

## 3.6.0 — 2026-08-20（版本锁步 · released）

> 与 Project 3.6.0 共用版本线。V-8 优先读成员 `requirements/sources/{簇 ID}/`，未迁完兼容 `{type}-source/`。去重键不变。禁止写入成员拆解产物。

---

## 3.5.1 — 2026-08-20（版本锁步 · released）

> 与 Project 3.5.1 共用版本线。规则零改动。

---

## 3.5.0 — 2026-08-20（版本锁步 · released）

> 与 Project 3.5.0 共用版本线。成员项目新增 `wps/`（schema 0.10.0）。本包只读可先读成员 `wps/_index.md`；禁止写入成员 WP 文件。

---

## 3.4.0 — 2026-08-20（版本锁步 · released）

> 与 Project 3.4.0 共用版本线。04 号临时摘改为成员项目 todos §3。

---

## 3.3.0 — 2026-08-20（版本锁步 · released）

> 与 Project 3.3.0 共用版本线。`05-resource-shared-rules.md`：跨项目人员归并按中文名，不按 TD 缩写。

---

## 3.2.0 — 2026-08-20（版本锁步 · released）

> 与 ChronoPM-Project 3.2.0 共用版本线。本包规则零改动。

---

## 3.1.1 — 2026-08-20（版本锁步 · released）

> 与 ChronoPM-Project 3.1.1 共用版本线。本包规则/模板/只读契约零改动。补齐 `governance/migrations/upgrade-to-3.1.1.md` 指针（主包为准）。

### Added
- `governance/migrations/upgrade-to-3.1.1.md`：指向主包 upgrade 的指针文件。

### Changed
- 版本触点同步到 3.1.1。

---

## 3.1.0 — 2026-08-20（版本锁步 · released）

> 与 ChronoPM-Project 3.1.0 共用版本线。本包规则/模板/只读契约零改动。Project 侧 CR-A 为路径残留纠偏 + 日报路由补全；伴生包 04 号 L35 `reports/daily/` 只读引用随 CR-D 处置。

### Changed
- 版本触点同步：`VERSION` / `skill.json` / `SKILL.md` front matter → 3.1.0。

---

## 3.0.0 — 2026-08-19（初版 · released）

独立只读伴生 Skill。写归 ChronoPM-Project，读归本包。联邦结构 `ai/portfolio/` + `ai/projects/{名}/ai/`。只读契约五条；能力 V-1～V-10（动态感知、进度总览、人×项目、跨项目风险、集周报、门禁最小值、P&L、合同去重、建议更新清单、健康巡检）。无 init 脚本。旧 09 号项目集规则整文件迁入本包 references。skill schemaVersion 0.7.0；workspace schema 0.9.0。

### Added
- `SKILL.md` / `skill.json` / `VERSION`：viewer 模式，零事实源。
- `references/01`～`06`：只读边界、聚合查询、挂载感知、集周报、共享资源、版本健康。
- 模板：建议更新清单、集周报、项目索引（含可选「下级集工作区路径」，仅登记不参与本期聚合）。
