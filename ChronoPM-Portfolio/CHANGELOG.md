# Changelog

本文件记录 ChronoPM-Portfolio 的版本变更。版本号与 ChronoPM-Project 共用同一条版本线。

---

## 3.0.0 — 2026-08-19（初版 · released）

独立只读伴生 Skill。写归 ChronoPM-Project，读归本包。联邦结构 `ai/portfolio/` + `ai/projects/{名}/ai/`。只读契约五条；能力 V-1～V-10（动态感知、进度总览、人×项目、跨项目风险、集周报、门禁最小值、P&L、合同去重、建议更新清单、健康巡检）。无 init 脚本。旧 09 号项目集规则整文件迁入本包 references。skill schemaVersion 0.7.0；workspace schema 0.9.0。

### Added
- `SKILL.md` / `skill.json` / `VERSION`：viewer 模式，零事实源。
- `references/01`～`06`：只读边界、聚合查询、挂载感知、集周报、共享资源、版本健康。
- 模板：建议更新清单、集周报、项目索引（含可选「下级集工作区路径」，仅登记不参与本期聚合）。
